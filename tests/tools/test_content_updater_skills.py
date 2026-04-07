"""content_updater.py のスキルコンフリクト処理テスト。

classify_skill_changes, resolve_skill_conflicts, apply_skill_decisions,
update_skills, checkout_content_paths の各関数を検証する。
"""
import shutil
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest


def _make_completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr,
    )


# ---------------------------------------------------------------------------
# 定数の検証
# ---------------------------------------------------------------------------

class TestSkillConstants:
    def test_skill_paths_defined(self):
        from content_updater import SKILL_PATHS
        assert ".claude/skills/" in SKILL_PATHS
        assert "skills/" in SKILL_PATHS

    def test_non_skill_paths_excludes_skills(self):
        from content_updater import NON_SKILL_CONTENT_PATHS, SKILL_PATHS
        for sp in SKILL_PATHS:
            assert sp not in NON_SKILL_CONTENT_PATHS

    def test_non_skill_plus_skill_covers_all(self):
        from content_updater import CONTENT_PATHS, NON_SKILL_CONTENT_PATHS, SKILL_PATHS
        combined = set(NON_SKILL_CONTENT_PATHS) | set(SKILL_PATHS)
        assert combined == set(CONTENT_PATHS)


# ---------------------------------------------------------------------------
# get_merge_base
# ---------------------------------------------------------------------------

class TestGetMergeBase:
    @patch("content_updater.run_git")
    def test_success(self, mock_git):
        from content_updater import get_merge_base
        mock_git.return_value = _make_completed(stdout="abc123def456\n")
        result = get_merge_base()
        assert result == "abc123def456"

    @patch("content_updater.run_git")
    def test_failure(self, mock_git):
        from content_updater import get_merge_base
        mock_git.return_value = _make_completed(returncode=1)
        result = get_merge_base()
        assert result is None


# ---------------------------------------------------------------------------
# list_skill_dirs
# ---------------------------------------------------------------------------

class TestListSkillDirs:
    @patch("content_updater.run_git")
    def test_combines_local_and_upstream(self, mock_git, tmp_path):
        import content_updater
        original = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            # ローカルにスキルを作成
            (tmp_path / "skills" / "local-skill").mkdir(parents=True)
            (tmp_path / "skills" / "shared-skill").mkdir(parents=True)

            # upstream にも存在するスキル（ls-tree）
            mock_git.return_value = _make_completed(
                stdout="shared-skill\nupstream-only-skill\n"
            )

            result = content_updater.list_skill_dirs("skills/")
            assert "skills/local-skill/" in result
            assert "skills/shared-skill/" in result
            assert "skills/upstream-only-skill/" in result
        finally:
            content_updater.PROJECT_ROOT = original

    @patch("content_updater.run_git")
    def test_excludes_hidden_dirs(self, mock_git, tmp_path):
        import content_updater
        original = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            (tmp_path / "skills" / ".hidden").mkdir(parents=True)
            (tmp_path / "skills" / "visible").mkdir(parents=True)
            mock_git.return_value = _make_completed(stdout="")

            result = content_updater.list_skill_dirs("skills/")
            assert "skills/visible/" in result
            assert "skills/.hidden/" not in result
        finally:
            content_updater.PROJECT_ROOT = original

    @patch("content_updater.run_git")
    def test_empty_skill_base(self, mock_git, tmp_path):
        import content_updater
        original = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            mock_git.return_value = _make_completed(returncode=1)
            result = content_updater.list_skill_dirs("skills/")
            assert result == []
        finally:
            content_updater.PROJECT_ROOT = original


# ---------------------------------------------------------------------------
# classify_skill_changes
# ---------------------------------------------------------------------------

class TestClassifySkillChanges:
    @patch("content_updater.list_skill_dirs", return_value=["skills/skill-a/"])
    @patch("content_updater.run_git")
    def test_unchanged(self, mock_git, mock_list):
        from content_updater import classify_skill_changes
        # All diffs return empty
        mock_git.return_value = _make_completed(stdout="")
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result == {"skills/skill-a/": "unchanged"}

    @patch("content_updater.list_skill_dirs", return_value=["skills/skill-a/"])
    @patch("content_updater.run_git")
    def test_upstream_only(self, mock_git, mock_list):
        from content_updater import classify_skill_changes

        def side_effect(*args, **kwargs):
            git_args = args
            # merge_base..HEAD (local) → empty
            if "abc123..HEAD" in git_args:
                return _make_completed(stdout="")
            # unstaged → empty
            if git_args == ("diff", "--name-only", "--", "skills/skill-a/"):
                return _make_completed(stdout="")
            # merge_base..upstream/main (upstream) → has changes
            if "abc123..upstream/main" in git_args:
                return _make_completed(stdout="skills/skill-a/SKILL.md\n")
            return _make_completed(stdout="")

        mock_git.side_effect = side_effect
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result == {"skills/skill-a/": "upstream_only"}

    @patch("content_updater.list_skill_dirs", return_value=["skills/skill-a/"])
    @patch("content_updater.run_git")
    def test_local_only(self, mock_git, mock_list):
        from content_updater import classify_skill_changes

        def side_effect(*args, **kwargs):
            if "abc123..HEAD" in args:
                return _make_completed(stdout="skills/skill-a/scripts/main.py\n")
            if "abc123..upstream/main" in args:
                return _make_completed(stdout="")
            return _make_completed(stdout="")

        mock_git.side_effect = side_effect
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result == {"skills/skill-a/": "local_only"}

    @patch("content_updater.list_skill_dirs", return_value=["skills/skill-a/"])
    @patch("content_updater.run_git")
    def test_conflict(self, mock_git, mock_list):
        from content_updater import classify_skill_changes

        def side_effect(*args, **kwargs):
            if "abc123..HEAD" in args:
                return _make_completed(stdout="skills/skill-a/scripts/main.py\n")
            if "abc123..upstream/main" in args:
                return _make_completed(stdout="skills/skill-a/SKILL.md\n")
            return _make_completed(stdout="")

        mock_git.side_effect = side_effect
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result == {"skills/skill-a/": "conflict"}

    @patch("content_updater.list_skill_dirs", return_value=["skills/skill-a/"])
    @patch("content_updater.run_git")
    def test_unstaged_changes_detected(self, mock_git, mock_list):
        """uncommitted な変更もローカル変更として検出する"""
        from content_updater import classify_skill_changes

        call_count = {"n": 0}

        def side_effect(*args, **kwargs):
            call_count["n"] += 1
            # merge_base..HEAD → empty (no commits)
            if "abc123..HEAD" in args:
                return _make_completed(stdout="")
            # unstaged diff → has changes
            if args == ("diff", "--name-only", "--", "skills/skill-a/"):
                return _make_completed(stdout="skills/skill-a/SKILL.md\n")
            # upstream → has changes
            if "abc123..upstream/main" in args:
                return _make_completed(stdout="skills/skill-a/SKILL.md\n")
            return _make_completed(stdout="")

        mock_git.side_effect = side_effect
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result == {"skills/skill-a/": "conflict"}

    @patch("content_updater.list_skill_dirs", return_value=[
        "skills/a/", "skills/b/", "skills/c/",
    ])
    @patch("content_updater.run_git")
    def test_multiple_skills(self, mock_git, mock_list):
        from content_updater import classify_skill_changes

        def side_effect(*args, **kwargs):
            path = args[-1] if args else ""
            if "abc123..HEAD" in args and path == "skills/b/":
                return _make_completed(stdout="skills/b/x.py\n")
            if "abc123..upstream/main" in args and path == "skills/c/":
                return _make_completed(stdout="skills/c/y.py\n")
            return _make_completed(stdout="")

        mock_git.side_effect = side_effect
        result = classify_skill_changes("skills/", merge_base="abc123")
        assert result["skills/a/"] == "unchanged"
        assert result["skills/b/"] == "local_only"
        assert result["skills/c/"] == "upstream_only"

    @patch("content_updater.list_skill_dirs", return_value=["skills/x/"])
    def test_no_merge_base_defaults_upstream_only(self, mock_list):
        from content_updater import classify_skill_changes
        result = classify_skill_changes("skills/", merge_base=None)
        assert result == {"skills/x/": "upstream_only"}


# ---------------------------------------------------------------------------
# resolve_skill_conflicts
# ---------------------------------------------------------------------------

class TestResolveSkillConflicts:
    def test_strategy_keep_mine(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict", "skills/b/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="keep-mine")
        assert result == {"skills/a/": "keep_mine", "skills/b/": "keep_mine"}

    def test_strategy_take_upstream(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="take-upstream")
        assert result == {"skills/a/": "take_upstream"}

    def test_strategy_keep_both(self):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="keep-both")
        assert result == {"skills/a/": "keep_both"}

    @patch("builtins.input", return_value="a")
    def test_strategy_ask_keep_mine(self, mock_input):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/my-skill/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="ask")
        assert result == {"skills/my-skill/": "keep_mine"}

    @patch("builtins.input", return_value="b")
    def test_strategy_ask_take_upstream(self, mock_input):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/my-skill/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="ask")
        assert result == {"skills/my-skill/": "take_upstream"}

    @patch("builtins.input", return_value="c")
    def test_strategy_ask_keep_both(self, mock_input):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/my-skill/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="ask")
        assert result == {"skills/my-skill/": "keep_both"}

    @patch("builtins.input", side_effect=EOFError)
    def test_strategy_ask_eof_defaults_keep_mine(self, mock_input):
        from content_updater import resolve_skill_conflicts
        conflicts = {"skills/a/": "conflict", "skills/b/": "conflict"}
        result = resolve_skill_conflicts(conflicts, strategy="ask")
        assert all(v == "keep_mine" for v in result.values())


# ---------------------------------------------------------------------------
# apply_skill_decisions
# ---------------------------------------------------------------------------

class TestApplySkillDecisions:
    @patch("content_updater.run_git")
    def test_keep_mine(self, mock_git):
        from content_updater import apply_skill_decisions
        updated, skipped = apply_skill_decisions(
            {"skills/my-skill/": "keep_mine"}, "2026-01-01_000000",
        )
        assert skipped == ["skills/my-skill/"]
        assert updated == []
        mock_git.assert_not_called()

    @patch("content_updater.run_git")
    def test_take_upstream(self, mock_git, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        original_backup = content_updater.BACKUP_BASE_DIR
        content_updater.PROJECT_ROOT = tmp_path
        content_updater.BACKUP_BASE_DIR = tmp_path / "work" / ".backup"

        try:
            # Create local skill
            skill_dir = tmp_path / "skills" / "my-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("local version")

            mock_git.return_value = _make_completed()

            updated, skipped = content_updater.apply_skill_decisions(
                {"skills/my-skill/": "take_upstream"}, "2026-01-01_000000",
            )
            assert "skills/my-skill/" in updated
            assert skipped == []

            # Verify backup was created
            backup = tmp_path / "work" / ".backup" / "2026-01-01_000000" / "skills" / "my-skill"
            assert backup.exists()
            assert (backup / "SKILL.md").read_text() == "local version"
        finally:
            content_updater.PROJECT_ROOT = original_root
            content_updater.BACKUP_BASE_DIR = original_backup

    @patch("content_updater.run_git")
    def test_keep_both(self, mock_git, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        content_updater.PROJECT_ROOT = tmp_path

        try:
            skill_dir = tmp_path / "skills" / "my-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("local version")

            mock_git.return_value = _make_completed()

            updated, skipped = content_updater.apply_skill_decisions(
                {"skills/my-skill/": "keep_both"}, "2026-01-01_000000",
            )
            assert "skills/my-skill/" in updated

            # Verify custom copy was created with timestamp
            custom = tmp_path / "skills" / "my-skill-custom-2026-01-01_000000"
            assert custom.exists()
            assert (custom / "SKILL.md").read_text() == "local version"
        finally:
            content_updater.PROJECT_ROOT = original_root

    @patch("content_updater.run_git")
    def test_take_upstream_git_failure(self, mock_git, tmp_path):
        import content_updater
        original_root = content_updater.PROJECT_ROOT
        original_backup = content_updater.BACKUP_BASE_DIR
        content_updater.PROJECT_ROOT = tmp_path
        content_updater.BACKUP_BASE_DIR = tmp_path / "work" / ".backup"

        try:
            skill_dir = tmp_path / "skills" / "fail-skill"
            skill_dir.mkdir(parents=True)

            mock_git.return_value = _make_completed(
                returncode=1, stderr="checkout error",
            )

            updated, skipped = content_updater.apply_skill_decisions(
                {"skills/fail-skill/": "take_upstream"}, "2026-01-01_000000",
            )
            assert updated == []
            assert "skills/fail-skill/" in skipped
        finally:
            content_updater.PROJECT_ROOT = original_root
            content_updater.BACKUP_BASE_DIR = original_backup


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
    def test_pathspec_not_found_is_skip(self, mock_git):
        from content_updater import checkout_content_paths

        def side_effect(*args, **kwargs):
            if args[3] == "courses/":
                return _make_completed(
                    returncode=1,
                    stderr="error: pathspec 'courses/' did not match any",
                )
            return _make_completed()

        mock_git.side_effect = side_effect
        success, failed = checkout_content_paths(["course/", "courses/"])
        assert success is True
        assert failed == []

    @patch("content_updater.run_git")
    def test_real_failure(self, mock_git):
        from content_updater import checkout_content_paths
        mock_git.return_value = _make_completed(
            returncode=1, stderr="fatal: permission denied",
        )
        success, failed = checkout_content_paths(["course/"])
        assert success is False


# ---------------------------------------------------------------------------
# update_skills (integration)
# ---------------------------------------------------------------------------

class TestUpdateSkills:
    @patch("content_updater.run_git")
    @patch("content_updater.classify_skill_changes")
    @patch("content_updater.get_merge_base", return_value="abc123")
    def test_auto_updates_upstream_only(self, mock_base, mock_classify, mock_git):
        from content_updater import update_skills
        mock_classify.return_value = {
            "skills/a/": "upstream_only",
            "skills/b/": "unchanged",
        }
        mock_git.return_value = _make_completed()

        updated, skipped, classifications = update_skills(
            skill_check=True, skill_strategy="ask",
        )
        assert "skills/a/" in updated
        assert classifications["skills/b/"] == "unchanged"

    @patch("content_updater.checkout_content_paths", return_value=(True, []))
    def test_no_skill_check_uses_force(self, mock_checkout):
        from content_updater import update_skills, SKILL_PATHS
        updated, skipped, classifications = update_skills(skill_check=False)
        mock_checkout.assert_called_once_with(SKILL_PATHS)
        assert classifications == {}

    @patch("content_updater.apply_skill_decisions", return_value=(["skills/x/"], []))
    @patch("content_updater.resolve_skill_conflicts", return_value={"skills/x/": "take_upstream"})
    @patch("content_updater.run_git")
    @patch("content_updater.classify_skill_changes")
    @patch("content_updater.get_merge_base", return_value="abc123")
    def test_handles_conflicts(self, mock_base, mock_classify, mock_git, mock_resolve, mock_apply):
        from content_updater import update_skills
        # First SKILL_PATH (.claude/skills/) returns no conflicts,
        # second (skills/) returns a conflict
        mock_classify.side_effect = [
            {},  # .claude/skills/ — empty
            {"skills/x/": "conflict"},  # skills/
        ]

        updated, skipped, classifications = update_skills(
            skill_check=True, skill_strategy="ask",
        )
        mock_resolve.assert_called_once()
        mock_apply.assert_called_once()
        assert "skills/x/" in updated

    @patch("content_updater.run_git")
    @patch("content_updater.classify_skill_changes")
    @patch("content_updater.get_merge_base", return_value="abc123")
    def test_strategy_keep_mine_skips_conflicts(self, mock_base, mock_classify, mock_git):
        from content_updater import update_skills
        mock_classify.return_value = {"skills/x/": "conflict"}

        updated, skipped, classifications = update_skills(
            skill_check=True, skill_strategy="keep-mine",
        )
        assert "skills/x/" in skipped
        assert updated == [] or "skills/x/" not in updated


# ---------------------------------------------------------------------------
# show_skill_diff
# ---------------------------------------------------------------------------

class TestShowSkillDiff:
    @patch("content_updater.run_git")
    def test_returns_diff(self, mock_git):
        from content_updater import show_skill_diff
        mock_git.return_value = _make_completed(stdout="diff --git a/x b/y\n+new line\n")
        result = show_skill_diff("skills/a/")
        assert "+new line" in result

    @patch("content_updater.run_git")
    def test_failure_returns_message(self, mock_git):
        from content_updater import show_skill_diff
        mock_git.return_value = _make_completed(returncode=1)
        result = show_skill_diff("skills/a/")
        assert "差分を取得できませんでした" in result
