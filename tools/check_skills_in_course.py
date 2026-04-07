#!/usr/bin/env python3
"""List which skills are referenced in course materials vs not.

Scans:
- course/ (**/*.html, **/*.md)
- .cursor/commands/lesson/*.md

A skill is considered "used" if its name (e.g. banner-creator) or the path
skills/<name>/ appears in any of these files.

Usage:
    uv run python tools/check_skills_in_course.py           # print used / not used
    uv run python tools/check_skills_in_course.py --json    # machine-readable
    uv run python tools/check_skills_in_course.py --not-used-only  # only list not used
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PROJECT_ROOT / "skills"
COURSE_DIR = PROJECT_ROOT / "course"
LESSON_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"


def collect_skill_names() -> list[str]:
    """Return sorted list of skill names (directories under skills/ that have SKILL.md)."""
    names = []
    if not SKILLS_DIR.is_dir():
        return names
    for path in SKILLS_DIR.iterdir():
        if path.is_dir() and (path / "SKILL.md").is_file():
            names.append(path.name)
    return sorted(names)


def collect_course_and_lesson_files() -> list[Path]:
    """Return list of files to search: course/**/*.html, course/**/*.md, lesson/*.md."""
    files: list[Path] = []
    if COURSE_DIR.is_dir():
        files.extend(COURSE_DIR.rglob("*.html"))
        files.extend(COURSE_DIR.rglob("*.md"))
    if LESSON_DIR.is_dir():
        files.extend(LESSON_DIR.glob("*.md"))
    return files


# Section in CURRICULUM.md that lists "not used" skills; we must not count those as "used".
CURRICULUM_SECTION_TO_EXCLUDE = "## 講義未使用スキル"


def get_searchable_text(file_path: Path) -> str:
    """Return file content, masking the '講義未使用スキル' section in CURRICULUM.md so it does not count as usage."""
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    # In CURRICULUM.md, exclude the "講義未使用スキル" section so names listed there are not considered "used".
    if file_path == COURSE_DIR / "CURRICULUM.md" and CURRICULUM_SECTION_TO_EXCLUDE in text:
        start = text.find(CURRICULUM_SECTION_TO_EXCLUDE)
        # Find next ## at start of line (start of next section)
        rest = text[start + len(CURRICULUM_SECTION_TO_EXCLUDE) :]
        next_h2 = rest.find("\n## ")
        if next_h2 != -1:
            block_to_remove = text[start : start + len(CURRICULUM_SECTION_TO_EXCLUDE) + next_h2]
            text = text.replace(block_to_remove, "")
        else:
            text = text[:start]
    return text


def is_skill_used_in_file(skill_name: str, file_path: Path) -> bool:
    """True if skill is referenced in the file content."""
    text = get_searchable_text(file_path)
    if not text:
        return False
    # Match exact skill name or path skills/<name>/
    if skill_name in text:
        return True
    path_ref = f"skills/{skill_name}/"
    if path_ref in text:
        return True
    return False


def compute_used_and_not_used(
    skill_names: list[str], files: list[Path]
) -> tuple[list[str], list[str]]:
    """For each skill, check if any file references it. Return (used, not_used)."""
    used: list[str] = []
    not_used: list[str] = []
    for name in skill_names:
        found = any(is_skill_used_in_file(name, f) for f in files)
        if found:
            used.append(name)
        else:
            not_used.append(name)
    return used, not_used


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List skills used vs not used in course/ and lesson commands."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON: { \"used\": [...], \"not_used\": [...] }",
    )
    parser.add_argument(
        "--not-used-only",
        action="store_true",
        help="Print only skill names not used in course (one per line).",
    )
    args = parser.parse_args()

    skill_names = collect_skill_names()
    files = collect_course_and_lesson_files()
    used, not_used = compute_used_and_not_used(skill_names, files)

    if args.json:
        out = {"used": used, "not_used": not_used, "total": len(skill_names)}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.not_used_only:
        for name in not_used:
            print(name)
        return 0

    print("Skills referenced in course/ or .cursor/commands/lesson/ (used):")
    print(" ", ", ".join(used))
    print()
    print("Skills NOT referenced (not used in course):")
    print(" ", ", ".join(not_used))
    print()
    print(f"Total: {len(skill_names)}  Used: {len(used)}  Not used: {len(not_used)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
