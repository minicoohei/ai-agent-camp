#!/usr/bin/env python3
"""Generate command and skill inventory sections from repository sources."""

from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml


COMMANDS_DOC = Path("docs/commands-reference.md")
SKILLS_DOC = Path("docs/skills-reference.md")
LOCALE_SUFFIX_RE = re.compile(r"\.(?:en|es)$")
START_COMMAND_RE = re.compile(r"^start-(\d+)-")
MODULE_TOKEN_RE = re.compile(r"(?:^|[-_/])module-?(\d+)(?:$|[-_/])", re.IGNORECASE)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class ReferenceEntry:
    """One generated reference row."""

    name: str
    description: str
    source: Path
    module: int | None = None


def parse_frontmatter(text: str, source: Path | None = None) -> dict[str, Any]:
    """Parse YAML frontmatter, returning an empty mapping when it is absent."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        label = f" in {source}" if source else ""
        raise ValueError(f"Unterminated frontmatter{label}") from exc

    data = yaml.safe_load("\n".join(lines[1:end])) or {}
    if not isinstance(data, dict):
        label = f" in {source}" if source else ""
        raise ValueError(f"Frontmatter must be a mapping{label}")
    return data


def first_heading(text: str) -> str:
    """Return the first level-one Markdown heading."""

    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def canonical_command_name(path: Path) -> str:
    """Remove file and locale suffixes from a command filename."""

    return LOCALE_SUFFIX_RE.sub("", path.stem)


def natural_key(value: str) -> tuple[object, ...]:
    """Sort strings with embedded numbers in numeric order."""

    return tuple(int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", value))


def unique_markdown_files(directory: Path) -> list[Path]:
    """Return one source file per command, preferring the unsuffixed locale."""

    selected: dict[str, Path] = {}
    for path in directory.glob("*.md"):
        name = canonical_command_name(path)
        current = selected.get(name)
        is_plain = not path.stem.endswith((".en", ".es"))
        if current is None or (is_plain and current.stem.endswith((".en", ".es"))):
            selected[name] = path
    return [selected[name] for name in sorted(selected, key=natural_key)]


def clean_heading(heading: str, command_name: str) -> str:
    """Turn a command heading into a compact table description."""

    value = heading.strip().lstrip("🎓 ")
    value = re.sub(rf"^/?{re.escape(command_name)}\s*(?:--|[-—:])?\s*", "", value, flags=re.I)
    value = re.sub(r"^Lesson\s+\d+(?:-[\w]+)?\s*:\s*", "", value, flags=re.I)
    value = re.sub(r"^\d+(?:-[\w]+)+\s*:\s*", "", value)
    value = re.sub(r"\s+", " ", value).strip(" -—:")
    return value or command_name


def command_description(metadata: dict[str, Any], heading: str, name: str) -> str:
    """Choose a useful description from frontmatter and the first heading."""

    raw = metadata.get("description")
    description = str(raw).strip() if raw is not None else ""
    generic = description.casefold() in {"command", "lesson command", "utility command"}
    if description and not generic and not description.casefold().startswith("lesson command"):
        return re.sub(r"\s+", " ", description)
    return clean_heading(heading, name)


def command_module(name: str, metadata: dict[str, Any]) -> int | None:
    """Infer a module number from the command name or frontmatter."""

    match = START_COMMAND_RE.match(name)
    if match:
        return int(match.group(1))

    values: list[str] = [name]
    chapter = metadata.get("chapter")
    if chapter:
        values.append(str(chapter))
    tags = metadata.get("tags", [])
    if isinstance(tags, str):
        values.append(tags)
    elif isinstance(tags, list):
        values.extend(str(tag) for tag in tags)
    for value in values:
        match = MODULE_TOKEN_RE.search(value)
        if match:
            return int(match.group(1))
    return None


def scan_command_directory(directory: Path, repo_root: Path) -> list[ReferenceEntry]:
    """Scan one command directory."""

    entries: list[ReferenceEntry] = []
    for path in unique_markdown_files(directory):
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text, path)
        name = canonical_command_name(path)
        entries.append(
            ReferenceEntry(
                name=name,
                description=command_description(metadata, first_heading(text), name),
                source=path.relative_to(repo_root),
                module=command_module(name, metadata),
            )
        )
    return entries


def scan_commands(repo_root: Path) -> OrderedDict[str, list[ReferenceEntry]]:
    """Scan lesson, utility, and top-level Cursor commands."""

    commands_root = repo_root / ".cursor/commands"
    groups: OrderedDict[str, list[ReferenceEntry]] = OrderedDict()
    groups["レッスン"] = scan_command_directory(commands_root / "lesson", repo_root)
    groups["ユーティリティ"] = scan_command_directory(commands_root / "utility", repo_root)
    groups["トップレベル"] = scan_command_directory(commands_root, repo_root)
    return groups


def scan_skills(repo_root: Path) -> list[ReferenceEntry]:
    """Scan all immediate skills/ directories containing SKILL.md."""

    entries: list[ReferenceEntry] = []
    for skill_dir in sorted((repo_root / "skills").iterdir(), key=lambda path: natural_key(path.name)):
        skill_file = skill_dir / "SKILL.md"
        if not skill_dir.is_dir() or not skill_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text, skill_file)
        name = str(metadata.get("name") or skill_dir.name).strip()
        description = str(metadata.get("description") or first_heading(text) or name).strip()
        entries.append(
            ReferenceEntry(
                name=name,
                description=re.sub(r"\s+", " ", description),
                source=skill_file.relative_to(repo_root),
            )
        )

    duplicates = sorted({entry.name for entry in entries if sum(item.name == entry.name for item in entries) > 1})
    if duplicates:
        raise ValueError(f"Duplicate skill names: {', '.join(duplicates)}")
    return entries


def markdown_cell(value: object) -> str:
    """Escape content for a one-line Markdown table cell."""

    return re.sub(r"\s+", " ", str(value)).replace("|", "\\|").strip()


def source_link(path: Path) -> str:
    """Build a docs-relative Markdown link."""

    display = path.as_posix()
    return f"[`{display}`](../{display})"


def command_table(entries: list[ReferenceEntry], include_module: bool = False) -> str:
    """Render command rows as a Markdown table."""

    if include_module:
        lines = ["| コマンド | Module | 説明 | 定義 |", "|---|---:|---|---|"]
    else:
        lines = ["| コマンド | 説明 | 定義 |", "|---|---|---|"]
    for entry in entries:
        command = f"`/{markdown_cell(entry.name)}`"
        description = markdown_cell(entry.description)
        source = source_link(entry.source)
        if include_module:
            module = f"Module {entry.module}" if entry.module is not None else "—"
            lines.append(f"| {command} | {module} | {description} | {source} |")
        else:
            lines.append(f"| {command} | {description} | {source} |")
    return "\n".join(lines)


def render_commands_block(groups: OrderedDict[str, list[ReferenceEntry]]) -> str:
    """Render the complete generated commands inventory."""

    lesson = groups["レッスン"]
    lines = [
        "## コマンド一覧",
        "",
        "`.en.md` / `.es.md` は同じ slash command の翻訳版として重複計上しません。",
        "",
        f"### レッスンコマンド（{len(lesson)}個）",
    ]

    by_module: dict[int | None, list[ReferenceEntry]] = {}
    for entry in lesson:
        by_module.setdefault(entry.module, []).append(entry)
    module_keys = sorted((key for key in by_module if key is not None))
    if None in by_module:
        module_keys.append(None)
    for module in module_keys:
        entries = sorted(by_module[module], key=lambda item: natural_key(item.name))
        label = f"Module {module}" if module is not None else "共通・セットアップ"
        lines.extend(["", f"#### {label}（{len(entries)}個）", "", command_table(entries)])

    for group_name in ("ユーティリティ", "トップレベル"):
        entries = groups[group_name]
        lines.extend(
            [
                "",
                f"### {group_name}コマンド（{len(entries)}個）",
                "",
                command_table(entries, include_module=group_name == "トップレベル"),
            ]
        )
    return "\n".join(lines)


def category_name(heading: str) -> str:
    """Remove generated counts from a category heading."""

    return re.sub(r"\s*[（(]\d+個[）)]\s*$", "", heading).strip()


def inherited_skill_categories(document: str) -> OrderedDict[str, list[str]]:
    """Read the existing category order and skill assignments from the document."""

    categories: OrderedDict[str, list[str]] = OrderedDict()
    current: str | None = None
    for line in document.splitlines():
        heading = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if heading:
            candidate = category_name(heading.group(1))
            if candidate == "未分類" or ("スキル" in candidate and candidate not in {"スキル一覧", "スキルの実行方法"}):
                current = candidate
                categories.setdefault(current, [])
                continue

        detailed = re.match(r"^###\s+\d+\.\s+`([^`]+)`", line)
        table = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        name_match = detailed or table
        if current and name_match:
            name = name_match.group(1)
            if name not in categories[current]:
                categories[current].append(name)
    return categories


def categorize_skills(
    entries: list[ReferenceEntry], inherited: OrderedDict[str, list[str]]
) -> OrderedDict[str, list[ReferenceEntry]]:
    """Apply inherited categories and put newly discovered skills in 未分類."""

    by_name = {entry.name: entry for entry in entries}
    assigned: set[str] = set()
    result: OrderedDict[str, list[ReferenceEntry]] = OrderedDict()
    for category, names in inherited.items():
        selected = [by_name[name] for name in names if name in by_name and name not in assigned]
        if selected:
            result[category] = sorted(selected, key=lambda item: natural_key(item.name))
            assigned.update(entry.name for entry in selected)

    uncategorized = sorted(
        (entry for entry in entries if entry.name not in assigned),
        key=lambda item: natural_key(item.name),
    )
    if uncategorized:
        result.setdefault("未分類", []).extend(uncategorized)
    return result


def render_skills_block(categories: OrderedDict[str, list[ReferenceEntry]]) -> str:
    """Render the complete generated skills inventory."""

    lines = [
        "## スキル一覧",
        "",
        "既存カテゴリを引き継ぎ、新しく検出したスキルは「未分類」に追加します。",
    ]
    for category, entries in categories.items():
        lines.extend(
            [
                "",
                f"### {category}（{len(entries)}個）",
                "",
                "| スキル | 説明 | 定義 |",
                "|---|---|---|",
            ]
        )
        for entry in entries:
            lines.append(
                f"| `{markdown_cell(entry.name)}` | {markdown_cell(entry.description)} | {source_link(entry.source)} |"
            )
    return "\n".join(lines)


def replace_generated_block(document: str, kind: str, body: str) -> str:
    """Replace one generated block, bootstrapping markers in legacy documents."""

    start_marker = f"<!-- AUTO-GENERATED:{kind} START -->"
    end_marker = f"<!-- AUTO-GENERATED:{kind} END -->"
    start_count = document.count(start_marker)
    end_count = document.count(end_marker)
    replacement = f"{start_marker}\n{body.rstrip()}\n{end_marker}"

    if start_count == end_count == 1:
        pattern = re.compile(
            rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
        )
        return pattern.sub(lambda _: replacement, document, count=1)
    if start_count or end_count:
        raise ValueError(f"Mismatched or duplicate {kind} generated markers")

    legacy_patterns = {
        "commands": re.compile(
            r"^## レッスンコマンド.*?(?=^## コマンド実行方法)",
            re.MULTILINE | re.DOTALL,
        ),
        "skills": re.compile(
            r"^## 画像生成・編集系スキル.*?(?=^## インストール方法)",
            re.MULTILINE | re.DOTALL,
        ),
    }
    pattern = legacy_patterns[kind]
    if not pattern.search(document):
        raise ValueError(f"Could not find {kind} generated markers or legacy inventory")
    return pattern.sub(lambda _: f"{replacement}\n\n", document, count=1)


def replace_once(document: str, pattern: str, replacement: str, label: str) -> str:
    """Replace exactly one metadata line."""

    updated, count = re.subn(pattern, replacement, document, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Could not update {label}")
    return updated


def update_commands_document(
    document: str,
    groups: OrderedDict[str, list[ReferenceEntry]],
    update_date: str,
) -> str:
    """Update command metadata and generated inventory."""

    counts = {name: len(entries) for name, entries in groups.items()}
    total = sum(counts.values())
    header = (
        f"**対応コマンド数**: {total}個（レッスン {counts['レッスン']}個 + "
        f"ユーティリティ {counts['ユーティリティ']}個 + トップレベル {counts['トップレベル']}個）"
    )
    document = replace_once(document, r"^\*\*対応コマンド数\*\*:.*$", header, "command count")
    document = replace_once(document, r"^最終更新:.*$", f"最終更新: {update_date}", "command date")
    return replace_generated_block(document, "commands", render_commands_block(groups))


def update_skills_document(document: str, entries: list[ReferenceEntry], update_date: str) -> str:
    """Update skill metadata and generated inventory."""

    inherited = inherited_skill_categories(document)
    categories = categorize_skills(entries, inherited)
    document = replace_once(
        document,
        r"^\*\*対応スキル数\*\*:.*$",
        f"**対応スキル数**: {len(entries)}個",
        "skill count",
    )
    document = replace_once(document, r"^最終更新:.*$", f"最終更新: {update_date}", "skill date")
    return replace_generated_block(document, "skills", render_skills_block(categories))


def deterministic_date(repo_root: Path, override: str | None) -> str:
    """Use --date or the last source-tree commit date; never use wall-clock time."""

    if override:
        if not ISO_DATE_RE.fullmatch(override):
            raise ValueError("--date must use YYYY-MM-DD")
        return override
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", ".cursor/commands", "skills"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    if not ISO_DATE_RE.fullmatch(value):
        raise ValueError("Could not determine a source commit date; pass --date YYYY-MM-DD")
    return value


def generate_updates(repo_root: Path, update_date: str) -> dict[Path, str]:
    """Return generated document content keyed by absolute path."""

    commands_path = repo_root / COMMANDS_DOC
    skills_path = repo_root / SKILLS_DOC
    groups = scan_commands(repo_root)
    skills = scan_skills(repo_root)
    return {
        commands_path: update_commands_document(
            commands_path.read_text(encoding="utf-8"), groups, update_date
        ),
        skills_path: update_skills_document(
            skills_path.read_text(encoding="utf-8"), skills, update_date
        ),
    }


def print_diff(path: Path, current: str, generated: str, repo_root: Path) -> None:
    """Print a bounded unified diff for CI diagnostics."""

    relative = path.relative_to(repo_root).as_posix()
    diff = list(
        difflib.unified_diff(
            current.splitlines(),
            generated.splitlines(),
            fromfile=relative,
            tofile=f"{relative} (generated)",
            lineterm="",
        )
    )
    limit = 120
    print("\n".join(diff[:limit]), file=sys.stderr)
    if len(diff) > limit:
        print(f"... {len(diff) - limit} additional diff lines omitted", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when generated docs are stale")
    parser.add_argument("--date", help="deterministic update date in YYYY-MM-DD format")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help=argparse.SUPPRESS,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.root.resolve()
    try:
        update_date = deterministic_date(repo_root, args.date)
        updates = generate_updates(repo_root, update_date)
    except (OSError, subprocess.CalledProcessError, ValueError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    stale = False
    for path, generated in updates.items():
        current = path.read_text(encoding="utf-8")
        if current == generated:
            continue
        stale = True
        if args.check:
            print_diff(path, current, generated, repo_root)
        else:
            path.write_text(generated, encoding="utf-8")

    if args.check and stale:
        print("Reference docs are stale. Run: python3 tools/generate_reference_docs.py", file=sys.stderr)
        return 1
    if args.check:
        print("Reference docs are up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
