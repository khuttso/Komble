import io
import json

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from project.backend.app import index, llm, main
from project.backend.app.extraction import Extraction, decide, prepare_image, extract as extract_advert
from project.backend.app.feedback import AnswerRequest, Feedback, assess
from project.backend.app.grounding import GroundedReply, answer, check_citations
from project.backend.app.llm import ModelError, ModelGateway


def extraction(**changes):
    data = {"applicable": True,
            "role_title": {"value": "Junior Developer", "evidence": "Junior Developer", "confidence": 0.95},
            "seniority": {"value": "Junior", "evidence": "Junior Developer", "confidence": 0.95},
            "requirements": {"value": ["Python"], "evidence": "Skills: Python", "confidence": 0.95}}
    data.update(changes)
    return Extraction.model_validate(data)


def test_clean_extraction_accepts_supported_fields():
    decision = decide(extraction())
    assert decision["route"] == "accept"
    assert decision["fields"]["role_title"] == "Junior Developer"


def test_degraded_missing_evidence_never_prefills_a_guess():
    result = decide(extraction(role_title={"value": "Invented title", "evidence": None, "confidence": 0.99}))
    assert result["route"] == "review"
    assert result["fields"]["role_title"] is None
    assert result["reasons"]


def test_uncertain_fields_require_confirmation_and_are_empty():
    result = decide(extraction(role_title={"value": "Junior Developer", "evidence": "Junior Developer", "confidence": 0.5}))
    assert result["route"] == "confirm"
    assert result["fields"]["role_title"] is None


def test_non_advert_rejects_all_values():
    result = decide(extraction(applicable=False))
    assert result["route"] == "reject"
    assert all(value is None for value in result["fields"].values())


def test_conflicting_value_and_evidence_requires_review():
    result = decide(extraction(role_title={"value": "Senior Engineer", "evidence": "Junior Developer", "confidence": 1.0}))
    assert result["route"] == "review"


def test_images_are_downscaled_and_invalid_content_rejected():
    stream = io.BytesIO()
    Image.new("RGB", (2400, 1200), "white").save(stream, "PNG")
    prepared = prepare_image(stream.getvalue())
    with Image.open(io.BytesIO(prepared)) as image:
        assert image.size == (1024, 512)
        assert image.format == "JPEG"
        assert not image.getexif()
    with pytest.raises(ModelError):
        prepare_image(b"not an image")
    with pytest.raises(ModelError):
        prepare_image(b"x" * (2 * 1024 * 1024 + 1))


@pytest.mark.parametrize("question,answer_text", [("Question?", "   "), (" ", "Answer"), ("Question?", "x" * 3001)])
def test_invalid_answers_never_call_feedback(monkeypatch, question, answer_text):
    def forbidden(_):
        pytest.fail("Invalid input reached model service")
    monkeypatch.setattr(main, "assess", forbidden)
    with TestClient(main.app) as client:
        assert client.post("/api/feedback", json={"question": question, "answer": answer_text}).status_code == 422


def test_feedback_uses_current_custom_question():
    class Client:
        def complete_json(self, operation, instructions, content, schema):
            assert content == {"question": "Custom question?", "answer": "Real example"}
            assert "untrusted" in instructions
            return Feedback(strengths="Specific example", improvements="Add the outcome", suggestion="Describe what changed")
    result = assess(AnswerRequest(question=" Custom question? ", answer=" Real example "), Client())
    assert result.suggestion


def test_invented_citation_and_uncited_sentences_are_rejected():
    assert not check_citations(GroundedReply(answer="Claim [99].", citations=[99], grounded=True), 2)
    assert not check_citations(GroundedReply(answer="Claim [1]. Another claim.", citations=[1], grounded=True), 2)
    assert not check_citations(GroundedReply(answer="Claim.", citations=[], grounded=True), 2)
    assert check_citations(GroundedReply(answer="Claim. [1]", citations=[1], grounded=True), 2)
    assert not check_citations(GroundedReply(answer="Claim. [1] Another claim.", citations=[1], grounded=True), 2)


def test_low_score_refuses_before_generation():
    class Client:
        def complete_json(self, *args):
            pytest.fail("Low score reached generation")
    result = answer("Unsupported question", client=Client(), retrieve_fn=lambda *args, **kwargs: [{"score": 0.1}])
    assert not result["grounded"] and result["reason"] == "below_threshold"


def test_answer_maps_marker_to_correct_document():
    class Client:
        def complete_json(self, *args):
            return GroundedReply(answer="Use your own contribution [2].", citations=[2], grounded=True)
    hits = [{"score": 0.9, "document": "first.md", "text": "First passage"},
            {"score": 0.8, "document": "second.md", "text": "Second passage"}]
    result = answer("Question", client=Client(), retrieve_fn=lambda *args, **kwargs: hits)
    assert result["grounded"] and result["citations"][0]["document"] == "second.md"
    assert result["citations"][0]["excerpt"] == "Second passage"


def test_bad_generated_citation_causes_refusal():
    class Client:
        def complete_json(self, *args):
            return GroundedReply(answer="Invented [7].", citations=[7], grounded=True)
    result = answer("Question", client=Client(), retrieve_fn=lambda *args, **kwargs: [{"score": 0.9, "document": "real.md", "text": "Real"}])
    assert not result["grounded"] and result["reason"] == "invalid_citations_or_ungrounded"


def test_different_embedding_model_index_is_refused(tmp_path, monkeypatch):
    path = tmp_path / "index.json"
    path.write_text(json.dumps({"model": "different", "corpus_hash": "old", "chunks": []}))
    monkeypatch.setattr(index, "INDEX_PATH", path)
    with pytest.raises(ModelError):
        index.load()


def test_free_only_gateway_blocks_paid_models_before_post(monkeypatch):
    monkeypatch.setattr(llm, "setting", lambda name, default="": {"OPENROUTER_API_KEY": "fake", "INTERVIEWCOACH_FREE_ONLY": "true", "OPENROUTER_TEXT_MODEL": "paid/model"}.get(name, default))
    def handler(request):
        assert request.method == "GET", "Paid generation must never be sent"
        return httpx.Response(200, json={"data": [{"id": "paid/model", "pricing": {"prompt": "0.1", "completion": "0.1"}}]})
    client = ModelGateway(httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(ModelError):
        client.complete_json("feedback", "instructions", {}, Feedback)


def test_provider_failure_has_no_retry_or_secret_leak(monkeypatch):
    monkeypatch.setattr(llm, "setting", lambda name, default="": {"OPENROUTER_API_KEY": "private-fake-key", "INTERVIEWCOACH_FREE_ONLY": "true"}.get(name, default))
    posted = []
    def handler(request):
        if request.method == "GET":
            return httpx.Response(200, json={"data": [{"id": "test/model:free", "pricing": {"prompt": "0", "completion": "0"}, "supported_parameters": ["structured_outputs"]}]})
        posted.append(request)
        return httpx.Response(429, json={"error": "private answer private-fake-key"})
    client = ModelGateway(httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(ModelError) as caught:
        client.complete_json("feedback", "instructions", {}, Feedback)
    assert len(posted) == 1
    assert "429" in str(caught.value) and "private" not in str(caught.value)


def test_timeout_is_readable_and_not_retried(monkeypatch):
    monkeypatch.setattr(llm, "setting", lambda name, default="": "fake" if name == "OPENROUTER_API_KEY" else default)
    client = ModelGateway()
    monkeypatch.setattr(client, "_select", lambda image: "test/model:free")
    def timeout(*args, **kwargs):
        raise httpx.ReadTimeout("private request")
    monkeypatch.setattr(client.http, "post", timeout)
    with pytest.raises(ModelError) as caught:
        client.complete_json("feedback", "instructions", {}, Feedback)
    assert caught.value.status == 504 and "private" not in str(caught.value)


def test_free_suffix_does_not_override_nonzero_pricing(monkeypatch):
    monkeypatch.setattr(llm, "setting", lambda name, default="": "fake" if name == "OPENROUTER_API_KEY" else default)
    def handler(request):
        assert request.method == "GET", "Nonzero pricing must block generation"
        return httpx.Response(200, json={"data": [{"id": "test/model:free", "pricing": {"prompt": "0", "completion": "0", "image": "0.01"}, "supported_parameters": ["structured_outputs"]}]})
    client = ModelGateway(httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(ModelError):
        client.complete_json("feedback", "instructions", {}, Feedback)


def test_malformed_model_json_is_not_displayed_or_retried(monkeypatch):
    monkeypatch.setattr(llm, "setting", lambda name, default="": "fake" if name == "OPENROUTER_API_KEY" else default)
    posted = []
    def handler(request):
        posted.append(request)
        return httpx.Response(200, json={"choices": [{"finish_reason": "stop", "message": {"content": "private broken JSON"}}]})
    client = ModelGateway(httpx.Client(transport=httpx.MockTransport(handler)))
    monkeypatch.setattr(client, "_select", lambda image: "test/model:free")
    with pytest.raises(ModelError) as caught:
        client.complete_json("feedback", "instructions", {}, Feedback)
    assert len(posted) == 1 and "private" not in str(caught.value)


def test_api_provider_error_is_readable_and_does_not_echo_answer(monkeypatch):
    def unavailable(request):
        raise ModelError("The free provider is unavailable; retry manually.", 502)
    monkeypatch.setattr(main, "assess", unavailable)
    with TestClient(main.app) as client:
        response = client.post("/api/feedback", json={"question": "Question?", "answer": "private synthetic answer"})
    assert response.status_code == 502
    assert "retry manually" in response.json()["error"]
    assert "private synthetic answer" not in response.text


def test_changed_vector_dimensions_refuse_index_load(tmp_path, monkeypatch):
    path = tmp_path / "index.json"
    path.write_text(json.dumps({"model": index.EMBEDDING_MODEL, "corpus_hash": index.corpus_hash([]), "dimension": 3, "chunks": [{"vector": [1.0, 0.0]}]}))
    monkeypatch.setattr(index, "INDEX_PATH", path)
    monkeypatch.setattr(index, "documents", lambda: [])
    with pytest.raises(ModelError):
        index.load()


def test_mixed_seniority_evidence_confirms_even_with_high_confidence():
    result = decide(extraction(role_title={"value": "Junior / Senior Developer", "evidence": "Junior / Senior Developer", "confidence": 1.0}))
    assert result["route"] == "confirm"
    assert result["fields"]["role_title"] is None


def test_extraction_response_has_field_confidence_without_leaking_a_guess():
    class Client:
        def complete_json(self, *args, **kwargs):
            return extraction(role_title={"value": "UnsafeGuess", "evidence": None, "confidence": 0.99})
    stream = io.BytesIO()
    Image.new("RGB", (40, 40), "white").save(stream, "PNG")
    result = extract_advert(stream.getvalue(), Client())
    assert result["fields"]["role_title"] == {"value": None, "evidence": None, "confidence": 0.99}
    assert "UnsafeGuess" not in json.dumps(result)
    assert result["decision"]["route"] == "review"
