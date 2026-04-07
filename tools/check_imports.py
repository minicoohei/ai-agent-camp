#!/usr/bin/env python3
"""Verify import consistency between requirements.txt and codebase.

Checks that Python files under tools/ and skills/ do not use
banned or deprecated import patterns. Currently checks:

1. No `import google.generativeai` (old SDK, replaced by google-genai)
2. No `from google.generativeai` (old SDK)

Excludes sync-data helper subdirectories from scanning.

Usage:
    uv run python tools/check_imports.py          # Run all checks
    uv run python tools/check_imports.py --verbose # Show scanned file count per directory
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Directories to scan for Python files
SCAN_DIRS = [
    PROJECT_ROOT / "tools",
    PROJECT_ROOT / "skills",
    PROJECT_ROOT / "examples",
]

# Directories to exclude (data directories, generated files, etc.)
EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules"}

# ---------------------------------------------------------------------------
# Banned import patterns
# ---------------------------------------------------------------------------
# Each entry: (compiled regex, human-readable description, suggested fix)
BANNED_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    (
        re.compile(r'^\s*import\s+google\.generativeai\b'),
        "import google.generativeai (deprecated old SDK)",
        "Use: from google import genai  (google-genai package)",
    ),
    (
        re.compile(r'^\s*from\s+google\.generativeai\b'),
        "from google.generativeai (deprecated old SDK)",
        "Use: from google import genai  (google-genai package)",
    ),
]

# ---------------------------------------------------------------------------
# Known package-name to import-name mappings (for reference / future checks)
# ---------------------------------------------------------------------------
PACKAGE_IMPORT_MAP = {
    "google-genai": "google.genai",          # from google import genai
    "beautifulsoup4": "bs4",
    "Pillow": "PIL",
    "opencv-python": "cv2",
    "python-pptx": "pptx",
    "python-docx": "docx",
    "PyPDF2": "PyPDF2",
    "python-dotenv": "dotenv",
    "PyYAML": "yaml",
    "scikit-learn": "sklearn",
    "slack-sdk": "slack_sdk",
    "notion-client": "notion_client",
}


def iter_python_files() -> list[Path]:
    """Collect all .py files under SCAN_DIRS, excluding EXCLUDE_DIRS."""
    files: list[Path] = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for py_file in sorted(scan_dir.rglob("*.py")):
            # Skip excluded directories
            if any(part in EXCLUDE_DIRS for part in py_file.relative_to(PROJECT_ROOT).parts):
                continue
            files.append(py_file)
    return files


def check_banned_imports(files: list[Path]) -> list[dict]:
    """Scan files for banned import patterns. Returns list of violations."""
    violations: list[dict] = []

    for py_file in files:
        try:
            text = py_file.read_text(encoding="utf-8")
        except OSError:
            continue

        rel_path = py_file.relative_to(PROJECT_ROOT)

        for lineno, line in enumerate(text.splitlines(), 1):
            # Skip comments
            stripped = line.lstrip()
            if stripped.startswith("#"):
                continue

            for pattern, description, fix in BANNED_PATTERNS:
                if pattern.search(line):
                    violations.append({
                        "file": str(rel_path),
                        "line": lineno,
                        "description": description,
                        "fix": fix,
                        "content": line.rstrip(),
                    })

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan Python files for banned/deprecated import patterns."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show scanned file count per directory",
    )
    args = parser.parse_args()
    verbose = args.verbose

    # Collect Python files
    files = iter_python_files()
    if verbose:
        print(f"Scanning {len(files)} Python file(s) ...")
        for scan_dir in SCAN_DIRS:
            count = sum(1 for f in files if str(f).startswith(str(scan_dir)))
            rel = scan_dir.relative_to(PROJECT_ROOT)
            print(f"  {rel}/: {count} file(s)")
        print()

    # Run banned-import checks
    violations = check_banned_imports(files)

    # Report results
    if violations:
        for v in violations:
            print(f"ERROR: {v['file']}:{v['line']} - {v['description']}")
            print(f"  {v['content']}")
            print(f"  Fix: {v['fix']}")
            print()

        print(f"FAIL: {len(violations)} banned import(s) found in {len(files)} file(s).")
        return 1

    print(f"OK: {len(files)} Python file(s) checked, no banned imports found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
