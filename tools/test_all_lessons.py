#!/usr/bin/env python3
"""
全レッスン構造検証スクリプト
- .claude/ と .cursor/ のミラー一致
- lessons.manifest.yaml の整合性
- 各レッスンMD内のパス参照・スキル参照・レッスン相互参照の実在チェック
"""

import json
import os
import re
import sys
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CLAUDE_LESSONS = BASE_DIR / ".claude" / "commands" / "lesson"
CURSOR_LESSONS = BASE_DIR / ".cursor" / "commands" / "lesson"
MANIFEST = BASE_DIR / "courses" / "lessons.manifest.yaml"
OUTPUT = BASE_DIR / "output" / "test-results" / "structural-validation.json"

results = {
    "summary": {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0},
    "mirror_check": [],
    "manifest_check": [],
    "path_reference_check": [],
    "skill_reference_check": [],
    "lesson_cross_reference_check": [],
    "course_page_check": [],
}


def check(category, name, passed, detail=""):
    results["summary"]["total_checks"] += 1
    status = "PASS" if passed else "FAIL"
    if passed:
        results["summary"]["passed"] += 1
    else:
        results["summary"]["failed"] += 1
    results[category].append({"name": name, "status": status, "detail": detail})
    return passed


def warn(category, name, detail=""):
    results["summary"]["total_checks"] += 1
    results["summary"]["warnings"] += 1
    results[category].append({"name": name, "status": "WARN", "detail": detail})


# === 1. Mirror check ===
def check_mirror():
    claude_files = sorted(f.name for f in CLAUDE_LESSONS.glob("*.md"))
    cursor_files = sorted(f.name for f in CURSOR_LESSONS.glob("*.md"))

    check(
        "mirror_check",
        "file_list_match",
        claude_files == cursor_files,
        f"claude={len(claude_files)}, cursor={len(cursor_files)}, "
        f"only_claude={set(claude_files) - set(cursor_files)}, "
        f"only_cursor={set(cursor_files) - set(claude_files)}",
    )

    for fname in claude_files:
        cf = (CLAUDE_LESSONS / fname).read_text()
        sf = (CURSOR_LESSONS / fname).read_text()
        check(
            "mirror_check",
            f"content_match:{fname}",
            cf == sf,
            f"Files differ" if cf != sf else "",
        )


# === 2. Manifest check ===
def check_manifest():
    with open(MANIFEST) as f:
        manifest = yaml.safe_load(f)

    for entry in manifest:
        lid = entry["lessonId"]
        # Check .claude file exists
        claude_path = CLAUDE_LESSONS / f"{lid}.md"
        check(
            "manifest_check",
            f"claude_file_exists:{lid}",
            claude_path.exists(),
            f"Missing: {claude_path}",
        )
        # Check .cursor file exists
        cursor_path = CURSOR_LESSONS / f"{lid}.md"
        check(
            "manifest_check",
            f"cursor_file_exists:{lid}",
            cursor_path.exists(),
            f"Missing: {cursor_path}",
        )
        if lid.startswith("start-") and "module" in entry and "lesson" in entry:
            match = re.fullmatch(r"start-(\d+)-(\d+)", lid)
            if match:
                expected_module = int(match.group(1))
                expected_lesson = int(match.group(2))
                check(
                    "manifest_check",
                    f"module_number_match:{lid}",
                    entry["module"] == expected_module,
                    f"manifest module={entry['module']} but lessonId implies module={expected_module}",
                )
                check(
                    "manifest_check",
                    f"lesson_number_match:{lid}",
                    entry["lesson"] == expected_lesson,
                    f"manifest lesson={entry['lesson']} but lessonId implies lesson={expected_lesson}",
                )
        if lid.startswith("start-") and "chapterRef" in entry:
            chapter_path = BASE_DIR / entry["chapterRef"]
            chapter_exists = chapter_path.exists() or chapter_path.with_name("chapter.yaml").exists()
            check(
                "manifest_check",
                f"chapter_ref_exists:{lid}",
                chapter_exists,
                f"Missing chapterRef target: {entry['chapterRef']}",
            )

    # Check reverse: files not in manifest
    manifest_ids = {e["lessonId"] for e in manifest}
    for f in CLAUDE_LESSONS.glob("*.md"):
        fid = f.stem
        if fid not in manifest_ids:
            warn(
                "manifest_check",
                f"not_in_manifest:{fid}",
                f"{fid}.md exists in .claude/commands/lesson/ but not in manifest",
            )


# === 3. Path reference check ===
PATH_PATTERNS = [
    # Relative paths from project root
    re.compile(r'(?:https://ai-agent\.camp/[^\s"\'<>)]+)'),
    re.compile(r'(?:tools/[^\s"\'<>)]+\.py)'),
    re.compile(r'(?:skills/[^\s"\'<>)]+)'),
    re.compile(r'(?:docs/[^\s"\'<>)]+)'),
    re.compile(r'(?:scripts/[^\s"\'<>)]+)'),
    re.compile(r'(?:\.claude/[^\s"\'<>)]+)'),
    re.compile(r'(?:\.cursor/[^\s"\'<>)]+)'),
]


def check_path_references():
    for md_file in sorted(CLAUDE_LESSONS.glob("start-*.md")):
        content = md_file.read_text()
        for pattern in PATH_PATTERNS:
            for match in pattern.findall(content):
                # Clean up the match
                path = match.rstrip(".,;:)")
                # Skip URLs
                if path.startswith("http"):
                    continue
                # Skip code fences and template patterns
                if "${" in path or "{" in path:
                    continue
                full_path = BASE_DIR / path
                # Check if it's a file or directory
                exists = full_path.exists() or full_path.parent.exists()
                if not exists:
                    # Try without trailing segments that might be anchors
                    exists = (BASE_DIR / path.split("#")[0]).exists()
                check(
                    "path_reference_check",
                    f"{md_file.stem}:{path}",
                    exists,
                    f"Referenced path does not exist: {path}",
                )


# === 4. Skill reference check ===
SKILL_PATTERN = re.compile(r'skills/([a-z0-9-]+)')


def check_skill_references():
    for md_file in sorted(CLAUDE_LESSONS.glob("start-*.md")):
        content = md_file.read_text()
        for match in SKILL_PATTERN.findall(content):
            skill_dir = BASE_DIR / "skills" / match
            # Also check .claude/skills
            alt_dir = BASE_DIR / ".claude" / "skills" / match
            exists = skill_dir.exists() or alt_dir.exists()
            check(
                "skill_reference_check",
                f"{md_file.stem}:skills/{match}",
                exists,
                f"Skill not found: skills/{match}",
            )


# === 5. Lesson cross-reference check ===
LESSON_REF_PATTERN = re.compile(r'/start-(\d+-\d+)')


def check_lesson_cross_references():
    all_lessons = {f.stem for f in CLAUDE_LESSONS.glob("start-*.md")}

    for md_file in sorted(CLAUDE_LESSONS.glob("start-*.md")):
        content = md_file.read_text()
        for match in LESSON_REF_PATTERN.findall(content):
            ref_name = f"start-{match}"
            check(
                "lesson_cross_reference_check",
                f"{md_file.stem} -> {ref_name}",
                ref_name in all_lessons,
                f"Referenced lesson does not exist: {ref_name}",
            )


# === 6. Course page reference check ===
COURSE_PAGE_PATTERN = re.compile(r'https://ai-agent\.camp/[^\s"\'<>)]+')


def check_course_pages():
    for md_file in sorted(CLAUDE_LESSONS.glob("start-*.md")):
        content = md_file.read_text()
        for match in COURSE_PAGE_PATTERN.findall(content):
            url = match.rstrip(".,;:)")
            # External URLs are validated by presence only (not local path check)
            check(
                "course_page_check",
                f"{md_file.stem}:{url}",
                url.startswith("https://ai-agent.camp/"),
                f"Course page URL is malformed: {url}",
            )


def main():
    print("=== 全レッスン構造検証 ===\n")

    print("1. ミラーチェック (.claude/ vs .cursor/)...")
    check_mirror()

    print("2. Manifest整合性チェック...")
    check_manifest()

    print("3. パス参照チェック...")
    check_path_references()

    print("4. スキル参照チェック...")
    check_skill_references()

    print("5. レッスン相互参照チェック...")
    check_lesson_cross_references()

    print("6. 教材ページ参照チェック...")
    check_course_pages()

    # Output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    s = results["summary"]
    print(f"\n=== 結果サマリー ===")
    print(f"Total: {s['total_checks']}, PASS: {s['passed']}, FAIL: {s['failed']}, WARN: {s['warnings']}")

    # Print failures
    failures = []
    for category, items in results.items():
        if category == "summary":
            continue
        for item in items:
            if item["status"] == "FAIL":
                failures.append(f"  [{category}] {item['name']}: {item['detail']}")

    if failures:
        print(f"\n=== FAILURES ({len(failures)}) ===")
        for f in failures:
            print(f)

    # Print warnings
    warnings = []
    for category, items in results.items():
        if category == "summary":
            continue
        for item in items:
            if item["status"] == "WARN":
                warnings.append(f"  [{category}] {item['name']}: {item['detail']}")

    if warnings:
        print(f"\n=== WARNINGS ({len(warnings)}) ===")
        for w in warnings:
            print(w)

    print(f"\n結果を {OUTPUT} に保存しました。")
    return 1 if s["failed"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
