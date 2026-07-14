"""Tests for executable references and fatality in verify_skill_metadata.py."""

from tests.conftest import import_module_from_repo


def load_module():
    return import_module_from_repo(
        "verify_skill_metadata_under_test", "tools/verify_skill_metadata.py"
    )


def test_extracts_python_bash_and_inline_commands():
    mod = load_module()
    content = """
```bash
python scripts/run.py --flag
uv run python tools/check.py
bash skills/example/scripts/setup.sh
```
Use `python3 scripts/inspect.py input.csv` when debugging.
python3 --version
sh "$SCRIPT_DIR/dynamic.sh"
"""

    assert mod.extract_executable_script_paths(content) == [
        "scripts/inspect.py",
        "scripts/run.py",
        "skills/example/scripts/setup.sh",
        "tools/check.py",
    ]


def test_checks_repo_root_and_skill_relative_paths(tmp_path):
    mod = load_module()
    skill_dir = tmp_path / "skills" / "example"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "scripts" / "local.py").write_text("pass\n", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "root.py").write_text("pass\n", encoding="utf-8")

    results = mod.check_executable_script_references(
        skill_dir,
        "python scripts/local.py\npython tools/root.py\nbash scripts/missing.sh\n",
        tmp_path,
    )

    assert [(item["reference"], item["status"]) for item in results] == [
        ("scripts/local.py", "OK"),
        ("scripts/missing.sh", "BROKEN"),
        ("tools/root.py", "OK"),
    ]


def test_allowlist_suppresses_only_named_skills(monkeypatch):
    mod = load_module()
    monkeypatch.setattr(mod, "MISSING_EXECUTABLE_ALLOWLIST", {"excluded-skill"})
    skills = [
        {"name": "excluded-skill", "missing_executable_scripts": ["scripts/qa.sh"]},
        {"name": "healthy-skill", "missing_executable_scripts": ["scripts/missing.py"]},
    ]

    assert mod.fatal_script_issues(skills) == [
        {"skill": "healthy-skill", "references": ["scripts/missing.py"]}
    ]


def test_production_allowlist_is_empty():
    # P2 (PR #77) で全スキルの参照を修理済み。ここが増える場合は理由を確認すること。
    mod = load_module()
    assert mod.MISSING_EXECUTABLE_ALLOWLIST == set()


def test_exit_code_branches_on_unallowlisted_missing_script(monkeypatch):
    mod = load_module()
    monkeypatch.setattr(mod, "MISSING_EXECUTABLE_ALLOWLIST", {"excluded-skill"})
    legacy_only = [{"name": "legacy", "issues": ["few-sections"]}]
    allowlisted = [
        {"name": "excluded-skill", "missing_executable_scripts": ["missing.py"]}
    ]
    fatal = [{"name": "new-skill", "missing_executable_scripts": ["missing.py"]}]

    assert mod.exit_code_for_skills(legacy_only) == 0
    assert mod.exit_code_for_skills(allowlisted) == 0
    assert mod.exit_code_for_skills(fatal) == 1
