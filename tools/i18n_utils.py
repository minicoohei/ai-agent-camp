#!/usr/bin/env python3
"""Shared i18n utilities for build and translation tools.

Provides constants, suffix detection, and file collection used by
both check_translations.py and build_release.py.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SUPPORTED_LANGS = ("ja", "en", "es")
DEFAULT_LANG = "ja"

# Matches language suffix: .en.md, .es.yaml, etc.
LANG_SUFFIX_RE = re.compile(r"\.(en|es)\.(\w+)$")


def is_lang_suffixed(filename: str) -> bool:
    """Check if a filename has a language suffix like .en.md or .es.yaml."""
    return bool(LANG_SUFFIX_RE.search(filename))


def get_lang_variant_path(base_path: Path, lang: str) -> Path:
    """Return the path for a language variant of a base file.

    Example: get_lang_variant_path(Path("start-0-1.md"), "en") -> Path("start-0-1.en.md")
    For DEFAULT_LANG ("ja"), returns the base path unchanged.
    """
    if lang == DEFAULT_LANG:
        return base_path
    stem = base_path.stem
    suffix = base_path.suffix
    return base_path.with_name(f"{stem}.{lang}{suffix}")


def strip_lang_suffix(filename: str) -> str:
    """Remove language suffix from filename.

    Example: "start-0-1.en.md" -> "start-0-1.md"
    """
    return LANG_SUFFIX_RE.sub(r".\2", filename)


def _has_cjk(text: str) -> bool:
    """Check if text contains CJK characters."""
    for ch in text:
        if unicodedata.category(ch).startswith("Lo"):
            # CJK Unified Ideographs, Hiragana, Katakana
            cp = ord(ch)
            if (0x3040 <= cp <= 0x30FF  # Hiragana + Katakana
                    or 0x4E00 <= cp <= 0x9FFF  # CJK Unified
                    or 0x3400 <= cp <= 0x4DBF):  # CJK Extension A
                return True
    return False


def collect_base_files(
    directory: Path,
    pattern: str = "*.md",
    recursive: bool = False,
    exclude_cjk: bool = True,
) -> list[Path]:
    """Collect base (non-suffixed) files matching a pattern.

    Returns files sorted by name, excluding language-suffixed variants.
    If exclude_cjk is True, files with CJK characters in the name are excluded
    (these are Japanese-only aliases like 研修開始.md).
    """
    if not directory.exists():
        return []

    if recursive:
        files = sorted(directory.rglob(pattern))
    else:
        files = sorted(directory.glob(pattern))

    result = []
    for f in files:
        if not f.is_file():
            continue
        if is_lang_suffixed(f.name):
            continue
        if exclude_cjk and _has_cjk(f.name):
            continue
        result.append(f)

    return result


# ---------------------------------------------------------------------------
# Asset group definitions — canonical list of translatable directories
# ---------------------------------------------------------------------------

ASSET_GROUPS = [
    {
        "name": "lesson-commands",
        "label": "Lesson Commands",
        "source": ".cursor/commands/lesson",
        "outputs": [".claude/commands/lesson", ".cursor/commands/lesson"],
        "pattern": "*.md",
        "recursive": False,
    },
    {
        "name": "claude-commands",
        "label": "Claude Non-Lesson Commands",
        "source": ".claude/commands",
        "outputs": [".claude/commands"],
        "pattern": "*.md",
        "recursive": False,
    },
    {
        "name": "cursor-utility",
        "label": "Cursor Utility Commands",
        "source": ".cursor/commands/utility",
        "outputs": [".cursor/commands/utility"],
        "pattern": "*.md",
        "recursive": False,
    },
    {
        "name": "skills",
        "label": "Skills",
        "source": "skills",
        "outputs": ["skills"],
        "pattern": "SKILL.md",
        "recursive": True,
        "exclude_dirs": ["_template"],
    },
    {
        "name": "courses",
        "label": "Courses YAML",
        "source": "courses",
        "outputs": ["courses"],
        "pattern": "*.yaml",
        "recursive": True,
    },
    {
        "name": "manifest",
        "label": "Lesson Manifest",
        "source": "courses",
        "outputs": ["courses"],
        "pattern": "lessons.manifest.yaml",
        "recursive": False,
    },
]


def get_base_files_for_group(group: dict) -> list[Path]:
    """Collect base files for an asset group, applying group-specific filters."""
    source_dir = PROJECT_ROOT / group["source"]
    files = collect_base_files(
        source_dir,
        pattern=group["pattern"],
        recursive=group.get("recursive", False),
    )

    # Apply directory exclusions
    exclude_dirs = group.get("exclude_dirs", [])
    if exclude_dirs:
        files = [
            f for f in files
            if not any(ex in f.relative_to(source_dir).parts for ex in exclude_dirs)
        ]

    # For "courses" group, exclude manifest files (handled separately)
    if group["name"] == "courses":
        files = [f for f in files if "lessons.manifest" not in f.name]

    return files
