#!/usr/bin/env python3
"""
Static analyzer for slash command markdown files (.claude/commands/**/*.md).

Detects blockers that prevent a command from running cleanly under
`claude -p` / `cursor-agent --print` (non-interactive / headless modes):

- AskQuestion blocks (interactive prompts)
- OAuth / browser auth flows
- Mid-flow AI tool restart instructions
- Secret-paste prompts that expect typed input
- Namespace issues (sub-directory commands invoked without `lesson:` prefix in docs)
- OS-specific install prompts that may stall on sudo / EULA

Usage:
    python tools/cli_mode_check/check.py [--root .claude/commands]
                                        [--csv reports/cli-mode.csv]
                                        [--md reports/cli-mode.md]
                                        [--locale ja]      # only scan *.md (skip *.en.md / *.es.md)
                                        [--strict]         # exit non-zero if any file scores < threshold

Report columns:
    file | total | askq | oauth | restart | secret | install | namespace | score | grade

Score = 100 - (askq*8 + oauth*6 + restart*15 + secret*4 + install*2 + namespace*5)
clamped to [0, 100]. Grade A>=90, B>=70, C>=50, D<50.

Designed to run with no third-party dependencies (stdlib only).
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable

# ---- detection patterns ---------------------------------------------------

# Each pattern is (regex, weight, label). Counts are accumulated then weighted.
ASKQ_PATTERNS = [
    re.compile(r"AskQuestion(?:\s*の設定)?", re.I),
    re.compile(r"```jsonc?\s*\n[^`]*?\"questions\"\s*:", re.S),
]

OAUTH_PATTERNS = [
    re.compile(r"(?:^|[^a-z])(OAuth|oauth)(?:[^a-z]|$)"),
    re.compile(r"ブラウザ(?:が自動で|で|を)?(?:開|ログイン|認証)"),
    re.compile(r"browser\s+(?:opens|login|auth)", re.I),
    re.compile(r"`?gcloud\s+auth\s+(?:login|application-default\s+login)`?"),
    re.compile(r"`?gh\s+auth\s+login`?"),
    re.compile(r"`?vercel\s+login`?"),
    re.compile(r"https://(?:accounts|login|auth)\.[a-z0-9.-]+/"),
]

RESTART_PATTERNS = [
    re.compile(r"(?:Claude\s*Code|Cursor|Codex)\s*(?:を|—)\s*(?:再起動|終了)"),
    re.compile(r"AI\s*ツール\s*を\s*(?:一度|もう一度)?\s*(?:終了|再起動|起動)"),
    re.compile(r"restart\s+(?:Claude\s*Code|Cursor|Codex|the\s+AI\s+tool)", re.I),
    re.compile(r"`?Ctrl\s*\+\s*C`?\s*(?:→|->|>)\s*`?(?:claude|cursor|codex)`?"),
]

SECRET_INPUT_PATTERNS = [
    re.compile(r"API\s*[キkK][ーeE][ーyY]?\s*(?:を|を貼|を入力|を設定)"),
    re.compile(r"[Tt]oken\s*(?:を|を貼|を入力|を設定)"),
    re.compile(r"`?wrangler\s+secret\s+put`?"),
    re.compile(r"`?npx\s+wrangler\s+secret\s+put`?"),
    re.compile(r"<paste[-_\s]?(?:token|key|secret)[^>]*>", re.I),
    re.compile(r"copy\s+(?:the\s+)?(?:token|key|secret)", re.I),
]

INSTALL_PATTERNS = [
    re.compile(r"`?brew\s+install\s+"),
    re.compile(r"`?npm\s+install\s+(?:-g|--global)\s+"),
    re.compile(r"`?pnpm\s+install\s+(?:-g|--global)\s+"),
    re.compile(r"`?bun\s+install\s+(?:-g|--global)\s+"),
    re.compile(r"`?pip\s+install\s+"),
    re.compile(r"`?uv\s+pip\s+install\s+"),
    re.compile(r"`?sudo\s+"),
    re.compile(r"`?apt(?:-get)?\s+install\s+"),
]

# A doc that says "Use /check-setup" while the file lives in a subdirectory
# would route to /lesson:check-setup under non-interactive invocation.
NAMESPACE_REFERENCE = re.compile(r"`?/[a-z][a-z0-9-]+`?\s*(?:を|スラッシュ|slash|command)", re.I)


# ---- core checker ---------------------------------------------------------


@dataclass
class FileReport:
    path: str
    relpath: str
    total: int = 0
    askq: int = 0
    oauth: int = 0
    restart: int = 0
    secret: int = 0
    install: int = 0
    namespace: int = 0
    score: int = 100
    grade: str = "A"
    nonInteractiveMode: str = ""
    blockers: list[str] = field(default_factory=list)


def _count_matches(patterns: list[re.Pattern], text: str) -> int:
    return sum(len(p.findall(text)) for p in patterns)


def analyze_file(path: Path, root: Path) -> FileReport:
    text = path.read_text(encoding="utf-8", errors="replace")
    rep = FileReport(path=str(path), relpath=str(path.relative_to(root.parent)))

    # Frontmatter inspection: a `nonInteractiveMode:` key declares opt-in compliance.
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if fm_match:
        fm = fm_match.group(1)
        m = re.search(r"^nonInteractiveMode:\s*(\S+)", fm, re.M)
        if m:
            rep.nonInteractiveMode = m.group(1).strip().strip('"').strip("'")

    rep.askq = _count_matches(ASKQ_PATTERNS, text)
    rep.oauth = _count_matches(OAUTH_PATTERNS, text)
    rep.restart = _count_matches(RESTART_PATTERNS, text)
    rep.secret = _count_matches(SECRET_INPUT_PATTERNS, text)
    rep.install = _count_matches(INSTALL_PATTERNS, text)

    # Namespace heuristic: file lives in a sub-dir AND references its own bare
    # slash name without the `lesson:` prefix
    parts = path.relative_to(root).parts
    if len(parts) > 1:
        own = path.stem.split(".")[0]  # strip locale suffix
        bare = re.compile(rf"`?/{re.escape(own)}`?(?!:)", re.I)
        if bare.search(text):
            rep.namespace = len(bare.findall(text))

    rep.total = rep.askq + rep.oauth + rep.restart + rep.secret + rep.install + rep.namespace

    # Scoring
    raw = (
        rep.askq * 8
        + rep.oauth * 6
        + rep.restart * 15
        + rep.secret * 4
        + rep.install * 2
        + rep.namespace * 5
    )
    rep.score = max(0, 100 - raw)

    # A valid `nonInteractiveMode` declaration means the AI knows how to behave
    # under -p, even when the underlying flow is genuinely interactive. The
    # floor reflects "declaration present, behavior defined":
    #   compliant  -> 90 (works headless out of the box)
    #   deferred   -> 80 (headless emits resume.md, then exits)
    #   incompatible -> 70 (headless prints clear refuse-message, exits)
    if rep.nonInteractiveMode == "compliant":
        rep.score = max(rep.score, 90)
    elif rep.nonInteractiveMode == "deferred":
        rep.score = max(rep.score, 80)
    elif rep.nonInteractiveMode == "incompatible":
        rep.score = max(rep.score, 70)

    if rep.score >= 90:
        rep.grade = "A"
    elif rep.score >= 70:
        rep.grade = "B"
    elif rep.score >= 50:
        rep.grade = "C"
    else:
        rep.grade = "D"

    if rep.askq:
        rep.blockers.append(f"AskQuestion×{rep.askq}")
    if rep.oauth:
        rep.blockers.append(f"OAuth×{rep.oauth}")
    if rep.restart:
        rep.blockers.append(f"Restart×{rep.restart}")
    if rep.secret:
        rep.blockers.append(f"Secret×{rep.secret}")
    if rep.install:
        rep.blockers.append(f"Install×{rep.install}")
    if rep.namespace:
        rep.blockers.append(f"Namespace×{rep.namespace}")
    if rep.nonInteractiveMode:
        rep.blockers.append(f"declared:{rep.nonInteractiveMode}")

    return rep


# ---- discovery ------------------------------------------------------------


def iter_command_files(root: Path, locale_filter: str | None) -> Iterable[Path]:
    for p in sorted(root.rglob("*.md")):
        # Skip locale variants if a filter was given. ".md" is the ja master.
        stem = p.stem
        if locale_filter == "ja" and (stem.endswith(".en") or stem.endswith(".es")):
            continue
        if locale_filter == "en" and not stem.endswith(".en"):
            continue
        if locale_filter == "es" and not stem.endswith(".es"):
            continue
        yield p


# ---- output ---------------------------------------------------------------


def _csv_safe(value) -> str:
    """Neutralise CSV-formula-injection (CWE-1236).

    Spreadsheet apps (Excel / Numbers / Google Sheets) execute cell content
    starting with `=`, `+`, `-`, `@`, TAB, or CR as a formula. We prefix any
    such cell with a single quote so the value is rendered as text. Numeric
    values are passed through unchanged.
    """
    if isinstance(value, (int, float)):
        return str(value)
    s = "" if value is None else str(value)
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s


def write_csv(rows: list[FileReport], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "file",
                "total",
                "askq",
                "oauth",
                "restart",
                "secret",
                "install",
                "namespace",
                "score",
                "grade",
                "nonInteractiveMode",
                "blockers",
            ]
        )
        for r in rows:
            w.writerow(
                _csv_safe(v)
                for v in [
                    r.relpath,
                    r.total,
                    r.askq,
                    r.oauth,
                    r.restart,
                    r.secret,
                    r.install,
                    r.namespace,
                    r.score,
                    r.grade,
                    r.nonInteractiveMode,
                    "; ".join(r.blockers),
                ]
            )


def write_md(rows: list[FileReport], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    grades = Counter(r.grade for r in rows)
    declared = sum(1 for r in rows if r.nonInteractiveMode)
    with dest.open("w", encoding="utf-8") as f:
        f.write("# CLI mode compatibility report\n\n")
        f.write(f"Total files scanned: **{len(rows)}**  \n")
        f.write(
            f"Grades — A: {grades['A']}, B: {grades['B']}, "
            f"C: {grades['C']}, D: {grades['D']}  \n"
        )
        f.write(f"Files with `nonInteractiveMode` frontmatter: **{declared}**\n\n")
        f.write("## Lowest-scoring files (top 30)\n\n")
        f.write("| score | grade | file | top blockers |\n")
        f.write("|---:|:--:|---|---|\n")
        for r in sorted(rows, key=lambda r: (r.score, r.relpath))[:30]:
            f.write(
                f"| {r.score} | {r.grade} | `{r.relpath}` | "
                f"{'; '.join(r.blockers) or '—'} |\n"
            )
        f.write("\n## Score distribution\n\n")
        for grade in ["A", "B", "C", "D"]:
            f.write(f"- **{grade}**: {grades[grade]}\n")


# ---- main -----------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="Commands root directory. Repeat to scan multiple repos.",
    )
    parser.add_argument("--csv", default="reports/cli-mode.csv")
    parser.add_argument("--md", default="reports/cli-mode.md")
    parser.add_argument(
        "--locale",
        choices=["ja", "en", "es", "all"],
        default="ja",
        help="Locale filter (default ja: scan only *.md masters).",
    )
    parser.add_argument(
        "--strict",
        type=int,
        default=None,
        help="Fail (exit 2) if any file scores below this threshold.",
    )
    args = parser.parse_args()

    if not args.root:
        # Default: scan both ai-agent-camp and aiagent-course command roots
        # if running from one of them.
        cwd = Path.cwd()
        for cand in [cwd / ".claude/commands"]:
            if cand.exists():
                args.root.append(str(cand))
        if not args.root:
            print("ERROR: --root not given and no .claude/commands found here.", file=sys.stderr)
            return 1

    rows: list[FileReport] = []
    for root_str in args.root:
        root = Path(root_str).resolve()
        if not root.exists():
            print(f"WARNING: {root} does not exist, skipping", file=sys.stderr)
            continue
        locale = None if args.locale == "all" else args.locale
        for path in iter_command_files(root, locale):
            rows.append(analyze_file(path, root))

    rows.sort(key=lambda r: (r.score, r.relpath))

    write_csv(rows, Path(args.csv))
    write_md(rows, Path(args.md))

    print(f"Scanned {len(rows)} files. Reports: {args.csv}, {args.md}")
    grades = Counter(r.grade for r in rows)
    print(f"Grades: A={grades['A']} B={grades['B']} C={grades['C']} D={grades['D']}")

    if args.strict is not None:
        bad = [r for r in rows if r.score < args.strict]
        if bad:
            print(
                f"FAIL: {len(bad)} files scored below {args.strict}",
                file=sys.stderr,
            )
            for r in bad[:10]:
                print(f"  {r.score:>3} {r.grade} {r.relpath}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
