"""notebooklm_cli.py の単体テスト"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def nlm_module():
    """外部依存をモックしてモジュールをインポート"""
    with patch.dict("sys.modules", {
        "requests": MagicMock(),
    }):
        from tests.conftest import import_module_from_repo
        mod = import_module_from_repo("notebooklm_cli", "tools/notebooklm_cli.py")
        yield mod


# ---------------------------------------------------------------------------
# normalize_endpoint_location
# ---------------------------------------------------------------------------

class TestNormalizeEndpointLocation:
    def test_without_trailing_dash(self, nlm_module):
        assert nlm_module.normalize_endpoint_location("us-central1") == "us-central1-"

    def test_with_trailing_dash(self, nlm_module):
        assert nlm_module.normalize_endpoint_location("us-central1-") == "us-central1-"

    def test_empty_string(self, nlm_module):
        assert nlm_module.normalize_endpoint_location("") == ""

    def test_global_dash(self, nlm_module):
        assert nlm_module.normalize_endpoint_location("global-") == "global-"

    def test_global_no_dash(self, nlm_module):
        assert nlm_module.normalize_endpoint_location("global") == "global-"


# ---------------------------------------------------------------------------
# resolve_param
# ---------------------------------------------------------------------------

class TestResolveParam:
    def test_arg_value_priority(self, nlm_module, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "env_val")
        result = nlm_module.resolve_param("arg_val", "TEST_VAR", label="test")
        assert result == "arg_val"

    def test_env_fallback(self, nlm_module, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "env_val")
        result = nlm_module.resolve_param(None, "TEST_VAR", label="test")
        assert result == "env_val"

    def test_default_fallback(self, nlm_module, monkeypatch):
        monkeypatch.delenv("TEST_VAR", raising=False)
        result = nlm_module.resolve_param(None, "TEST_VAR", default="def", label="test")
        assert result == "def"

    def test_required_missing(self, nlm_module, monkeypatch):
        monkeypatch.delenv("TEST_VAR", raising=False)
        with pytest.raises(SystemExit) as exc_info:
            nlm_module.resolve_param(None, "TEST_VAR", required=True, label="test")
        assert "Missing" in str(exc_info.value)

    def test_required_with_value(self, nlm_module):
        result = nlm_module.resolve_param("val", "UNUSED", required=True, label="test")
        assert result == "val"

    def test_none_not_required(self, nlm_module, monkeypatch):
        monkeypatch.delenv("X", raising=False)
        result = nlm_module.resolve_param(None, "X", label="test")
        assert result is None

    def test_empty_string_arg(self, nlm_module, monkeypatch):
        """空文字列はfalsyなのでenvにフォールバック"""
        monkeypatch.setenv("X", "env")
        result = nlm_module.resolve_param("", "X", label="test")
        assert result == "env"


# ---------------------------------------------------------------------------
# resolve_access_token
# ---------------------------------------------------------------------------

class TestResolveAccessToken:
    def test_cli_token(self, nlm_module):
        assert nlm_module.resolve_access_token("my-token") == "my-token"

    def test_env_token(self, nlm_module, monkeypatch):
        monkeypatch.setenv("NOTEBOOKLM_ACCESS_TOKEN", "env-token")
        assert nlm_module.resolve_access_token(None) == "env-token"

    def test_gcloud_fallback(self, nlm_module, monkeypatch):
        monkeypatch.delenv("NOTEBOOKLM_ACCESS_TOKEN", raising=False)
        mock_result = MagicMock()
        mock_result.stdout = "gcloud-token\n"
        with patch("subprocess.run", return_value=mock_result):
            result = nlm_module.resolve_access_token(None)
        assert result == "gcloud-token"

    def test_gcloud_not_found(self, nlm_module, monkeypatch):
        monkeypatch.delenv("NOTEBOOKLM_ACCESS_TOKEN", raising=False)
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(SystemExit) as exc_info:
                nlm_module.resolve_access_token(None)
            assert "gcloud not found" in str(exc_info.value)

    def test_gcloud_error(self, nlm_module, monkeypatch):
        import subprocess
        monkeypatch.delenv("NOTEBOOKLM_ACCESS_TOKEN", raising=False)
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gcloud", stderr="auth error")):
            with pytest.raises(SystemExit) as exc_info:
                nlm_module.resolve_access_token(None)
            assert "Failed" in str(exc_info.value)

    def test_gcloud_empty_token(self, nlm_module, monkeypatch):
        monkeypatch.delenv("NOTEBOOKLM_ACCESS_TOKEN", raising=False)
        mock_result = MagicMock()
        mock_result.stdout = "  \n"
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(SystemExit) as exc_info:
                nlm_module.resolve_access_token(None)
            assert "Empty" in str(exc_info.value)


# ---------------------------------------------------------------------------
# build_base_url
# ---------------------------------------------------------------------------

class TestBuildBaseUrl:
    def test_basic(self, nlm_module):
        url = nlm_module.build_base_url("global-", "123456", "global")
        assert "discoveryengine.googleapis.com" in url
        assert "123456" in url
        assert "global" in url

    def test_normalizes_location(self, nlm_module):
        url = nlm_module.build_base_url("us-central1", "123", "us-central1")
        assert "us-central1-" in url

    def test_empty_project(self, nlm_module):
        url = nlm_module.build_base_url("global-", "", "global")
        assert "projects//" in url


# ---------------------------------------------------------------------------
# make_headers
# ---------------------------------------------------------------------------

class TestMakeHeaders:
    def test_basic(self, nlm_module):
        headers = nlm_module.make_headers("my-token")
        assert headers["Authorization"] == "Bearer my-token"
        assert headers["Content-Type"] == "application/json"

    def test_empty_token(self, nlm_module):
        headers = nlm_module.make_headers("")
        assert headers["Authorization"] == "Bearer "


# ---------------------------------------------------------------------------
# print_response
# ---------------------------------------------------------------------------

class TestPrintResponse:
    def test_ok_json(self, nlm_module, capsys):
        response = MagicMock()
        response.ok = True
        response.headers = {"content-type": "application/json"}
        response.text = '{"key": "value"}'
        response.json.return_value = {"key": "value"}

        nlm_module.print_response(response, raw=False)
        out = capsys.readouterr().out
        assert "key" in out

    def test_ok_raw(self, nlm_module, capsys):
        response = MagicMock()
        response.ok = True
        response.headers = {"content-type": "application/json"}
        response.text = '{"key":"value"}'

        nlm_module.print_response(response, raw=True)
        out = capsys.readouterr().out
        assert '{"key":"value"}' in out

    def test_error_response(self, nlm_module):
        response = MagicMock()
        response.ok = False
        response.status_code = 401
        response.headers = {"content-type": "text/plain"}
        response.text = "Unauthorized"

        with pytest.raises(SystemExit):
            nlm_module.print_response(response, raw=False)

    def test_ok_non_json(self, nlm_module, capsys):
        response = MagicMock()
        response.ok = True
        response.headers = {"content-type": "text/plain"}
        response.text = "plain text"

        nlm_module.print_response(response, raw=False)
        out = capsys.readouterr().out
        assert "plain text" in out

    def test_ok_json_decode_error(self, nlm_module, capsys):
        response = MagicMock()
        response.ok = True
        response.headers = {"content-type": "application/json"}
        response.text = "not json"
        response.json.side_effect = json.JSONDecodeError("err", "doc", 0)

        nlm_module.print_response(response, raw=False)
        out = capsys.readouterr().out
        assert "not json" in out

    def test_empty_body(self, nlm_module, capsys):
        response = MagicMock()
        response.ok = True
        response.headers = {"content-type": "text/plain"}
        response.text = ""

        nlm_module.print_response(response, raw=False)
        out = capsys.readouterr().out
        assert out.strip() == ""


# ---------------------------------------------------------------------------
# build_parser
# ---------------------------------------------------------------------------

class TestBuildParser:
    def test_parser_creation(self, nlm_module):
        parser = nlm_module.build_parser()
        assert parser is not None

    def test_create_subcommand(self, nlm_module):
        parser = nlm_module.build_parser()
        args = parser.parse_args(["create", "--title", "Test Notebook"])
        assert args.command == "create"
        assert args.title == "Test Notebook"

    def test_get_subcommand(self, nlm_module):
        parser = nlm_module.build_parser()
        args = parser.parse_args(["get", "--notebook-id", "nb123"])
        assert args.command == "get"
        assert args.notebook_id == "nb123"

    def test_list_recent_subcommand(self, nlm_module):
        parser = nlm_module.build_parser()
        args = parser.parse_args(["list-recent", "--page-size", "5"])
        assert args.command == "list-recent"
        assert args.page_size == 5

    def test_list_recent_no_page_size(self, nlm_module):
        parser = nlm_module.build_parser()
        args = parser.parse_args(["list-recent"])
        assert args.page_size is None

    def test_no_command(self, nlm_module):
        parser = nlm_module.build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_common_args(self, nlm_module):
        parser = nlm_module.build_parser()
        args = parser.parse_args([
            "create", "--title", "T",
            "--project-number", "123",
            "--location", "us",
            "--endpoint-location", "us-",
            "--access-token", "tok",
            "--raw",
        ])
        assert args.project_number == "123"
        assert args.location == "us"
        assert args.access_token == "tok"
        assert args.raw is True


# ---------------------------------------------------------------------------
# handle_create / handle_get / handle_list_recent (API mocked)
# ---------------------------------------------------------------------------

class TestHandlers:
    def _make_args(self, **kwargs):
        args = MagicMock()
        args.project_number = kwargs.get("project_number", "12345")
        args.location = kwargs.get("location", "global")
        args.endpoint_location = kwargs.get("endpoint_location", "global-")
        args.access_token = kwargs.get("access_token", "test-token")
        args.raw = kwargs.get("raw", False)
        return args

    def test_handle_create(self, nlm_module, capsys):
        args = self._make_args()
        args.title = "Test"

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"name": "notebook/123"}'
        mock_response.json.return_value = {"name": "notebook/123"}

        with patch("requests.post", return_value=mock_response):
            nlm_module.handle_create(args)
        out = capsys.readouterr().out
        assert "notebook/123" in out

    def test_handle_get(self, nlm_module, capsys):
        args = self._make_args()
        args.notebook_id = "nb123"

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"id": "nb123"}'
        mock_response.json.return_value = {"id": "nb123"}

        with patch("requests.get", return_value=mock_response):
            nlm_module.handle_get(args)
        out = capsys.readouterr().out
        assert "nb123" in out

    def test_handle_list_recent(self, nlm_module, capsys):
        args = self._make_args()
        args.page_size = 10

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"notebooks": []}'
        mock_response.json.return_value = {"notebooks": []}

        with patch("requests.get", return_value=mock_response):
            nlm_module.handle_list_recent(args)
        out = capsys.readouterr().out
        assert "notebooks" in out

    def test_handle_list_recent_no_page_size(self, nlm_module, capsys):
        args = self._make_args()
        args.page_size = None

        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = '{"notebooks": []}'
        mock_response.json.return_value = {"notebooks": []}

        with patch("requests.get", return_value=mock_response):
            nlm_module.handle_list_recent(args)

    def test_handle_create_missing_project(self, nlm_module, monkeypatch):
        monkeypatch.delenv("NOTEBOOKLM_PROJECT_NUMBER", raising=False)
        args = MagicMock()
        args.project_number = None
        args.title = "T"
        args.location = None
        args.endpoint_location = None
        args.access_token = "tok"
        args.raw = False

        with pytest.raises(SystemExit):
            nlm_module.handle_create(args)
