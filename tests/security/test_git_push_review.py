"""git-push-review.sh の単体テスト。"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HOOK_SCRIPT = PROJECT_ROOT / ".claude" / "hooks" / "git-push-review.sh"


def run_hook(repo: Path, command: str) -> subprocess.CompletedProcess[str]:
    hook_input = json.dumps({
        "tool_name": "Bash",
        "tool_input": {"command": command},
    })
    return subprocess.run(
        ["bash", str(HOOK_SCRIPT)],
        cwd=repo,
        input=hook_input,
        capture_output=True,
        text=True,
    )


def init_repo(path: Path, branch: str) -> None:
    subprocess.run(
        ["git", "init", "-q", "-b", branch, str(path)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_direct_push_from_main_is_blocked(tmp_path):
    init_repo(tmp_path, "main")

    result = run_hook(tmp_path, "git push origin main")

    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"] == "block"
    assert "main" in result.stdout


def test_direct_push_from_master_is_blocked(tmp_path):
    init_repo(tmp_path, "master")

    result = run_hook(tmp_path, "git push origin master")

    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"] == "block"
    assert "master" in result.stdout


def test_push_from_feature_branch_is_allowed(tmp_path):
    init_repo(tmp_path, "feature/security-hooks")

    result = run_hook(tmp_path, "git push origin feature/security-hooks")

    assert result.returncode == 0
    assert result.stdout == ""
    assert "Branch: feature/security-hooks" in result.stderr
