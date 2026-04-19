#!/usr/bin/env python3
"""Verify consistency between CURRICULUM.md and MODULES_GUIDE.md.

Checks:
1. Module numbers and names in CURRICULUM.md Phase 3 table
2. Module numbers and names in MODULES_GUIDE.md Module Overview
3. Cross-references between the two documents

Usage:
    uv run python tools/check_module_consistency.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = PROJECT_ROOT / "course" / "CURRICULUM.md"
MODULES_GUIDE_PATH = PROJECT_ROOT / "course" / "MODULES_GUIDE.md"

# Match rows in CURRICULUM.md Phase 3 table:
#   | 1 | バナー・画像生成 | 90分 | 3 | `/start-1-1` ~ `/start-1-3` |
CURRICULUM_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|"   # module number
    r"\s*(.+?)\s*\|"      # module name
)

# Match headers in MODULES_GUIDE.md:
#   ### Module 1: バナー・画像生成 (Banner & Image Generation)
MODULE_HEADER_RE = re.compile(
    r"^###\s+Module\s+(\d+)\s*:\s*(.+?)\s*\(.*\)\s*$"
)

# Also handle headers without English name in parens:
#   ### Module 1: バナー・画像生成
MODULE_HEADER_NOPAREN_RE = re.compile(
    r"^###\s+Module\s+(\d+)\s*:\s*(.+?)\s*$"
)


def parse_curriculum(text: str) -> dict[int, str]:
    """Parse Phase 3 Core Modules table from CURRICULUM.md.

    Returns dict mapping module number -> module name.
    """
    modules: dict[int, str] = {}
    in_phase3 = False

    for line in text.splitlines():
        # Detect the Phase 3 section
        if "Phase 3" in line and "コアスキル" in line:
            in_phase3 = True
            continue

        # Stop at the next section (--- or ## heading)
        if in_phase3 and (line.startswith("## ") or line.startswith("---")):
            break

        if not in_phase3:
            continue

        # Skip header/separator rows
        if line.startswith("|--") or line.startswith("| モジュール") or line.startswith("| -"):
            continue

        m = CURRICULUM_ROW_RE.match(line)
        if m:
            num = int(m.group(1))
            name = m.group(2).strip()
            modules[num] = name

    return modules


def parse_modules_guide(text: str) -> dict[int, str]:
    """Parse Module Overview headers from MODULES_GUIDE.md.

    Returns dict mapping module number -> module name (Japanese part only).
    """
    modules: dict[int, str] = {}

    for line in text.splitlines():
        # Try with English name in parens first
        m = MODULE_HEADER_RE.match(line)
        if m:
            num = int(m.group(1))
            name = m.group(2).strip()
            modules[num] = name
            continue

        # Fallback: no parens
        m = MODULE_HEADER_NOPAREN_RE.match(line)
        if m:
            num = int(m.group(1))
            name = m.group(2).strip()
            modules[num] = name

    return modules



def main() -> int:
    errors: list[str] = []

    # --- Load files ---
    if not CURRICULUM_PATH.exists():
        print(f"FAIL: {CURRICULUM_PATH.relative_to(PROJECT_ROOT)} not found")
        return 1
    if not MODULES_GUIDE_PATH.exists():
        print(f"FAIL: {MODULES_GUIDE_PATH.relative_to(PROJECT_ROOT)} not found")
        return 1

    curriculum_text = CURRICULUM_PATH.read_text(encoding="utf-8")
    guide_text = MODULES_GUIDE_PATH.read_text(encoding="utf-8")

    # --- Parse ---
    curriculum_modules = parse_curriculum(curriculum_text)
    guide_modules = parse_modules_guide(guide_text)
    print(f"CURRICULUM.md Phase 3 modules: {len(curriculum_modules)}")
    print(f"MODULES_GUIDE.md modules:      {len(guide_modules)}")
    print()

    curriculum_nums = set(curriculum_modules.keys())
    guide_nums = set(guide_modules.keys())

    # --- Check 1: Modules in CURRICULUM but not in MODULES_GUIDE ---
    only_curriculum = sorted(curriculum_nums - guide_nums)
    if only_curriculum:
        for num in only_curriculum:
            msg = (
                f"Module {num} ({curriculum_modules[num]}) is in CURRICULUM.md "
                f"but missing from MODULES_GUIDE.md"
            )
            errors.append(msg)
            print(f"FAIL: {msg}")
    else:
        print("OK: All CURRICULUM.md modules are present in MODULES_GUIDE.md")

    # --- Check 2: Modules in MODULES_GUIDE but not in CURRICULUM ---
    # Module 0 is in Phase 2 (Setup), not Phase 3 (Core), so it's expected
    # to be absent from the Core Modules table.
    phase2_modules = {0}
    only_guide = sorted((guide_nums - curriculum_nums) - phase2_modules)
    if only_guide:
        for num in only_guide:
            msg = (
                f"Module {num} ({guide_modules[num]}) is in MODULES_GUIDE.md "
                f"but missing from CURRICULUM.md"
            )
            errors.append(msg)
            print(f"FAIL: {msg}")
    else:
        print("OK: All MODULES_GUIDE.md modules are present in CURRICULUM.md")

    # --- Check 3: Name mismatches ---
    common_nums = sorted(curriculum_nums & guide_nums)
    name_mismatches = []
    for num in common_nums:
        c_name = curriculum_modules[num]
        g_name = guide_modules[num]
        if c_name != g_name:
            name_mismatches.append((num, c_name, g_name))

    if name_mismatches:
        for num, c_name, g_name in name_mismatches:
            msg = (
                f"Module {num} name mismatch: "
                f"CURRICULUM.md=\"{c_name}\" vs MODULES_GUIDE.md=\"{g_name}\""
            )
            errors.append(msg)
            print(f"FAIL: {msg}")
    else:
        print(f"OK: All {len(common_nums)} common module names are consistent")

    # --- Summary ---
    print()
    if errors:
        print(f"FAIL: {len(errors)} error(s) found")
        return 1
    else:
        print("OK: All module consistency checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
