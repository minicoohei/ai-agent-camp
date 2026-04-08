"""screenshot_analyzer.py の単体テスト"""
import json
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path


class TestImport:
    def test_import_module(self):
        import screenshot_analyzer
        assert hasattr(screenshot_analyzer, 'main')
        assert hasattr(screenshot_analyzer, 'analyze_screenshot')
        assert hasattr(screenshot_analyzer, 'analyze_for_tutorial')

    def test_import_helpers(self):
        from screenshot_analyzer import (
            get_rel_path, add_annotations, generate_next_steps,
            build_analyze_html, build_tutorial_html
        )
        assert callable(get_rel_path)
        assert callable(add_annotations)
        assert callable(generate_next_steps)
        assert callable(build_analyze_html)
        assert callable(build_tutorial_html)


class TestGetRelPath:
    def test_basic(self, tmp_path):
        from screenshot_analyzer import get_rel_path
        target = str(tmp_path / "images" / "test.png")
        output = tmp_path / "output" / "report.html"
        result = get_rel_path(target, output)
        assert result  # Should return a non-empty string

    def test_empty_string(self):
        from screenshot_analyzer import get_rel_path
        assert get_rel_path("") == ""

    def test_none_output(self, tmp_path):
        from screenshot_analyzer import get_rel_path
        target = str(tmp_path / "test.png")
        result = get_rel_path(target, None)
        assert result  # non-empty string

    def test_same_directory(self, tmp_path):
        from screenshot_analyzer import get_rel_path
        target = str(tmp_path / "test.png")
        output = tmp_path / "report.html"
        result = get_rel_path(target, output)
        assert result == "test.png"


class TestAnalyzeScreenshot:
    def test_no_client_returns_default(self, sample_image):
        from screenshot_analyzer import analyze_screenshot
        result = analyze_screenshot(None, sample_image)
        assert "description" in result
        assert result["has_error"] is False

    def test_invalid_image_returns_error(self, tmp_path):
        from screenshot_analyzer import analyze_screenshot
        fake_image = tmp_path / "nonexistent.png"
        result = analyze_screenshot(MagicMock(), fake_image)
        assert "description" in result

    def test_successful_json_response(self, sample_image):
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "description": "ターミナル画面",
            "has_error": True,
            "error_details": {
                "error_message": "ModuleNotFoundError",
                "error_type": "ImportError",
                "possible_causes": ["モジュール未インストール"]
            },
            "suggestions": ["pip installを実行"]
        })
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_screenshot(mock_client, sample_image)
        assert result["has_error"] is True
        assert result["description"] == "ターミナル画面"

    def test_non_json_response(self, sample_image):
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is just plain text about an error"
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_screenshot(mock_client, sample_image)
        assert "description" in result
        # "error" is in the text, so has_error should be True
        assert result["has_error"] is True

    def test_api_error(self, sample_image):
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        result = analyze_screenshot(mock_client, sample_image)
        assert "description" in result
        assert result["has_error"] is False

    def test_plain_json_response(self, sample_image):
        """Test that a clean JSON response is parsed correctly"""
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"description": "正常画面", "has_error": false, "error_details": null, "suggestions": ["次へ進む"]}'
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_screenshot(mock_client, sample_image)
        assert result["description"] == "正常画面"
        assert result["has_error"] is False
        assert "次へ進む" in result["suggestions"]


class TestGenerateNextSteps:
    def test_no_client_returns_default(self):
        from screenshot_analyzer import generate_next_steps
        analysis = {"description": "test", "has_error": False, "suggestions": ["do A", "do B"]}
        result = generate_next_steps(None, analysis)
        assert "summary" in result
        assert "steps" in result

    def test_empty_suggestions(self):
        from screenshot_analyzer import generate_next_steps
        analysis = {"description": "test", "has_error": False, "suggestions": []}
        result = generate_next_steps(None, analysis)
        assert len(result["steps"]) >= 1

    def test_successful_json_response(self):
        from screenshot_analyzer import generate_next_steps
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "summary": "以下の手順を実行",
            "steps": [
                {"step": "1", "action": "パッケージをインストール", "explanation": "依存関係解決"}
            ],
            "expected_result": "正常に動作する"
        })
        mock_client.models.generate_content.return_value = mock_response

        analysis = {"description": "error", "has_error": True, "suggestions": []}
        result = generate_next_steps(mock_client, analysis)
        assert result["summary"] == "以下の手順を実行"
        assert len(result["steps"]) == 1

    def test_non_json_response(self):
        from screenshot_analyzer import generate_next_steps
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Not a valid JSON response"
        mock_client.models.generate_content.return_value = mock_response

        analysis = {"description": "test", "has_error": False, "suggestions": ["fix it"]}
        result = generate_next_steps(mock_client, analysis)
        assert "summary" in result

    def test_api_error(self):
        from screenshot_analyzer import generate_next_steps
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API Error")

        analysis = {"description": "test", "has_error": True, "suggestions": []}
        result = generate_next_steps(mock_client, analysis)
        assert "summary" in result
        assert "steps" in result


class TestAddAnnotations:
    @patch("screenshot_analyzer.subprocess.run")
    def test_successful_annotation(self, mock_run, tmp_path, sample_image):
        from screenshot_analyzer import add_annotations
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create the expected output file
        expected_output = output_dir / f"{sample_image.stem}_annotated.png"
        expected_output.write_bytes(b"fake image")

        mock_run.return_value = MagicMock(returncode=0, stderr="")

        result = add_annotations(sample_image, "add red box", output_dir)
        assert result is not None

    @patch("screenshot_analyzer.subprocess.run")
    def test_failed_annotation(self, mock_run, tmp_path, sample_image):
        from screenshot_analyzer import add_annotations
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_run.return_value = MagicMock(returncode=1, stderr="Error occurred")

        result = add_annotations(sample_image, "add red box", output_dir)
        assert result is None

    @patch("screenshot_analyzer.subprocess.run")
    def test_exception_in_annotation(self, mock_run, tmp_path, sample_image):
        from screenshot_analyzer import add_annotations
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        mock_run.side_effect = Exception("subprocess error")

        result = add_annotations(sample_image, "add red box", output_dir)
        assert result is None

    @patch("screenshot_analyzer.subprocess.run")
    def test_with_text_label(self, mock_run, tmp_path, sample_image):
        from screenshot_analyzer import add_annotations
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        expected_output = output_dir / f"{sample_image.stem}_annotated.png"
        expected_output.write_bytes(b"fake image")

        mock_run.return_value = MagicMock(returncode=0, stderr="")

        result = add_annotations(
            sample_image, "add label", output_dir,
            style="callout", text_label="ここ"
        )
        assert result is not None
        # Verify --text flag was passed
        call_args = mock_run.call_args[0][0]
        assert "--text" in call_args
        assert "ここ" in call_args


class TestAnalyzeForTutorial:
    def test_no_client(self, sample_image):
        from screenshot_analyzer import analyze_for_tutorial
        result = analyze_for_tutorial(None, sample_image)
        assert "title" in result
        assert result["steps"] == []

    def test_successful_response(self, sample_image):
        from screenshot_analyzer import analyze_for_tutorial
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "ログイン画面",
            "description": "ユーザー認証画面",
            "steps": [
                {"step": 1, "action": "メールを入力", "detail": "上のフィールド", "location": "中央"}
            ],
            "tips": ["パスワードは8文字以上"]
        })
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_for_tutorial(mock_client, sample_image)
        assert result["title"] == "ログイン画面"
        assert len(result["steps"]) == 1

    def test_non_json_response(self, sample_image):
        from screenshot_analyzer import analyze_for_tutorial
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Not JSON"
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_for_tutorial(mock_client, sample_image)
        assert "title" in result

    def test_api_error(self, sample_image):
        from screenshot_analyzer import analyze_for_tutorial
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("Error")

        result = analyze_for_tutorial(mock_client, sample_image)
        assert "title" in result
        assert result["steps"] == []


class TestBuildAnalyzeHtml:
    def test_basic_html(self, tmp_path, sample_image):
        from screenshot_analyzer import build_analyze_html
        analysis = {
            "description": "テスト画面",
            "has_error": False,
        }
        next_steps = {
            "summary": "問題なし",
            "steps": [],
        }
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, None, next_steps, output_path)
        assert "テスト画面" in html
        assert "問題なし" in html

    def test_with_error(self, tmp_path, sample_image):
        from screenshot_analyzer import build_analyze_html
        analysis = {
            "description": "エラー画面",
            "has_error": True,
            "error_details": {
                "error_message": "ModuleNotFoundError",
                "error_type": "ImportError",
                "possible_causes": ["モジュール未インストール"]
            },
        }
        next_steps = {
            "summary": "修正手順",
            "steps": [{"step": "1", "action": "pip install", "explanation": "依存関係"}],
            "expected_result": "正常動作"
        }
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, None, next_steps, output_path)
        assert "ModuleNotFoundError" in html
        assert "モジュール未インストール" in html

    def test_with_annotated_image(self, tmp_path, sample_image):
        from screenshot_analyzer import build_analyze_html
        analysis = {
            "description": "エラー画面",
            "has_error": True,
            "error_details": {"error_message": "Error"},
        }
        next_steps = {"summary": "修正", "steps": []}
        annotated = str(tmp_path / "annotated.png")
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, annotated, next_steps, output_path)
        assert "注釈付き" in html


class TestBuildTutorialHtml:
    def test_basic_tutorial(self, tmp_path, sample_image):
        from screenshot_analyzer import build_tutorial_html
        result = {
            "title": "設定画面",
            "description": "アプリの設定を変更",
            "steps": [
                {"step": 1, "action": "設定を開く", "detail": "左メニュー", "location": "左上"}
            ],
            "tips": ["保存を忘れずに"]
        }
        output_path = tmp_path / "tutorial.html"
        html = build_tutorial_html(sample_image, result, output_path)
        assert "設定画面" in html
        assert "設定を開く" in html
        assert "保存を忘れずに" in html

    def test_with_annotated_paths(self, tmp_path, sample_image):
        from screenshot_analyzer import build_tutorial_html
        result = {
            "title": "チュートリアル",
            "description": "テスト",
            "steps": [
                {"step": 1, "action": "Step 1"},
                {"step": 2, "action": "Step 2"},
            ],
        }
        annotated = [str(tmp_path / "step1.png"), str(tmp_path / "step2.png")]
        output_path = tmp_path / "tutorial.html"
        html = build_tutorial_html(sample_image, result, output_path, annotated)
        assert "Step 1" in html
        assert "Step 2" in html

    def test_empty_steps(self, tmp_path, sample_image):
        from screenshot_analyzer import build_tutorial_html
        result = {"title": "Empty", "description": "No steps", "steps": [], "tips": []}
        output_path = tmp_path / "tutorial.html"
        html = build_tutorial_html(sample_image, result, output_path)
        assert "Empty" in html

    def test_no_tips(self, tmp_path, sample_image):
        from screenshot_analyzer import build_tutorial_html
        result = {
            "title": "No tips",
            "description": "テスト",
            "steps": [{"step": 1, "action": "action"}],
        }
        output_path = tmp_path / "tutorial.html"
        html = build_tutorial_html(sample_image, result, output_path)
        assert "No tips" in html


# ===========================================================================
# get_rel_path edge cases (lines 51-52)
# ===========================================================================

class TestGetRelPathEdge:
    def test_relative_to_cwd_fallback(self, tmp_path):
        """output_path が None で cwd からの相対パスに失敗する場合 (lines 51-52, 55-57)"""
        from screenshot_analyzer import get_rel_path
        # Absolute path that can't be relativized to cwd
        result = get_rel_path("/some/absolute/path/image.png", None)
        assert result  # Should return a non-empty string

    def test_different_drives_value_error(self, tmp_path):
        """os.path.relpath が ValueError を出す場合 (line 52)"""
        from screenshot_analyzer import get_rel_path
        # On Unix, this won't naturally trigger ValueError,
        # but we can still test the function handles it
        with patch("os.path.relpath", side_effect=ValueError("different drives")):
            result = get_rel_path(str(tmp_path / "image.png"), tmp_path / "output.html")
        # Should fallback to absolute path
        assert str(tmp_path) in result


# ===========================================================================
# analyze_screenshot JSON in code block (line 167)
# ===========================================================================

class TestAnalyzeScreenshotCodeBlock:
    def test_json_with_trailing_backticks(self, sample_image):
        """JSON の後に ``` がある形式のレスポンス (line 165-167)"""
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_response = MagicMock()
        # The regex r'\s*(.*?)\s*```' extracts content before the first ```
        mock_response.text = '{"description": "抽出テスト", "has_error": false, "error_details": null, "suggestions": []} ```'
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_screenshot(mock_client, sample_image)
        assert result["description"] == "抽出テスト"

    def test_json_response_with_error_keyword(self, sample_image):
        """Non-JSON response containing "エラー" triggers has_error (line 175)"""
        from screenshot_analyzer import analyze_screenshot
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "この画面にはエラーが表示されています"
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_screenshot(mock_client, sample_image)
        assert result["has_error"] is True


# ===========================================================================
# generate_next_steps JSON in code block (line 237)
# ===========================================================================

class TestGenerateNextStepsCodeBlock:
    def test_json_with_trailing_backticks(self):
        """JSON の後に ``` がある形式のレスポンス (line 235-237)"""
        from screenshot_analyzer import generate_next_steps
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"summary": "手順", "steps": [{"step": "1", "action": "確認", "explanation": "理由"}], "expected_result": "解決"} ```'
        mock_client.models.generate_content.return_value = mock_response

        analysis = {"description": "test", "has_error": True, "suggestions": []}
        result = generate_next_steps(mock_client, analysis)
        assert result["summary"] == "手順"


# ===========================================================================
# add_step_annotations (lines 416-448)
# ===========================================================================

class TestAddStepAnnotations:
    @patch("screenshot_analyzer.add_annotations")
    def test_all_steps_annotated(self, mock_annotate, tmp_path, sample_image):
        """全ステップに注釈が付く (lines 416-448)"""
        from screenshot_analyzer import add_step_annotations
        mock_annotate.return_value = str(tmp_path / "annotated.png")

        steps = [
            {"step": 1, "action": "クリック", "location": "右上"},
            {"step": 2, "action": "入力", "location": "中央"},
        ]
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = add_step_annotations(sample_image, steps, output_dir)
        assert len(result) == 2
        assert all(r is not None for r in result)

    @patch("screenshot_analyzer.add_annotations")
    def test_some_steps_fail(self, mock_annotate, tmp_path, sample_image):
        """一部ステップの注釈が失敗 (line 446)"""
        from screenshot_analyzer import add_step_annotations
        mock_annotate.side_effect = [
            str(tmp_path / "step1.png"),
            None,  # fail
        ]

        steps = [
            {"step": 1, "action": "成功"},
            {"step": 2, "action": "失敗"},
        ]
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = add_step_annotations(sample_image, steps, output_dir)
        assert len(result) == 2
        assert result[0] is not None
        assert result[1] is None

    @patch("screenshot_analyzer.add_annotations")
    def test_step_without_location(self, mock_annotate, tmp_path, sample_image):
        """location がないステップ"""
        from screenshot_analyzer import add_step_annotations
        mock_annotate.return_value = str(tmp_path / "annotated.png")

        steps = [{"step": 1, "action": "アクション"}]
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        result = add_step_annotations(sample_image, steps, output_dir)
        assert len(result) == 1


# ===========================================================================
# analyze_for_tutorial JSON in code block (line 389)
# ===========================================================================

class TestAnalyzeForTutorialCodeBlock:
    def test_json_with_trailing_backticks(self, sample_image):
        """JSON の後に ``` がある形式のレスポンス (line 387-389)"""
        from screenshot_analyzer import analyze_for_tutorial
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"title": "ブロック内", "description": "テスト", "steps": [], "tips": []} ```'
        mock_client.models.generate_content.return_value = mock_response

        result = analyze_for_tutorial(mock_client, sample_image)
        assert result["title"] == "ブロック内"


# ===========================================================================
# main function (lines 508-611)
# ===========================================================================

class TestMainFunction:
    @patch("screenshot_analyzer.save_html_file")
    @patch("screenshot_analyzer.create_html_template", return_value="<html></html>")
    @patch("screenshot_analyzer.get_client")
    def test_main_analyze_mode(self, mock_get_client, mock_template, mock_save, tmp_path, sample_image):
        """analyze モード (lines 575-594)"""
        from screenshot_analyzer import main
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "description": "テスト画面",
            "has_error": False,
            "error_details": None,
            "suggestions": ["次へ"],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "analyze",
            "--output", str(tmp_path / "report.html"),
        ]):
            main()
        mock_save.assert_called_once()

    @patch("screenshot_analyzer.save_html_file")
    @patch("screenshot_analyzer.create_html_template", return_value="<html></html>")
    @patch("screenshot_analyzer.get_client")
    def test_main_tutorial_mode(self, mock_get_client, mock_template, mock_save, tmp_path, sample_image):
        """tutorial モード (lines 596-607)"""
        from screenshot_analyzer import main
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "チュートリアル",
            "description": "テスト",
            "steps": [{"step": 1, "action": "実行", "detail": "詳細", "location": "上"}],
            "tips": ["ヒント"],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "tutorial",
            "--no-annotate",
            "--output", str(tmp_path / "tutorial.html"),
        ]):
            main()
        mock_save.assert_called_once()

    @patch("screenshot_analyzer.get_client", return_value=None)
    def test_main_no_client_exits(self, mock_get_client, sample_image):
        """client なしで sys.exit(1) (lines 560-563)"""
        from screenshot_analyzer import main
        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "analyze",
        ]), pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_main_missing_image_exits(self, tmp_path):
        """画像ファイルが見つからない (lines 554-556)"""
        from screenshot_analyzer import main
        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(tmp_path / "nonexistent.png"),
            "--mode", "analyze",
        ]), pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    @patch("screenshot_analyzer.save_html_file")
    @patch("screenshot_analyzer.create_html_template", return_value="<html></html>")
    @patch("screenshot_analyzer.get_client")
    def test_main_analyze_with_error_and_annotation(
        self, mock_get_client, mock_template, mock_save, tmp_path, sample_image
    ):
        """analyze モードでエラー + 注釈 (lines 581-587)"""
        from screenshot_analyzer import main
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # First call: analyze_screenshot
        analyze_resp = MagicMock()
        analyze_resp.text = json.dumps({
            "description": "エラー画面",
            "has_error": True,
            "error_details": {
                "error_message": "ModuleNotFoundError: no module named 'foo'",
                "error_type": "ImportError",
                "possible_causes": ["モジュール未インストール"],
            },
            "suggestions": ["pip install foo"],
        })
        # Second call: generate_next_steps
        next_steps_resp = MagicMock()
        next_steps_resp.text = json.dumps({
            "summary": "修正手順",
            "steps": [{"step": "1", "action": "pip install foo", "explanation": "依存追加"}],
            "expected_result": "正常動作",
        })
        mock_client.models.generate_content.side_effect = [analyze_resp, next_steps_resp]

        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "analyze",
            "--output", str(tmp_path / "report.html"),
        ]), patch("screenshot_analyzer.add_annotations", return_value=str(tmp_path / "annotated.png")):
            main()
        mock_save.assert_called_once()

    @patch("screenshot_analyzer.save_html_file")
    @patch("screenshot_analyzer.create_html_template", return_value="<html></html>")
    @patch("screenshot_analyzer.get_client")
    def test_main_default_output_path(self, mock_get_client, mock_template, mock_save, sample_image):
        """output 未指定時のデフォルトパス (lines 566-570)"""
        from screenshot_analyzer import main
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "description": "テスト",
            "has_error": False,
            "error_details": None,
            "suggestions": [],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "analyze",
        ]):
            main()
        mock_save.assert_called_once()

    @patch("screenshot_analyzer.save_html_file")
    @patch("screenshot_analyzer.create_html_template", return_value="<html></html>")
    @patch("screenshot_analyzer.get_client")
    def test_main_tutorial_with_annotations(
        self, mock_get_client, mock_template, mock_save, tmp_path, sample_image
    ):
        """tutorial モードで注釈あり (lines 600-603)"""
        from screenshot_analyzer import main
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "title": "手順",
            "description": "操作説明",
            "steps": [
                {"step": 1, "action": "クリック", "detail": "ボタン", "location": "右"},
            ],
            "tips": [],
        })
        mock_client.models.generate_content.return_value = mock_response

        with patch("sys.argv", [
            "screenshot_analyzer.py",
            str(sample_image),
            "--mode", "tutorial",
            "--output", str(tmp_path / "tutorial.html"),
        ]), patch("screenshot_analyzer.add_step_annotations", return_value=[str(tmp_path / "step1.png")]):
            main()
        mock_save.assert_called_once()


# ===========================================================================
# build_analyze_html edge cases (step_data is string, not dict)
# ===========================================================================

class TestBuildAnalyzeHtmlEdge:
    def test_steps_as_strings(self, tmp_path, sample_image):
        """steps が文字列リストの場合の処理"""
        from screenshot_analyzer import build_analyze_html
        analysis = {"description": "テスト", "has_error": False}
        next_steps = {
            "summary": "概要",
            "steps": ["ステップ1を実行", "ステップ2を実行"],
        }
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, None, next_steps, output_path)
        assert "ステップ1を実行" in html

    def test_with_expected_result(self, tmp_path, sample_image):
        """expected_result がある場合 (line 327)"""
        from screenshot_analyzer import build_analyze_html
        analysis = {"description": "テスト", "has_error": False}
        next_steps = {
            "summary": "概要",
            "steps": [],
            "expected_result": "問題が解決される",
        }
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, None, next_steps, output_path)
        assert "問題が解決される" in html

    def test_error_without_details(self, tmp_path, sample_image):
        """has_error=True だが error_details が None"""
        from screenshot_analyzer import build_analyze_html
        analysis = {"description": "エラー", "has_error": True, "error_details": None}
        next_steps = {"summary": "修正", "steps": []}
        output_path = tmp_path / "report.html"
        html = build_analyze_html(sample_image, analysis, None, next_steps, output_path)
        assert "検出された問題" in html
