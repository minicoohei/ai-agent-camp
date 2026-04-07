#!/usr/bin/env python3
"""Generate the Codex command manifest from .cursor command sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from codex_commands import MANIFEST_PATH, manifest_as_dict, write_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", action="store_true", help="Print instead of writing the manifest")
    parser.add_argument(
        "--output",
        type=Path,
        default=MANIFEST_PATH,
        help="Custom manifest output path",
    )
    args = parser.parse_args()

    if args.stdout:
        print(json.dumps(manifest_as_dict(), ensure_ascii=False, indent=2))
        return 0

    path = write_manifest(args.output)
    print(path.relative_to(Path.cwd()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
