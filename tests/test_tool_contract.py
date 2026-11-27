import json
import os
from dataclasses import replace
from pathlib import Path

import pytest

from src.act import call_tool
from src.tools import TOOLS, tools_for
from project.backend.app import content


@pytest.mark.parametrize("arguments", [
    {"pack_id": "../../private"}, {"pack_id": "ignore instructions"},
    {"pack_id": "frontend", "limit": True}, {"pack_id": "frontend", "limit": "2"},
    {"pack_id": "frontend", "limit": 5}, {"pack_id": "frontend", "limit": -1},
    {"pack_id": "frontend", "student_id": "other"}, [], None, "broken JSON",
])
def test_bad_input_never_executes(arguments):
    def forbidden(args):
        pytest.fail("Invalid input reached the tool body")
    allowed = {name: replace(tool, run=forbidden) for name, tool in TOOLS.items()}
    assert not call_tool({"name": "get_pack_questions", "arguments": arguments}, allowed)["ok"]


def test_tool_not_offered():
    out = call_tool({"name": "get_pack_questions", "arguments": {"pack_id": "frontend"}}, {})
    assert not out["ok"] and "offered list" in out["error"]


def test_reads_current_catalogue_and_does_not_mutate_it(monkeypatch):
    pack = content.PACKS[0].model_copy(update={"title": "Current catalogue title"}, deep=True)
    monkeypatch.setattr(content, "PACKS", (pack,))
    call = {"name": "get_pack_questions", "arguments": {"pack_id": "frontend", "limit": 1}}
    first = call_tool(call)
    assert first == call_tool(call)
    assert first["result"]["title"] == "Current catalogue title"
    assert first["result"]["questions"][0] == pack.questions[0].model_dump()
    assert len(pack.questions) == 4


def test_missing_pack_is_actionable(monkeypatch):
    monkeypatch.setattr(content, "PACKS", ())
    out = call_tool({"name": "get_pack_questions", "arguments": {"pack_id": "frontend"}})
    assert not out["ok"] and "Choose another" in out["error"]


def test_logs_and_errors_do_not_echo_untrusted_content():
    secret = "PRIVATE_TEST_VALUE"
    call_tool({"name": secret, "arguments": {"user_id": secret}}, caller=secret)
    out = call_tool({"name": "get_pack_questions", "arguments": {"pack_id": secret}}, caller=secret)
    lines = Path(os.environ["INTERVIEWCOACH_TOOL_LOG"]).read_text().splitlines()
    assert len(lines) == 2
    assert secret not in str(out) + str(lines)
    assert set(json.loads(lines[0])) == {"timestamp", "tool", "outcome", "elapsed_ms"}


def test_internal_errors_are_sanitized():
    def broken(args):
        raise RuntimeError("private/path/table")
    allowed = {name: replace(tool, run=broken) for name, tool in tools_for().items()}
    out = call_tool({"name": "get_pack_questions", "arguments": {"pack_id": "frontend"}}, allowed)
    assert not out["ok"] and "private" not in out["error"]


def test_log_failure_is_actionable(tmp_path, monkeypatch):
    monkeypatch.setenv("INTERVIEWCOACH_TOOL_LOG", str(tmp_path))
    out = call_tool({"name": "get_pack_questions", "arguments": {"pack_id": "frontend"}})
    assert not out["ok"] and "audit logging" in out["error"]
