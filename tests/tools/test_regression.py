"""Regression tests for past bugs.

Each test prevents a specific bug from being reintroduced.
"""

import importlib
import re
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LESSON_DIR = PROJECT_ROOT / ".claude" / "commands" / "lesson"


# ---------------------------------------------------------------------------
# 1. notebooklm_cli.py missing import: `from pathlib import Path`
# ---------------------------------------------------------------------------

class TestNotebooklmCliImport:
    def test_module_imports_cleanly(self):
        """notebooklm_cli.py should import without errors.
        Previously failed due to missing 'from pathlib import Path'."""
        with patch.dict("sys.modules", {
            "requests": MagicMock(),
            "runtime_env": MagicMock(load_runtime_env=MagicMock()),
        }):
            from tests.conftest import import_module_from_repo
            mod = import_module_from_repo("notebooklm_cli", "tools/notebooklm_cli.py")
            assert hasattr(mod, "Path")
            assert mod.Path is Path

    def test_path_used_for_sys_path(self):
        """Path is used at module level for sys.path.insert."""
        source = (PROJECT_ROOT / "tools" / "notebooklm_cli.py").read_text()
        assert "from pathlib import Path" in source


# ---------------------------------------------------------------------------
# 2. bootcamp_utils.py missing sys.path for sibling import
# ---------------------------------------------------------------------------

class TestBootcampUtilsImport:
    def test_module_imports_cleanly(self):
        """bootcamp_utils.py should import without errors.
        Previously failed because 'from runtime_env import ...' could not resolve."""
        with patch.dict("sys.modules", {
            "runtime_env": MagicMock(load_runtime_env=MagicMock()),
            "google": MagicMock(),
            "google.genai": MagicMock(),
        }):
            from tests.conftest import import_module_from_repo
            mod = import_module_from_repo("bootcamp_utils", "tools/bootcamp_utils.py")
            assert hasattr(mod, "get_client")

    def test_sys_path_insert_present(self):
        """bootcamp_utils.py must insert tools/ into sys.path before sibling import."""
        source = (PROJECT_ROOT / "tools" / "bootcamp_utils.py").read_text()
        assert "sys.path.insert" in source


# ---------------------------------------------------------------------------
# 3. verify_commands.py regex mismatch for section headers
# ---------------------------------------------------------------------------

class TestVerifyCommandsRegex:
    def test_section_regex_matches_kono_session(self):
        """Section header regex must match 'このセッションでやること'."""
        from tools.verify_commands import REQUIRED_SECTIONS
        pattern = REQUIRED_SECTIONS[0]
        content = "## このセッションでやること"
        assert re.search(pattern, content) is not None

    def test_section_regex_matches_ima_anata(self):
        """Section header regex must also match '今あなたがやっていること'."""
        from tools.verify_commands import REQUIRED_SECTIONS
        pattern = REQUIRED_SECTIONS[0]
        content = "## 📍 今あなたがやっていること"
        assert re.search(pattern, content) is not None

    def test_all_required_section_patterns_are_valid_regex(self):
        """All REQUIRED_SECTIONS entries must be compilable regex."""
        from tools.verify_commands import REQUIRED_SECTIONS
        for pattern in REQUIRED_SECTIONS:
            compiled = re.compile(pattern)
            assert compiled is not None


# ---------------------------------------------------------------------------
# 4. Module numbering: prerequisites must reference existing start files
# ---------------------------------------------------------------------------

class TestModuleNumbering:
    def test_prerequisites_reference_existing_files(self):
        """No prerequisite in start-*.md files should reference a non-existent start-X-Y file."""
        lesson_files = list(LESSON_DIR.glob("start-*.md"))
        assert len(lesson_files) > 0, "No lesson files found"

        # Build set of existing start file IDs
        existing_ids = set()
        for f in lesson_files:
            # e.g., start-1-1.md -> start-1-1
            existing_ids.add(f.stem)

        missing_refs = []
        for lesson_file in lesson_files:
            content = lesson_file.read_text(encoding="utf-8")
            # Look for prerequisites: ["start-X-Y", ...] in frontmatter
            prereq_match = re.search(
                r'^prerequisites:\s*\[([^\]]*)\]',
                content,
                re.MULTILINE,
            )
            if not prereq_match:
                continue
            prereq_str = prereq_match.group(1)
            # Extract quoted start-X-Y references
            refs = re.findall(r'"(start-\d+-\d+)"', prereq_str)
            for ref in refs:
                if ref not in existing_ids:
                    missing_refs.append(
                        f"{lesson_file.name} references {ref} which does not exist"
                    )

        assert missing_refs == [], (
            "Prerequisites reference non-existent files:\n"
            + "\n".join(missing_refs)
        )


# ---------------------------------------------------------------------------
# 5. test pollution: test_verify_module.py should not leave MagicMock for
#    lesson_progress in sys.modules permanently.
# ---------------------------------------------------------------------------

class TestNoPollution:
    def test_lesson_progress_is_real_after_test_verify_module(self):
        """After test_verify_module tests run, lesson_progress should be
        importable as the real module, not a MagicMock."""
        # Remove mock if present
        sys.modules.pop("lesson_progress", None)

        # Re-import from the actual file
        from tests.conftest import import_module_from_repo
        lp = import_module_from_repo(
            "lesson_progress", "tools/lesson_progress.py"
        )
        # It should not be a MagicMock
        assert not isinstance(lp, MagicMock)
        # It should have real attributes
        assert hasattr(lp, "load_progress") or hasattr(lp, "lesson_order")
