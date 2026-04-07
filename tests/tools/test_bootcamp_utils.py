"""bootcamp_utils.py の単体テスト"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestImport:
    def test_import_module(self):
        import bootcamp_utils
        assert hasattr(bootcamp_utils, 'get_client')
        assert hasattr(bootcamp_utils, 'get_flash_model')
        assert hasattr(bootcamp_utils, 'get_image_model')


class TestGetClient:
    def test_no_api_key(self, clean_env):
        from bootcamp_utils import get_client
        with patch("dotenv.load_dotenv"):  # .env 再読み込みを防止
            result = get_client()
        assert result is None

    def test_with_gemini_key(self, monkeypatch):
        from bootcamp_utils import get_client
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")
        with patch("google.genai.Client") as mock_client:
            mock_client.return_value = "mock_client"
            result = get_client()
            assert result == "mock_client"

    def test_with_google_key(self, monkeypatch):
        from bootcamp_utils import get_client
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.setenv("GOOGLE_API_KEY", "test_google_key")
        with patch("google.genai.Client") as mock_client:
            mock_client.return_value = "mock_client"
            result = get_client()
            assert result == "mock_client"


class TestGetFlashModel:
    def test_default(self, monkeypatch):
        from bootcamp_utils import get_flash_model
        monkeypatch.delenv("GEMINI_FLASH_MODEL", raising=False)
        assert get_flash_model() == "gemini-3-flash-preview"

    def test_custom(self, monkeypatch):
        from bootcamp_utils import get_flash_model
        monkeypatch.setenv("GEMINI_FLASH_MODEL", "custom-model")
        assert get_flash_model() == "custom-model"


class TestGetImageModel:
    def test_default(self, monkeypatch):
        from bootcamp_utils import get_image_model
        monkeypatch.delenv("GEMINI_IMAGE_MODEL", raising=False)
        assert get_image_model() == "nano-banana-pro-preview"

    def test_custom(self, monkeypatch):
        from bootcamp_utils import get_image_model
        monkeypatch.setenv("GEMINI_IMAGE_MODEL", "custom-image")
        assert get_image_model() == "custom-image"


class TestGetLatestSpecstoryFiles:
    def test_no_directory(self, monkeypatch):
        from bootcamp_utils import get_latest_specstory_files
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", Path("/nonexistent"))
        result = get_latest_specstory_files()
        assert result == []

    def test_with_files(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        for i in range(5):
            (tmp_path / f"2024-01-0{i+1}_12-00Z-test.md").write_text(
                f"# Test {i}", encoding="utf-8"
            )
        result = bootcamp_utils.get_latest_specstory_files(limit=3)
        assert len(result) == 3

    def test_limit_param(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        for i in range(10):
            (tmp_path / f"2024-01-{i+1:02d}_12-00Z-test.md").write_text(
                f"# Test {i}", encoding="utf-8"
            )
        result = bootcamp_utils.get_latest_specstory_files(limit=5)
        assert len(result) == 5


class TestParseSpecstoryFile:
    def test_basic_parsing(self, tmp_path):
        from bootcamp_utils import parse_specstory_file
        content = """# Test Session (2024-01-15 12:00Z)

cursor Session abc-def-123

---

_**User**_

Hello, this is a test

---

_**Agent (Claude)**_

Hi, I can help with that

---
"""
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = parse_specstory_file(f)
        assert result["title"] == "Test Session"
        assert result["session_id"] == "abc-def-123"
        assert result["timestamp"] == "2024-01-15 12:00Z"
        assert len(result["user_messages"]) >= 1
        assert "raw_content" in result

    def test_no_metadata(self, tmp_path):
        from bootcamp_utils import parse_specstory_file
        f = tmp_path / "minimal.md"
        f.write_text("Just some text", encoding="utf-8")
        result = parse_specstory_file(f)
        assert result["title"] == "minimal"
        assert result["session_id"] == ""
        assert result["timestamp"] == ""


class TestExtractTitleFromFilename:
    def test_standard_filename(self):
        from bootcamp_utils import extract_title_from_filename
        result = extract_title_from_filename("2024-01-15_12-00Z-my-test-session.md")
        assert "My Test Session" == result

    def test_nonstandard_filename(self):
        from bootcamp_utils import extract_title_from_filename
        result = extract_title_from_filename("random-file.md")
        assert result == "random-file.md"


class TestExtractTimestampFromFilename:
    def test_standard_filename(self):
        from bootcamp_utils import extract_timestamp_from_filename
        result = extract_timestamp_from_filename("2024-01-15_12-30Z-test.md")
        assert result == "2024-01-15 12:30Z"

    def test_nonstandard_filename(self):
        from bootcamp_utils import extract_timestamp_from_filename
        result = extract_timestamp_from_filename("random.md")
        assert result == ""


class TestGetRecentSpecstoryContent:
    def test_no_files(self, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", Path("/nonexistent"))
        result = bootcamp_utils.get_recent_specstory_content()
        assert result == ""

    def test_with_files(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        f = tmp_path / "2024-01-15_12-00Z-test.md"
        f.write_text(
            "# Test (2024-01-15 12:00Z)\n\ncursor Session abc-123\n\n---\n\n_**User**_\n\nHello\n\n---\n",
            encoding="utf-8",
        )
        result = bootcamp_utils.get_recent_specstory_content(limit=1)
        assert "Test" in result


class TestListSpecstoryFilesForSelection:
    def test_returns_formatted_list(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        f = tmp_path / "2024-01-15_12-00Z-test.md"
        f.write_text("# Test (2024-01-15 12:00Z)\ncursor Session abc-123", encoding="utf-8")
        result = bootcamp_utils.list_specstory_files_for_selection(limit=10)
        assert len(result) == 1
        assert result[0]["index"] == 1
        assert "filename" in result[0]


class TestGetSelectedSpecstoryFiles:
    def test_single_selection(self, tmp_path, monkeypatch):
        import bootcamp_utils
        available = [
            {"path": tmp_path / "file1.md"},
            {"path": tmp_path / "file2.md"},
        ]
        result = bootcamp_utils.get_selected_specstory_files("1", available)
        assert len(result) == 1
        assert result[0] == tmp_path / "file1.md"

    def test_range_selection(self, tmp_path, monkeypatch):
        import bootcamp_utils
        available = [
            {"path": tmp_path / "file1.md"},
            {"path": tmp_path / "file2.md"},
            {"path": tmp_path / "file3.md"},
        ]
        result = bootcamp_utils.get_selected_specstory_files("1-3", available)
        assert len(result) == 3

    def test_comma_separated(self, tmp_path, monkeypatch):
        import bootcamp_utils
        available = [
            {"path": tmp_path / "file1.md"},
            {"path": tmp_path / "file2.md"},
            {"path": tmp_path / "file3.md"},
        ]
        result = bootcamp_utils.get_selected_specstory_files("1,3", available)
        assert len(result) == 2

    def test_invalid_selection(self, tmp_path, monkeypatch):
        import bootcamp_utils
        available = [{"path": tmp_path / "file1.md"}]
        result = bootcamp_utils.get_selected_specstory_files("abc", available)
        assert result == []

    def test_out_of_range(self, tmp_path, monkeypatch):
        import bootcamp_utils
        available = [{"path": tmp_path / "file1.md"}]
        result = bootcamp_utils.get_selected_specstory_files("5", available)
        assert result == []


class TestGetSpecstoryFilesByNames:
    def test_existing_files(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        f = tmp_path / "test.md"
        f.write_text("content", encoding="utf-8")
        result = bootcamp_utils.get_specstory_files_by_names(["test.md"])
        assert len(result) == 1

    def test_nonexistent_files(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        result = bootcamp_utils.get_specstory_files_by_names(["nonexistent.md"])
        assert result == []

    def test_no_directory(self, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", Path("/nonexistent"))
        result = bootcamp_utils.get_specstory_files_by_names(["test.md"])
        assert result == []


class TestListSpecstoryFilesJson:
    def test_returns_valid_json(self, tmp_path, monkeypatch):
        import bootcamp_utils
        monkeypatch.setattr(bootcamp_utils, "SPECSTORY_DIR", tmp_path)
        f = tmp_path / "2024-01-15_12-00Z-test.md"
        f.write_text("# Test (2024-01-15 12:00Z)\ncursor Session abc-123", encoding="utf-8")
        result = bootcamp_utils.list_specstory_files_json(limit=10)
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) == 1
        assert "id" in parsed[0]
        assert "label" in parsed[0]


class TestGetSpecstoryContentFromFiles:
    def test_with_files(self, tmp_path):
        from bootcamp_utils import get_specstory_content_from_files
        f = tmp_path / "test.md"
        f.write_text(
            "# Test (2024-01-15 12:00Z)\ncursor Session abc-123\n---\n_**User**_\n\nHello\n---\n",
            encoding="utf-8",
        )
        content, filenames = get_specstory_content_from_files([f])
        assert "Test" in content
        assert "test.md" in filenames

    def test_nonexistent_file(self, tmp_path):
        from bootcamp_utils import get_specstory_content_from_files
        content, filenames = get_specstory_content_from_files([tmp_path / "nonexistent.md"])
        assert content == ""
        assert filenames == []


class TestMarkdownToHtml:
    def test_headings(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("# Heading 1\n\n## Heading 2\n\n### Heading 3")
        assert "<h1>Heading 1</h1>" in result
        assert "<h2>Heading 2</h2>" in result
        assert "<h3>Heading 3</h3>" in result

    def test_bold(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("**bold text**")
        assert "<strong>bold text</strong>" in result

    def test_italic(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("*italic text*")
        assert "<em>italic text</em>" in result

    def test_inline_code(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("`code`")
        assert "<code>code</code>" in result

    def test_horizontal_rule(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("---")
        assert "<hr>" in result

    def test_bullet_list(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("- item1\n- item2")
        assert "<ul>" in result
        assert "<li>item1</li>" in result

    def test_numbered_list(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("1. first\n2. second")
        assert "<ol>" in result
        assert "<li>first</li>" in result

    def test_code_block(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("```python\nprint('hello')\n```")
        assert "<pre>" in result
        assert "print" in result

    def test_empty_input(self):
        from bootcamp_utils import markdown_to_html
        assert markdown_to_html("") == ""

    def test_paragraphs(self):
        from bootcamp_utils import markdown_to_html
        result = markdown_to_html("para 1\n\npara 2")
        assert "<p>" in result


class TestPlantumlEncode:
    def test_basic_encode(self):
        from bootcamp_utils import plantuml_encode
        result = plantuml_encode("@startuml\nA -> B\n@enduml")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_empty_input(self):
        from bootcamp_utils import plantuml_encode
        result = plantuml_encode("")
        assert isinstance(result, str)


class TestGeneratePlantumlUrl:
    def test_returns_url(self):
        from bootcamp_utils import generate_plantuml_url
        url = generate_plantuml_url("@startuml\nA -> B\n@enduml")
        assert url.startswith("https://www.plantuml.com/plantuml/svg/")


class TestValidatePlantumlUrl:
    def test_valid_url(self):
        from bootcamp_utils import validate_plantuml_url
        with patch("urllib.request.urlopen") as mock_open:
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.__enter__ = MagicMock(return_value=mock_response)
            mock_response.__exit__ = MagicMock(return_value=False)
            mock_open.return_value = mock_response
            assert validate_plantuml_url("https://example.com/svg") is True

    def test_invalid_url(self):
        from bootcamp_utils import validate_plantuml_url
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            assert validate_plantuml_url("https://bad.url") is False


class TestGeneratePlantumlImgTag:
    def test_without_validation(self):
        from bootcamp_utils import generate_plantuml_img_tag
        result = generate_plantuml_img_tag("@startuml\nA -> B\n@enduml")
        assert "<img" in result
        assert "plantuml.com" in result

    def test_with_validation_success(self):
        from bootcamp_utils import generate_plantuml_img_tag
        with patch("bootcamp_utils.validate_plantuml_url", return_value=True):
            result = generate_plantuml_img_tag("@startuml\n@enduml", validate=True)
            assert "<img" in result

    def test_with_validation_failure(self):
        from bootcamp_utils import generate_plantuml_img_tag
        with patch("bootcamp_utils.validate_plantuml_url", return_value=False):
            result = generate_plantuml_img_tag("@startuml\n@enduml", validate=True)
            assert "warning-box" in result
            assert "図の生成に失敗しました" in result


class TestBuildReferencedFilesHtml:
    def test_empty_list(self):
        from bootcamp_utils import build_referenced_files_html
        assert build_referenced_files_html([]) == ""

    def test_with_filenames(self):
        from bootcamp_utils import build_referenced_files_html
        result = build_referenced_files_html(["2024-01-15_12-00Z-test.md"])
        assert "info-box" in result
        assert "test.md" in result


class TestCreateHtmlTemplate:
    def test_basic_template(self):
        from bootcamp_utils import create_html_template
        html = create_html_template("Test Title", "<p>Content</p>")
        assert "Test Title" in html
        assert "<p>Content</p>" in html
        assert "<!DOCTYPE html>" in html

    def test_with_css_extra(self):
        from bootcamp_utils import create_html_template
        html = create_html_template("T", "<p>C</p>", css_extra=".custom { color: red; }")
        assert ".custom { color: red; }" in html


class TestSaveHtmlFile:
    def test_saves_file(self, tmp_path):
        from bootcamp_utils import save_html_file
        output = tmp_path / "output.html"
        save_html_file("<html></html>", output, "Test")
        assert output.exists()
        assert output.read_text() == "<html></html>"

    def test_creates_parent_dirs(self, tmp_path):
        from bootcamp_utils import save_html_file
        output = tmp_path / "sub" / "dir" / "output.html"
        save_html_file("<html></html>", output, "Test")
        assert output.exists()
