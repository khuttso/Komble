import pytest


@pytest.fixture(autouse=True)
def isolate_tool_logs(tmp_path, monkeypatch):
    monkeypatch.setenv("INTERVIEWCOACH_TOOL_LOG", str(tmp_path / "tools.jsonl"))
