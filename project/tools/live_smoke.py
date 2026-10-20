"""One bounded real feedback request using synthetic, shareable answer content."""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from project.backend.app.feedback import AnswerRequest, assess
from project.backend.app.llm import ModelError

started = time.monotonic()
result = {"input_origin": "synthetic test content, not a student's personal history"}
try:
    feedback = assess(AnswerRequest(question="Tell me about a time you solved a problem.",
        answer="In a course project, our form lost typed input after a validation error. I reproduced it, kept draft state separate from validation, and tested an empty submission. The draft then remained visible when validation failed."))
    result.update(outcome="validated", feedback=feedback.model_dump())
except ModelError as error:
    result.update(outcome="failed", error=str(error))
result["elapsed_ms"] = round((time.monotonic() - started) * 1000)
result["timestamp"] = datetime.now(timezone.utc).isoformat()
path = REPO / "docs/evidence/live-feedback.json"
path.parent.mkdir(parents=True, exist_ok=True)
history = path.with_name("feedback-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
history.write_text(json.dumps(result, indent=2), encoding="utf-8")
path.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
