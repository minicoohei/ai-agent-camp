"""lesson_progress.py の単体テスト"""
import importlib
import sys

import pytest
import json
from pathlib import Path
from unittest.mock import patch


@pytest.fixture(autouse=True)
def _reload_lesson_progress():
    """他テストが sys.modules['lesson_progress'] をモックで上書きしている場合があるため、
    毎テスト前に実モジュールを再ロードして復元する。"""
    mod = sys.modules.get("lesson_progress")
    # MagicMock など実モジュールでない場合、キャッシュを消してリロード
    if mod is None or not hasattr(mod, "__file__"):
        sys.modules.pop("lesson_progress", None)
        import lesson_progress
        importlib.reload(lesson_progress)
    yield


class TestImport:
    def test_import_module(self):
        import lesson_progress
        assert hasattr(lesson_progress, 'load_progress')
        assert hasattr(lesson_progress, 'save_progress')
        assert hasattr(lesson_progress, 'is_command_line')
        assert hasattr(lesson_progress, 'has_placeholder')

    def test_import_additional(self):
        from lesson_progress import (
            extract_outputs, extract_commands, check_lesson,
            normalize_path, lesson_order, mark_lesson, print_result
        )
        assert callable(extract_outputs)
        assert callable(extract_commands)
        assert callable(check_lesson)


class TestLoadProgress:
    def test_no_file(self, monkeypatch):
        import lesson_progress
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", Path("/nonexistent/progress.json"))
        result = lesson_progress.load_progress()
        assert result == {"lessons": {}}

    def test_valid_file(self, tmp_path, monkeypatch):
        import lesson_progress
        progress_file = tmp_path / "progress.json"
        progress_file.write_text('{"lessons": {"1-1": "completed"}}', encoding="utf-8")
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        result = lesson_progress.load_progress()
        assert result["lessons"]["1-1"] == "completed"

    def test_corrupt_file(self, tmp_path, monkeypatch):
        import lesson_progress
        progress_file = tmp_path / "progress.json"
        progress_file.write_text("not json", encoding="utf-8")
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        result = lesson_progress.load_progress()
        assert result == {"lessons": {}}

    def test_empty_file(self, tmp_path, monkeypatch):
        import lesson_progress
        progress_file = tmp_path / "progress.json"
        progress_file.write_text("", encoding="utf-8")
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        result = lesson_progress.load_progress()
        assert result == {"lessons": {}}


class TestSaveProgress:
    def test_save_creates_file(self, tmp_path, monkeypatch):
        import lesson_progress
        progress_file = tmp_path / "subdir" / "progress.json"
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        lesson_progress.save_progress({"lessons": {"1-1": "done"}})
        assert progress_file.exists()
        data = json.loads(progress_file.read_text(encoding="utf-8"))
        assert "updated_at" in data

    def test_save_overwrites(self, tmp_path, monkeypatch):
        import lesson_progress
        progress_file = tmp_path / "progress.json"
        progress_file.write_text('{"old": true}', encoding="utf-8")
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        lesson_progress.save_progress({"lessons": {"new": True}})
        data = json.loads(progress_file.read_text(encoding="utf-8"))
        assert "new" in data["lessons"]
        assert "old" not in data


class TestIsCommandLine:
    def test_python_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("python test.py") is True

    def test_slash_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("/start-1-1") is True

    def test_git_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("git status") is True

    def test_plain_text(self):
        from lesson_progress import is_command_line
        assert is_command_line("Hello world") is False

    def test_empty(self):
        from lesson_progress import is_command_line
        assert is_command_line("") is False

    def test_pip_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("pip install requests") is True

    def test_npm_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("npm install") is True

    def test_curl_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("curl http://example.com") is True

    def test_whitespace_only(self):
        from lesson_progress import is_command_line
        assert is_command_line("   ") is False

    def test_indented_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("  python test.py") is True

    def test_export_command(self):
        from lesson_progress import is_command_line
        assert is_command_line("export VAR=value") is True


class TestHasPlaceholder:
    def test_with_placeholder(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("python test.py --key YOUR_KEY") is True

    def test_with_angle_brackets(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("python test.py <filename>") is True

    def test_no_placeholder(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("python test.py --verbose") is False

    def test_xxx_placeholder(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("token: xxxx") is True

    def test_your_in_text(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("Enter your API key") is True

    def test_case_insensitive(self):
        from lesson_progress import has_placeholder
        assert has_placeholder("YOUR_KEY") is True
        assert has_placeholder("your_key") is True


class TestNormalizePath:
    def test_absolute_path(self):
        from lesson_progress import normalize_path
        result = normalize_path("/usr/local/bin")
        assert result == Path("/usr/local/bin")

    def test_relative_path(self):
        from lesson_progress import normalize_path, PROJECT_ROOT
        result = normalize_path("tools/test.py")
        assert result == PROJECT_ROOT / "tools/test.py"

    def test_tilde_path(self):
        from lesson_progress import normalize_path
        result = normalize_path("~/Documents")
        assert str(result).startswith("/")  # Should be expanded

    def test_strip_backticks(self):
        from lesson_progress import normalize_path, PROJECT_ROOT
        result = normalize_path("`tools/test.py`")
        assert result == PROJECT_ROOT / "tools/test.py"

    def test_strip_quotes(self):
        from lesson_progress import normalize_path, PROJECT_ROOT
        result = normalize_path('"tools/test.py"')
        assert result == PROJECT_ROOT / "tools/test.py"

    def test_strip_trailing_period(self):
        from lesson_progress import normalize_path, PROJECT_ROOT
        result = normalize_path("tools/test.py.")
        assert result == PROJECT_ROOT / "tools/test.py"


class TestExtractOutputs:
    def test_basic_output_line(self):
        from lesson_progress import extract_outputs
        text = "出力先: docs/output.html"
        outputs = extract_outputs(text)
        assert len(outputs) == 1
        assert outputs[0].name == "output.html"

    def test_multiple_outputs(self):
        from lesson_progress import extract_outputs
        text = "出力: docs/a.html、docs/b.html"
        outputs = extract_outputs(text)
        assert len(outputs) == 2

    def test_no_output_lines(self):
        from lesson_progress import extract_outputs
        text = "This is regular text without output lines"
        outputs = extract_outputs(text)
        assert len(outputs) == 0

    def test_output_with_backticks(self):
        from lesson_progress import extract_outputs
        text = "出力先: `docs/output.html`"
        outputs = extract_outputs(text)
        assert len(outputs) == 1


class TestExtractCommands:
    def test_commands_in_code_block(self):
        from lesson_progress import extract_commands
        text = "説明テキスト\n```\npython test.py\ngit status\n```"
        commands = extract_commands(text)
        assert "python test.py" in commands
        assert "git status" in commands

    def test_no_commands(self):
        from lesson_progress import extract_commands
        text = "これはただのテキスト"
        commands = extract_commands(text)
        assert len(commands) == 0

    def test_commands_outside_code_block_ignored(self):
        from lesson_progress import extract_commands
        text = "python test.py\n```\ngit status\n```"
        commands = extract_commands(text)
        assert "python test.py" not in commands
        assert "git status" in commands

    def test_non_command_in_code_block(self):
        from lesson_progress import extract_commands
        text = "```\nHello world\npython test.py\n```"
        commands = extract_commands(text)
        assert len(commands) == 1
        assert commands[0] == "python test.py"

    def test_duplicate_commands_removed(self):
        from lesson_progress import extract_commands
        text = "```\npython test.py\npython test.py\n```"
        commands = extract_commands(text)
        assert len(commands) == 1


class TestCheckLesson:
    def test_check_with_existing_output(self, tmp_path):
        from lesson_progress import check_lesson

        # Create a lesson file with output reference
        lesson_file = tmp_path / "start-1-1.md"
        output_file = tmp_path / "result.html"
        output_file.write_text("done", encoding="utf-8")
        lesson_file.write_text(f"出力先: {output_file}\n", encoding="utf-8")

        progress = {"lessons": {}}
        result = check_lesson("start-1-1", lesson_file, progress)
        assert result["lesson_id"] == "start-1-1"
        assert result["completed"] is True

    def test_check_with_missing_output(self, tmp_path):
        from lesson_progress import check_lesson

        lesson_file = tmp_path / "start-1-2.md"
        lesson_file.write_text("出力先: /nonexistent/file.html\n", encoding="utf-8")

        progress = {"lessons": {}}
        result = check_lesson("start-1-2", lesson_file, progress)
        assert result["completed"] is False

    def test_check_with_commands_unconfirmed(self, tmp_path):
        from lesson_progress import check_lesson

        lesson_file = tmp_path / "start-2-1.md"
        lesson_file.write_text("```\npython test.py\n```\n", encoding="utf-8")

        progress = {"lessons": {}}
        result = check_lesson("start-2-1", lesson_file, progress)
        assert result["completed"] is False
        assert result["command_confirmed"] is False

    def test_check_with_commands_confirmed(self, tmp_path):
        from lesson_progress import check_lesson

        lesson_file = tmp_path / "start-2-2.md"
        lesson_file.write_text("```\npython test.py\n```\n", encoding="utf-8")

        progress = {"lessons": {"start-2-2": {"command_confirmed": True}}}
        result = check_lesson("start-2-2", lesson_file, progress)
        assert result["command_confirmed"] is True

    def test_check_no_outputs_no_commands(self, tmp_path):
        from lesson_progress import check_lesson

        lesson_file = tmp_path / "start-3-1.md"
        lesson_file.write_text("ただの説明テキスト\n", encoding="utf-8")

        progress = {"lessons": {}}
        result = check_lesson("start-3-1", lesson_file, progress)
        # No outputs and no commands, manual_confirmed defaults to False
        assert result["completed"] is False

    def test_check_no_outputs_manual_confirmed(self, tmp_path):
        from lesson_progress import check_lesson

        lesson_file = tmp_path / "start-3-2.md"
        lesson_file.write_text("手動確認レッスン\n", encoding="utf-8")

        progress = {"lessons": {"start-3-2": {"manual_confirmed": True}}}
        result = check_lesson("start-3-2", lesson_file, progress)
        assert result["completed"] is True


class TestMarkLesson:
    def test_mark_new_lesson(self):
        from lesson_progress import mark_lesson
        progress = {"lessons": {}}
        mark_lesson("start-1-1", progress)
        assert progress["lessons"]["start-1-1"]["command_confirmed"] is True
        assert progress["lessons"]["start-1-1"]["manual_confirmed"] is True

    def test_mark_existing_lesson(self):
        from lesson_progress import mark_lesson
        progress = {"lessons": {"start-1-1": {"command_confirmed": False}}}
        mark_lesson("start-1-1", progress)
        assert progress["lessons"]["start-1-1"]["command_confirmed"] is True
        assert progress["lessons"]["start-1-1"]["manual_confirmed"] is True


class TestPrintResult:
    def test_print_completed(self, capsys):
        from lesson_progress import print_result
        result = {
            "lesson_id": "start-1-1",
            "outputs": [{"path": "/tmp/test.html", "exists": True}],
            "commands": ["python test.py"],
            "command_confirmed": True,
            "manual_confirmed": False,
            "completed": True,
        }
        print_result(result)
        captured = capsys.readouterr()
        assert "start-1-1" in captured.out
        assert "完了" in captured.out

    def test_print_incomplete(self, capsys):
        from lesson_progress import print_result
        result = {
            "lesson_id": "start-2-1",
            "outputs": [{"path": "/tmp/test.html", "exists": False}],
            "commands": [],
            "command_confirmed": False,
            "manual_confirmed": False,
            "completed": False,
        }
        print_result(result)
        captured = capsys.readouterr()
        assert "未完" in captured.out

    def test_print_no_outputs(self, capsys):
        from lesson_progress import print_result
        result = {
            "lesson_id": "start-3-1",
            "outputs": [],
            "commands": [],
            "command_confirmed": False,
            "manual_confirmed": False,
            "completed": False,
        }
        print_result(result)
        captured = capsys.readouterr()
        assert "対象なし" in captured.out
        assert "手動確認" in captured.out

    def test_print_with_commands_pending(self, capsys):
        from lesson_progress import print_result
        result = {
            "lesson_id": "start-4-1",
            "outputs": [],
            "commands": ["python run.py"],
            "command_confirmed": False,
            "manual_confirmed": True,
            "completed": False,
        }
        print_result(result)
        captured = capsys.readouterr()
        assert "要確認" in captured.out


# ===========================================================================
# lesson_order (lines 58-69)
# ===========================================================================

class TestLessonOrder:
    def test_returns_sorted_order(self, tmp_path, monkeypatch):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-2-1.md").write_text("lesson 2-1")
        (lesson_dir / "start-1-1.md").write_text("lesson 1-1")
        (lesson_dir / "start-1-2.md").write_text("lesson 1-2")
        (lesson_dir / "not-a-lesson.md").write_text("ignored")

        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        order, mapping = lesson_progress.lesson_order()
        assert order == ["start-1-1", "start-1-2", "start-2-1"]
        assert "start-1-1" in mapping
        assert mapping["start-1-1"].name == "start-1-1.md"

    def test_empty_dir(self, tmp_path, monkeypatch):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        order, mapping = lesson_progress.lesson_order()
        assert order == []
        assert mapping == {}

    def test_non_matching_files_ignored(self, tmp_path, monkeypatch):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-abc.md").write_text("bad name")
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        order, _ = lesson_progress.lesson_order()
        assert order == []


# ===========================================================================
# extract_outputs: empty part after split (line 102)
# ===========================================================================

class TestExtractOutputsEmptyPart:
    def test_empty_parts_skipped(self):
        from lesson_progress import extract_outputs
        text = "出力: , , docs/a.html"
        outputs = extract_outputs(text)
        assert len(outputs) == 1
        assert outputs[0].name == "a.html"


# ===========================================================================
# main() (lines 196-245)
# ===========================================================================

class TestMain:
    def test_main_list(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-1-1.md").write_text("lesson")
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", tmp_path / "progress.json")
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--list"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "start-1-1" in captured.out

    def test_main_mark(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-1-1.md").write_text("lesson")
        progress_file = tmp_path / "progress.json"
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--mark", "start-1-1"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "完了" in captured.out
        assert progress_file.exists()

    def test_main_mark_unknown(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", tmp_path / "p.json")
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--mark", "start-99-99"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "未対応" in captured.out

    def test_main_check(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        (lesson_dir / "start-1-1.md").write_text("ただのテキスト\n")
        progress_file = tmp_path / "progress.json"
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--check", "start-1-1"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "start-1-1" in captured.out

    def test_main_check_unknown(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", tmp_path / "p.json")
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--check", "start-99-99"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "未対応" in captured.out

    def test_main_next_all_completed(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        f = lesson_dir / "start-1-1.md"
        output_file = tmp_path / "result.html"
        output_file.write_text("done")
        f.write_text(f"出力先: {output_file}\n")
        progress_file = tmp_path / "progress.json"
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--next"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "全レッスン完了" in captured.out

    def test_main_next_incomplete(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        f = lesson_dir / "start-1-1.md"
        f.write_text("出力先: /nonexistent/file.html\n")
        progress_file = tmp_path / "progress.json"
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", progress_file)
        monkeypatch.setattr("sys.argv", ["lesson_progress", "--next"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "次に実行" in captured.out

    def test_main_no_args_prints_help(self, tmp_path, monkeypatch, capsys):
        import lesson_progress
        lesson_dir = tmp_path / "lesson"
        lesson_dir.mkdir(parents=True)
        monkeypatch.setattr(lesson_progress, "LESSON_DIR", lesson_dir)
        monkeypatch.setattr(lesson_progress, "PROGRESS_PATH", tmp_path / "p.json")
        monkeypatch.setattr("sys.argv", ["lesson_progress"])
        lesson_progress.main()
        captured = capsys.readouterr()
        assert "usage" in captured.out.lower() or "help" in captured.out.lower() or "Lesson" in captured.out
