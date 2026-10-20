"""Read private configuration without printing it or mutating the environment."""

import os
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
RUNTIME = ROOT / "runtime"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


def setting(name: str, default: str = "") -> str:
    return os.environ.get(name) or str(dotenv_values(ROOT / ".env").get(name) or default)
