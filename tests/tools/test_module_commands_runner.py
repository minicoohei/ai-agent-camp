"""Pytest bridge for stable checks in tools/test_module_commands.py."""

from tests.conftest import import_module_from_repo


def test_module_command_metadata_references_and_mirrors():
    mod = import_module_from_repo("module_commands_runner", "tools/test_module_commands.py")
    filenames = [
        *(f"start-4-{index}.md" for index in range(1, 8)),
        *(f"start-7-{index}.md" for index in range(1, 5)),
    ]
    failures = []

    for filename in filenames:
        path = mod.ROOT / ".cursor" / "commands" / "lesson" / filename
        content = path.read_text(encoding="utf-8")
        checks = [
            mod.test_file_exists(path),
            *mod.test_yaml_frontmatter(content, filename),
            *mod.test_prerequisite_files_exist(content),
            *mod.test_next_lesson_reference(content),
            *mod.test_referenced_paths(content),
            *mod.test_cursor_claude_parity(filename),
        ]
        failures.extend(
            f"{filename}: {check.name}: {check.detail}"
            for check in checks
            if not check.passed
        )

    assert failures == []
