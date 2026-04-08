"""check_command_paths.py の単体テスト。

コマンドパス検証ロジック（Python呼び出し検出、ファイル存在チェック）をテストする。
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
import check_command_paths as ccp


# ---------------------------------------------------------------------------
# find_python_invocations
# ---------------------------------------------------------------------------

class TestFindPythonInvocations:
    def test_basic_python_script(self):
        text = "python tools/setup.py"
        result = ccp.find_python_invocations(text)
        assert len(result) == 1
        assert result[0] == (1, "tools/setup.py")

    def test_python3_script(self):
        text = "python3 tools/setup.py"
        result = ccp.find_python_invocations(text)
        assert len(result) == 1
        assert result[0] == (1, "tools/setup.py")

    def test_module_invocation_skipped(self):
        text = "python -m pytest"
        result = ccp.find_python_invocations(text)
        assert result == []

    def test_python_m_venv_skipped(self):
        text = "python -m venv .venv"
        assert ccp.find_python_invocations(text) == []

    def test_multiple_invocations(self):
        text = """\
python tools/a.py
some text
python3 tools/b.py
"""
        result = ccp.find_python_invocations(text)
        assert len(result) == 2
        assert result[0] == (1, "tools/a.py")
        assert result[1] == (3, "tools/b.py")

    def test_no_invocations(self):
        text = "This is just text with no python calls"
        assert ccp.find_python_invocations(text) == []

    def test_empty_text(self):
        assert ccp.find_python_invocations("") == []

    def test_inline_python_call(self):
        text = "Run `python tools/demo.py` to start"
        result = ccp.find_python_invocations(text)
        assert len(result) == 1

    def test_skills_path(self):
        text = "python skills/banner-creator/scripts/create.py"
        result = ccp.find_python_invocations(text)
        assert len(result) == 1
        assert result[0][1] == "skills/banner-creator/scripts/create.py"


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

class TestRegexPatterns:
    def test_python_script_re_matches(self):
        m = ccp.PYTHON_SCRIPT_RE.search("python tools/test.py")
        assert m is not None
        assert m.group(1) == "tools/test.py"

    def test_python_script_re_no_module(self):
        m = ccp.PYTHON_SCRIPT_RE.search("python -m pip install")
        assert m is None

    def test_bare_scripts_re_matches(self):
        assert ccp.BARE_SCRIPTS_RE.match("scripts/foo.py") is not None

    def test_bare_scripts_re_no_tools(self):
        assert ccp.BARE_SCRIPTS_RE.match("tools/foo.py") is None

    def test_skill_literal_re_double_quoted(self):
        m = ccp.SKILL_STRING_LITERAL_RE.search('"skills/banner/scripts/run.py"')
        assert m is not None
        assert m.group(1) == "skills/banner/scripts/run.py"

    def test_skill_literal_re_single_quoted(self):
        m = ccp.SKILL_STRING_LITERAL_RE.search("'skills/banner/scripts/run.py'")
        assert m is not None

    def test_skill_literal_re_no_match(self):
        m = ccp.SKILL_STRING_LITERAL_RE.search('"tools/setup.py"')
        assert m is None


# ---------------------------------------------------------------------------
# check_file
# ---------------------------------------------------------------------------

class TestCheckFile:
    def test_no_issues(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("# Lesson\nJust text, no python calls\n")
        errors, warnings = ccp.check_file(f)
        assert errors == []
        assert warnings == []

    def test_bare_scripts_error(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("python scripts/foo.py\n")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            errors, warnings = ccp.check_file(f)
        assert len(errors) == 1
        assert errors[0]["kind"] == "bare_scripts"

    def test_missing_file_warning(self, tmp_path):
        f = tmp_path / "lesson.md"
        f.write_text("python tools/nonexistent.py\n")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            errors, warnings = ccp.check_file(f)
        assert len(warnings) == 1
        assert warnings[0]["kind"] == "not_found"

    def test_existing_file_no_warning(self, tmp_path):
        (tmp_path / "tools").mkdir()
        (tmp_path / "tools" / "real.py").write_text("pass")
        f = tmp_path / "lesson.md"
        f.write_text("python tools/real.py\n")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            errors, warnings = ccp.check_file(f)
        assert errors == []
        assert warnings == []

    def test_unreadable_file(self, tmp_path):
        f = tmp_path / "missing.md"
        errors, warnings = ccp.check_file(f)
        assert len(errors) == 1
        assert errors[0]["kind"] == "read_error"

    def test_bare_scripts_with_suggestion(self, tmp_path):
        skills_dir = tmp_path / "skills" / "my-skill" / "scripts"
        skills_dir.mkdir(parents=True)
        (skills_dir / "foo.py").write_text("pass")

        f = tmp_path / "lesson.md"
        f.write_text("python scripts/foo.py\n")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            errors, _ = ccp.check_file(f)
        assert len(errors) == 1
        assert errors[0]["suggestion"] is not None
        assert "skills/my-skill/scripts/foo.py" in errors[0]["suggestion"]

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.md"
        f.write_text("")
        errors, warnings = ccp.check_file(f)
        assert errors == []
        assert warnings == []


# ---------------------------------------------------------------------------
# _suggest_skill_path
# ---------------------------------------------------------------------------

class TestSuggestSkillPath:
    def test_found(self, tmp_path):
        skills_dir = tmp_path / "skills" / "test-skill" / "scripts"
        skills_dir.mkdir(parents=True)
        (skills_dir / "run.py").write_text("pass")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            result = ccp._suggest_skill_path("scripts/run.py")
        assert result is not None
        assert "test-skill" in result

    def test_not_found(self, tmp_path):
        (tmp_path / "skills").mkdir()
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            result = ccp._suggest_skill_path("scripts/nonexistent.py")
        assert result is None

    def test_no_skills_dir(self, tmp_path):
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            result = ccp._suggest_skill_path("scripts/any.py")
        assert result is None


# ---------------------------------------------------------------------------
# check_tools_skill_refs
# ---------------------------------------------------------------------------

class TestCheckToolsSkillRefs:
    def test_no_warnings_when_paths_exist(self, tmp_path):
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        skills_path = tmp_path / "skills" / "test" / "SKILL.md"
        skills_path.parent.mkdir(parents=True)
        skills_path.write_text("skill")

        tool_file = tools_dir / "my_tool.py"
        tool_file.write_text('path = "skills/test/SKILL.md"\n')

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch.object(ccp, "TOOLS_DIR", tools_dir):
            warnings = ccp.check_tools_skill_refs()
        assert warnings == []

    def test_warning_for_missing_skill_path(self, tmp_path):
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        tool_file = tools_dir / "my_tool.py"
        tool_file.write_text('path = "skills/nonexistent/SKILL.md"\n')

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch.object(ccp, "TOOLS_DIR", tools_dir):
            warnings = ccp.check_tools_skill_refs()
        assert len(warnings) == 1
        assert warnings[0]["kind"] == "not_found"


# ---------------------------------------------------------------------------
# _run_lesson_checks
# ---------------------------------------------------------------------------

class TestRunLessonChecks:
    def test_no_files_found(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        with patch.object(ccp, "LESSON_DIR", lesson_dir):
            errors, warnings, checked = ccp._run_lesson_checks("nonexistent")
        assert checked == 0

    def test_all_lessons_checked(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("# Lesson 1-1\n")
        (lesson_dir / "start-1-2.md").write_text("# Lesson 1-2\n")
        with patch.object(ccp, "LESSON_DIR", lesson_dir):
            errors, warnings, checked = ccp._run_lesson_checks(None)
        assert checked == 2

    def test_specific_target(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("# Lesson 1-1\n")
        (lesson_dir / "start-1-2.md").write_text("# Lesson 1-2\n")
        with patch.object(ccp, "LESSON_DIR", lesson_dir):
            errors, warnings, checked = ccp._run_lesson_checks("start-1-1")
        assert checked == 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_no_args(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("# No python calls\n")
        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_command_paths.py"]):
            exit_code = ccp.main()
        assert exit_code == 0

    def test_main_with_error(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("python scripts/bad.py\n")
        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py"]):
            exit_code = ccp.main()
        assert exit_code == 1

    def test_main_tools_flag(self, tmp_path):
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "sample.py").write_text("x = 1\n")
        with patch.object(ccp, "TOOLS_DIR", tools_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py", "--tools"]):
            exit_code = ccp.main()
        assert exit_code == 0

    def test_main_target_not_found(self, tmp_path):
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch("sys.argv", ["check_command_paths.py", "nonexistent"]):
            exit_code = ccp.main()
        assert exit_code == 1


# ---------------------------------------------------------------------------
# _suggest_skill_path advanced (lines 125-126)
# ---------------------------------------------------------------------------

class TestSuggestSkillPathAdvanced:
    def test_non_dir_in_skills(self, tmp_path):
        """Lines 125-126: iterdir() returns files (not dirs) -> skip"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        # Create a file (not a dir) in skills/
        (skills_dir / "README.md").write_text("readme")
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            result = ccp._suggest_skill_path("scripts/run.py")
        assert result is None

    def test_oserror_on_iterdir(self, tmp_path):
        """Line 126: OSError during iterdir"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("pathlib.Path.iterdir", side_effect=OSError("permission denied")):
            result = ccp._suggest_skill_path("scripts/foo.py")
        assert result is None


# ---------------------------------------------------------------------------
# check_tools_skill_refs advanced (lines 154, 157-165)
# ---------------------------------------------------------------------------

class TestCheckToolsSkillRefsAdvanced:
    def test_skips_self(self, tmp_path):
        """Line 154: skip self file"""
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        # Write self-referencing content in a file named like the module
        self_file = tools_dir / "check_command_paths.py"
        self_file.write_text('x = "skills/example/SKILL.md"\n')

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch.object(ccp, "TOOLS_DIR", tools_dir):
            warnings = ccp.check_tools_skill_refs()
        # Self should be skipped
        assert all(w["file"] != "check_command_paths.py" for w in warnings)

    def test_read_error(self, tmp_path):
        """Lines 157-165: unreadable file"""
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        tool_file = tools_dir / "broken.py"
        tool_file.write_text("x = 1")

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch.object(ccp, "TOOLS_DIR", tools_dir), \
             patch("pathlib.Path.read_text", side_effect=OSError("cannot read")):
            warnings = ccp.check_tools_skill_refs()
        assert len(warnings) >= 1
        assert any(w["kind"] == "read_error" for w in warnings)


# ---------------------------------------------------------------------------
# check_plugin_registry (lines 185-228)
# ---------------------------------------------------------------------------

class TestCheckPluginRegistry:
    def test_registry_not_found(self, tmp_path):
        """Lines 185-188: file not found"""
        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            result = ccp.check_plugin_registry()
        assert len(result) == 1
        assert "not found" in result[0]["message"]

    def test_no_yaml_module(self, tmp_path):
        """Lines 195-197: PyYAML not installed"""
        registry = tmp_path / "external-plugins.yaml"
        registry.write_text("plugins: {}")

        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("No module named yaml")
            return real_import(name, *args, **kwargs)

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("builtins.__import__", side_effect=mock_import):
            result = ccp.check_plugin_registry()
        assert len(result) == 1
        assert "PyYAML" in result[0]["message"]

    def test_parse_error(self, tmp_path):
        """Lines 202-204: YAML parse failure"""
        registry = tmp_path / "external-plugins.yaml"
        registry.write_text("{{invalid yaml", encoding="utf-8")

        with patch.object(ccp, "PROJECT_ROOT", tmp_path):
            try:
                import yaml
                result = ccp.check_plugin_registry()
                # If yaml is installed, it should report parse error
                assert len(result) >= 1
            except ImportError:
                pass  # yaml not installed, can't test this

    def test_git_not_found(self, tmp_path):
        """Lines 207-209: git not found"""
        registry = tmp_path / "external-plugins.yaml"
        registry.write_text("plugins: {}", encoding="utf-8")

        with patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("shutil.which", return_value=None):
            try:
                import yaml
                result = ccp.check_plugin_registry()
                assert any("git not found" in w["message"] for w in result)
            except ImportError:
                pass


# ---------------------------------------------------------------------------
# main() advanced (lines 263-265, 267-268, 293, 298-300, 309, 317-348)
# ---------------------------------------------------------------------------

class TestMainAdvanced:
    def test_main_all_flag(self, tmp_path):
        """Lines 263-265: --all flag"""
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("# No python\n")
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "sample.py").write_text("x = 1\n")

        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch.object(ccp, "TOOLS_DIR", tools_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch.object(ccp, "check_plugin_registry", return_value=[]), \
             patch("sys.argv", ["check_command_paths.py", "--all"]):
            exit_code = ccp.main()
        assert exit_code == 0

    def test_main_plugins_flag(self, tmp_path):
        """Lines 267-268: --plugins flag"""
        with patch.object(ccp, "check_plugin_registry", return_value=[]), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py", "--plugins"]):
            exit_code = ccp.main()
        assert exit_code == 0

    def test_main_plugins_with_warnings(self, tmp_path):
        """Lines 327-336: plugin warnings -> exit code 1"""
        plugin_warn = [{
            "file": "external-plugins.yaml",
            "line": 0,
            "path": "repo@ref",
            "message": "not reachable",
        }]
        with patch.object(ccp, "check_plugin_registry", return_value=plugin_warn), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py", "--plugins"]):
            exit_code = ccp.main()
        assert exit_code == 1

    def test_main_lessons_with_warnings_no_errors(self, tmp_path):
        """Lines 298-300, 309: warnings printed but exit 0"""
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        (lesson_dir / "start-1-1.md").write_text("python tools/nonexistent.py\n")
        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py"]):
            exit_code = ccp.main()
        # warnings only -> exit 0
        assert exit_code == 0

    def test_main_error_with_suggestion(self, tmp_path, capsys):
        """Lines 293: error with suggestion printed"""
        lesson_dir = tmp_path / "lessons"
        lesson_dir.mkdir()
        skills_dir = tmp_path / "skills" / "my-skill" / "scripts"
        skills_dir.mkdir(parents=True)
        (skills_dir / "foo.py").write_text("pass")
        (lesson_dir / "start-1-1.md").write_text("python scripts/foo.py\n")

        with patch.object(ccp, "LESSON_DIR", lesson_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py"]):
            exit_code = ccp.main()
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Did you mean" in captured.out

    def test_main_tools_with_warnings(self, tmp_path, capsys):
        """Lines 317-319: tools warnings printed"""
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        (tools_dir / "my_tool.py").write_text('x = "skills/nonexistent/foo.py"\n')

        with patch.object(ccp, "TOOLS_DIR", tools_dir), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py", "--tools"]):
            exit_code = ccp.main()
        captured = capsys.readouterr()
        assert "WARN" in captured.out

    def test_main_plugins_ok_with_count(self, tmp_path, capsys):
        """Lines 337-348: successful plugin check with count"""
        registry = tmp_path / "external-plugins.yaml"
        try:
            import yaml
            registry.write_text(yaml.dump({"plugins": {"p1": {"repo": "o/r", "ref": "main"}}}))
        except ImportError:
            registry.write_text("plugins:\n  p1:\n    repo: o/r\n    ref: main\n")

        with patch.object(ccp, "check_plugin_registry", return_value=[]), \
             patch.object(ccp, "PROJECT_ROOT", tmp_path), \
             patch("sys.argv", ["check_command_paths.py", "--plugins"]):
            exit_code = ccp.main()
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "OK" in captured.out
