"""guide_action.py の単体テスト"""
import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def guide_module():
    """外部依存をモックしてモジュールをインポート"""
    mock_bootcamp = MagicMock()
    mock_bootcamp.DEFAULT_OUTPUT_DIR = Path("/tmp/test_output")
    mock_bootcamp.get_client.return_value = None
    mock_bootcamp.get_flash_model.return_value = "flash-model"
    mock_bootcamp.markdown_to_html.side_effect = lambda x: f"<p>{x}</p>"
    mock_bootcamp.build_referenced_files_html.return_value = "<div>refs</div>"
    mock_bootcamp.create_html_template.side_effect = lambda title, content: f"<html>{content}</html>"
    mock_bootcamp.save_html_file.return_value = None

    with patch.dict("sys.modules", {
        "bootcamp_utils": mock_bootcamp,
    }):
        from tests.conftest import import_module_from_repo
        mod = import_module_from_repo("guide_action", "tools/guide_action.py")
        yield mod


# ---------------------------------------------------------------------------
# analyze_current_situation
# ---------------------------------------------------------------------------

class TestAnalyzeCurrentSituation:
    def test_without_client(self, guide_module):
        """client=Noneの場合はデフォルトを返す"""
        result = guide_module.analyze_current_situation(None, "some content")
        assert "current_task" in result
        assert "next_steps" in result
        assert isinstance(result["next_steps"], list)

    def test_with_client_success(self, guide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "current_task": "テスト実装",
            "progress": "50%",
            "challenges": ["課題1"],
            "next_steps": ["ステップ1"],
            "context": "テスト中",
        })
        mock_client.models.generate_content.return_value = mock_response

        result = guide_module.analyze_current_situation(mock_client, "content")
        assert result["current_task"] == "テスト実装"

    def test_with_client_json_in_code_block(self, guide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '```json\n{"current_task": "T", "progress": "P", "challenges": [], "next_steps": ["S"], "context": "C"}\n```'
        mock_client.models.generate_content.return_value = mock_response

        result = guide_module.analyze_current_situation(mock_client, "content")
        assert result["current_task"] == "T"

    def test_with_client_error(self, guide_module):
        """APIエラー時はデフォルトを返す"""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API error")

        result = guide_module.analyze_current_situation(mock_client, "content")
        assert "current_task" in result

    def test_empty_content(self, guide_module):
        result = guide_module.analyze_current_situation(None, "")
        assert "current_task" in result

    def test_very_long_content(self, guide_module):
        """8000文字超のコンテンツ（truncateされる）"""
        long_content = "x" * 20000
        result = guide_module.analyze_current_situation(None, long_content)
        assert "current_task" in result


# ---------------------------------------------------------------------------
# generate_background_explanation
# ---------------------------------------------------------------------------

class TestGenerateBackgroundExplanation:
    def test_without_client(self, guide_module):
        situation = {"current_task": "テスト", "next_steps": ["次"]}
        result = guide_module.generate_background_explanation(None, situation, "content")
        assert isinstance(result, str)
        assert "テスト" in result

    def test_with_client_success(self, guide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "背景説明テキスト"
        mock_client.models.generate_content.return_value = mock_response

        situation = {"current_task": "T", "progress": "P", "next_steps": ["S"]}
        result = guide_module.generate_background_explanation(mock_client, situation, "content")
        assert result == "背景説明テキスト"

    def test_with_client_error(self, guide_module):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")

        situation = {"current_task": "T", "next_steps": []}
        result = guide_module.generate_background_explanation(mock_client, situation, "content")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# generate_prompt_example
# ---------------------------------------------------------------------------

class TestGeneratePromptExample:
    def test_without_client(self, guide_module):
        situation = {"current_task": "テスト", "next_steps": ["次のアクション"]}
        result = guide_module.generate_prompt_example(None, situation, "bg")
        assert "テスト" in result
        assert "次のアクション" in result

    def test_without_client_empty_steps(self, guide_module):
        situation = {"current_task": "タスク", "next_steps": []}
        result = guide_module.generate_prompt_example(None, situation, "bg")
        assert isinstance(result, str)

    def test_with_client_success(self, guide_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "プロンプト例テキスト"
        mock_client.models.generate_content.return_value = mock_response

        situation = {"current_task": "T", "progress": "P", "next_steps": ["S"]}
        result = guide_module.generate_prompt_example(mock_client, situation, "bg")
        assert result == "プロンプト例テキスト"

    def test_with_client_error(self, guide_module):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("fail")

        situation = {"current_task": "T", "next_steps": []}
        result = guide_module.generate_prompt_example(mock_client, situation, "bg")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# build_html_content
# ---------------------------------------------------------------------------

class TestBuildHtmlContent:
    def test_basic(self, guide_module):
        situation = {
            "current_task": "テスト作成",
            "progress": "50%",
            "challenges": ["チャレンジ1"],
            "next_steps": ["ステップ1", "ステップ2"],
        }
        html = guide_module.build_html_content(
            situation, "背景説明", "プロンプト例", ["file1.md"]
        )
        assert "テスト作成" in html
        assert "50%" in html
        assert "チャレンジ1" in html
        assert "ステップ1" in html
        assert "プロンプト例" in html

    def test_no_challenges(self, guide_module):
        situation = {
            "current_task": "T",
            "progress": "P",
            "challenges": [],
            "next_steps": ["S1"],
        }
        html = guide_module.build_html_content(situation, "bg", "prompt", [])
        assert "T" in html
        # challenges が空なので <li> がない

    def test_no_next_steps(self, guide_module):
        situation = {
            "current_task": "T",
            "progress": "P",
            "challenges": [],
            "next_steps": [],
        }
        html = guide_module.build_html_content(situation, "bg", "prompt", [])
        assert "特定できません" in html

    def test_unicode_content(self, guide_module):
        situation = {
            "current_task": "日本語タスク",
            "progress": "進行中",
            "challenges": ["日本語課題"],
            "next_steps": ["日本語ステップ"],
        }
        html = guide_module.build_html_content(situation, "日本語背景", "日本語プロンプト", [])
        assert "日本語タスク" in html

    def test_many_next_steps(self, guide_module):
        """期待される結果は最大3つまで"""
        situation = {
            "current_task": "T",
            "progress": "P",
            "challenges": [],
            "next_steps": ["S1", "S2", "S3", "S4", "S5"],
        }
        html = guide_module.build_html_content(situation, "bg", "prompt", [])
        # step-number が5つある (next_steps)
        assert "S5" in html
        # 期待される結果 section は最大3つのliのみ
        assert "S4が完了する" not in html

    def test_with_referenced_files(self, guide_module):
        situation = {
            "current_task": "T",
            "progress": "P",
            "challenges": [],
            "next_steps": ["S1"],
        }
        html = guide_module.build_html_content(
            situation, "bg", "prompt", ["file1.md", "file2.md"]
        )
        assert "refs" in html  # from mocked build_referenced_files_html


# ---------------------------------------------------------------------------
# main function (lines 152-223)
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_list_mode(self, guide_module):
        """Lines 165-174: --list flag"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = [
            {"index": 1, "name": "file1.md", "path": "/tmp/file1.md"},
        ]
        mock_bootcamp.print_specstory_file_list.return_value = None

        with patch("sys.argv", ["guide_action.py", "--list"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 0

    def test_main_list_empty(self, guide_module):
        """Lines 167-169: --list with no files"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = []

        with patch("sys.argv", ["guide_action.py", "--list"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 1

    def test_main_list_json(self, guide_module):
        """Lines 170-171: --list --json"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = [
            {"index": 1, "name": "file1.md", "path": "/tmp/file1.md"},
        ]
        mock_bootcamp.list_specstory_files_json.return_value = '[]'

        with patch("sys.argv", ["guide_action.py", "--list", "--json"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 0

    def test_main_names_mode(self, guide_module):
        """Lines 177-184: --names flag"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.get_specstory_files_by_names.return_value = ["/tmp/file1.md"]
        mock_bootcamp.get_specstory_content_from_files.return_value = ("content", ["/tmp/file1.md"])
        mock_bootcamp.get_client.return_value = None
        mock_bootcamp.create_html_template.side_effect = lambda title, content: f"<html>{content}</html>"
        mock_bootcamp.save_html_file.return_value = None

        with patch("sys.argv", ["guide_action.py", "--names", "file1.md"]):
            guide_module.main()

    def test_main_names_empty(self, guide_module):
        """Lines 180-182: --names with no valid files"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.get_specstory_files_by_names.return_value = []

        with patch("sys.argv", ["guide_action.py", "--names", "nonexistent.md"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 1

    def test_main_select_mode(self, guide_module):
        """Lines 185-195: --select flag"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = [
            {"index": 1, "name": "file1.md", "path": "/tmp/file1.md"},
        ]
        mock_bootcamp.get_selected_specstory_files.return_value = ["/tmp/file1.md"]
        mock_bootcamp.get_specstory_content_from_files.return_value = ("content", ["/tmp/file1.md"])
        mock_bootcamp.get_client.return_value = None
        mock_bootcamp.create_html_template.side_effect = lambda title, content: f"<html>{content}</html>"
        mock_bootcamp.save_html_file.return_value = None

        with patch("sys.argv", ["guide_action.py", "--select", "1"]):
            guide_module.main()

    def test_main_select_no_files(self, guide_module):
        """Lines 187-189: --select with no specstory files"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = []

        with patch("sys.argv", ["guide_action.py", "--select", "1"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 1

    def test_main_select_invalid(self, guide_module):
        """Lines 191-193: --select with invalid selection"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.list_specstory_files_for_selection.return_value = [
            {"index": 1, "name": "file1.md", "path": "/tmp/file1.md"},
        ]
        mock_bootcamp.get_selected_specstory_files.return_value = []

        with patch("sys.argv", ["guide_action.py", "--select", "99"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 1

    def test_main_default_mode(self, guide_module):
        """Lines 196-202: default mode (latest files)"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.get_latest_specstory_files.return_value = ["/tmp/file1.md"]
        mock_bootcamp.get_specstory_content_from_files.return_value = ("content", ["/tmp/file1.md"])
        mock_bootcamp.get_client.return_value = None
        mock_bootcamp.create_html_template.side_effect = lambda title, content: f"<html>{content}</html>"
        mock_bootcamp.save_html_file.return_value = None

        with patch("sys.argv", ["guide_action.py"]):
            guide_module.main()

    def test_main_default_no_files(self, guide_module):
        """Lines 198-200: default mode with no files"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.get_latest_specstory_files.return_value = []

        with patch("sys.argv", ["guide_action.py"]):
            with pytest.raises(SystemExit) as exc_info:
                guide_module.main()
            assert exc_info.value.code == 1

    def test_main_custom_output(self, guide_module, tmp_path):
        """Lines 216-217: --output custom path"""
        mock_bootcamp = sys.modules["bootcamp_utils"]
        mock_bootcamp.get_latest_specstory_files.return_value = ["/tmp/file1.md"]
        mock_bootcamp.get_specstory_content_from_files.return_value = ("content", ["/tmp/file1.md"])
        mock_bootcamp.get_client.return_value = None
        mock_bootcamp.create_html_template.side_effect = lambda title, content: f"<html>{content}</html>"
        mock_bootcamp.save_html_file.return_value = None

        output_path = str(tmp_path / "custom_guide.html")
        with patch("sys.argv", ["guide_action.py", "--output", output_path]):
            guide_module.main()
        # Verify save_html_file was called with the custom path
        call_args = mock_bootcamp.save_html_file.call_args
        assert str(call_args[0][1]) == output_path
