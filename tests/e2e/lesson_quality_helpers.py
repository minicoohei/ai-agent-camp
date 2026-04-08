"""レッスン品質テスト用共有ユーティリティ"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = PROJECT_ROOT / "output" / "test-results"

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

class CodeBlock(NamedTuple):
    language: str  # "" if no language specifier
    content: str
    line_number: int


class MermaidBlock(NamedTuple):
    content: str
    line_number: int


class AsciiArtBlock(NamedTuple):
    lines: list[str]
    line_start: int
    line_end: int


class TableBlock(NamedTuple):
    rows: list[str]
    line_start: int
    column_count: int
    has_separator: bool


# ---------------------------------------------------------------------------
# Extraction functions
# ---------------------------------------------------------------------------

_FENCE_OPEN_RE = re.compile(r"^(`{3,})(\w*)\s*$")
_FENCE_CLOSE_RE = re.compile(r"^`{3,}\s*$")
_BOX_CHARS = set("┌┐└┘│─├┤┬┴┼╭╮╰╯╔╗╚╝║═╠╣╦╩╬┏┓┗┛┃━┣┫┳┻╋")
_TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\|[\s\-:]+\|\s*$")


def extract_code_blocks(text: str) -> list[CodeBlock]:
    """テキストから全コードブロックを抽出する。"""
    blocks: list[CodeBlock] = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = _FENCE_OPEN_RE.match(lines[i])
        if m:
            fence_marker = m.group(1)
            lang = m.group(2)
            start = i + 1
            content_lines: list[str] = []
            i += 1
            while i < len(lines):
                if lines[i].startswith(fence_marker) and _FENCE_CLOSE_RE.match(lines[i]):
                    break
                content_lines.append(lines[i])
                i += 1
            blocks.append(CodeBlock(lang, "\n".join(content_lines), start))
        i += 1
    return blocks


def extract_mermaid_blocks(text: str) -> list[MermaidBlock]:
    """```mermaid ブロックを抽出する。"""
    return [
        MermaidBlock(cb.content, cb.line_number)
        for cb in extract_code_blocks(text)
        if cb.language == "mermaid"
    ]


def extract_ascii_art_blocks(text: str) -> list[AsciiArtBlock]:
    """Box-drawing 文字を含む連続行ブロックを抽出する。"""
    blocks: list[AsciiArtBlock] = []
    lines = text.split("\n")
    current: list[str] = []
    start = 0
    for i, line in enumerate(lines, 1):
        if any(c in _BOX_CHARS for c in line):
            if not current:
                start = i
            current.append(line)
        else:
            if current:
                blocks.append(AsciiArtBlock(current[:], start, start + len(current) - 1))
                current = []
    if current:
        blocks.append(AsciiArtBlock(current[:], start, start + len(current) - 1))
    return blocks


def extract_tables(text: str) -> list[TableBlock]:
    """Markdown テーブルを抽出する。"""
    tables: list[TableBlock] = []
    lines = text.split("\n")
    current: list[str] = []
    start = 0
    has_sep = False
    for i, line in enumerate(lines, 1):
        if _TABLE_ROW_RE.match(line):
            if not current:
                start = i
            current.append(line)
            if _TABLE_SEP_RE.match(line):
                has_sep = True
        else:
            if len(current) >= 2:
                col_count = current[0].count("|") - 1
                tables.append(TableBlock(current[:], start, col_count, has_sep))
            current = []
            has_sep = False
    if len(current) >= 2:
        col_count = current[0].count("|") - 1
        tables.append(TableBlock(current[:], start, col_count, has_sep))
    return tables


# ---------------------------------------------------------------------------
# Mermaid validation
# ---------------------------------------------------------------------------

_MERMAID_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "gantt",
    "pie", "journey", "gitgraph", "mindmap", "timeline",
    "quadrantChart", "sankey-beta", "xychart-beta",
}


def validate_mermaid_syntax(content: str) -> tuple[bool, str]:
    """Mermaid ブロックの基本構文をチェック。(valid, error_message)"""
    stripped = content.strip()
    if not stripped:
        return False, "empty mermaid block"
    first_word = stripped.split()[0].rstrip(";")
    if first_word not in _MERMAID_TYPES:
        return False, f"unknown diagram type: {first_word}"
    return True, ""


# ---------------------------------------------------------------------------
# Evidence report
# ---------------------------------------------------------------------------

def write_evidence_report(data: dict, filename: str) -> Path:
    """エビデンスレポートを JSON で出力する。"""
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    data["_generated_at"] = datetime.now(timezone.utc).isoformat()
    path = EVIDENCE_DIR / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Jargon terms (for beginner readability check)
# ---------------------------------------------------------------------------

JARGON_TERMS = {
    "API": r"(Application Programming Interface|インターフェース|接続|連携)",
    "CLI": r"(Command Line Interface|コマンドライン|ターミナル)",
    "SDK": r"(Software Development Kit|開発キット)",
    "JSON": r"(JavaScript Object Notation|データ形式|フォーマット)",
    "YAML": r"(YAML Ain't Markup Language|設定ファイル|マークアップ)",
    "OAuth": r"(認証|認可|アクセス許可|ログイン)",
    "webhook": r"(通知|コールバック|自動連携)",
    "deploy": r"(デプロイ|公開|配置|リリース)",
    "CI/CD": r"(継続的|自動テスト|自動デプロイ|パイプライン)",
    "repository": r"(リポジトリ|レポ|コード管理|保管場所)",
    "endpoint": r"(エンドポイント|接続先|URL|アドレス)",
    "token": r"(トークン|認証キー|アクセスキー|認証情報)",
}
