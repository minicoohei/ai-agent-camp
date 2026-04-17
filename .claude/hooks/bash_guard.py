#!/usr/bin/env python3
"""Claude Code PreToolUse hook: Bash コマンドの事前検査。

危険なコマンドをブロックし、rm コマンドを gomi に自動置換する。

入力: stdin から JSON (tool_input.command)
出力:
  - exit 0 + stdout JSON: 許可（updatedInput でコマンド書き換え可能）
  - exit 2 + stderr: ブロック
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys


# ---------------------------------------------------------------------------
# ブロックパターン: マッチした場合は即座に exit 2
# (compiled regex, stderr に表示するメッセージ)
# ---------------------------------------------------------------------------
BLOCK_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # .env への上書き（追記 >> は許可）
    (
        re.compile(r'[^>]>\s*\.env\b'),
        "セキュリティ: .env への上書き (>) は禁止です。追記 (>>) を使用してください。",
    ),
    # .env ファイルの削除（rm / gomi 両方）
    (
        re.compile(r'\b(?:rm|gomi)\s+.*\.env\b'),
        "セキュリティ: .env の削除は禁止です。",
    ),
    # 鍵・証明書ファイルの削除
    (
        re.compile(r'\b(?:rm|gomi)\s+.*\.(pem|key|p12|pfx)\b'),
        "セキュリティ: 鍵ファイル (.pem/.key/.p12/.pfx) の削除は禁止です。",
    ),
    # credentials / token ファイルの削除
    (
        re.compile(r'\b(?:rm|gomi)\s+.*(?:credentials|client_secret|token).*\.json\b'),
        "セキュリティ: 認証情報ファイルの削除は禁止です。",
    ),
    # sudo
    (
        re.compile(r'\bsudo\b'),
        "セキュリティ: sudo は使用禁止です。",
    ),
    # git push --force / -f （--force-with-lease / --force-if-includes は許可）
    (
        re.compile(r'\bgit\s+push\s+.*(?:--force(?![-\w])|(?<!\w)-f(?![-\w]))'),
        "セキュリティ: git push --force は禁止です。--force-with-lease を検討してください。",
    ),
    # git clean with -x（.env も削除される）
    (
        re.compile(r'\bgit\s+clean\s+.*-[a-zA-Z]*x'),
        "セキュリティ: git clean -x は .env 等も削除します。使用禁止です。",
    ),
    # curl/wget + API_KEY/TOKEN/SECRET 環境変数（データ流出防止）
    (
        re.compile(
            r'\b(?:curl|wget)\b.*\$\{?[A-Z_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)[A-Z_]*\}?',
            re.IGNORECASE,
        ),
        "セキュリティ: API キー等の環境変数を含む curl/wget は禁止です。",
    ),
    # curl/wget + Authorization/Bearer/X-* / 任意の独自認証ヘッダー（H3 強化）
    # `-H`, `--header`, `-H=`, `--header=` のいずれの形式でもマッチ。
    # ヘッダー名は標準（Authorization / X-Api-Key / X-Auth-Token）+ 一般的な
    # `X-*-Key` / `X-*-Token` / `X-*-Secret` / `Api-Key` / `Auth-Token` を網羅。
    (
        re.compile(
            r'\b(?:curl|wget)\b.*(?:-H[\s=]+|--header[\s=]+)["\']?'
            r'(?:Authorization|X-Api-Key|X-Auth-Token|Api-Key|Auth-Token|'
            r'X-[A-Za-z0-9_-]*-(?:Key|Token|Secret|Auth))\s*:\s*',
            re.IGNORECASE,
        ),
        "セキュリティ: 認証ヘッダーを含む curl/wget は禁止です。環境変数経由の認証情報が漏洩する可能性があります。",
    ),
    # curl/wget + --data/--form でトークンを送信
    (
        re.compile(
            r'\b(?:curl|wget)\b.*(?:--data|--form|-d\b|-F\b).*\$\{?[A-Z_]*(?:API_KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)[A-Z_]*\}?',
            re.IGNORECASE,
        ),
        "セキュリティ: リクエストボディに認証情報を含む curl/wget は禁止です。",
    ),
    # H3: -F file=@~/.ssh/... 等のローカルファイル添付経由のアップロード
    (
        re.compile(
            r'\b(?:curl|wget)\b.*(?:-F|--form)[\s=]+["\']?[A-Za-z0-9_-]+=@'
            r'(?:~|\$HOME|\$\{HOME\})?/?(?:\.ssh|\.aws|\.gnupg|\.config/gh|\.npmrc|\.pypirc)',
            re.IGNORECASE,
        ),
        "セキュリティ: 機密ファイル (.ssh / .aws / .gnupg 等) を curl で送信する操作は禁止です。",
    ),
    # H3: netcat / Bash の /dev/tcp/ 経由の exfil
    (
        re.compile(r'\|\s*nc\s+(?:-[A-Za-z]+\s+)*[\w.-]+\s+\d+'),
        "セキュリティ: netcat (`| nc host port`) によるデータ送信は禁止です。",
    ),
    (
        re.compile(r'>\s*/dev/(?:tcp|udp)/'),
        "セキュリティ: /dev/tcp/ 経由のネットワーク送信は禁止です。",
    ),
    # フォークボム
    (
        re.compile(r':\(\)\s*\{'),
        "セキュリティ: フォークボムパターンを検知しました。",
    ),
]

# ---------------------------------------------------------------------------
# H3: ネット転送系コマンド + 環境変数展開（警告ログ用、ブロックはしない）
# ---------------------------------------------------------------------------
NETWORK_TX_WITH_ENV: re.Pattern[str] = re.compile(
    r'\b(?:curl|wget|http|httpie)\b.*\$\{?[A-Z_][A-Z0-9_]*\}?',
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# L4: Unicode 悪用検知
# ---------------------------------------------------------------------------
# Bidirectional override (Trojan Source, CVE-2021-42574 系)。
# 表示上は無害に見えるが実際の実行順序を変えられるため、シェルコマンドに
# 現れた場合は常にブロックする。
BIDI_OVERRIDES: frozenset[str] = frozenset([
    "\u202a",  # LRE
    "\u202b",  # RLE
    "\u202c",  # PDF
    "\u202d",  # LRO
    "\u202e",  # RLO
    "\u2066",  # LRI
    "\u2067",  # RLI
    "\u2068",  # FSI
    "\u2069",  # PDI
])

# ゼロ幅・不可視文字。シェルで意図的に使う理由はまずなく、コマンド名の
# 偽装 (c\u200burl → curl と同一視されうる環境) や、監査ログ回避の手口に
# 使われうる。
INVISIBLE_CHARS: frozenset[str] = frozenset([
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\u2060",  # WORD JOINER
    "\ufeff",  # ZERO WIDTH NO-BREAK SPACE (BOM)
])

# よくある homograph: Latin 文字として見えるが別コードポイントの字。
# コマンド全体が非 ASCII なのは `echo "日本語"` 等で普通にあるので、
# 「Latin アルファベットとこれらの字が同じトークンに混在した場合のみ」
# 警告対象とする。
_SUSPICIOUS_HOMOGLYPHS: frozenset[str] = frozenset([
    # Cyrillic look-alikes
    "\u0430", "\u0435", "\u043e", "\u0440", "\u0441", "\u0443", "\u0445",
    "\u0455", "\u0456", "\u0458", "\u0501", "\u051b", "\u051d",
    # Greek look-alikes
    "\u03bf", "\u03c1", "\u03c5", "\u03c7",
    # Fullwidth Latin
    *(chr(cp) for cp in range(0xFF21, 0xFF5B)),
])


def _check_unicode_threats(command: str) -> tuple[bool, str | None]:
    """Unicode ベースの攻撃ベクタを検知する。

    Returns:
        (blocked, message). blocked=True なら呼び出し側で exit 2 する。
    """
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

    # homograph は警告のみ（誤検知を避けるため、Latin と混在したトークンを
    # 切り分けてから判定）。
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

# ---------------------------------------------------------------------------
# rm コマンドの検出パターン
# ---------------------------------------------------------------------------
RM_PATTERN = re.compile(r'(?:^|[;&|]\s*)rm\s')


def _check_gomi_available() -> bool:
    """gomi コマンドがインストールされているか確認する。"""
    return shutil.which("gomi") is not None


def _replace_rm_with_gomi(command: str) -> str:
    """コマンド内の rm を gomi に置換する。

    rm のオプション (-r, -f, -i 等) は除去し、ファイルパス引数のみ残す。
    """
    def _replacer(m: re.Match) -> str:
        full = m.group(0)
        # rm の前にある区切り文字（;, &&, || 等）を保持
        prefix_match = re.match(r'^(.*?)\brm\s+', full)
        if not prefix_match:
            return full
        prefix = prefix_match.group(1)
        # rm 以降の部分からオプションを除去
        after_rm = full[prefix_match.end():]
        # -X 形式のオプションを除去し、ファイルパスのみ残す
        args = []
        for token in after_rm.split():
            if not token.startswith("-"):
                args.append(token)
        return prefix + "gomi " + " ".join(args)

    return re.sub(r'(?:^|[;&|]\s*)rm\s+[^\n;|&]*', _replacer, command)


def _emit_skip_warning(command: str) -> None:
    """CLAUDE_GUARDRAILS_SKIP=1 でスキップした際の警告出力（H1）。"""
    preview = command if len(command) <= 120 else command[:117] + "..."
    print(
        "[GUARDRAILS_SKIP] bash_guard をスキップしました。"
        f" command={preview!r}"
        " 意図したテスト操作以外で本変数が立っている場合は環境を疑ってください。",
        file=sys.stderr,
    )


def main() -> int:
    """メインエントリポイント。stdin から JSON を読み取り検査する。"""
    if os.environ.get("CLAUDE_GUARDRAILS_SKIP") == "1":
        # H1: サイレントスキップを廃止し stderr に警告
        try:
            raw = sys.stdin.read()
            data = json.loads(raw) if raw.strip() else {}
            cmd = data.get("tool_input", {}).get("command", "")
        except Exception:
            cmd = ""
        _emit_skip_warning(cmd)
        return 0

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        # パース失敗時は fail-open（許可）。
        # 自動レビュー等の非標準環境でコマンドが全拒否される問題を防ぐ。
        return 0

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        return 0

    # --- L4: Unicode 悪用チェック（他のパターンより先に判定） ---
    blocked, message = _check_unicode_threats(command)
    if blocked:
        print(message, file=sys.stderr)
        return 2

    # --- ブロックパターンチェック ---
    for pattern, message in BLOCK_PATTERNS:
        if pattern.search(command):
            print(message, file=sys.stderr)
            return 2

    # --- H3: ネット転送系 + 環境変数展開を警告（ブロックはしない） ---
    if NETWORK_TX_WITH_ENV.search(command):
        print(
            "[SECURITY WARNING] ネット転送コマンドに環境変数展開が含まれます。"
            " 認証情報・秘密の漏洩経路になり得ます。意図した操作か確認してください。",
            file=sys.stderr,
        )
        # 警告のみで通過（過検知防止）

    # --- rm → gomi 自動置換 ---
    if RM_PATTERN.search(command):
        if _check_gomi_available():
            new_command = _replace_rm_with_gomi(command)
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "updatedInput": {
                        "command": new_command,
                        "description": tool_input.get("description", ""),
                    },
                    "additionalContext": (
                        "セキュリティ: rm コマンドを gomi に自動置換しました。"
                        f" 元のコマンド: {command}"
                    ),
                }
            }
            json.dump(output, sys.stdout)
            return 0
        else:
            print(
                "セキュリティ: rm コマンドは使用禁止です。\n"
                "安全な削除ツール gomi をインストールしてください:\n"
                "  brew install gomi  (macOS)\n"
                "  go install github.com/b4b4r07/gomi@latest  (Go)",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
