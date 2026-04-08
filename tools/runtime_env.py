"""Shared runtime environment loading for local tools.

Runtime precedence is:
1. Existing process environment
2. OS Credential Store via ``credential_manager``
3. Local ``.env.local`` files as a non-destructive fallback
4. Local ``.env`` files as a non-destructive fallback
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parent.parent


def _inject_credential_store() -> int:
    for module_name in ("credential_manager", "tools.credential_manager"):
        try:
            module = __import__(module_name, fromlist=["inject_to_environ"])
            return int(module.inject_to_environ())
        except ImportError:
            continue
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.debug("Failed to inject runtime credentials via %s: %s", module_name, exc)
            return 0
    return 0


def load_runtime_env(
    root_dir: Path | None = None,
    dotenv_paths: list[Path] | None = None,
) -> int:
    """Load environment variables without overriding the current process env."""
    from dotenv import dotenv_values

    resolved_root = root_dir or ROOT_DIR
    injected = _inject_credential_store()

    candidates = dotenv_paths or [
        resolved_root / ".env.local",
        resolved_root / ".env",
    ]
    for env_path in candidates:
        for key, value in dotenv_values(env_path).items():
            if value:  # skip empty values
                os.environ.setdefault(key, value)

    return injected
