#!/usr/bin/env python3
"""
Module Renumbering Script
カリキュラムのモジュール番号を一括で振り直すスクリプト。
2段階リネーム（一時名経由）で衝突を回避する。
"""

import os
import re
import shutil
import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Old module number → New module number mapping
# Modules 1, 2, 3, 5 stay the same
# Module 18 → 4 (but 18 doesn't exist yet, will be created separately)
# Module 7 (NEW) will be created separately
MODULE_MAP = {
    4: 8,    # データ分析
    6: 9,    # Slack検索
    7: 13,   # 動画生成
    8: 10,   # GAS自動化
    9: 11,   # GitHub Actions
    10: 12,  # Notion連携
    11: 6,   # エージェント開発 & リサーチ
    12: 17,  # マーケティング
    13: 15,  # LP/HP制作
    14: 18,  # PM & システム要件定義
    15: 16,  # メール配信 (Resend CLI)
    16: 14,  # 記事作成
}

# Directory name suffixes (historically used for course/modules/{N}-{name}/, now external)
MODULE_DIR_NAMES = {
    4: "data",
    6: "search",
    7: "video",
    8: "gas",
    9: "actions",
    10: "notion",
    11: "agent",
    12: "marketing",
    13: "lp",
    14: "pm-sysdef",
    15: "email",
    16: "article",
}

# New directory names (for the new module numbers)
NEW_MODULE_DIR_NAMES = {
    6: "agent",       # 旧11
    8: "data",         # 旧4
    9: "search",       # 旧6
    10: "gas",         # 旧8
    11: "actions",     # 旧9
    12: "notion",      # 旧10
    13: "video",       # 旧7
    14: "article",     # 旧16
    15: "lp",          # 旧13
    16: "email",       # 旧15
    17: "marketing",   # 旧12
    18: "pm-sysdef",   # 旧14
}

TEMP_PREFIX = "__tmp_renumber_"


def rename_command_files(base_dir: Path, dry_run: bool = True):
    """Rename start-{old}-*.md files in lesson command directories."""
    lesson_dir = base_dir / "commands" / "lesson"
    if not lesson_dir.exists():
        print(f"  [SKIP] {lesson_dir} does not exist")
        return

    # Phase 1: Rename to temp names
    renames = []
    for old_num, new_num in MODULE_MAP.items():
        pattern = f"start-{old_num}-*.md"
        for f in sorted(lesson_dir.glob(pattern)):
            # Extract lesson number (e.g., start-4-1.md → 1)
            match = re.match(rf"start-{old_num}-(.+)\.md", f.name)
            if match:
                lesson_suffix = match.group(1)
                temp_name = f"{TEMP_PREFIX}{new_num}-{lesson_suffix}.md"
                final_name = f"start-{new_num}-{lesson_suffix}.md"
                renames.append((f, lesson_dir / temp_name, lesson_dir / final_name))

    if not renames:
        print(f"  [SKIP] No files to rename in {lesson_dir}")
        return

    # Phase 1: old → temp
    print(f"  Phase 1: Renaming {len(renames)} files to temp names in {lesson_dir}")
    for src, tmp, _ in renames:
        print(f"    {src.name} → {tmp.name}")
        if not dry_run:
            src.rename(tmp)

    # Phase 2: temp → final
    print(f"  Phase 2: Renaming {len(renames)} files to final names")
    for _, tmp, dst in renames:
        print(f"    {tmp.name} → {dst.name}")
        if not dry_run:
            if dst.exists():
                print(f"    [WARN] {dst.name} already exists, overwriting")
            tmp.rename(dst)


def rename_course_modules(dry_run: bool = True):
    """Rename course/modules/{N}-{name}/ directories (no-op if directory removed)."""
    modules_dir = ROOT / "course" / "modules"
    if not modules_dir.exists():
        print(f"  [SKIP] {modules_dir} does not exist")
        return

    renames = []
    for old_num, new_num in MODULE_MAP.items():
        dir_name = MODULE_DIR_NAMES.get(old_num)
        if dir_name:
            old_dir = modules_dir / f"{old_num}-{dir_name}"
            new_dir_name = NEW_MODULE_DIR_NAMES.get(new_num, dir_name)
            temp_dir = modules_dir / f"{TEMP_PREFIX}{new_num}-{new_dir_name}"
            final_dir = modules_dir / f"{new_num}-{new_dir_name}"
            if old_dir.exists():
                renames.append((old_dir, temp_dir, final_dir))
            else:
                print(f"  [SKIP] {old_dir} does not exist")

    if not renames:
        print("  [SKIP] No course module directories to rename")
        return

    # Phase 1: old → temp
    print(f"  Phase 1: Renaming {len(renames)} directories to temp names")
    for src, tmp, _ in renames:
        print(f"    {src.name} → {tmp.name}")
        if not dry_run:
            src.rename(tmp)

    # Phase 2: temp → final
    print(f"  Phase 2: Renaming {len(renames)} directories to final names")
    for _, tmp, dst in renames:
        print(f"    {tmp.name} → {dst.name}")
        if not dry_run:
            if dst.exists():
                print(f"    [WARN] {dst.name} already exists!")
            tmp.rename(dst)


def replace_in_file(filepath: Path, replacements: list[tuple[str, str]], dry_run: bool = True):
    """Apply text replacements in a file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError):
        return 0

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content != original:
        changes = sum(1 for old, new in replacements if old in original)
        if not dry_run:
            filepath.write_text(content, encoding="utf-8")
        return changes
    return 0


def build_content_replacements():
    """Build the list of (old_string, new_string) replacements for file contents."""
    replacements = []

    # We need to do replacements in a specific order to avoid partial matches.
    # Use a 2-phase approach: old → temp, then temp → new
    temp_replacements = []
    final_replacements = []

    for old_num, new_num in sorted(MODULE_MAP.items()):
        # Command references: start-{N}-
        temp_replacements.append((f"start-{old_num}-", f"start-{TEMP_PREFIX}{new_num}-"))
        final_replacements.append((f"start-{TEMP_PREFIX}{new_num}-", f"start-{new_num}-"))

        # Course module paths: modules/{N}-
        old_dir_name = MODULE_DIR_NAMES.get(old_num, "")
        new_dir_name = NEW_MODULE_DIR_NAMES.get(new_num, old_dir_name)
        if old_dir_name:
            temp_replacements.append(
                (f"modules/{old_num}-{old_dir_name}", f"modules/{TEMP_PREFIX}{new_num}-{new_dir_name}")
            )
            final_replacements.append(
                (f"modules/{TEMP_PREFIX}{new_num}-{new_dir_name}", f"modules/{new_num}-{new_dir_name}")
            )

        # Module references in docs: "Module {N}" / "モジュール {N}"
        # These are trickier - we'll handle them with regex in a separate pass

    return temp_replacements, final_replacements


def replace_content_in_tree(dry_run: bool = True):
    """Replace module references in all relevant files."""
    temp_replacements, final_replacements = build_content_replacements()

    # Directories to scan
    scan_dirs = [
        ROOT / ".cursor" / "commands",
        ROOT / ".claude" / "commands",
        ROOT / "course",
        ROOT / "courses",
        ROOT / "docs",
    ]

    # Individual files
    scan_files = [
        ROOT / "CLAUDE.md",
        ROOT / "README.md",
    ]

    # Collect all files
    all_files = list(scan_files)
    for d in scan_dirs:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and f.suffix in (".md", ".html", ".yaml", ".yml", ".json", ".css", ".js"):
                    all_files.append(f)

    total_changes = 0

    # Phase 1: Apply temp replacements
    print(f"\n  Content Phase 1: Applying temp replacements to {len(all_files)} files...")
    for f in all_files:
        if f.exists():
            changes = replace_in_file(f, temp_replacements, dry_run)
            if changes > 0:
                total_changes += changes
                if dry_run:
                    print(f"    [DRY] {f.relative_to(ROOT)}: {changes} replacement patterns matched")

    # Phase 2: Apply final replacements
    print(f"  Content Phase 2: Applying final replacements...")
    for f in all_files:
        if f.exists():
            changes = replace_in_file(f, final_replacements, dry_run)
            if changes > 0:
                total_changes += changes

    print(f"  Total files with replacements: {total_changes}")
    return total_changes


def verify_no_old_refs():
    """Check for remaining old module references after renumbering."""
    print("\n=== Verification: Checking for remaining old references ===")
    issues = []

    scan_dirs = [
        ROOT / ".cursor" / "commands" / "lesson",
        ROOT / ".claude" / "commands" / "lesson",
    ]

    for d in scan_dirs:
        if not d.exists():
            continue
        for old_num in MODULE_MAP.keys():
            pattern = f"start-{old_num}-*.md"
            matches = list(d.glob(pattern))
            if matches:
                for m in matches:
                    issues.append(f"  [ISSUE] Old file still exists: {m.relative_to(ROOT)}")

    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(issue)
    else:
        print("  [OK] No old module references found in file names")

    return len(issues)


def main():
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No changes will be made")
        print("Run with --execute to apply changes")
        print("=" * 60)
    else:
        print("=" * 60)
        print("EXECUTING - Changes will be applied!")
        print("=" * 60)

    print(f"\nProject root: {ROOT}")
    print(f"\nModule mapping (old → new):")
    for old, new in sorted(MODULE_MAP.items()):
        print(f"  {old} → {new}")

    # Step 1: Rename command files
    print("\n=== Step 1: Rename .cursor command files ===")
    rename_command_files(ROOT / ".cursor", dry_run)

    print("\n=== Step 2: Rename .claude command files ===")
    rename_command_files(ROOT / ".claude", dry_run)

    # Step 3: Rename course module directories
    print("\n=== Step 3: Rename course module directories ===")
    rename_course_modules(dry_run)

    # Step 4: Replace content references
    print("\n=== Step 4: Replace content references in files ===")
    replace_content_in_tree(dry_run)

    # Step 5: Verify
    if not dry_run:
        verify_no_old_refs()

    if dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN COMPLETE - Run with --execute to apply")
        print("=" * 60)


if __name__ == "__main__":
    main()
