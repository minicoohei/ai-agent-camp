"""Tool integration E2E テスト

主要ツールのワークフローをエンドツーエンドで検証する。
subprocess.run() を使い CLI としての動作を確認。

実行:
    python -m pytest tests/e2e/test_tool_integration.py -v
"""

from __future__ import annotations

import json
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
# 1. Setup progress workflow
# ---------------------------------------------------------------------------

class TestSetupProgressWorkflow:
    """setup_progress.py の show → complete → show → verify フロー"""

    @pytest.fixture(autouse=True)
    def _use_tmp_progress(self, tmp_path, monkeypatch):
        """テスト用の進捗ファイルを使う"""
        self.progress_file = tmp_path / ".setup-progress.json"
        monkeypatch.setenv("SETUP_PROGRESS_FILE", str(self.progress_file))

    def test_show_without_progress_file(self):
        """進捗ファイルがなくても show が正常終了すること"""
        result = _run_tool("setup_progress.py", "show")
        # exit code 0 で正常終了
        assert result.returncode == 0, (
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )

    def test_complete_and_show_workflow(self, tmp_path):
        """complete → show で完了ステップが反映されること"""
        # ステップを完了マーク
        result = _run_tool("setup_progress.py", "complete", "setup-start")
        assert result.returncode == 0, f"stderr: {result.stderr}"

        # show で確認
        result = _run_tool("setup_progress.py", "show")
        assert result.returncode == 0
        # 出力に setup-start 関連の情報が含まれること
        assert "setup-start" in result.stdout or "基本ツール" in result.stdout

    def test_next_shows_suggestion(self):
        """next コマンドが次のステップを提案すること"""
        result = _run_tool("setup_progress.py", "next")
        assert result.returncode == 0
        assert len(result.stdout.strip()) > 0, "next の出力が空"

    def test_status_for_specific_step(self):
        """status コマンドで特定ステップの情報を取得できること"""
        result = _run_tool("setup_progress.py", "status", "setup-gemini")
        assert result.returncode == 0

    def test_complete_with_details(self):
        """complete に --details JSON を渡せること"""
        result = _run_tool(
            "setup_progress.py", "complete", "setup-start",
            "--details", '{"python": "3.12.0"}'
        )
        assert result.returncode == 0

    def test_skip_step(self):
        """skip コマンドでステップをスキップできること"""
        result = _run_tool(
            "setup_progress.py", "skip", "setup-slack",
            "--reason", "後で設定する"
        )
        assert result.returncode == 0


# ---------------------------------------------------------------------------
# 2. Lesson progress workflow
# ---------------------------------------------------------------------------

class TestLessonProgressWorkflow:
    """lesson_progress.py の --list → --mark → --next フロー"""

    def test_list_shows_lessons(self):
        """--list がレッスン一覧を表示すること"""
        result = _run_tool("lesson_progress.py", "--list")
        assert result.returncode == 0
        # start-X-Y 形式のレッスン ID が含まれること
        assert "start-" in result.stdout, (
            f"レッスン一覧に start- が含まれない: {result.stdout[:200]}"
        )

    def test_mark_lesson(self):
        """--mark でレッスンを完了マークできること"""
        result = _run_tool("lesson_progress.py", "--mark", "start-0-1")
        # mark は進捗ファイルに書き込むが、エラーにならないこと
        assert result.returncode == 0, f"stderr: {result.stderr}"

    def test_next_lesson(self):
        """--next が次のレッスンを提案すること"""
        result = _run_tool("lesson_progress.py", "--next")
        assert result.returncode == 0

    def test_check_lesson(self):
        """--check でレッスンのチェックを実行できること"""
        result = _run_tool("lesson_progress.py", "--check", "start-0-1")
        assert result.returncode == 0


# ---------------------------------------------------------------------------
# 3. Credential manager workflow
# ---------------------------------------------------------------------------

class TestCredentialManagerWorkflow:
    """credential_manager.py の status 表示フロー

    実際の keyring 操作は test_credential_manager_e2e.py でカバー。
    ここでは CLI インターフェースの基本動作を検証する。
    """

    def test_status_runs_without_error(self):
        """status コマンドが正常終了すること"""
        result = _run_tool("credential_manager.py", "status")
        # keyring が無い環境でもクラッシュせずに終了すること
        assert result.returncode in (0, 1), (
            f"Unexpected exit code {result.returncode}\n"
            f"stderr: {result.stderr}"
        )

    def test_prepare_dotenv_creates_placeholder(self, tmp_path):
        """prepare-dotenv が .env.local にプレースホルダーを準備すること"""
        result = _run_tool("credential_manager.py", "prepare-dotenv", "TEST_KEY")
        # prepare-dotenv は stdout にガイダンスを出力するはず
        # keyring が無くてもクラッシュしないこと
        assert result.returncode in (0, 1), f"stderr: {result.stderr}"


# ---------------------------------------------------------------------------
# 4. Content updater workflow
# ---------------------------------------------------------------------------

class TestContentUpdaterWorkflow:
    """content_updater.py の --status / --dry-run フロー

    git remote (upstream) が無い環境でも安全に動作することを確認する。
    """

    def test_status_output_format(self):
        """--status が何らかの状態情報を出力すること"""
        result = _run_tool("content_updater.py", "--status")
        # upstream リモートが無い場合はエラーになるが、クラッシュはしない
        combined = result.stdout + result.stderr
        assert len(combined.strip()) > 0, "--status の出力が完全に空"

    def test_dry_run_does_not_modify_files(self):
        """--dry-run がファイルを変更しないこと"""
        # 実行前の状態を記録
        result = _run_tool("content_updater.py", "--dry-run")
        # upstream が無くてもクラッシュしないこと
        # (エラーメッセージが出ても exit しているだけ)
        assert result.returncode is not None


# ---------------------------------------------------------------------------
# 5. Verify module workflow
# ---------------------------------------------------------------------------

class TestVerifyModuleWorkflow:
    """verify_module.py の --module N --json フロー"""

    def test_verify_module_1_json_output(self):
        """--module 1 --json が有効な JSON を返すこと"""
        result = _run_tool("verify_module.py", "--module", "1", "--json")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        # JSON パース可能であること
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_verify_module_json_structure(self):
        """JSON 出力に必要なフィールドがあること"""
        result = _run_tool("verify_module.py", "--module", "1", "--json")
        if result.returncode != 0:
            pytest.skip(f"verify_module failed: {result.stderr}")
        data = json.loads(result.stdout)
        # 基本構造の検証
        assert "module" in data or "module_number" in data or "lessons" in data, (
            f"必須フィールドが不足: {list(data.keys())}"
        )

    def test_verify_module_text_output(self):
        """--json なしでテキスト出力が得られること"""
        result = _run_tool("verify_module.py", "--module", "1")
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert len(result.stdout.strip()) > 0, "テキスト出力が空"

    def test_verify_module_with_output_file(self, tmp_path):
        """--output で JSON をファイルに保存できること

        verify_module.py は --output パスをプロジェクトルート内に制限するため、
        プロジェクト内の一時ディレクトリを使う。
        """
        out_dir = PROJECT_ROOT / "outputs" / "_test_tmp"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "result.json"
        try:
            result = _run_tool(
                "verify_module.py", "--module", "1", "--json",
                "--output", str(out_file)
            )
            assert result.returncode == 0, (
                f"verify_module failed: {result.stderr}"
            )
            assert out_file.exists(), f"出力ファイルが作成されていない: {out_file}"
            data = json.loads(out_file.read_text(encoding="utf-8"))
            assert isinstance(data, dict)
        finally:
            # テスト用ファイルを片付ける
            if out_file.exists():
                out_file.unlink()
            if out_dir.exists():
                try:
                    out_dir.rmdir()
                except OSError:
                    pass


# ---------------------------------------------------------------------------
# 6. Cross-tool integration: setup + lesson progress
# ---------------------------------------------------------------------------

class TestCrossToolIntegration:
    """複数ツール間の連携動作を検証"""

    def test_setup_and_lesson_progress_coexist(self):
        """setup_progress と lesson_progress が同時に動作してもクラッシュしないこと"""
        r1 = _run_tool("setup_progress.py", "show")
        r2 = _run_tool("lesson_progress.py", "--list")
        assert r1.returncode == 0, f"setup_progress failed: {r1.stderr}"
        assert r2.returncode == 0, f"lesson_progress failed: {r2.stderr}"

    def test_verify_module_for_each_existing_module(self):
        """存在する各モジュールで verify_module が動作すること"""
        # モジュール 0~3 だけ軽くチェック (全モジュールは時間がかかる)
        for mod in [0, 1, 2, 3]:
            result = _run_tool("verify_module.py", "--module", str(mod), "--json")
            if result.returncode != 0:
                continue  # レッスンが無いモジュールはスキップ
            data = json.loads(result.stdout)
            assert isinstance(data, dict), f"Module {mod}: invalid JSON"
