"""Test setup: this individual submission is importable and network-free."""
from pathlib import Path
import socket
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.fixture(autouse=True)
def no_credentials_or_network(monkeypatch):
    for name in (
        "OPENROUTER_API_KEY", "OPENROUTER_MODEL",
        "OPENROUTER_INPUT_USD_PER_MILLION", "OPENROUTER_OUTPUT_USD_PER_MILLION",
    ):
        monkeypatch.delenv(name, raising=False)

    def blocked(*args, **kwargs):
        pytest.fail("Automated tests must not open network connections.")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
