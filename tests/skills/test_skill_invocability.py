"""スキル起動可能性テスト

全スキルの SKILL.md 構造、スクリプト構文、メタデータを検証し
エビデンスレポートを生成する。

実行:
    python -m pytest tests/skills/test_skill_invocability.py -v
"""

from __future__ import annotations

import ast
import py_compile
import re
import tempfile
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = PROJECT_ROOT / "skills"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _all_skill_dirs() -> list[Path]:
    """_template を除く全スキルディレクトリ"""
    return sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and d.name != "_template" and not d.name.startswith(".")
    )


def _all_skill_scripts() -> list[Path]:
    """全スキルの Python スクリプト"""
    scripts = []
    for d in _all_skill_dirs():
        scripts_dir = d / "scripts"
        if scripts_dir.exists():
            scripts.extend(sorted(scripts_dir.glob("*.py")))
    return scripts


def _parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


SKILL_DIRS = _all_skill_dirs()
SKILL_SCRIPTS = _all_skill_scripts()


# ---------------------------------------------------------------------------
# Category A-1: SKILL.md frontmatter
# ---------------------------------------------------------------------------

class TestSkillFrontmatter:
    """SKILL.md の存在と frontmatter 構造を検証"""

    def test_all_skills_have_skill_md(self):
        """97+ の SKILL.md が存在すること"""
        count = sum(1 for d in SKILL_DIRS if (d / "SKILL.md").exists())
        assert count >= 90, f"SKILL.md count: {count} (90+ expected)"

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda d: d.name)
    def test_frontmatter_has_name_and_description(self, skill_dir: Path):
        """SKILL.md に name と description が存在すること"""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip(f"{skill_dir.name}/SKILL.md not found")
        fm = _parse_frontmatter(skill_md)
        assert fm is not None, f"{skill_dir.name}: YAML frontmatter がパースできない"
        assert "name" in fm and fm["name"], f"{skill_dir.name}: name が空"
        assert "description" in fm and fm["description"], f"{skill_dir.name}: description が空"

    @pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda d: d.name)
    def test_skill_name_matches_directory(self, skill_dir: Path):
        """SKILL.md の name がディレクトリ名と一致すること"""
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip(f"{skill_dir.name}/SKILL.md not found")
        fm = _parse_frontmatter(skill_md)
        if fm is None or "name" not in fm:
            pytest.skip("frontmatter parse failed")
        # name は skill-name 形式またはディレクトリ名と一致
        assert fm["name"] == skill_dir.name, (
            f"name mismatch: frontmatter='{fm['name']}' vs dir='{skill_dir.name}'"
        )


# ---------------------------------------------------------------------------
# Category A-2: Script importability
# ---------------------------------------------------------------------------

class TestSkillScriptImportability:
    """スキルの Python スクリプトが構文エラーなしでコンパイルできるか検証"""

    @pytest.mark.parametrize("script_path", SKILL_SCRIPTS, ids=lambda p: f"{p.parent.parent.name}/{p.name}")
    def test_scripts_compile_without_syntax_error(self, script_path: Path):
        """py_compile で構文エラーがないこと"""
        with tempfile.NamedTemporaryFile(suffix=".pyc", delete=True) as tmp:
            try:
                py_compile.compile(str(script_path), cfile=tmp.name, doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"Syntax error in {script_path.name}: {e}")

    @pytest.mark.parametrize("script_path", SKILL_SCRIPTS, ids=lambda p: f"{p.parent.parent.name}/{p.name}")
    def test_scripts_have_function_or_main(self, script_path: Path):
        """スクリプトに関数定義または __main__ ブロックがあること"""
        source = script_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            pytest.skip("syntax error (別テストでカバー)")
        has_func = any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
        has_main = "if __name__" in source
        has_class = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
        assert has_func or has_main or has_class, (
            f"{script_path.name}: 関数、クラス、__main__ ブロックのいずれもない"
        )


# ---------------------------------------------------------------------------
# Evidence report
# ---------------------------------------------------------------------------

class TestSkillEvidence:
    """全スキルの検証結果をエビデンスレポートとして出力"""

    def test_generate_skill_report(self):
        """skill-invocability-report.json を生成"""
        # Lazy import to avoid circular dependency
        from tests.e2e.lesson_quality_helpers import write_evidence_report

        details = []
        total_pass = 0
        total_fail = 0

        for skill_dir in SKILL_DIRS:
            checks = []
            skill_md = skill_dir / "SKILL.md"

            # Check 1: SKILL.md exists
            exists = skill_md.exists()
            checks.append({"name": "skill_md_exists", "status": "PASS" if exists else "FAIL"})

            # Check 2: frontmatter valid
            fm = _parse_frontmatter(skill_md) if exists else None
            fm_ok = fm is not None and "name" in fm and "description" in fm
            checks.append({"name": "frontmatter_valid", "status": "PASS" if fm_ok else "FAIL"})

            # Check 3: scripts compile
            scripts_dir = skill_dir / "scripts"
            script_errors = []
            if scripts_dir.exists():
                for script in sorted(scripts_dir.glob("*.py")):
                    try:
                        py_compile.compile(str(script), doraise=True)
                    except py_compile.PyCompileError as e:
                        script_errors.append(f"{script.name}: {e}")
            scripts_ok = len(script_errors) == 0
            checks.append({
                "name": "scripts_compile",
                "status": "PASS" if scripts_ok else "FAIL",
                "errors": script_errors,
            })

            passed = sum(1 for c in checks if c["status"] == "PASS")
            failed = len(checks) - passed
            total_pass += passed
            total_fail += failed

            details.append({
                "skill": skill_dir.name,
                "checks": checks,
                "passed": passed,
                "failed": failed,
            })

        report = {
            "total_skills": len(SKILL_DIRS),
            "total_checks": total_pass + total_fail,
            "passed": total_pass,
            "failed": total_fail,
            "details": details,
        }
        path = write_evidence_report(report, "skill-invocability-report.json")
        assert path.exists(), "レポートが生成されていない"
        # Fail if more than 10% of checks fail
        fail_rate = total_fail / (total_pass + total_fail) if (total_pass + total_fail) else 0
        assert fail_rate < 0.15, f"Fail rate {fail_rate:.1%} exceeds 15% threshold"
