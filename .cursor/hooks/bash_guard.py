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
            r'\b(?:curl|wget)\b.*\$\{?[A-Z_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)[A-Z_]*\}?',
            re.IGNORECASE,
        ),
        "セキュリティ: API キー等の環境変数を含む curl/wget は禁止です。",
    ),
    # H3: 認証ヘッダー（標準 + 一般的な独自ヘッダー）
    (
        re.compile(
            r'\b(?:curl|wget)\b.*(?:-H[\s=]+|--header[\s=]+)["\']?'
            r'(?:Authorization|X-Api-Key|X-Auth-Token|Api-Key|Auth-Token|'
            r'X-[A-Za-z0-9_-]*-(?:Key|Token|Secret|Auth))\s*:\s*',
            re.IGNORECASE,
        ),
        "セキュリティ: 認証ヘッダーを含む curl/wget は禁止です。",
    ),
    # H3: 機密ファイル添付アップロード
    (
        re.compile(
            r'\b(?:curl|wget)\b.*(?:-F|--form)[\s=]+["\']?[A-Za-z0-9_-]+=@'
            r'(?:~|\$HOME|\$\{HOME\})?/?(?:\.ssh|\.aws|\.gnupg|\.config/gh|\.npmrc|\.pypirc)',
            re.IGNORECASE,
        ),
        "セキュリティ: 機密ファイル (.ssh / .aws / .gnupg 等) を curl で送信する操作は禁止です。",
    ),
    # H3: nc / /dev/tcp/ 経由の exfil
    (
        re.compile(r'\|\s*nc\s+(?:-[A-Za-z]+\s+)*[\w.-]+\s+\d+'),
        "セキュリティ: netcat (`| nc host port`) によるデータ送信は禁止です。",
    ),
    (
        re.compile(r'>\s*/dev/(?:tcp|udp)/'),
        "セキュリティ: /dev/tcp/ 経由のネットワーク送信は禁止です。",
    ),
    (
        re.compile(r':\(\)\s*\{'),
        "セキュリティ: フォークボムパターンを検知しました。",
    ),
]

RM_PATTERN = re.compile(r'(?:^|[;&|]\s*)rm\s')

NETWORK_TX_WITH_ENV: re.Pattern[str] = re.compile(
    r'\b(?:curl|wget|http|httpie)\b.*\$\{?[A-Z_][A-Z0-9_]*\}?',
    re.IGNORECASE,
)

# L4: Unicode 悪用検知（.claude/hooks/bash_guard.py と同じ集合）
BIDI_OVERRIDES: frozenset[str] = frozenset([
    "\u202a", "\u202b", "\u202c", "\u202d", "\u202e",
    "\u2066", "\u2067", "\u2068", "\u2069",
])
INVISIBLE_CHARS: frozenset[str] = frozenset([
    "\u200b", "\u200c", "\u200d", "\u2060", "\ufeff",
])
_SUSPICIOUS_HOMOGLYPHS: frozenset[str] = frozenset([
    "\u0430", "\u0435", "\u043e", "\u0440", "\u0441", "\u0443", "\u0445",
    "\u0455", "\u0456", "\u0458", "\u0501", "\u051b", "\u051d",
    "\u03bf", "\u03c1", "\u03c5", "\u03c7",
    *(chr(cp) for cp in range(0xFF21, 0xFF5B)),
])


def _check_unicode_threats(command: str) -> tuple[bool, str | None]:
    bidi_hit = [c for c in command if c in BIDI_OVERRIDES]
    if bidi_hit:
        points = ", ".join(f"U+{ord(c):04X}" for c in bidi_hit)
        return True, (
            f"セキュリティ: 双方向テキスト制御文字 ({points}) を検知しました。"
            " 表示と実行が食い違う Trojan Source 系攻撃に使われる文字のため、"
            " シェルコマンドでの使用は禁止です。"
        )
    invisible_hit = [c for c in command if c in INVISIBLE_CHARS]
    if invisible_hit:
        points = ", ".join(f"U+{ord(c):04X}" for c in invisible_hit)
        return True, (
            f"セキュリティ: ゼロ幅・不可視文字 ({points}) を検知しました。"
            " コマンド名の偽装や監査ログ回避に使われる字のため、"
            " シェルコマンドでの使用は禁止です。"
        )
    for token in command.split():
        has_latin = any("a" <= c.lower() <= "z" for c in token)
        homoglyph_hit = [c for c in token if c in _SUSPICIOUS_HOMOGLYPHS]
        if has_latin and homoglyph_hit:
            points = ", ".join(f"U+{ord(c):04X}" for c in homoglyph_hit[:3])
            return True, (
                f"セキュリティ: Latin 文字と紛らわしい Unicode 文字 ({points}) が"
                f" 同一トークン {token!r} 内に混在しています。"
                " コマンド名・URL 偽装の可能性があるため、ブロックします。"
            )
    return False, None


def _allow_response() -> int:
    """Cursor hook 向けの許可レスポンスを返す。"""
    json.dump({"permission": "allow"}, sys.stdout)
    return 0


def _emit_skip_warning(command: str) -> None:
    preview = command if len(command) <= 120 else command[:117] + "..."
    print(
        "[GUARDRAILS_SKIP] cursor bash_guard をスキップしました。"
        f" command={preview!r}"
        " 意図したテスト操作以外で本変数が立っている場合は環境を疑ってください。",
        file=sys.stderr,
    )


def main() -> int:
    if os.environ.get("CLAUDE_GUARDRAILS_SKIP") == "1":
        try:
            raw = sys.stdin.read()
            data = json.loads(raw) if raw.strip() else {}
            cmd = data.get("command", "")
        except Exception:
            cmd = ""
        _emit_skip_warning(cmd)
        return _allow_response()

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        # パース失敗時は fail-open（許可）。
        # Cursor Automation 等の非標準環境でコマンドが全拒否される問題を防ぐ。
        return _allow_response()

    # Cursor 形式: {command: "...", cwd: "...", hook_event_name: "beforeShellExecution"}
    command = data.get("command", "")
    if not command:
        return _allow_response()

    # --- L4: Unicode 悪用チェック ---
    blocked, message = _check_unicode_threats(command)
    if blocked:
        output = {
            "permission": "deny",
            "userMessage": message,
            "agentMessage": message,
        }
        json.dump(output, sys.stdout)
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

    # --- H3: ネット転送系 + 環境変数展開を警告 ---
    if NETWORK_TX_WITH_ENV.search(command):
        print(
            "[SECURITY WARNING] ネット転送コマンドに環境変数展開が含まれます。"
            " 認証情報・秘密の漏洩経路になり得ます。",
            file=sys.stderr,
        )

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

    return _allow_response()


if __name__ == "__main__":
    sys.exit(main())
