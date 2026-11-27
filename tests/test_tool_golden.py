"""Run every student's golden file through the real dispatcher, without keys."""
from pathlib import Path

import pytest
import yaml

from src.act import call_tool
from src.tools import tools_for

FILES = sorted((Path(__file__).resolve().parents[1] / "evals/tools").glob("*.yaml"))
CASES = [(file.stem, case) for file in FILES
         for case in yaml.safe_load(file.read_text(encoding="utf-8"))["cases"]]


@pytest.mark.parametrize("owner,case", CASES, ids=[f"{owner}:{case['id']}" for owner, case in CASES])
def test_tool_golden_case(owner, case):
    out = call_tool({"name": case["tool"], "arguments": case["arguments"]},
                    tools_for(case.get("caller")), case.get("caller"))
    if case["expect"] == "ok":
        assert out["ok"], out
        for key, value in case.get("result_has", {}).items():
            assert out["result"][key] == value
    else:
        assert not out["ok"], out
        for phrase in case.get("error_has", []):
            assert phrase.casefold() in out["error"].casefold()


def test_golden_files_have_required_coverage():
    assert FILES, "No golden files found"
    for file in FILES:
        data = yaml.safe_load(file.read_text(encoding="utf-8"))
        assert data["tool_owner"] == file.stem
        cases = data["cases"]
        kinds = [case["type"] for case in cases]
        assert len(cases) >= 5 and kinds.count("normal") >= 3
        assert "adversarial" in kinds and "bad-input" in kinds
        assert len({case["id"] for case in cases}) == len(cases)
        assert all(case["why"].strip() for case in cases)
