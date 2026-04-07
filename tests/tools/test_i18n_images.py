"""
i18n_images.py のユニットテスト

画像翻訳ツールのテスト:
- scan_images: 画像スキャン
- classify_single_image: 画像分類
- load_manifest: マニフェスト読み込み
- copy_image: 画像コピー
- 定数・バリデーション
- 境界値テスト
"""

import json
import shutil
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    """i18n_images モジュールをロード"""
    return import_module_from_repo("i18n_images", "tools/i18n_images.py")


# ===================================================================
# 定数テスト
# ===================================================================

class TestConstants:

    def test_image_extensions(self, mod):
        assert ".png" in mod.IMAGE_EXTENSIONS
        assert ".jpg" in mod.IMAGE_EXTENSIONS
        assert ".jpeg" in mod.IMAGE_EXTENSIONS
        assert ".gif" in mod.IMAGE_EXTENSIONS
        assert ".webp" in mod.IMAGE_EXTENSIONS
        # SVG は含まれない
        assert ".svg" not in mod.IMAGE_EXTENSIONS

    def test_valid_categories(self, mod):
        expected = {"text-heavy", "annotated", "decorative", "chart"}
        assert mod.VALID_CATEGORIES == expected

    def test_api_delay_positive(self, mod):
        assert mod.API_DELAY > 0


# ===================================================================
# scan_images
# ===================================================================

class TestScanImages:

    def test_empty_directory(self, mod, tmp_path):
        """空のディレクトリ"""
        result = mod.scan_images(tmp_path)
        assert result == []

    def test_finds_png_files(self, mod, tmp_path):
        (tmp_path / "test.png").write_bytes(b"fake png")
        result = mod.scan_images(tmp_path)
        assert "test.png" in result

    def test_finds_jpg_files(self, mod, tmp_path):
        (tmp_path / "test.jpg").write_bytes(b"fake jpg")
        result = mod.scan_images(tmp_path)
        assert "test.jpg" in result

    def test_nested_directories(self, mod, tmp_path):
        """ネストされたディレクトリの再帰スキャン"""
        subdir = tmp_path / "sub" / "deep"
        subdir.mkdir(parents=True)
        (subdir / "nested.png").write_bytes(b"fake")
        result = mod.scan_images(tmp_path)
        assert any("nested.png" in r for r in result)

    def test_ignores_non_image_files(self, mod, tmp_path):
        (tmp_path / "readme.md").write_text("text")
        (tmp_path / "script.py").write_text("code")
        (tmp_path / "data.json").write_text("{}")
        result = mod.scan_images(tmp_path)
        assert result == []

    def test_deduplicates(self, mod, tmp_path):
        """同じファイルが重複しない"""
        (tmp_path / "test.png").write_bytes(b"fake")
        result = mod.scan_images(tmp_path)
        assert len(result) == len(set(result))

    def test_sorted_output(self, mod, tmp_path):
        """結果がソートされている"""
        (tmp_path / "z_image.png").write_bytes(b"fake")
        (tmp_path / "a_image.png").write_bytes(b"fake")
        result = mod.scan_images(tmp_path)
        assert result == sorted(result)

    def test_unicode_filename(self, mod, tmp_path):
        """Unicode ファイル名"""
        (tmp_path / "画像テスト.png").write_bytes(b"fake")
        result = mod.scan_images(tmp_path)
        assert len(result) == 1

    def test_multiple_extensions(self, mod, tmp_path):
        """複数の拡張子"""
        for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            (tmp_path / f"test{ext}").write_bytes(b"fake")
        result = mod.scan_images(tmp_path)
        assert len(result) == 5


# ===================================================================
# classify_single_image
# ===================================================================

class TestClassifySingleImage:

    def test_unopenable_image(self, mod, tmp_path):
        """開けない画像ファイル"""
        bad_img = tmp_path / "bad.png"
        bad_img.write_bytes(b"not an image")
        result = mod.classify_single_image(MagicMock(), bad_img)
        assert result["category"] == "decorative"
        assert result["needs_translation"] is False
        assert "error" in result

    def test_successful_classification(self, mod, tmp_path):
        """正常な分類"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (100, 100), "white").save(img_path)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "text-heavy",
            "texts": ["テキスト1", "テキスト2"],
            "needs_translation": True,
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["category"] == "text-heavy"
        assert result["needs_translation"] is True
        assert len(result["texts"]) == 2

    def test_invalid_category_normalized(self, mod, tmp_path):
        """不正なカテゴリはデフォルト化"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "red").save(img_path)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "invalid_category",
            "texts": [],
            "needs_translation": False,
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["category"] == "decorative"

    def test_json_parse_error(self, mod, tmp_path):
        """JSON パースエラー"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "blue").save(img_path)

        mock_response = MagicMock()
        mock_response.text = "not json {{"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["category"] == "decorative"
        assert "error" in result

    def test_api_exception(self, mod, tmp_path):
        """API 呼び出しで例外"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "green").save(img_path)

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API down")

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["category"] == "decorative"
        assert "error" in result

    def test_texts_not_list_normalized(self, mod, tmp_path):
        """texts がリストでない場合"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "white").save(img_path)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "decorative",
            "texts": "not a list",
            "needs_translation": False,
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["texts"] == []

    def test_needs_translation_not_bool(self, mod, tmp_path):
        """needs_translation がブールでない場合"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "white").save(img_path)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "decorative",
            "texts": [],
            "needs_translation": 1,  # int instead of bool
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["needs_translation"] is True  # bool(1) == True

    def test_response_with_code_fences(self, mod, tmp_path):
        """レスポンスがコードフェンスで囲まれている"""
        try:
            from PIL import Image
        except ImportError:
            pytest.skip("Pillow not installed")

        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "white").save(img_path)

        inner = json.dumps({"category": "chart", "texts": ["label"], "needs_translation": True})
        mock_response = MagicMock()
        mock_response.text = f"```json\n{inner}\n```"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path)

        assert result["category"] == "chart"


# ===================================================================
# load_manifest
# ===================================================================

class TestLoadManifest:

    def test_file_not_found(self, mod, tmp_path):
        """マニフェストファイルが存在しない"""
        with pytest.raises(SystemExit):
            mod.load_manifest(tmp_path / "nonexistent.json")

    def test_valid_manifest(self, mod, tmp_path):
        """正常なマニフェスト読み込み"""
        manifest = {"test.png": {"category": "decorative", "texts": [], "needs_translation": False}}
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
        result = mod.load_manifest(manifest_file)
        assert "test.png" in result


# ===================================================================
# copy_image
# ===================================================================

class TestCopyImage:

    def test_successful_copy(self, mod, tmp_path):
        src = tmp_path / "source.png"
        src.write_bytes(b"image data")
        dst = tmp_path / "output" / "dest.png"
        result = mod.copy_image(src, dst)
        assert result is True
        assert dst.exists()
        assert dst.read_bytes() == b"image data"

    def test_source_not_found(self, mod, tmp_path):
        src = tmp_path / "nonexistent.png"
        dst = tmp_path / "dest.png"
        result = mod.copy_image(src, dst)
        assert result is False

    def test_creates_parent_dirs(self, mod, tmp_path):
        src = tmp_path / "source.png"
        src.write_bytes(b"data")
        dst = tmp_path / "deep" / "nested" / "dest.png"
        result = mod.copy_image(src, dst)
        assert result is True
        assert dst.exists()


# ===================================================================
# classify_images (高レベル)
# ===================================================================

class TestClassifyImages:

    def test_dry_run(self, mod, tmp_path):
        """dry_run=True の場合はファイルを作成しない"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        (images_dir / "test.png").write_bytes(b"fake")

        manifest_path = tmp_path / "manifest.json"
        result = mod.classify_images(
            client=None,
            images_dir=images_dir,
            manifest_path=manifest_path,
            dry_run=True,
        )
        assert result == {}
        assert not manifest_path.exists()

    def test_empty_directory(self, mod, tmp_path):
        """画像なしのディレクトリ"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        manifest_path = tmp_path / "manifest.json"

        result = mod.classify_images(
            client=MagicMock(),
            images_dir=images_dir,
            manifest_path=manifest_path,
        )
        assert result == {}


# ===================================================================
# translate_images (高レベル)
# ===================================================================

class TestTranslateImages:

    def test_dry_run(self, mod, tmp_path):
        """dry_run=True"""
        manifest = {"test.png": {"category": "text-heavy", "texts": ["テスト"], "needs_translation": True}}
        # IMAGES_DIR をモック
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        (images_dir / "test.png").write_bytes(b"fake")

        with patch.object(mod, "IMAGES_DIR", images_dir):
            with patch.object(mod, "DIST_DIR", tmp_path / "dist"):
                result = mod.translate_images(
                    client=None,
                    manifest=manifest,
                    images_dir=images_dir,
                    languages=["en"],
                    dry_run=True,
                )
        # dry_run は API を呼ばない
        assert isinstance(result, dict)

    def test_empty_manifest(self, mod, tmp_path):
        """空のマニフェスト"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest={},
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["total"] == 0

    def test_no_translation_needed_copies(self, mod, tmp_path):
        """翻訳不要な画像はコピーされる"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        (images_dir / "icon.png").write_bytes(b"icon data")

        manifest = {
            "icon.png": {"category": "decorative", "texts": [], "needs_translation": False}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["copied"] == 1

    def test_skip_existing(self, mod, tmp_path):
        """既存ファイルのスキップ"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        (images_dir / "test.png").write_bytes(b"data")

        # 出力先にファイルを事前作成
        dist_dir = tmp_path / "dist"
        output_path = dist_dir / "en" / "assets" / "images" / "test.png"
        output_path.parent.mkdir(parents=True)
        output_path.write_bytes(b"existing")

        manifest = {
            "test.png": {"category": "decorative", "texts": [], "needs_translation": False}
        }

        with patch.object(mod, "DIST_DIR", dist_dir):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
                skip_existing=True,
            )
        assert result["en"]["skipped"] == 1

    def test_source_not_found(self, mod, tmp_path):
        """元画像が見つからない場合"""
        images_dir = tmp_path / "images"
        images_dir.mkdir()

        manifest = {
            "missing.png": {"category": "text-heavy", "texts": ["text"], "needs_translation": True}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["errors"] == 1


# ===================================================================
# classify_single_image: verbose mode (line 77)
# ===================================================================

class TestClassifySingleImageVerbose:
    def test_verbose_output(self, mod, tmp_path, capsys):
        """verbose=True でファイル名を出力 (line 77)"""
        from PIL import Image
        img_path = tmp_path / "verbose_test.png"
        Image.new("RGB", (10, 10), "white").save(img_path)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "decorative",
            "texts": [],
            "needs_translation": False,
        })
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            mod.classify_single_image(mock_client, img_path, verbose=True)

        captured = capsys.readouterr()
        assert "verbose_test.png" in captured.out

    def test_verbose_json_error(self, mod, tmp_path, capsys):
        """verbose=True でJSON解析エラー時にrawレスポンスを出力 (line 152)"""
        from PIL import Image
        img_path = tmp_path / "test.png"
        Image.new("RGB", (10, 10), "blue").save(img_path)

        mock_response = MagicMock()
        mock_response.text = "not json at all"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.classify_single_image(mock_client, img_path, verbose=True)

        captured = capsys.readouterr()
        assert "Raw response" in captured.out
        assert result["category"] == "decorative"


# ===================================================================
# classify_images: full run (lines 198-236)
# ===================================================================

class TestClassifyImagesFull:
    def test_classify_with_images(self, mod, tmp_path):
        """画像ありの分類実行 (lines 198-236)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (10, 10), "white").save(images_dir / "img1.png")
        Image.new("RGB", (10, 10), "red").save(images_dir / "img2.png")

        manifest_path = tmp_path / "manifest.json"

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "category": "text-heavy",
            "texts": ["hello"],
            "needs_translation": True,
        })
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"), \
             patch("time.sleep"):
            result = mod.classify_images(
                client=mock_client,
                images_dir=images_dir,
                manifest_path=manifest_path,
            )

        assert len(result) == 2
        assert manifest_path.exists()

    def test_classify_with_error(self, mod, tmp_path, capsys):
        """分類中にエラーが発生 (lines 207-209)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (10, 10), "white").save(images_dir / "img1.png")

        manifest_path = tmp_path / "manifest.json"

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API down")

        with patch.object(mod, "get_flash_model", return_value="test-model"), \
             patch("time.sleep"):
            result = mod.classify_images(
                client=mock_client,
                images_dir=images_dir,
                manifest_path=manifest_path,
            )

        # Should still return result with error entry
        assert len(result) == 1
        assert result["img1.png"].get("error") is not None


# ===================================================================
# translate_single_image (lines 276-377)
# ===================================================================

class TestTranslateSingleImage:
    def test_translate_success(self, mod, tmp_path):
        """正常な翻訳 (lines 276-360)"""
        from PIL import Image
        source = tmp_path / "source.png"
        Image.new("RGB", (1920, 1080), "white").save(source)
        output = tmp_path / "output" / "translated.png"

        mock_result_image = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()

        mock_types = MagicMock()
        mock_types.Part.as_image.return_value = mock_result_image

        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            # Need to reload types reference
            mod.types = mock_types
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=["テスト"],
                category="text-heavy",
            )
        assert result is True

    def test_translate_unopenable_source(self, mod, tmp_path):
        """開けないソース画像 (lines 280-282)"""
        source = tmp_path / "bad.png"
        source.write_bytes(b"not an image")
        output = tmp_path / "out.png"

        with patch.object(mod, "get_language_name", return_value="English"):
            result = mod.translate_single_image(
                client=MagicMock(),
                source_path=source,
                output_path=output,
                lang="en",
                texts=[],
                category="decorative",
            )
        assert result is False

    def test_translate_chart_category(self, mod, tmp_path):
        """chart カテゴリのプロンプト (line 291-296)"""
        from PIL import Image
        source = tmp_path / "chart.png"
        Image.new("RGB", (800, 600), "white").save(source)
        output = tmp_path / "out.png"

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_types.Part.as_image.return_value = MagicMock()

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mod.types = mock_types
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=["Label"],
                category="chart",
            )
        assert result is True

    def test_translate_annotated_category(self, mod, tmp_path):
        """annotated カテゴリのプロンプト (lines 297-302)"""
        from PIL import Image
        source = tmp_path / "annotated.png"
        Image.new("RGB", (800, 600), "white").save(source)
        output = tmp_path / "out.png"

        mock_types = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_types.Part.as_image.return_value = MagicMock()

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mod.types = mock_types
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=[],
                category="annotated",
            )
        assert result is True

    def test_translate_api_error_with_retry(self, mod, tmp_path):
        """API エラー後にリトライ (lines 369-375)"""
        from PIL import Image
        source = tmp_path / "retry.png"
        Image.new("RGB", (800, 600), "white").save(source)
        output = tmp_path / "out.png"

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch("time.sleep"):
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=[],
                category="text-heavy",
                retry=True,
            )
        assert result is False
        # Should have tried twice
        assert mock_client.models.generate_content.call_count == 2

    def test_translate_no_retry(self, mod, tmp_path):
        """リトライなし (retry=False)"""
        from PIL import Image
        source = tmp_path / "noretry.png"
        Image.new("RGB", (800, 600), "white").save(source)
        output = tmp_path / "out.png"

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch("time.sleep"):
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=[],
                category="text-heavy",
                retry=False,
            )
        assert result is False
        assert mock_client.models.generate_content.call_count == 1

    def test_translate_no_image_in_response(self, mod, tmp_path):
        """レスポンスに画像がない (lines 362-367)"""
        from PIL import Image
        source = tmp_path / "noimgresponse.png"
        Image.new("RGB", (800, 600), "white").save(source)
        output = tmp_path / "out.png"

        mock_types = MagicMock()
        # Empty candidates with no inline_data
        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_candidate = MagicMock()
        mock_candidate.content.parts = [mock_part]
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_image_model", return_value="test-model"), \
             patch.object(mod, "get_language_name", return_value="English"), \
             patch("time.sleep"), \
             patch.dict("sys.modules", {"google.genai.types": mock_types}):
            mod.types = mock_types
            result = mod.translate_single_image(
                client=mock_client,
                source_path=source,
                output_path=output,
                lang="en",
                texts=[],
                category="text-heavy",
                retry=True,
            )
        assert result is False

    def test_translate_various_aspect_ratios(self, mod, tmp_path):
        """各種アスペクト比テスト (lines 323-334)"""
        from PIL import Image

        test_cases = [
            ((2100, 900), "21:9"),   # > 1.9
            ((1600, 900), "16:9"),   # > 1.5
            ((400, 300), "4:3"),     # > 1.2
            ((100, 100), "1:1"),     # > 0.9
            ((300, 400), "3:4"),     # > 0.7
            ((100, 200), "9:16"),    # <= 0.7
        ]

        for size, expected_ar in test_cases:
            source = tmp_path / f"ar_{size[0]}x{size[1]}.png"
            Image.new("RGB", size, "white").save(source)
            output = tmp_path / f"out_{size[0]}x{size[1]}.png"

            mock_types = MagicMock()
            mock_part = MagicMock()
            mock_part.inline_data = MagicMock()
            mock_candidate = MagicMock()
            mock_candidate.content.parts = [mock_part]
            mock_response = MagicMock()
            mock_response.candidates = [mock_candidate]
            mock_types.Part.as_image.return_value = MagicMock()

            mock_client = MagicMock()
            mock_client.models.generate_content.return_value = mock_response

            with patch.object(mod, "get_image_model", return_value="test-model"), \
                 patch.object(mod, "get_language_name", return_value="English"), \
                 patch.dict("sys.modules", {"google.genai.types": mock_types}):
                mod.types = mock_types
                result = mod.translate_single_image(
                    client=mock_client,
                    source_path=source,
                    output_path=output,
                    lang="en",
                    texts=[],
                    category="text-heavy",
                    retry=False,
                )
            assert result is True


# ===================================================================
# translate_images: translation success & failure (lines 460-485)
# ===================================================================

class TestTranslateImagesTranslation:
    def test_translate_success(self, mod, tmp_path):
        """翻訳成功パス (lines 460-471)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (100, 100), "white").save(images_dir / "text.png")

        manifest = {
            "text.png": {"category": "text-heavy", "texts": ["hello"], "needs_translation": True}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"), \
             patch.object(mod, "translate_single_image", return_value=True), \
             patch("time.sleep"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["translated"] == 1

    def test_translate_failure(self, mod, tmp_path):
        """翻訳失敗パス (lines 472-474)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (100, 100), "white").save(images_dir / "text.png")

        manifest = {
            "text.png": {"category": "text-heavy", "texts": ["hello"], "needs_translation": True}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"), \
             patch.object(mod, "translate_single_image", return_value=False), \
             patch("time.sleep"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["errors"] == 1

    def test_copy_failure(self, mod, tmp_path):
        """コピー失敗パス (lines 483-485)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (100, 100), "white").save(images_dir / "icon.png")

        manifest = {
            "icon.png": {"category": "decorative", "texts": [], "needs_translation": False}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"), \
             patch.object(mod, "copy_image", return_value=False):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
            )
        assert result["en"]["errors"] == 1

    def test_skip_existing_verbose(self, mod, tmp_path, capsys):
        """既存スキップ + verbose (lines 441-444)"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (100, 100), "white").save(images_dir / "test.png")

        dist_dir = tmp_path / "dist"
        output_path = dist_dir / "en" / "assets" / "images" / "test.png"
        output_path.parent.mkdir(parents=True)
        output_path.write_bytes(b"existing")

        manifest = {
            "test.png": {"category": "decorative", "texts": [], "needs_translation": False}
        }

        with patch.object(mod, "DIST_DIR", dist_dir):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en"],
                skip_existing=True,
                verbose=True,
            )
        assert result["en"]["skipped"] == 1
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_translate_multiple_languages(self, mod, tmp_path):
        """複数言語の翻訳"""
        from PIL import Image
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        Image.new("RGB", (100, 100), "white").save(images_dir / "test.png")

        manifest = {
            "test.png": {"category": "decorative", "texts": [], "needs_translation": False}
        }

        with patch.object(mod, "DIST_DIR", tmp_path / "dist"):
            result = mod.translate_images(
                client=MagicMock(),
                manifest=manifest,
                images_dir=images_dir,
                languages=["en", "es"],
            )
        assert "en" in result
        assert "es" in result
