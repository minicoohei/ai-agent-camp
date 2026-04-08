"""tests for tools/i18n_install.py — Phase 4: install translated files"""

from pathlib import Path

import pytest

from tests.conftest import import_module_from_repo

_MOD_PATH = "tools/i18n_install.py"
_COMMON_PATH = "tools/i18n_common.py"


@pytest.fixture
def mod():
    import_module_from_repo("i18n_common", _COMMON_PATH)
    return import_module_from_repo("i18n_install", _MOD_PATH)


def _setup_dist(tmp_path, lang="en"):
    """dist/{lang}/ にダミー翻訳ファイルを作成"""
    dist = tmp_path / "dist" / lang

    # .claude/commands/
    cmd = dist / ".claude" / "commands" / "lesson"
    cmd.mkdir(parents=True)
    (cmd / "start-1-1.md").write_text("# Lesson 1-1\n", encoding="utf-8")

    # skills/
    skill = dist / "skills" / "aiagent-guide"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Guide Skill\n", encoding="utf-8")

    return dist


# ===========================================================================
# install_lang — 基本動作
# ===========================================================================


class TestInstallBasic:
    def test_copies_files_to_root(self, mod, tmp_path):
        """ファイルが ROOT_DIR にコピーされる"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            result = mod.install_lang("en")

        assert result["copied"] == 2
        work = tmp_path / "work"
        assert (work / ".claude" / "commands" / "lesson" / "start-1-1.md").exists()
        assert (work / "skills" / "aiagent-guide" / "SKILL.md").exists()

    def test_creates_lang_marker(self, mod, tmp_path):
        """.aiagent-lang マーカーが作成される"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            mod.install_lang("en")

        marker = tmp_path / "work" / ".aiagent-lang"
        assert marker.exists()
        assert marker.read_text(encoding="utf-8") == "en"

    def test_preserves_directory_structure(self, mod, tmp_path):
        """ディレクトリ構造が保持される"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            mod.install_lang("en")

        assert (tmp_path / "work" / ".claude" / "commands" / "lesson").is_dir()
        assert (tmp_path / "work" / "skills" / "aiagent-guide").is_dir()

    def test_file_content_matches(self, mod, tmp_path):
        """コピー後のファイル内容が一致"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            mod.install_lang("en")

        content = (tmp_path / "work" / ".claude" / "commands" / "lesson" / "start-1-1.md").read_text(encoding="utf-8")
        assert content == "# Lesson 1-1\n"


# ===========================================================================
# install_lang — backup
# ===========================================================================


class TestInstallBackup:
    def test_backup_creates_bak_files(self, mod, tmp_path):
        """--backup で .bak ファイルが作成される"""
        _setup_dist(tmp_path)
        work = tmp_path / "work"
        # 既存ファイルを配置
        existing = work / ".claude" / "commands" / "lesson" / "start-1-1.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("# Old content\n", encoding="utf-8")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", work)
            result = mod.install_lang("en", backup=True)

        assert result["backed_up"] >= 1
        bak = existing.with_suffix(".md.bak")
        assert bak.exists()
        assert bak.read_text(encoding="utf-8") == "# Old content\n"

    def test_backup_does_not_create_bak_for_new_files(self, mod, tmp_path):
        """新規ファイルには .bak を作成しない"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            result = mod.install_lang("en", backup=True)

        assert result["backed_up"] == 0
        assert result["copied"] == 2


# ===========================================================================
# install_lang — エッジケース
# ===========================================================================


class TestInstallEdgeCases:
    def test_missing_dist_returns_empty(self, mod, tmp_path):
        """dist/{lang}/ が存在しない場合、何もコピーしない"""
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            result = mod.install_lang("xx")

        assert result["copied"] == 0

    def test_dry_run_no_changes(self, mod, tmp_path):
        """dry-run ではファイルが作成されない"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            result = mod.install_lang("en", dry_run=True)

        assert result["copied"] > 0
        assert not (tmp_path / "work").exists()

    def test_idempotent(self, mod, tmp_path):
        """2回実行しても壊れない"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ROOT_DIR", tmp_path / "work")
            r1 = mod.install_lang("en")
            r2 = mod.install_lang("en")

        assert r1["copied"] == r2["copied"]
        content = (tmp_path / "work" / ".claude" / "commands" / "lesson" / "start-1-1.md").read_text(encoding="utf-8")
        assert content == "# Lesson 1-1\n"
