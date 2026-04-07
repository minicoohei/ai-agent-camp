#!/usr/bin/env python3
"""E2E checks that course-displayed commands dispatch to the expected Codex handler."""

from __future__ import annotations

import os
import unittest
from pathlib import Path

from codex_commands import ROOT, resolve_command


COURSE_ROOT = Path(
    os.environ.get("AIAGENT_COURSE_ROOT", str(ROOT.parent / "aiagent-course"))
)


class CourseCodexParityTests(unittest.TestCase):
    def test_course_repo_exists(self) -> None:
        self.assertTrue(COURSE_ROOT.exists(), "aiagent-course repo not found next to aiagent-base")

    def test_codex_only_copy_is_removed_from_runtime_components(self) -> None:
        files = [
            COURSE_ROOT / "src/app/[locale]/onboarding/_components/steps/LearningFlowStep.tsx",
            COURSE_ROOT / "src/app/[locale]/onboarding/_components/steps/CodexSetupStep.tsx",
        ]

        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("step2TitleCodex", text)
            self.assertNotIn("step2DescCodex", text)
            self.assertNotIn("codexRunnerDesc", text)

    def test_representative_course_commands_dispatch(self) -> None:
        representative = {
            "/start-0-1": "aiagent-lesson-runner",
            "/start-5-1": "aiagent-lesson-runner",
            "/start-17-1": "aiagent-lesson-runner",
            "/guide": "aiagent-utility-runner",
            "/setup-api-key": "aiagent-utility-runner",
            "/generate-slide": "aiagent-utility-runner",
        }

        course_files = [
            COURSE_ROOT / "src",
            COURSE_ROOT / "messages",
        ]

        corpus = []
        for base in course_files:
            for path in base.rglob("*"):
                if path.is_file() and path.suffix in {".ts", ".tsx", ".json"}:
                    corpus.append(path.read_text(encoding="utf-8"))
        full_text = "\n".join(corpus)

        for command, expected_handler in representative.items():
            self.assertIn(command, full_text, msg=f"{command} must be displayed in aiagent-course")
            resolved = resolve_command(command)
            self.assertTrue(resolved["ok"], msg=f"{command} should resolve in Codex")
            self.assertEqual(resolved["handler"], expected_handler)

    def test_alias_and_unmapped_e2e_cases(self) -> None:
        alias_cases = {
            "/lesson/start-0-1": "aiagent-lesson-runner",
            "/utility/guide": "aiagent-utility-runner",
        }
        for command, expected_handler in alias_cases.items():
            resolved = resolve_command(command)
            self.assertTrue(resolved["ok"])
            self.assertEqual(resolved["handler"], expected_handler)
            self.assertEqual(resolved["resolvedAlias"], command)

        unmapped = resolve_command("/not-a-real-command")
        self.assertFalse(unmapped["ok"])
        self.assertEqual(unmapped["status"], "unmapped")


if __name__ == "__main__":
    unittest.main()
