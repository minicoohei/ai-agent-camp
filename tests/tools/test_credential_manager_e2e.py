"""credential_manager.py E2Eテスト

keyring をインメモリ dict でモックし、credential_manager のロジックを検証する。

実行: python -m pytest tests/tools/test_credential_manager_e2e.py -v
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest

from tests.conftest import import_module_from_repo


# ---------------------------------------------------------------------------
# In-memory keyring mock
# ---------------------------------------------------------------------------

def _make_mock_keyring() -> ModuleType:
    """dict ベースの keyring モックモジュールを生成する。"""
    store: dict[tuple[str, str], str] = {}

    mock_module = ModuleType("keyring")

    def get_password(service: str, key: str) -> str | None:
        return store.get((service, key))

    def set_password(service: str, key: str, value: str) -> None:
        store[(service, key)] = value

    def delete_password(service: str, key: str) -> None:
        if (service, key) in store:
            del store[(service, key)]

    backend = MagicMock()
    type(backend).__name__ = "MockKeyring"

    def get_keyring():
        return backend

    mock_module.get_password = get_password
    mock_module.set_password = set_password
    mock_module.delete_password = delete_password
    mock_module.get_keyring = get_keyring

    # Expose internal store for test inspection
    mock_module._store = store  # type: ignore[attr-defined]

    return mock_module


@pytest.fixture(autouse=True)
def _mock_keyring():
    """keyring モジュールをインメモリ dict バックエンドで差し替える。

    テストごとに新しい空ストアで credential_manager を再インポートする。
    """
    mock_kr = _make_mock_keyring()
    # sys.modules に差し込むことで import keyring が mock を返す
    original = sys.modules.get("keyring")
    sys.modules["keyring"] = mock_kr
    try:
        yield mock_kr
    finally:
        if original is not None:
            sys.modules["keyring"] = original
        else:
            sys.modules.pop("keyring", None)


def _import_cm():
    mod = import_module_from_repo("credential_manager", "tools/credential_manager.py")
    # キャッシュをリセットして _check_keyring() が再評価されるようにする
    mod._keyring_available = None
    return mod


def _import_runtime_env():
    return import_module_from_repo("runtime_env", "tools/runtime_env.py")


# テスト用のキー名 (既存キーと衝突しない接頭辞)
_TEST_PREFIX = "__E2E_TEST_"
_TEST_KEY_1 = f"{_TEST_PREFIX}KEY_1"
_TEST_KEY_2 = f"{_TEST_PREFIX}KEY_2"
_TEST_KEY_3 = f"{_TEST_PREFIX}KEY_3"


@pytest.fixture(autouse=True)
def _cleanup_test_keys(_mock_keyring):
    """テスト前後にテスト用キーをCredential Storeから削除"""
    cm = _import_cm()
    test_keys = [_TEST_KEY_1, _TEST_KEY_2, _TEST_KEY_3]
    for key in test_keys:
        cm.delete(key)
    yield
    for key in test_keys:
        cm.delete(key)


class TestE2EStoreGetDelete:
    """store → get → delete の実フロー"""

    def test_store_and_retrieve(self):
        cm = _import_cm()
        assert cm.store(_TEST_KEY_1, "e2e-secret-value") is True
        retrieved = cm.get(_TEST_KEY_1)
        assert retrieved == "e2e-secret-value"

    def test_delete_removes_value(self):
        cm = _import_cm()
        cm.store(_TEST_KEY_1, "to-be-deleted")
        assert cm.get(_TEST_KEY_1) == "to-be-deleted"
        assert cm.delete(_TEST_KEY_1) is True
        assert cm.get(_TEST_KEY_1) is None

    def test_overwrite_existing_key(self):
        cm = _import_cm()
        cm.store(_TEST_KEY_1, "original")
        cm.store(_TEST_KEY_1, "updated")
        assert cm.get(_TEST_KEY_1) == "updated"

    def test_get_nonexistent_returns_none(self):
        cm = _import_cm()
        assert cm.get(f"{_TEST_PREFIX}DOES_NOT_EXIST") is None


class TestE2EInjectToEnviron:
    """store → inject_to_environ → os.environ 反映"""

    def test_inject_populates_environ(self, monkeypatch):
        cm = _import_cm()
        # MANAGED_KEYS に一時的にテストキーを追加
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            cm.store(_TEST_KEY_1, "injected-e2e-value")
            monkeypatch.delenv(_TEST_KEY_1, raising=False)

            count = cm.inject_to_environ()

            assert count >= 1
            assert os.environ.get(_TEST_KEY_1) == "injected-e2e-value"
        finally:
            cm.MANAGED_KEYS[:] = original_keys
            monkeypatch.delenv(_TEST_KEY_1, raising=False)

    def test_inject_does_not_override_existing(self, monkeypatch):
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            cm.store(_TEST_KEY_1, "store-value")
            monkeypatch.setenv(_TEST_KEY_1, "env-value")

            cm.inject_to_environ()

            assert os.environ[_TEST_KEY_1] == "env-value"
        finally:
            cm.MANAGED_KEYS[:] = original_keys


class TestE2EMigrate:
    """migrate_from_dotenv → store → get の実フロー"""

    def test_migrate_dotenv_to_credential_store(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            f"{_TEST_KEY_1}=migrated-value-1\n"
            f"{_TEST_KEY_2}=migrated-value-2\n",
            encoding="utf-8",
        )

        results = cm.migrate_from_dotenv(env_file)

        assert results[_TEST_KEY_1] == "ok"
        assert results[_TEST_KEY_2] == "ok"
        assert cm.get(_TEST_KEY_1) == "migrated-value-1"
        assert cm.get(_TEST_KEY_2) == "migrated-value-2"

    def test_migrate_skips_placeholder_values(self, tmp_path):
        cm = _import_cm()
        env_file = tmp_path / ".env"
        env_file.write_text(
            f"{_TEST_KEY_1}=your_api_key_here\n",
            encoding="utf-8",
        )

        results = cm.migrate_from_dotenv(env_file)

        assert "skipped" in results[_TEST_KEY_1]
        assert cm.get(_TEST_KEY_1) is None


class TestE2ECleanup:
    """migrate → cleanup の安全削除フロー"""

    def test_cleanup_deletes_env_after_migration(self, tmp_path):
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            env_file = tmp_path / ".env"
            env_file.write_text(
                f"{_TEST_KEY_1}=cleanup-test-value\n",
                encoding="utf-8",
            )

            # migrate first
            cm.migrate_from_dotenv(env_file)
            assert cm.get(_TEST_KEY_1) == "cleanup-test-value"

            # re-write .env since migrate doesn't delete it
            env_file.write_text(
                f"{_TEST_KEY_1}=cleanup-test-value\n",
                encoding="utf-8",
            )

            # cleanup
            assert cm.cleanup_dotenv(env_file) is True
            assert not env_file.exists()
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_cleanup_blocks_without_migration(self, tmp_path):
        cm = _import_cm()
        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            env_file = tmp_path / ".env"
            env_file.write_text(
                f"{_TEST_KEY_1}=not-yet-migrated\n",
                encoding="utf-8",
            )

            # cleanup without migration should fail
            assert cm.cleanup_dotenv(env_file) is False
            assert env_file.exists()
        finally:
            cm.MANAGED_KEYS[:] = original_keys


class TestE2ERuntimeEnv:
    """runtime_env.load_runtime_env の優先順位確認"""

    def test_priority_env_over_credential_store(self, monkeypatch, tmp_path):
        cm = _import_cm()
        runtime_env = _import_runtime_env()

        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            cm.store(_TEST_KEY_1, "credential-store-value")
            monkeypatch.setenv(_TEST_KEY_1, "process-env-value")

            env_file = tmp_path / ".env"
            env_file.write_text(
                f"{_TEST_KEY_1}=dotenv-value\n",
                encoding="utf-8",
            )
            runtime_env.load_runtime_env(root_dir=tmp_path)

            # process env should win
            assert os.environ[_TEST_KEY_1] == "process-env-value"
        finally:
            cm.MANAGED_KEYS[:] = original_keys

    def test_priority_credential_store_over_dotenv(self, monkeypatch, tmp_path):
        cm = _import_cm()
        runtime_env = _import_runtime_env()

        original_keys = cm.MANAGED_KEYS.copy()
        cm.MANAGED_KEYS.append(_TEST_KEY_1)
        try:
            cm.store(_TEST_KEY_1, "credential-store-value")
            monkeypatch.delenv(_TEST_KEY_1, raising=False)

            env_file = tmp_path / ".env"
            env_file.write_text(
                f"{_TEST_KEY_1}=dotenv-value\n",
                encoding="utf-8",
            )
            runtime_env.load_runtime_env(root_dir=tmp_path)

            # credential store should win (injected before dotenv, dotenv override=False)
            assert os.environ[_TEST_KEY_1] == "credential-store-value"
        finally:
            cm.MANAGED_KEYS[:] = original_keys
            monkeypatch.delenv(_TEST_KEY_1, raising=False)
