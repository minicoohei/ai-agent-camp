#!/usr/bin/env python3
"""Validation and routing tests for the Codex command manifest."""

from __future__ import annotations

import unittest

from codex_commands import ROOT, build_manifest, iter_command_files, resolve_command


class ManifestCoverageTests(unittest.TestCase):
    def test_every_cursor_command_is_manifested(self) -> None:
        files = iter_command_files()
        entries = build_manifest()
        self.assertEqual(len(entries), len(files))

        source_paths = {entry.sourcePath for entry in entries}
        expected_paths = {str(path.relative_to(ROOT)) for path in files}
        self.assertSetEqual(source_paths, expected_paths)

    def test_aliases_are_unique(self) -> None:
        alias_to_id: dict[str, str] = {}
        for entry in build_manifest():
            self.assertTrue(entry.codexRoute["handler"])
            self.assertTrue(entry.expectedHandler)
            for alias in entry.aliases:
                previous = alias_to_id.get(alias)
                self.assertIsNone(
                    previous,
                    msg=f"Alias collision: {alias} -> {previous}, {entry.canonicalId}",
                )
                alias_to_id[alias] = entry.canonicalId


class RouterResolutionTests(unittest.TestCase):
    def test_start_lesson_route(self) -> None:
        resolved = resolve_command("/start-0-1")
        self.assertTrue(resolved["ok"])
        self.assertEqual(resolved["handler"], "aiagent-lesson-runner")
        self.assertEqual(resolved["target"], "start-0-1")

    def test_nested_lesson_alias_route(self) -> None:
        resolved = resolve_command("/lesson/start-0-1")
        self.assertTrue(resolved["ok"])
        self.assertEqual(resolved["handler"], "aiagent-lesson-runner")
        self.assertEqual(resolved["canonicalId"], "start-0-1")

    def test_utility_route(self) -> None:
        resolved = resolve_command("/guide")
        self.assertTrue(resolved["ok"])
        self.assertEqual(resolved["handler"], "aiagent-utility-runner")
        self.assertEqual(resolved["target"], "guide")

    def test_nested_utility_alias_route(self) -> None:
        resolved = resolve_command("/utility/guide")
        self.assertTrue(resolved["ok"])
        self.assertEqual(resolved["handler"], "aiagent-utility-runner")
        self.assertEqual(resolved["canonicalId"], "guide")

    def test_unmapped_route(self) -> None:
        resolved = resolve_command("/does-not-exist")
        self.assertFalse(resolved["ok"])
        self.assertEqual(resolved["status"], "unmapped")


if __name__ == "__main__":
    unittest.main()
