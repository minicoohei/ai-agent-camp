#!/usr/bin/env python3
"""Migrate course/modules/ local paths to external URLs.

Replaces all references to course/modules/{N}-{name}/... with
https://ai-agent.camp/ja/course/module-{N}

Special case: course/modules/11-agent/ → module-7 (renumbering)
"""

import re
import sys
from pathlib import Path

BASE_URL = "https://ai-agent.camp/ja/course"

# Special renumbering: old dir number → new module number
RENUMBER_MAP = {
    "11": "7",  # 11-agent → module-7 (used by start-7-* commands)
}

# Pattern: captures optional ../ prefixes, then course/modules/{N}-{name}/{anything}.html
# Also captures plain text references without ../ prefix
PATTERN = re.compile(
    r'(?:\.\./)*(course/modules/(\d+)-[\w-]+/[\w./-]*\.html)'
)


def replace_match(m: re.Match) -> str:
    full_path = m.group(1)
    module_num = m.group(2)
    # Apply renumbering if needed
    mapped_num = RENUMBER_MAP.get(module_num, module_num)
    return f"{BASE_URL}/module-{mapped_num}"


def process_file(filepath: Path) -> bool:
    """Process a single file. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")
    new_text = PATTERN.sub(replace_match, text)
    if new_text != text:
        filepath.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    repo = Path(__file__).resolve().parent.parent

    # Directories to scan
    scan_dirs = [
        repo / ".claude" / "commands" / "lesson",
        repo / ".cursor" / "commands" / "lesson",
        repo / "courses",
        repo / "course",
        repo / "tools",
        repo / "docs",
        repo / "skills",
        repo / ".claude" / "skills",
        repo / "tests",
    ]

    # File extensions to process
    extensions = {".md", ".yaml", ".yml", ".html", ".py", ".json"}

    modified = []
    scanned = 0

    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for filepath in scan_dir.rglob("*"):
            if filepath.is_file() and filepath.suffix in extensions:
                scanned += 1
                if process_file(filepath):
                    modified.append(str(filepath.relative_to(repo)))

    print(f"Scanned: {scanned} files")
    print(f"Modified: {len(modified)} files")
    for f in sorted(modified):
        print(f"  {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
