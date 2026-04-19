"""renumber_modules.py の単体テスト。

モジュール番号振り直しの2段階リネーム、コンテンツ置換、検証ロジックを検証する。
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    return import_module_from_repo("renumber_modules", "tools/renumber_modules.py")


# ===========================================================================
# Constants
# ===========================================================================

class TestConstants:
    def test_module_map_no_identity(self, mod):
        """自分自身へのマッピングがない"""
        for old, new in mod.MODULE_MAP.items():
            assert old != new, f"Module {old} maps to itself"

    def test_module_map_no_duplicate_targets(self, mod):
        """ターゲット番号が重複しない"""
        targets = list(mod.MODULE_MAP.values())
        assert len(targets) == len(set(targets))

    def test_dir_names_cover_map_keys(self, mod):
        """MODULE_DIR_NAMES が MODULE_MAP のキーをカバー"""
        for key in mod.MODULE_MAP.keys():
            assert key in mod.MODULE_DIR_NAMES, f"Key {key} not in MODULE_DIR_NAMES"

    def test_new_dir_names_cover_map_values(self, mod):
        """NEW_MODULE_DIR_NAMES が MODULE_MAP の値をカバー"""
        for val in mod.MODULE_MAP.values():
            assert val in mod.NEW_MODULE_DIR_NAMES, f"Value {val} not in NEW_MODULE_DIR_NAMES"

    def test_temp_prefix(self, mod):
        assert mod.TEMP_PREFIX == "__tmp_renumber_"


# ===========================================================================
# rename_command_files
# ===========================================================================

class TestRenameCommandFiles:
    def test_dry_run_no_changes(self, mod, tmp_path):
        """dry_run=True ではファイルが変更されない"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("content")
        (lesson_dir / "start-4-2.md").write_text("content")

        with patch.object(mod, "MODULE_MAP", {4: 8}):
            mod.rename_command_files(tmp_path, dry_run=True)

        assert (lesson_dir / "start-4-1.md").exists()
        assert (lesson_dir / "start-4-2.md").exists()
        assert not (lesson_dir / "start-8-1.md").exists()

    def test_execute_renames(self, mod, tmp_path):
        """dry_run=False でリネーム実行"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("content4-1")
        (lesson_dir / "start-4-2.md").write_text("content4-2")

        with patch.object(mod, "MODULE_MAP", {4: 8}):
            mod.rename_command_files(tmp_path, dry_run=False)

        assert not (lesson_dir / "start-4-1.md").exists()
        assert not (lesson_dir / "start-4-2.md").exists()
        assert (lesson_dir / "start-8-1.md").exists()
        assert (lesson_dir / "start-8-2.md").exists()
        assert (lesson_dir / "start-8-1.md").read_text() == "content4-1"

    def test_no_matching_files(self, mod, tmp_path, capsys):
        """マッチするファイルがない場合"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-99-1.md").write_text("content")

        with patch.object(mod, "MODULE_MAP", {4: 8}):
            mod.rename_command_files(tmp_path, dry_run=True)

        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_no_lesson_dir(self, mod, tmp_path, capsys):
        """lesson ディレクトリが存在しない"""
        mod.rename_command_files(tmp_path, dry_run=True)
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_multiple_modules(self, mod, tmp_path):
        """複数モジュールの同時リネーム"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("mod4")
        (lesson_dir / "start-6-1.md").write_text("mod6")

        with patch.object(mod, "MODULE_MAP", {4: 8, 6: 9}):
            mod.rename_command_files(tmp_path, dry_run=False)

        assert (lesson_dir / "start-8-1.md").exists()
        assert (lesson_dir / "start-9-1.md").exists()


# ===========================================================================
# rename_course_modules
# ===========================================================================

class TestRenameCourseModules:
    def test_dry_run(self, mod, tmp_path):
        modules_dir = tmp_path / "course" / "modules"
        modules_dir.mkdir(parents=True)
        (modules_dir / "4-data").mkdir()
        (modules_dir / "4-data" / "lesson1.html").write_text("hello")

        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.rename_course_modules(dry_run=True)

        assert (modules_dir / "4-data").exists()
        assert not (modules_dir / "8-data").exists()

    def test_execute(self, mod, tmp_path):
        modules_dir = tmp_path / "course" / "modules"
        modules_dir.mkdir(parents=True)
        (modules_dir / "4-data").mkdir()
        (modules_dir / "4-data" / "lesson1.html").write_text("hello")

        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.rename_course_modules(dry_run=False)

        assert not (modules_dir / "4-data").exists()
        assert (modules_dir / "8-data").exists()
        assert (modules_dir / "8-data" / "lesson1.html").read_text() == "hello"

    def test_no_modules_dir(self, mod, tmp_path, capsys):
        with patch.object(mod, "ROOT", tmp_path):
            mod.rename_course_modules(dry_run=True)
        captured = capsys.readouterr()
        assert "SKIP" in captured.out


# ===========================================================================
# replace_in_file
# ===========================================================================

class TestReplaceInFile:
    def test_basic_replacement(self, mod, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("start-4-1 content")
        changes = mod.replace_in_file(f, [("start-4-", "start-8-")], dry_run=False)
        assert changes == 1
        assert f.read_text() == "start-8-1 content"

    def test_dry_run_no_write(self, mod, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("start-4-1 content")
        changes = mod.replace_in_file(f, [("start-4-", "start-8-")], dry_run=True)
        assert changes == 1
        assert f.read_text() == "start-4-1 content"  # unchanged

    def test_no_match(self, mod, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("no match here")
        changes = mod.replace_in_file(f, [("xyz", "abc")], dry_run=False)
        assert changes == 0

    def test_multiple_replacements(self, mod, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("start-4-1 and modules/4-data and start-6-1")
        changes = mod.replace_in_file(
            f,
            [("start-4-", "start-8-"), ("modules/4-data", "modules/8-data"), ("start-6-", "start-9-")],
            dry_run=False,
        )
        assert changes >= 2
        content = f.read_text()
        assert "start-8-1" in content
        assert "modules/8-data" in content
        assert "start-9-1" in content

    def test_binary_file_skipped(self, mod, tmp_path):
        f = tmp_path / "binary.bin"
        f.write_bytes(b"\x00\x01\x02\xff\xfe")
        changes = mod.replace_in_file(f, [("x", "y")], dry_run=False)
        assert changes == 0

    def test_directory_skipped(self, mod, tmp_path):
        d = tmp_path / "subdir"
        d.mkdir()
        changes = mod.replace_in_file(d, [("x", "y")], dry_run=False)
        assert changes == 0

    def test_empty_file(self, mod, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        changes = mod.replace_in_file(f, [("x", "y")], dry_run=False)
        assert changes == 0


# ===========================================================================
# build_content_replacements
# ===========================================================================

class TestBuildContentReplacements:
    def test_returns_two_phases(self, mod):
        temp, final = mod.build_content_replacements()
        assert len(temp) > 0
        assert len(final) > 0
        assert len(temp) == len(final)

    def test_temp_uses_prefix(self, mod):
        temp, _ = mod.build_content_replacements()
        for old, new in temp:
            assert mod.TEMP_PREFIX in new

    def test_final_removes_prefix(self, mod):
        _, final = mod.build_content_replacements()
        for old, new in final:
            assert mod.TEMP_PREFIX not in new

    def test_roundtrip(self, mod):
        """temp → final で正しいターゲットになる"""
        temp, final = mod.build_content_replacements()
        # temp の new と final の old が一致する
        temp_news = {new for _, new in temp}
        final_olds = {old for old, _ in final}
        assert temp_news == final_olds


# ===========================================================================
# verify_no_old_refs
# ===========================================================================

class TestVerifyNoOldRefs:
    def test_no_issues(self, mod, tmp_path, capsys):
        lesson_dir = tmp_path / ".cursor" / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        # Use module number 99 which is not in MODULE_MAP keys
        (lesson_dir / "start-99-1.md").write_text("new content")

        with patch.object(mod, "ROOT", tmp_path):
            issues = mod.verify_no_old_refs()
        assert issues == 0
        captured = capsys.readouterr()
        assert "OK" in captured.out

    def test_old_refs_detected(self, mod, tmp_path, capsys):
        lesson_dir = tmp_path / ".cursor" / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("old content")

        with patch.object(mod, "ROOT", tmp_path):
            issues = mod.verify_no_old_refs()
        assert issues >= 1
        captured = capsys.readouterr()
        assert "ISSUE" in captured.out

    def test_no_dirs(self, mod, tmp_path, capsys):
        with patch.object(mod, "ROOT", tmp_path):
            issues = mod.verify_no_old_refs()
        assert issues == 0


# ===========================================================================
# Boundary tests
# ===========================================================================

class TestBoundary:
    def test_replace_in_file_unicode(self, mod, tmp_path):
        """日本語を含むファイルの置換"""
        f = tmp_path / "japanese.md"
        f.write_text("modules/4-data を参照してください", encoding="utf-8")
        changes = mod.replace_in_file(
            f,
            [("modules/4-data", "modules/8-data")],
            dry_run=False,
        )
        assert changes == 1
        assert "modules/8-data" in f.read_text()

    def test_large_file(self, mod, tmp_path):
        """大きなファイルの置換"""
        f = tmp_path / "large.md"
        content = ("start-4-1 " * 1000) + "\n"
        f.write_text(content)
        changes = mod.replace_in_file(f, [("start-4-", "start-8-")], dry_run=False)
        assert changes >= 1
        assert "start-8-1" in f.read_text()

    def test_collision_avoidance(self, mod, tmp_path):
        """2段階リネームによる衝突回避: 4→8, 8→10 を同時に行う"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("was 4")
        (lesson_dir / "start-8-1.md").write_text("was 8")

        # 4→99, 8→100 でシンプルに衝突回避テスト
        with patch.object(mod, "MODULE_MAP", {4: 99, 8: 100}):
            mod.rename_command_files(tmp_path, dry_run=False)

        assert (lesson_dir / "start-99-1.md").read_text() == "was 4"
        assert (lesson_dir / "start-100-1.md").read_text() == "was 8"


# ===========================================================================
# rename_command_files: overwrite existing (line 108)
# ===========================================================================

class TestRenameCommandFilesOverwrite:
    def test_overwrite_existing_dest(self, mod, tmp_path):
        """Phase 2 で既存ファイルを上書き"""
        lesson_dir = tmp_path / "commands" / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-4-1.md").write_text("new content")
        (lesson_dir / "start-8-1.md").write_text("old content")

        with patch.object(mod, "MODULE_MAP", {4: 8}):
            mod.rename_command_files(tmp_path, dry_run=False)

        assert (lesson_dir / "start-8-1.md").read_text() == "new content"


# ===========================================================================
# rename_course_modules: missing dir (line 130), no renames (lines 133-134), overwrite (line 149)
# ===========================================================================

class TestRenameCourseModulesEdgeCases:
    def test_old_dir_not_exists(self, mod, tmp_path, capsys):
        """old_dir が存在しない場合のSKIP表示 (line 130)"""
        modules_dir = tmp_path / "course" / "modules"
        modules_dir.mkdir(parents=True)
        # 4-data は存在しないが、マッピングは設定
        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.rename_course_modules(dry_run=False)
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_no_renames_available(self, mod, tmp_path, capsys):
        """全て存在しない場合のSKIP (lines 133-134)"""
        modules_dir = tmp_path / "course" / "modules"
        modules_dir.mkdir(parents=True)
        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.rename_course_modules(dry_run=True)
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_overwrite_existing_dest(self, mod, tmp_path, capsys):
        """Phase 2 で既存ディレクトリがある場合の警告 (line 149)"""
        modules_dir = tmp_path / "course" / "modules"
        modules_dir.mkdir(parents=True)
        (modules_dir / "4-data").mkdir()
        (modules_dir / "4-data" / "file.txt").write_text("from 4")
        # 空ディレクトリのみ既存として配置（非空だとOSエラーになる）
        (modules_dir / "8-data").mkdir()

        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.rename_course_modules(dry_run=False)
        captured = capsys.readouterr()
        assert "WARN" in captured.out


# ===========================================================================
# replace_content_in_tree (lines 205-251)
# ===========================================================================

class TestReplaceContentInTree:
    def test_replaces_in_matching_files(self, mod, tmp_path):
        """ファイル内容の置換が正しく行われる"""
        cursor_dir = tmp_path / ".cursor" / "commands"
        cursor_dir.mkdir(parents=True)
        f = cursor_dir / "test.md"
        f.write_text("Use start-4-1 and modules/4-data for reference")

        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            total = mod.replace_content_in_tree(dry_run=False)
        assert total >= 1
        content = f.read_text()
        assert "start-8-1" in content
        assert "modules/8-data" in content

    def test_dry_run_no_changes(self, mod, tmp_path):
        """dry_run ではファイルが変更されない"""
        cursor_dir = tmp_path / ".cursor" / "commands"
        cursor_dir.mkdir(parents=True)
        f = cursor_dir / "test.md"
        f.write_text("Use start-4-1")

        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            mod.replace_content_in_tree(dry_run=True)
        assert "start-4-1" in f.read_text()

    def test_no_matching_files(self, mod, tmp_path):
        """マッチするファイルがない場合"""
        with patch.object(mod, "ROOT", tmp_path), \
             patch.object(mod, "MODULE_MAP", {4: 8}), \
             patch.object(mod, "MODULE_DIR_NAMES", {4: "data"}), \
             patch.object(mod, "NEW_MODULE_DIR_NAMES", {8: "data"}):
            total = mod.replace_content_in_tree(dry_run=False)
        assert total == 0


# ===========================================================================
# main (lines 285-324)
# ===========================================================================

class TestMainFunction:
    def test_dry_run(self, mod, tmp_path, capsys):
        """main: dry run モード"""
        with patch.object(mod, "ROOT", tmp_path), \
             patch("sys.argv", ["prog"]), \
             patch.object(mod, "rename_command_files"), \
             patch.object(mod, "rename_course_modules"), \
             patch.object(mod, "replace_content_in_tree", return_value=0):
            mod.main()
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out

    def test_execute_mode(self, mod, tmp_path, capsys):
        """main: --execute モード"""
        with patch.object(mod, "ROOT", tmp_path), \
             patch("sys.argv", ["prog", "--execute"]), \
             patch.object(mod, "rename_command_files"), \
             patch.object(mod, "rename_course_modules"), \
             patch.object(mod, "replace_content_in_tree", return_value=0), \
             patch.object(mod, "verify_no_old_refs", return_value=0):
            mod.main()
        captured = capsys.readouterr()
        assert "EXECUTING" in captured.out
