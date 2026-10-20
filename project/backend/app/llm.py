"""Single logged gateway: free OpenRouter generation and local CPU embeddings."""

import base64
import json
import math
import threading
import time
from decimal import Decimal, InvalidOperation
from functools import lru_cache

import httpx
from pydantic import BaseModel, ValidationError

from .config import EMBEDDING_MODEL, RUNTIME, setting
from .usage import log_event


class ModelError(Exception):
    def __init__(self, message: str, status: int = 503):
        super().__init__(message)
        self.status = status


@lru_cache(maxsize=1)
def embedding_engine():
    from fastembed import TextEmbedding
    return TextEmbedding(model_name=EMBEDDING_MODEL, cache_dir=str(RUNTIME / "models"), threads=2)


class ModelGateway:
    def __init__(self, http=None):
        self.http = http or httpx.Client(timeout=20, follow_redirects=False)
        self.catalog = None
        self.catalog_time = 0.0
        self.calls = 0
        self.lock = threading.Lock()

    def _select(self, image: bool) -> str:
        if setting("INTERVIEWCOACH_FREE_ONLY", "true").lower() != "true":
            raise ModelError("This app is authorized for free models only. Set INTERVIEWCOACH_FREE_ONLY=true.")
        if self.catalog is None or time.monotonic() - self.catalog_time > 300:
            response = self.http.get("https://openrouter.ai/api/v1/models")
            response.raise_for_status()
            self.catalog = response.json()["data"]
            self.catalog_time = time.monotonic()
        configured = setting("OPENROUTER_VISION_MODEL" if image else "OPENROUTER_TEXT_MODEL")
        candidates = []
        for item in self.catalog:
            model_id = item.get("id", "")
            if not model_id.endswith(":free") or (configured and configured != model_id):
                continue
            pricing = item.get("pricing", {})
            try:
                # Reject missing or nonzero text pricing and any nonzero ancillary charge.
                if any(Decimal(str(pricing[key])) != 0 for key in ("prompt", "completion")):
                    continue
                if any(Decimal(str(value)) != 0 for value in pricing.values()):
                    continue
            except (KeyError, InvalidOperation, TypeError):
                continue
            supported = item.get("supported_parameters", [])
            if "structured_outputs" not in supported:
                continue
            if image and "image" not in item.get("architecture", {}).get("input_modalities", []):
                continue
            candidates.append(model_id)
        if not candidates:
            raise ModelError("No compatible zero-price model was found. Check the configured free model and its structured-output/image support.")
        return sorted(candidates)[0]

    def complete_json(self, operation: str, instructions: str, content: dict,
                      schema: type[BaseModel], image: bytes | None = None):
        started = time.monotonic()
        model = "unselected"
        outcome = "failed"
        usage = {}
        status = None
        reason = "configuration"
        finish_reason = None
        try:
            key = setting("OPENROUTER_API_KEY")
            if not key:
                raise ModelError("AI is not configured. Add OPENROUTER_API_KEY to project/.env, then try again. Your input is still here.")
            model = self._select(image is not None)
            parameters = next(item.get("supported_parameters", []) for item in self.catalog if item["id"] == model) if self.catalog else []
            user_content = [{"type": "text", "text": json.dumps(content)}]
            if image is not None:
                encoded = base64.b64encode(image).decode("ascii")
                user_content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + encoded}})
            with self.lock:
                if self.calls >= 24:
                    raise ModelError("The local 24-call safety limit has been reached. Review usage before restarting the app.")
                self.calls += 1
            reason = "provider"
            response = self.http.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": "Bearer " + key},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": user_content if image else json.dumps(content)},
                    ],
                    "response_format": {"type": "json_schema", "json_schema": {
                        "name": schema.__name__, "strict": True, "schema": schema.model_json_schema()}},
                    "max_tokens": 1000,
                    **({"reasoning": {"enabled": False}} if "reasoning" in parameters else {}),
                    "stream": False,
                    "provider": {"allow_fallbacks": False, "require_parameters": True},
                },
            )
            status = response.status_code
            if status != 200:
                raise ModelError(f"The free AI provider could not complete this request (HTTP {status}). Your input is preserved; retry manually later.", 502)
            body = response.json()
            usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
            choice = body["choices"][0]
            reason = "invalid_output"
            finish_reason = choice.get("finish_reason") if choice.get("finish_reason") in ("stop", "length", "content_filter", "tool_calls") else "other"
            if choice.get("finish_reason") != "stop":
                reason = "truncated" if finish_reason == "length" else "invalid_output"
                raise ModelError("The model did not finish a usable response. Your input is preserved; retry manually.", 502)
            result = schema.model_validate_json(choice["message"]["content"])
            outcome, reason = "success", "validated"
            return result
        except httpx.TimeoutException:
            reason = "timeout"
            raise ModelError("The AI request timed out. Your input is still here; retry manually.", 504) from None
        except (httpx.HTTPError, ValueError, KeyError, IndexError, TypeError, AttributeError, ValidationError):
            raise ModelError("The AI service returned an unavailable or unusable response. Your input is still here.", 502) from None
        finally:
            def number(key):
                value = usage.get(key)
                return value if isinstance(value, (int, float)) and math.isfinite(value) else None
            log_event(operation, model=model, outcome=outcome, reason=reason,
                      provider_status=status, finish_reason=finish_reason, elapsed_ms=round((time.monotonic() - started) * 1000),
                      tokens_in=number("prompt_tokens"), tokens_out=number("completion_tokens"),
                      cost_usd=number("cost"), usage="reported" if usage else "unavailable")

    def embed(self, texts: list[str], *, query=False) -> list[list[float]]:
        started = time.monotonic()
        outcome = "failed"
        try:
            engine = embedding_engine()
            vectors = list(engine.query_embed(texts) if query else engine.passage_embed(texts))
            outcome = "success"
            return [vector.tolist() for vector in vectors]
        finally:
            log_event("embedding_query" if query else "embedding_index", model=EMBEDDING_MODEL,
                      outcome=outcome, elapsed_ms=round((time.monotonic() - started) * 1000),
                      count=len(texts), cost_usd=0, tokens_in=None, tokens_out=None,
                      usage="local_cpu_no_provider_tokens")


gateway = ModelGateway()
