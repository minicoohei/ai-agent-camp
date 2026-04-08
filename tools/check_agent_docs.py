#!/usr/bin/env python3
"""Validate Codex-facing documentation required for the rollout."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    PROJECT_ROOT / "AGENTS.md",
    PROJECT_ROOT / "docs" / "codex-guide.md",
    PROJECT_ROOT / "docs" / "codex-safety.md",
    PROJECT_ROOT / "docs" / "codex-mcp.md",
]

TEXT_CHECKS = [
    (PROJECT_ROOT / "README.md", "Codex"),
    (PROJECT_ROOT / "README.md", "Claude Code"),
    (PROJECT_ROOT / "README.md", "Cursor"),
    (PROJECT_ROOT / "courses" / "aiagent" / "course.yaml", "Codex"),
    (PROJECT_ROOT / "courses" / "aiagent" / "course.en.yaml", "Codex"),
    (PROJECT_ROOT / "courses" / "aiagent" / "course.es.yaml", "Codex"),
    (
        PROJECT_ROOT / "courses" / "aiagent" / "lesson02-setup" / "lesson.yaml",
        "Codex",
    ),
    (
        PROJECT_ROOT / "courses" / "aiagent" / "lesson01-foundation" / "ch05-cursor-usage" / "chapter.yaml",
        "Codex",
    ),
    (PROJECT_ROOT / "AGENTS.md", "Claude Code"),
    (PROJECT_ROOT / "AGENTS.md", "Cursor"),
    (PROJECT_ROOT / "docs" / "codex-guide.md", "Claude Code"),
    (PROJECT_ROOT / "docs" / "codex-guide.md", "Cursor"),
    (PROJECT_ROOT / "docs" / "codex-guide.md", "sandbox"),
    (PROJECT_ROOT / "docs" / "codex-guide.md", "approval"),
]


def _check_exists(path: Path) -> str | None:
    """Return an error message when a required file is missing."""
    if not path.exists():
        return f"Missing required file: {path.relative_to(PROJECT_ROOT)}"
    return None


def _check_contains(path: Path, needle: str) -> str | None:
    """Return an error message when a file cannot be read or lacks a required string."""
    if not path.exists():
        return f"Missing required file for text check: {path.relative_to(PROJECT_ROOT)}"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return f"Failed to read {path.relative_to(PROJECT_ROOT)}: {exc}"
    if needle not in text:
        return f"Missing '{needle}' in {path.relative_to(PROJECT_ROOT)}"
    return None


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        error = _check_exists(path)
        if error:
            errors.append(error)

    for path, needle in TEXT_CHECKS:
        error = _check_contains(path, needle)
        if error:
            errors.append(error)

    if errors:
        print("Codex doc validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Codex doc validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
