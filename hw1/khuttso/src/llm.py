"""One OpenRouter request per invocation, with sanitized usage logging."""

from dataclasses import dataclass, field
from decimal import Decimal, DecimalException, InvalidOperation
from http.client import HTTPException
import json
import time
from typing import Callable, Mapping, TextIO
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_TIMEOUT_SECONDS = 20
MAX_RESPONSE_BYTES = 1_048_576


class CoachError(Exception):
    """An error whose message is safe to show in the CLI."""


def _price(value: str | None) -> Decimal | None:
    if value is None:
        return None
    try:
        price = Decimal(value)
    except InvalidOperation:
        return None
    return price if price.is_finite() and price >= 0 else None


@dataclass(frozen=True)
class Settings:
    api_key: str = field(repr=False)
    model: str
    input_price: Decimal | None = None
    output_price: Decimal | None = None

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> "Settings":
        key = environment.get("OPENROUTER_API_KEY", "").strip()
        model = environment.get("OPENROUTER_MODEL", "").strip()
        if not key or not model:
            raise CoachError("Set OPENROUTER_API_KEY and OPENROUTER_MODEL before generating questions.")
        if any(ord(char) < 32 or ord(char) == 127 for char in key + model):
            raise CoachError("The API key or model configuration contains invalid control characters.")
        if not key.isascii():
            raise CoachError("The API key configuration must contain ASCII characters only.")
        return cls(
            key,
            model,
            _price(environment.get("OPENROUTER_INPUT_USD_PER_MILLION")),
            _price(environment.get("OPENROUTER_OUTPUT_USD_PER_MILLION")),
        )


class _NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward an Authorization header to a redirected destination.
        return None


def send_request(request: Request, timeout: float) -> bytes:
    """Production transport. Tests replace this function with a local fake."""
    with build_opener(_NoRedirects()).open(request, timeout=timeout) as response:
        body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise CoachError("The provider response was too large. Try again manually.")
    return body


def _reject_constant(value: str):
    raise ValueError("Non-finite numbers are not valid JSON.")


def _token_count(usage: object, name: str) -> int | str:
    value = usage.get(name) if isinstance(usage, dict) else None
    return value if type(value) is int and value >= 0 else "unavailable"


def _usage_log(usage: object, settings: Settings) -> dict:
    prompt = _token_count(usage, "prompt_tokens")
    completion = _token_count(usage, "completion_tokens")
    cost = "unavailable"
    if (
        isinstance(prompt, int)
        and isinstance(completion, int)
        and settings.input_price is not None
        and settings.output_price is not None
    ):
        try:
            cost = str(
                (Decimal(prompt) * settings.input_price + Decimal(completion) * settings.output_price)
                / Decimal(1_000_000)
            )
        except DecimalException:
            # Unusable optional pricing must not hide a completed request.
            cost = "unavailable"
    return {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": _token_count(usage, "total_tokens"),
        "estimated_cost_usd": cost,
    }


class OpenRouterClient:
    def __init__(
        self,
        settings: Settings,
        log_stream: TextIO,
        transport: Callable[[Request, float], bytes] | None = None,
    ):
        self.settings = settings
        self.log_stream = log_stream
        self.transport = transport if transport is not None else send_request

    def complete_json(self, messages: list[dict[str, str]], validator: Callable):
        payload = {
            "model": self.settings.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "provider": {"require_parameters": True, "allow_fallbacks": False},
            "max_tokens": 1200,
            "stream": False,
        }
        request = Request(
            ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + self.settings.api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        start = time.perf_counter()
        outcome = "provider_error"
        usage = None
        try:
            body = self.transport(request, REQUEST_TIMEOUT_SECONDS)
            outcome = "invalid_output"
            try:
                response = json.loads(body, parse_constant=_reject_constant)
            except (ValueError, UnicodeError, RecursionError):
                raise CoachError("The provider returned unreadable JSON. Try again manually.") from None
            if not isinstance(response, dict):
                raise CoachError("The provider returned an invalid response. Try again manually.")
            usage = response.get("usage")
            if "error" in response:
                outcome = "provider_error"
                raise CoachError("The provider could not complete the request. Try again manually.")
            try:
                choice = response["choices"][0]
                if choice.get("finish_reason") != "stop":
                    raise CoachError("The model did not finish its response. Try again manually.")
                content = choice["message"]["content"]
                if not isinstance(content, str):
                    raise ValueError("Missing text content.")
                value = json.loads(content, parse_constant=_reject_constant)
            except (KeyError, IndexError, TypeError, AttributeError, ValueError, RecursionError):
                raise CoachError("The model returned unreadable questions. Try again manually.") from None
            result = validator(value)
            outcome = "success"
            return result
        except HTTPError as error:
            status = error.code
            error.close()
            raise CoachError(f"The provider returned HTTP {status}. Try again manually.") from None
        except TimeoutError:
            outcome = "timeout"
            raise CoachError("The model request timed out after 20 seconds. Try again manually.") from None
        except URLError as error:
            if isinstance(error.reason, TimeoutError):
                outcome = "timeout"
                raise CoachError("The model request timed out after 20 seconds. Try again manually.") from None
            raise CoachError("Could not connect to the model provider. Try again manually.") from None
        except (OSError, HTTPException):
            raise CoachError("The model connection failed. Try again manually.") from None
        finally:
            event = {
                "event": "model_call",
                "model": self.settings.model,
                "outcome": outcome,
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                **_usage_log(usage, self.settings),
            }
            print(json.dumps(event), file=self.log_stream)
