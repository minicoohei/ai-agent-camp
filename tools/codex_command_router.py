#!/usr/bin/env python3
"""Resolve slash-style commands to the Codex handler trace."""

from __future__ import annotations

import argparse
import json

from codex_commands import resolve_command


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Slash-style command such as /start-0-1 or /guide")
    parser.add_argument("--trace", action="store_true", help="Print machine-readable route trace")
    args = parser.parse_args()

    resolved = resolve_command(args.command)
    if args.trace:
        print(json.dumps(resolved, ensure_ascii=False, indent=2))
    else:
        if resolved["ok"]:
            print(f"{resolved['handler']} {resolved['target']}")
        else:
            print(resolved["message"])
    return 0 if resolved["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
