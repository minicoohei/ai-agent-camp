"""console-log-guard.sh の単体テスト。"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = PROJECT_ROOT / ".claude" / "hooks" / "console-log-guard.sh"


def run_hook(payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(HOOK_SCRIPT)],
        input=payload,
        capture_output=True,
        text=True,
    )


def hook_input(file_path: Path) -> str:
    return json.dumps({
        "tool_name": "Edit",
        "tool_input": {"file_path": str(file_path)},
    })


def test_console_log_emits_warning(tmp_path):
    source = tmp_path / "app.ts"
    source.write_text("console.log('debug');\n", encoding="utf-8")

    result = run_hook(hook_input(source))

    assert result.returncode == 0
    assert "WARNING: console.log found" in result.stderr
    assert "1:console.log" in result.stderr


def test_file_without_console_log_is_silent(tmp_path):
    source = tmp_path / "app.js"
    source.write_text("export const answer = 42;\n", encoding="utf-8")

    result = run_hook(hook_input(source))

    assert result.returncode == 0
    assert result.stderr == ""


def test_invalid_json_fails_open():
    result = run_hook("not-json")

    assert result.returncode == 0
    assert result.stdout == ""
