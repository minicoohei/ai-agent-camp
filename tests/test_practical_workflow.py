"""Exercise contracts: intentional failures, repaired results and local links.

Run without extra dependencies: python3 -m unittest discover -s tests
    -p test_practical_workflow.py -v
"""

import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/practical-workflow"
STARTER = GUIDE / "starter"


class PracticalWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / "practice"
        shutil.copytree(STARTER, self.work)

    def run_checks(self):
        return subprocess.run(
            [sys.executable, "checks.py"], cwd=self.work,
            capture_output=True, text=True, check=False,
        )

    def repair_copy(self):
        path = self.work / "quote.py"
        source = path.read_text()
        source = source.replace("items[:-1]", "items")
        source = source.replace("subtotal > DISCOUNT_THRESHOLD", "subtotal >= DISCOUNT_THRESHOLD")
        path.write_text(source)

    def test_starter_has_exactly_two_expected_failures(self):
        result = self.run_checks()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ran 4 tests", result.stderr)
        self.assertIn("FAILED (failures=2)", result.stderr)
        self.assertIn("FAIL: test_discount_at_threshold", result.stderr)
        self.assertIn("FAIL: test_subtotal_includes_last_item", result.stderr)

    def test_repair_passes_same_four_checks_without_changing_tests(self):
        before = (self.work / "checks.py").read_bytes()
        self.repair_copy()
        result = self.run_checks()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 4 tests", result.stderr)
        self.assertEqual((self.work / "checks.py").read_bytes(), before)

    def test_skill_fixture_expectations_match_repaired_calculation(self):
        self.repair_copy()
        spec = importlib.util.spec_from_file_location("practice_quote", self.work / "quote.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cases = json.loads((self.work / "cases.json").read_text())
        self.assertEqual([case["id"] for case in cases], ["Q-001", "Q-002"])
        for case, total, difference in zip(cases, [60_500, 104_500], [0, 5_500]):
            with self.subTest(case=case["id"]):
                actual = module.calculate_quote(case["items"])
                self.assertEqual(actual["total"], total)
                self.assertEqual(case["quoted_total"] - actual["total"], difference)
        self.assertEqual(module.calculate_quote([])["total"], 0)
        self.assertEqual(module.calculate_quote([(15, 1)])["tax"], 2)
        self.assertEqual(module.apply_discount(100_010), 95_010)

    def test_workshop_and_entry_links_resolve_inside_repo(self):
        files = list(GUIDE.rglob("*.md")) + [
            ROOT / "README.ja.md", ROOT / "docs/README.md",
            ROOT / "courses/aiagent/lesson01-foundation/ch03-agents/practice/reference.md",
            ROOT / "courses/aiagent/lesson03-core/module06-agent-development/practice/exercise.md",
            ROOT / "courses/aiagent/lesson03-core/module11-github-actions/practice/exercise.md",
            ROOT / "courses/aiagent/lesson03-core/module18-pm-sysdef/practice/exercise.md",
        ]
        for path in files:
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                if not path.is_relative_to(GUIDE) and "practical-workflow" not in target:
                    continue  # Existing unrelated links are outside this change.
                resolved = (path.parent / target.split("#")[0]).resolve()
                with self.subTest(file=path.name, link=target):
                    self.assertTrue(resolved.is_relative_to(ROOT))
                    self.assertTrue(resolved.exists())

    def test_starter_uses_only_local_assets_and_four_states(self):
        html = (STARTER / "design/specimen.html").read_text()
        self.assertEqual(set(re.findall(r'data-state="(.*?)"', html)),
                         {"normal", "empty", "loading", "error"})
        for target in re.findall(r'(?:src|href)="(.*?)"', html):
            self.assertNotIn(":", target)
            self.assertTrue((STARTER / "design" / target).is_file())
        self.assertNotIn("<script", html.lower())


if __name__ == "__main__":
    unittest.main()
