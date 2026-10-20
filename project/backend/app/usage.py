"""Allowlisted operational evidence: never log inputs or provider response bodies."""

import json
import threading
from datetime import datetime, timezone

from .config import REPO

_lock = threading.Lock()


def log_event(operation: str, **fields):
    allowed = {"outcome", "reason", "model", "elapsed_ms", "tokens_in", "tokens_out",
               "cost_usd", "usage", "count", "provider_status", "finish_reason", "k", "threshold"}
    event = {"timestamp": datetime.now(timezone.utc).isoformat(), "operation": operation}
    event.update({key: value for key, value in fields.items() if key in allowed})
    path = REPO / "logs" / "runtime" / "events.jsonl"
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, allow_nan=False) + "\n")
