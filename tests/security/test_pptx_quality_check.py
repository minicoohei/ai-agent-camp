"""pptx_quality_check.py の単体テスト。"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = PROJECT_ROOT / ".claude" / "hooks" / "pptx_quality_check.py"


def run_hook(payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=payload,
        capture_output=True,
        text=True,
    )


def test_invalid_pptx_emits_quality_warning(tmp_path):
    pptx_path = tmp_path / "broken.pptx"
    pptx_path.write_bytes(b"not a pptx archive")
    payload = json.dumps({
        "tool_name": "Bash",
        "tool_input": {"command": f"python build_slides.py {pptx_path}"},
        "tool_result": {"stdout": ""},
    })

    result = run_hook(payload)

    assert result.returncode == 0
    assert "PPTX Quality Check" in result.stderr
    assert "PPTX open failed" in result.stderr


def test_command_without_pptx_is_silent():
    payload = json.dumps({
        "tool_name": "Bash",
        "tool_input": {"command": "python build_report.py"},
        "tool_result": {"stdout": "report.md"},
    })

    result = run_hook(payload)

    assert result.returncode == 0
    assert result.stderr == ""


def test_invalid_json_fails_open():
    result = run_hook("not-json")

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
