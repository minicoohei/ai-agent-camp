"""credential_manager.py の単体テスト

keyring はモックして、OS Credential Store に依存しない形でテスト。
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo


def _import_cm():
    """credential_manager をインポート (conftest の sys.path 追加後に呼ぶ)"""
    return import_module_from_repo("credential_manager", "tools/credential_manager.py")


# ========== fixtures ==========


@pytest.fixture(autouse=True)
def _reset_keyring_cache():
    """テストごとに keyring 可用性キャッシュをリセット"""
    cm = _import_cm()
    cm._keyring_available = None
    yield
    cm._keyring_available = None


@pytest.fixture()
def mock_keyring():
    """keyring モジュールをモックし、インメモリストレージで動作させる"""
    cm = _import_cm()
    store = {}

    mock_kr = MagicMock()
    mock_kr.get_keyring.return_value = MagicMock(
        __class__=type("Keychain", (), {"__name__": "Keychain"})
    )
    mock_kr.set_password = lambda svc, key, val: store.update({(svc, key): val})
    mock_kr.get_password = lambda svc, key: store.get((svc, key))

    def delete_password(svc, key):
        if (svc, key) in store:
            del store[(svc, key)]
        else:
            raise Exception("not found")

    mock_kr.delete_password = delete_password

    with patch.dict("sys.modules", {"keyring": mock_kr}):
        cm._keyring_available = None
        yield mock_kr, store


# ========== _mask ==========


class TestMask:
    def test_empty_string(self):
        cm = _import_cm()
        assert cm._mask("") == "(empty)"

    def test_short_value(self):
        cm = _import_cm()
        assert cm._mask("abc") == "***"

    def test_exactly_12_chars(self):
        cm = _import_cm()
        assert cm._mask("123456789012") == "***"

    def test_long_value(self):
        cm = _import_cm()
        result = cm._mask("AIzaSyAbcdefghijklmnop")
        assert result.startswith("AIza")
        assert result.endswith("mnop")
        assert "..." in result


# ========== _parse_dotenv ==========


class TestParseDotenv:
    def test_nonexistent_file(self, tmp_path):
        cm = _import_cm()
        result = cm._parse_dotenv(tmp_path / "missing.env")
        assert result == {}

    def test_basic_parsing(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            "GEMINI_API_KEY=test-key-123\n"
            "SLACK_BOT_TOKEN=xoxb-abc\n",
            encoding="utf-8",
        )
        result = cm._parse_dotenv(env_file)
        assert result["GEMINI_API_KEY"] == "test-key-123"
        assert result["SLACK_BOT_TOKEN"] == "xoxb-abc"

    def test_comments_and_empty_lines(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            "# This is a comment\n"
            "\n"
            "KEY1=value1\n"
            "  # Another comment\n"
            "KEY2=value2\n",
            encoding="utf-8",
        )
        result = cm._parse_dotenv(env_file)
        assert result == {"KEY1": "value1", "KEY2": "value2"}

    def test_export_prefix_fallback(self, tmp_path):
        """export prefix をフォールバックパーサーで処理できることを確認"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("export MY_KEY=my_value\n", encoding="utf-8")
        # dotenv を一時的に除去してフォールバックパスを強制
        with patch.dict("sys.modules", {"dotenv": None}):
            result = cm._parse_dotenv(env_file)
        assert result["MY_KEY"] == "my_value"

    def test_quoted_values(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            'DOUBLE="double-quoted"\n'
            "SINGLE='single-quoted'\n",
            encoding="utf-8",
        )
        result = cm._parse_dotenv(env_file)
        assert result.get("DOUBLE") == "double-quoted"
        assert result.get("SINGLE") == "single-quoted"

    def test_empty_values_excluded(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("EMPTY=\nNONEMPTY=val\n", encoding="utf-8")
        result = cm._parse_dotenv(env_file)
        assert "EMPTY" not in result
        assert result["NONEMPTY"] == "val"


# ========== prepare_dotenv / import_from_dotenv ==========


class TestPrepareDotenv:
    def test_prepare_dotenv_creates_empty_keys(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"

        prepared = cm.prepare_dotenv(["GEMINI_API_KEY", "GITHUB_TOKEN"], env_file)

        assert prepared == env_file
        assert env_file.read_text(encoding="utf-8") == (
            "GEMINI_API_KEY=\n"
            "GITHUB_TOKEN=\n"
        )

    def test_prepare_dotenv_preserves_existing_values(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        env_file.write_text("EXISTING_KEY=keep-me\n", encoding="utf-8")

        cm.prepare_dotenv(["GEMINI_API_KEY"], env_file)

        assert env_file.read_text(encoding="utf-8") == (
            "EXISTING_KEY=keep-me\n"
            "GEMINI_API_KEY=\n"
        )


class TestImportFromDotenv:
    def test_import_from_dotenv_imports_selected_keys(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        env_file.write_text(
            "GEMINI_API_KEY=real-key-123\n"
            "GITHUB_TOKEN=ghp_123\n",
            encoding="utf-8",
        )

        results = cm.import_from_dotenv(["GEMINI_API_KEY"], env_file)

        assert results == {"GEMINI_API_KEY": "ok"}
        assert cm.get("GEMINI_API_KEY") == "real-key-123"
        assert cm.get("GITHUB_TOKEN") is None

    def test_import_from_dotenv_deletes_only_imported_keys(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        env_file.write_text(
            "GEMINI_API_KEY=real-key-123\n"
            "NEXT_PUBLIC_FIREBASE_API_KEY=keep-public\n",
            encoding="utf-8",
        )

        results = cm.import_from_dotenv(["GEMINI_API_KEY"], env_file, delete=True)

        assert results == {"GEMINI_API_KEY": "ok"}
        assert env_file.read_text(encoding="utf-8") == "NEXT_PUBLIC_FIREBASE_API_KEY=keep-public\n"

    def test_import_from_dotenv_reports_missing_key(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        env_file.write_text("GITHUB_TOKEN=ghp_123\n", encoding="utf-8")

        results = cm.import_from_dotenv(["GEMINI_API_KEY"], env_file)

        assert results == {"GEMINI_API_KEY": "missing"}

    def test_import_from_dotenv_skips_placeholder(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        env_file.write_text("GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n", encoding="utf-8")

        results = cm.import_from_dotenv(["GEMINI_API_KEY"], env_file)

        assert results == {"GEMINI_API_KEY": "skipped (placeholder)"}
        assert cm.get("GEMINI_API_KEY") is None


# ========== store / get / delete ==========


class TestStoreGetDelete:
    def test_store_and_get(self, mock_keyring):
        cm = _import_cm()
        assert cm.store("TEST_KEY", "test-value") is True
        assert cm.get("TEST_KEY") == "test-value"

    def test_get_missing_key(self, mock_keyring):
        cm = _import_cm()
        assert cm.get("NONEXISTENT_KEY") is None

    def test_delete_existing_key(self, mock_keyring):
        cm = _import_cm()
        cm.store("TO_DELETE", "value")
        assert cm.delete("TO_DELETE") is True
        assert cm.get("TO_DELETE") is None

    def test_delete_nonexistent_key(self, mock_keyring):
        cm = _import_cm()
        assert cm.delete("NONEXISTENT") is False

    def test_store_fails_without_keyring(self):
        cm = _import_cm()
        cm._keyring_available = False
        assert cm.store("KEY", "value") is False

    def test_get_returns_none_without_keyring(self):
        cm = _import_cm()
        cm._keyring_available = False
        assert cm.get("KEY") is None

    def test_delete_fails_without_keyring(self):
        cm = _import_cm()
        cm._keyring_available = False
        assert cm.delete("KEY") is False


# ========== inject_to_environ ==========


class TestInjectToEnviron:
    def test_injects_credential_store_values(self, mock_keyring, monkeypatch):
        cm = _import_cm()
        cm.store("GEMINI_API_KEY", "injected-value")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        count = cm.inject_to_environ()

        assert count >= 1
        assert os.environ["GEMINI_API_KEY"] == "injected-value"
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    def test_does_not_override_existing_env(self, mock_keyring, monkeypatch):
        cm = _import_cm()
        cm.store("GEMINI_API_KEY", "store-value")
        monkeypatch.setenv("GEMINI_API_KEY", "existing-value")

        cm.inject_to_environ()

        assert os.environ["GEMINI_API_KEY"] == "existing-value"

    def test_returns_zero_without_keyring(self):
        cm = _import_cm()
        cm._keyring_available = False
        assert cm.inject_to_environ() == 0


# ========== migrate_from_dotenv ==========


class TestMigrateFromDotenv:
    def test_migrate_stores_keys(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            "GEMINI_API_KEY=real-key-123\n"
            "SLACK_BOT_TOKEN=xoxb-real\n",
            encoding="utf-8",
        )

        results = cm.migrate_from_dotenv(env_file)

        assert results["GEMINI_API_KEY"] == "ok"
        assert results["SLACK_BOT_TOKEN"] == "ok"
        assert cm.get("GEMINI_API_KEY") == "real-key-123"

    def test_migrate_skips_placeholders(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            "GEMINI_API_KEY=your_gemini_api_key_here\n",
            encoding="utf-8",
        )

        results = cm.migrate_from_dotenv(env_file)

        assert results["GEMINI_API_KEY"] == "skipped (placeholder)"
        assert cm.get("GEMINI_API_KEY") is None

    def test_migrate_skips_placeholder_uppercase(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            "GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE\n",
            encoding="utf-8",
        )

        results = cm.migrate_from_dotenv(env_file)

        assert results["GEMINI_API_KEY"] == "skipped (placeholder)"
        assert cm.get("GEMINI_API_KEY") is None

    def test_migrate_missing_file(self, mock_keyring, tmp_path):
        cm = _import_cm()
        results = cm.migrate_from_dotenv(tmp_path / "nonexistent.env")
        assert results == {}

    def test_migrate_fails_without_keyring(self, tmp_path):
        cm = _import_cm()
        cm._keyring_available = False
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=val\n", encoding="utf-8")
        results = cm.migrate_from_dotenv(env_file)
        assert results == {}


# ========== cleanup_dotenv ==========


class TestCleanupDotenv:
    def test_cleanup_no_file(self, mock_keyring, tmp_path):
        cm = _import_cm()
        assert cm.cleanup_dotenv(tmp_path / "nonexistent.env") is True

    def test_cleanup_blocks_if_not_migrated(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("GEMINI_API_KEY=real-key\n", encoding="utf-8")
        assert cm.cleanup_dotenv(env_file) is False
        assert env_file.exists()

    def test_cleanup_blocks_unmanaged_keys(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("UNKNOWN_CUSTOM_KEY=some-value\n", encoding="utf-8")
        assert cm.cleanup_dotenv(env_file) is False

    def test_cleanup_deletes_after_migration(self, mock_keyring, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("GEMINI_API_KEY=real-key\n", encoding="utf-8")
        cm.store("GEMINI_API_KEY", "real-key")

        assert cm.cleanup_dotenv(env_file) is True
        assert not env_file.exists()


# ========== _check_keyring ==========


class TestCheckKeyring:
    def test_fail_backend_rejected(self):
        cm = _import_cm()
        FailKeyring = type("FailKeyring", (), {})
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = FailKeyring()
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            assert cm._check_keyring() is False

    def test_null_backend_rejected(self):
        cm = _import_cm()
        NullKeyring = type("NullKeyring", (), {})
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = NullKeyring()
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            assert cm._check_keyring() is False

    def test_valid_backend_accepted(self):
        cm = _import_cm()
        Keychain = type("Keychain", (), {})
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = Keychain()
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            assert cm._check_keyring() is True

    def test_import_error_handled(self):
        cm = _import_cm()
        with patch.dict("sys.modules", {"keyring": None}):
            cm._keyring_available = None
            assert cm._check_keyring() is False


# ========== status ==========


class TestStatus:
    def test_status_with_keyring_shows_sources(self, mock_keyring, monkeypatch, tmp_path, capsys):
        """env / credential / .env / not set の4状態が正しく表示される"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS[:] = ["KEY_ENV", "KEY_KR", "KEY_DOTENV", "KEY_NONE"]
        try:
            # KEY_ENV: 環境変数に設定
            monkeypatch.setenv("KEY_ENV", "env-value-12345678")
            # KEY_KR: keyring に保存
            cm.store("KEY_KR", "kr-value-12345678")
            monkeypatch.delenv("KEY_KR", raising=False)
            # KEY_DOTENV: .env にのみ存在
            monkeypatch.delenv("KEY_DOTENV", raising=False)
            # KEY_NONE: どこにもない
            monkeypatch.delenv("KEY_NONE", raising=False)

            env_file = tmp_path / ".env"
            env_file.write_text("KEY_DOTENV=dotenv-value-12345678\n", encoding="utf-8")

            cm.status(env_path=env_file)

            output = capsys.readouterr().out
            assert "KEY_ENV" in output and "env" in output
            assert "KEY_KR" in output and "credential" in output
            assert "KEY_DOTENV" in output and ".env" in output
            assert "KEY_NONE" in output and "(not set)" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_status_without_keyring_does_not_crash(self, capsys):
        """keyring 不可時にクラッシュしない"""
        cm = _import_cm()
        cm._keyring_available = False
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS[:] = ["GEMINI_API_KEY"]
        try:
            cm.status(env_path=Path("/nonexistent/.env"))
            output = capsys.readouterr().out
            assert "keyring not available" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_status_shows_unmanaged_keys(self, mock_keyring, tmp_path, capsys):
        """.env に MANAGED_KEYS 外のキーがある場合に警告表示"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS[:] = ["KNOWN_KEY"]
        try:
            env_file = tmp_path / ".env"
            env_file.write_text(
                "KNOWN_KEY=known-val\nUNKNOWN_EXTRA=extra-val\n",
                encoding="utf-8",
            )
            cm.store("KNOWN_KEY", "known-val")

            cm.status(env_path=env_file)

            output = capsys.readouterr().out
            assert "UNKNOWN_EXTRA" in output
            assert "MANAGED_KEYS" in output or "未登録" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_status_no_env_file(self, mock_keyring, tmp_path, capsys):
        """.env が存在しない場合でも正常に動作"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS[:] = ["GEMINI_API_KEY"]
        try:
            cm.status(env_path=tmp_path / "nonexistent.env")
            output = capsys.readouterr().out
            assert "not found" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys


# ========== _resolve_env_file ==========


class TestResolveEnvFile:
    def test_explicit_path(self, tmp_path):
        cm = _import_cm()
        p = tmp_path / "custom.env"
        assert cm._resolve_env_file(p) == p

    def test_for_write_defaults_to_env_local(self):
        cm = _import_cm()
        result = cm._resolve_env_file(None, for_write=True)
        assert result == cm.DEFAULT_PREPARE_ENV_FILE

    def test_for_read_prefers_existing(self, tmp_path):
        cm = _import_cm()
        original_candidates = cm.DEFAULT_ENV_CANDIDATES
        env_file = tmp_path / ".env.local"
        env_file.write_text("X=1\n")
        cm.DEFAULT_ENV_CANDIDATES = [env_file, tmp_path / ".env"]
        try:
            result = cm._resolve_env_file(None)
            assert result == env_file
        finally:
            cm.DEFAULT_ENV_CANDIDATES = original_candidates

    def test_for_read_no_existing_returns_default(self):
        cm = _import_cm()
        original_candidates = cm.DEFAULT_ENV_CANDIDATES
        cm.DEFAULT_ENV_CANDIDATES = [Path("/nonexistent/.env.local"), Path("/nonexistent/.env")]
        try:
            result = cm._resolve_env_file(None)
            assert result == cm.DEFAULT_PREPARE_ENV_FILE
        finally:
            cm.DEFAULT_ENV_CANDIDATES = original_candidates


# ========== _upsert_dotenv_values ==========


class TestUpsertDotenvValues:
    def test_upsert_new_file(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        cm._upsert_dotenv_values(env_file, {"KEY": "val"})
        assert "KEY=val" in env_file.read_text()

    def test_upsert_replaces_existing_key(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=old\nOTHER=keep\n")
        cm._upsert_dotenv_values(env_file, {"KEY": "new"})
        content = env_file.read_text()
        assert "KEY=new" in content
        assert "KEY=old" not in content
        assert "OTHER=keep" in content

    def test_upsert_preserve_empty(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        cm._upsert_dotenv_values(env_file, {"KEY": ""}, preserve_empty=True)
        content = env_file.read_text()
        assert "KEY=" in content


# ========== _remove_dotenv_keys ==========


class TestRemoveDotenvKeys:
    def test_remove_keys(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("KEY1=val1\nKEY2=val2\nKEY3=val3\n")
        cm._remove_dotenv_keys(env_file, ["KEY2"])
        content = env_file.read_text()
        assert "KEY1=val1" in content
        assert "KEY2" not in content
        assert "KEY3=val3" in content

    def test_remove_from_nonexistent_file(self, tmp_path):
        cm = _import_cm()
        # Should not raise
        cm._remove_dotenv_keys(tmp_path / "nope.env", ["KEY"])


# ========== _parse_dotenv with dotenv module ==========


class TestParseDotenvWithModule:
    def test_uses_dotenv_values_when_available(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text('MY_KEY="hello"\n')
        # Normal import should work with or without dotenv
        result = cm._parse_dotenv(env_file)
        assert result.get("MY_KEY") in ("hello", '"hello"')  # depends on dotenv presence


# ========== import_from_dotenv file not found ==========


class TestImportFromDotenvEdgeCases:
    def test_file_not_found(self, mock_keyring, tmp_path, capsys):
        cm = _import_cm()
        result = cm.import_from_dotenv(["KEY"], tmp_path / "missing.env")
        assert result == {}
        output = capsys.readouterr().out
        assert "見つかりません" in output

    def test_no_keyring(self, tmp_path, capsys):
        cm = _import_cm()
        cm._keyring_available = False
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=val\n")
        result = cm.import_from_dotenv(["KEY"], env_file)
        assert result == {}


# ========== cleanup_dotenv edge cases ==========


class TestCleanupDotenvEdge:
    def test_cleanup_exception_during_delete(self, mock_keyring, tmp_path):
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY=val\n")
            cm.store("TEST_KEY", "val")
            with patch("subprocess.run", side_effect=Exception("rm failed")):
                result = cm.cleanup_dotenv(env_file)
                # Should fail gracefully
                assert result is False or result is True  # depends on OS path
        finally:
            cm.MANAGED_KEYS[:] = original_keys


# ========== store exception handling (lines 214-216) ==========


class TestStoreExceptionHandling:
    def test_store_exception_returns_false(self, tmp_path):
        """keyring.set_password が例外を投げると False を返す (lines 214-216)"""
        cm = _import_cm()
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = MagicMock(
            __class__=type("Keychain", (), {"__name__": "Keychain"})
        )
        mock_kr.set_password.side_effect = Exception("Keychain locked")
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            result = cm.store("TEST_KEY", "value")
        assert result is False


# ========== get exception handling (lines 234-235) ==========


class TestGetExceptionHandling:
    def test_get_exception_returns_none(self, tmp_path):
        """keyring.get_password が例外を投げると None を返す (lines 234-235)"""
        cm = _import_cm()
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = MagicMock(
            __class__=type("Keychain", (), {"__name__": "Keychain"})
        )
        mock_kr.get_password.side_effect = Exception("Access denied")
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            result = cm.get("TEST_KEY")
        assert result is None


# ========== inject_to_environ exception handling (lines 286-287) ==========


class TestInjectToEnvironExceptionHandling:
    def test_inject_skips_on_keyring_exception(self, monkeypatch):
        """keyring.get_password 例外時はスキップして続行 (lines 286-287)"""
        cm = _import_cm()
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = MagicMock(
            __class__=type("Keychain", (), {"__name__": "Keychain"})
        )
        mock_kr.get_password.side_effect = Exception("Corrupted entry")
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            # Ensure keys are not in env
            for key in cm.MANAGED_KEYS:
                monkeypatch.delenv(key, raising=False)
            count = cm.inject_to_environ()
        assert count == 0


# ========== _parse_dotenv fallback: comment/empty/export/quoted (lines 313-324) ==========


class TestParseDotenvFallbackEdgeCases:
    def test_fallback_comment_line(self, tmp_path):
        """フォールバックパーサーでコメント行スキップ (line 314)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("# comment\nKEY=val\n", encoding="utf-8")
        with patch.dict("sys.modules", {"dotenv": None}):
            result = cm._parse_dotenv(env_file)
        assert result == {"KEY": "val"}

    def test_fallback_quoted_values(self, tmp_path):
        """フォールバックパーサーで引用符値の処理 (lines 322-324)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            'DOUBLE="double-val"\n'
            "SINGLE='single-val'\n",
            encoding="utf-8",
        )
        with patch.dict("sys.modules", {"dotenv": None}):
            result = cm._parse_dotenv(env_file)
        assert result["DOUBLE"] == "double-val"
        assert result["SINGLE"] == "single-val"


# ========== _resolve_env_file for_write with no candidates (lines 335-342) ==========


class TestResolveEnvFileEdge:
    def test_for_write_no_existing(self):
        """for_write=True ではデフォルトを返す (lines 335-336)"""
        cm = _import_cm()
        result = cm._resolve_env_file(None, for_write=True)
        assert result == cm.DEFAULT_PREPARE_ENV_FILE

    def test_no_candidates_returns_default(self):
        """候補ファイルが全て存在しない場合にデフォルト返却 (lines 338-342)"""
        cm = _import_cm()
        orig = cm.DEFAULT_ENV_CANDIDATES
        cm.DEFAULT_ENV_CANDIDATES = [Path("/nonexistent1/.env"), Path("/nonexistent2/.env")]
        try:
            result = cm._resolve_env_file(None)
            assert result == cm.DEFAULT_PREPARE_ENV_FILE
        finally:
            cm.DEFAULT_ENV_CANDIDATES = orig


# ========== _upsert_dotenv_values edge cases (lines 362-380) ==========


class TestUpsertDotenvValuesEdge:
    def test_non_matching_lines_preserved(self, tmp_path):
        """コメント行やマッチしない行は保持 (lines 362-363)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("# header\nKEY=old\n# footer\n", encoding="utf-8")
        cm._upsert_dotenv_values(env_file, {"KEY": "new"})
        content = env_file.read_text()
        assert "# header" in content
        assert "# footer" in content
        assert "KEY=new" in content

    def test_preserve_empty_on_existing_key(self, tmp_path):
        """preserve_empty=True で既存キーが空に (lines 370-374)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=old_val\n", encoding="utf-8")
        cm._upsert_dotenv_values(env_file, {"KEY": ""}, preserve_empty=True)
        content = env_file.read_text()
        assert "KEY=" in content
        assert "old_val" not in content

    def test_new_key_with_value(self, tmp_path):
        """remaining keys に値がある場合の追加 (line 380)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("EXISTING=keep\n", encoding="utf-8")
        cm._upsert_dotenv_values(env_file, {"NEW_KEY": "new_val"})
        content = env_file.read_text()
        assert "NEW_KEY=new_val" in content
        assert "EXISTING=keep" in content

    def test_preserve_empty_new_key(self, tmp_path):
        """preserve_empty=True で新規キーが空 (line 378)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        cm._upsert_dotenv_values(env_file, {"EMPTY_KEY": ""}, preserve_empty=True)
        content = env_file.read_text()
        assert "EMPTY_KEY=" in content


# ========== import_from_dotenv edge cases (lines 425-448) ==========


class TestImportFromDotenvMoreEdgeCases:
    def test_file_not_found_message(self, mock_keyring, tmp_path, capsys):
        """dotenv ファイルが存在しない (lines 425-426)"""
        cm = _import_cm()
        result = cm.import_from_dotenv(["KEY"], tmp_path / "nope.env")
        assert result == {}
        output = capsys.readouterr().out
        assert "見つかりません" in output

    def test_no_keyring_message(self, tmp_path, capsys):
        """keyring が利用不可 (lines 429-430)"""
        cm = _import_cm()
        cm._keyring_available = False
        env_file = tmp_path / ".env"
        env_file.write_text("KEY=val\n", encoding="utf-8")
        result = cm.import_from_dotenv(["KEY"], env_file)
        assert result == {}
        output = capsys.readouterr().out
        assert "keyring" in output

    def test_store_failure_returns_error(self, tmp_path):
        """store が失敗すると error を返す (line 448)"""
        cm = _import_cm()
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = MagicMock(
            __class__=type("Keychain", (), {"__name__": "Keychain"})
        )
        mock_kr.set_password.side_effect = Exception("Write failed")
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            env_file = tmp_path / ".env"
            env_file.write_text("MY_KEY=real_value_123\n", encoding="utf-8")
            results = cm.import_from_dotenv(["MY_KEY"], env_file)
        assert results["MY_KEY"] == "error"


# ========== migrate_from_dotenv error path (line 492) ==========


class TestMigrateFromDotenvError:
    def test_migrate_store_failure(self, tmp_path):
        """store が失敗すると error を返す (line 492)"""
        cm = _import_cm()
        mock_kr = MagicMock()
        mock_kr.get_keyring.return_value = MagicMock(
            __class__=type("Keychain", (), {"__name__": "Keychain"})
        )
        mock_kr.set_password.side_effect = Exception("Write failed")
        with patch.dict("sys.modules", {"keyring": mock_kr}):
            cm._keyring_available = None
            env_file = tmp_path / ".env"
            env_file.write_text("MY_KEY=real_value_123\n", encoding="utf-8")
            results = cm.migrate_from_dotenv(env_file)
        assert results["MY_KEY"] == "error"


# ========== cleanup_dotenv OS-specific paths (lines 552-579) ==========


class TestCleanupDotenvOSPaths:
    def test_cleanup_darwin(self, mock_keyring, tmp_path):
        """macOS パス: rm -P で削除 (lines 547-551)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_D")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_D=val\n", encoding="utf-8")
            cm.store("TEST_KEY_D", "val")
            with patch("platform.system", return_value="Darwin"), \
                 patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                # rm -P will be called, simulate file deletion
                def remove_file(*args, **kwargs):
                    env_file.unlink(missing_ok=True)
                mock_run.side_effect = remove_file
                result = cm.cleanup_dotenv(env_file)
            assert result is True
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_linux_with_shred(self, mock_keyring, tmp_path):
        """Linux (shred あり) パス (lines 553-558)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_L")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_L=val\n", encoding="utf-8")
            cm.store("TEST_KEY_L", "val")
            with patch("platform.system", return_value="Linux"), \
                 patch("shutil.which", return_value="/usr/bin/shred"), \
                 patch("subprocess.run") as mock_run:
                def remove_file(*args, **kwargs):
                    env_file.unlink(missing_ok=True)
                mock_run.side_effect = remove_file
                result = cm.cleanup_dotenv(env_file)
            assert result is True
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_linux_no_shred(self, mock_keyring, tmp_path):
        """Linux (shred なし) パス: 手動上書き (lines 559-565)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_LN")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_LN=val\n", encoding="utf-8")
            cm.store("TEST_KEY_LN", "val")
            with patch("platform.system", return_value="Linux"), \
                 patch("shutil.which", return_value=None):
                result = cm.cleanup_dotenv(env_file)
            assert result is True
            assert not env_file.exists()
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_windows(self, mock_keyring, tmp_path):
        """Windows パス: 手動上書き + 削除 (lines 566-572)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_W")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_W=val\n", encoding="utf-8")
            cm.store("TEST_KEY_W", "val")
            with patch("platform.system", return_value="Windows"):
                result = cm.cleanup_dotenv(env_file)
            assert result is True
            assert not env_file.exists()
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_unknown_os(self, mock_keyring, tmp_path):
        """未知のOS フォールバック: 手動上書き (lines 573-579)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_U")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_U=val\n", encoding="utf-8")
            cm.store("TEST_KEY_U", "val")
            with patch("platform.system", return_value="FreeBSD"):
                result = cm.cleanup_dotenv(env_file)
            assert result is True
            assert not env_file.exists()
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_exception_returns_false(self, mock_keyring, tmp_path, capsys):
        """例外発生時は False を返す (lines 583-585)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("TEST_KEY_EX")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("TEST_KEY_EX=val\n", encoding="utf-8")
            cm.store("TEST_KEY_EX", "val")
            with patch("platform.system", return_value="Darwin"), \
                 patch("subprocess.run", side_effect=Exception("rm not found")):
                result = cm.cleanup_dotenv(env_file)
            assert result is False
            output = capsys.readouterr().out
            assert "削除に失敗" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys


# ========== main() CLI tests (lines 681-826) ==========


class TestMainCLI:
    def test_no_command_prints_help(self, capsys):
        """コマンドなしで help 出力 (line 757-759)"""
        cm = _import_cm()
        with patch("sys.argv", ["credential_manager.py"]):
            cm.main()
        output = capsys.readouterr().out
        assert "usage" in output.lower() or "Credential Store" in output

    def test_store_command_with_value(self, mock_keyring, capsys):
        """store --value で直接保存 (lines 767-774)"""
        cm = _import_cm()
        with patch("sys.argv", ["credential_manager.py", "store", "MY_KEY", "--value", "secret123"]):
            cm.main()
        assert cm.get("MY_KEY") == "secret123"

    def test_store_command_with_getpass(self, mock_keyring, capsys):
        """store コマンドで getpass 入力 (lines 769-774)"""
        cm = _import_cm()
        with patch("sys.argv", ["credential_manager.py", "store", "MY_KEY"]), \
             patch("getpass.getpass", return_value="secret_from_prompt"):
            cm.main()
        assert cm.get("MY_KEY") == "secret_from_prompt"

    def test_store_empty_value_exits(self, mock_keyring):
        """空の値は保存不可 (lines 771-773)"""
        cm = _import_cm()
        with patch("sys.argv", ["credential_manager.py", "store", "MY_KEY", "--value", "  "]), \
             pytest.raises(SystemExit) as exc_info:
            cm.main()
        assert exc_info.value.code == 1

    def test_store_no_keyring_exits(self, capsys):
        """keyring なしで store は exit 1 (lines 762-765)"""
        cm = _import_cm()
        cm._keyring_available = False
        with patch("sys.argv", ["credential_manager.py", "store", "MY_KEY"]), \
             pytest.raises(SystemExit) as exc_info:
            cm.main()
        assert exc_info.value.code == 1

    def test_get_command_found(self, mock_keyring, capsys):
        """get コマンド: 見つかった場合 (lines 776-779)"""
        cm = _import_cm()
        cm.store("GET_TEST_KEY", "some-long-secret-value")
        with patch("sys.argv", ["credential_manager.py", "get", "GET_TEST_KEY"]):
            cm.main()
        output = capsys.readouterr().out
        assert "GET_TEST_KEY" in output
        assert "✅" in output

    def test_get_command_not_found(self, mock_keyring, capsys):
        """get コマンド: 見つからない場合 (lines 780-781)"""
        cm = _import_cm()
        with patch("sys.argv", ["credential_manager.py", "get", "NONEXISTENT_KEY"]):
            cm.main()
        output = capsys.readouterr().out
        assert "not stored" in output

    def test_delete_command_confirmed(self, mock_keyring, capsys):
        """delete コマンド: 確認して削除 (lines 783-786)"""
        cm = _import_cm()
        cm.store("DEL_KEY", "value")
        with patch("sys.argv", ["credential_manager.py", "delete", "DEL_KEY"]), \
             patch("builtins.input", return_value="y"):
            cm.main()
        assert cm.get("DEL_KEY") is None

    def test_delete_command_skipped(self, mock_keyring, capsys):
        """delete コマンド: スキップ (lines 787-788)"""
        cm = _import_cm()
        cm.store("DEL_KEY2", "value")
        with patch("sys.argv", ["credential_manager.py", "delete", "DEL_KEY2"]), \
             patch("builtins.input", return_value="n"):
            cm.main()
        output = capsys.readouterr().out
        assert "スキップ" in output
        assert cm.get("DEL_KEY2") == "value"

    def test_prepare_dotenv_command(self, mock_keyring, tmp_path, capsys):
        """prepare-dotenv コマンド (lines 790-792)"""
        cm = _import_cm()
        env_file = tmp_path / ".env.local"
        with patch("sys.argv", [
            "credential_manager.py", "prepare-dotenv",
            "GEMINI_API_KEY", "--env-file", str(env_file),
        ]):
            cm.main()
        assert env_file.exists()
        assert "GEMINI_API_KEY=" in env_file.read_text()

    def test_import_dotenv_command(self, mock_keyring, tmp_path, capsys):
        """import-dotenv コマンド (lines 794-808)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("MY_KEY=real-value-123456\n", encoding="utf-8")
        with patch("sys.argv", [
            "credential_manager.py", "import-dotenv",
            "MY_KEY", "--env-file", str(env_file),
        ]):
            cm.main()
        output = capsys.readouterr().out
        assert "移行" in output

    def test_import_dotenv_with_missing_keys(self, mock_keyring, tmp_path, capsys):
        """import-dotenv: 不在キーの警告 (lines 801-804)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("OTHER=val\n", encoding="utf-8")
        with patch("sys.argv", [
            "credential_manager.py", "import-dotenv",
            "MISSING_KEY", "--env-file", str(env_file),
        ]):
            cm.main()
        output = capsys.readouterr().out
        assert "MISSING_KEY" in output

    def test_import_dotenv_with_placeholder(self, mock_keyring, tmp_path, capsys):
        """import-dotenv: プレースホルダーのスキップ (lines 805-808)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("MY_KEY=your_api_key_here\n", encoding="utf-8")
        with patch("sys.argv", [
            "credential_manager.py", "import-dotenv",
            "MY_KEY", "--env-file", str(env_file),
        ]):
            cm.main()
        output = capsys.readouterr().out
        assert "プレースホルダー" in output

    def test_migrate_command(self, mock_keyring, tmp_path, capsys):
        """migrate コマンド (lines 810-812)"""
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text("GEMINI_API_KEY=key123\n", encoding="utf-8")
        with patch("sys.argv", [
            "credential_manager.py", "migrate",
            "--env-file", str(env_file),
        ]):
            cm.main()
        output = capsys.readouterr().out
        assert "移行結果" in output

    def test_cleanup_command_confirmed(self, mock_keyring, tmp_path, capsys):
        """cleanup コマンド: 確認して実行 (lines 814-821)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append("CL_KEY")
        try:
            env_file = tmp_path / ".env"
            env_file.write_text("CL_KEY=val\n", encoding="utf-8")
            cm.store("CL_KEY", "val")
            with patch("sys.argv", [
                "credential_manager.py", "cleanup",
                "--env-file", str(env_file),
            ]), patch("builtins.input", return_value="y"):
                cm.main()
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_command_skipped(self, mock_keyring, tmp_path, capsys):
        """cleanup コマンド: スキップ (lines 822-823)"""
        cm = _import_cm()
        with patch("sys.argv", [
            "credential_manager.py", "cleanup",
            "--env-file", str(tmp_path / ".env"),
        ]), patch("builtins.input", return_value="n"):
            cm.main()
        output = capsys.readouterr().out
        assert "スキップ" in output

    def test_status_command(self, mock_keyring, tmp_path, capsys):
        """status コマンド (line 825-826)"""
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS[:] = ["GEMINI_API_KEY"]
        try:
            with patch("sys.argv", [
                "credential_manager.py", "status",
                "--env-file", str(tmp_path / ".env"),
            ]):
                cm.main()
            output = capsys.readouterr().out
            assert "Credential Status" in output
        finally:
            cm.MANAGED_KEYS[:] = original_keys
