#!/usr/bin/env python3
"""Validate prerequisites consistency between YAML frontmatter and body text.

Checks that the lesson IDs listed in YAML `prerequisites` match
the "Lesson X-Y" references in the body's 前提条件 table row.

Usage:
    uv run python tools/check_prerequisites.py              # Check all lessons
    uv run python tools/check_prerequisites.py --fix         # Show suggested fixes
    uv run python tools/check_prerequisites.py --fix-write   # Auto-fix and write files
    uv run python tools/check_prerequisites.py --fix-write --backup  # Auto-fix with .bak backup
    uv run python tools/check_prerequisites.py start-16-5    # Check specific lesson
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"

# --- YAML frontmatter parsing (lightweight, no PyYAML dependency) ---

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PREREQ_YAML_RE = re.compile(r'prerequisites:\s*\[([^\]]*)\]')

# --- Lesson ID extraction patterns ---

# Matches "start-X-Y" or "Lesson X-Y" and extracts "X-Y"
LESSON_ID_RE = re.compile(r'(?:start-|Lesson\s*)(\d+-\d+)')

# Body: "前提条件" table row
BODY_PREREQ_RE = re.compile(r'\|\s*前提条件\s*\|([^|]+)\|')

# Range: "Lesson 16-1〜16-6" or "Lesson 0-1～0-3"
RANGE_RE = re.compile(r'Lesson\s*(\d+)-(\d+)\s*[〜～]\s*(?:Lesson\s*)?(\d+)-(\d+)')

# Multi with dot separator: "Lesson 0-1・0-2" or "Lesson 4-1・4-2"
MULTI_DOT_RE = re.compile(r'Lesson\s*(\d+)-(\d+)\s*[・]\s*(?:Lesson\s*)?(\d+)-(\d+)')

# Single: "Lesson 16-4"
SINGLE_RE = re.compile(r'Lesson\s*(\d+-\d+)')


def parse_yaml_prerequisites(text: str) -> list[str]:
    """Extract lesson IDs from YAML frontmatter prerequisites."""
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return []
    frontmatter = fm_match.group(1)
    prereq_match = PREREQ_YAML_RE.search(frontmatter)
    if not prereq_match:
        return []

    raw = prereq_match.group(1)
    items = [s.strip().strip('"').strip("'") for s in raw.split(",") if s.strip()]

    lesson_ids = []
    for item in items:
        m = LESSON_ID_RE.search(item)
        if m:
            lesson_ids.append(m.group(1))
    return sorted(lesson_ids, key=_sort_key)


def parse_body_prerequisites(text: str) -> list[str]:
    """Extract lesson IDs from body 前提条件 row."""
    match = BODY_PREREQ_RE.search(text)
    if not match:
        return []

    prereq_text = match.group(1)
    lesson_ids: set[str] = set()

    # Check ranges first: "Lesson 16-1〜16-6"
    for m in RANGE_RE.finditer(prereq_text):
        mod_start, les_start, mod_end, les_end = (
            int(m.group(1)), int(m.group(2)),
            int(m.group(3)), int(m.group(4)),
        )
        if mod_start == mod_end:
            for i in range(les_start, les_end + 1):
                lesson_ids.add(f"{mod_start}-{i}")

    # Check multi dot: "Lesson 0-1・0-2"
    for m in MULTI_DOT_RE.finditer(prereq_text):
        lesson_ids.add(f"{m.group(1)}-{m.group(2)}")
        lesson_ids.add(f"{m.group(3)}-{m.group(4)}")

    # If no ranges/multi found, extract singles
    if not lesson_ids:
        for m in SINGLE_RE.finditer(prereq_text):
            lesson_ids.add(m.group(1))

    return sorted(lesson_ids, key=_sort_key)


def _sort_key(lesson_id: str) -> tuple[int, int]:
    parts = lesson_id.split("-")
    return int(parts[0]), int(parts[1])


def has_body_prereq_row(text: str) -> bool:
    """Check if the file has a 前提条件 table row at all."""
    return bool(BODY_PREREQ_RE.search(text))


def check_file(path: Path) -> dict | None:
    """Check a single lesson file. Returns None if no prerequisites to check."""
    text = path.read_text(encoding="utf-8")
    yaml_ids = parse_yaml_prerequisites(text)
    body_ids = parse_body_prerequisites(text)
    has_body_row = has_body_prereq_row(text)

    # Skip files with no lesson prerequisites in either place
    if not yaml_ids and not body_ids:
        return None

    yaml_set = set(yaml_ids)
    body_set = set(body_ids)

    if yaml_set == body_set:
        return {
            "file": path.name,
            "status": "ok",
            "yaml": yaml_ids,
            "body": body_ids,
        }

    # YAML has IDs but file has no 前提条件 row → warning (different template)
    if yaml_ids and not has_body_row:
        return {
            "file": path.name,
            "status": "warn",
            "yaml": yaml_ids,
            "body": body_ids,
            "reason": "no 前提条件 table row in body",
        }

    # YAML has IDs and body row exists but contains free-text (no Lesson X-Y refs)
    # → warning, not mismatch (body uses descriptive text instead of lesson refs)
    if yaml_ids and has_body_row and not body_ids:
        return {
            "file": path.name,
            "status": "warn",
            "yaml": yaml_ids,
            "body": body_ids,
            "reason": "前提条件 row has free-text, no Lesson X-Y references",
        }

    return {
        "file": path.name,
        "status": "mismatch",
        "yaml": yaml_ids,
        "body": body_ids,
        "only_in_yaml": sorted(yaml_set - body_set, key=_sort_key),
        "only_in_body": sorted(body_set - yaml_set, key=_sort_key),
    }


def fix_file(path: Path, result: dict, backup: bool = False) -> bool:
    """Rewrite YAML prerequisites to union of YAML + body IDs. Returns True if fixed."""
    combined = sorted(set(result["yaml"]) | set(result["body"]), key=_sort_key)
    new_yaml_str = ", ".join(f'"start-{lid}"' for lid in combined)
    new_prereq_line = f"prerequisites: [{new_yaml_str}]"

    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    if not fm_match:
        return False

    frontmatter = fm_match.group(1)
    prereq_match = PREREQ_YAML_RE.search(frontmatter)
    if not prereq_match:
        return False

    old_line = prereq_match.group(0)
    new_frontmatter = frontmatter.replace(old_line, new_prereq_line, 1)
    new_text = text[:fm_match.start(1)] + new_frontmatter + text[fm_match.end(1):]

    if new_text == text:
        return False

    if backup:
        shutil.copy2(path, path.with_suffix(".md.bak"))

    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    args = sys.argv[1:]
    target = None
    for arg in args:
        if not arg.startswith("-"):
            target = arg
            break

    show_fix = "--fix" in args
    do_write = "--fix-write" in args
    do_backup = "--backup" in args

    if target:
        files = list(LESSON_DIR.glob(f"{target}.md"))
        if not files:
            print(f"File not found: {target}.md")
            return 1
    else:
        files = sorted(LESSON_DIR.glob("start-*.md"))

    mismatches = []
    warnings = []
    fixed = []
    checked = 0

    for path in files:
        result = check_file(path)
        if result is None:
            continue
        checked += 1

        if result["status"] == "warn":
            warnings.append(result)
            print(f"WARN: {result['file']} - {result.get('reason', 'unknown')}")
            print(f"  YAML prerequisites:  {result['yaml']}")
            print()
        elif result["status"] == "mismatch":
            mismatches.append(result)
            print(f"MISMATCH: {result['file']}")
            print(f"  YAML prerequisites:  {result['yaml']}")
            print(f"  Body 前提条件:       {result['body']}")
            if result.get("only_in_yaml"):
                print(f"  Only in YAML:        {result['only_in_yaml']}")
            if result.get("only_in_body"):
                print(f"  Only in body:        {result['only_in_body']}")

            combined = sorted(set(result["yaml"]) | set(result["body"]), key=_sort_key)
            yaml_str = ", ".join(f'"start-{lid}"' for lid in combined)

            if do_write:
                ok = fix_file(path, result, backup=do_backup)
                if ok:
                    fixed.append(result["file"])
                    print(f"  FIXED → prerequisites: [{yaml_str}]")
                else:
                    print(f"  SKIP: could not auto-fix")
            elif show_fix:
                print(f"  Suggested YAML fix:  prerequisites: [{yaml_str}]")
            print()

    if do_write and fixed:
        print(f"Fixed {len(fixed)} file(s): {', '.join(fixed)}")

    if not mismatches:
        msg = f"OK: {checked} lesson(s) checked, no mismatches found."
        if warnings:
            msg += f" ({len(warnings)} warning(s))"
        print(msg)
        return 0

    unfixed = len(mismatches) - len(fixed)
    if unfixed == 0:
        print(f"OK: {len(fixed)} mismatch(es) auto-fixed in {checked} lesson(s).")
        return 0

    print(f"FAIL: {unfixed} mismatch(es) remain in {checked} lesson(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
