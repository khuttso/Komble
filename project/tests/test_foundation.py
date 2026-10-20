"""Check the real public API and its starter content without any provider."""

from fastapi.testclient import TestClient

from project.backend.app.main import app


def test_health_never_exposes_environment_secrets(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "must-never-be-returned")
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "InterviewCoach", "stage": "local-prototype"}
    assert "must-never-be-returned" not in response.text


def test_library_has_distinct_packs_and_question_ids():
    with TestClient(app) as client:
        response = client.get("/api/packs")
    assert response.status_code == 200
    packs = response.json()
    assert len(packs) >= 3
    assert len({pack["id"] for pack in packs}) == len(packs)
    questions = [question for pack in packs for question in pack["questions"]]
    assert len({question["id"] for question in questions}) == len(questions)
    for pack in packs:
        assert pack["title"].strip() and pack["role"].strip()
        assert pack["tags"] and pack["questions"]
        assert all(question["text"].strip() for question in pack["questions"])


def test_unknown_routes_do_not_return_fake_success():
    with TestClient(app) as client:
        assert client.get("/api/does-not-exist").status_code == 404
        assert client.post("/api/feedback", json={"answer": "example"}).status_code == 422


def test_api_disables_response_caching():
    with TestClient(app) as client:
        response = client.get("/api/packs")
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
