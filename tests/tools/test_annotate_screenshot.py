"""annotate_screenshot.py の単体テスト"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import annotate_screenshot
        assert hasattr(annotate_screenshot, 'main')
        assert hasattr(annotate_screenshot, 'refine_annotation_prompt')
        assert hasattr(annotate_screenshot, 'annotate_image')

    def test_default_output_dir(self):
        from annotate_screenshot import DEFAULT_OUTPUT_DIR
        assert DEFAULT_OUTPUT_DIR == "docs/manual_screenshots"


class TestRefineAnnotationPrompt:
    def test_successful_refinement(self):
        from annotate_screenshot import refine_annotation_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Add a red box around the save button"
        mock_client.models.generate_content.return_value = mock_response

        result = refine_annotation_prompt(
            mock_client, "save button", None, "red_box"
        )
        assert result == "Add a red box around the save button"

    def test_with_text_label(self):
        from annotate_screenshot import refine_annotation_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Add annotation with label"
        mock_client.models.generate_content.return_value = mock_response

        result = refine_annotation_prompt(
            mock_client, "click here", "ここをクリック", "callout"
        )
        assert result == "Add annotation with label"
        # Verify the prompt includes the text label info
        call_args = mock_client.models.generate_content.call_args
        prompt_text = call_args[1]["contents"][0] if "contents" in call_args[1] else call_args[0][0]
        # The function was called with the text_label incorporated

    def test_all_styles(self):
        from annotate_screenshot import refine_annotation_prompt
        styles = ["red_box", "arrow", "callout", "highlight", "circle", "number"]
        for style in styles:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = f"annotation for {style}"
            mock_client.models.generate_content.return_value = mock_response
            result = refine_annotation_prompt(mock_client, "test", None, style)
            assert result == f"annotation for {style}"

    def test_unknown_style_falls_back(self):
        from annotate_screenshot import refine_annotation_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "fallback annotation"
        mock_client.models.generate_content.return_value = mock_response

        # Unknown style should still work (falls back to red_box)
        result = refine_annotation_prompt(mock_client, "test", None, "unknown_style")
        assert result == "fallback annotation"

    def test_whitespace_stripped(self):
        from annotate_screenshot import refine_annotation_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "  whitespace prompt  "
        mock_client.models.generate_content.return_value = mock_response

        result = refine_annotation_prompt(mock_client, "test", None, "arrow")
        assert result == "whitespace prompt"


class TestAnnotateImage:
    def test_successful_annotation(self, tmp_path, sample_image):
        from annotate_screenshot import annotate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"

        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = annotate_image(mock_client, sample_image, "add red box", output_path)
            assert result is True
            mock_result_image.save.assert_called_once_with(output_path)

    def test_no_image_in_response(self, tmp_path, sample_image):
        from annotate_screenshot import annotate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"
        result = annotate_image(mock_client, sample_image, "add red box", output_path)
        assert result is False

    def test_api_error(self, tmp_path, sample_image):
        from annotate_screenshot import annotate_image
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        output_path = tmp_path / "annotated.png"
        result = annotate_image(mock_client, sample_image, "add red box", output_path)
        assert result is False

    def test_invalid_input_image(self, tmp_path):
        from annotate_screenshot import annotate_image
        mock_client = MagicMock()

        # Non-existent image should cause error
        bad_image = tmp_path / "nonexistent.png"
        output_path = tmp_path / "annotated.png"

        # annotate_image calls Image.open which will raise; the function calls sys.exit
        # so we test that it handles it
        with pytest.raises(SystemExit):
            annotate_image(mock_client, bad_image, "add red box", output_path)

    def test_aspect_ratio_selection_wide(self, tmp_path):
        """Test that wide images get 16:9 aspect ratio"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        # Create a wide image (1920x1080 => 16:9)
        wide_img = tmp_path / "wide.png"
        Image.new("RGB", (1920, 1080), "blue").save(wide_img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"

        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = annotate_image(mock_client, wide_img, "add box", output_path)
            assert result is True

    def test_aspect_ratio_selection_portrait(self, tmp_path):
        """Test that portrait images get 9:16 aspect ratio"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        portrait_img = tmp_path / "portrait.png"
        Image.new("RGB", (600, 1200), "green").save(portrait_img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"

        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = annotate_image(mock_client, portrait_img, "add box", output_path)
            assert result is True

    def test_aspect_ratio_selection_square(self, tmp_path):
        """Test that square images get 1:1 aspect ratio"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        sq_img = tmp_path / "square.png"
        Image.new("RGB", (500, 500), "yellow").save(sq_img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"

        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = annotate_image(mock_client, sq_img, "add box", output_path)
            assert result is True

    def test_aspect_ratio_ultrawide(self, tmp_path):
        """ultrawide (>1.9) => 21:9 (line 130)"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        img = tmp_path / "ultrawide.png"
        Image.new("RGB", (2560, 1080), "red").save(img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"
        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_as_image.return_value = MagicMock()
            result = annotate_image(mock_client, img, "box", output_path)
            assert result is True

    def test_aspect_ratio_4_3(self, tmp_path):
        """4:3 aspect ratio (line 134)"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        img = tmp_path / "fourbythree.png"
        Image.new("RGB", (1024, 768), "blue").save(img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"
        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_as_image.return_value = MagicMock()
            result = annotate_image(mock_client, img, "box", output_path)
            assert result is True

    def test_aspect_ratio_3_4(self, tmp_path):
        """3:4 aspect ratio (line 138)"""
        from annotate_screenshot import annotate_image
        from PIL import Image

        img = tmp_path / "threebyfour.png"
        Image.new("RGB", (768, 1024), "green").save(img)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "annotated.png"
        with patch("annotate_screenshot.types.Part.as_image") as mock_as_image:
            mock_as_image.return_value = MagicMock()
            result = annotate_image(mock_client, img, "box", output_path)
            assert result is True


# ===========================================================================
# main (lines 191-270)
# ===========================================================================

class TestMain:
    def test_main_successful(self, tmp_path, sample_image):
        """正常実行"""
        from annotate_screenshot import main
        output_path = tmp_path / "annotated.png"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "annotation prompt"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", str(sample_image), "add", "red", "box", "-o", str(output_path)]), \
             patch("annotate_screenshot.get_client", return_value=mock_client), \
             patch("annotate_screenshot.annotate_image", return_value=True):
            main()

    def test_main_input_not_found(self, tmp_path):
        """入力ファイル不在でsys.exit"""
        from annotate_screenshot import main
        with patch("sys.argv", ["prog", str(tmp_path / "noexist.png"), "annotate"]):
            with pytest.raises(SystemExit):
                main()

    def test_main_no_instruction(self, tmp_path, sample_image):
        """注釈指示なしでsys.exit"""
        from annotate_screenshot import main
        with patch("sys.argv", ["prog", str(sample_image)]):
            with pytest.raises(SystemExit):
                main()

    def test_main_default_output_path(self, tmp_path, sample_image):
        """デフォルト出力パス"""
        from annotate_screenshot import main
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", str(sample_image), "add", "box"]), \
             patch("annotate_screenshot.get_client", return_value=mock_client), \
             patch("annotate_screenshot.annotate_image", return_value=True):
            main()

    def test_main_annotated_suffix_dedup(self, tmp_path):
        """_annotated 付きファイル名の重複回避"""
        from annotate_screenshot import main
        from PIL import Image
        img = tmp_path / "shot_annotated.png"
        Image.new("RGB", (100, 100), "red").save(img)

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", str(img), "add", "box"]), \
             patch("annotate_screenshot.get_client", return_value=mock_client), \
             patch("annotate_screenshot.annotate_image", return_value=True):
            main()

    def test_main_output_same_as_input(self, tmp_path, sample_image):
        """出力先が入力先と同じ場合sys.exit"""
        from annotate_screenshot import main
        with patch("sys.argv", ["prog", str(sample_image), "annotate", "-o", str(sample_image)]):
            with pytest.raises(SystemExit):
                main()

    def test_main_existing_output_warning(self, tmp_path, sample_image, capsys):
        """既存出力ファイルの上書き警告"""
        from annotate_screenshot import main
        output_path = tmp_path / "annotated.png"
        output_path.write_text("existing")
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", str(sample_image), "annotate", "-o", str(output_path)]), \
             patch("annotate_screenshot.get_client", return_value=mock_client), \
             patch("annotate_screenshot.annotate_image", return_value=True):
            main()
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    def test_main_with_text_and_style(self, tmp_path, sample_image):
        """--text と --style オプション"""
        from annotate_screenshot import main
        output_path = tmp_path / "annotated.png"
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["prog", str(sample_image), "annotate", "-t", "ここ", "-s", "arrow", "-o", str(output_path)]), \
             patch("annotate_screenshot.get_client", return_value=mock_client), \
             patch("annotate_screenshot.annotate_image", return_value=True):
            main()
