"""One real request for each synthetic fixture; retain every outcome."""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from project.backend.app.extraction import extract
from project.backend.app.llm import ModelError

results = []
for name in ("clean", "degraded", "ambiguous", "not-applicable"):
    started = time.monotonic()
    try:
        result = extract((REPO / f"project/tests/images/{name}.jpg").read_bytes())
        route = result["decision"]["route"]
        passed = route == "accept" if name == "clean" else route in ("confirm", "review") if name in ("degraded", "ambiguous") else route == "reject"
        record = {"fixture": name, "passed": passed, "result": result}
    except ModelError as error:
        record = {"fixture": name, "passed": False, "error": str(error)}
    record["elapsed_ms"] = round((time.monotonic() - started) * 1000)
    results.append(record)
    print(f"{name}: {'PASS' if record['passed'] else 'FAIL'} ({record['elapsed_ms']} ms)", flush=True)
timestamp = datetime.now(timezone.utc)
path = REPO / ("docs/evidence/images-" + timestamp.strftime("%Y%m%dT%H%M%SZ") + ".json")
path.write_text(json.dumps({"timestamp": timestamp.isoformat(), "origin": "synthetic", "cases": results}, indent=2), encoding="utf-8")
print(path.relative_to(REPO))
