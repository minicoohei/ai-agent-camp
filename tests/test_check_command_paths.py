"""
check_command_paths のユニットテスト。
レッスンコマンド内のスクリプトパス検証ロジックをテスト。
"""
import pytest
from pathlib import Path

# Import the module under test
from tools.check_command_paths import (
    find_python_invocations,
    check_file,
    BARE_SCRIPTS_RE,
)


class TestFindPythonInvocations:
    """python 呼び出しの検出テスト"""

    def test_detect_tools_path(self):
        text = "python tools/banner_creator.py --platform x_post"
        results = find_python_invocations(text)
        assert len(results) == 1
        assert results[0] == (1, "tools/banner_creator.py")

    def test_detect_python3(self):
        text = "python3 tools/test_planner.py --format json"
        results = find_python_invocations(text)
        assert len(results) == 1
        assert results[0] == (1, "tools/test_planner.py")

    def test_detect_skill_path(self):
        text = "python skills/article-writer/scripts/article_writer.py --topic test"
        results = find_python_invocations(text)
        assert len(results) == 1
        assert results[0] == (1, "skills/article-writer/scripts/article_writer.py")

    def test_detect_bare_scripts(self):
        text = "python scripts/style_analyzer.py --input text.md"
        results = find_python_invocations(text)
        assert len(results) == 1
        assert results[0] == (1, "scripts/style_analyzer.py")

    def test_skip_module_invocation(self):
        text = "python -m ugc.storyboard_anime_pipeline --config test"
        results = find_python_invocations(text)
        assert len(results) == 0

    def test_skip_venv(self):
        text = "python -m venv venv"
        results = find_python_invocations(text)
        assert len(results) == 0

    def test_skip_pip(self):
        text = "python -m pip install --upgrade pip"
        results = find_python_invocations(text)
        assert len(results) == 0

    def test_multiple_invocations(self):
        text = (
            "line 1\n"
            "python tools/nanobanana.py --prompt test\n"
            "line 3\n"
            "python skills/csv-analyzer/scripts/analyzer.py --input data.csv\n"
        )
        results = find_python_invocations(text)
        assert len(results) == 2
        assert results[0] == (2, "tools/nanobanana.py")
        assert results[1] == (4, "skills/csv-analyzer/scripts/analyzer.py")

    def test_line_numbers_correct(self):
        text = "line 1\nline 2\nline 3\npython tools/foo.py\nline 5"
        results = find_python_invocations(text)
        assert results[0][0] == 4

    def test_ugc_subdir(self):
        text = "python tools/ugc/clipper_marketing_pipeline.py --config test"
        results = find_python_invocations(text)
        assert len(results) == 1
        assert results[0] == (1, "tools/ugc/clipper_marketing_pipeline.py")


class TestBareScriptsRegex:
    """bare scripts/ パターン検出テスト"""

    def test_matches_bare_scripts(self):
        assert BARE_SCRIPTS_RE.match("scripts/foo.py")

    def test_no_match_tools(self):
        assert not BARE_SCRIPTS_RE.match("tools/foo.py")

    def test_no_match_skill_scripts(self):
        assert not BARE_SCRIPTS_RE.match("skills/x/scripts/foo.py")


class TestCheckFile:
    """ファイルレベルの検証テスト"""

    def test_valid_tools_path(self, project_root):
        """tools/ パスが実際に存在する場合はエラーなし"""
        lesson_dir = project_root / ".cursor" / "commands" / "lesson"
        start_1_1 = lesson_dir / "start-1-1.md"
        if start_1_1.exists():
            errors, _warnings = check_file(start_1_1)
            assert len(errors) == 0

    def test_bare_scripts_detected(self, tmp_path):
        """scripts/xxx.py パターンがエラーになる"""
        lesson_file = tmp_path / "start-99-1.md"
        lesson_file.write_text(
            "---\n"
            'description: "test"\n'
            "---\n"
            "# Test\n"
            "python scripts/style_analyzer.py --input text.md\n"
        )
        errors, _warnings = check_file(lesson_file)
        assert len(errors) == 1
        assert errors[0]["kind"] == "bare_scripts"
        assert errors[0]["path"] == "scripts/style_analyzer.py"
        assert errors[0]["line"] == 5

    def test_nonexistent_tools_path_is_warning(self, tmp_path):
        """存在しない tools/ パスは警告(エラーではない)"""
        lesson_file = tmp_path / "start-99-2.md"
        lesson_file.write_text(
            "---\n"
            'description: "test"\n'
            "---\n"
            "# Test\n"
            "python tools/nonexistent_tool_xyz.py --test\n"
        )
        errors, warnings = check_file(lesson_file)
        assert len(errors) == 0
        assert len(warnings) == 1
        assert warnings[0]["kind"] == "not_found"

    def test_no_python_invocations(self, tmp_path):
        """python 呼び出しがないファイルはエラーも警告もなし"""
        lesson_file = tmp_path / "start-99-3.md"
        lesson_file.write_text(
            "---\n"
            'description: "test"\n'
            "---\n"
            "# Test lesson with no python calls\n"
            "Just theory content here.\n"
        )
        errors, warnings = check_file(lesson_file)
        assert len(errors) == 0
        assert len(warnings) == 0


class TestRealLessonFiles:
    """実際のレッスンファイルに対する統合テスト"""

    def test_no_bare_scripts_in_lessons(self, project_root):
        """全レッスンファイルで bare_scripts エラーが0であることを確認"""
        lesson_dir = project_root / ".cursor" / "commands" / "lesson"
        all_errors = []
        for path in sorted(lesson_dir.glob("start-*.md")):
            errors, _ = check_file(path)
            all_errors.extend(errors)

        if all_errors:
            msg_lines = ["Bare scripts/ path errors found:"]
            for e in all_errors:
                msg_lines.append(f"  {e['file']}:{e['line']} - {e['path']}")
            pytest.fail("\n".join(msg_lines))
