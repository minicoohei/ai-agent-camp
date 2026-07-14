"""Pytest bridge for the structural checks in tools/test_all_lessons.py."""

from pathlib import Path

import yaml

from tests.conftest import import_module_from_repo


def test_lesson_mirror_and_manifest_integrity():
    mod = import_module_from_repo("all_lessons_runner", "tools/test_all_lessons.py")

    mod.check_mirror()
    mod.check_manifest()

    failures = [
        item
        for category in ("mirror_check", "manifest_check")
        for item in mod.results[category]
        if item["status"] == "FAIL"
    ]
    assert failures == []


def test_localized_manifests_cover_all_lesson_commands():
    root = Path(__file__).parents[2]
    command_ids = {
        path.stem.removesuffix(".en").removesuffix(".es")
        for path in (root / ".cursor/commands/lesson").glob("*.md")
    }
    manifest_paths = [
        root / "courses/lessons.manifest.yaml",
        root / "courses/lessons.manifest.en.yaml",
        root / "courses/lessons.manifest.es.yaml",
    ]

    for manifest_path in manifest_paths:
        entries = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest_ids = [entry["lessonId"] for entry in entries]
        assert len(manifest_ids) == len(set(manifest_ids))
        assert set(manifest_ids) == command_ids
