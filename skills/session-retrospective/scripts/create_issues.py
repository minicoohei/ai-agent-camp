#!/usr/bin/env python3
"""Batch-create GitHub issues from a JSON file.

Usage:
    python skills/session-retrospective/scripts/create_issues.py --input issues.json
    python skills/session-retrospective/scripts/create_issues.py --input issues.json --dry-run
    python skills/session-retrospective/scripts/create_issues.py --input issues.json --repo owner/repo

Input JSON format:
[
  {
    "title": "改善: ...",
    "body": "## 背景\\n...\\n## 問題\\n...\\n## 提案\\n...",
    "labels": ["improvement"]
  }
]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_REPO = "TokenPocket/ai-agent-camp"


def get_gh_token() -> str | None:
    """Get GitHub token from environment or git remote URL."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, cwd=ROOT_DIR,
        )
        if result.returncode == 0:
            match = re.search(r"https://x-access-token:([^@]+)@", result.stdout)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass

    return None


def create_issue(
    title: str,
    body: str,
    repo: str,
    labels: list[str] | None = None,
    dry_run: bool = False,
) -> str | None:
    """Create a single GitHub issue. Returns issue URL or None."""
    if dry_run:
        print(f"[DRY-RUN] Would create: {title}")
        print(f"  repo: {repo}")
        if labels:
            print(f"  labels: {', '.join(labels)}")
        print(f"  body: {body[:100]}...")
        print()
        return None

    # --body-file を使用（heredoc/--body では Markdown 内のコードブロックや
    # 特殊文字でシェルエスケープ問題が発生するため）
    body_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    )
    body_file.write(body)
    body_file.close()

    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", title,
        "--body-file", body_file.name,
    ]
    if labels:
        for label in labels:
            cmd.extend(["--label", label])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR creating '{title}': {result.stderr.strip()}", file=sys.stderr)
        return None

    url = result.stdout.strip()
    print(f"Created: {url}")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch-create GitHub issues from JSON")
    parser.add_argument("--input", "-i", required=True, help="JSON file with issue definitions")
    parser.add_argument("--repo", "-r", default=DEFAULT_REPO, help=f"GitHub repo (default: {DEFAULT_REPO})")
    parser.add_argument("--dry-run", action="store_true", help="Print issues without creating them")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"File not found: {input_path}", file=sys.stderr)
        return 1

    issues = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(issues, list):
        print("JSON must be a list of issue objects", file=sys.stderr)
        return 1

    if not args.dry_run:
        token = get_gh_token()
        if not token:
            print("ERROR: GH_TOKEN not found. Set GH_TOKEN env var or ensure git remote has token.", file=sys.stderr)
            return 1
        os.environ["GH_TOKEN"] = token

    created = 0
    failed = 0

    for issue in issues:
        title = issue.get("title", "")
        body = issue.get("body", "")
        labels = issue.get("labels")

        if not title:
            print("SKIP: issue with empty title", file=sys.stderr)
            failed += 1
            continue

        url = create_issue(title, body, args.repo, labels, args.dry_run)
        if url or args.dry_run:
            created += 1
        else:
            failed += 1

    print(f"\nSummary: {created} created, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
