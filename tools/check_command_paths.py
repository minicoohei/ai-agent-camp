#!/usr/bin/env python3
"""Validate script paths referenced in lesson command files and tools/*.py.

Scans all lesson command files (.cursor/commands/lesson/start-*.md) for
Python script invocations and checks:

1. `python scripts/xxx.py` → ERROR (should be skills/*/scripts/)
2. `uv run python tools/xxx.py` → existence check
3. `python skills/xxx/scripts/yyy.py` → existence check
4. `uv run python tools/ugc/xxx.py` → existence check
5. `python -m xxx` → skipped (module invocations are hard to validate)
6. `python -m venv` / `python -m pip` → skipped (stdlib)

Also scans tools/*.py files for skills/ path references and checks:
- String literals containing `skills/` paths (e.g. `"skills/foo/bar.py"`)
- Path combination patterns (e.g. `project_root / "skills/foo/bar.py"`)

Usage:
    uv run python tools/check_command_paths.py              # Check all lessons
    uv run python tools/check_command_paths.py start-16-2   # Check specific lesson
    uv run python tools/check_command_paths.py --tools      # Check tools/*.py skill refs
    uv run python tools/check_command_paths.py --plugins    # Check external plugin registry URLs
    uv run python tools/check_command_paths.py --all        # Check lessons, tools, and plugins
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"
TOOLS_DIR = PROJECT_ROOT / "tools"

# Match `python[3] [path/to/script.py]` but NOT `python -m ...`
PYTHON_SCRIPT_RE = re.compile(
    r'python[3]?\s+'           # python or python3
    r'(?!-m\s)'               # negative lookahead: skip module invocations
    r'(\S+\.py)'              # capture the script path
)

# Bare `scripts/xxx.py` without `.claude/skills/` prefix
BARE_SCRIPTS_RE = re.compile(r'^scripts/')

# Match skills/ path in string literals: "..." or '...'
SKILL_STRING_LITERAL_RE = re.compile(
    r'["\']'                        # opening quote
    r'(skills/[^"\']+)'            # capture: skills/... up to closing quote
    r'["\']'                        # closing quote
)


def find_python_invocations(text: str) -> list[tuple[int, str]]:
    """Find all python script invocations with line numbers.

    Returns list of (line_number, script_path) tuples.
    """
    results = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in PYTHON_SCRIPT_RE.finditer(line):
            script_path = m.group(1)
            results.append((lineno, script_path))
    return results


def check_file(path: Path) -> tuple[list[dict], list[dict]]:
    """Check a single lesson file for invalid script paths.

    Returns (errors, warnings) where:
    - errors: bare_scripts issues (CI blocker)
    - warnings: not_found issues (informational)
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return ([{
            "file": path.name,
            "line": 0,
            "path": str(path),
            "kind": "read_error",
            "message": f"Failed to read file: {exc}",
        }], [])
    invocations = find_python_invocations(text)
    errors = []
    warnings = []

    for lineno, script_path in invocations:
        # 教材テンプレート内のプレースホルダ例は実在確認の対象外
        if "[" in script_path or script_path in {"main.py", "<skill-name>.py"}:
            continue

        # Rule 1: bare `scripts/xxx.py` is always wrong
        if BARE_SCRIPTS_RE.match(script_path):
            suggestion = _suggest_skill_path(script_path)
            errors.append({
                "file": path.name,
                "line": lineno,
                "path": script_path,
                "kind": "bare_scripts",
                "message": "Bare 'scripts/' path is not allowed. "
                           "Use 'skills/*/scripts/' or 'tools/' instead.",
                "suggestion": suggestion,
            })
            continue

        # Rule 2-4: validate file existence (warning only)
        full_path = PROJECT_ROOT / script_path
        if not full_path.exists():
            warnings.append({
                "file": path.name,
                "line": lineno,
                "path": script_path,
                "kind": "not_found",
                "message": f"Referenced script does not exist: {script_path}",
            })

    return errors, warnings


def _suggest_skill_path(bare_path: str) -> str | None:
    """Try to find the correct skills/*/scripts/ path."""
    filename = Path(bare_path).name
    skills_dir = PROJECT_ROOT / "skills"
    if not skills_dir.exists():
        return None

    try:
        skill_dirs = list(skills_dir.iterdir())
    except OSError:
        return None
    for skill_dir in skill_dirs:
        if not skill_dir.is_dir():
            continue
        candidate = skill_dir / "scripts" / filename
        if candidate.exists():
            return str(candidate.relative_to(PROJECT_ROOT))

    return None


def check_tools_skill_refs() -> list[dict]:
    """Check tools/*.py files for skills/ path references.

    Scans all Python files directly under tools/ (non-recursive) and extracts
    skills/ path references from:
    - String literals: "skills/foo/bar.py" or 'skills/foo/bar.py'
    - Path combination patterns: some_var / "skills/foo/bar.py"

    Returns list of warning dicts for paths that do not exist under PROJECT_ROOT.
    """
    warnings = []
    self_name = Path(__file__).resolve().name
    tool_files = sorted(TOOLS_DIR.glob("*.py"))

    for tool_path in tool_files:
        # Skip self to avoid false positives from docstrings/examples
        if tool_path.name == self_name:
            continue
        try:
            text = tool_path.read_text(encoding="utf-8")
        except OSError as exc:
            warnings.append({
                "file": tool_path.name,
                "line": 0,
                "path": str(tool_path),
                "kind": "read_error",
                "message": f"Failed to read file: {exc}",
            })
            continue

        for lineno, line in enumerate(text.splitlines(), 1):
            for m in SKILL_STRING_LITERAL_RE.finditer(line):
                skill_rel_path = m.group(1)
                full_path = PROJECT_ROOT / skill_rel_path
                if not full_path.exists():
                    warnings.append({
                        "file": tool_path.name,
                        "line": lineno,
                        "path": skill_rel_path,
                        "kind": "not_found",
                        "message": f"Referenced skill path does not exist: {skill_rel_path}",
                    })

    return warnings


def check_plugin_registry() -> list[dict]:
    """Validate external-plugins.yaml: check repo URLs via git ls-remote."""
    registry_path = PROJECT_ROOT / "external-plugins.yaml"
    if not registry_path.exists():
        return [{"file": "external-plugins.yaml", "line": 0, "path": str(registry_path),
                 "message": "Registry file not found"}]

    import shutil
    import subprocess

    try:
        import yaml
    except ImportError:
        return [{"file": "external-plugins.yaml", "line": 0, "path": "",
                 "message": "PyYAML not installed, cannot validate registry"}]

    try:
        with open(registry_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as exc:
        return [{"file": "external-plugins.yaml", "line": 0, "path": "",
                 "message": f"Failed to parse registry: {exc}"}]

    git = shutil.which("git")
    if not git:
        return [{"file": "external-plugins.yaml", "line": 0, "path": "",
                 "message": "git not found, cannot validate URLs"}]

    warnings = []
    plugins = data.get("plugins", {})
    for name, config in plugins.items():
        repo = config.get("repo", "")
        ref = config.get("ref", "main")
        url = f"https://github.com/{repo}.git"
        ret = subprocess.run(
            [git, "ls-remote", "--exit-code", url, ref],
            capture_output=True, text=True, timeout=30,
        )
        if ret.returncode != 0:
            warnings.append({
                "file": "external-plugins.yaml",
                "line": 0,
                "path": f"{repo}@{ref}",
                "message": f"Plugin '{name}': repo or ref not reachable: {url} @ {ref}",
            })
    return warnings


def _run_lesson_checks(target: str | None) -> tuple[list[dict], list[dict], int]:
    """Run lesson file checks and return (errors, warnings, checked_count)."""
    if target:
        files = list(LESSON_DIR.glob(f"{target}.md"))
        if not files:
            print(f"File not found: {target}.md")
            return [], [], 0
    else:
        files = sorted(LESSON_DIR.glob("start-*.md"))

    all_errors: list[dict] = []
    all_warnings: list[dict] = []
    checked = 0

    for path in files:
        checked += 1
        errors, warnings = check_file(path)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    return all_errors, all_warnings, checked


def main() -> int:
    args = sys.argv[1:]

    run_lessons = True
    run_tools = False
    run_plugins = False
    target = None

    if "--all" in args:
        run_lessons = True
        run_tools = True
        run_plugins = True
    elif "--plugins" in args:
        run_lessons = False
        run_plugins = True
    elif "--tools" in args:
        run_lessons = False
        run_tools = True
    else:
        # Positional argument (lesson target) or no argument → lessons only
        for arg in args:
            if not arg.startswith("-"):
                target = arg
                break

    exit_code = 0

    # --- Lesson checks ---
    if run_lessons:
        all_errors, all_warnings, checked = _run_lesson_checks(target)

        if run_lessons and target and checked == 0:
            return 1

        # Print errors (CI blockers)
        for err in all_errors:
            print(f"ERROR: {err['file']}:{err['line']} - {err['path']}")
            print(f"  {err['message']}")
            if err.get("suggestion"):
                print(f"  -> Did you mean: {err['suggestion']}?")
            print()

        # Print warnings (informational)
        for warn in all_warnings:
            print(f"WARN: {warn['file']}:{warn['line']} - {warn['path']}")
            print(f"  {warn['message']}")
            print()

        if all_errors:
            print(f"FAIL: {len(all_errors)} error(s) in {checked} lesson(s)."
                  f" ({len(all_warnings)} warning(s))")
            exit_code = 1
        else:
            msg = f"OK: {checked} lesson(s) checked, 0 error(s) found."
            if all_warnings:
                msg += f" ({len(all_warnings)} warning(s))"
            print(msg)

    # --- Tools skill-ref checks ---
    if run_tools:
        tools_warnings = check_tools_skill_refs()

        for warn in tools_warnings:
            print(f"WARN: {warn['file']}:{warn['line']} - {warn['path']}")
            print(f"  {warn['message']}")
            print()

        tool_files_count = len(list(TOOLS_DIR.glob("*.py")))
        msg = f"OK: {tool_files_count} tool file(s) checked, {len(tools_warnings)} warning(s) found."
        print(msg)

    # --- Plugin registry checks ---
    if run_plugins:
        plugin_warnings = check_plugin_registry()

        for warn in plugin_warnings:
            print(f"WARN: {warn['file']} - {warn['path']}")
            print(f"  {warn['message']}")
            print()

        if plugin_warnings:
            print(f"FAIL: {len(plugin_warnings)} plugin registry error(s) found.")
            exit_code = 1
        else:
            plugins_count = 0
            registry_path = PROJECT_ROOT / "external-plugins.yaml"
            if registry_path.exists():
                try:
                    import yaml
                    with open(registry_path, encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    plugins_count = len(data.get("plugins", {}))
                except Exception:
                    pass
            print(f"OK: {plugins_count} plugin(s) checked, all reachable.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
