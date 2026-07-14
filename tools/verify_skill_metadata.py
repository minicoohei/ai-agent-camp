#!/usr/bin/env python3
"""
Skill Metadata Verification System

Validates all skills for structural integrity across Codex / Cursor / Claude Code.
Checks: SKILL.md, frontmatter, agents/openai.yaml, .claude/skills/ sync, readability.
"""

import json
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
CLAUDE_SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"
CLAUDE_COMMANDS_DIR = PROJECT_ROOT / ".claude" / "commands" / "lesson"
CURSOR_COMMANDS_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"
OUTPUT_DIR = PROJECT_ROOT / "data" / "skill-verification"

MISSING_EXECUTABLE_ISSUE = "missing-executable-script"

# P2 (PR #77) で全スキルの参照を修理済み。新たな除外が必要になった場合のみ追加する。
MISSING_EXECUTABLE_ALLOWLIST: set[str] = set()

EXECUTABLE_COMMAND_RE = re.compile(
    r"(?:^|[`|]\s*)(?:\$\s*)?(?:uv\s+run\s+)?(?:python3?|bash|sh)\s+"
    r"[\"']?(?P<path>[A-Za-z0-9_./{}$<>-]+\.(?:py|sh))",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {"_parse_error": True}


def extract_executable_script_paths(content: str) -> list[str]:
    """Extract relative script paths used in shell/Python execution commands."""
    return sorted(
        {
            match.group("path")
            for match in EXECUTABLE_COMMAND_RE.finditer(content)
            if not any(marker in match.group("path") for marker in ("$", "{", "<"))
        }
    )


def executable_script_candidates(
    reference: str,
    skill_dir: Path,
    project_root: Path = PROJECT_ROOT,
) -> list[Path]:
    """Return the supported repo-root and skill-relative resolutions for a reference."""
    relative = Path(reference.removeprefix("./"))
    if relative.is_absolute():
        return []

    if relative.parts and relative.parts[0] == "scripts":
        candidates = [skill_dir / relative, project_root / relative]
    else:
        candidates = [project_root / relative, skill_dir / relative]
    if len(relative.parts) == 1:
        candidates.append(skill_dir / "scripts" / relative)
        candidates.extend((project_root / "skills").glob(f"*/scripts/{relative}"))
    return candidates


def check_executable_script_references(
    skill_dir: Path,
    content: str,
    project_root: Path = PROJECT_ROOT,
) -> list[dict]:
    """Check executable script references in one SKILL.md."""
    results = []
    for reference in extract_executable_script_paths(content):
        candidates = executable_script_candidates(reference, skill_dir, project_root)
        existing = next((path for path in candidates if path.is_file()), None)
        results.append(
            {
                "reference": reference,
                "status": "OK" if existing else "BROKEN",
                "resolved_path": (
                    str(existing.relative_to(project_root)) if existing else ""
                ),
            }
        )
    return results


def fatal_script_issues(
    skills: list[dict],
    allowlist: set[str] | None = None,
) -> list[dict]:
    """Return missing executable references not temporarily allowlisted for P2."""
    if allowlist is None:
        allowlist = MISSING_EXECUTABLE_ALLOWLIST
    return [
        {
            "skill": skill["name"],
            "references": skill.get("missing_executable_scripts", []),
        }
        for skill in skills
        if skill.get("missing_executable_scripts") and skill["name"] not in allowlist
    ]


def exit_code_for_skills(skills: list[dict]) -> int:
    """Return the CI exit code for the currently fatal issue categories."""
    return 1 if fatal_script_issues(skills) else 0


def check_skill(skill_dir: Path) -> dict:
    """Check a single skill directory."""
    name = skill_dir.name
    result = {
        "name": name,
        "skill_md_exists": False,
        "frontmatter_name": False,
        "frontmatter_description": False,
        "frontmatter_description_text": "",
        "trigger_words_present": False,
        "openai_yaml_exists": False,
        "openai_yaml_description": "",
        "claude_skills_copy": False,
        "claude_skills_diff": False,
        "skill_md_lines": 0,
        "section_count": 0,
        "language": "unknown",
        "has_prerequisites": False,
        "has_scripts": False,
        "executable_script_references": [],
        "missing_executable_scripts": [],
        "issues": [],
    }

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        result["issues"].append("no-skill-md")
        return result

    result["skill_md_exists"] = True
    content = skill_md.read_text(encoding="utf-8")
    lines = content.split("\n")
    result["skill_md_lines"] = len(lines)

    # Frontmatter
    fm = parse_frontmatter(content)
    if fm.get("_parse_error"):
        result["issues"].append("frontmatter-parse-error")
    if fm.get("name"):
        result["frontmatter_name"] = True
    else:
        result["issues"].append("no-frontmatter-name")
    if fm.get("description"):
        result["frontmatter_description"] = True
        desc = str(fm["description"]).strip()
        result["frontmatter_description_text"] = desc[:200]
        result["_full_description_len"] = len(desc)
    else:
        result["issues"].append("no-frontmatter-description")

    # Trigger words
    trigger_patterns = [
        r"トリガー", r"trigger", r"Use when", r"使う場面",
        r"キーワード", r"発動", r"呼び出し",
    ]
    for pat in trigger_patterns:
        if re.search(pat, content, re.IGNORECASE):
            result["trigger_words_present"] = True
            break
    if not result["trigger_words_present"]:
        result["issues"].append("no-trigger-words")

    # Section count
    result["section_count"] = len(re.findall(r"^##\s+", content, re.MULTILINE))
    if result["section_count"] < 3:
        result["issues"].append("few-sections")

    # Language detection
    jp_chars = len(re.findall(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]", content))
    en_chars = len(re.findall(r"[a-zA-Z]", content))
    if jp_chars > en_chars:
        result["language"] = "ja"
    elif en_chars > jp_chars:
        result["language"] = "en"
    else:
        result["language"] = "mixed"

    # Prerequisites
    if re.search(r"prerequisit|前提|事前", content, re.IGNORECASE):
        result["has_prerequisites"] = True

    # Scripts
    scripts_dir = skill_dir / "scripts"
    result["has_scripts"] = scripts_dir.exists() and any(scripts_dir.iterdir())
    result["executable_script_references"] = check_executable_script_references(
        skill_dir, content
    )
    result["missing_executable_scripts"] = [
        item["reference"]
        for item in result["executable_script_references"]
        if item["status"] == "BROKEN"
    ]
    if result["missing_executable_scripts"]:
        result["issues"].append(MISSING_EXECUTABLE_ISSUE)

    # agents/openai.yaml
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        result["openai_yaml_exists"] = True
        try:
            yaml_data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
            if not isinstance(yaml_data, dict):
                result["issues"].append("openai-yaml-not-dict")
            else:
                iface = yaml_data.get("interface", {})
                result["openai_yaml_description"] = iface.get("short_description", "")[:200]
        except yaml.YAMLError:
            result["issues"].append("openai-yaml-parse-error")
    else:
        result["issues"].append("no-openai-yaml")

    # .claude/skills/ copy
    claude_copy = CLAUDE_SKILLS_DIR / name / "SKILL.md"
    if claude_copy.exists():
        result["claude_skills_copy"] = True
        claude_content = claude_copy.read_text(encoding="utf-8")
        if claude_content != content:
            result["claude_skills_diff"] = True
            result["issues"].append("claude-skills-content-diff")
    else:
        result["issues"].append("no-claude-skills-copy")

    # Readability: description length
    if result["frontmatter_description"]:
        desc_len = result.get("_full_description_len", len(result["frontmatter_description_text"]))
        if desc_len > 500:
            result["issues"].append("description-too-long")

    # Skill.md too large
    if result["skill_md_lines"] > 500:
        result["issues"].append("skill-md-too-large")

    return result


def check_path_references(commands_dir: Path, label: str) -> list:
    """Check skill path references in lesson commands."""
    results = []
    if not commands_dir.exists():
        return results

    for cmd_file in sorted(commands_dir.glob("*.md")):
        content = cmd_file.read_text(encoding="utf-8")
        # Find skill path references
        refs = re.findall(
            r"(?:skills/|\.claude/skills/)([a-z0-9_.-]+)", content
        )
        for ref in refs:
            skill_path = PROJECT_ROOT / "skills" / ref
            claude_path = PROJECT_ROOT / ".claude" / "skills" / ref
            exists_skills = skill_path.exists()
            exists_claude = claude_path.exists()
            if not exists_skills and not exists_claude:
                results.append({
                    "file": str(cmd_file.relative_to(PROJECT_ROOT)),
                    "reference": ref,
                    "status": "BROKEN",
                    "label": label,
                })
            else:
                results.append({
                    "file": str(cmd_file.relative_to(PROJECT_ROOT)),
                    "reference": ref,
                    "status": "OK",
                    "label": label,
                })
    return results


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Check all skills
    print("=== Phase 1-1: Skill Metadata Audit ===")
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir() and d.name != "_template":
            result = check_skill(d)
            skills.append(result)
            status = "OK" if not result["issues"] else f"ISSUES: {', '.join(result['issues'])}"
            print(f"  {result['name']:40s} {status}")

    fatal = fatal_script_issues(skills)
    for skill in skills:
        skill["severity"] = (
            "fatal"
            if skill["missing_executable_scripts"]
            and skill["name"] not in MISSING_EXECUTABLE_ALLOWLIST
            else "informational"
        )

    # Summary
    total = len(skills)
    no_issues = sum(1 for s in skills if not s["issues"])
    print(f"\n  Total: {total}, Clean: {no_issues}, With issues: {total - no_issues}")

    # Save
    audit_path = OUTPUT_DIR / "metadata-audit.json"
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(skills, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {audit_path}")

    # 2. Path integrity
    print("\n=== Phase 1-2: Path Integrity ===")
    path_refs = []
    path_refs.extend(check_path_references(CLAUDE_COMMANDS_DIR, "claude-commands"))
    path_refs.extend(check_path_references(CURSOR_COMMANDS_DIR, "cursor-commands"))

    broken = [r for r in path_refs if r["status"] == "BROKEN"]
    print(f"  Total references: {len(path_refs)}, Broken: {len(broken)}")
    for b in broken:
        print(f"    BROKEN: {b['file']} -> {b['reference']} ({b['label']})")

    path_path = OUTPUT_DIR / "path-integrity.json"
    with open(path_path, "w", encoding="utf-8") as f:
        json.dump(path_refs, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {path_path}")

    # 3. Discovery diff summary
    print("\n=== Phase 1-3: CLI Discovery Diff ===")
    diff_results = {
        "skills_only": [],
        "claude_only": [],
        "content_diff": [],
        "openai_yaml_mismatch": [],
    }

    skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and d.name != "_template"}
    claude_names = {d.name for d in CLAUDE_SKILLS_DIR.iterdir() if d.is_dir()} if CLAUDE_SKILLS_DIR.exists() else set()

    diff_results["skills_only"] = sorted(skill_names - claude_names)
    diff_results["claude_only"] = sorted(claude_names - skill_names)

    for s in skills:
        if s["claude_skills_diff"]:
            diff_results["content_diff"].append(s["name"])
        # Check openai.yaml vs SKILL.md description mismatch
        if s["openai_yaml_description"] and s["frontmatter_description_text"]:
            # Simple check: first 50 chars should overlap
            yaml_start = s["openai_yaml_description"][:50].lower()
            fm_start = s["frontmatter_description_text"][:50].lower()
            if yaml_start != fm_start and yaml_start not in fm_start and fm_start not in yaml_start:
                diff_results["openai_yaml_mismatch"].append({
                    "name": s["name"],
                    "yaml": s["openai_yaml_description"][:100],
                    "frontmatter": s["frontmatter_description_text"][:100],
                })

    print(f"  skills/ only: {diff_results['skills_only']}")
    print(f"  .claude/skills/ only: {diff_results['claude_only']}")
    print(f"  Content diffs: {len(diff_results['content_diff'])}")
    print(f"  openai.yaml mismatches: {len(diff_results['openai_yaml_mismatch'])}")

    diff_path = OUTPUT_DIR / "discovery-diff.json"
    with open(diff_path, "w", encoding="utf-8") as f:
        json.dump(diff_results, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {diff_path}")

    # Issue summary
    print("\n=== Issue Summary ===")
    issue_counts = {}
    for s in skills:
        for issue in s["issues"]:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
    for issue, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        print(f"  {issue:35s} {count}")

    allowlisted = [
        skill
        for skill in skills
        if skill["missing_executable_scripts"]
        and skill["name"] in MISSING_EXECUTABLE_ALLOWLIST
    ]
    print("\n=== Executable Script Reference Gate ===")
    print(f"  Fatal: {len(fatal)}, Allowlisted for P2: {len(allowlisted)}")
    for item in fatal:
        print(f"  FATAL: {item['skill']} -> {', '.join(item['references'])}")
    for skill in allowlisted:
        print(
            f"  ALLOWLISTED: {skill['name']} -> "
            f"{', '.join(skill['missing_executable_scripts'])}"
        )

    stale_allowlist = sorted(
        MISSING_EXECUTABLE_ALLOWLIST
        - {skill["name"] for skill in allowlisted}
    )
    if stale_allowlist:
        print(f"  INFO: stale P2 allowlist entries: {', '.join(stale_allowlist)}")

    print(f"\nAll results saved to: {OUTPUT_DIR}")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
