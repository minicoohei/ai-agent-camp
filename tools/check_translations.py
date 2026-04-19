#!/usr/bin/env python3
"""Translation coverage checker for i18n migration.

Scans all translatable directories and reports missing or stale translations.

Usage:
    uv run python tools/check_translations.py [--lang en|es|all] [--verbose] [--json]

Exit codes:
    0 — all translations present and up-to-date
    1 — missing or stale translations found
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from i18n_utils import (
    ASSET_GROUPS,
    DEFAULT_LANG,
    PROJECT_ROOT,
    SUPPORTED_LANGS,
    get_base_files_for_group,
    get_lang_variant_path,
)


@dataclass
class FileStatus:
    base_file: Path
    lang: str
    translated_file: Path
    exists: bool
    stale: bool  # True if base is newer than translation


@dataclass
class GroupReport:
    name: str
    label: str
    lang: str
    total: int = 0
    translated: int = 0
    missing: int = 0
    stale: int = 0
    files: list[FileStatus] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return (self.translated / self.total * 100) if self.total else 100.0


def check_group(group: dict, lang: str) -> GroupReport:
    """Check translation coverage for one asset group and language."""
    base_files = get_base_files_for_group(group)
    report = GroupReport(
        name=group["name"],
        label=group["label"],
        lang=lang,
        total=len(base_files),
    )

    for base_file in base_files:
        translated_file = get_lang_variant_path(base_file, lang)
        exists = translated_file.exists()
        stale = False

        if exists:
            base_mtime = base_file.stat().st_mtime
            trans_mtime = translated_file.stat().st_mtime
            stale = base_mtime > trans_mtime

        status = FileStatus(
            base_file=base_file,
            lang=lang,
            translated_file=translated_file,
            exists=exists,
            stale=stale,
        )
        report.files.append(status)

        if not exists:
            report.missing += 1
        elif stale:
            report.stale += 1
            report.translated += 1
        else:
            report.translated += 1

    return report


def format_table(reports: list[GroupReport], verbose: bool = False) -> str:
    """Format reports as a human-readable table."""
    lines: list[str] = []

    for report in reports:
        lines.append(f"--- {report.label} ({report.name}) ---")
        lines.append(
            f"  Total: {report.total}  "
            f"Translated: {report.translated}  "
            f"Missing: {report.missing}  "
            f"Stale: {report.stale}"
        )
        lines.append(f"  Coverage: {report.coverage:.1f}%")

        if verbose:
            for fs in report.files:
                if not fs.exists:
                    rel = fs.translated_file.relative_to(PROJECT_ROOT)
                    lines.append(f"    MISSING: {rel}")
                elif fs.stale:
                    rel = fs.translated_file.relative_to(PROJECT_ROOT)
                    lines.append(f"    STALE:   {rel}")
        lines.append("")

    return "\n".join(lines)


def format_summary(reports: list[GroupReport]) -> str:
    """Format a one-line summary across all groups."""
    total = sum(r.total for r in reports)
    translated = sum(r.translated for r in reports)
    missing = sum(r.missing for r in reports)
    stale = sum(r.stale for r in reports)
    coverage = (translated / total * 100) if total else 100.0
    return (
        f"Total: {total}  Translated: {translated}  "
        f"Missing: {missing}  Stale: {stale}  "
        f"Coverage: {coverage:.1f}%"
    )


def to_json(reports: list[GroupReport]) -> dict:
    """Convert reports to a JSON-serialisable dict."""
    groups = []
    for r in reports:
        g = {
            "name": r.name,
            "label": r.label,
            "lang": r.lang,
            "total": r.total,
            "translated": r.translated,
            "missing": r.missing,
            "stale": r.stale,
            "coverage": round(r.coverage, 1),
            "files": {
                "missing": [
                    str(fs.translated_file.relative_to(PROJECT_ROOT))
                    for fs in r.files if not fs.exists
                ],
                "stale": [
                    str(fs.translated_file.relative_to(PROJECT_ROOT))
                    for fs in r.files if fs.stale
                ],
            },
        }
        groups.append(g)

    total = sum(r.total for r in reports)
    translated = sum(r.translated for r in reports)
    return {
        "groups": groups,
        "summary": {
            "total": total,
            "translated": translated,
            "missing": sum(r.missing for r in reports),
            "stale": sum(r.stale for r in reports),
            "coverage": round(translated / total * 100, 1) if total else 100.0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check translation coverage for i18n migration."
    )
    parser.add_argument(
        "--lang",
        choices=["en", "es", "all"],
        default="all",
        help="Language to check (default: all)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show individual missing/stale files",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output as JSON",
    )
    parser.add_argument(
        "--ignore-stale",
        action="store_true",
        help="Do not fail on stale translations (only fail on missing)",
    )
    args = parser.parse_args()

    langs = [l for l in SUPPORTED_LANGS if l != DEFAULT_LANG]
    if args.lang != "all":
        langs = [args.lang]

    all_reports: list[GroupReport] = []

    for lang in langs:
        for group in ASSET_GROUPS:
            report = check_group(group, lang)
            all_reports.append(report)

    if args.json_output:
        print(json.dumps(to_json(all_reports), indent=2, ensure_ascii=False))
    else:
        for lang in langs:
            lang_reports = [r for r in all_reports if r.lang == lang]
            print(f"=== Translation Coverage: {lang.upper()} ===\n")
            print(format_table(lang_reports, verbose=args.verbose))
            print(f"=== Summary ({lang.upper()}) ===")
            print(format_summary(lang_reports))
            print()

    # Exit code: 1 if any missing (or stale, unless --ignore-stale)
    if args.ignore_stale:
        has_issues = any(r.missing > 0 for r in all_reports)
    else:
        has_issues = any(r.missing > 0 or r.stale > 0 for r in all_reports)
    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
