#!/usr/bin/env python3
"""Release build script for multi-language distribution.

Collects files for the specified language, strips language suffixes,
and outputs a clean distribution tree under dist/{lang}/.

Usage:
    uv run python tools/build_release.py --lang ja|en|es [--output dist/] [--strict] [--dry-run]

Exit codes:
    0 — build completed (possibly with skipped files)
    1 — build failed or --strict with missing translations
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from i18n_utils import (
    ASSET_GROUPS,
    DEFAULT_LANG,
    PROJECT_ROOT,
    SUPPORTED_LANGS,
    collect_base_files,
    get_base_files_for_group,
    get_lang_variant_path,
    is_lang_suffixed,
    _has_cjk,
)


def copy_file(src: Path, dst: Path, dry_run: bool = False) -> bool:
    """Copy a file, creating parent directories as needed."""
    if dry_run:
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def build_simple_group(
    group: dict,
    lang: str,
    output_root: Path,
    dry_run: bool,
    verbose: bool,
) -> tuple[int, int, list[str]]:
    """Build a simple asset group (commands, manifest).

    Returns (copied, skipped, warnings).
    """
    base_files = get_base_files_for_group(group)
    copied = 0
    skipped = 0
    warnings: list[str] = []

    for base_file in base_files:
        # For non-default lang, skip CJK-named files (ja-only aliases)
        if lang != DEFAULT_LANG and _has_cjk(base_file.name):
            continue

        source_dir = PROJECT_ROOT / group["source"]
        rel = base_file.relative_to(source_dir)

        if lang == DEFAULT_LANG:
            src = base_file
        else:
            src = get_lang_variant_path(base_file, lang)
            if not src.exists():
                skipped += 1
                warnings.append(f"  SKIP: {src.relative_to(PROJECT_ROOT)}")
                continue

        # Write to each output path
        for out_dir in group["outputs"]:
            dst = output_root / out_dir / rel
            if verbose:
                print(f"  COPY: {src.relative_to(PROJECT_ROOT)} -> {dst.relative_to(output_root)}")
            copy_file(src, dst, dry_run)

        copied += 1

    return copied, skipped, warnings


def build_skills_group(
    group: dict,
    lang: str,
    output_root: Path,
    dry_run: bool,
    verbose: bool,
) -> tuple[int, int, list[str]]:
    """Build skills group — copy full directory structure, swap SKILL.md.

    Returns (copied, skipped, warnings).
    """
    skills_dir = PROJECT_ROOT / group["source"]
    exclude_dirs = set(group.get("exclude_dirs", []))
    copied = 0
    skipped = 0
    warnings: list[str] = []

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name in exclude_dirs:
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        # Determine the SKILL.md to use
        if lang == DEFAULT_LANG:
            src_md = skill_md
        else:
            src_md = get_lang_variant_path(skill_md, lang)
            if not src_md.exists():
                skipped += 1
                warnings.append(f"  SKIP: {src_md.relative_to(PROJECT_ROOT)}")
                src_md = None

        rel_skill = skill_dir.relative_to(PROJECT_ROOT)
        out_skill_dir = output_root / rel_skill

        # Copy all files in the skill directory except language variants of SKILL.md
        for item in sorted(skill_dir.rglob("*")):
            if not item.is_file():
                continue
            # Skip language-suffixed SKILL files
            if item.name.startswith("SKILL.") and is_lang_suffixed(item.name):
                continue
            # Skip base SKILL.md (we'll copy the correct version separately)
            if item.name == "SKILL.md":
                continue

            rel_item = item.relative_to(skill_dir)
            dst = out_skill_dir / rel_item
            if verbose:
                print(f"  COPY: {item.relative_to(PROJECT_ROOT)} -> {dst.relative_to(output_root)}")
            copy_file(item, dst, dry_run)

        # Copy the appropriate SKILL.md
        if src_md is not None:
            dst_md = out_skill_dir / "SKILL.md"
            if verbose:
                print(f"  COPY: {src_md.relative_to(PROJECT_ROOT)} -> {dst_md.relative_to(output_root)}")
            copy_file(src_md, dst_md, dry_run)
            copied += 1
        else:
            # No translation — still copy the base SKILL.md for completeness
            if skill_md.exists():
                dst_md = out_skill_dir / "SKILL.md"
                copy_file(skill_md, dst_md, dry_run)

    return copied, skipped, warnings


def build_courses_group(
    group: dict,
    lang: str,
    output_root: Path,
    dry_run: bool,
    verbose: bool,
) -> tuple[int, int, list[str]]:
    """Build courses YAML group — existing suffix pattern.

    Returns (copied, skipped, warnings).
    """
    courses_dir = PROJECT_ROOT / group["source"]
    base_files = get_base_files_for_group(group)
    copied = 0
    skipped = 0
    warnings: list[str] = []

    for base_file in base_files:
        rel = base_file.relative_to(courses_dir)

        if lang == DEFAULT_LANG:
            src = base_file
        else:
            src = get_lang_variant_path(base_file, lang)
            if not src.exists():
                skipped += 1
                warnings.append(f"  SKIP: {src.relative_to(PROJECT_ROOT)}")
                continue

        dst = output_root / "courses" / rel
        if verbose:
            print(f"  COPY: {src.relative_to(PROJECT_ROOT)} -> {dst.relative_to(output_root)}")
        copy_file(src, dst, dry_run)
        copied += 1

    return copied, skipped, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a single-language release distribution."
    )
    parser.add_argument(
        "--lang",
        choices=SUPPORTED_LANGS,
        required=True,
        help="Target language",
    )
    parser.add_argument(
        "--output", "-o",
        default="dist",
        help="Output base directory (default: dist/)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any translations are missing",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without writing",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show individual file copies",
    )
    args = parser.parse_args()

    lang = args.lang
    output_root = Path(args.output).resolve() / lang

    if args.dry_run:
        print(f"[DRY RUN] Building {lang} release to {output_root}\n")
    else:
        # Clean output directory
        if output_root.exists():
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True, exist_ok=True)
        print(f"Building {lang} release to {output_root}\n")

    total_copied = 0
    total_skipped = 0
    all_warnings: list[str] = []

    for group in ASSET_GROUPS:
        print(f"--- {group['label']} ({group['name']}) ---")

        if group["name"] == "skills":
            copied, skipped, warnings = build_skills_group(
                group, lang, output_root, args.dry_run, args.verbose,
            )
        elif group["name"] in ("courses", "manifest"):
            copied, skipped, warnings = build_courses_group(
                group, lang, output_root, args.dry_run, args.verbose,
            )
        else:
            copied, skipped, warnings = build_simple_group(
                group, lang, output_root, args.dry_run, args.verbose,
            )

        print(f"  Copied: {copied}  Skipped: {skipped}")
        for w in warnings:
            print(w, file=sys.stderr)
        print()

        total_copied += copied
        total_skipped += skipped
        all_warnings.extend(warnings)

    print("=== Build Summary ===")
    print(f"Language: {lang}")
    print(f"Output:   {output_root}")
    print(f"Copied:   {total_copied}")
    print(f"Skipped:  {total_skipped}")

    if args.dry_run:
        print("\n[DRY RUN] No files were written.")

    if args.strict and total_skipped > 0:
        print(f"\nERROR: {total_skipped} translations missing (--strict mode)", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
