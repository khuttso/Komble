"""Run the real JavaScript checks through the course's required pytest command."""

from pathlib import Path
import shutil
import subprocess


def test_pack_hub_acceptance_rules():
    project_dir = Path(__file__).resolve().parents[1]
    node = shutil.which("node")
    assert node, "Install Node.js 20.19+ or 22.12+ and make node available on PATH."

    # Python is only the test entry point; the app's JavaScript rules are not duplicated.
    result = subprocess.run(
        [node, "--test", "src/tests/packHub.test.js"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
