"""tests for tools/i18n_build_zip.py — Phase 4: zip distribution"""

import zipfile
from pathlib import Path

import pytest

from tests.conftest import import_module_from_repo

_MOD_PATH = "tools/i18n_build_zip.py"
_COMMON_PATH = "tools/i18n_common.py"


@pytest.fixture
def mod():
    import_module_from_repo("i18n_common", _COMMON_PATH)
    return import_module_from_repo("i18n_build_zip", _MOD_PATH)


def _setup_dist(tmp_path, lang="en"):
    """dist/{lang}/ にダミー翻訳ファイルを作成"""
    dist = tmp_path / "dist" / lang
    # .claude/commands/
    cmd = dist / ".claude" / "commands" / "lesson"
    cmd.mkdir(parents=True)
    (cmd / "start-1-1.md").write_text("# Lesson 1-1", encoding="utf-8")

    # skills/
    skill = dist / "skills" / "aiagent-guide"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Skill", encoding="utf-8")

    return dist


def _setup_mo(tmp_path, lang="en"):
    """locales/cli/{lang}/LC_MESSAGES/aiagent.mo を作成"""
    mo_dir = tmp_path / "locales" / "cli" / lang / "LC_MESSAGES"
    mo_dir.mkdir(parents=True)
    (mo_dir / "aiagent.mo").write_bytes(b"\xde\x12\x04\x95fake-mo")
    return mo_dir


# ===========================================================================
# build_zip — 基本動作
# ===========================================================================


class TestBuildZipBasic:
    def test_creates_zip_file(self, mod, tmp_path):
        """zip ファイルが dist/zip/ に生成される"""
        _setup_dist(tmp_path)
        with (
            pytest.MonkeyPatch.context() as mp,
        ):
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        assert result["files"] > 0
        assert result["size_bytes"] > 0
        zip_path = Path(result["path"])
        assert zip_path.exists()
        assert zip_path.name == "ai-agent-camp-en.zip"

    def test_zip_contains_marker(self, mod, tmp_path):
        """.aiagent-lang マーカーが zip 内に含まれる"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        with zipfile.ZipFile(result["path"]) as zf:
            assert ".aiagent-lang" in zf.namelist()
            assert zf.read(".aiagent-lang").decode() == "en"

    def test_zip_contains_translated_files(self, mod, tmp_path):
        """翻訳済みファイルが zip に含まれる"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        with zipfile.ZipFile(result["path"]) as zf:
            names = zf.namelist()
            assert ".claude/commands/lesson/start-1-1.md" in names
            assert "skills/aiagent-guide/SKILL.md" in names

    def test_zip_contains_mo_file(self, mod, tmp_path):
        """.mo ファイルが zip に含まれる"""
        _setup_dist(tmp_path)
        _setup_mo(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        with zipfile.ZipFile(result["path"]) as zf:
            assert "locales/cli/en/LC_MESSAGES/aiagent.mo" in zf.namelist()

    def test_zip_naming_convention(self, mod, tmp_path):
        """zip ファイル名が ai-agent-camp-{lang}.zip"""
        _setup_dist(tmp_path, "es")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("es")

        assert Path(result["path"]).name == "ai-agent-camp-es.zip"

    def test_file_count_includes_marker(self, mod, tmp_path):
        """ファイル数にマーカーが含まれる (+1)"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        # 2 dist files + 1 marker = 3
        assert result["files"] == 3


# ===========================================================================
# build_zip — エッジケース
# ===========================================================================


class TestBuildZipEdgeCases:
    def test_missing_dist_returns_empty(self, mod, tmp_path):
        """dist/{lang}/ が存在しない場合、スキップ"""
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("xx")

        assert result["files"] == 0
        assert result["path"] == ""

    def test_dry_run_no_file_created(self, mod, tmp_path):
        """dry-run ではファイルが作成されない"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en", dry_run=True)

        assert result["files"] > 0
        assert result["size_bytes"] == 0
        assert result["path"] == ""
        assert not (tmp_path / "dist" / "zip").exists()

    def test_no_mo_still_builds(self, mod, tmp_path):
        """.mo なしでも zip 生成は成功する"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "nonexistent")
            result = mod.build_zip("en")

        assert result["files"] > 0
        assert Path(result["path"]).exists()

    def test_zip_is_valid(self, mod, tmp_path):
        """生成された zip が有効な ZIP ファイルである"""
        _setup_dist(tmp_path)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(mod, "DIST_DIR_ROOT", tmp_path / "dist")
            mp.setattr(mod, "ZIP_DIST_DIR", tmp_path / "dist" / "zip")
            mp.setattr(mod, "CLI_LOCALES_DIR", tmp_path / "locales" / "cli")
            result = mod.build_zip("en")

        assert zipfile.is_zipfile(result["path"])
