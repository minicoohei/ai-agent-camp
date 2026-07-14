"""Pytest bridge for the structural checks in tools/test_all_lessons.py."""

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
