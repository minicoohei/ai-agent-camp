"""generate_slide.py の単体テスト"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helper: import with mocked dependencies
# ---------------------------------------------------------------------------

@pytest.fixture
def slide_module():
    """外部依存をモックしてモジュールをインポート"""
    mock_genai = MagicMock()
    mock_types = MagicMock()
    with patch.dict("sys.modules", {
        "google": MagicMock(),
        "google.genai": mock_genai,
        "google.genai.types": mock_types,
        "bootcamp_utils": MagicMock(
            get_client=MagicMock(return_value=MagicMock()),
            get_flash_model=MagicMock(return_value="flash-model"),
            get_image_model=MagicMock(return_value="image-model"),
        ),
    }):
        from tests.conftest import import_module_from_repo
        mod = import_module_from_repo("generate_slide", "tools/generate_slide.py")
        yield mod


# ---------------------------------------------------------------------------
# Module import & constants
# ---------------------------------------------------------------------------

class TestImportAndConstants:
    def test_import_module(self, slide_module):
        assert hasattr(slide_module, "main")
        assert hasattr(slide_module, "DESIGN_SPEC")
        assert hasattr(slide_module, "DEFAULT_OUTPUT_DIR")

    def test_design_spec_structure(self, slide_module):
        spec = slide_module.DESIGN_SPEC
        assert "background" in spec
        assert "main_color" in spec
        assert "sub_color" in spec
        assert "style" in spec

    def test_default_output_dir(self, slide_module):
        assert "slides" in slide_module.DEFAULT_OUTPUT_DIR


# ---------------------------------------------------------------------------
# get_client
# ---------------------------------------------------------------------------

class TestGetClient:
    def test_no_key(self, slide_module, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        with pytest.raises(SystemExit):
            slide_module.get_client()

    def test_with_key(self, slide_module, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        client = slide_module.get_client()
        assert client is not None


# ---------------------------------------------------------------------------
# sanitize_filename
# ---------------------------------------------------------------------------

class TestSanitizeFilename:
    def test_basic(self, slide_module):
        assert slide_module.sanitize_filename("hello world") == "hello_world"

    def test_special_chars(self, slide_module):
        result = slide_module.sanitize_filename('file<name>:test')
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result

    def test_length_limit(self, slide_module):
        long_name = "x" * 100
        result = slide_module.sanitize_filename(long_name, max_length=30)
        assert len(result) == 30

    def test_empty_string(self, slide_module):
        assert slide_module.sanitize_filename("") == ""

    def test_unicode_japanese(self, slide_module):
        result = slide_module.sanitize_filename("AIエージェントの仕組み")
        assert "AI" in result

    def test_multiple_spaces(self, slide_module):
        assert slide_module.sanitize_filename("a  b  c") == "a_b_c"

    def test_boundary_exact_max(self, slide_module):
        """ちょうどmax_lengthの場合はそのまま"""
        result = slide_module.sanitize_filename("abcde", max_length=5)
        assert result == "abcde"

    def test_boundary_one_over(self, slide_module):
        result = slide_module.sanitize_filename("abcdef", max_length=5)
        assert len(result) == 5


# ---------------------------------------------------------------------------
# generate_slide_content (API mocked)
# ---------------------------------------------------------------------------

class TestGenerateSlideContent:
    def test_returns_string(self, slide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"title": "Test", "points": ["a", "b"]}'
        mock_client.models.generate_content.return_value = mock_response

        result = slide_module.generate_slide_content(mock_client, "テスト")
        assert isinstance(result, str)

    def test_strips_json_block(self, slide_module):
        """```json ... ``` ブロックからJSONを抽出"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '```json\n{"title": "T"}\n```'
        mock_client.models.generate_content.return_value = mock_response

        result = slide_module.generate_slide_content(mock_client, "topic")
        assert result == '{"title": "T"}'

    def test_plain_json(self, slide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '   {"title": "T"}   '
        mock_client.models.generate_content.return_value = mock_response

        result = slide_module.generate_slide_content(mock_client, "topic")
        assert result == '{"title": "T"}'


# ---------------------------------------------------------------------------
# create_slide_prompt
# ---------------------------------------------------------------------------

class TestCreateSlidePrompt:
    def test_returns_string(self, slide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Create a professional slide..."
        mock_client.models.generate_content.return_value = mock_response

        result = slide_module.create_slide_prompt(
            mock_client, "topic", '{"title": "T"}', "auto"
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_all_styles(self, slide_module):
        """全スタイルでエラーが出ないことを確認"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt text"
        mock_client.models.generate_content.return_value = mock_response

        for style in ["auto", "title", "content", "diagram", "summary"]:
            result = slide_module.create_slide_prompt(
                mock_client, "t", "{}", style
            )
            assert isinstance(result, str)

    def test_unknown_style_falls_back_to_auto(self, slide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_response

        result = slide_module.create_slide_prompt(
            mock_client, "t", "{}", "unknown_style"
        )
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# generate_slide_image (API mocked)
# ---------------------------------------------------------------------------

class TestGenerateSlideImage:
    def test_success(self, slide_module, tmp_path):
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output = tmp_path / "slide.png"
        with patch.object(slide_module, "get_image_model", return_value="model"):
            result = slide_module.generate_slide_image(mock_client, "prompt", output)
        assert result is True

    def test_no_image_data(self, slide_module, tmp_path):
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output = tmp_path / "slide.png"
        with patch.object(slide_module, "get_image_model", return_value="model"):
            result = slide_module.generate_slide_image(mock_client, "prompt", output)
        assert result is False

    def test_api_error(self, slide_module, tmp_path):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")

        output = tmp_path / "slide.png"
        with patch.object(slide_module, "get_image_model", return_value="model"):
            result = slide_module.generate_slide_image(mock_client, "prompt", output)
        assert result is False

    def test_creates_parent_directory(self, slide_module, tmp_path):
        """出力先ディレクトリがなくても作成される"""
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output = tmp_path / "subdir" / "deep" / "slide.png"
        with patch.object(slide_module, "get_image_model", return_value="model"):
            result = slide_module.generate_slide_image(mock_client, "prompt", output)
        assert result is True


# ---------------------------------------------------------------------------
# main (lines 288-364)
# ---------------------------------------------------------------------------

class TestMain:
    def test_successful_run_with_output(self, slide_module, tmp_path):
        """正常実行: --output 指定"""
        output_path = tmp_path / "slide.png"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "content text"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", "テスト", "-o", str(output_path)]), \
             patch.object(slide_module, "get_client", return_value=mock_client), \
             patch.object(slide_module, "get_flash_model", return_value="flash"), \
             patch.object(slide_module, "generate_slide_image", return_value=True):
            slide_module.main()

    def test_successful_run_default_output(self, slide_module):
        """正常実行: デフォルト出力パス"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "content text"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", "AI", "Agent"]), \
             patch.object(slide_module, "get_client", return_value=mock_client), \
             patch.object(slide_module, "get_flash_model", return_value="flash"), \
             patch.object(slide_module, "generate_slide_image", return_value=True):
            slide_module.main()

    def test_failure_exits(self, slide_module, tmp_path):
        """生成失敗でsys.exit(1)"""
        output_path = tmp_path / "slide.png"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "content"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", "テスト", "-o", str(output_path)]), \
             patch.object(slide_module, "get_client", return_value=mock_client), \
             patch.object(slide_module, "get_flash_model", return_value="flash"), \
             patch.object(slide_module, "generate_slide_image", return_value=False):
            with pytest.raises(SystemExit):
                slide_module.main()

    def test_existing_output_warning(self, slide_module, tmp_path, capsys):
        """既存出力ファイルの上書き警告"""
        output_path = tmp_path / "slide.png"
        output_path.write_text("existing")
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "content"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", "テスト", "-o", str(output_path)]), \
             patch.object(slide_module, "get_client", return_value=mock_client), \
             patch.object(slide_module, "get_flash_model", return_value="flash"), \
             patch.object(slide_module, "generate_slide_image", return_value=True):
            slide_module.main()
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_with_style_option(self, slide_module, tmp_path):
        """--style オプション"""
        output_path = tmp_path / "slide.png"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "content"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", "テスト", "-s", "title", "-o", str(output_path)]), \
             patch.object(slide_module, "get_client", return_value=mock_client), \
             patch.object(slide_module, "get_flash_model", return_value="flash"), \
             patch.object(slide_module, "generate_slide_image", return_value=True):
            slide_module.main()
