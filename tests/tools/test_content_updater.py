"""content_updater.py の単体テスト。

git/gh コマンドをモックし、コンテンツ更新ロジックを検証する。
"""
import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr,
    )


# ---------------------------------------------------------------------------
# _sanitize_url
# ---------------------------------------------------------------------------

class TestSanitizeUrl:
    def test_plain_url_unchanged(self):
        from content_updater import _sanitize_url
        url = "https://github.com/user/repo.git"
        assert _sanitize_url(url) == url

    def test_strips_token_from_url(self):
        from content_updater import _sanitize_url
        url = "https://ghp_secret123@github.com/user/repo.git"
        result = _sanitize_url(url)
        assert "ghp_secret123" not in result
        assert "github.com" in result

    def test_strips_user_password(self):
        from content_updater import _sanitize_url
        url = "https://user:password@github.com/user/repo.git"
        result = _sanitize_url(url)
        assert "password" not in result
        assert "user:" not in result


# ---------------------------------------------------------------------------
# run_git
# ---------------------------------------------------------------------------

class TestRunGit:
    @patch("content_updater.subprocess.run")
    def test_passes_project_root(self, mock_run):
        from content_updater import run_git, PROJECT_ROOT
        mock_run.return_value = _make_completed()
        run_git("status")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "git"
        assert "-C" in args
        assert str(PROJECT_ROOT) in args


# ---------------------------------------------------------------------------
# is_git_repo / has_upstream
# ---------------------------------------------------------------------------

class TestGitChecks:
    @patch("content_updater.run_git")
    def test_is_git_repo_true(self, mock_git):
        from content_updater import is_git_repo
        mock_git.return_value = _make_completed(returncode=0)
        assert is_git_repo() is True

    @patch("content_updater.run_git")
    def test_is_git_repo_false(self, mock_git):
        from content_updater import is_git_repo
        mock_git.return_value = _make_completed(returncode=128)
        assert is_git_repo() is False

    @patch("content_updater.run_git")
    def test_has_upstream_true(self, mock_git):
        from content_updater import has_upstream
        mock_git.return_value = _make_completed(stdout="origin\nupstream\n")
        assert has_upstream() is True

    @patch("content_updater.run_git")
    def test_has_upstream_false(self, mock_git):
        from content_updater import has_upstream
        mock_git.return_value = _make_completed(stdout="origin\n")
        assert has_upstream() is False

    @patch("content_updater.run_git")
    def test_has_upstream_error(self, mock_git):
        from content_updater import has_upstream
        mock_git.return_value = _make_completed(returncode=1)
        assert has_upstream() is False


# ---------------------------------------------------------------------------
# fetch_upstream
# ---------------------------------------------------------------------------

class TestFetchUpstream:
    @patch("content_updater.run_git")
    def test_fetch_success(self, mock_git):
        from content_updater import fetch_upstream
        mock_git.return_value = _make_completed()
        assert fetch_upstream() is True

    @patch("content_updater.run_git")
    def test_fetch_failure(self, mock_git):
        from content_updater import fetch_upstream
        mock_git.return_value = _make_completed(returncode=1, stderr="fatal: remote error")
        assert fetch_upstream() is False


# ---------------------------------------------------------------------------
# get_changed_files / get_new_files_in_upstream / get_deleted_files_in_upstream
# ---------------------------------------------------------------------------

class TestDiffFunctions:
    @patch("content_updater.run_git")
    def test_get_changed_files(self, mock_git):
        from content_updater import get_changed_files
        # 各 CONTENT_PATHS ごとに呼ばれる。最初の呼び出しだけ結果を返す
        mock_git.return_value = _make_completed(stdout="https://ai-agent.camp/ja/course/module-1\n")
        result = get_changed_files()
        assert "https://ai-agent.camp/ja/course/module-1" in result

    @patch("content_updater.run_git")
    def test_get_changed_files_empty(self, mock_git):
        from content_updater import get_changed_files
        mock_git.return_value = _make_completed(stdout="")
        result = get_changed_files()
        assert result == []

    @patch("content_updater.run_git")
    def test_get_changed_files_deduplicates(self, mock_git):
        from content_updater import get_changed_files
        # 同じファイルが複数パスから返される場合
        mock_git.return_value = _make_completed(stdout="CLAUDE.md\n")
        result = get_changed_files()
        assert result.count("CLAUDE.md") == 1

    @patch("content_updater.run_git")
    def test_get_new_files(self, mock_git):
        from content_updater import get_new_files_in_upstream
        mock_git.return_value = _make_completed(stdout="courses/aiagent/lesson03-core/module01-banner/chapter.yaml\n")
        result = get_new_files_in_upstream()
        assert len(result) >= 1

    @patch("content_updater.run_git")
    def test_get_deleted_files(self, mock_git):
        from content_updater import get_deleted_files_in_upstream
        mock_git.return_value = _make_completed(stdout="tools/old_script.py\n")
        result = get_deleted_files_in_upstream()
        assert "tools/old_script.py" in result


# ---------------------------------------------------------------------------
# backup_files
# ---------------------------------------------------------------------------

class TestBackupFiles:
    def test_backup_matching_files(self, tmp_path):
        from content_updater import BACKUP_BEFORE_UPDATE
        import content_updater

        # Override PROJECT_ROOT for test
        original_root = content_updater.PROJECT_ROOT
        original_backup = content_updater.BACKUP_BASE_DIR
        content_updater.PROJECT_ROOT = tmp_path
        content_updater.BACKUP_BASE_DIR = tmp_path / "work" / ".backup"

        try:
            # Create a file that matches BACKUP_BEFORE_UPDATE pattern
            exercise_file = tmp_path / "course" / "exercises" / "test.md"
            exercise_file.parent.mkdir(parents=True, exist_ok=True)
            exercise_file.write_text("user work")

            result = content_updater.backup_files(
                ["course/exercises/test.md", "https://ai-agent.camp/ja/course/module-1"],
                "2026-01-01_000000",
            )
            assert result is not None
            assert (result / "course" / "exercises" / "test.md").exists()
        finally:
            content_updater.PROJECT_ROOT = original_root
            content_updater.BACKUP_BASE_DIR = original_backup

    def test_backup_no_matching_files(self, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        original_backup = content_updater.BACKUP_BASE_DIR
        content_updater.PROJECT_ROOT = tmp_path
        content_updater.BACKUP_BASE_DIR = tmp_path / "work" / ".backup"

        try:
            result = content_updater.backup_files(
                ["https://ai-agent.camp/ja/course/module-1"],
                "2026-01-01_000000",
            )
            assert result is None
        finally:
            content_updater.PROJECT_ROOT = original_root
            content_updater.BACKUP_BASE_DIR = original_backup


# ---------------------------------------------------------------------------
# checkout_content
# ---------------------------------------------------------------------------

class TestCheckoutContent:
    @patch("content_updater.run_git")
    def test_all_success(self, mock_git):
        from content_updater import checkout_content
        mock_git.return_value = _make_completed()
        success, failed = checkout_content()
        assert success is True
        assert failed == []

    @patch("content_updater.run_git")
    def test_some_paths_missing(self, mock_git):
        """upstream に存在しないパスはスキップされ、失敗にはならない"""
        from content_updater import checkout_content

        def side_effect(*args, **kwargs):
            path = args[3] if len(args) > 3 else ""
            if path == "courses/":
                return _make_completed(
                    returncode=1,
                    stderr="error: pathspec 'courses/' did not match any file(s) known to git",
                )
            return _make_completed()

        mock_git.side_effect = side_effect
        success, failed = checkout_content()
        assert success is True
        assert failed == []

    @patch("content_updater.run_git")
    def test_real_failure(self, mock_git):
        """パーミッションエラーなどの実際の失敗"""
        from content_updater import checkout_content

        def side_effect(*args, **kwargs):
            path = args[3] if len(args) > 3 else ""
            if path == "course/":
                return _make_completed(returncode=1, stderr="error: unable to write file")
            return _make_completed()

        mock_git.side_effect = side_effect
        success, failed = checkout_content()
        assert success is False
        assert "course/" in failed

    @patch("content_updater.run_git")
    def test_all_fail(self, mock_git):
        from content_updater import checkout_content
        mock_git.return_value = _make_completed(returncode=1, stderr="fatal: error")
        success, failed = checkout_content()
        assert success is False


# ---------------------------------------------------------------------------
# delete_removed_files
# ---------------------------------------------------------------------------

class TestDeleteRemovedFiles:
    def test_deletes_existing_files(self, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            target = tmp_path / "tools" / "old.py"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("old content")

            count = content_updater.delete_removed_files(["tools/old.py"])
            assert count == 1
            assert not target.exists()
        finally:
            content_updater.PROJECT_ROOT = original_root

    def test_skips_nonexistent_files(self, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            count = content_updater.delete_removed_files(["tools/nonexistent.py"])
            assert count == 0
        finally:
            content_updater.PROJECT_ROOT = original_root


# ---------------------------------------------------------------------------
# update_log (load/save/record)
# ---------------------------------------------------------------------------

class TestUpdateLog:
    def test_load_empty(self, tmp_path):
        import content_updater
        original = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "log.json"

        try:
            result = content_updater.load_update_log()
            assert result == []
        finally:
            content_updater.UPDATE_LOG_FILE = original

    def test_save_and_load(self, tmp_path):
        import content_updater
        original = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "work" / "log.json"

        try:
            log = [{"timestamp": "2026-01-01", "files_updated": 5}]
            content_updater.save_update_log(log)
            loaded = content_updater.load_update_log()
            assert loaded == log
        finally:
            content_updater.UPDATE_LOG_FILE = original

    def test_record_update(self, tmp_path):
        import content_updater
        original = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "work" / "log.json"

        try:
            content_updater.record_update(
                "2026-03-16_120000",
                "abc1234",
                "def5678",
                ["course/test.html", "tools/test.py"],
                tmp_path / "backup",
            )
            log = content_updater.load_update_log()
            assert len(log) == 1
            assert log[0]["files_updated"] == 2
            assert log[0]["before_commit"] == "abc1234"
            assert log[0]["after_commit"] == "def5678"
        finally:
            content_updater.UPDATE_LOG_FILE = original

    def test_record_truncates_to_100(self, tmp_path):
        import content_updater
        original = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "work" / "log.json"

        try:
            # Pre-populate with 100 entries
            existing = [{"timestamp": f"entry-{i}", "files_updated": 0} for i in range(100)]
            content_updater.save_update_log(existing)

            content_updater.record_update("new-entry", "a", "b", [], None)
            log = content_updater.load_update_log()
            assert len(log) == 100  # truncated
            assert log[-1]["timestamp"] == "new-entry"
        finally:
            content_updater.UPDATE_LOG_FILE = original


# ---------------------------------------------------------------------------
# cmd_setup
# ---------------------------------------------------------------------------

class TestCmdSetup:
    @patch("content_updater.checkout_content", return_value=(True, []))
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.run_git")
    @patch("content_updater.subprocess.run")
    @patch("content_updater.has_upstream", return_value=False)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_setup_success(self, mock_is_git, mock_has_up, mock_subproc, mock_git, mock_fetch, mock_checkout, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            # gh auth status succeeds
            mock_subproc.return_value = _make_completed()
            mock_git.return_value = _make_completed()

            result = content_updater.cmd_setup()
            assert result == 0
        finally:
            content_updater.PROJECT_ROOT = original_root

    @patch("content_updater.is_git_repo", return_value=False)
    def test_setup_not_git_repo(self, mock_is_git):
        import content_updater
        result = content_updater.cmd_setup()
        assert result == 1

    @patch("content_updater.has_upstream", return_value=True)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_setup_upstream_exists(self, mock_is_git, mock_has_up):
        import content_updater
        result = content_updater.cmd_setup()
        assert result == 1

    @patch("content_updater.subprocess.run")
    @patch("content_updater.has_upstream", return_value=False)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_setup_gh_auth_not_logged_in(self, mock_is_git, mock_has_up, mock_subproc):
        import content_updater
        mock_subproc.return_value = _make_completed(returncode=1)
        result = content_updater.cmd_setup()
        assert result == 1


# ---------------------------------------------------------------------------
# cmd_update
# ---------------------------------------------------------------------------

class TestCmdUpdate:
    @patch("content_updater.record_update")
    @patch("content_updater.get_upstream_commit", return_value="def5678")
    @patch("content_updater.update_skills", return_value=([], [], {}))
    @patch("content_updater.checkout_content_paths", return_value=(True, []))
    @patch("content_updater.get_deleted_files_in_upstream", return_value=[])
    @patch("content_updater.get_changed_files", return_value=["course/test.html"])
    @patch("content_updater.get_current_commit", return_value="abc1234")
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_update_success(self, *mocks):
        import content_updater
        result = content_updater.cmd_update()
        assert result == 0

    @patch("content_updater.get_deleted_files_in_upstream", return_value=[])
    @patch("content_updater.get_changed_files", return_value=[])
    @patch("content_updater.get_current_commit", return_value="abc1234")
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_update_no_changes(self, *mocks):
        import content_updater
        result = content_updater.cmd_update()
        assert result == 0

    @patch("content_updater.has_upstream", return_value=False)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_update_no_upstream(self, *mocks):
        import content_updater
        result = content_updater.cmd_update()
        assert result == 1

    @patch("content_updater.checkout_content_paths", return_value=(False, ["course/"]))
    @patch("content_updater.get_deleted_files_in_upstream", return_value=[])
    @patch("content_updater.get_changed_files", return_value=["course/test.html"])
    @patch("content_updater.get_current_commit", return_value="abc1234")
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_update_checkout_failure(self, *mocks):
        import content_updater
        result = content_updater.cmd_update()
        assert result == 1

    @patch("content_updater.record_update")
    @patch("content_updater.get_upstream_commit", return_value="def5678")
    @patch("content_updater.checkout_content", return_value=(True, []))
    @patch("content_updater.get_deleted_files_in_upstream", return_value=[])
    @patch("content_updater.get_changed_files", return_value=["course/test.html"])
    @patch("content_updater.get_current_commit", return_value="abc1234")
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    @patch("content_updater.is_git_repo", return_value=True)
    def test_update_no_skill_check(self, *mocks):
        """--no-skill-check で従来の強制上書きモード"""
        import content_updater
        result = content_updater.cmd_update(skill_check=False)
        assert result == 0


# ---------------------------------------------------------------------------
# cmd_rollback
# ---------------------------------------------------------------------------

class TestCmdRollback:
    @patch("content_updater.run_git")
    def test_rollback_success(self, mock_git, tmp_path):
        import content_updater
        original_log = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "work" / "log.json"

        try:
            mock_git.return_value = _make_completed()

            log = [{
                "timestamp": "2026-03-16_120000",
                "before_commit": "abc1234",
                "after_commit": "def5678",
                "files_updated": 2,
                "changed_files": ["course/test.html"],
                "backup_dir": None,
            }]
            content_updater.save_update_log(log)

            result = content_updater.cmd_rollback()
            assert result == 0

            # Verify the log entry is marked as rolled_back
            updated_log = content_updater.load_update_log()
            assert updated_log[-1]["type"] == "rolled_back"
        finally:
            content_updater.UPDATE_LOG_FILE = original_log

    def test_rollback_no_log(self, tmp_path):
        import content_updater
        original_log = content_updater.UPDATE_LOG_FILE
        content_updater.UPDATE_LOG_FILE = tmp_path / "nonexistent" / "log.json"

        try:
            result = content_updater.cmd_rollback()
            assert result == 1
        finally:
            content_updater.UPDATE_LOG_FILE = original_log

    @patch("content_updater.run_git")
    def test_rollback_restores_backup(self, mock_git, tmp_path):
        import content_updater
        original_log = content_updater.UPDATE_LOG_FILE
        original_root = content_updater.PROJECT_ROOT
        content_updater.UPDATE_LOG_FILE = tmp_path / "work" / "log.json"
        content_updater.PROJECT_ROOT = tmp_path

        try:
            mock_git.return_value = _make_completed()

            # Create backup
            backup_dir = tmp_path / "work" / ".backup" / "test"
            backup_file = backup_dir / "course" / "exercises" / "test.md"
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            backup_file.write_text("backed up content")

            log = [{
                "timestamp": "2026-03-16_120000",
                "before_commit": "abc1234",
                "after_commit": "def5678",
                "files_updated": 1,
                "changed_files": ["course/exercises/test.md"],
                "backup_dir": str(backup_dir),
            }]
            content_updater.save_update_log(log)

            result = content_updater.cmd_rollback()
            assert result == 0

            # Verify backup was restored
            restored = tmp_path / "course" / "exercises" / "test.md"
            assert restored.exists()
            assert restored.read_text() == "backed up content"
        finally:
            content_updater.UPDATE_LOG_FILE = original_log
            content_updater.PROJECT_ROOT = original_root


# ---------------------------------------------------------------------------
# cmd_dry_run
# ---------------------------------------------------------------------------

class TestCmdDryRun:
    @patch("content_updater.get_deleted_files_in_upstream", return_value=[])
    @patch("content_updater.get_new_files_in_upstream", return_value=[])
    @patch("content_updater.get_changed_files", return_value=[])
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    def test_no_changes(self, *mocks):
        import content_updater
        result = content_updater.cmd_dry_run()
        assert result == 0

    @patch("content_updater.get_deleted_files_in_upstream", return_value=["tools/old.py"])
    @patch("content_updater.get_new_files_in_upstream", return_value=["course/new.html"])
    @patch("content_updater.get_changed_files", return_value=["course/new.html", "CLAUDE.md"])
    @patch("content_updater.fetch_upstream", return_value=True)
    @patch("content_updater.has_upstream", return_value=True)
    def test_with_changes(self, *mocks):
        import content_updater
        result = content_updater.cmd_dry_run()
        assert result == 0

    @patch("content_updater.has_upstream", return_value=False)
    def test_no_upstream(self, mock_has):
        import content_updater
        result = content_updater.cmd_dry_run()
        assert result == 1


# ---------------------------------------------------------------------------
# CONTENT_PATHS validation
# ---------------------------------------------------------------------------

class TestConstants:
    def test_content_paths_not_empty(self):
        from content_updater import CONTENT_PATHS
        assert len(CONTENT_PATHS) > 0

    def test_backup_paths_subset_of_content(self):
        from content_updater import CONTENT_PATHS, BACKUP_BEFORE_UPDATE
        for bp in BACKUP_BEFORE_UPDATE:
            assert any(bp.startswith(cp) for cp in CONTENT_PATHS), \
                f"BACKUP_BEFORE_UPDATE '{bp}' is not within CONTENT_PATHS"

    def test_skill_paths_defined(self):
        from content_updater import SKILL_PATHS, NON_SKILL_CONTENT_PATHS
        assert len(SKILL_PATHS) > 0
        assert len(NON_SKILL_CONTENT_PATHS) > 0
        # skill paths should not be in non-skill paths
        for sp in SKILL_PATHS:
            assert sp not in NON_SKILL_CONTENT_PATHS


# ---------------------------------------------------------------------------
# _sanitize_url edge cases
# ---------------------------------------------------------------------------

class TestSanitizeUrlEdge:
    def test_url_with_port(self):
        from content_updater import _sanitize_url
        url = "https://user:pass@host.com:8080/path"
        result = _sanitize_url(url)
        assert "pass" not in result
        assert "8080" in result

    def test_ssh_url_unchanged(self):
        from content_updater import _sanitize_url
        url = "git@github.com:user/repo.git"
        assert _sanitize_url(url) == url


# ---------------------------------------------------------------------------
# get_upstream_url / get_current_commit / get_upstream_commit
# ---------------------------------------------------------------------------

class TestUpstreamHelpers:
    @patch("content_updater.has_upstream", return_value=False)
    def test_get_upstream_url_no_upstream(self, mock_has):
        from content_updater import get_upstream_url
        assert get_upstream_url() is None

    @patch("content_updater.run_git")
    @patch("content_updater.has_upstream", return_value=True)
    def test_get_upstream_url_success(self, mock_has, mock_git):
        from content_updater import get_upstream_url
        mock_git.return_value = _make_completed(stdout="https://github.com/org/repo.git\n")
        assert get_upstream_url() == "https://github.com/org/repo.git"

    @patch("content_updater.run_git")
    @patch("content_updater.has_upstream", return_value=True)
    def test_get_upstream_url_error(self, mock_has, mock_git):
        from content_updater import get_upstream_url
        mock_git.return_value = _make_completed(returncode=1)
        assert get_upstream_url() is None

    @patch("content_updater.run_git")
    def test_get_current_commit_success(self, mock_git):
        from content_updater import get_current_commit
        mock_git.return_value = _make_completed(stdout="abc1234\n")
        assert get_current_commit() == "abc1234"

    @patch("content_updater.run_git")
    def test_get_current_commit_error(self, mock_git):
        from content_updater import get_current_commit
        mock_git.return_value = _make_completed(returncode=1)
        assert get_current_commit() is None

    @patch("content_updater.run_git")
    def test_get_upstream_commit_success(self, mock_git):
        from content_updater import get_upstream_commit
        mock_git.return_value = _make_completed(stdout="def5678\n")
        assert get_upstream_commit() == "def5678"

    @patch("content_updater.run_git")
    def test_get_upstream_commit_error(self, mock_git):
        from content_updater import get_upstream_commit
        mock_git.return_value = _make_completed(returncode=1)
        assert get_upstream_commit() is None


# ---------------------------------------------------------------------------
# get_merge_base
# ---------------------------------------------------------------------------

class TestGetMergeBase:
    @patch("content_updater.run_git")
    def test_merge_base_success(self, mock_git):
        from content_updater import get_merge_base
        mock_git.return_value = _make_completed(stdout="merge123\n")
        assert get_merge_base() == "merge123"

    @patch("content_updater.run_git")
    def test_merge_base_failure(self, mock_git):
        from content_updater import get_merge_base
        mock_git.return_value = _make_completed(returncode=1)
        assert get_merge_base() is None


# ---------------------------------------------------------------------------
# checkout_content_paths
# ---------------------------------------------------------------------------

class TestCheckoutContentPaths:
    @patch("content_updater.run_git")
    def test_all_success(self, mock_git):
        from content_updater import checkout_content_paths
        mock_git.return_value = _make_completed()
        success, failed = checkout_content_paths(["course/", "tools/"])
        assert success is True
        assert failed == []

    @patch("content_updater.run_git")
    def test_pathspec_error_skipped(self, mock_git):
        from content_updater import checkout_content_paths
        def side_effect(*args, **kwargs):
            if args[3] == "missing/":
                return _make_completed(returncode=1, stderr="error: pathspec 'missing/' did not match")
            return _make_completed()
        mock_git.side_effect = side_effect
        success, failed = checkout_content_paths(["course/", "missing/"])
        assert success is True
        assert failed == []

    @patch("content_updater.run_git")
    def test_all_fail(self, mock_git):
        from content_updater import checkout_content_paths
        mock_git.return_value = _make_completed(returncode=1, stderr="fatal error")
        success, failed = checkout_content_paths(["course/"])
        assert success is False


# ---------------------------------------------------------------------------
# resolve_skill_conflicts
# ---------------------------------------------------------------------------

class TestResolveSkillConflicts:
    def test_keep_mine_strategy(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict", "skills/b/": "conflict"}
        result = resolve_skill_conflicts(conflicts, "keep-mine")
        assert all(v == "keep_mine" for v in result.values())

    def test_take_upstream_strategy(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict"}
        result = resolve_skill_conflicts(conflicts, "take-upstream")
        assert result["skills/a/"] == "take_upstream"

    def test_keep_both_strategy(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict"}
        result = resolve_skill_conflicts(conflicts, "keep-both")
        assert result["skills/a/"] == "keep_both"

    def test_invalid_strategy_raises(self):
        from content_updater import resolve_skill_conflicts
        with pytest.raises(ValueError, match="Invalid strategy"):
            resolve_skill_conflicts({"s/": "conflict"}, "invalid")


# ---------------------------------------------------------------------------
# show_skill_diff
# ---------------------------------------------------------------------------

class TestShowSkillDiff:
    @patch("content_updater.run_git")
    def test_diff_success(self, mock_git):
        from content_updater import show_skill_diff
        mock_git.return_value = _make_completed(stdout="+new line\n-old line\n")
        result = show_skill_diff("skills/test/")
        assert "+new line" in result

    @patch("content_updater.run_git")
    def test_diff_failure(self, mock_git):
        from content_updater import show_skill_diff
        mock_git.return_value = _make_completed(returncode=1)
        result = show_skill_diff("skills/test/")
        assert "差分を取得できませんでした" in result
