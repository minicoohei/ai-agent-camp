"""Tests for Codex documentation validation."""
from pathlib import Path

from tools import check_agent_docs


def test_required_files_exist():
    for path in check_agent_docs.REQUIRED_FILES:
        assert path.exists(), f"Missing required file: {path}"


def test_text_checks_contain_codex():
    for path, needle in check_agent_docs.TEXT_CHECKS:
        text = Path(path).read_text(encoding="utf-8")
        assert needle in text, f"Missing '{needle}' in {path}"
