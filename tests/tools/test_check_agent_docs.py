"""check_agent_docs.py の単体テスト。

Codex向けドキュメント検証ロジックをテストする。
"""
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

cad = import_module_from_repo("check_agent_docs", "tools/check_agent_docs.py")

_check_exists = cad._check_exists
_check_contains = cad._check_contains
main = cad.main
REQUIRED_FILES = cad.REQUIRED_FILES
TEXT_CHECKS = cad.TEXT_CHECKS


# ---------------------------------------------------------------------------
# _check_exists
# ---------------------------------------------------------------------------

class TestCheckExists:
    def test_existing_file(self, tmp_path):
        f = tmp_path / "AGENTS.md"
        f.write_text("content")
        result = _check_exists(f)
        assert result is None  # No error

    def test_missing_file(self, tmp_path):
        with patch.object(cad, "PROJECT_ROOT", tmp_path):
            result = _check_exists(tmp_path / "missing.md")
        assert result is not None
        assert "Missing" in result

    def test_directory_exists(self, tmp_path):
        # Directories also "exist"
        d = tmp_path / "docs"
        d.mkdir()
        result = _check_exists(d)
        assert result is None


# ---------------------------------------------------------------------------
# _check_contains
# ---------------------------------------------------------------------------

class TestCheckContains:
    def test_contains_needle(self, tmp_path):
        f = tmp_path / "README.md"
        f.write_text("Welcome to Codex guide")
        result = _check_contains(f, "Codex")
        assert result is None

    def test_missing_needle(self, tmp_path):
        f = tmp_path / "README.md"
        f.write_text("Welcome to the guide")
        with patch.object(cad, "PROJECT_ROOT", tmp_path):
            result = _check_contains(f, "Codex")
        assert result is not None
        assert "Missing 'Codex'" in result

    def test_missing_file(self, tmp_path):
        with patch.object(cad, "PROJECT_ROOT", tmp_path):
            result = _check_contains(tmp_path / "missing.md", "anything")
        assert result is not None
        assert "Missing required file" in result

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        with patch.object(cad, "PROJECT_ROOT", tmp_path):
            result = _check_contains(f, "something")
        assert result is not None

    def test_unicode_content(self, tmp_path):
        f = tmp_path / "jp.md"
        f.write_text("日本語コンテンツ Claude Code ガイド")
        result = _check_contains(f, "Claude Code")
        assert result is None

    def test_needle_is_empty(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("any content")
        result = _check_contains(f, "")
        assert result is None  # Empty string is always "in" any string

    def test_case_sensitive(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("codex")
        with patch.object(cad, "PROJECT_ROOT", tmp_path):
            result = _check_contains(f, "Codex")
        assert result is not None  # Case-sensitive check


# ---------------------------------------------------------------------------
# REQUIRED_FILES / TEXT_CHECKS data integrity
# ---------------------------------------------------------------------------

class TestDataIntegrity:
    def test_required_files_not_empty(self):
        assert len(REQUIRED_FILES) > 0

    def test_text_checks_not_empty(self):
        assert len(TEXT_CHECKS) > 0

    def test_all_required_files_are_paths(self):
        for f in REQUIRED_FILES:
            assert isinstance(f, Path)

    def test_all_text_checks_are_tuples(self):
        for item in TEXT_CHECKS:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], Path)
            assert isinstance(item[1], str)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestMain:
    def test_all_files_present_and_valid(self, tmp_path, capsys):
        """全ファイルが存在し、必要なテキストを含む場合、成功する"""
        # Create all required files
        required_files = []
        for orig_path in REQUIRED_FILES:
            rel = orig_path.relative_to(cad.PROJECT_ROOT)
            new_path = tmp_path / rel
            new_path.parent.mkdir(parents=True, exist_ok=True)
            new_path.write_text("Codex Claude Code Cursor sandbox approval")
            required_files.append(new_path)

        # Create all text check files
        text_checks = []
        for orig_path, needle in TEXT_CHECKS:
            rel = orig_path.relative_to(cad.PROJECT_ROOT)
            new_path = tmp_path / rel
            new_path.parent.mkdir(parents=True, exist_ok=True)
            # Write content that contains the needle
            existing = ""
            if new_path.exists():
                existing = new_path.read_text()
            if needle not in existing:
                new_path.write_text(existing + f" {needle}")
            text_checks.append((new_path, needle))

        # Patch the module-level constants
        with patch.object(cad, "REQUIRED_FILES", required_files), \
             patch.object(cad, "TEXT_CHECKS", text_checks), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 0
        assert "passed" in capsys.readouterr().out

    def test_missing_required_file(self, tmp_path, capsys):
        """必須ファイルが欠けている場合、失敗する"""
        missing = [tmp_path / "nonexistent.md"]
        with patch.object(cad, "REQUIRED_FILES", missing), \
             patch.object(cad, "TEXT_CHECKS", []), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1
        assert "failed" in capsys.readouterr().out

    def test_missing_text_in_file(self, tmp_path, capsys):
        """テキストチェックが失敗する場合"""
        f = tmp_path / "README.md"
        f.write_text("No codex mention here")
        checks = [(f, "Codex")]  # Case sensitive: "codex" != "Codex"
        with patch.object(cad, "REQUIRED_FILES", []), \
             patch.object(cad, "TEXT_CHECKS", checks), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1

    def test_empty_checks(self, tmp_path, capsys):
        """チェック項目がない場合、成功する"""
        with patch.object(cad, "REQUIRED_FILES", []), \
             patch.object(cad, "TEXT_CHECKS", []), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 0

    def test_multiple_errors_all_reported(self, tmp_path, capsys):
        """複数エラーがすべて報告される"""
        missing = [
            tmp_path / "file1.md",
            tmp_path / "file2.md",
        ]
        with patch.object(cad, "REQUIRED_FILES", missing), \
             patch.object(cad, "TEXT_CHECKS", []), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        assert exit_code == 1
        out = capsys.readouterr().out
        assert out.count("Missing") == 2

    def test_binary_file_error(self, tmp_path, capsys):
        """バイナリファイルでも適切にエラーハンドリング"""
        f = tmp_path / "binary.md"
        f.write_bytes(b"\x80\x81\x82")
        checks = [(f, "text")]
        with patch.object(cad, "REQUIRED_FILES", []), \
             patch.object(cad, "TEXT_CHECKS", checks), \
             patch.object(cad, "PROJECT_ROOT", tmp_path):
            exit_code = main()
        # Should either find the text or report an error, not crash
        assert exit_code in (0, 1)
