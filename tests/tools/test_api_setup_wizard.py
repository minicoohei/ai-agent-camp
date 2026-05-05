"""api_setup_wizard.py の単体テスト。

API設定確認・検証ロジックのテスト。外部API呼び出しはモックする。
"""

import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import argparse

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    """api_setup_wizard を runtime_env / credential_manager のモック込みでロード"""
    with patch.dict("sys.modules", {
        "runtime_env": MagicMock(load_runtime_env=MagicMock()),
        "credential_manager": MagicMock(
            store=MagicMock(return_value=True),
            get=MagicMock(return_value=None),
            _check_keyring=MagicMock(return_value=False),
        ),
    }):
        return import_module_from_repo("api_setup_wizard", "tools/api_setup_wizard.py")


# ===========================================================================
# SERVICES definition
# ===========================================================================

class TestServicesConfig:
    def test_all_services_present(self, mod):
        expected = {"google", "slack", "fal", "gemini", "heygen", "elevenlabs", "typefully"}
        assert set(mod.SERVICES.keys()) == expected

    def test_service_has_required_fields(self, mod):
        for sid, service in mod.SERVICES.items():
            assert "name" in service, f"{sid} missing name"
            assert "description" in service, f"{sid} missing description"
            assert "env_vars" in service, f"{sid} missing env_vars"
            assert "docs_url" in service, f"{sid} missing docs_url"

    def test_env_vars_have_name(self, mod):
        for sid, service in mod.SERVICES.items():
            for var in service["env_vars"]:
                assert "name" in var, f"{sid} env_var missing name"
                assert "description" in var
                assert "required" in var


# ===========================================================================
# check_env_var
# ===========================================================================

class TestCheckEnvVar:
    def test_found_long_key(self, mod, monkeypatch):
        monkeypatch.setenv("TEST_KEY", "abcdefghijklmnop")
        with patch.object(mod, "cred_get", return_value=None):
            exists, masked = mod.check_env_var("TEST_KEY")
        assert exists is True
        assert "abcd" in masked
        assert "mnop" in masked
        assert "env" in masked

    def test_found_short_key(self, mod, monkeypatch):
        monkeypatch.setenv("SHORT_KEY", "abc")
        with patch.object(mod, "cred_get", return_value=None):
            exists, masked = mod.check_env_var("SHORT_KEY")
        assert exists is True
        assert "***" in masked

    def test_not_found(self, mod, monkeypatch):
        monkeypatch.delenv("MISSING_KEY", raising=False)
        exists, masked = mod.check_env_var("MISSING_KEY")
        assert exists is False
        assert masked is None

    def test_credential_store_source(self, mod, monkeypatch):
        monkeypatch.setenv("CR_KEY", "credential_value_12345")
        with patch.object(mod, "cred_get", return_value="credential_value_12345"):
            exists, masked = mod.check_env_var("CR_KEY")
        assert exists is True
        assert "credential" in masked


# ===========================================================================
# check_token_file
# ===========================================================================

class TestCheckTokenFile:
    def test_valid_token(self, mod, tmp_path):
        token = {"token": "abc", "expiry": "2026-12-31T00:00:00Z"}
        (tmp_path / "token.json").write_text(json.dumps(token))
        with patch.object(mod, "ROOT_DIR", tmp_path):
            exists, info = mod.check_token_file("token.json")
        assert exists is True
        assert "2026-12-31" in info

    def test_invalid_json(self, mod, tmp_path):
        (tmp_path / "token.json").write_text("not json")
        with patch.object(mod, "ROOT_DIR", tmp_path):
            exists, info = mod.check_token_file("token.json")
        assert exists is True
        assert "parse error" in info

    def test_missing_file(self, mod, tmp_path):
        with patch.object(mod, "ROOT_DIR", tmp_path):
            exists, info = mod.check_token_file("token.json")
        assert exists is False
        assert info is None


# ===========================================================================
# _write_updates_to_dotenv
# ===========================================================================

class TestWriteUpdatesToDotenv:
    def test_create_new_env(self, mod, tmp_path):
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod._write_updates_to_dotenv([("KEY1", "value1"), ("KEY2", "value2")])
        env_path = tmp_path / ".env"
        assert env_path.exists()
        content = env_path.read_text()
        assert 'KEY1="value1"' in content
        assert 'KEY2="value2"' in content

    def test_update_existing(self, mod, tmp_path):
        (tmp_path / ".env").write_text('KEY1="old"\nKEY2="keep"\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            mod._write_updates_to_dotenv([("KEY1", "new")])
        content = (tmp_path / ".env").read_text()
        assert 'KEY1="new"' in content
        assert 'KEY2="keep"' in content
        assert "old" not in content

    def test_append_new_var(self, mod, tmp_path):
        (tmp_path / ".env").write_text('EXISTING="val"\n')
        with patch.object(mod, "ROOT_DIR", tmp_path):
            mod._write_updates_to_dotenv([("NEW_VAR", "new_val")])
        content = (tmp_path / ".env").read_text()
        assert 'EXISTING="val"' in content
        assert 'NEW_VAR="new_val"' in content

    def test_empty_updates(self, mod, tmp_path):
        with patch.object(mod, "ROOT_DIR", tmp_path):
            mod._write_updates_to_dotenv([])
        env_path = tmp_path / ".env"
        assert env_path.exists()
        assert env_path.read_text() == ""

    def test_file_permissions(self, mod, tmp_path):
        with patch.object(mod, "ROOT_DIR", tmp_path):
            mod._write_updates_to_dotenv([("K", "V")])
        env_path = tmp_path / ".env"
        mode = oct(env_path.stat().st_mode)[-3:]
        assert mode == "600"


# ===========================================================================
# validate_google_credentials
# ===========================================================================

class TestValidateGoogleCredentials:
    def test_no_credentials(self, mod, monkeypatch):
        monkeypatch.delenv("GCP_SA_KEY", raising=False)
        monkeypatch.delenv("GMAIL_ACCOUNTS_CONFIG", raising=False)
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["service_account"] is False
        assert result["oauth"] is False

    def test_valid_sa_key(self, mod, monkeypatch):
        sa_key = json.dumps({"type": "service_account", "project_id": "test", "client_email": "sa@test.iam.gserviceaccount.com"})
        monkeypatch.setenv("GCP_SA_KEY", sa_key)
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["service_account"] is True
        assert any("sa@test" in d for d in result["details"])

    def test_invalid_sa_key(self, mod, monkeypatch):
        monkeypatch.setenv("GCP_SA_KEY", "not valid json")
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["service_account"] is False
        assert any("Parse error" in d for d in result["details"])

    def test_oauth_token_exists(self, mod, tmp_path, monkeypatch):
        monkeypatch.delenv("GCP_SA_KEY", raising=False)
        monkeypatch.delenv("GMAIL_ACCOUNTS_CONFIG", raising=False)
        (tmp_path / "token.json").write_text(json.dumps({"expiry": "2026-12-31"}))
        with patch.object(mod, "ROOT_DIR", tmp_path):
            result = mod.validate_google_credentials()
        assert result["oauth"] is True

    def test_multi_gmail(self, mod, monkeypatch):
        monkeypatch.delenv("GCP_SA_KEY", raising=False)
        monkeypatch.setenv("GMAIL_ACCOUNTS_CONFIG", json.dumps({"accounts": [{"email": "a@b.com"}]}))
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["multi_gmail"] is True


# ===========================================================================
# validate_fal_api
# ===========================================================================

class TestValidateFalApi:
    def test_no_key(self, mod, monkeypatch):
        monkeypatch.delenv("FAL_KEY", raising=False)
        result = mod.validate_fal_api()
        assert result["valid"] is False

    def test_valid_key_prefix(self, mod, monkeypatch):
        monkeypatch.setenv("FAL_KEY", "fal_abcdefghijklmnop12345")
        result = mod.validate_fal_api()
        assert result["valid"] is True

    def test_valid_key_long(self, mod, monkeypatch):
        monkeypatch.setenv("FAL_KEY", "x" * 30)
        result = mod.validate_fal_api()
        assert result["valid"] is True

    def test_short_invalid_key(self, mod, monkeypatch):
        monkeypatch.setenv("FAL_KEY", "short")
        result = mod.validate_fal_api()
        assert result["valid"] is False


# ===========================================================================
# validate_gemini_api
# ===========================================================================

class TestValidateGeminiApi:
    def test_no_key(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        result = mod.validate_gemini_api()
        assert result["valid"] is False

    @patch("requests.get")
    def test_valid_key(self, mock_get, mod, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")
        mock_get.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"models": [{"name": "models/gemini-pro"}]})
        )
        result = mod.validate_gemini_api()
        assert result["valid"] is True

    @patch("requests.get")
    def test_invalid_key(self, mock_get, mod, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "bad_key")
        mock_get.return_value = MagicMock(status_code=401)
        result = mod.validate_gemini_api()
        assert result["valid"] is False


# ===========================================================================
# cmd_guide
# ===========================================================================

class TestCmdGuide:
    def test_known_service(self, mod, capsys):
        args = argparse.Namespace(service="google")
        mod.cmd_guide(args)
        captured = capsys.readouterr()
        assert "Google" in captured.out
        assert "OAuth" in captured.out

    def test_unknown_service(self, mod, capsys):
        args = argparse.Namespace(service="nonexistent")
        mod.cmd_guide(args)
        captured = capsys.readouterr()
        assert "Unknown service" in captured.out

    def test_all_services_have_guides(self, mod, capsys):
        for service_id in mod.SERVICES:
            args = argparse.Namespace(service=service_id)
            mod.cmd_guide(args)
            captured = capsys.readouterr()
            assert service_id in captured.out.lower() or mod.SERVICES[service_id]["name"] in captured.out


# ===========================================================================
# CLI parser
# ===========================================================================

class TestCliParser:
    def test_check_command(self, mod):
        """check コマンドのパース"""
        # main() はcheck_env_varなどを呼ぶのでcmd_checkをモックする
        with patch.object(mod, "cmd_check") as mock_check:
            with patch("sys.argv", ["prog", "check"]):
                mod.main()
            mock_check.assert_called_once()

    def test_guide_command(self, mod):
        with patch.object(mod, "cmd_guide") as mock_guide:
            with patch("sys.argv", ["prog", "guide", "google"]):
                mod.main()
            mock_guide.assert_called_once()
            args = mock_guide.call_args[0][0]
            assert args.service == "google"

    def test_setup_command(self, mod):
        with patch.object(mod, "cmd_setup") as mock_setup:
            with patch("sys.argv", ["prog", "setup", "gemini"]):
                mod.main()
            mock_setup.assert_called_once()
            args = mock_setup.call_args[0][0]
            assert args.service == "gemini"

    def test_no_command_defaults_to_check(self, mod):
        """No subcommand defaults to check"""
        with patch.object(mod, "cmd_check") as mock_check:
            with patch("sys.argv", ["prog"]):
                mod.main()
            mock_check.assert_called_once()


# ===========================================================================
# cmd_check
# ===========================================================================

class TestCmdCheck:
    def test_check_runs_without_error(self, mod, monkeypatch, capsys):
        """cmd_check executes end-to-end with no API keys"""
        for service in mod.SERVICES.values():
            for env_var in service.get("env_vars", []):
                monkeypatch.delenv(env_var["name"], raising=False)
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            args = argparse.Namespace()
            mod.cmd_check(args)
        output = capsys.readouterr().out
        assert "API 設定状況チェック" in output

    def test_check_with_keyring_enabled(self, mod, monkeypatch, capsys):
        """cmd_check shows credential store status when keyring available"""
        for service in mod.SERVICES.values():
            for env_var in service.get("env_vars", []):
                monkeypatch.delenv(env_var["name"], raising=False)
        with patch.object(mod, "_check_keyring", return_value=True):
            with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
                args = argparse.Namespace()
                mod.cmd_check(args)
        output = capsys.readouterr().out
        assert "Credential Store: 有効" in output


# ===========================================================================
# cmd_setup
# ===========================================================================

class TestCmdSetup:
    def test_setup_unknown_service(self, mod, capsys):
        args = argparse.Namespace(service="nonexistent", storage="credential-store")
        mod.cmd_setup(args)
        output = capsys.readouterr().out
        assert "Unknown service" in output

    def test_setup_no_keyring_with_credential_store(self, mod, capsys):
        """setup with credential-store storage but keyring unavailable"""
        with patch.object(mod, "_check_keyring", return_value=False):
            args = argparse.Namespace(service="gemini", storage="credential-store")
            mod.cmd_setup(args)
        output = capsys.readouterr().out
        assert "Credential Store が利用できません" in output

    def test_setup_with_dotenv_and_no_input(self, mod, capsys, monkeypatch):
        """setup with dotenv storage, user provides no input"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "_check_keyring", return_value=False):
            with patch("getpass.getpass", return_value=""):
                args = argparse.Namespace(service="gemini", storage="dotenv")
                mod.cmd_setup(args)
        output = capsys.readouterr().out
        assert "セットアップ完了" in output


# ===========================================================================
# validate_google_credentials: base64-encoded SA key
# ===========================================================================

class TestValidateGoogleBase64:
    def test_base64_encoded_sa_key(self, mod, monkeypatch):
        import base64
        sa_json = json.dumps({"type": "service_account", "project_id": "test", "client_email": "sa@test.iam"})
        encoded = base64.b64encode(sa_json.encode()).decode()
        monkeypatch.setenv("GCP_SA_KEY", encoded)
        monkeypatch.delenv("GMAIL_ACCOUNTS_CONFIG", raising=False)
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["service_account"] is True

    def test_gmail_config_parse_error(self, mod, monkeypatch):
        monkeypatch.delenv("GCP_SA_KEY", raising=False)
        monkeypatch.setenv("GMAIL_ACCOUNTS_CONFIG", "not json")
        with patch.object(mod, "ROOT_DIR", Path("/nonexistent")):
            result = mod.validate_google_credentials()
        assert result["multi_gmail"] is False
        assert any("parse error" in d for d in result["details"])
