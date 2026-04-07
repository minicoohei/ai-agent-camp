"""google_api_setup.py の単体テスト"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def gapi_module():
    """外部依存をモックしてモジュールをインポート"""
    mock_credentials = MagicMock()
    mock_flow = MagicMock()
    mock_request = MagicMock()

    with patch.dict("sys.modules", {
        "google.oauth2.credentials": mock_credentials,
        "google.oauth2": MagicMock(),
        "google.auth.transport.requests": mock_request,
        "google.auth.transport": MagicMock(),
        "google.auth": MagicMock(),
        "google_auth_oauthlib.flow": mock_flow,
        "google_auth_oauthlib": MagicMock(),
        "google": MagicMock(),
    }):
        from tests.conftest import import_module_from_repo
        mod = import_module_from_repo("google_api_setup", "tools/google_api_setup.py")
        yield mod


@pytest.fixture
def valid_credentials_file(tmp_path):
    """有効なクレデンシャルJSONファイル"""
    data = {
        "installed": {
            "client_id": "12345.apps.googleusercontent.com",
            "client_secret": "secret123",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    path = tmp_path / "credentials.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.fixture
def web_credentials_file(tmp_path):
    """Web型クレデンシャル"""
    data = {
        "web": {
            "client_id": "web-id.apps.googleusercontent.com",
            "client_secret": "web-secret",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    path = tmp_path / "web_credentials.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.fixture
def invalid_credentials_file(tmp_path):
    """無効な形式のクレデンシャルJSON"""
    data = {"unknown": {"something": "value"}}
    path = tmp_path / "invalid_creds.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.fixture
def missing_fields_credentials(tmp_path):
    """必須フィールドが欠けたクレデンシャル"""
    data = {"installed": {"client_id": "id-only"}}
    path = tmp_path / "partial_creds.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Import
# ---------------------------------------------------------------------------

class TestImport:
    def test_import(self, gapi_module):
        assert hasattr(gapi_module, "main")
        assert hasattr(gapi_module, "SCOPES")

    def test_scopes_defined(self, gapi_module):
        assert "gmail" in gapi_module.SCOPES
        assert "calendar" in gapi_module.SCOPES
        assert "drive" in gapi_module.SCOPES
        assert "sheets" in gapi_module.SCOPES


# ---------------------------------------------------------------------------
# validate_credentials
# ---------------------------------------------------------------------------

class TestValidateCredentials:
    def test_valid_installed(self, gapi_module, valid_credentials_file):
        result = gapi_module.validate_credentials(str(valid_credentials_file))
        assert "installed" in result
        assert result["installed"]["client_id"].endswith("googleusercontent.com")

    def test_valid_web(self, gapi_module, web_credentials_file):
        result = gapi_module.validate_credentials(str(web_credentials_file))
        assert "web" in result

    def test_file_not_found(self, gapi_module, tmp_path):
        with pytest.raises(FileNotFoundError):
            gapi_module.validate_credentials(str(tmp_path / "nope.json"))

    def test_invalid_format(self, gapi_module, invalid_credentials_file):
        with pytest.raises(ValueError) as exc_info:
            gapi_module.validate_credentials(str(invalid_credentials_file))
        assert "installed" in str(exc_info.value) or "web" in str(exc_info.value)

    def test_missing_fields(self, gapi_module, missing_fields_credentials):
        with pytest.raises(ValueError) as exc_info:
            gapi_module.validate_credentials(str(missing_fields_credentials))
        assert "Missing" in str(exc_info.value)

    def test_corrupt_json(self, gapi_module, tmp_path):
        path = tmp_path / "corrupt.json"
        path.write_text("not json {{{", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            gapi_module.validate_credentials(str(path))

    def test_empty_file(self, gapi_module, tmp_path):
        path = tmp_path / "empty.json"
        path.write_text("", encoding="utf-8")
        with pytest.raises(Exception):
            gapi_module.validate_credentials(str(path))

    def test_zero_byte_file(self, gapi_module, tmp_path):
        path = tmp_path / "zero.json"
        path.write_bytes(b"")
        with pytest.raises(Exception):
            gapi_module.validate_credentials(str(path))

    def test_binary_garbage(self, gapi_module, tmp_path):
        path = tmp_path / "garbage.json"
        path.write_bytes(b"\x00\x01\x02\xff\xfe")
        with pytest.raises(Exception):
            gapi_module.validate_credentials(str(path))

    def test_tilde_expansion(self, gapi_module, valid_credentials_file):
        """Path.expanduser が呼ばれるか(直接テストは困難なのでフルパスで検証)"""
        result = gapi_module.validate_credentials(str(valid_credentials_file))
        assert result is not None


# ---------------------------------------------------------------------------
# parse_scopes
# ---------------------------------------------------------------------------

class TestParseScopes:
    def test_single_scope(self, gapi_module):
        result = gapi_module.parse_scopes("gmail")
        assert any("gmail" in s for s in result)

    def test_multiple_scopes(self, gapi_module):
        result = gapi_module.parse_scopes("gmail,calendar")
        assert any("gmail" in s for s in result)
        assert any("calendar" in s for s in result)

    def test_direct_url_scope(self, gapi_module):
        result = gapi_module.parse_scopes("https://example.com/scope")
        assert "https://example.com/scope" in result

    def test_unknown_scope(self, gapi_module, capsys):
        result = gapi_module.parse_scopes("unknown_scope")
        captured = capsys.readouterr()
        assert "Unknown scope" in captured.out
        assert result == []

    def test_mixed_scopes(self, gapi_module):
        result = gapi_module.parse_scopes("gmail,https://custom.scope,drive")
        assert any("gmail" in s for s in result)
        assert any("drive" in s for s in result)
        assert "https://custom.scope" in result

    def test_with_spaces(self, gapi_module):
        result = gapi_module.parse_scopes(" gmail , calendar ")
        assert any("gmail" in s for s in result)

    def test_empty_string(self, gapi_module, capsys):
        result = gapi_module.parse_scopes("")
        # "" is unknown
        assert result == []

    def test_dedup(self, gapi_module):
        result = gapi_module.parse_scopes("gmail,gmail")
        # set() dedup ensures unique
        gmail_scopes = [s for s in result if "gmail" in s]
        assert len(gmail_scopes) == len(set(gmail_scopes))

    def test_all_known_scopes(self, gapi_module):
        result = gapi_module.parse_scopes("gmail,calendar,drive,sheets")
        assert len(result) > 0


# ---------------------------------------------------------------------------
# generate_mcp_config
# ---------------------------------------------------------------------------

class TestGenerateMcpConfig:
    def test_basic(self, gapi_module, tmp_path):
        scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        result = gapi_module.generate_mcp_config(
            str(tmp_path / "token.json"), scopes, str(tmp_path)
        )
        config_path = Path(result)
        assert config_path.exists()

        data = json.loads(config_path.read_text())
        assert "example_mcp_config" in data
        assert "gmail" in data["apis_enabled"]

    def test_no_matching_apis(self, gapi_module, tmp_path):
        scopes = ["https://custom.scope/test"]
        result = gapi_module.generate_mcp_config(
            str(tmp_path / "token.json"), scopes, str(tmp_path)
        )
        data = json.loads(Path(result).read_text())
        assert data["apis_enabled"] == []

    def test_multiple_apis(self, gapi_module, tmp_path):
        scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar",
        ]
        result = gapi_module.generate_mcp_config(
            str(tmp_path / "token.json"), scopes, str(tmp_path)
        )
        data = json.loads(Path(result).read_text())
        assert "gmail" in data["apis_enabled"]
        assert "calendar" in data["apis_enabled"]

    def test_output_dir_creation(self, gapi_module, tmp_path):
        scopes = []
        out_dir = tmp_path / "sub" / "dir"
        # generate_mcp_config does NOT create dirs, it expects them to exist
        out_dir.mkdir(parents=True)
        result = gapi_module.generate_mcp_config(
            str(tmp_path / "token.json"), scopes, str(out_dir)
        )
        assert Path(result).exists()


# ---------------------------------------------------------------------------
# refresh_token
# ---------------------------------------------------------------------------

class TestRefreshToken:
    def test_token_not_found(self, gapi_module, tmp_path):
        with pytest.raises(FileNotFoundError):
            gapi_module.refresh_token(
                str(tmp_path / "nonexistent_token.json"),
                str(tmp_path / "creds.json"),
            )

    def test_no_scopes_in_token(self, gapi_module, tmp_path, valid_credentials_file):
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "access_token",
            "refresh_token": "refresh",
        }))
        with pytest.raises(ValueError) as exc_info:
            gapi_module.refresh_token(str(token_path), str(valid_credentials_file))
        assert "scopes" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# CLI argparse
# ---------------------------------------------------------------------------

class TestCLIArgparse:
    def test_no_command(self, gapi_module):
        """コマンドなしはhelp表示とsys.exit"""
        with patch("sys.argv", ["google_api_setup.py"]):
            with pytest.raises(SystemExit):
                gapi_module.main()

    def test_validate_command(self, gapi_module, valid_credentials_file):
        with patch("sys.argv", [
            "google_api_setup.py", "validate",
            "--credentials", str(valid_credentials_file),
        ]):
            # Should not raise
            gapi_module.main()

    def test_validate_missing_file(self, gapi_module, tmp_path):
        with patch("sys.argv", [
            "google_api_setup.py", "validate",
            "--credentials", str(tmp_path / "nope.json"),
        ]):
            with pytest.raises(SystemExit):
                gapi_module.main()


# ---------------------------------------------------------------------------
# run_oauth_flow (lines 83-115)
# ---------------------------------------------------------------------------

class TestRunOauthFlow:
    def test_existing_valid_token(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 90-93, 112-114: existing valid token"""
        token_path = tmp_path / "token.json"
        token_path.write_text('{"token": "access"}', encoding="utf-8")

        mock_creds = MagicMock()
        mock_creds.valid = True

        with patch.object(
            gapi_module, "Credentials"
        ) as mock_creds_cls:
            mock_creds_cls.from_authorized_user_file.return_value = mock_creds
            result = gapi_module.run_oauth_flow(
                str(valid_credentials_file),
                ["https://www.googleapis.com/auth/gmail.readonly"],
                str(tmp_path),
            )
        assert result == str(token_path)

    def test_expired_token_refresh(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 95-97: expired token with refresh"""
        token_path = tmp_path / "token.json"
        token_path.write_text('{"token": "old"}', encoding="utf-8")

        mock_creds = MagicMock()
        mock_creds.valid = False
        mock_creds.expired = True
        mock_creds.refresh_token = "refresh_token_value"
        mock_creds.to_json.return_value = '{"token": "new"}'

        with patch.object(gapi_module, "Credentials") as mock_creds_cls, \
             patch.object(gapi_module, "Request") as mock_req:
            mock_creds_cls.from_authorized_user_file.return_value = mock_creds
            result = gapi_module.run_oauth_flow(
                str(valid_credentials_file),
                ["https://www.googleapis.com/auth/gmail.readonly"],
                str(tmp_path),
            )
        mock_creds.refresh.assert_called_once()
        assert result == str(token_path)

    def test_new_oauth_flow(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 99-106: new OAuth flow when no token exists"""
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = '{"token": "new"}'

        mock_flow = MagicMock()
        mock_flow.run_local_server.return_value = mock_creds

        with patch.object(gapi_module, "InstalledAppFlow") as mock_iaf:
            mock_iaf.from_client_secrets_file.return_value = mock_flow
            result = gapi_module.run_oauth_flow(
                str(valid_credentials_file),
                ["https://www.googleapis.com/auth/gmail.readonly"],
                str(tmp_path / "newdir"),
            )
        assert Path(result).name == "token.json"

    def test_output_dir_created(self, gapi_module, tmp_path, valid_credentials_file):
        """Line 85: output_dir.mkdir creates dirs"""
        mock_creds = MagicMock()
        mock_creds.to_json.return_value = '{"token": "t"}'
        mock_flow = MagicMock()
        mock_flow.run_local_server.return_value = mock_creds

        out_dir = tmp_path / "a" / "b" / "c"
        with patch.object(gapi_module, "InstalledAppFlow") as mock_iaf:
            mock_iaf.from_client_secrets_file.return_value = mock_flow
            gapi_module.run_oauth_flow(
                str(valid_credentials_file),
                ["https://www.googleapis.com/auth/gmail.readonly"],
                str(out_dir),
            )
        assert out_dir.exists()


# ---------------------------------------------------------------------------
# refresh_token advanced (lines 180-213)
# ---------------------------------------------------------------------------

class TestRefreshTokenAdvanced:
    def test_with_scopes_override(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 180-182: scopes_override provided"""
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "access",
            "refresh_token": "refresh",
            "client_id": "id",
            "client_secret": "secret",
            "token_uri": "https://oauth2.googleapis.com/token",
        }), encoding="utf-8")

        mock_creds = MagicMock()
        mock_creds.refresh_token = "refresh"
        mock_creds.to_json.return_value = '{"token": "refreshed"}'

        with patch.object(gapi_module, "Credentials") as mock_creds_cls, \
             patch.object(gapi_module, "Request"):
            mock_creds_cls.from_authorized_user_info.return_value = mock_creds
            result = gapi_module.refresh_token(
                str(token_path), str(valid_credentials_file), scopes_override="gmail"
            )
        assert result == str(token_path)

    def test_no_refresh_token(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 201-203: no refresh_token in creds"""
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "access",
            "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
            "client_id": "id",
            "client_secret": "secret",
            "token_uri": "https://oauth2.googleapis.com/token",
        }), encoding="utf-8")

        mock_creds = MagicMock()
        mock_creds.refresh_token = None

        with patch.object(gapi_module, "Credentials") as mock_creds_cls:
            mock_creds_cls.from_authorized_user_info.return_value = mock_creds
            with pytest.raises(ValueError, match="refresh_token"):
                gapi_module.refresh_token(str(token_path), str(valid_credentials_file))

    def test_missing_client_fields_补完(self, gapi_module, tmp_path, valid_credentials_file):
        """Lines 192-198: missing client_id etc filled from credentials.json"""
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "access",
            "refresh_token": "refresh",
            "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
        }), encoding="utf-8")

        mock_creds = MagicMock()
        mock_creds.refresh_token = "refresh"
        mock_creds.to_json.return_value = '{"token": "refreshed"}'

        with patch.object(gapi_module, "Credentials") as mock_creds_cls, \
             patch.object(gapi_module, "Request"):
            mock_creds_cls.from_authorized_user_info.return_value = mock_creds
            result = gapi_module.refresh_token(str(token_path), str(valid_credentials_file))
        assert result == str(token_path)

    def test_scopes_override_invalid(self, gapi_module, tmp_path, valid_credentials_file):
        """Line 182: invalid scopes_override raises ValueError"""
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "access",
            "refresh_token": "refresh",
            "client_id": "id",
            "client_secret": "secret",
            "token_uri": "uri",
        }), encoding="utf-8")

        with pytest.raises(ValueError, match="No valid scopes"):
            gapi_module.refresh_token(
                str(token_path), str(valid_credentials_file), scopes_override="invalid_scope_name"
            )


# ---------------------------------------------------------------------------
# main() advanced (lines 251-270)
# ---------------------------------------------------------------------------

class TestMainAdvanced:
    def test_auth_command(self, gapi_module, valid_credentials_file, tmp_path):
        """Lines 251-266: auth command"""
        mock_creds = MagicMock()
        mock_creds.valid = True

        with patch("sys.argv", [
            "google_api_setup.py", "auth",
            "--credentials", str(valid_credentials_file),
            "--scopes", "gmail",
            "--output", str(tmp_path),
        ]), patch.object(gapi_module, "run_oauth_flow", return_value=str(tmp_path / "token.json")), \
             patch.object(gapi_module, "generate_mcp_config", return_value=str(tmp_path / "mcp.json")):
            gapi_module.main()

    def test_auth_no_valid_scopes(self, gapi_module, valid_credentials_file, tmp_path):
        """Lines 254-256: auth with no valid scopes"""
        with patch("sys.argv", [
            "google_api_setup.py", "auth",
            "--credentials", str(valid_credentials_file),
            "--scopes", "invalid_scope",
        ]):
            with pytest.raises(SystemExit):
                gapi_module.main()

    def test_refresh_command(self, gapi_module, valid_credentials_file, tmp_path):
        """Lines 268-273: refresh command"""
        token_path = tmp_path / "token.json"
        token_path.write_text(json.dumps({
            "token": "a", "refresh_token": "r",
            "client_id": "c", "client_secret": "s",
            "token_uri": "u", "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
        }))
        mock_creds = MagicMock()
        mock_creds.refresh_token = "r"
        mock_creds.to_json.return_value = '{"token": "new"}'

        with patch("sys.argv", [
            "google_api_setup.py", "refresh",
            "--token", str(token_path),
            "--credentials", str(valid_credentials_file),
        ]), patch.object(gapi_module, "Credentials") as mc, \
             patch.object(gapi_module, "Request"):
            mc.from_authorized_user_info.return_value = mock_creds
            gapi_module.main()
