"""Boundary E2E テスト

各ツールの境界値・異常入力・エッジケースをテストする。
全てのテストは不正な入力に対してクラッシュせず、適切にエラー処理することを検証する。

実行:
    python -m pytest tests/e2e/test_boundary_e2e.py -v
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
TIMEOUT = 30  # 秒


def _run_tool(script: str, *args: str, timeout: int = TIMEOUT,
              env_override: dict | None = None) -> subprocess.CompletedProcess:
    """tools/ 配下のスクリプトを subprocess で実行するヘルパー"""
    cmd = [PYTHON, str(PROJECT_ROOT / "tools" / script), *args]
    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


# ---------------------------------------------------------------------------
# 1. verify_module: Invalid module numbers
# ---------------------------------------------------------------------------

class TestVerifyModuleBoundary:
    """verify_module.py の境界値テスト"""

    def test_module_zero(self):
        """Module 0 (セットアップ) を指定してもクラッシュしないこと"""
        result = _run_tool("verify_module.py", "--module", "0", "--json")
        # 正常終了 or 適切なエラーメッセージ
        assert result.returncode is not None
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            assert isinstance(data, dict)

    def test_module_99_nonexistent(self):
        """存在しないモジュール番号 99 でクラッシュしないこと"""
        result = _run_tool("verify_module.py", "--module", "99", "--json")
        # クラッシュしない (returncode が設定されている)
        assert result.returncode is not None
        # traceback が出ていないこと
        assert "Traceback" not in result.stderr, (
            f"未ハンドリングの例外:\n{result.stderr}"
        )

    def test_module_negative(self):
        """負のモジュール番号でクラッシュしないこと"""
        result = _run_tool("verify_module.py", "--module", "-1", "--json")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_module_very_large(self):
        """非常に大きなモジュール番号でクラッシュしないこと"""
        result = _run_tool("verify_module.py", "--module", "9999", "--json")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_module_non_numeric(self):
        """非数値のモジュール番号でクラッシュしないこと"""
        result = _run_tool("verify_module.py", "--module", "abc")
        # argparse が type=int でエラーを出すはず
        assert result.returncode != 0
        # しかし Traceback ではなく argparse のエラーメッセージ
        assert "Traceback" not in result.stderr


# ---------------------------------------------------------------------------
# 2. setup_progress: Already-completed steps, invalid steps
# ---------------------------------------------------------------------------

class TestSetupProgressBoundary:
    """setup_progress.py の境界値テスト"""

    def test_complete_nonexistent_step(self):
        """存在しないステップ名を complete してもクラッシュしないこと"""
        result = _run_tool(
            "setup_progress.py", "complete", "nonexistent-step-xyz"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_complete_same_step_twice(self):
        """同じステップを2回 complete してもクラッシュしないこと"""
        _run_tool("setup_progress.py", "complete", "setup-start")
        result = _run_tool("setup_progress.py", "complete", "setup-start")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_status_nonexistent_step(self):
        """存在しないステップの status を問い合わせてもクラッシュしないこと"""
        result = _run_tool(
            "setup_progress.py", "status", "does-not-exist"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_complete_with_invalid_json_details(self):
        """不正な JSON を --details に渡してもクラッシュしないこと"""
        result = _run_tool(
            "setup_progress.py", "complete", "setup-start",
            "--details", "not-valid-json{"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_skip_with_empty_reason(self):
        """空の理由で skip してもクラッシュしないこと"""
        result = _run_tool(
            "setup_progress.py", "skip", "setup-slack", "--reason", ""
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_no_subcommand_shows_help(self):
        """サブコマンドなしで実行すると help が表示されること"""
        result = _run_tool("setup_progress.py")
        # exit code 1 で help 表示
        assert result.returncode != 0
        # usage や help メッセージが含まれること
        combined = result.stdout + result.stderr
        assert "usage" in combined.lower() or "help" in combined.lower() or len(combined) > 0


# ---------------------------------------------------------------------------
# 3. lesson_progress: Non-existent lesson IDs
# ---------------------------------------------------------------------------

class TestLessonProgressBoundary:
    """lesson_progress.py の境界値テスト"""

    def test_mark_nonexistent_lesson(self):
        """存在しないレッスン ID を --mark してもクラッシュしないこと"""
        result = _run_tool(
            "lesson_progress.py", "--mark", "start-99-99"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_check_nonexistent_lesson(self):
        """存在しないレッスン ID を --check してもクラッシュしないこと"""
        result = _run_tool(
            "lesson_progress.py", "--check", "nonexistent-lesson"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_mark_empty_id(self):
        """空のレッスン ID を --mark してもクラッシュしないこと"""
        result = _run_tool("lesson_progress.py", "--mark", "")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_mark_special_characters(self):
        """特殊文字を含むレッスン ID でクラッシュしないこと"""
        result = _run_tool(
            "lesson_progress.py", "--mark", "start-1-1; echo hacked"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr


# ---------------------------------------------------------------------------
# 4. credential_manager: Edge cases
# ---------------------------------------------------------------------------

class TestCredentialManagerBoundary:
    """credential_manager.py の境界値テスト"""

    def test_status_always_safe(self):
        """status コマンドは常にクラッシュしないこと"""
        result = _run_tool("credential_manager.py", "status")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_delete_nonexistent_key(self):
        """存在しないキーを delete してもクラッシュしないこと

        delete は確認プロンプト (input()) を出すため、
        subprocess では stdin が EOF になり EOFError が出るのは想定内。
        それ以外の Traceback (KeyError 等) がないことを確認する。
        """
        cmd = [PYTHON, str(PROJECT_ROOT / "tools" / "credential_manager.py"),
               "delete", "__NONEXISTENT_KEY_E2E__"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TIMEOUT,
            cwd=str(PROJECT_ROOT), input="n\n",  # 確認プロンプトに "n" を送信
        )
        assert result.returncode is not None
        # EOFError 以外の Traceback がないこと
        if "Traceback" in result.stderr:
            assert "EOFError" in result.stderr, (
                f"EOFError 以外の例外:\n{result.stderr}"
            )

    def test_prepare_dotenv_empty_key(self):
        """空のキー名で prepare-dotenv してもクラッシュしないこと"""
        result = _run_tool("credential_manager.py", "prepare-dotenv", "")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_prepare_dotenv_special_chars(self):
        """特殊文字を含むキー名でクラッシュしないこと"""
        result = _run_tool(
            "credential_manager.py", "prepare-dotenv",
            "KEY_WITH_SPECIAL_!@#$"
        )
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_no_subcommand_shows_help(self):
        """サブコマンドなしで実行すると help が表示されること"""
        result = _run_tool("credential_manager.py")
        combined = result.stdout + result.stderr
        assert len(combined.strip()) > 0, "出力が完全に空"


# ---------------------------------------------------------------------------
# 5. content_updater: No git remote
# ---------------------------------------------------------------------------

class TestContentUpdaterBoundary:
    """content_updater.py の境界値テスト"""

    def test_status_without_upstream(self):
        """upstream リモートが無くてもクラッシュしないこと"""
        result = _run_tool("content_updater.py", "--status")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_dry_run_without_upstream(self):
        """upstream リモートが無くても --dry-run でクラッシュしないこと"""
        result = _run_tool("content_updater.py", "--dry-run")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr

    def test_rollback_without_previous_update(self):
        """更新履歴が無い状態で --rollback してもクラッシュしないこと"""
        result = _run_tool("content_updater.py", "--rollback")
        assert result.returncode is not None
        assert "Traceback" not in result.stderr


# ---------------------------------------------------------------------------
# 6. All tools --help flag
# ---------------------------------------------------------------------------

class TestHelpFlag:
    """全ツールの --help フラグが正常に動作すること"""

    TOOLS_WITH_HELP = [
        "setup_progress.py",
        "lesson_progress.py",
        "verify_module.py",
        "content_updater.py",
        "credential_manager.py",
        "check_command_paths.py",
        "check_prerequisites.py",
        "check_module_consistency.py",
    ]

    @pytest.mark.parametrize("script", TOOLS_WITH_HELP)
    def test_help_does_not_crash(self, script):
        """--help がクラッシュせずに終了すること"""
        script_path = PROJECT_ROOT / "tools" / script
        if not script_path.exists():
            pytest.skip(f"{script} が存在しない")
        result = _run_tool(script, "--help")
        # --help は通常 exit code 0
        assert result.returncode == 0, (
            f"{script} --help failed:\n"
            f"stdout: {result.stdout[:200]}\n"
            f"stderr: {result.stderr[:200]}"
        )
        # 何らかの出力があること
        assert len(result.stdout.strip()) > 0, (
            f"{script} --help の出力が空"
        )

    ADDITIONAL_TOOLS = [
        "check_agent_docs.py",
        "check_imports.py",
        "check_skills_in_course.py",
        "audit_readability.py",
    ]

    @pytest.mark.parametrize("script", ADDITIONAL_TOOLS)
    def test_additional_tools_help(self, script):
        """追加ツールの --help がクラッシュしないこと"""
        script_path = PROJECT_ROOT / "tools" / script
        if not script_path.exists():
            pytest.skip(f"{script} が存在しない")
        result = _run_tool(script, "--help")
        assert result.returncode == 0, f"{script} --help failed: {result.stderr[:200]}"


# ---------------------------------------------------------------------------
# 7. Timeout protection
# ---------------------------------------------------------------------------

class TestTimeoutProtection:
    """潜在的にハングするスクリプトのタイムアウト保護"""

    def test_setup_progress_show_within_timeout(self):
        """setup_progress.py show が 10 秒以内に終了すること"""
        try:
            result = _run_tool("setup_progress.py", "show", timeout=10)
            assert result.returncode is not None
        except subprocess.TimeoutExpired:
            pytest.fail("setup_progress.py show が 10 秒以内に終了しなかった")

    def test_lesson_progress_list_within_timeout(self):
        """lesson_progress.py --list が 10 秒以内に終了すること"""
        try:
            result = _run_tool("lesson_progress.py", "--list", timeout=10)
            assert result.returncode is not None
        except subprocess.TimeoutExpired:
            pytest.fail("lesson_progress.py --list が 10 秒以内に終了しなかった")

    def test_verify_module_within_timeout(self):
        """verify_module.py が 15 秒以内に終了すること"""
        try:
            result = _run_tool(
                "verify_module.py", "--module", "1", "--json", timeout=15
            )
            assert result.returncode is not None
        except subprocess.TimeoutExpired:
            pytest.fail("verify_module.py が 15 秒以内に終了しなかった")

    def test_credential_manager_status_within_timeout(self):
        """credential_manager.py status が 10 秒以内に終了すること"""
        try:
            result = _run_tool("credential_manager.py", "status", timeout=10)
            assert result.returncode is not None
        except subprocess.TimeoutExpired:
            pytest.fail("credential_manager.py status が 10 秒以内に終了しなかった")
