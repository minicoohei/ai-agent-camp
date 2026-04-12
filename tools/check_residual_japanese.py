#!/usr/bin/env python3
"""Detect residual Japanese text in en/es translation files.

Scans .en.md, .es.md, .en.yaml, .es.yaml files for leftover Japanese text
that should have been translated.

Usage:
    python tools/check_residual_japanese.py [--verbose]

Exit codes:
    0 — no residual Japanese found
    1 — residual Japanese detected
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from i18n_utils import ASSET_GROUPS, LANG_SUFFIX_RE, PROJECT_ROOT

# 3+ consecutive CJK characters (Hiragana, Katakana, CJK Unified, CJK Ext A)
CJK_RUN_RE = re.compile(
    r"[\u3040-\u30FF\u4E00-\u9FFF\u3400-\u4DBF]{3,}"
)

# Patterns to exclude from detection
FRONTMATTER_RE = re.compile(r"^---\s*$")
TRIGGERS_KEY_RE = re.compile(r"^\s*triggers:\s*$")
TRIGGER_ITEM_RE = re.compile(r"^\s*-\s*[\"'].*[\"']\s*$")
CODE_FENCE_RE = re.compile(r"^```")


@dataclass
class Finding:
    file: Path
    line_num: int
    line: str
    matches: list[str]


def scan_file(path: Path) -> list[Finding]:
    """Scan a single file for residual Japanese text."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    findings: list[Finding] = []
    in_code_block = False
    in_triggers = False
    in_frontmatter = False
    frontmatter_count = 0

    for i, line in enumerate(content.splitlines(), 1):
        # Track frontmatter boundaries
        if FRONTMATTER_RE.match(line):
            frontmatter_count += 1
            in_frontmatter = frontmatter_count == 1
            if frontmatter_count == 2:
                in_frontmatter = False
                in_triggers = False
            continue

        # Track triggers section in frontmatter (Japanese triggers are intentional)
        if in_frontmatter:
            if TRIGGERS_KEY_RE.match(line):
                in_triggers = True
                continue
            if in_triggers:
                if TRIGGER_ITEM_RE.match(line):
                    continue
                if not line.startswith(" ") and not line.startswith("\t"):
                    in_triggers = False

        # Track code blocks (Japanese in code comments may be intentional)
        if CODE_FENCE_RE.match(line):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Skip triggers array items
        if in_triggers:
            continue

        # Detect CJK runs
        matches = CJK_RUN_RE.findall(line)
        if matches:
            findings.append(Finding(
                file=path, line_num=i, line=line.strip(), matches=matches,
            ))

    return findings


def collect_translation_files() -> list[Path]:
    """Collect all en/es translation files from asset groups."""
    files: list[Path] = []

    for group in ASSET_GROUPS:
        source_dir = PROJECT_ROOT / group["source"]
        if not source_dir.exists():
            continue

        pattern = group["pattern"]
        recursive = group.get("recursive", False)

        # Collect language-suffixed files
        for lang in ("en", "es"):
            stem, ext = pattern.rsplit(".", 1) if "." in pattern else (pattern, "")
            lang_pattern = f"{stem}.{lang}.{ext}" if ext else f"{stem}.{lang}"

            if recursive:
                found = sorted(source_dir.rglob(lang_pattern))
            else:
                found = sorted(source_dir.glob(lang_pattern))

            files.extend(f for f in found if f.is_file())

        # Also check output directories for synced copies
        for output_path in group.get("outputs", []):
            output_dir = PROJECT_ROOT / output_path
            if output_dir == source_dir or not output_dir.exists():
                continue
            for lang in ("en", "es"):
                stem, ext = pattern.rsplit(".", 1) if "." in pattern else (pattern, "")
                lang_pattern = f"{stem}.{lang}.{ext}" if ext else f"{stem}.{lang}"

                if recursive:
                    found = sorted(output_dir.rglob(lang_pattern))
                else:
                    found = sorted(output_dir.glob(lang_pattern))

                files.extend(f for f in found if f.is_file())

    # Deduplicate
    seen = set()
    unique = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)

    return unique


def main():
    parser = argparse.ArgumentParser(description="Detect residual Japanese in translations")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show each finding")
    args = parser.parse_args()

    files = collect_translation_files()
    print(f"Scanning {len(files)} translation files...")

    all_findings: list[Finding] = []
    files_with_issues: set[Path] = set()

    for f in files:
        findings = scan_file(f)
        if findings:
            all_findings.extend(findings)
            files_with_issues.add(f)

    if all_findings:
        print(f"\nFound {len(all_findings)} residual Japanese occurrences in {len(files_with_issues)} files:\n")
        if args.verbose:
            for finding in all_findings:
                rel = finding.file.relative_to(PROJECT_ROOT)
                print(f"  {rel}:{finding.line_num}")
                print(f"    {finding.line[:120]}")
                print(f"    matches: {finding.matches}")
                print()
        else:
            for f in sorted(files_with_issues):
                rel = f.relative_to(PROJECT_ROOT)
                count = sum(1 for fd in all_findings if fd.file == f)
                print(f"  {rel} ({count} occurrences)")
            print(f"\nRun with --verbose for details.")

        sys.exit(1)
    else:
        print("No residual Japanese found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
