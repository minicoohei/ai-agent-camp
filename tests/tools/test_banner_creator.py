"""banner_creator.py の単体テスト"""
import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import banner_creator
        assert hasattr(banner_creator, 'main')

    def test_import_constants(self):
        from banner_creator import PLATFORM_PRESETS, TONE_PROMPTS, COLOR_SCHEME_PROMPTS
        assert len(PLATFORM_PRESETS) > 0
        assert len(TONE_PROMPTS) > 0
        assert len(COLOR_SCHEME_PROMPTS) > 0


class TestSanitizeFilename:
    def test_spaces_replaced(self):
        from banner_creator import sanitize_filename
        assert sanitize_filename("hello world") == "hello_world"

    def test_special_chars_removed(self):
        from banner_creator import sanitize_filename
        assert sanitize_filename('file<>:name') == "filename"

    def test_truncation(self):
        from banner_creator import sanitize_filename
        long_name = "a" * 100
        assert len(sanitize_filename(long_name)) == 50

    def test_empty_string(self):
        from banner_creator import sanitize_filename
        assert sanitize_filename("") == ""

    def test_only_special_chars(self):
        from banner_creator import sanitize_filename
        assert sanitize_filename('<>:"/\\|?*') == ""

    def test_mixed_special_and_spaces(self):
        from banner_creator import sanitize_filename
        result = sanitize_filename('my <banner> file: v2')
        assert result == "my_banner_file_v2"


class TestBuildBannerPrompt:
    def test_basic_prompt(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
        )
        assert "テスト" in prompt
        assert "1200x675" in prompt
        assert "16:9" in prompt

    def test_with_options(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="instagram_feed",
            tone="casual",
            sub_copy="サブコピー",
            cta="今すぐ登録",
            brand_name="TestBrand",
        )
        assert "サブコピー" in prompt
        assert "今すぐ登録" in prompt
        assert "TestBrand" in prompt
        assert "1080x1080" in prompt

    def test_hex_color_scheme(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
            color_scheme="#FF5733",
        )
        assert "#FF5733" in prompt

    def test_unknown_platform_falls_back(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="unknown_platform",
        )
        # Falls back to x_post preset
        assert "1200x675" in prompt

    def test_unknown_tone_falls_back(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
            tone="unknown_tone",
        )
        # Falls back to professional
        assert "プロフェッショナル" in prompt

    def test_unknown_priority_falls_back(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
            priority="unknown_priority",
        )
        # Falls back to ctr
        assert "クリック率" in prompt

    def test_no_sub_copy_or_cta(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
        )
        assert "Sub-headline" not in prompt
        assert "Call-to-action" not in prompt
        assert "Brand name" not in prompt

    def test_all_platforms(self):
        from banner_creator import build_banner_prompt, PLATFORM_PRESETS
        for platform in PLATFORM_PRESETS:
            prompt = build_banner_prompt(message="test", platform=platform)
            preset = PLATFORM_PRESETS[platform]
            assert f"{preset['width']}x{preset['height']}" in prompt

    def test_named_color_scheme(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
            color_scheme="warm",
        )
        assert "暖色" in prompt

    def test_unknown_color_scheme_falls_back(self):
        from banner_creator import build_banner_prompt
        prompt = build_banner_prompt(
            message="テスト",
            platform="x_post",
            color_scheme="nonexistent",
        )
        # Falls back to "auto"
        assert "自動選択" in prompt


class TestPlatformPresets:
    def test_all_presets_have_required_keys(self):
        from banner_creator import PLATFORM_PRESETS
        required_keys = {"name", "width", "height", "aspect_ratio", "description"}
        for platform, preset in PLATFORM_PRESETS.items():
            assert required_keys.issubset(preset.keys()), f"{platform} missing keys"

    def test_aspect_ratios_valid(self):
        from banner_creator import PLATFORM_PRESETS
        valid_ratios = {"16:9", "9:16", "1:1", "4:3", "3:4"}
        for platform, preset in PLATFORM_PRESETS.items():
            assert preset["aspect_ratio"] in valid_ratios, f"{platform} has invalid ratio"

    def test_dimensions_positive(self):
        from banner_creator import PLATFORM_PRESETS
        for platform, preset in PLATFORM_PRESETS.items():
            assert preset["width"] > 0
            assert preset["height"] > 0


class TestSaveCopyText:
    def test_save_creates_file(self, tmp_path):
        from banner_creator import save_copy_text
        copy_data = {
            "post_texts": ["投稿文1", "投稿文2"],
            "hashtags": ["#テスト", "#AI"],
            "cta_phrases": ["今すぐ登録"],
        }
        output_path = tmp_path / "banner.png"
        result = save_copy_text(copy_data, output_path)
        assert result.exists()
        content = result.read_text(encoding="utf-8")
        assert "投稿文1" in content
        assert "#テスト" in content

    def test_save_empty_data(self, tmp_path):
        from banner_creator import save_copy_text
        copy_data = {"post_texts": [], "hashtags": [], "cta_phrases": []}
        output_path = tmp_path / "banner.png"
        result = save_copy_text(copy_data, output_path)
        assert result.exists()

    def test_save_with_cta_phrases(self, tmp_path):
        from banner_creator import save_copy_text
        copy_data = {
            "post_texts": ["テスト投稿"],
            "hashtags": [],
            "cta_phrases": ["CTA1", "CTA2"],
        }
        output_path = tmp_path / "banner.png"
        result = save_copy_text(copy_data, output_path)
        content = result.read_text(encoding="utf-8")
        assert "CTA1" in content
        assert "CTA2" in content


class TestGenerateCopyText:
    def test_api_error_returns_fallback(self):
        from banner_creator import generate_copy_text
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")
        result = generate_copy_text(mock_client, "テスト", "x_post")
        assert "post_texts" in result
        assert result["post_texts"] == ["テスト"]

    def test_successful_json_response(self):
        from banner_creator import generate_copy_text
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "post_texts": ["投稿文案1"],
            "hashtags": ["#テスト"],
            "cta_phrases": ["今すぐ"]
        })
        mock_client.models.generate_content.return_value = mock_response

        result = generate_copy_text(mock_client, "テスト", "x_post")
        assert result["post_texts"] == ["投稿文案1"]
        assert result["hashtags"] == ["#テスト"]

    def test_non_json_response_returns_fallback(self):
        from banner_creator import generate_copy_text
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is not JSON at all"
        mock_client.models.generate_content.return_value = mock_response

        result = generate_copy_text(mock_client, "テスト", "x_post", sub_copy="サブ", cta="CTA")
        assert "post_texts" in result

    def test_with_all_options(self):
        from banner_creator import generate_copy_text
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "post_texts": ["完全な投稿"],
            "hashtags": ["#完全"],
            "cta_phrases": ["今すぐ"]
        })
        mock_client.models.generate_content.return_value = mock_response

        result = generate_copy_text(
            mock_client, "テスト", "instagram_feed",
            tone="pop", sub_copy="サブコピー", cta="登録",
            brand_name="MyBrand"
        )
        assert result["post_texts"] == ["完全な投稿"]


class TestDownloadReferenceImage:
    @patch("banner_creator.requests.get")
    def test_successful_download(self, mock_get, tmp_path):
        from banner_creator import download_reference_image
        mock_response = MagicMock()
        mock_response.content = b"fake image data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = download_reference_image("http://example.com/image.jpg", tmp_path)
        assert result is not None
        assert result.exists()

    @patch("banner_creator.requests.get")
    def test_png_extension(self, mock_get, tmp_path):
        from banner_creator import download_reference_image
        mock_response = MagicMock()
        mock_response.content = b"fake png data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = download_reference_image("http://example.com/image.png", tmp_path)
        assert result is not None
        assert result.suffix == ".png"

    @patch("banner_creator.requests.get")
    def test_gif_extension(self, mock_get, tmp_path):
        from banner_creator import download_reference_image
        mock_response = MagicMock()
        mock_response.content = b"fake gif data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = download_reference_image("http://example.com/anim.gif", tmp_path)
        assert result is not None
        assert result.suffix == ".gif"

    @patch("banner_creator.requests.get")
    def test_network_error_returns_none(self, mock_get, tmp_path):
        from banner_creator import download_reference_image
        mock_get.side_effect = Exception("Connection refused")

        result = download_reference_image("http://example.com/image.jpg", tmp_path)
        assert result is None


class TestGenerateBanner:
    def test_successful_generation(self, tmp_path):
        from banner_creator import generate_banner
        mock_client = MagicMock()

        # Build a proper mock response with inline_data
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_image = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "test_banner.png"

        with patch("banner_creator.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image

            result = generate_banner(mock_client, "test prompt", output_path)
            assert result is True
            mock_result_image.save.assert_called_once_with(output_path)

    def test_no_image_in_response(self, tmp_path):
        from banner_creator import generate_banner
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "test_banner.png"
        result = generate_banner(mock_client, "test prompt", output_path)
        assert result is False

    def test_api_error(self, tmp_path):
        from banner_creator import generate_banner
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        output_path = tmp_path / "test_banner.png"
        result = generate_banner(mock_client, "test prompt", output_path)
        assert result is False

    def test_with_reference_image(self, tmp_path, sample_image):
        from banner_creator import generate_banner
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "test_banner.png"

        with patch("banner_creator.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image

            result = generate_banner(
                mock_client, "test prompt", output_path,
                reference_image=sample_image
            )
            assert result is True

    def test_with_nonexistent_reference(self, tmp_path):
        from banner_creator import generate_banner
        mock_client = MagicMock()

        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_client.models.generate_content.return_value = mock_response

        output_path = tmp_path / "test_banner.png"

        with patch("banner_creator.types.Part.as_image") as mock_as_image:
            mock_result_image = MagicMock()
            mock_as_image.return_value = mock_result_image

            # Nonexistent reference should be ignored
            result = generate_banner(
                mock_client, "test prompt", output_path,
                reference_image=Path("/nonexistent/ref.png")
            )
            assert result is True


# ========== main() CLI tests (lines 436-626) ==========


class TestMainCLI:
    def _make_mock_client(self, success=True):
        """テスト用の mock client を作成"""
        mock_client = MagicMock()
        if success:
            mock_part = MagicMock()
            mock_part.inline_data = True
            mock_candidate = MagicMock()
            mock_candidate.content.parts = [mock_part]
            mock_response = MagicMock()
            mock_response.candidates = [mock_candidate]
            mock_client.models.generate_content.return_value = mock_response
        else:
            mock_client.models.generate_content.side_effect = Exception("API Error")
        return mock_client

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_basic(self, mock_get_client, mock_as_image, tmp_path):
        """基本的な main 実行 (lines 436-626)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        output = tmp_path / "output.png"
        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テストバナー",
            "--output", str(output),
        ]):
            main()

    @patch("banner_creator.get_client", return_value=None)
    def test_main_no_client_exits(self, mock_get_client):
        """client なしで sys.exit(1) (lines 521-523)"""
        from banner_creator import main
        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
        ]), pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_session(self, mock_get_client, mock_as_image, tmp_path):
        """session オプション付き (lines 535-537)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--session", "my test session",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_default_output_dir(self, mock_get_client, mock_as_image, tmp_path):
        """output 未指定時のデフォルトパス (lines 534-542)"""
        from banner_creator import main, DEFAULT_OUTPUT_DIR
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "instagram_feed",
            "--message", "テスト",
        ]), patch.object(Path, "mkdir"):
            main()

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_reference_url(self, mock_get_client, mock_as_image, tmp_path):
        """参考画像 URL (lines 548-550)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--reference", "http://example.com/img.png",
            "--output", str(tmp_path / "out.png"),
        ]), patch("banner_creator.download_reference_image", return_value=None):
            main()

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_reference_file(self, mock_get_client, mock_as_image, tmp_path, sample_image):
        """参考画像ファイルパス (lines 551-554)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--reference", str(sample_image),
            "--output", str(tmp_path / "out.png"),
        ]):
            main()

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_nonexistent_reference_file(self, mock_get_client, mock_as_image, tmp_path, capsys):
        """存在しない参考画像ファイル (lines 555-556)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--reference", "/nonexistent/ref.png",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()
        output = capsys.readouterr().out
        assert "Warning" in output or "not found" in output or "✨" in output

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_variants(self, mock_get_client, mock_as_image, tmp_path):
        """複数バリアント生成 (lines 559-590)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--variants", "2",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()

    @patch("banner_creator.get_client")
    def test_main_variant_failure(self, mock_get_client, tmp_path, capsys):
        """バリアント生成失敗 (lines 589-590)"""
        from banner_creator import main
        mock_client = self._make_mock_client(success=False)
        mock_get_client.return_value = mock_client

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--variants", "2",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()
        output = capsys.readouterr().out
        assert "Failed" in output or "Error" in output

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_copy(self, mock_get_client, mock_as_image, tmp_path):
        """--with-copy オプション (lines 593-624)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        # Mock generate_copy_text response
        copy_resp = MagicMock()
        copy_resp.text = json.dumps({
            "post_texts": ["テスト投稿"],
            "hashtags": ["#テスト"],
            "cta_phrases": ["今すぐ"],
        })
        # Make the second call return copy text
        call_count = [0]
        original_gen = mock_client.models.generate_content

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return original_gen(*args, **kwargs)
            return copy_resp

        mock_client.models.generate_content.side_effect = side_effect

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "x_post",
            "--message", "テスト",
            "--with-copy",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()

    @patch("banner_creator.types.Part.as_image")
    @patch("banner_creator.get_client")
    def test_main_with_all_options(self, mock_get_client, mock_as_image, tmp_path):
        """全オプション指定 (lines 566-576)"""
        from banner_creator import main
        mock_client = self._make_mock_client()
        mock_get_client.return_value = mock_client
        mock_as_image.return_value = MagicMock()

        with patch("sys.argv", [
            "banner_creator.py",
            "--platform", "youtube",
            "--message", "テストメッセージ",
            "--sub-copy", "サブコピー",
            "--cta", "今すぐ登録",
            "--tone", "pop",
            "--color-scheme", "#FF5733",
            "--font-style", "bold",
            "--priority", "brand",
            "--brand-name", "TestBrand",
            "--output", str(tmp_path / "out.png"),
        ]):
            main()
