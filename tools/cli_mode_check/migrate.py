#!/usr/bin/env python3
"""
Bulk-apply `nonInteractiveMode` frontmatter to slash command markdown files
based on the same heuristics as `check.py`.

Heuristic:
- Has OAuth / browser-auth references OR mid-flow AI tool restart → incompatible
- Has AskQuestion blocks (and no OAuth/restart) → deferred
- Has neither → compliant

Usage:
    python tools/cli_mode_check/migrate.py [--root .claude/commands]
                                           [--dry-run]
                                           [--force]      # overwrite existing nonInteractiveMode

Output: prints one line per file describing the action taken.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Reuse pattern lists from check.py (kept duplicated to avoid the package import).
ASKQ_PATTERN = re.compile(
    r"AskQuestion(?:\s*の設定)?|```jsonc?\s*\n[^`]*?\"questions\"\s*:", re.S
)
OAUTH_PATTERN = re.compile(
    r"(?:^|[^a-z])(OAuth|oauth)(?:[^a-z]|$)|"
    r"ブラウザ(?:が自動で|で|を)?(?:開|ログイン|認証)|"
    r"browser\s+(?:opens|login|auth)|"
    r"`?gcloud\s+auth\s+login`?|"
    r"`?gh\s+auth\s+login`?|"
    r"`?vercel\s+login`?|"
    r"`?wrangler\s+login`?|"
    r"`?npx\s+wrangler\s+login`?",
    re.I,
)
RESTART_PATTERN = re.compile(
    r"(?:Claude\s*Code|Cursor|Codex)\s*(?:を|—)\s*(?:再起動|終了)|"
    r"AI\s*ツール\s*を\s*(?:一度|もう一度)?\s*(?:終了|再起動|起動)|"
    r"restart\s+(?:Claude\s*Code|Cursor|Codex|the\s+AI\s+tool)",
    re.I,
)


def classify(text: str) -> str:
    has_oauth = bool(OAUTH_PATTERN.search(text))
    has_restart = bool(RESTART_PATTERN.search(text))
    has_askq = bool(ASKQ_PATTERN.search(text))
    if has_oauth or has_restart:
        return "incompatible"
    if has_askq:
        return "deferred"
    return "compliant"


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
NIM_KEY_RE = re.compile(r"^nonInteractiveMode:\s*(\S+)", re.M)


def update_text(text: str, mode: str, force: bool) -> tuple[str, str]:
    """Return (new_text, action) where action is one of skip/inject/update/added-frontmatter."""
    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        fm = fm_match.group(1)
        existing = NIM_KEY_RE.search(fm)
        if existing:
            if not force or existing.group(1).strip().strip('"').strip("'") == mode:
                return text, f"skip (already={existing.group(1)})"
            new_fm = NIM_KEY_RE.sub(f"nonInteractiveMode: {mode}", fm)
            new_text = "---\n" + new_fm + "\n---\n" + text[fm_match.end():]
            return new_text, f"update (was={existing.group(1)} now={mode})"
        # No nonInteractiveMode key yet — inject it before the closing ---
        new_fm = fm.rstrip() + f"\nnonInteractiveMode: {mode}"
        new_text = "---\n" + new_fm + "\n---\n" + text[fm_match.end():]
        return new_text, f"inject ({mode})"
    # No frontmatter at all — add a minimal one.
    new_text = f"---\nnonInteractiveMode: {mode}\n---\n\n" + text
    return new_text, f"added-frontmatter ({mode})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help="Commands root directory. Repeat to scan multiple repos.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--locale", choices=["ja", "en", "es", "all"], default="all")
    args = parser.parse_args()

    if not args.root:
        cwd = Path.cwd()
        if (cwd / ".claude/commands").exists():
            args.root.append(str(cwd / ".claude/commands"))
        else:
            print("ERROR: --root not given and no .claude/commands found here.", file=sys.stderr)
            return 1

    summary = {"skip": 0, "inject": 0, "update": 0, "added-frontmatter": 0}
    for root_str in args.root:
        root = Path(root_str).resolve()
        if not root.exists():
            print(f"WARN: {root} missing, skip", file=sys.stderr)
            continue
        for path in sorted(root.rglob("*.md")):
            stem = path.stem
            if args.locale == "ja" and (stem.endswith(".en") or stem.endswith(".es")):
                continue
            if args.locale == "en" and not stem.endswith(".en"):
                continue
            if args.locale == "es" and not stem.endswith(".es"):
                continue

            text = path.read_text(encoding="utf-8", errors="replace")
            mode = classify(text)
            new_text, action = update_text(text, mode, args.force)
            key = action.split(" ", 1)[0]
            summary[key] = summary.get(key, 0) + 1
            print(f"{action:<48} {path.relative_to(root.parent)}")
            if not args.dry_run and new_text != text:
                path.write_text(new_text, encoding="utf-8")

    print("\nSummary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
