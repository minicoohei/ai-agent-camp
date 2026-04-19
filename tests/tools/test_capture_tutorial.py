"""
capture_tutorial.py のユニットテスト

スクリーンショットから操作チュートリアルを生成する機能のテスト:
- 画面解析 (analyze_screen_for_tutorial)
- HTML 構築 (build_tutorial_html)
- 注釈画像生成 (add_step_annotations)
- 境界値テスト
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    """capture_tutorial モジュールをロード"""
    return import_module_from_repo("capture_tutorial", "tools/capture_tutorial.py")


# ===================================================================
# analyze_screen_for_tutorial
# ===================================================================

class TestAnalyzeScreenForTutorial:

    def test_no_client_returns_fallback(self, mod, tmp_path):
        """client=None の場合はフォールバック結果"""
        img = tmp_path / "test.png"
        img.write_bytes(b"fake")
        result = mod.analyze_screen_for_tutorial(None, img)
        assert result["title"] == "APIキー未設定"
        assert result["steps"] == []

    def test_successful_analysis(self, mod, tmp_path):
        """正常な解析結果"""
        img = tmp_path / "test.png"
        # 最小限の PNG (1x1 pixel)
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "テスト画面",
            "description": "テスト用の画面",
            "steps": [{"step": 1, "action": "ボタンをクリック", "detail": "", "location": "右上"}],
            "tips": ["ヒント1"]
        })

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_screen_for_tutorial(mock_client, img)

        assert result["title"] == "テスト画面"
        assert len(result["steps"]) == 1

    def test_json_in_code_block(self, mod, tmp_path):
        """レスポンスが ```json ... ``` で囲まれている場合"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        inner = json.dumps({"title": "テスト", "description": "", "steps": [], "tips": []})
        mock_response = MagicMock()
        mock_response.text = f"```json\n{inner}\n```"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_screen_for_tutorial(mock_client, img)

        assert result["title"] == "テスト"

    def test_json_parse_error(self, mod, tmp_path):
        """JSON パースエラーのフォールバック"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        mock_response = MagicMock()
        mock_response.text = "not valid json {{"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_screen_for_tutorial(mock_client, img)

        assert result["title"] == "解析エラー"
        assert result["steps"] == []

    def test_api_exception(self, mod, tmp_path):
        """API 呼び出しで例外が発生"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API error")

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_screen_for_tutorial(mock_client, img)

        assert "エラー" in result["title"]


# ===================================================================
# build_tutorial_html
# ===================================================================

class TestBuildTutorialHtml:

    def test_basic_output(self, mod, tmp_path):
        """基本的な HTML 出力"""
        result = {
            "title": "テスト画面",
            "description": "テスト説明",
            "steps": [
                {"step": 1, "action": "クリック", "detail": "詳細", "location": "右上"}
            ],
            "tips": ["ヒント1"]
        }
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "テスト画面" in html
        assert "クリック" in html
        assert "ヒント1" in html

    def test_empty_steps(self, mod, tmp_path):
        """ステップなしの場合"""
        result = {"title": "テスト", "description": "説明", "steps": [], "tips": []}
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "テスト" in html
        assert "操作手順" not in html  # ステップセクションは生成されない

    def test_empty_tips(self, mod, tmp_path):
        """ヒントなしの場合"""
        result = {"title": "テスト", "description": "説明", "steps": [], "tips": []}
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "ヒント" not in html

    def test_with_annotated_paths(self, mod, tmp_path):
        """注釈画像パス付き"""
        result = {
            "title": "テスト",
            "description": "",
            "steps": [{"step": 1, "action": "クリック"}],
            "tips": []
        }
        annotated = [str(tmp_path / "annotated.png")]
        html = mod.build_tutorial_html(
            tmp_path / "img.png", result,
            output_path=tmp_path / "out.html",
            annotated_paths=annotated,
        )
        assert "annotated.png" in html

    def test_missing_title(self, mod, tmp_path):
        """title がない場合のデフォルト"""
        result = {"description": "説明", "steps": [], "tips": []}
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "チュートリアル" in html

    def test_none_detail_and_location(self, mod, tmp_path):
        """detail/location が None の場合"""
        result = {
            "title": "テスト",
            "description": "",
            "steps": [{"step": 1, "action": "アクション", "detail": None, "location": None}],
            "tips": []
        }
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "アクション" in html

    def test_unicode_content(self, mod, tmp_path):
        """Unicode 文字を含むコンテンツ"""
        result = {
            "title": "日本語テスト 🎯",
            "description": "特殊文字: <>&\"'",
            "steps": [{"step": 1, "action": "操作①②③"}],
            "tips": ["ヒント: こんにちは"]
        }
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "操作①②③" in html

    def test_many_steps(self, mod, tmp_path):
        """境界値: 大量のステップ"""
        steps = [{"step": i, "action": f"ステップ{i}"} for i in range(1, 101)]
        result = {"title": "多ステップ", "description": "", "steps": steps, "tips": []}
        html = mod.build_tutorial_html(tmp_path / "img.png", result)
        assert "ステップ100" in html


# ===================================================================
# add_step_annotations
# ===================================================================

class TestAddStepAnnotations:

    def test_empty_steps(self, mod, tmp_path):
        """ステップなしの場合"""
        results = mod.add_step_annotations(tmp_path / "img.png", [], tmp_path)
        assert results == []

    def test_subprocess_failure(self, mod, tmp_path):
        """サブプロセスが失敗した場合"""
        steps = [{"step": 1, "action": "クリック", "location": "右上"}]
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="error")
            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
            assert len(results) == 1
            assert results[0] is None

    def test_subprocess_exception(self, mod, tmp_path):
        """サブプロセスで例外"""
        steps = [{"step": 1, "action": "アクション"}]
        with patch("subprocess.run", side_effect=OSError("exec error")):
            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
            assert len(results) == 1
            assert results[0] is None

    def test_step_without_location(self, mod, tmp_path):
        """location が空の場合"""
        steps = [{"step": 1, "action": "クリック", "location": ""}]
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="")
            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
            assert len(results) == 1


# ===================================================================
# DEFAULT_TUTORIAL_DIR
# ===================================================================

class TestAddStepAnnotationsExtended:
    """add_step_annotations の拡張テスト (lines 86-87)"""

    def test_successful_annotation(self, mod, tmp_path):
        """サブプロセスが成功した場合"""
        steps = [{"step": 1, "action": "クリック", "location": "右上"}]
        output_file = tmp_path / f"{tmp_path.name}_step1_annotated.png"
        # Create the expected output file
        output_file.write_bytes(b"annotated_image")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            # We need to create the file before the check
            expected_name = f"{(tmp_path / 'img.png').stem}_step1_annotated.png"
            expected_path = tmp_path / expected_name
            expected_path.write_bytes(b"annotated_image")

            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
        assert len(results) == 1
        assert results[0] is not None

    def test_multiple_steps(self, mod, tmp_path):
        """複数ステップ"""
        steps = [
            {"step": 1, "action": "クリック", "location": "左上"},
            {"step": 2, "action": "入力"},
            {"step": 3, "action": "送信", "location": "右下"},
        ]
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="fail")
            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
        assert len(results) == 3

    def test_step_without_step_key(self, mod, tmp_path):
        """step キーがない場合はインデックス+1が使われる"""
        steps = [{"action": "テスト"}]
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="")
            results = mod.add_step_annotations(tmp_path / "img.png", steps, tmp_path)
        assert len(results) == 1


class TestBuildTutorialHtmlExtended:
    """build_tutorial_html の追加テスト (lines 210, 217-218)"""

    def test_output_path_relative_calculation(self, mod, tmp_path):
        """output_path が指定された場合の相対パス計算"""
        img = tmp_path / "subdir" / "img.png"
        img.parent.mkdir(parents=True, exist_ok=True)
        img.write_bytes(b"fake")

        result = {
            "title": "テスト",
            "description": "",
            "steps": [],
            "tips": [],
        }
        output = tmp_path / "out" / "tutorial.html"
        html = mod.build_tutorial_html(img, result, output_path=output)
        assert "img.png" in html

    def test_annotated_path_none_in_list(self, mod, tmp_path):
        """annotated_paths に None が含まれる場合"""
        result = {
            "title": "テスト",
            "description": "",
            "steps": [
                {"step": 1, "action": "A"},
                {"step": 2, "action": "B"},
            ],
            "tips": [],
        }
        annotated = [None, str(tmp_path / "ann.png")]
        html = mod.build_tutorial_html(
            tmp_path / "img.png", result,
            output_path=tmp_path / "out.html",
            annotated_paths=annotated,
        )
        assert "ann.png" in html

    def test_annotated_paths_shorter_than_steps(self, mod, tmp_path):
        """annotated_paths がステップ数より少ない場合"""
        result = {
            "title": "テスト",
            "description": "",
            "steps": [
                {"step": 1, "action": "A"},
                {"step": 2, "action": "B"},
                {"step": 3, "action": "C"},
            ],
            "tips": [],
        }
        annotated = [str(tmp_path / "ann1.png")]
        html = mod.build_tutorial_html(
            tmp_path / "img.png", result,
            output_path=tmp_path / "out.html",
            annotated_paths=annotated,
        )
        assert "ann1.png" in html


class TestMainFunctionCaptureTutorial:
    """main() 関数のテスト (lines 267-333)"""

    def test_main_file_not_found(self, mod, tmp_path):
        """画像ファイルが見つからない場合"""
        with patch("sys.argv", ["cmd", str(tmp_path / "nonexistent.png")]):
            with pytest.raises(SystemExit) as exc_info:
                mod.main()
            assert exc_info.value.code == 1

    def test_main_no_client(self, mod, tmp_path):
        """Gemini API クライアントがない場合"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        with patch("sys.argv", ["cmd", str(img)]):
            with patch.object(mod, "get_client", return_value=None):
                with pytest.raises(SystemExit) as exc_info:
                    mod.main()
            assert exc_info.value.code == 1

    def test_main_successful(self, mod, tmp_path):
        """正常な実行"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        output = tmp_path / "output" / "tutorial.html"

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "Test",
            "description": "Desc",
            "steps": [{"step": 1, "action": "Click", "detail": "", "location": "top"}],
            "tips": ["Tip 1"],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["cmd", str(img), "--output", str(output), "--no-annotate"]):
            with patch.object(mod, "get_client", return_value=mock_client):
                with patch.object(mod, "get_flash_model", return_value="test-model"):
                    with patch.object(mod, "create_html_template", return_value="<html></html>"):
                        with patch.object(mod, "save_html_file"):
                            mod.main()

    def test_main_with_annotation(self, mod, tmp_path):
        """注釈付きの実行"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        output = tmp_path / "output" / "tutorial.html"

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "Test",
            "description": "Desc",
            "steps": [{"step": 1, "action": "Click"}],
            "tips": [],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["cmd", str(img), "--output", str(output)]):
            with patch.object(mod, "get_client", return_value=mock_client):
                with patch.object(mod, "get_flash_model", return_value="test-model"):
                    with patch.object(mod, "add_step_annotations", return_value=[None]):
                        with patch.object(mod, "create_html_template", return_value="<html></html>"):
                            with patch.object(mod, "save_html_file"):
                                mod.main()

    def test_main_auto_output_path(self, mod, tmp_path):
        """output 未指定の場合は自動生成"""
        img = tmp_path / "test.png"
        try:
            from PIL import Image
            im = Image.new("RGB", (10, 10), "white")
            im.save(img)
        except ImportError:
            img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "Test",
            "description": "Desc",
            "steps": [],
            "tips": [],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", ["cmd", str(img), "--no-annotate"]):
            with patch.object(mod, "get_client", return_value=mock_client):
                with patch.object(mod, "get_flash_model", return_value="test-model"):
                    with patch.object(mod, "create_html_template", return_value="<html></html>"):
                        with patch.object(mod, "save_html_file"):
                            mod.main()


class TestConstants:

    def test_default_tutorial_dir_is_path(self, mod):
        assert isinstance(mod.DEFAULT_TUTORIAL_DIR, Path)
