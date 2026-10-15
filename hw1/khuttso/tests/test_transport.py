"""Verify the real HTTP adapter without sending any network requests."""
import io
from urllib.error import HTTPError
from urllib.request import Request

import pytest

import llm


def test_default_client_uses_production_transport(monkeypatch):
    calls = []

    def fake(request, timeout):
        calls.append((request, timeout))
        return b'{"choices":[{"finish_reason":"stop","message":{"content":"{}"}}]}'

    monkeypatch.setattr(llm, "send_request", fake)
    stream = io.StringIO()
    client = llm.OpenRouterClient(llm.Settings("test-key", "test/model"), stream)
    assert client.complete_json([], lambda value: value) == {}
    assert len(calls) == 1 and calls[0][1] == 20


@pytest.mark.parametrize("too_large", [False, True])
def test_http_adapter_bounds_response_size_and_closes_response(monkeypatch, too_large):
    body = b"x" * (llm.MAX_RESPONSE_BYTES + 1) if too_large else b"{}"
    response = io.BytesIO(body)
    observed = {}

    class FakeOpener:
        def open(self, request, *, timeout):
            observed.update(request=request, timeout=timeout)
            return response

    def fake_opener(handler):
        assert isinstance(handler, llm.HTTPRedirectHandler)
        return FakeOpener()

    monkeypatch.setattr(llm, "build_opener", fake_opener)
    request = Request(llm.ENDPOINT)
    if too_large:
        with pytest.raises(llm.CoachError, match="too large"):
            llm.send_request(request, 20)
    else:
        assert llm.send_request(request, 20) == body
    assert observed == {"request": request, "timeout": 20}
    assert response.closed


def test_redirect_never_receives_authorization_header():
    request = Request(llm.ENDPOINT, headers={"Authorization": "Bearer synthetic-test-key"})
    handler = llm._NoRedirects()
    assert handler.redirect_request(request, None, 302, "Moved", {}, "https://other.invalid/") is None


def test_http_error_response_is_closed_and_logged(monkeypatch):
    body = io.BytesIO(b"private-provider-body")

    def fake(request, timeout):
        raise HTTPError(llm.ENDPOINT, 503, "private-provider-body", {}, body)

    stream = io.StringIO()
    client = llm.OpenRouterClient(llm.Settings("test-key", "test/model"), stream, fake)
    with pytest.raises(llm.CoachError, match="HTTP 503"):
        client.complete_json([], lambda value: value)
    assert body.closed and "private-provider-body" not in stream.getvalue()


def test_settings_repr_never_includes_api_key():
    assert "synthetic-secret-key" not in repr(llm.Settings("synthetic-secret-key", "test/model"))
