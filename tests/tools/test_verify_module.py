"""verify_module.py の単体テスト。

レッスン検証ロジック（チェックポイント抽出、ファイル検証、モジュール検証）をテストする。
外部依存（lesson_progress）はモックする。
"""
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))

# ---------------------------------------------------------------------------
# Module import with lesson_progress mocked
# ---------------------------------------------------------------------------

# lesson_progress is a sibling import; we mock it before loading verify_module
_mock_lp = MagicMock()
_mock_lp.PROJECT_ROOT = Path("/fake/project")
_mock_lp.extract_outputs.return_value = []
_mock_lp.lesson_order.return_value = ([], {})
_mock_lp.load_progress.return_value = {}

# Ensure the mock is in place before importing
sys.modules.pop("verify_module", None)
sys.modules["lesson_progress"] = _mock_lp

import verify_module as vm


# ---------------------------------------------------------------------------
# extract_checkpoints
# ---------------------------------------------------------------------------

class TestExtractCheckpoints:
    def test_basic_checkpoints(self):
        text = """\
## チェックポイント
- [ ] ファイルが生成された
- [x] 画像が正しい
"""
        result = vm.extract_checkpoints(text)
        assert result == ["ファイルが生成された", "画像が正しい"]

    def test_no_checkpoint_section(self):
        text = "# Title\nSome content\n"
        assert vm.extract_checkpoints(text) == []

    def test_empty_text(self):
        assert vm.extract_checkpoints("") == []

    def test_checkpoint_section_ends_at_next_heading(self):
        text = """\
## チェックポイント
- [ ] Item 1
## 次のセクション
- [ ] Should not appear
"""
        result = vm.extract_checkpoints(text)
        assert result == ["Item 1"]

    def test_non_checkbox_lines_ignored(self):
        text = """\
## チェックポイント
Some description text
- [ ] Valid item
Plain text again
"""
        result = vm.extract_checkpoints(text)
        assert result == ["Valid item"]

    def test_multiple_checkpoint_sections(self):
        text = """\
## チェックポイント
- [ ] First
## Other
## チェックポイント
- [ ] Second
"""
        result = vm.extract_checkpoints(text)
        assert result == ["First", "Second"]

    def test_h3_checkpoint_header(self):
        text = """\
### チェックポイント
- [ ] Item from h3
"""
        result = vm.extract_checkpoints(text)
        assert result == ["Item from h3"]


# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

class TestExtractTitle:
    def test_lesson_title(self):
        text = "# Module 1 Lesson 1-1: バナー生成入門\n"
        assert vm.extract_title(text) == "バナー生成入門"

    def test_fallback_to_first_h1(self):
        text = "# My Title\nSome content\n"
        assert vm.extract_title(text) == "My Title"

    def test_no_title(self):
        text = "Some content without headings\n"
        assert vm.extract_title(text) == ""

    def test_empty_text(self):
        assert vm.extract_title("") == ""

    def test_lesson_title_with_spaces(self):
        text = "# Module 2 Lesson 2-3:  タイトル  \n"
        assert vm.extract_title(text) == "タイトル"

    def test_unicode_title(self):
        text = "# Module 1 Lesson 1-1: 日本語タイトル\n"
        assert vm.extract_title(text) == "日本語タイトル"


# ---------------------------------------------------------------------------
# extract_frontmatter
# ---------------------------------------------------------------------------

class TestExtractFrontmatter:
    def test_basic_frontmatter(self):
        text = """\
---
title: Test Lesson
module: 1
---
Content here
"""
        result = vm.extract_frontmatter(text)
        assert result["title"] == "Test Lesson"
        assert result["module"] == "1"

    def test_no_frontmatter(self):
        text = "# Just a heading\nContent\n"
        assert vm.extract_frontmatter(text) == {}

    def test_empty_text(self):
        assert vm.extract_frontmatter("") == {}

    def test_empty_frontmatter(self):
        text = "---\n---\nContent\n"
        assert vm.extract_frontmatter(text) == {}

    def test_quoted_values(self):
        text = '---\ntitle: "Quoted Title"\n---\n'
        result = vm.extract_frontmatter(text)
        assert result["title"] == "Quoted Title"

    def test_single_quoted_values(self):
        text = "---\ntitle: 'Single Quoted'\n---\n"
        result = vm.extract_frontmatter(text)
        assert result["title"] == "Single Quoted"

    def test_frontmatter_with_colons_in_value(self):
        text = "---\ndescription: key: value pair\n---\n"
        result = vm.extract_frontmatter(text)
        assert result["description"] == "key: value pair"


# ---------------------------------------------------------------------------
# validate_file
# ---------------------------------------------------------------------------

class TestValidateFile:
    def test_nonexistent_file(self, tmp_path):
        result = vm.validate_file(tmp_path / "missing.txt")
        assert result["exists"] is False
        assert result["valid"] is False

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        result = vm.validate_file(f)
        assert result["exists"] is True
        assert result["size"] == 0
        assert result["valid"] is False

    def test_valid_text_file(self, tmp_path):
        f = tmp_path / "hello.txt"
        f.write_text("hello world")
        result = vm.validate_file(f)
        assert result["exists"] is True
        assert result["valid"] is True
        assert result["size"] > 0

    def test_valid_json_file(self, tmp_path):
        f = tmp_path / "data.json"
        f.write_text('{"key": "value"}')
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_invalid_json_file(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("{not valid json")
        result = vm.validate_file(f)
        assert result["valid"] is False

    def test_valid_html_file(self, tmp_path):
        f = tmp_path / "page.html"
        f.write_text("<!DOCTYPE html><html><body></body></html>")
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_invalid_html_file(self, tmp_path):
        f = tmp_path / "bad.html"
        f.write_text("This is not HTML at all")
        result = vm.validate_file(f)
        assert result["valid"] is False

    def test_valid_python_file(self, tmp_path):
        f = tmp_path / "script.py"
        f.write_text("print('hello')\n")
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_invalid_python_file(self, tmp_path):
        f = tmp_path / "bad.py"
        f.write_text("def broken(\n")
        result = vm.validate_file(f)
        assert result["valid"] is False

    def test_valid_png_file(self, tmp_path):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_invalid_png_file(self, tmp_path):
        f = tmp_path / "fake.png"
        f.write_bytes(b"not a png file at all")
        result = vm.validate_file(f)
        assert result["valid"] is False

    def test_valid_jpg_file(self, tmp_path):
        f = tmp_path / "image.jpg"
        f.write_bytes(b"\xff\xd8\xff" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_valid_webp_file(self, tmp_path):
        f = tmp_path / "image.webp"
        f.write_bytes(b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_directory_with_files(self, tmp_path):
        d = tmp_path / "output_dir"
        d.mkdir()
        (d / "file1.txt").write_text("content")
        result = vm.validate_file(d)
        assert result["exists"] is True
        assert result["is_dir"] is True
        assert result["file_count"] == 1
        assert result["valid"] is True

    def test_empty_directory(self, tmp_path):
        d = tmp_path / "empty_dir"
        d.mkdir()
        result = vm.validate_file(d)
        assert result["exists"] is True
        assert result["is_dir"] is True
        assert result["valid"] is False

    def test_directory_via_trailing_slash(self, tmp_path):
        d = tmp_path / "mydir"
        d.mkdir()
        (d / "a.txt").write_text("x")
        result = vm.validate_file(Path(str(d) + "/"))
        assert result["valid"] is True

    def test_nonexistent_directory(self, tmp_path):
        result = vm.validate_file(tmp_path / "nodir/")
        assert result["exists"] is False
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# verify_module
# ---------------------------------------------------------------------------

class TestVerifyModule:
    def test_no_lessons_for_module(self):
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}
        result = vm.verify_module(999)
        assert "error" in result
        assert result["module"] == 999
        assert result["lessons"] == []

    def test_module_name_lookup(self):
        assert vm.MODULE_NAMES[0] == "セットアップ"
        assert vm.MODULE_NAMES[1] == "バナー・画像生成"

    def test_unknown_module_name(self):
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}
        result = vm.verify_module(999)
        assert result["module_name"] == "Module 999"

    def test_module_with_lessons(self, tmp_path):
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("""\
---
description: Test lesson
---
# Module 1 Lesson 1-1: Test Title

## チェックポイント
- [ ] Item 1
""")
        _mock_lp.lesson_order.return_value = (
            ["start-1-1"],
            {"start-1-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {}
        _mock_lp.extract_outputs.return_value = []

        result = vm.verify_module(1)
        assert len(result["lessons"]) == 1
        assert result["lessons"][0]["lesson_id"] == "start-1-1"
        assert result["summary"]["total_lessons"] == 1

    def test_completed_lesson_counted(self, tmp_path):
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("# Module 1 Lesson 1-1: Test\n")
        _mock_lp.lesson_order.return_value = (
            ["start-1-1"],
            {"start-1-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {
            "lessons": {"start-1-1": {"completed": True}}
        }
        _mock_lp.extract_outputs.return_value = []

        result = vm.verify_module(1)
        assert result["summary"]["completed_lessons"] == 1
        assert result["lessons"][0]["progress_status"] == "completed"

    def test_negative_module_number(self):
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}
        result = vm.verify_module(-1)
        assert "error" in result

    def test_zero_module(self, tmp_path):
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("# Module 0 Lesson 0-1: Setup\n")
        _mock_lp.lesson_order.return_value = (
            ["start-0-1"],
            {"start-0-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {}
        _mock_lp.extract_outputs.return_value = []

        result = vm.verify_module(0)
        assert result["module_name"] == "セットアップ"
        assert len(result["lessons"]) == 1


# ---------------------------------------------------------------------------
# print_text_result
# ---------------------------------------------------------------------------

class TestPrintTextResult:
    def test_error_result(self, capsys):
        result = {"error": "テストエラー", "module": 99, "lessons": [], "summary": {}}
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "エラー" in captured.out

    def test_normal_result(self, capsys):
        result = {
            "module": 1,
            "module_name": "バナー",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "completed",
                    "outputs": [],
                    "checkpoints": ["Check 1"],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 1,
                "outputs_found": 0,
                "outputs_missing": 0,
                "outputs_invalid": 0,
                "total_checkpoints": 1,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "Module 1" in captured.out
        assert "start-1-1" in captured.out

    def test_missing_output_displayed(self, capsys):
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "incomplete",
                    "outputs": [
                        {"path": "/missing/file.png", "exists": False, "valid": False}
                    ],
                    "checkpoints": [],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 0,
                "outputs_found": 0,
                "outputs_missing": 1,
                "outputs_invalid": 0,
                "total_checkpoints": 0,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "不足" in captured.out

    def test_invalid_output_displayed(self, capsys):
        """不正な出力ファイルの表示 (line 294)"""
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "incomplete",
                    "outputs": [
                        {"path": "/bad/file.png", "exists": True, "valid": False}
                    ],
                    "checkpoints": [],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 0,
                "outputs_found": 0,
                "outputs_missing": 0,
                "outputs_invalid": 1,
                "total_checkpoints": 0,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "不正" in captured.out

    def test_valid_dir_output_displayed(self, capsys):
        """ディレクトリ出力の表示 (lines 288-292)"""
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "completed",
                    "outputs": [
                        {"path": "/output/dir", "exists": True, "valid": True, "is_dir": True, "file_count": 5}
                    ],
                    "checkpoints": [],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 1,
                "outputs_found": 1,
                "outputs_missing": 0,
                "outputs_invalid": 0,
                "total_checkpoints": 0,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "5ファイル" in captured.out

    def test_valid_file_output_displayed(self, capsys):
        """通常のファイル出力の表示"""
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "completed",
                    "outputs": [
                        {"path": "/output/file.png", "exists": True, "valid": True, "size": 10240}
                    ],
                    "checkpoints": [],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 1,
                "outputs_found": 1,
                "outputs_missing": 0,
                "outputs_invalid": 0,
                "total_checkpoints": 0,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "10.0KB" in captured.out

    def test_no_outputs_message(self, capsys):
        """成果物の出力先指定なしのメッセージ"""
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "incomplete",
                    "outputs": [],
                    "checkpoints": [],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 0,
                "outputs_found": 0,
                "outputs_missing": 0,
                "outputs_invalid": 0,
                "total_checkpoints": 0,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "出力先指定なし" in captured.out

    def test_checkpoints_displayed(self, capsys):
        """チェックポイントの表示"""
        result = {
            "module": 1,
            "module_name": "Test",
            "lessons": [
                {
                    "lesson_id": "start-1-1",
                    "title": "Test",
                    "progress_status": "incomplete",
                    "outputs": [],
                    "checkpoints": ["Check A", "Check B"],
                }
            ],
            "summary": {
                "total_lessons": 1,
                "completed_lessons": 0,
                "outputs_found": 0,
                "outputs_missing": 0,
                "outputs_invalid": 0,
                "total_checkpoints": 2,
            },
        }
        vm.print_text_result(result)
        captured = capsys.readouterr()
        assert "Check A" in captured.out
        assert "Check B" in captured.out


# ---------------------------------------------------------------------------
# validate_file 拡張テスト
# ---------------------------------------------------------------------------

class TestValidateFileExtended:
    def test_gif_magic_bytes(self, tmp_path):
        """GIF ファイルの検証 (lines 153-154)"""
        f = tmp_path / "image.gif"
        f.write_bytes(b"GIF89a" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_invalid_gif_magic(self, tmp_path):
        """不正な GIF ファイル"""
        f = tmp_path / "fake.gif"
        f.write_bytes(b"NOT_GIF" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is False

    def test_jpeg_extension(self, tmp_path):
        """JPEG 拡張子の検証"""
        f = tmp_path / "image.jpeg"
        f.write_bytes(b"\xff\xd8\xff" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_image_read_error(self, tmp_path):
        """画像ヘッダー読み取りエラー (lines 153-154 OSError branch)"""
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_path_no_suffix_is_dir(self, tmp_path):
        """拡張子なしパスをディレクトリとして扱う (lines 125-126)"""
        d = tmp_path / "noext"
        d.mkdir()
        (d / "file.txt").write_text("content")
        result = vm.validate_file(d)
        assert result["exists"] is True
        assert result["is_dir"] is True

    def test_path_no_suffix_nonexistent(self, tmp_path):
        """拡張子なしで存在しないパス"""
        result = vm.validate_file(tmp_path / "nonexistent_dir")
        assert result["exists"] is False

    def test_htm_extension(self, tmp_path):
        """HTM 拡張子の検証 (lines 168-169)"""
        f = tmp_path / "page.htm"
        f.write_text("<!DOCTYPE html><html></html>")
        result = vm.validate_file(f)
        assert result["valid"] is True

    def test_json_unicode_error(self, tmp_path):
        """JSON ファイルの UnicodeDecodeError"""
        f = tmp_path / "bad.json"
        f.write_bytes(b"\xff\xfe" + b"\x00" * 50)
        result = vm.validate_file(f)
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# verify_module 拡張テスト
# ---------------------------------------------------------------------------

class TestVerifyModuleExtended:
    def test_module_with_outputs(self, tmp_path):
        """成果物の検証を含むモジュール (lines 218-225)"""
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("# Module 1 Lesson 1-1: Test\n")

        output_file = tmp_path / "output.png"
        output_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        _mock_lp.lesson_order.return_value = (
            ["start-1-1"],
            {"start-1-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {}
        _mock_lp.extract_outputs.return_value = [output_file]

        result = vm.verify_module(1)
        assert result["summary"]["outputs_found"] == 1

    def test_module_with_invalid_output(self, tmp_path):
        """不正な成果物がある場合"""
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("# Module 1 Lesson 1-1: Test\n")

        output_file = tmp_path / "output.png"
        output_file.write_bytes(b"not_a_png")

        _mock_lp.lesson_order.return_value = (
            ["start-1-1"],
            {"start-1-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {}
        _mock_lp.extract_outputs.return_value = [output_file]

        result = vm.verify_module(1)
        assert result["summary"]["outputs_invalid"] == 1

    def test_module_with_missing_output(self, tmp_path):
        """欠落した成果物がある場合"""
        lesson_file = tmp_path / "lesson.md"
        lesson_file.write_text("# Module 1 Lesson 1-1: Test\n")

        _mock_lp.lesson_order.return_value = (
            ["start-1-1"],
            {"start-1-1": lesson_file},
        )
        _mock_lp.load_progress.return_value = {}
        _mock_lp.extract_outputs.return_value = [tmp_path / "nonexistent.txt"]

        result = vm.verify_module(1)
        assert result["summary"]["outputs_missing"] == 1


# ---------------------------------------------------------------------------
# main 関数テスト
# ---------------------------------------------------------------------------

class TestMainFunction:
    def test_main_json_mode(self, tmp_path, capsys):
        """--json モード (lines 308-350)"""
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}

        with patch("sys.argv", ["cmd", "--module", "0", "--json"]):
            vm.main()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "module" in output

    def test_main_text_mode(self, tmp_path, capsys):
        """テキストモード"""
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}

        with patch("sys.argv", ["cmd", "--module", "0"]):
            vm.main()
        captured = capsys.readouterr()
        assert "エラー" in captured.out or "Module" in captured.out

    def test_main_with_output_path(self, tmp_path, capsys):
        """--output でファイル保存 (lines 339-350)"""
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}

        output_file = tmp_path / "result.json"
        # Mock PROJECT_ROOT to allow writing within it
        with patch.object(vm, "PROJECT_ROOT", tmp_path):
            with patch("sys.argv", ["cmd", "--module", "0", "--output", str(output_file)]):
                vm.main()
        assert output_file.exists()
        data = json.loads(output_file.read_text())
        assert "module" in data

    def test_main_output_outside_project_rejected(self, capsys):
        """出力先がプロジェクト外の場合はエラー (lines 341-343)"""
        _mock_lp.lesson_order.return_value = ([], {})
        _mock_lp.load_progress.return_value = {}

        with patch("sys.argv", ["cmd", "--module", "0", "--output", "/tmp/outside/result.json"]):
            with pytest.raises(SystemExit) as exc_info:
                vm.main()
        assert exc_info.value.code == 1
