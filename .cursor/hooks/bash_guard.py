#!/usr/bin/env python3
"""Cursor beforeShellExecution hook: Bash コマンドの事前検査。

Claude Code 用の .claude/hooks/bash_guard.py と同じ検知ロジックを使用し、
Cursor の入力形式（stdin JSON: {command, cwd, ...}）に対応するアダプター。

入力: stdin から JSON ({command, cwd, hook_event_name, ...})
出力:
  - exit 0 + stdout JSON: 許可 ({permission: "allow"})
  - exit 2 + stderr: ブロック
  - exit 0 + stdout JSON {permission: "deny"}: ブロック
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

# Claude Code 用の bash_guard.py からロジックを共有
# プロジェクトルートを特定
_THIS_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _THIS_DIR.parent.parent
_CLAUDE_HOOKS = _PROJECT_ROOT / ".claude" / "hooks"

# BLOCK_PATTERNS と RM_PATTERN を直接定義（独立性を保つため）
BLOCK_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r'[^>]>\s*\.env\b'),
        "セキュリティ: .env への上書き (>) は禁止です。追記 (>>) を使用してください。",
    ),
    (
        re.compile(r'\b(?:rm|gomi)\s+.*\.env\b'),
        "セキュリティ: .env の削除は禁止です。",
    ),
    (
        re.compile(r'\b(?:rm|gomi)\s+.*\.(pem|key|p12|pfx)\b'),
        "セキュリティ: 鍵ファイル (.pem/.key/.p12/.pfx) の削除は禁止です。",
    ),
    (
        re.compile(r'\b(?:rm|gomi)\s+.*(?:credentials|client_secret|token).*\.json\b'),
        "セキュリティ: 認証情報ファイルの削除は禁止です。",
    ),
    (
        re.compile(r'\bsudo\b'),
        "セキュリティ: sudo は使用禁止です。",
    ),
    (
        re.compile(r'\bgit\s+push\s+.*(?:--force\b|-f\b)'),
        "セキュリティ: git push --force は禁止です。--force-with-lease を検討してください。",
    ),
    (
        re.compile(r'\bgit\s+clean\s+.*-[a-zA-Z]*x'),
        "セキュリティ: git clean -x は .env 等も削除します。使用禁止です。",
    ),
    (
        re.compile(
            r'\b(?:curl|wget)\b.*\$\{?[A-Z_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)[A-Z_]*\}?',
            re.IGNORECASE,
        ),
        "セキュリティ: API キー等の環境変数を含む curl/wget は禁止です。",
    ),
    (
        re.compile(r':\(\)\s*\{'),
        "セキュリティ: フォークボムパターンを検知しました。",
    ),
]

RM_PATTERN = re.compile(r'(?:^|[;&|]\s*)rm\s')


def main() -> int:
    if os.environ.get("CLAUDE_GUARDRAILS_SKIP") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        # パース失敗時は fail-open（許可）。
        # Cursor Automation 等の非標準環境でコマンドが全拒否される問題を防ぐ。
        return 0

    # Cursor 形式: {command: "...", cwd: "...", hook_event_name: "beforeShellExecution"}
    command = data.get("command", "")
    if not command:
        return 0

    # --- ブロックパターンチェック ---
    for pattern, message in BLOCK_PATTERNS:
        if pattern.search(command):
            output = {
                "permission": "deny",
                "userMessage": message,
                "agentMessage": message,
            }
            json.dump(output, sys.stdout)
            return 0

    # --- rm → gomi 置換の案内 ---
    if RM_PATTERN.search(command):
        if shutil.which("gomi"):
            msg = (
                "セキュリティ: rm コマンドの代わりに gomi を使用してください。"
                " gomi はファイルをゴミ箱に移動し、後から復元できます。"
            )
        else:
            msg = (
                "セキュリティ: rm コマンドは使用禁止です。\n"
                "安全な削除ツール gomi をインストールしてください:\n"
                "  brew install gomi  (macOS)"
            )
        output = {
            "permission": "deny",
            "userMessage": msg,
            "agentMessage": msg,
        }
        json.dump(output, sys.stdout)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
