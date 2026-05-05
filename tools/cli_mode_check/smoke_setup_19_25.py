#!/usr/bin/env python3
"""
Smoke-invoke each new /setup-* command (PR #60) under both claude -p and
cursor-agent --print, in plan mode, with bounded budgets.

For each (cli, command) pair we record:
- exit code
- whether the command was recognised (no "Unknown command" preamble)
- whether the nonInteractiveMode declaration's behaviour was honoured
- latency
- first ~30 lines of output (saved to reports/cli-smoke/<cli>-<cmd>.txt)

Output:
- reports/cli-smoke.md — summary table
- reports/cli-smoke/<cli>-<cmd>.txt — per-run transcripts

Stdlib only.

Usage:
    # Default budget per claude run = $0.30
    python3 tools/cli_mode_check/smoke_setup_19_25.py [--budget 0.30]
                                                      [--skip-claude]
                                                      [--skip-cursor]
                                                      [--cmd setup-m365cli]
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

COMMANDS = [
    ("setup-m365cli",    "deferred",     19),
    ("setup-freee",      "incompatible", 20),
    ("setup-figma",      "incompatible", 21),
    ("setup-salesforce", "incompatible", 24),
    ("setup-google-ads", "incompatible", 25),
]

PROMPT_TEMPLATE = (
    "/{slug}\n\n"
    "You are running in non-interactive mode. Respect the file's "
    "`nonInteractiveMode` frontmatter. If it is `deferred` or `incompatible`, "
    "describe what you would do and stop quickly. Do NOT execute setup steps. "
    "Output under 200 words."
)


def run(cmd_argv: list[str], stdin_data: str = "", timeout: int = 180) -> tuple[int, str, float]:
    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            cmd_argv,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return proc.returncode, out, time.monotonic() - t0
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s", time.monotonic() - t0


def detect_signals(text: str, mode: str) -> dict[str, bool]:
    lc = text.lower()
    # Deferred: AI mentions deferring, resume.md, interactive session, or
    # explicitly notes it would skip the interactive parts.
    deferred_kw = (
        "resume", "interactive", "対話", "非対話", "再起動", "後で", "later",
        "modo interactivo", "deferred",
    )
    # Incompatible: AI refuses to run end-to-end, points back to the
    # interactive mode, or names the OAuth / browser blocker.
    incompatible_kw = (
        "cannot", "incompatible", "対話", "完走できません", "完走しません",
        "interactive mode", "no termina", "modo interactivo",
        "browser", "ブラウザ", "oauth",
    )
    return {
        "recognised": "unknown command" not in lc,
        "deferred_signal": any(k in lc or k in text for k in deferred_kw),
        "incompatible_signal": any(k in lc or k in text for k in incompatible_kw),
        "any_setup_step_executed": (
            re.search(r"^\$\s+(npm|bun|brew|pip|gcloud|wrangler)\s+install", text, re.M) is not None
            and "would" not in lc
        ),
    }


def verdict(mode: str, signals: dict[str, bool], rc: int) -> str:
    if not signals["recognised"]:
        return "FAIL (unknown command)"
    if rc != 0 and rc not in (1, 2):  # plan mode + budget exceedance allowed
        return f"FAIL (exit {rc})"
    if signals["any_setup_step_executed"]:
        return "FAIL (executed steps in plan mode)"
    if mode == "deferred" and not signals["deferred_signal"]:
        return "WARN (deferred declared but no resume/interactive hint)"
    if mode == "incompatible" and not signals["incompatible_signal"]:
        return "WARN (incompatible declared but no refusal hint)"
    return "PASS"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--budget", type=float, default=0.30)
    ap.add_argument("--skip-claude", action="store_true")
    ap.add_argument("--skip-cursor", action="store_true")
    ap.add_argument("--cmd", default=None, help="run only this slug")
    ap.add_argument("--out", default="reports/cli-smoke")
    ap.add_argument("--summary", default="reports/cli-smoke.md")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    targets = [c for c in COMMANDS if not args.cmd or c[0] == args.cmd]

    have_claude = shutil.which("claude") is not None
    have_cursor = shutil.which("cursor-agent") is not None

    for slug, mode, mod in targets:
        prompt = PROMPT_TEMPLATE.format(slug=f"lesson:{slug}")
        if have_claude and not args.skip_claude:
            argv = [
                "claude",
                "-p",
                "--permission-mode", "plan",
                "--output-format", "text",
                "--max-budget-usd", str(args.budget),
                "--no-session-persistence",
                prompt,
            ]
            rc, out, dt = run(argv, stdin_data="", timeout=240)
            (out_dir / f"claude-{slug}.txt").write_text(out, encoding="utf-8")
            sig = detect_signals(out, mode)
            rows.append({
                "cli": "claude -p",
                "slug": slug,
                "mode": mode,
                "module": mod,
                "rc": rc,
                "dt": dt,
                "verdict": verdict(mode, sig, rc),
                "head": "\n".join(out.splitlines()[:6]),
            })
            print(f"[claude -p] /{slug} → {rows[-1]['verdict']} ({dt:.1f}s rc={rc})")

        if have_cursor and not args.skip_cursor:
            argv = [
                "cursor-agent",
                "--print",
                "--mode", "plan",
                "--trust",
                prompt,
            ]
            rc, out, dt = run(argv, stdin_data="", timeout=240)
            (out_dir / f"cursor-{slug}.txt").write_text(out, encoding="utf-8")
            sig = detect_signals(out, mode)
            rows.append({
                "cli": "cursor-agent --print",
                "slug": slug,
                "mode": mode,
                "module": mod,
                "rc": rc,
                "dt": dt,
                "verdict": verdict(mode, sig, rc),
                "head": "\n".join(out.splitlines()[:6]),
            })
            print(f"[cursor-agent] /{slug} → {rows[-1]['verdict']} ({dt:.1f}s rc={rc})")

    summary = Path(args.summary)
    summary.parent.mkdir(parents=True, exist_ok=True)
    with summary.open("w", encoding="utf-8") as f:
        f.write("# CLI smoke (PR #60 — /setup-19..25)\n\n")
        f.write("Plan-mode invocation against each new setup command via both CLIs. ")
        f.write("Verdict = PASS / WARN (signal mismatch) / FAIL (executed work or unknown command).\n\n")
        f.write("| CLI | Module | command | mode | verdict | rc | sec |\n")
        f.write("|---|---:|---|---|---|---:|---:|\n")
        for r in rows:
            f.write(
                f"| {r['cli']} | {r['module']} | `/{r['slug']}` | "
                f"`{r['mode']}` | {r['verdict']} | {r['rc']} | {r['dt']:.1f} |\n"
            )
        passes = sum(1 for r in rows if r["verdict"] == "PASS")
        warns = sum(1 for r in rows if r["verdict"].startswith("WARN"))
        fails = sum(1 for r in rows if r["verdict"].startswith("FAIL"))
        f.write(f"\nTotals: {passes} PASS / {warns} WARN / {fails} FAIL out of {len(rows)} runs.\n\n")
        f.write("Per-run transcripts: `reports/cli-smoke/<cli>-<slug>.txt`\n")

    print(f"\nReport: {summary}")
    return 0 if all(r["verdict"] == "PASS" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
