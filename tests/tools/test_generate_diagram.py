"""generate_diagram.py の単体テスト"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import generate_diagram
        assert hasattr(generate_diagram, 'main')
        assert hasattr(generate_diagram, 'refine_prompt')
        assert hasattr(generate_diagram, 'generate_image')

    def test_default_output_dir(self):
        from generate_diagram import DEFAULT_OUTPUT_DIR
        assert DEFAULT_OUTPUT_DIR == "reports/visualizations"


class TestRefinePrompt:
    def test_successful_refinement(self):
        from generate_diagram import refine_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "A detailed infographic showing the water cycle"
        mock_client.models.generate_content.return_value = mock_response

        result = refine_prompt(mock_client, "water cycle", "colorful_infographic")
        assert result == "A detailed infographic showing the water cycle"
        mock_client.models.generate_content.assert_called_once()

    def test_long_topic_preview_truncated(self):
        from generate_diagram import refine_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "  refined prompt  "
        mock_client.models.generate_content.return_value = mock_response

        # Long topic (>50 chars) should be handled without error
        long_topic = "a" * 100
        result = refine_prompt(mock_client, long_topic, "sketch")
        assert result == "refined prompt"

    def test_short_topic_no_truncation(self):
        from generate_diagram import refine_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "refined"
        mock_client.models.generate_content.return_value = mock_response

        result = refine_prompt(mock_client, "short", "minimalist")
        assert result == "refined"

    def test_whitespace_stripped(self):
        from generate_diagram import refine_prompt
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "\n  prompt with spaces  \n"
        mock_client.models.generate_content.return_value = mock_response

        result = refine_prompt(mock_client, "test", "photorealistic")
        assert result == "prompt with spaces"

    def test_all_styles(self):
        from generate_diagram import refine_prompt
        styles = ["colorful_infographic", "sketch", "photorealistic",
                   "minimalist", "claymation", "pixel_art"]
        for style in styles:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.text = f"prompt for {style}"
            mock_client.models.generate_content.return_value = mock_response
            result = refine_prompt(mock_client, "topic", style)
            assert result == f"prompt for {style}"


class TestGenerateImage:
    def test_successful_generation(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "diagram.png"

        with patch("generate_diagram.types.Part.as_image") as mock_as_image:
            mock_image = MagicMock()
            mock_as_image.return_value = mock_image
            result = generate_image(mock_client, "test prompt", output_path)
            assert result is True
            mock_image.save.assert_called_once_with(output_path)

    def test_no_image_in_response(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "diagram.png"
        result = generate_image(mock_client, "test prompt", output_path)
        assert result is False

    def test_api_error(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        output_path = tmp_path / "diagram.png"
        result = generate_image(mock_client, "test prompt", output_path)
        assert result is False

    def test_custom_aspect_ratio(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "diagram.png"

        with patch("generate_diagram.types.Part.as_image") as mock_as_image:
            mock_image = MagicMock()
            mock_as_image.return_value = mock_image
            result = generate_image(mock_client, "test", output_path, aspect_ratio="1:1")
            assert result is True

    def test_output_dir_creation(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        # Nested directory that doesn't exist yet
        output_path = tmp_path / "a" / "b" / "c" / "diagram.png"

        with patch("generate_diagram.types.Part.as_image") as mock_as_image:
            mock_image = MagicMock()
            mock_as_image.return_value = mock_image
            result = generate_image(mock_client, "test", output_path)
            assert result is True
            assert output_path.parent.exists()

    def test_empty_parts_list(self, tmp_path):
        from generate_diagram import generate_image
        mock_client = MagicMock()

        mock_response = MagicMock()
        mock_response.parts = []
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "diagram.png"
        result = generate_image(mock_client, "test", output_path)
        assert result is False
