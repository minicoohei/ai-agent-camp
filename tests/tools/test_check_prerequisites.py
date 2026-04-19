"""check_prerequisites.py の単体テスト。

YAML frontmatter と本文の前提条件一致検証ロジックをテストする。
"""
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

cp = import_module_from_repo("check_prerequisites", "tools/check_prerequisites.py")

parse_yaml_prerequisites = cp.parse_yaml_prerequisites
parse_body_prerequisites = cp.parse_body_prerequisites
has_body_prereq_row = cp.has_body_prereq_row
check_file = cp.check_file
fix_file = cp.fix_file
_sort_key = cp._sort_key
main = cp.main


# ---------------------------------------------------------------------------
# _sort_key
# ---------------------------------------------------------------------------

class TestSortKey:
    def test_basic(self):
        assert _sort_key("1-1") == (1, 1)

    def test_two_digit(self):
        assert _sort_key("16-5") == (16, 5)

    def test_ordering(self):
        ids = ["2-1", "1-3", "1-1"]
        assert sorted(ids, key=_sort_key) == ["1-1", "1-3", "2-1"]


# ---------------------------------------------------------------------------
# parse_yaml_prerequisites
# ---------------------------------------------------------------------------

class TestParseYamlPrerequisites:
    def test_basic(self):
        text = '---\nprerequisites: ["start-1-1", "start-1-2"]\n---\nContent\n'
        result = parse_yaml_prerequisites(text)
        assert result == ["1-1", "1-2"]

    def test_single_prerequisite(self):
        text = '---\nprerequisites: ["start-0-1"]\n---\nContent\n'
        result = parse_yaml_prerequisites(text)
        assert result == ["0-1"]

    def test_empty_array(self):
        text = '---\nprerequisites: []\n---\nContent\n'
        result = parse_yaml_prerequisites(text)
        assert result == []

    def test_no_frontmatter(self):
        text = "# No frontmatter\nContent\n"
        result = parse_yaml_prerequisites(text)
        assert result == []

    def test_no_prerequisites_key(self):
        text = "---\ntitle: Test\n---\nContent\n"
        result = parse_yaml_prerequisites(text)
        assert result == []

    def test_empty_text(self):
        assert parse_yaml_prerequisites("") == []

    def test_sorted_output(self):
        text = '---\nprerequisites: ["start-2-1", "start-1-3", "start-1-1"]\n---\n'
        result = parse_yaml_prerequisites(text)
        assert result == ["1-1", "1-3", "2-1"]

    def test_single_quoted(self):
        text = "---\nprerequisites: ['start-1-1']\n---\n"
        result = parse_yaml_prerequisites(text)
        assert result == ["1-1"]


# ---------------------------------------------------------------------------
# parse_body_prerequisites
# ---------------------------------------------------------------------------

class TestParseBodyPrerequisites:
    def test_single_lesson(self):
        text = "| 前提条件 | Lesson 1-1 |\n"
        result = parse_body_prerequisites(text)
        assert result == ["1-1"]

    def test_range(self):
        text = "| 前提条件 | Lesson 16-1〜16-3 |\n"
        result = parse_body_prerequisites(text)
        assert result == ["16-1", "16-2", "16-3"]

    def test_range_with_tilde(self):
        text = "| 前提条件 | Lesson 0-1～0-3 |\n"
        result = parse_body_prerequisites(text)
        assert result == ["0-1", "0-2", "0-3"]

    def test_multi_dot(self):
        text = "| 前提条件 | Lesson 4-1・4-2 |\n"
        result = parse_body_prerequisites(text)
        assert result == ["4-1", "4-2"]

    def test_no_prereq_row(self):
        text = "| 項目 | 内容 |\n"
        result = parse_body_prerequisites(text)
        assert result == []

    def test_empty_text(self):
        assert parse_body_prerequisites("") == []

    def test_free_text_prereq(self):
        text = "| 前提条件 | プログラミング基礎知識 |\n"
        result = parse_body_prerequisites(text)
        assert result == []

    def test_multiple_singles(self):
        text = "| 前提条件 | Lesson 1-1, Lesson 2-1 |\n"
        result = parse_body_prerequisites(text)
        assert result == ["1-1", "2-1"]


# ---------------------------------------------------------------------------
# has_body_prereq_row
# ---------------------------------------------------------------------------

class TestHasBodyPrereqRow:
    def test_present(self):
        assert has_body_prereq_row("| 前提条件 | something |") is True

    def test_absent(self):
        assert has_body_prereq_row("| 項目 | 内容 |") is False

    def test_empty(self):
        assert has_body_prereq_row("") is False


# ---------------------------------------------------------------------------
# check_file
# ---------------------------------------------------------------------------

class TestCheckFile:
    def test_ok_match(self, tmp_path):
        f = tmp_path / "start-1-2.md"
        f.write_text(
            '---\nprerequisites: ["start-1-1"]\n---\n'
            "| 前提条件 | Lesson 1-1 |\n"
        )
        result = check_file(f)
        assert result is not None
        assert result["status"] == "ok"

    def test_mismatch(self, tmp_path):
        f = tmp_path / "start-1-3.md"
        f.write_text(
            '---\nprerequisites: ["start-1-1"]\n---\n'
            "| 前提条件 | Lesson 1-2 |\n"
        )
        result = check_file(f)
        assert result is not None
        assert result["status"] == "mismatch"
        assert "1-1" in result["only_in_yaml"]
        assert "1-2" in result["only_in_body"]

    def test_no_prerequisites_anywhere(self, tmp_path):
        f = tmp_path / "start-0-1.md"
        f.write_text("---\ntitle: Test\n---\n# Content\n")
        result = check_file(f)
        assert result is None

    def test_yaml_only_no_body_row(self, tmp_path):
        f = tmp_path / "start-2-1.md"
        f.write_text('---\nprerequisites: ["start-1-1"]\n---\n# Content\n')
        result = check_file(f)
        assert result is not None
        assert result["status"] == "warn"
        assert "no 前提条件 table row" in result["reason"]

    def test_yaml_with_freetext_body(self, tmp_path):
        f = tmp_path / "start-3-1.md"
        f.write_text(
            '---\nprerequisites: ["start-1-1"]\n---\n'
            "| 前提条件 | Python基礎知識 |\n"
        )
        result = check_file(f)
        assert result is not None
        assert result["status"] == "warn"
        assert "free-text" in result["reason"]


# ---------------------------------------------------------------------------
# fix_file
# ---------------------------------------------------------------------------

class TestFixFile:
    def test_fix_mismatch(self, tmp_path):
        f = tmp_path / "start-1-3.md"
        original = (
            '---\nprerequisites: ["start-1-1"]\n---\n'
            "| 前提条件 | Lesson 1-2 |\n"
        )
        f.write_text(original)
        result = {
            "file": f.name,
            "status": "mismatch",
            "yaml": ["1-1"],
            "body": ["1-2"],
        }
        ok = fix_file(f, result)
        assert ok is True
        new_text = f.read_text()
        assert "start-1-1" in new_text
        assert "start-1-2" in new_text

    def test_fix_with_backup(self, tmp_path):
        f = tmp_path / "start-1-3.md"
        f.write_text('---\nprerequisites: ["start-1-1"]\n---\n| 前提条件 | Lesson 1-2 |\n')
        result = {"yaml": ["1-1"], "body": ["1-2"]}
        fix_file(f, result, backup=True)
        assert (tmp_path / "start-1-3.md.bak").exists()

    def test_fix_no_frontmatter(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("# No frontmatter\n")
        result = {"yaml": ["1-1"], "body": ["1-2"]}
        ok = fix_file(f, result)
        assert ok is False

    def test_fix_no_change_needed(self, tmp_path):
        f = tmp_path / "start-1-2.md"
        f.write_text('---\nprerequisites: ["start-1-1"]\n---\nContent\n')
        result = {"yaml": ["1-1"], "body": ["1-1"]}
        ok = fix_file(f, result)
        assert ok is False


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestMain:
    def test_no_mismatches(self, tmp_path, capsys):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text(
            '---\nprerequisites: ["start-0-1"]\n---\n| 前提条件 | Lesson 0-1 |\n'
        )
        with patch.object(cp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_prerequisites.py"]):
            exit_code = main()
        assert exit_code == 0
        assert "OK" in capsys.readouterr().out

    def test_mismatch_returns_1(self, tmp_path, capsys):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text(
            '---\nprerequisites: ["start-0-1"]\n---\n| 前提条件 | Lesson 0-2 |\n'
        )
        with patch.object(cp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_prerequisites.py"]):
            exit_code = main()
        assert exit_code == 1

    def test_target_not_found(self, tmp_path, capsys):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        with patch.object(cp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_prerequisites.py", "nonexistent"]):
            exit_code = main()
        assert exit_code == 1

    def test_fix_write(self, tmp_path, capsys):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        f = lesson_dir / "start-1-1.md"
        f.write_text(
            '---\nprerequisites: ["start-0-1"]\n---\n| 前提条件 | Lesson 0-2 |\n'
        )
        with patch.object(cp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_prerequisites.py", "--fix-write"]):
            exit_code = main()
        assert exit_code == 0
        out = capsys.readouterr().out
        assert "FIXED" in out

    def test_empty_lesson_dir(self, tmp_path, capsys):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        with patch.object(cp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_prerequisites.py"]):
            exit_code = main()
        assert exit_code == 0
