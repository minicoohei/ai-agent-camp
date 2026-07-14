#!/usr/bin/env python3
"""
Detect drift between ai-agent-camp slash commands and aiagent-course slides.

For each lesson command in ai-agent-camp/.claude/commands/**/*.md, find the
matching aiagent-course module (from the filename: e.g. start-22-1.md →
module-22, module-18-calendar.md → module-18) and compare extracted facts:

- URLs (https?://…)
- Package install commands (npm install, brew install, bun install, pip install …)
- Code commands ($ … in fenced blocks, common CLI verbs)
- File paths referenced (`apps/…`, `tools/…`, `.mcp.json`, etc.)
- Step counts (## Step N or n01–n99)

Output:
- reports/lesson-drift.csv: one row per command file
- reports/lesson-drift.md: top drift offenders + summary

Exit codes:
- 0 always (informational), unless --max-drift is given and any file exceeds it.

Stdlib-only. Run via `make drift-check`.

Usage:
    python3 tools/lesson_drift_check/check.py \
        --commands .claude/commands \
        --course   ../aiagent-course \
        [--csv reports/lesson-drift.csv] \
        [--md  reports/lesson-drift.md] \
        [--max-drift 5]   # exit 2 if any command has > N drift items
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ---- module-id mapping ----------------------------------------------------

_MODULE_ID_PATTERNS = [
    re.compile(r"start-(?P<n>\d+)-\d+(?:\.[a-z]{2})?\.md$"),
    re.compile(r"module-(?P<n>\d+)(?:[-.][^/]+)?\.md$"),
    re.compile(r"setup-(?P<slug>[a-z0-9-]+)\.md$"),  # setup commands → manual map
]

# Manual mapping from setup-* slug → aiagent-course module id
_SETUP_TO_MODULE = {
    "discord": "module-22",
    "line-harness": "module-23",
    "notion": "module-12",
    "freee": "module-20",
    "salesforce": "module-24",
    "m365": "module-19",
    "m365cli": "module-19",
    "google-ads": "module-25",
    "figma": "module-21",
    "bigquery": "module-8",
    "gas": "module-10",
    "github": "module-11",
    "clasp": "module-10",
    "gogcli": "module-4",
    "elevenlabs": "module-15",
    "fal": "module-15",
    "remotion": "module-15",
    "gemini": "module-1",
    "pencil": "module-13",
    "slack": "module-9",
    "vercel": "module-13",
    "typefully": "module-17",
    "x-api": "module-17",
}


def derive_module_id(path: Path) -> str | None:
    name = path.name
    for pat in _MODULE_ID_PATTERNS:
        m = pat.search(name)
        if not m:
            continue
        if "n" in m.groupdict():
            return f"module-{m.group('n')}"
        slug = m.group("slug")
        # strip locale suffix (.en / .es) embedded in slug
        slug = slug.removesuffix(".en").removesuffix(".es")
        return _SETUP_TO_MODULE.get(slug)
    return None


# ---- fingerprint extraction -----------------------------------------------

# Stop URLs at whitespace, ASCII or Japanese punctuation/brackets that
# typically follow a URL in narrative text.
URL_RE = re.compile(
    r"https?://[^\s)'\"`<>\]、。，．・「」『』（）【】〈〉《》〔〕]+"
)

# Install commands must be preceded by a clear "code-context" anchor:
#   - start of line followed by `$` shell prompt
#   - inside a backtick-fenced span
#   - inside a ```...``` code block (handled by stripping non-code text below)
# This avoids matching narrative phrases like "npm install を実行" or i18n
# strings that contain "npm install Install" (a translation key concatenation).
_INSTALL_VERB = (
    r"(?:bun|npm|pnpm|yarn)\s+install\s+(?:-g\s+|--global\s+)?[A-Za-z0-9@/.+-]+|"
    r"brew\s+install\s+[A-Za-z0-9@/.+-]+|"
    r"pip\s+install\s+[A-Za-z0-9@/.<>=+-]+|"
    r"uv\s+pip\s+install\s+[A-Za-z0-9@/.<>=+-]+|"
    r"npx\s+(?:wrangler|create-[\w-]+)(?:\s+[A-Za-z0-9@/.+-]+)?|"
    r"go\s+install\s+[A-Za-z0-9@/.+-]+"
)
INSTALL_RE = re.compile(
    rf"(?:^|[\n\r])\s*\$\s*({_INSTALL_VERB})|"  # `$ npm install foo` shell prompt
    rf"`({_INSTALL_VERB})`",                     # `inline-codespan`
    re.I | re.M,
)
CODE_VERB_RE = re.compile(
    r"(?:^|\s|`)("
    r"git\s+clone\s+\S+|"
    r"wrangler\s+(?:d1\s+create|secret\s+put|deploy|login)\s*\S*|"
    r"claude\s+mcp\s+(?:add|list)|"
    r"security\s+(?:add|find)-generic-password\s+\S*|"
    r"gcloud\s+auth\s+\S+"
    r")",
    re.I,
)
FILE_PATH_RE = re.compile(
    r"(?:^|\s|`|/)(?:apps|tools|src|packages|public|messages|reports|data)/[\w./-]+"
)
STEP_RE = re.compile(r"^\s*##\s+(?:Step|ステップ|Paso|n)\s*\d", re.M | re.I)


@dataclass
class Fingerprint:
    urls: set[str] = field(default_factory=set)
    installs: set[str] = field(default_factory=set)
    cmds: set[str] = field(default_factory=set)
    paths: set[str] = field(default_factory=set)
    step_count: int = 0

    @classmethod
    def from_text(cls, text: str) -> "Fingerprint":
        fp = cls()
        for m in URL_RE.finditer(text):
            url = m.group(0).rstrip(".,;:!?")
            # filter generic / placeholder / docs URLs
            if any(s in url for s in ("example.com", "your-worker", "<", ">")):
                continue
            fp.urls.add(_norm(url))
        for m in INSTALL_RE.finditer(text):
            verb = m.group(1) or m.group(2)
            if verb:
                fp.installs.add(_norm(verb))
        for m in CODE_VERB_RE.finditer(text):
            fp.cmds.add(_norm(m.group(1)))
        for m in FILE_PATH_RE.finditer(text):
            fp.paths.add(_norm(m.group(0).strip("`/ ")))
        fp.step_count = len(STEP_RE.findall(text))
        return fp


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().rstrip("`).,;:!?")


# ---- aiagent-course corpus loader -----------------------------------------


def load_module_corpus(course_root: Path, module_id: str) -> str:
    """Concat all locale JSON + slide tsx for a given module id (e.g., 'module-22')."""
    parts: list[str] = []
    n_part = module_id.split("-", 1)[1]  # 22 / "skills"
    json_name = f"module{n_part}.json" if n_part != "skills" else "moduleSkills.json"
    for locale in ("ja", "en", "es"):
        p = course_root / f"messages/{locale}/course/{json_name}"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            parts.append(_flatten_json(data))
    slide_dir = course_root / f"src/app/[locale]/course/[moduleId]/_components/slides/{module_id}"
    if slide_dir.exists():
        for tsx in slide_dir.rglob("*.tsx"):
            try:
                tsx_text = tsx.read_text(encoding="utf-8")
            except OSError:
                continue
            # Drop ESM import lines + TS type-only refs — those are framework
            # plumbing, not user-facing slide content. We keep the rest of the
            # JSX (which contains hardcoded shell snippets, URLs, etc.).
            cleaned = []
            for line in tsx_text.splitlines():
                stripped = line.lstrip()
                if stripped.startswith(("import ", "export {", "export type", "export interface")):
                    continue
                cleaned.append(line)
            parts.append("\n".join(cleaned))
    return "\n\n".join(parts)


def _flatten_json(obj, acc: list[str] | None = None) -> str:
    """Concat all string values in nested dict/list."""
    if acc is None:
        acc = []
    if isinstance(obj, dict):
        for v in obj.values():
            _flatten_json(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _flatten_json(v, acc)
    elif isinstance(obj, str):
        acc.append(obj)
    return "\n".join(acc)


# ---- comparison -----------------------------------------------------------


@dataclass
class DriftRow:
    command_file: str
    module_id: str
    cmd_only_urls: list[str] = field(default_factory=list)
    slide_only_urls: list[str] = field(default_factory=list)
    cmd_only_installs: list[str] = field(default_factory=list)
    slide_only_installs: list[str] = field(default_factory=list)
    cmd_only_cmds: list[str] = field(default_factory=list)
    slide_only_cmds: list[str] = field(default_factory=list)
    cmd_only_paths: list[str] = field(default_factory=list)
    slide_only_paths: list[str] = field(default_factory=list)
    cmd_steps: int = 0
    slide_steps: int = 0
    drift_score: int = 0
    note: str = ""


def compare(cmd_fp: Fingerprint, slide_fp: Fingerprint) -> tuple[int, dict]:
    """Set-difference each fingerprint dimension. drift_score = total uniques."""
    diffs = {
        "cmd_only_urls": sorted(cmd_fp.urls - slide_fp.urls),
        "slide_only_urls": sorted(slide_fp.urls - cmd_fp.urls),
        "cmd_only_installs": sorted(cmd_fp.installs - slide_fp.installs),
        "slide_only_installs": sorted(slide_fp.installs - cmd_fp.installs),
        "cmd_only_cmds": sorted(cmd_fp.cmds - slide_fp.cmds),
        "slide_only_cmds": sorted(slide_fp.cmds - cmd_fp.cmds),
        "cmd_only_paths": sorted(cmd_fp.paths - slide_fp.paths),
        "slide_only_paths": sorted(slide_fp.paths - cmd_fp.paths),
    }
    score = sum(len(v) for v in diffs.values())
    return score, diffs


# ---- discovery + main -----------------------------------------------------


def iter_command_files(root: Path) -> Iterable[Path]:
    for p in sorted(root.rglob("*.md")):
        # ja master only — locale variants follow the same content shape.
        stem = p.stem
        if stem.endswith(".en") or stem.endswith(".es"):
            continue
        # Skip aliases / library docs
        if "_lib" in p.parts:
            continue
        yield p


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--commands", required=True, help="ai-agent-camp .claude/commands root")
    parser.add_argument("--course", required=True, help="aiagent-course repository root")
    parser.add_argument("--csv", default="reports/lesson-drift.csv")
    parser.add_argument("--md", default="reports/lesson-drift.md")
    parser.add_argument(
        "--max-drift",
        type=int,
        default=None,
        help="Fail (exit 2) if any command's drift_score exceeds this.",
    )
    args = parser.parse_args()

    cmd_root = Path(args.commands).resolve()
    course = Path(args.course).resolve()
    if not cmd_root.exists():
        print(f"ERROR: commands root not found: {cmd_root}", file=sys.stderr)
        return 1
    if not course.exists():
        print(f"ERROR: course root not found: {course}", file=sys.stderr)
        return 1

    rows: list[DriftRow] = []
    skipped = 0
    for path in iter_command_files(cmd_root):
        module_id = derive_module_id(path)
        rel = path.relative_to(cmd_root.parent)
        if not module_id:
            skipped += 1
            rows.append(
                DriftRow(
                    command_file=str(rel),
                    module_id="(unmapped)",
                    note="No module-id derivable from filename",
                )
            )
            continue

        cmd_text = path.read_text(encoding="utf-8", errors="replace")
        slide_text = load_module_corpus(course, module_id)
        if not slide_text.strip():
            rows.append(
                DriftRow(
                    command_file=str(rel),
                    module_id=module_id,
                    note=f"No slide corpus found for {module_id}",
                )
            )
            continue

        cmd_fp = Fingerprint.from_text(cmd_text)
        slide_fp = Fingerprint.from_text(slide_text)
        score, diffs = compare(cmd_fp, slide_fp)

        rows.append(
            DriftRow(
                command_file=str(rel),
                module_id=module_id,
                cmd_only_urls=diffs["cmd_only_urls"],
                slide_only_urls=diffs["slide_only_urls"],
                cmd_only_installs=diffs["cmd_only_installs"],
                slide_only_installs=diffs["slide_only_installs"],
                cmd_only_cmds=diffs["cmd_only_cmds"],
                slide_only_cmds=diffs["slide_only_cmds"],
                cmd_only_paths=diffs["cmd_only_paths"],
                slide_only_paths=diffs["slide_only_paths"],
                cmd_steps=cmd_fp.step_count,
                slide_steps=slide_fp.step_count,
                drift_score=score,
            )
        )

    rows.sort(key=lambda r: (-r.drift_score, r.command_file))

    csv_path = Path(args.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    def _csv_safe(value) -> str:
        """Neutralise CSV-formula-injection (CWE-1236)."""
        if isinstance(value, (int, float)):
            return str(value)
        s = "" if value is None else str(value)
        if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
            return "'" + s
        return s

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "command_file",
                "module_id",
                "drift_score",
                "cmd_steps",
                "slide_steps",
                "cmd_only_urls",
                "slide_only_urls",
                "cmd_only_installs",
                "slide_only_installs",
                "cmd_only_cmds",
                "slide_only_cmds",
                "cmd_only_paths",
                "slide_only_paths",
                "note",
            ]
        )
        for r in rows:
            w.writerow(
                _csv_safe(v)
                for v in [
                    r.command_file,
                    r.module_id,
                    r.drift_score,
                    r.cmd_steps,
                    r.slide_steps,
                    " | ".join(r.cmd_only_urls),
                    " | ".join(r.slide_only_urls),
                    " | ".join(r.cmd_only_installs),
                    " | ".join(r.slide_only_installs),
                    " | ".join(r.cmd_only_cmds),
                    " | ".join(r.slide_only_cmds),
                    " | ".join(r.cmd_only_paths),
                    " | ".join(r.slide_only_paths),
                    r.note,
                ]
            )

    md_path = Path(args.md)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Lesson command ↔ slide drift report\n\n")
        scored = [r for r in rows if not r.note]
        unmapped = [r for r in rows if r.module_id == "(unmapped)"]
        no_slides = [r for r in rows if r.note and "No slide corpus" in r.note]
        f.write(f"Scanned commands: **{len(rows)}**  \n")
        f.write(f"With matching slide module: **{len(scored)}**  \n")
        f.write(f"Unmapped (filename does not encode a module): **{len(unmapped)}**  \n")
        f.write(f"Mapped but slide module missing: **{len(no_slides)}**\n\n")
        if scored:
            f.write("## Top 30 drift offenders\n\n")
            f.write("| score | module | command | top diffs |\n")
            f.write("|---:|---|---|---|\n")
            for r in scored[:30]:
                top = []
                for label, items in [
                    ("cmd-url", r.cmd_only_urls),
                    ("slide-url", r.slide_only_urls),
                    ("cmd-pkg", r.cmd_only_installs),
                    ("slide-pkg", r.slide_only_installs),
                    ("cmd-cli", r.cmd_only_cmds),
                    ("slide-cli", r.slide_only_cmds),
                ]:
                    if items:
                        top.append(f"{label}×{len(items)}")
                f.write(
                    f"| {r.drift_score} | `{r.module_id}` | `{r.command_file}` | "
                    f"{' '.join(top) or '—'} |\n"
                )
        if no_slides:
            f.write("\n## Commands with no matching slide module\n\n")
            for r in no_slides[:30]:
                f.write(f"- `{r.command_file}` → `{r.module_id}` ({r.note})\n")

    print(f"Scanned {len(rows)} commands. Reports: {args.csv}, {args.md}")
    print(f"  scored={len(scored)} unmapped={len(unmapped)} missing_slides={len(no_slides)}")
    if scored:
        print(f"  drift_score distribution: max={max(r.drift_score for r in scored)} "
              f"avg={sum(r.drift_score for r in scored)/len(scored):.1f}")

    if args.max_drift is not None:
        bad = [r for r in scored if r.drift_score > args.max_drift]
        if bad:
            print(f"FAIL: {len(bad)} commands have drift > {args.max_drift}", file=sys.stderr)
            for r in bad[:10]:
                print(f"  {r.drift_score:>3} {r.command_file}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
