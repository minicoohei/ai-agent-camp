"""check_imports.py の単体テスト。

禁止インポートパターン検出ロジックをテストする。
"""
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

ci = import_module_from_repo("check_imports", "tools/check_imports.py")

iter_python_files = ci.iter_python_files
check_banned_imports = ci.check_banned_imports
BANNED_PATTERNS = ci.BANNED_PATTERNS
EXCLUDE_DIRS = ci.EXCLUDE_DIRS
PACKAGE_IMPORT_MAP = ci.PACKAGE_IMPORT_MAP
main = ci.main


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def scan_root(tmp_path):
    """スキャン対象ディレクトリを作成"""
    (tmp_path / "tools").mkdir()
    (tmp_path / "skills").mkdir()
    return tmp_path


# ---------------------------------------------------------------------------
# BANNED_PATTERNS
# ---------------------------------------------------------------------------

class TestBannedPatterns:
    def test_import_google_generativeai(self):
        line = "import google.generativeai"
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        assert len(matches) == 1

    def test_from_google_generativeai(self):
        line = "from google.generativeai import configure"
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        assert len(matches) == 1

    def test_from_google_genai_not_banned(self):
        line = "from google import genai"
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        assert len(matches) == 0

    def test_comment_line_has_pattern(self):
        """コメント行にパターンがあっても正規表現自体はマッチする（除外はcheck_banned_importsで行う）"""
        line = "# import google.generativeai"
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        # Comments start with # so the pattern ^\s*import won't match
        assert len(matches) == 0

    def test_indented_import(self):
        line = "    import google.generativeai"
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        assert len(matches) == 1

    def test_partial_name_no_match(self):
        line = "import google.generativeai_v2"
        # The \b boundary should prevent this, but generativeai_v2 starts with generativeai
        # Actually \b matches at word boundary after "generativeai", so "i_" won't match \b
        # Let's just verify the behavior
        matches = [p for p, _, _ in BANNED_PATTERNS if p.search(line)]
        # The pattern uses \b, so "generativeai_v2" should NOT match because _ is a word char
        assert len(matches) == 0


# ---------------------------------------------------------------------------
# iter_python_files
# ---------------------------------------------------------------------------

class TestIterPythonFiles:
    def test_finds_py_files(self, scan_root):
        (scan_root / "tools" / "test.py").write_text("pass")
        (scan_root / "tools" / "readme.md").write_text("not python")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root):
            files = iter_python_files()
        assert len(files) == 1
        assert files[0].name == "test.py"

    def test_excludes_pycache(self, scan_root):
        cache_dir = scan_root / "tools" / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "cached.py").write_text("pass")
        (scan_root / "tools" / "real.py").write_text("pass")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root):
            files = iter_python_files()
        names = [f.name for f in files]
        assert "cached.py" not in names
        assert "real.py" in names

    def test_nonexistent_scan_dir(self, scan_root):
        scan_dirs = [scan_root / "nonexistent"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root):
            files = iter_python_files()
        assert files == []

    def test_empty_scan_dirs(self, scan_root):
        with patch.object(ci, "SCAN_DIRS", []), \
             patch.object(ci, "PROJECT_ROOT", scan_root):
            files = iter_python_files()
        assert files == []

    def test_recursive_scanning(self, scan_root):
        nested = scan_root / "tools" / "sub" / "deep"
        nested.mkdir(parents=True)
        (nested / "deep_tool.py").write_text("pass")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root):
            files = iter_python_files()
        assert any(f.name == "deep_tool.py" for f in files)


# ---------------------------------------------------------------------------
# check_banned_imports
# ---------------------------------------------------------------------------

class TestCheckBannedImports:
    def test_no_violations(self, tmp_path):
        f = tmp_path / "clean.py"
        f.write_text("from google import genai\nprint('hello')\n")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert violations == []

    def test_detects_old_import(self, tmp_path):
        f = tmp_path / "old.py"
        f.write_text("import google.generativeai\n")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert len(violations) == 1
        assert violations[0]["line"] == 1

    def test_detects_from_import(self, tmp_path):
        f = tmp_path / "old2.py"
        f.write_text("from google.generativeai import configure\n")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert len(violations) == 1

    def test_skips_comments(self, tmp_path):
        f = tmp_path / "commented.py"
        f.write_text("# import google.generativeai\nprint('ok')\n")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert violations == []

    def test_multiple_violations(self, tmp_path):
        f = tmp_path / "multi.py"
        f.write_text(
            "import google.generativeai\n"
            "from google.generativeai import something\n"
        )
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert len(violations) == 2

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.py"
        f.write_text("")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert violations == []

    def test_empty_file_list(self):
        violations = check_banned_imports([])
        assert violations == []

    def test_violation_has_fix(self, tmp_path):
        f = tmp_path / "old.py"
        f.write_text("import google.generativeai\n")
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert violations[0]["fix"] is not None
        assert "google-genai" in violations[0]["fix"]

    def test_unreadable_file_skipped(self, tmp_path):
        f = tmp_path / "missing.py"
        # File doesn't exist
        with patch.object(ci, "PROJECT_ROOT", tmp_path):
            violations = check_banned_imports([f])
        assert violations == []


# ---------------------------------------------------------------------------
# PACKAGE_IMPORT_MAP
# ---------------------------------------------------------------------------

class TestPackageImportMap:
    def test_known_mappings(self):
        assert PACKAGE_IMPORT_MAP["beautifulsoup4"] == "bs4"
        assert PACKAGE_IMPORT_MAP["Pillow"] == "PIL"
        assert PACKAGE_IMPORT_MAP["google-genai"] == "google.genai"
        assert PACKAGE_IMPORT_MAP["PyYAML"] == "yaml"

    def test_not_empty(self):
        assert len(PACKAGE_IMPORT_MAP) > 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestMain:
    def test_clean_exit_0(self, scan_root, capsys):
        (scan_root / "tools" / "clean.py").write_text("x = 1\n")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root), \
             patch("sys.argv", ["check_imports.py"]):
            exit_code = main()
        assert exit_code == 0
        assert "OK" in capsys.readouterr().out

    def test_violation_exit_1(self, scan_root, capsys):
        (scan_root / "tools" / "bad.py").write_text("import google.generativeai\n")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root), \
             patch("sys.argv", ["check_imports.py"]):
            exit_code = main()
        assert exit_code == 1
        assert "FAIL" in capsys.readouterr().out

    def test_verbose_flag(self, scan_root, capsys):
        (scan_root / "tools" / "a.py").write_text("pass")
        scan_dirs = [scan_root / "tools"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root), \
             patch("sys.argv", ["check_imports.py", "--verbose"]):
            exit_code = main()
        assert exit_code == 0
        out = capsys.readouterr().out
        assert "Scanning" in out

    def test_no_files(self, scan_root, capsys):
        scan_dirs = [scan_root / "nonexistent"]
        with patch.object(ci, "SCAN_DIRS", scan_dirs), \
             patch.object(ci, "PROJECT_ROOT", scan_root), \
             patch("sys.argv", ["check_imports.py"]):
            exit_code = main()
        assert exit_code == 0
