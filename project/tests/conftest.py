import pytest

from project.backend.app import usage


@pytest.fixture(autouse=True)
def isolate_test_logs(tmp_path, monkeypatch):
    """Mocked tests must not contaminate real operational evidence."""
    monkeypatch.setattr(usage, "REPO", tmp_path)
