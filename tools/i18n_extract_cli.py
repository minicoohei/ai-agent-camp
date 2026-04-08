"""
i18n CLI Extract Tool

Python CLI ツールの翻訳対象文字列を抽出し、gettext パイプラインを管理する。
- AST パースで _() 呼び出しから文字列を抽出
- 標準 .pot 形式で出力
- Gemini API で .po 翻訳
- 純 Python で .po → .mo コンパイル（外部バイナリ不要）

使い方:
  uv run python tools/i18n_extract_cli.py                          # .pot 生成
  uv run python tools/i18n_extract_cli.py --scan                    # 未マーキング print() 検出
  uv run python tools/i18n_extract_cli.py --translate --lang en es  # .po + .mo 生成
  uv run python tools/i18n_extract_cli.py --check                   # .pot が最新か検証
  uv run python tools/i18n_extract_cli.py --dry-run                 # 統計のみ
"""

import argparse
import ast
import json
import struct
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_common import ROOT_DIR, CLI_LOCALES_DIR, get_language_name
except ImportError:
    from tools.i18n_common import ROOT_DIR, CLI_LOCALES_DIR, get_language_name

# 対象ファイル（ハードコード、段階的に追加）
DEFAULT_CLI_FILES = [
    "tools/credential_manager.py",
    "tools/setup_progress.py",
    "tools/banner_creator.py",
]

DOMAIN = "aiagent"
BATCH_SIZE = 50


# =============================================================================
# データ構造
# =============================================================================

@dataclass
class PotEntry:
    """POT ファイルの 1 エントリ"""
    msgid: str
    references: List[str] = field(default_factory=list)  # "file:line" のリスト


# =============================================================================
# AST 抽出
# =============================================================================

class _GettextVisitor(ast.NodeVisitor):
    """_() 呼び出しから文字列リテラルを抽出する AST ビジター"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.entries: List[PotEntry] = []

    def visit_Call(self, node: ast.Call):
        # _("文字列") パターンを検出
        if (isinstance(node.func, ast.Name) and node.func.id == "_"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            msgid = node.args[0].value
            if msgid.strip():
                ref = f"{self.filepath}:{node.lineno}"
                self.entries.append(PotEntry(msgid=msgid, references=[ref]))
        self.generic_visit(node)


class _UnmarkedPrintVisitor(ast.NodeVisitor):
    """print() 呼び出しで _() を使っていないものを検出"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.unmarked: List[dict] = []

    def visit_Call(self, node: ast.Call):
        if not (isinstance(node.func, ast.Name) and node.func.id == "print"):
            self.generic_visit(node)
            return

        # file=sys.stderr やファイルオブジェクトへの出力はスキップ
        # file=sys.stdout は通常の stdout 出力なので検査対象
        for kw in node.keywords:
            if kw.arg == "file":
                val = kw.value
                # sys.stdout は検査対象として続行
                if (isinstance(val, ast.Attribute)
                        and isinstance(val.value, ast.Name)
                        and val.value.id == "sys" and val.attr == "stdout"):
                    break
                # それ以外 (sys.stderr, open() 等) はスキップ
                self.generic_visit(node)
                return

        # 引数なし print はスキップ
        if not node.args:
            self.generic_visit(node)
            return

        first_arg = node.args[0]

        # print(_("...")) はマーキング済み → スキップ
        if (isinstance(first_arg, ast.Call)
                and isinstance(first_arg.func, ast.Name)
                and first_arg.func.id == "_"):
            self.generic_visit(node)
            return

        # print("-" * N) 等の装飾はスキップ
        if isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Mult):
            self.generic_visit(node)
            return

        # 文字列リテラルまたは f-string を含む print を報告
        text = ""
        is_fstring = False
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            text = first_arg.value
        elif isinstance(first_arg, ast.JoinedStr):
            is_fstring = True
            # f-string のテキスト部分を抽出
            parts = []
            for v in first_arg.values:
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    parts.append(v.value)
                else:
                    parts.append("{...}")
            text = "".join(parts)

        if text.strip():
            self.unmarked.append({
                "file": self.filepath,
                "line": node.lineno,
                "text": text,
                "is_fstring": is_fstring,
            })

        self.generic_visit(node)


def extract_strings_from_file(filepath: str) -> List[PotEntry]:
    """ファイルから _() 呼び出しの文字列を AST で抽出"""
    source_path = ROOT_DIR / filepath
    if not source_path.exists():
        return []
    source = source_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        print(f"[WARN] SyntaxError in {filepath}, skipping", file=sys.stderr)
        return []
    visitor = _GettextVisitor(filepath)
    visitor.visit(tree)
    return visitor.entries


def scan_unmarked_prints(filepath: str) -> List[dict]:
    """ファイル内の未マーキング print() を検出"""
    source_path = ROOT_DIR / filepath
    if not source_path.exists():
        return []
    source = source_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return []
    visitor = _UnmarkedPrintVisitor(filepath)
    visitor.visit(tree)
    return visitor.unmarked


def extract_all(files: List[str]) -> List[PotEntry]:
    """複数ファイルから抽出して重複を統合"""
    all_entries: Dict[str, PotEntry] = {}
    for filepath in files:
        entries = extract_strings_from_file(filepath)
        for entry in entries:
            if entry.msgid in all_entries:
                all_entries[entry.msgid].references.extend(entry.references)
            else:
                all_entries[entry.msgid] = entry
    return list(all_entries.values())


# =============================================================================
# POT 生成
# =============================================================================

def _escape_po_string(s: str) -> str:
    """PO ファイル用の文字列エスケープ"""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\t", "\\t")
    return s


def _format_po_string(s: str) -> str:
    """長い文字列を PO 形式の複数行に分割"""
    escaped = _escape_po_string(s)
    if "\\n" in escaped and escaped != "\\n":
        # 改行を含む場合は分割
        parts = escaped.split("\\n")
        lines = ['""']
        for i, part in enumerate(parts):
            suffix = "\\n" if i < len(parts) - 1 else ""
            if part or suffix:
                lines.append(f'"{part}{suffix}"')
        return "\n".join(lines)
    return f'"{escaped}"'


def generate_pot(entries: List[PotEntry]) -> str:
    """PotEntry リストから .pot ファイル文字列を生成"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M+0000")
    lines = [
        '# aiagent-base CLI translation template.',
        f'# Generated: {now}',
        '#',
        'msgid ""',
        'msgstr ""',
        f'"Project-Id-Version: aiagent-base 1.0\\n"',
        f'"POT-Creation-Date: {now}\\n"',
        '"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"',
        '"Language: \\n"',
        '"MIME-Version: 1.0\\n"',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Content-Transfer-Encoding: 8bit\\n"',
        '',
    ]

    for entry in entries:
        lines.append("")
        for ref in entry.references:
            lines.append(f"#: {ref}")
        lines.append(f"msgid {_format_po_string(entry.msgid)}")
        lines.append('msgstr ""')

    lines.append("")
    return "\n".join(lines)


# =============================================================================
# PO パーサー
# =============================================================================

def _unescape_po_string(s: str) -> str:
    """PO 文字列のアンエスケープ"""
    s = s.replace("\\n", "\n")
    s = s.replace("\\t", "\t")
    s = s.replace('\\"', '"')
    s = s.replace("\\\\", "\\")
    return s


def parse_po_file(po_path: Path) -> List[Tuple[str, str]]:
    """PO ファイルを解析して (msgid, msgstr) ペアを返す"""
    content = po_path.read_text(encoding="utf-8")
    entries: List[Tuple[str, str]] = []

    current_key = None  # "msgid" or "msgstr"
    msgid_parts: List[str] = []
    msgstr_parts: List[str] = []

    def _flush():
        nonlocal msgid_parts, msgstr_parts
        mid = _unescape_po_string("".join(msgid_parts))
        mstr = _unescape_po_string("".join(msgstr_parts))
        # ヘッダ (msgid "") も含める — MO コンパイルに charset 情報が必要
        entries.append((mid, mstr))
        msgid_parts = []
        msgstr_parts = []

    for line in content.split("\n"):
        line = line.strip()

        # コメント・空行
        if line.startswith("#") or not line:
            if current_key == "msgstr":
                _flush()
                current_key = None
            continue

        if line.startswith("msgid "):
            if current_key == "msgstr":
                _flush()
            current_key = "msgid"
            # "..." 部分を抽出
            val = line[6:].strip().strip('"')
            msgid_parts = [val]
            msgstr_parts = []
        elif line.startswith("msgstr "):
            current_key = "msgstr"
            val = line[7:].strip().strip('"')
            msgstr_parts = [val]
        elif line.startswith('"') and line.endswith('"'):
            # 継続行
            val = line[1:-1]
            if current_key == "msgid":
                msgid_parts.append(val)
            elif current_key == "msgstr":
                msgstr_parts.append(val)

    # 最後のエントリ
    if current_key == "msgstr":
        _flush()

    return entries


# =============================================================================
# MO コンパイラ（純 Python 実装）
# =============================================================================

def compile_mo(po_path: Path, mo_path: Path) -> bool:
    """Pure-Python .po → .mo コンパイラ。

    CPython Tools/i18n/msgfmt.py のロジックに基づく。
    外部バイナリ (msgfmt) は不要。
    """
    entries = parse_po_file(po_path)

    if not entries:
        return False

    # msgid バイト列でソート（バイナリサーチ用）
    byte_entries = [
        (msgid.encode("utf-8"), msgstr.encode("utf-8"))
        for msgid, msgstr in entries
    ]
    byte_entries.sort(key=lambda x: x[0])

    # オフセット計算
    n = len(byte_entries)
    # ヘッダ: 7 x uint32 = 28 bytes
    # オフセットテーブル: 2 x n x (2 x uint32) = 16n bytes
    header_size = 28
    table_size = 8 * n  # 各テーブル n エントリ x (length, offset)
    keystart = header_size + 2 * table_size
    # ids の合計サイズ
    ids = bytearray()
    strs = bytearray()
    koffsets = []
    voffsets = []

    for msgid_b, msgstr_b in byte_entries:
        koffsets.append((len(msgid_b), keystart + len(ids)))
        ids += msgid_b + b"\0"
        voffsets.append((len(msgstr_b), keystart + len(ids) + len(strs)))

    # strs のベースオフセットを再計算
    valuestart = keystart + len(ids)
    voffsets = []
    strs = bytearray()
    for msgid_b, msgstr_b in byte_entries:
        voffsets.append((len(msgstr_b), valuestart + len(strs)))
        strs += msgstr_b + b"\0"

    # バイナリ出力
    output = struct.pack(
        "Iiiiiii",
        0x950412DE,             # magic number
        0,                      # revision
        n,                      # number of strings
        header_size,            # offset of table with original strings
        header_size + table_size,  # offset of table with translation strings
        0, 0,                   # size/offset of hash table
    )

    for length, offset in koffsets:
        output += struct.pack("ii", length, offset)
    for length, offset in voffsets:
        output += struct.pack("ii", length, offset)

    output += bytes(ids) + bytes(strs)

    mo_path.parent.mkdir(parents=True, exist_ok=True)
    mo_path.write_bytes(output)
    return True


# =============================================================================
# PO 生成（翻訳付き）
# =============================================================================

def generate_po(pot_text: str, translations: Dict[str, str], lang: str) -> str:
    """POT テキストに翻訳を埋めて PO を生成"""
    lines = pot_text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # ヘッダの Language フィールドを設定
        if line == '"Language: \\n"':
            result.append(f'"Language: {lang}\\n"')
            i += 1
            continue

        # msgid を検出して対応する msgstr を埋める
        if line.startswith("msgid ") and not line.startswith('msgid ""'):
            # msgid の全行を収集
            msgid_lines = [line]
            j = i + 1
            while j < len(lines) and lines[j].startswith('"'):
                msgid_lines.append(lines[j])
                j += 1

            # msgid テキストを復元
            parts = []
            for ml in msgid_lines:
                if ml.startswith("msgid "):
                    parts.append(ml[6:].strip().strip('"'))
                else:
                    parts.append(ml.strip('"'))
            msgid_text = _unescape_po_string("".join(parts))

            # 翻訳を検索
            trans = translations.get(msgid_text, "")

            result.extend(msgid_lines)
            result.append(f"msgstr {_format_po_string(trans)}" if trans else 'msgstr ""')

            # 元の msgstr 行をスキップ
            i = j
            if i < len(lines) and lines[i].startswith("msgstr "):
                i += 1
                while i < len(lines) and lines[i].startswith('"'):
                    i += 1
            continue

        result.append(line)
        i += 1

    return "\n".join(result)


# =============================================================================
# 翻訳（Gemini API）
# =============================================================================

def translate_pot_entries(
    client,
    entries: List[PotEntry],
    lang: str,
    model: Optional[str] = None,
) -> Dict[str, str]:
    """Gemini API で PotEntry のバッチ翻訳"""
    lang_name = get_language_name(lang)
    translations: Dict[str, str] = {}

    # バッチに分割
    for batch_start in range(0, len(entries), BATCH_SIZE):
        batch = entries[batch_start:batch_start + BATCH_SIZE]
        source = {e.msgid: e.msgid for e in batch}

        prompt = f"""Translate the following CLI tool messages from Japanese to {lang_name}.

RULES:
1. Keep keys exactly as-is (they are the Japanese original), translate only values.
2. Preserve emoji characters at their original positions.
3. Preserve {{placeholder}} and %s/%d format specifiers exactly.
4. Keep technical terms: keyring, Credential Store, dotenv, API key, etc.
5. Keep file paths, command names, environment variable names untranslated.
6. Return ONLY valid JSON (no markdown fences).

Input JSON:
{json.dumps(source, ensure_ascii=False, indent=2)}
"""
        try:
            response = client.models.generate_content(
                model=model or "gemini-2.0-flash",
                contents=prompt,
            )
            text = response.text.strip()
            # JSON フェンス除去
            if text.startswith("```"):
                text = "\n".join(text.split("\n")[1:])
            if text.endswith("```"):
                text = "\n".join(text.split("\n")[:-1])
            result = json.loads(text)
            translations.update(result)
        except Exception as e:
            print(f"[WARN] Batch translation failed: {e}", file=sys.stderr)

    return translations


# =============================================================================
# チェックモード
# =============================================================================

def check_pot_freshness(pot_path: Path, files: List[str]) -> bool:
    """現在のソースから抽出した結果と既存 .pot の msgid を比較"""
    if not pot_path.exists():
        print("[CHECK] .pot file not found", file=sys.stderr)
        return False

    # 現在のソースから抽出
    current_entries = extract_all(files)
    current_msgids = {e.msgid for e in current_entries}

    # 既存 .pot の msgid を取得（multiline 対応: parse_po_file 使用）
    existing_msgids = set()
    for mid, _mstr in parse_po_file(pot_path):
        if mid:  # ヘッダー (msgid "") を除外
            existing_msgids.add(mid)

    added = current_msgids - existing_msgids
    removed = existing_msgids - current_msgids

    if added or removed:
        if added:
            print(f"[CHECK] {len(added)} new msgid(s) not in .pot:")
            for m in sorted(added)[:5]:
                print(f"  + {m[:60]}")
        if removed:
            print(f"[CHECK] {len(removed)} msgid(s) in .pot but not in source:")
            for m in sorted(removed)[:5]:
                print(f"  - {m[:60]}")
        return False

    print(f"[CHECK] .pot is up to date ({len(current_msgids)} msgids)")
    return True


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract translatable strings from CLI tools and manage gettext pipeline"
    )
    parser.add_argument("--scan", action="store_true",
                        help="Scan for unmarked print() calls")
    parser.add_argument("--translate", action="store_true",
                        help="Translate .pot to .po and compile .mo")
    parser.add_argument("--lang", nargs="+", default=["en"],
                        help="Target languages (default: en)")
    parser.add_argument("--check", action="store_true",
                        help="Check if .pot is up to date")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show stats without writing files")
    parser.add_argument("--files", nargs="+",
                        help="Target Python files (default: auto-discover)")
    parser.add_argument("--model", default=None,
                        help="Gemini model override")
    args = parser.parse_args()

    files = args.files or DEFAULT_CLI_FILES
    pot_path = CLI_LOCALES_DIR / f"{DOMAIN}.pot"

    # --scan モード
    if args.scan:
        total = 0
        for filepath in files:
            unmarked = scan_unmarked_prints(filepath)
            if unmarked:
                print(f"\n{filepath}:")
                for item in unmarked:
                    fstr = " [f-string]" if item["is_fstring"] else ""
                    print(f"  L{item['line']}: {item['text'][:70]}{fstr}")
                total += len(unmarked)
        print(f"\nTotal unmarked print(): {total}")
        return

    # --check モード
    if args.check:
        ok = check_pot_freshness(pot_path, files)
        sys.exit(0 if ok else 1)

    # 抽出
    entries = extract_all(files)
    print(f"Extracted {len(entries)} unique msgids from {len(files)} files")

    if args.dry_run:
        for entry in entries[:10]:
            print(f"  [{entry.references[0]}] {entry.msgid[:60]}")
        if len(entries) > 10:
            print(f"  ... and {len(entries) - 10} more")
        return

    # .pot 生成
    pot_text = generate_pot(entries)
    CLI_LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    pot_path.write_text(pot_text, encoding="utf-8")
    print(f"Written: {pot_path}")

    # --translate モード
    if args.translate:
        from i18n_common import require_gemini_client
        client = require_gemini_client()

        for lang in args.lang:
            print(f"\n--- Translating to {get_language_name(lang)} ({lang}) ---")
            translations = translate_pot_entries(client, entries, lang, model=args.model)
            print(f"  Translated: {len(translations)} / {len(entries)}")

            # .po 生成
            po_text = generate_po(pot_text, translations, lang)
            po_path = CLI_LOCALES_DIR / lang / "LC_MESSAGES" / f"{DOMAIN}.po"
            po_path.parent.mkdir(parents=True, exist_ok=True)
            po_path.write_text(po_text, encoding="utf-8")
            print(f"  Written: {po_path}")

            # .mo コンパイル
            mo_path = po_path.with_suffix(".mo")
            if compile_mo(po_path, mo_path):
                print(f"  Compiled: {mo_path}")
            else:
                print(f"  [WARN] Failed to compile {mo_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
