"""runtime_env.py の単体テスト"""

from __future__ import annotations

import os

from tests.conftest import import_module_from_repo


def test_load_runtime_env_preserves_existing_env(tmp_path, monkeypatch):
    runtime_env = import_module_from_repo("runtime_env", "tools/runtime_env.py")

    env_path = tmp_path / ".env"
    env_path.write_text(
        "GEMINI_API_KEY=dotenv-value\n"
        "OUTPUT_DIR=./output\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("GEMINI_API_KEY", "process-value")
    monkeypatch.delenv("OUTPUT_DIR", raising=False)
    monkeypatch.setattr(runtime_env, "_inject_credential_store", lambda: 0)

    runtime_env.load_runtime_env(root_dir=tmp_path)

    assert os.environ["GEMINI_API_KEY"] == "process-value"
    assert os.environ["OUTPUT_DIR"] == "./output"


def test_load_runtime_env_prefers_env_local_over_env(tmp_path, monkeypatch):
    runtime_env = import_module_from_repo("runtime_env", "tools/runtime_env.py")

    (tmp_path / ".env.local").write_text(
        "OUTPUT_DIR=./local-output\n",
        encoding="utf-8",
    )
    (tmp_path / ".env").write_text(
        "OUTPUT_DIR=./fallback-output\n",
        encoding="utf-8",
    )

    monkeypatch.delenv("OUTPUT_DIR", raising=False)
    monkeypatch.setattr(runtime_env, "_inject_credential_store", lambda: 0)

    runtime_env.load_runtime_env(root_dir=tmp_path)

    assert os.environ["OUTPUT_DIR"] == "./local-output"
