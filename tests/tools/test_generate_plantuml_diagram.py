"""generate_plantuml_diagram.py の単体テスト"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helper: import with mocked dependencies
# ---------------------------------------------------------------------------

@pytest.fixture
def puml_module():
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
        mod = import_module_from_repo(
            "generate_plantuml_diagram", "tools/generate_plantuml_diagram.py"
        )
        yield mod


@pytest.fixture
def sample_puml(tmp_path):
    """基本的なPlantUMLファイル"""
    content = """@startuml
participant "User" as user
participant "API" as api
participant "Database" as db

user -> api: リクエスト送信
api -> db: データ取得
db --> api: レスポンス
api --> user: 結果表示

alt 成功時
    user -> api: 確認
else 失敗時
    user -> api: 再試行
end
@enduml"""
    path = tmp_path / "test.puml"
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def empty_puml(tmp_path):
    path = tmp_path / "empty.puml"
    path.write_text("", encoding="utf-8")
    return path


@pytest.fixture
def complex_puml(tmp_path):
    """多数のparticipantとメッセージを持つPlantUML"""
    lines = ["@startuml"]
    for i in range(6):
        lines.append(f'participant "Service{i}" as s{i}')
    for i in range(25):
        lines.append(f"s{i % 6} -> s{(i+1) % 6}: message_{i}")
    lines.append("@enduml")
    path = tmp_path / "complex.puml"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# parse_plantuml_structure
# ---------------------------------------------------------------------------

class TestParsePlantumlStructure:
    def test_basic_parsing(self, puml_module, sample_puml):
        content = sample_puml.read_text(encoding="utf-8")
        structure = puml_module.parse_plantuml_structure(content)
        assert structure["participant_count"] == 3
        assert structure["message_count"] >= 3
        assert structure["branch_count"] >= 2  # alt + else

    def test_empty_content(self, puml_module):
        structure = puml_module.parse_plantuml_structure("")
        assert structure["participant_count"] == 0
        assert structure["message_count"] == 0
        assert structure["branch_count"] == 0

    def test_no_participants(self, puml_module):
        content = "user -> api: hello"
        structure = puml_module.parse_plantuml_structure(content)
        assert structure["participant_count"] == 0

    def test_loop_and_opt(self, puml_module):
        content = """loop 5 times
  a -> b: repeat
end
opt condition
  b -> c: optional
end"""
        structure = puml_module.parse_plantuml_structure(content)
        assert structure["branch_count"] >= 2  # loop + opt

    def test_unicode_content(self, puml_module):
        content = """participant "ユーザー" as user
participant "サーバー" as server
user -> server: データ送信"""
        structure = puml_module.parse_plantuml_structure(content)
        assert structure["participant_count"] == 2


# ---------------------------------------------------------------------------
# determine_aspect_ratio
# ---------------------------------------------------------------------------

class TestDetermineAspectRatio:
    def test_many_participants_wide(self, puml_module):
        """5+ participants -> 21:9"""
        structure = {"participant_count": 5, "message_count": 5, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "21:9"

    def test_long_sequence_tall(self, puml_module):
        """20+ messages -> 9:16"""
        structure = {"participant_count": 2, "message_count": 25, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "9:16"

    def test_medium_participants(self, puml_module):
        """3-4 participants -> 16:9"""
        structure = {"participant_count": 3, "message_count": 10, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "16:9"

    def test_default(self, puml_module):
        """少数 -> 16:9"""
        structure = {"participant_count": 2, "message_count": 5, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "16:9"

    def test_boundary_5_participants(self, puml_module):
        """境界値: ちょうど5"""
        structure = {"participant_count": 5, "message_count": 0, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "21:9"

    def test_boundary_4_participants(self, puml_module):
        structure = {"participant_count": 4, "message_count": 0, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "16:9"

    def test_boundary_20_messages(self, puml_module):
        structure = {"participant_count": 2, "message_count": 20, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "9:16"

    def test_boundary_19_messages(self, puml_module):
        structure = {"participant_count": 2, "message_count": 19, "branch_count": 0}
        assert puml_module.determine_aspect_ratio(structure) == "16:9"


# ---------------------------------------------------------------------------
# sanitize_filename
# ---------------------------------------------------------------------------

class TestSanitizeFilename:
    def test_basic(self, puml_module):
        assert puml_module.sanitize_filename("hello world") == "hello_world"

    def test_special_characters(self, puml_module):
        assert "<" not in puml_module.sanitize_filename('te<s>t:"file"')
        assert ">" not in puml_module.sanitize_filename('te<s>t:"file"')

    def test_length_limit(self, puml_module):
        long_name = "a" * 100
        result = puml_module.sanitize_filename(long_name, max_length=30)
        assert len(result) == 30

    def test_custom_max_length(self, puml_module):
        result = puml_module.sanitize_filename("abcdef", max_length=3)
        assert result == "abc"

    def test_empty_string(self, puml_module):
        result = puml_module.sanitize_filename("")
        assert result == ""

    def test_unicode(self, puml_module):
        result = puml_module.sanitize_filename("日本語テスト")
        assert "日本語" in result

    def test_multiple_spaces(self, puml_module):
        result = puml_module.sanitize_filename("a  b   c")
        assert result == "a_b_c"


# ---------------------------------------------------------------------------
# get_client
# ---------------------------------------------------------------------------

class TestGetClient:
    def test_get_client_no_key(self, puml_module, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        with pytest.raises(SystemExit):
            puml_module.get_client()

    def test_get_client_with_gemini_key(self, puml_module, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key")
        # get_client calls genai.Client which is mocked
        client = puml_module.get_client()
        assert client is not None


# ---------------------------------------------------------------------------
# create_diagram_prompt (API call mocked)
# ---------------------------------------------------------------------------

class TestCreateDiagramPrompt:
    def test_returns_string(self, puml_module):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Generated prompt text here"
        mock_client.models.generate_content.return_value = mock_response

        structure = {"participant_count": 2, "message_count": 3, "branch_count": 1}
        result = puml_module.create_diagram_prompt(mock_client, "test content", structure)
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# generate_diagram_image (API call mocked)
# ---------------------------------------------------------------------------

class TestGenerateDiagramImage:
    def test_success(self, puml_module, tmp_path):
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = True
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output = tmp_path / "diagram.png"
        with patch.object(puml_module, "get_image_model", return_value="model"):
            result = puml_module.generate_diagram_image(
                mock_client, "prompt", output, "16:9"
            )
        assert result is True

    def test_no_image_in_response(self, puml_module, tmp_path):
        mock_client = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = None
        mock_response = MagicMock()
        mock_response.parts = [mock_part]
        mock_client.models.generate_content.return_value = mock_response

        output = tmp_path / "diagram.png"
        with patch.object(puml_module, "get_image_model", return_value="model"):
            result = puml_module.generate_diagram_image(
                mock_client, "prompt", output, "16:9"
            )
        assert result is False

    def test_api_error(self, puml_module, tmp_path):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API error")

        output = tmp_path / "diagram.png"
        with patch.object(puml_module, "get_image_model", return_value="model"):
            result = puml_module.generate_diagram_image(
                mock_client, "prompt", output, "16:9"
            )
        assert result is False


# ---------------------------------------------------------------------------
# main (lines 288-382)
# ---------------------------------------------------------------------------

class TestMain:
    def test_file_not_found(self, puml_module, tmp_path):
        """存在しないファイル指定でsys.exit"""
        with patch("sys.argv", ["prog", str(tmp_path / "nonexistent.puml")]):
            with pytest.raises(SystemExit):
                puml_module.main()

    def test_empty_file(self, puml_module, empty_puml):
        """空のPlantUMLファイルでsys.exit"""
        with patch("sys.argv", ["prog", str(empty_puml)]):
            with pytest.raises(SystemExit):
                puml_module.main()

    def test_read_error(self, puml_module, tmp_path):
        """読み込みエラーでsys.exit"""
        bad_file = tmp_path / "bad.puml"
        bad_file.write_bytes(b"\x80\x81\x82")
        with patch("sys.argv", ["prog", str(bad_file)]):
            with pytest.raises((SystemExit, UnicodeDecodeError)):
                puml_module.main()

    def test_successful_run_auto_aspect(self, puml_module, sample_puml, tmp_path):
        """正常実行: auto aspect ratio"""
        output_path = tmp_path / "output.png"
        mock_client = MagicMock()

        mock_prompt_response = MagicMock()
        mock_prompt_response.text = "generated prompt"
        mock_client.models.generate_content.return_value = mock_prompt_response

        with patch("sys.argv", ["prog", str(sample_puml), "-o", str(output_path)]), \
             patch.object(puml_module, "get_client", return_value=mock_client), \
             patch.object(puml_module, "get_flash_model", return_value="flash"), \
             patch.object(puml_module, "generate_diagram_image", return_value=True):
            puml_module.main()

    def test_successful_run_fixed_aspect(self, puml_module, sample_puml, tmp_path):
        """正常実行: 固定 aspect ratio"""
        output_path = tmp_path / "output.png"
        mock_client = MagicMock()

        mock_prompt_response = MagicMock()
        mock_prompt_response.text = "generated prompt"
        mock_client.models.generate_content.return_value = mock_prompt_response

        with patch("sys.argv", ["prog", str(sample_puml), "-a", "1:1", "-o", str(output_path)]), \
             patch.object(puml_module, "get_client", return_value=mock_client), \
             patch.object(puml_module, "get_flash_model", return_value="flash"), \
             patch.object(puml_module, "generate_diagram_image", return_value=True):
            puml_module.main()

    def test_default_output_path(self, puml_module, sample_puml):
        """出力パス未指定時のデフォルト生成"""
        mock_client = MagicMock()
        mock_prompt_response = MagicMock()
        mock_prompt_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_prompt_response

        with patch("sys.argv", ["prog", str(sample_puml)]), \
             patch.object(puml_module, "get_client", return_value=mock_client), \
             patch.object(puml_module, "get_flash_model", return_value="flash"), \
             patch.object(puml_module, "generate_diagram_image", return_value=True):
            puml_module.main()

    def test_failure_exits(self, puml_module, sample_puml, tmp_path):
        """画像生成失敗でsys.exit(1)"""
        output_path = tmp_path / "output.png"
        mock_client = MagicMock()
        mock_prompt_response = MagicMock()
        mock_prompt_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_prompt_response

        with patch("sys.argv", ["prog", str(sample_puml), "-o", str(output_path)]), \
             patch.object(puml_module, "get_client", return_value=mock_client), \
             patch.object(puml_module, "get_flash_model", return_value="flash"), \
             patch.object(puml_module, "generate_diagram_image", return_value=False):
            with pytest.raises(SystemExit):
                puml_module.main()

    def test_existing_output_file_warning(self, puml_module, sample_puml, tmp_path, capsys):
        """既存ファイルへの上書き警告"""
        output_path = tmp_path / "output.png"
        output_path.write_text("existing")
        mock_client = MagicMock()
        mock_prompt_response = MagicMock()
        mock_prompt_response.text = "prompt"
        mock_client.models.generate_content.return_value = mock_prompt_response

        with patch("sys.argv", ["prog", str(sample_puml), "-o", str(output_path)]), \
             patch.object(puml_module, "get_client", return_value=mock_client), \
             patch.object(puml_module, "get_flash_model", return_value="flash"), \
             patch.object(puml_module, "generate_diagram_image", return_value=True):
            puml_module.main()
        captured = capsys.readouterr()
        assert "Warning" in captured.out
