"""Opt-in live evaluation of the same service used by /api/guidance."""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from project.backend.app.grounding import answer  # noqa: E402
from project.backend.app.llm import ModelError  # noqa: E402


def run(k, threshold):
    cases = yaml.safe_load((REPO / "evals/golden.yaml").read_text(encoding="utf-8"))["cases"]
    results = []
    for case in cases:
        started = time.monotonic()
        try:
            result = answer(case["question"], k=k, threshold=threshold)
            cited = {citation["document"] for citation in result["citations"]}
            missing_sources = sorted(set(case["must_cite"]) - cited)
            missing_mentions = [term for term in case["must_mention"] if term.casefold() not in result["answer"].casefold()]
            correct_route = result["grounded"] == (case["expect"] == "answer")
            passed = correct_route and not missing_sources and not missing_mentions
            entry = {"id": case["id"], "passed": passed, "result": result,
                     "missing_sources": missing_sources, "missing_mentions": missing_mentions,
                     "diagnosis": "Passed mechanical checks; human support review remains necessary." if passed else "Expected route, required source or exact required term was missing."}
        except Exception as error:
            # Do not serialize arbitrary exception bodies, transport URLs or secrets.
            entry = {"id": case["id"], "passed": False, "error": str(error) if isinstance(error, ModelError) else "Local evaluation error; inspect setup.",
                     "error_type": type(error).__name__, "diagnosis": "No verified answer; operational failure counts as a failed case."}
        entry["elapsed_ms"] = round((time.monotonic() - started) * 1000)
        results.append(entry)
        print(f"{case['id']}: {'PASS' if entry['passed'] else 'FAIL'} ({entry['elapsed_ms']} ms)", flush=True)
    timestamp = datetime.now(timezone.utc)
    report = {"timestamp": timestamp.isoformat(), "mode": "live", "k": k, "threshold": threshold,
              "passed": sum(case["passed"] for case in results), "total": len(results), "cases": results}
    folder = REPO / "evals/results"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (timestamp.strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Result: {report['passed']}/{report['total']} saved to {path.relative_to(REPO)}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Explicitly authorize this real free-model run")
    parser.add_argument("--k", type=int, default=3, choices=range(1, 9))
    parser.add_argument("--threshold", type=float, default=0.55)
    args = parser.parse_args()
    if not args.live:
        parser.error("Use --live; this evaluation calls a real free provider and consumes quota.")
    if not 0 <= args.threshold <= 1:
        parser.error("threshold must be between 0 and 1")
    run(args.k, args.threshold)
