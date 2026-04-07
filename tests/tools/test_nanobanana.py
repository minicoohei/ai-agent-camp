"""nanobanana.py の単体テスト"""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import nanobanana
        assert hasattr(nanobanana, 'main')

    def test_import_functions(self):
        from nanobanana import generate_image, edit_image, get_aspect_ratio, sanitize_filename
        assert callable(generate_image)
        assert callable(edit_image)
        assert callable(get_aspect_ratio)
        assert callable(sanitize_filename)


class TestGetAspectRatio:
    def test_wide(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1920, 1080) == "16:9"

    def test_square(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1080, 1080) == "1:1"

    def test_portrait(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1080, 1920) == "9:16"

    def test_ultrawide(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(2560, 1080) == "21:9"

    def test_four_three(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1024, 768) == "4:3"

    def test_three_four(self):
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(768, 1024) == "3:4"

    def test_boundary_ultrawide(self):
        # aspect_ratio > 1.9 => 21:9
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1910, 1000) == "21:9"

    def test_boundary_wide(self):
        # 1.5 < aspect_ratio <= 1.9 => 16:9
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1600, 1000) == "16:9"

    def test_boundary_four_three(self):
        # 1.2 < aspect_ratio <= 1.5 => 4:3
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1300, 1000) == "4:3"

    def test_boundary_square_low(self):
        # 0.9 < aspect_ratio <= 1.2 => 1:1
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(1000, 1000) == "1:1"

    def test_boundary_three_four(self):
        # 0.7 < aspect_ratio <= 0.9 => 3:4
        from nanobanana import get_aspect_ratio
        assert get_aspect_ratio(800, 1000) == "3:4"


class TestSanitizeFilename:
    def test_basic(self):
        from nanobanana import sanitize_filename
        assert sanitize_filename("hello world") == "hello_world"

    def test_special_chars(self):
        from nanobanana import sanitize_filename
        result = sanitize_filename('test<>file')
        assert "<" not in result
        assert ">" not in result

    def test_truncation(self):
        from nanobanana import sanitize_filename
        assert len(sanitize_filename("x" * 100)) == 50

    def test_empty_string(self):
        from nanobanana import sanitize_filename
        assert sanitize_filename("") == ""


class TestGenerateImage:
    def test_successful_generation(self, tmp_path):
        from nanobanana import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "output.png"

        with patch("nanobanana.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = generate_image(mock_client, "a cat", output_path)
            assert result is True
            mock_result_image.save.assert_called_once_with(output_path)

    def test_no_image_in_response(self, tmp_path):
        from nanobanana import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "output.png"
        result = generate_image(mock_client, "a cat", output_path)
        assert result is False

    def test_api_error(self, tmp_path):
        from nanobanana import generate_image
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        output_path = tmp_path / "output.png"
        result = generate_image(mock_client, "a cat", output_path)
        assert result is False

    def test_custom_aspect_ratio(self, tmp_path):
        from nanobanana import generate_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "output.png"

        with patch("nanobanana.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = generate_image(mock_client, "a cat", output_path, aspect_ratio="1:1")
            assert result is True


class TestEditImage:
    def test_successful_edit(self, tmp_path, sample_image):
        from nanobanana import edit_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "edited.png"

        with patch("nanobanana.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = edit_image(mock_client, [sample_image], "make it blue", output_path)
            assert result is True
            mock_result_image.save.assert_called_once_with(output_path)

    def test_edit_no_image_in_response(self, tmp_path, sample_image):
        from nanobanana import edit_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "edited.png"
        result = edit_image(mock_client, [sample_image], "make it blue", output_path)
        assert result is False

    def test_edit_api_error(self, tmp_path, sample_image):
        from nanobanana import edit_image
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        output_path = tmp_path / "edited.png"
        result = edit_image(mock_client, [sample_image], "make it blue", output_path)
        assert result is False

    def test_edit_force_aspect_ratio(self, tmp_path, sample_image):
        from nanobanana import edit_image
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "edited.png"

        with patch("nanobanana.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = edit_image(
                mock_client, [sample_image], "make it blue", output_path,
                aspect_ratio="9:16", force_aspect_ratio=True
            )
            assert result is True

    def test_edit_multiple_images(self, tmp_path):
        from nanobanana import edit_image
        from PIL import Image

        img1 = tmp_path / "img1.png"
        img2 = tmp_path / "img2.png"
        Image.new("RGB", (100, 100), "red").save(img1)
        Image.new("RGB", (200, 200), "blue").save(img2)

        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "merged.png"

        with patch("nanobanana.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image
            result = edit_image(mock_client, [img1, img2], "combine", output_path)
            assert result is True

    def test_edit_invalid_image_exits(self, tmp_path):
        """無効な画像ファイルでsys.exit (lines 117-119)"""
        from nanobanana import edit_image
        mock_client = MagicMock()
        bad_img = tmp_path / "bad.png"
        bad_img.write_text("not an image")
        output_path = tmp_path / "out.png"
        with pytest.raises(SystemExit):
            edit_image(mock_client, [bad_img], "edit", output_path)


# ===========================================================================
# main (lines 163-248)
# ===========================================================================

class TestMain:
    def test_main_generate_with_output(self, tmp_path):
        """テキストから画像生成モード: --output 指定"""
        from nanobanana import main
        output_path = tmp_path / "output.png"
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "cat", "-o", str(output_path)]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.generate_image", return_value=True) as mock_gen:
            main()
            mock_gen.assert_called_once()

    def test_main_generate_default_output(self, tmp_path):
        """テキストから画像生成モード: デフォルト出力パス"""
        from nanobanana import main
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "mountain", "scenery"]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.generate_image", return_value=True) as mock_gen:
            main()
            mock_gen.assert_called_once()

    def test_main_generate_with_session(self, tmp_path):
        """テキストから画像生成モード: --session 指定"""
        from nanobanana import main
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "cat", "--session", "my_project"]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.generate_image", return_value=True) as mock_gen:
            main()
            mock_gen.assert_called_once()

    def test_main_edit_mode(self, tmp_path, sample_image):
        """画像編集モード"""
        from nanobanana import main
        mock_client = MagicMock()
        output_path = tmp_path / "edited.png"

        with patch("sys.argv", ["prog", "make blue", "-i", str(sample_image), "-o", str(output_path)]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.edit_image", return_value=True) as mock_edit:
            main()
            mock_edit.assert_called_once()

    def test_main_edit_default_output(self, tmp_path, sample_image):
        """画像編集モード: デフォルト出力パス"""
        from nanobanana import main
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "enhance", "-i", str(sample_image)]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.edit_image", return_value=True) as mock_edit:
            main()
            mock_edit.assert_called_once()

    def test_main_edit_already_edited_name(self, tmp_path):
        """画像編集モード: _edited 付きファイル名の重複回避"""
        from nanobanana import main
        from PIL import Image
        img = tmp_path / "photo_edited.png"
        Image.new("RGB", (100, 100), "red").save(img)
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "enhance", "-i", str(img)]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.edit_image", return_value=True) as mock_edit:
            main()
            mock_edit.assert_called_once()
            call_args = mock_edit.call_args
            output_path = call_args[0][3]
            assert "_edited_" not in str(output_path) or "photo_edited_" in str(output_path)

    def test_main_edit_nonexistent_input(self, tmp_path):
        """画像編集モード: 存在しない入力ファイルでsys.exit"""
        from nanobanana import main
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "edit", "-i", str(tmp_path / "noexist.png")]), \
             patch("nanobanana.get_client", return_value=mock_client):
            with pytest.raises(SystemExit):
                main()

    def test_main_edit_with_force_ar(self, tmp_path, sample_image):
        """画像編集モード: --force-ar"""
        from nanobanana import main
        mock_client = MagicMock()

        with patch("sys.argv", ["prog", "edit", "-i", str(sample_image), "-far", "-ar", "9:16"]), \
             patch("nanobanana.get_client", return_value=mock_client), \
             patch("nanobanana.edit_image", return_value=True) as mock_edit:
            main()
            call_args = mock_edit.call_args
            assert call_args[0][4] == "9:16"  # aspect_ratio
            assert call_args[0][5] is True  # force_aspect_ratio
