"""One dispatcher for both doors: availability, validation, trusted caller context."""
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import ValidationError

from .tools import TOOLS, ToolFailure, tools_for

_lock = threading.Lock()


def call_tool(call: dict, allowed=None, caller: str | None = None) -> dict:
    started = time.perf_counter()
    name = call.get("name")
    available = tools_for(caller) if allowed is None else allowed
    tool = available.get(name) if isinstance(name, str) else None
    result = None
    error = None
    reason = "ok"
    if tool is None:
        reason, error = "not_offered", "This tool is not available. Choose a tool from the offered list."
    else:
        try:
            raw = call.get("arguments", {})
            if isinstance(raw, str):
                if len(raw) > 4096:
                    raise ValueError("oversized")
                raw = json.loads(raw)
            args = tool.args.model_validate(raw)
        except (ValidationError, ValueError, TypeError):
            reason = "invalid_arguments"
            error = ("Invalid arguments: use pack_id frontend, support or graduate and an integer "
                     "limit from 1 to 4. Remove all other fields, including identity fields.")
        else:
            try:
                result = tool.run(args).model_dump(mode="json")
            except ToolFailure as failure:
                reason, error = "unavailable", str(failure)
            except Exception:
                reason = "internal_error"
                error = "The tool is temporarily unavailable. Ask the maintainer to check it before retrying."
    event = {"timestamp": datetime.now(timezone.utc).isoformat(),
             "tool": name if isinstance(name, str) and name in TOOLS else "unknown",
             "outcome": reason, "elapsed_ms": round((time.perf_counter() - started) * 1000)}
    path = Path(os.environ.get("INTERVIEWCOACH_TOOL_LOG",
                str(Path(__file__).resolve().parents[1] / "logs/runtime/tools.jsonl")))
    try:
        with _lock:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(event) + "\n")
    except OSError:
        return {"ok": False, "error": "Tool audit logging is unavailable. Ask the maintainer to restore it before retrying."}
    return {"ok": False, "error": error} if error else {"ok": True, "result": result}
