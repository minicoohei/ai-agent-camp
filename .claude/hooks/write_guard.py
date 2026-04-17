#!/usr/bin/env python3
"""Claude Code PreToolUse hook: Write/Edit ツールの事前検査。

保護対象ファイルへの書き込みブロックと、Prompt Injection 対策を行う。

入力: stdin から JSON (tool_input.file_path + tool_input.content/new_string)
出力:
  - exit 0: 許可（PI 警告時は stderr に出力）
  - exit 2 + stderr: ブロック
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import PurePosixPath


# ---------------------------------------------------------------------------
# 保護対象ファイルパターン: マッチしたパスへの書き込みをブロック
# ---------------------------------------------------------------------------
PROTECTED_FILE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'(^|/)\.env$'),
    re.compile(r'(^|/)\.env\.local$'),
    re.compile(r'(^|/)\.env\.(?!example$)[a-zA-Z][a-zA-Z.]*$'),
    re.compile(r'(^|/)credentials.*\.json$'),
    re.compile(r'(^|/)client_secret.*\.json$'),
    re.compile(r'(^|/)token\.json$'),
    re.compile(r'(^|/)refresh_token\.json$'),
    re.compile(r'\.(pem|key|p12|pfx)$'),
]

# ---------------------------------------------------------------------------
# Prompt Injection 検知パターン
# ---------------------------------------------------------------------------
PI_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'ignore\s+(?:all\s+)?(?:previous|above|prior)\s+instructions?', re.IGNORECASE),
    re.compile(r'disregard\s+(?:your|all|any)\s+(?:previous\s+)?(?:instructions?|rules?)', re.IGNORECASE),
    re.compile(r'override\s+(?:your\s+)?(?:previous\s+)?instructions?', re.IGNORECASE),
    re.compile(r'forget\s+(?:everything|all)\s+(?:you|i)\s+(?:have\s+)?(?:told|said|written)', re.IGNORECASE),
    re.compile(r'you\s+are\s+now\s+(?:a\s+)?(?:different|new|unrestricted)', re.IGNORECASE),
    re.compile(r'act\s+as\s+(?:if\s+)?(?:you\s+are\s+)?(?:an?\s+)?unrestricted', re.IGNORECASE),
    re.compile(r'system\s*prompt\s*:', re.IGNORECASE),
    # LLM 系メタタグ（チャットテンプレートや境界偽装）
    re.compile(r'<\s*\|?\s*im_(?:start|end)\s*\|?\s*>', re.IGNORECASE),
    re.compile(r'<\s*\|?\s*(?:system|assistant|user)\s*\|?\s*>', re.IGNORECASE),
    re.compile(r'<\s*EXTREMELY[-_\s]*IMPORTANT\s*>', re.IGNORECASE),
    re.compile(r'</?\s*external_untrusted_content\s*/?\s*>', re.IGNORECASE),
    # 日本語パターン（拡充）
    re.compile(r'新しい指示.*従[えい]'),
    re.compile(r'前の指示.*無視'),
    re.compile(r'(?:これまで|以前)の(?:指示|ルール).*(?:無視|忘れ)'),
    re.compile(r'指示.*上書き'),
    re.compile(r'新しい役割'),
    re.compile(r'ルール.*無視'),
    re.compile(r'制限.*解除'),
    re.compile(r'制限なく'),
]

# PI と組み合わせた場合に危険な操作パターン
PI_DANGEROUS_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r'\bcurl\s+.*https?://', re.IGNORECASE),
    re.compile(r'\bwget\s+.*https?://', re.IGNORECASE),
    re.compile(r'\beval\s*\(', re.IGNORECASE),
    re.compile(r'\bexec\s*\(', re.IGNORECASE),
    re.compile(r'\bos\.system\s*\(', re.IGNORECASE),
    re.compile(r'\bsubprocess\b', re.IGNORECASE),
    re.compile(r'\brm\s+-rf\b'),
    re.compile(r'\bbase64\s+--decode\b'),
]


def _is_protected_file(file_path: str) -> bool:
    """ファイルパスが保護対象にマッチするか判定する。"""
    # 絶対パスの場合はファイル名部分のみで判定
    normalized = PurePosixPath(file_path).as_posix()
    for pattern in PROTECTED_FILE_PATTERNS:
        if pattern.search(normalized):
            return True
    return False


def _check_pi(content: str) -> tuple[bool, bool]:
    """PI パターンと危険操作パターンを検査する。

    Returns:
        (has_pi, has_dangerous): PI パターン検出, 危険操作検出
    """
    has_pi = any(p.search(content) for p in PI_PATTERNS)
    has_dangerous = any(p.search(content) for p in PI_DANGEROUS_PATTERNS)
    return has_pi, has_dangerous


def _emit_skip_warning(file_path: str) -> None:
    """CLAUDE_GUARDRAILS_SKIP=1 でスキップした際の警告出力（H1）。"""
    print(
        "[GUARDRAILS_SKIP] write_guard をスキップしました "
        f"(file={file_path or 'unknown'})。"
        " 意図したテスト操作以外で本変数が立っている場合は環境を疑ってください。",
        file=sys.stderr,
    )


def main() -> int:
    """メインエントリポイント。"""
    if os.environ.get("CLAUDE_GUARDRAILS_SKIP") == "1":
        # H1: サイレントスキップを廃止し stderr に警告
        try:
            raw = sys.stdin.read()
            data = json.loads(raw) if raw.strip() else {}
            fp = data.get("tool_input", {}).get("file_path", "")
        except Exception:
            fp = ""
        _emit_skip_warning(fp)
        return 0

    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        print("セキュリティ: hook 入力を解析できないため書き込みを拒否しました。", file=sys.stderr)
        return 2

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        return 0

    # --- 保護対象ファイルチェック ---
    if _is_protected_file(file_path):
        print(
            f"セキュリティ: {file_path} は保護対象ファイルです。書き込みは禁止されています。",
            file=sys.stderr,
        )
        return 2

    # --- PI + 危険操作の組み合わせ検知 ---
    # Write: content, Edit: new_string
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    if content:
        has_pi, has_dangerous = _check_pi(content)
        if has_pi and has_dangerous:
            print(
                "セキュリティ: Prompt Injection パターンと危険な操作の組み合わせを検知しました。"
                " 書き込みをブロックします。",
                file=sys.stderr,
            )
            return 2
        if has_pi:
            # H2: PI 単独でも書き込みをブロックし、人間の確認を要求する。
            # 正当な書き込みであれば CLAUDE_GUARDRAILS_SKIP=1 で再実行可能。
            print(
                "セキュリティ: Prompt Injection パターンを検知しました。"
                " 書き込みをブロックします。"
                " 正当な内容（PI ペイロードのテストデータ等）であれば"
                " CLAUDE_GUARDRAILS_SKIP=1 を付けて再実行してください。",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
