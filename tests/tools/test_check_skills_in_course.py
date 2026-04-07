"""check_skills_in_course.py の単体テスト。

スキル使用状況チェックロジックをテストする。
"""
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.conftest import import_module_from_repo

csc = import_module_from_repo("check_skills_in_course", "tools/check_skills_in_course.py")

collect_skill_names = csc.collect_skill_names
collect_course_and_lesson_files = csc.collect_course_and_lesson_files
get_searchable_text = csc.get_searchable_text
is_skill_used_in_file = csc.is_skill_used_in_file
compute_used_and_not_used = csc.compute_used_and_not_used
main = csc.main


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def skills_dir(tmp_path):
    """スキルディレクトリ構造を作成"""
    for name in ["banner-creator", "chart-maker", "unused-skill"]:
        d = tmp_path / "skills" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"# {name}\n")
    return tmp_path / "skills"


@pytest.fixture
def course_dir(tmp_path):
    """コースディレクトリ構造を作成"""
    d = tmp_path / "course"
    d.mkdir()
    (d / "lesson1.md").write_text("Use banner-creator for images\n")
    (d / "lesson2.html").write_text("<p>Use skills/chart-maker/ here</p>\n")
    return d


@pytest.fixture
def lesson_dir(tmp_path):
    """レッスンコマンドディレクトリ"""
    d = tmp_path / ".cursor" / "commands" / "lesson"
    d.mkdir(parents=True)
    (d / "start-1-1.md").write_text("Run banner-creator\n")
    return d


# ---------------------------------------------------------------------------
# collect_skill_names
# ---------------------------------------------------------------------------

class TestCollectSkillNames:
    def test_returns_sorted_names(self, skills_dir):
        with patch.object(csc, "SKILLS_DIR", skills_dir):
            names = collect_skill_names()
        assert names == ["banner-creator", "chart-maker", "unused-skill"]

    def test_empty_skills_dir(self, tmp_path):
        d = tmp_path / "skills"
        d.mkdir()
        with patch.object(csc, "SKILLS_DIR", d):
            assert collect_skill_names() == []

    def test_no_skills_dir(self, tmp_path):
        with patch.object(csc, "SKILLS_DIR", tmp_path / "nonexistent"):
            assert collect_skill_names() == []

    def test_dir_without_skill_md_ignored(self, tmp_path):
        d = tmp_path / "skills" / "no-skill-md"
        d.mkdir(parents=True)
        # No SKILL.md file
        with patch.object(csc, "SKILLS_DIR", tmp_path / "skills"):
            assert collect_skill_names() == []

    def test_file_in_skills_dir_ignored(self, tmp_path):
        d = tmp_path / "skills"
        d.mkdir()
        (d / "README.md").write_text("not a skill")
        with patch.object(csc, "SKILLS_DIR", d):
            assert collect_skill_names() == []


# ---------------------------------------------------------------------------
# collect_course_and_lesson_files
# ---------------------------------------------------------------------------

class TestCollectCourseAndLessonFiles:
    def test_collects_files(self, course_dir, lesson_dir, tmp_path):
        with patch.object(csc, "COURSE_DIR", course_dir), \
             patch.object(csc, "LESSON_DIR", lesson_dir):
            files = collect_course_and_lesson_files()
        assert len(files) >= 3  # 2 course + 1 lesson

    def test_no_dirs(self, tmp_path):
        with patch.object(csc, "COURSE_DIR", tmp_path / "no_course"), \
             patch.object(csc, "LESSON_DIR", tmp_path / "no_lesson"):
            files = collect_course_and_lesson_files()
        assert files == []


# ---------------------------------------------------------------------------
# get_searchable_text
# ---------------------------------------------------------------------------

class TestGetSearchableText:
    def test_normal_file(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Hello world")
        text = get_searchable_text(f)
        assert text == "Hello world"

    def test_nonexistent_file(self, tmp_path):
        text = get_searchable_text(tmp_path / "missing.md")
        assert text == ""

    def test_curriculum_excludes_unused_section(self, tmp_path):
        course_dir = tmp_path / "course"
        course_dir.mkdir()
        curriculum = course_dir / "CURRICULUM.md"
        curriculum.write_text(
            "# Course\nbanner-creator is used\n"
            "## 講義未使用スキル\nunused-skill listed here\n"
            "## Next Section\nMore content\n"
        )
        with patch.object(csc, "COURSE_DIR", course_dir):
            text = get_searchable_text(curriculum)
        assert "banner-creator" in text
        assert "unused-skill" not in text

    def test_curriculum_excludes_to_end(self, tmp_path):
        course_dir = tmp_path / "course"
        course_dir.mkdir()
        curriculum = course_dir / "CURRICULUM.md"
        curriculum.write_text(
            "# Course\n"
            "## 講義未使用スキル\nunused-skill\n"
        )
        with patch.object(csc, "COURSE_DIR", course_dir):
            text = get_searchable_text(curriculum)
        assert "unused-skill" not in text


# ---------------------------------------------------------------------------
# is_skill_used_in_file
# ---------------------------------------------------------------------------

class TestIsSkillUsedInFile:
    def test_found_by_name(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("Use banner-creator for this task")
        assert is_skill_used_in_file("banner-creator", f) is True

    def test_found_by_path(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("See skills/chart-maker/ for details")
        assert is_skill_used_in_file("chart-maker", f) is True

    def test_not_found(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("Nothing about skills here")
        assert is_skill_used_in_file("banner-creator", f) is False

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        assert is_skill_used_in_file("banner-creator", f) is False


# ---------------------------------------------------------------------------
# compute_used_and_not_used
# ---------------------------------------------------------------------------

class TestComputeUsedAndNotUsed:
    def test_all_used(self, tmp_path):
        f = tmp_path / "all.md"
        f.write_text("banner-creator chart-maker")
        used, not_used = compute_used_and_not_used(
            ["banner-creator", "chart-maker"], [f]
        )
        assert used == ["banner-creator", "chart-maker"]
        assert not_used == []

    def test_none_used(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("nothing")
        used, not_used = compute_used_and_not_used(
            ["banner-creator", "chart-maker"], [f]
        )
        assert used == []
        assert not_used == ["banner-creator", "chart-maker"]

    def test_partial_use(self, tmp_path):
        f = tmp_path / "partial.md"
        f.write_text("Use banner-creator here")
        used, not_used = compute_used_and_not_used(
            ["banner-creator", "chart-maker"], [f]
        )
        assert used == ["banner-creator"]
        assert not_used == ["chart-maker"]

    def test_empty_skill_list(self, tmp_path):
        f = tmp_path / "any.md"
        f.write_text("content")
        used, not_used = compute_used_and_not_used([], [f])
        assert used == []
        assert not_used == []

    def test_empty_file_list(self):
        used, not_used = compute_used_and_not_used(["banner-creator"], [])
        assert used == []
        assert not_used == ["banner-creator"]


# ---------------------------------------------------------------------------
# main (CLI)
# ---------------------------------------------------------------------------

class TestMain:
    def test_default_output(self, skills_dir, course_dir, lesson_dir, capsys):
        with patch.object(csc, "SKILLS_DIR", skills_dir), \
             patch.object(csc, "COURSE_DIR", course_dir), \
             patch.object(csc, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_skills_in_course.py"]):
            exit_code = main()
        assert exit_code == 0
        out = capsys.readouterr().out
        assert "Total:" in out

    def test_json_output(self, skills_dir, course_dir, lesson_dir, capsys):
        with patch.object(csc, "SKILLS_DIR", skills_dir), \
             patch.object(csc, "COURSE_DIR", course_dir), \
             patch.object(csc, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_skills_in_course.py", "--json"]):
            exit_code = main()
        assert exit_code == 0
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "used" in data
        assert "not_used" in data
        assert "total" in data

    def test_not_used_only(self, skills_dir, course_dir, lesson_dir, capsys):
        with patch.object(csc, "SKILLS_DIR", skills_dir), \
             patch.object(csc, "COURSE_DIR", course_dir), \
             patch.object(csc, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_skills_in_course.py", "--not-used-only"]):
            exit_code = main()
        assert exit_code == 0
        out = capsys.readouterr().out
        # unused-skill should appear
        assert "unused-skill" in out

    def test_no_skills(self, tmp_path, capsys):
        with patch.object(csc, "SKILLS_DIR", tmp_path / "none"), \
             patch.object(csc, "COURSE_DIR", tmp_path / "none2"), \
             patch.object(csc, "LESSON_DIR", tmp_path / "none3"), \
             patch("sys.argv", ["check_skills_in_course.py"]):
            exit_code = main()
        assert exit_code == 0
