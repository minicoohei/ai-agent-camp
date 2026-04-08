#!/usr/bin/env python3
"""i18n QA checking tool for translated MD files.

Verifies the quality of translated MD files in ``dist/{lang}/``.
Runs 6 named checks covering frontmatter, key coverage, tables,
inline code, image references, and AskQuestion JSON blocks.

Usage:
    uv run python tools/i18n_check_md.py --lang en es
    uv run python tools/i18n_check_md.py --lang en --checks key_coverage,table_cell_count
    uv run python tools/i18n_check_md.py --lang en --json
    uv run python tools/i18n_check_md.py --lang en --verbose
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_check import Issue, CheckResult
except ImportError:
    from tools.i18n_check import Issue, CheckResult

try:
    from i18n_common import ROOT_DIR, MD_LOCALES_DIR, DIST_DIR_ROOT, COMMANDS_DIR, SKILLS_DIR
except ImportError:
    from tools.i18n_common import ROOT_DIR, MD_LOCALES_DIR, DIST_DIR_ROOT, COMMANDS_DIR, SKILLS_DIR


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RE_JAPANESE = re.compile(
    r"[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\u4E00-\u9FFF\u3400-\u4DBF\u3000-\u303F\uFF01-\uFF5E]"
)
TABLE_SEP_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
IMAGE_REF_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
FRONTMATTER_REQUIRED_FIELDS = {"description"}


# ---------------------------------------------------------------------------
# File loading helpers
# ---------------------------------------------------------------------------

def _load_md_files(base_dir: Path) -> Dict[str, str]:
    """base_dir 配下の .md ファイルを {相対パス: 内容} で返す"""
    files: Dict[str, str] = {}
    if not base_dir.exists():
        return files
    for f in sorted(base_dir.rglob("*.md")):
        rel = str(f.relative_to(base_dir))
        files[rel] = f.read_text(encoding="utf-8", errors="replace")
    return files


def _load_locale_json(lang: str) -> Dict[str, Any]:
    """locales/md/{lang}.json を読み込む"""
    path = MD_LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _parse_frontmatter(content: str) -> Dict[str, str] | None:
    """YAML frontmatter を簡易パース。なければ None。"""
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fm_lines: List[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    else:
        return None  # 閉じ --- がない

    result: Dict[str, str] = {}
    for line in fm_lines:
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _count_table_cols(line: str) -> int:
    """テーブル行のカラム数を返す（パイプ区切りのセル数）"""
    stripped = line.strip()
    if "|" not in stripped:
        return 0
    # 先頭・末尾のパイプを除去してセルで分割
    inner = stripped.strip("|")
    return len([c for c in inner.split("|")])


def _extract_tables(content: str) -> List[List[str]]:
    """MD コンテンツからテーブルブロック（行リスト）を抽出"""
    tables: List[List[str]] = []
    current: List[str] = []
    in_code = False

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if "|" in stripped and not TABLE_SEP_RE.match(stripped):
            current.append(stripped)
        elif TABLE_SEP_RE.match(stripped):
            current.append(stripped)
        else:
            if current:
                tables.append(current)
                current = []
    if current:
        tables.append(current)
    return tables


def _extract_json_blocks(content: str) -> List[str]:
    """コードブロック内の JSON を抽出"""
    blocks: List[str] = []
    in_json = False
    buf: List[str] = []

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```json"):
            in_json = True
            buf = []
            continue
        if in_json and stripped == "```":
            in_json = False
            text = "\n".join(buf)
            if text.strip():
                blocks.append(text)
            continue
        if in_json:
            buf.append(line)
    return blocks


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------

def check_frontmatter_integrity(
    lang: str,
    source_files: Dict[str, str],
    translated_files: Dict[str, str],
    **kw: Any,
) -> CheckResult:
    """翻訳済み MD の frontmatter 整合性チェック"""
    result = CheckResult("frontmatter_integrity")

    for rel, content in translated_files.items():
        result.total += 1
        fm = _parse_frontmatter(content)
        file_has_issue = False

        if fm is None:
            result.add_issue(Issue(rel, None, "frontmatter が存在しない"))
            continue

        # 必須フィールド
        for field in FRONTMATTER_REQUIRED_FIELDS:
            if field not in fm or not fm[field]:
                result.add_issue(Issue(rel, None, f"frontmatter に {field} がない"))
                file_has_issue = True

        # 日本語残留チェック（en等の非日本語言語のみ）
        if lang != "ja":
            for key, val in fm.items():
                if val and RE_JAPANESE.search(val):
                    result.add_issue(Issue(
                        rel, None,
                        f"frontmatter.{key} に日本語が残っている: {val[:40]}...",
                        severity="WARN",
                    ))
                    file_has_issue = True

        if not file_has_issue:
            result.passed += 1

    return result


def check_key_coverage(
    lang: str,
    source_files: Dict[str, str] | None = None,
    translated_files: Dict[str, str] | None = None,
    **kw: Any,
) -> CheckResult:
    """locales/md/ja.json vs {lang}.json のキーカバレッジ"""
    result = CheckResult("key_coverage")

    ja_data = _load_locale_json("ja")
    lang_data = _load_locale_json(lang)

    if not ja_data:
        # ja.json がない → 抽出未実行、PASS扱い
        return result
    if not lang_data:
        result.add_issue(Issue(
            f"locales/md/{lang}.json", None,
            f"{lang}.json が見つからない（翻訳未実行）",
        ))
        return result

    # ファイル単位で比較
    for file_key in ja_data:
        result.total += 1
        if file_key not in lang_data:
            result.add_issue(Issue(
                file_key, None,
                f"ファイル全体が {lang}.json に欠落",
            ))
            continue

        if not isinstance(ja_data[file_key], dict):
            result.add_issue(Issue(
                file_key, None,
                f"ja.json のデータ構造が不正 (dict 以外)",
                severity="WARN",
            ))
            continue
        ja_keys = set(ja_data[file_key].keys())
        lang_keys = set(lang_data[file_key].keys()) if isinstance(lang_data[file_key], dict) else set()
        missing = ja_keys - lang_keys

        if missing:
            sample = sorted(missing)[:3]
            result.add_issue(Issue(
                file_key, None,
                f"{len(missing)} キーが欠落: {', '.join(sample)}...",
                severity="WARN",
            ))
        else:
            result.passed += 1

    return result


def check_table_cell_count(
    lang: str,
    source_files: Dict[str, str],
    translated_files: Dict[str, str],
    **kw: Any,
) -> CheckResult:
    """ソース vs 翻訳でテーブル列数が一致するか"""
    result = CheckResult("table_cell_count")

    for rel in translated_files:
        if rel not in source_files:
            continue

        src_tables = _extract_tables(source_files[rel])
        trans_tables = _extract_tables(translated_files[rel])

        # テーブル数の差を検出
        if len(src_tables) != len(trans_tables):
            result.total += 1
            result.add_issue(Issue(
                rel, None,
                f"テーブル数不一致 (src={len(src_tables)}, trans={len(trans_tables)})",
                severity="WARN",
            ))

        for i, (src_t, trans_t) in enumerate(zip(src_tables, trans_tables)):
            result.total += 1
            if not src_t or not trans_t:
                result.passed += 1
                continue
            # ヘッダー行の列数で比較
            src_cols = _count_table_cols(src_t[0])
            trans_cols = _count_table_cols(trans_t[0])
            if src_cols != trans_cols:
                result.add_issue(Issue(
                    rel, None,
                    f"テーブル#{i+1}: 列数不一致 (src={src_cols}, trans={trans_cols})",
                ))
            else:
                result.passed += 1

    return result


def check_inline_code_preserved(
    lang: str,
    source_files: Dict[str, str],
    translated_files: Dict[str, str],
    **kw: Any,
) -> CheckResult:
    """バッククォート内コードが翻訳で保持されているか"""
    result = CheckResult("inline_code_preserved")

    for rel in translated_files:
        if rel not in source_files:
            continue

        src_codes = set(INLINE_CODE_RE.findall(source_files[rel]))
        trans_codes = set(INLINE_CODE_RE.findall(translated_files[rel]))

        result.total += 1
        missing = src_codes - trans_codes
        if missing:
            sample = sorted(missing)[:3]
            result.add_issue(Issue(
                rel, None,
                f"インラインコードが欠落: {', '.join(f'`{c}`' for c in sample)}",
                severity="WARN",
            ))
        else:
            result.passed += 1

    return result


def check_image_refs_preserved(
    lang: str,
    source_files: Dict[str, str],
    translated_files: Dict[str, str],
    **kw: Any,
) -> CheckResult:
    """画像参照パスが翻訳で保持されているか"""
    result = CheckResult("image_refs_preserved")

    for rel in translated_files:
        if rel not in source_files:
            continue

        src_refs = {path for _, path in IMAGE_REF_RE.findall(source_files[rel])}
        trans_refs = {path for _, path in IMAGE_REF_RE.findall(translated_files[rel])}

        result.total += 1
        missing = src_refs - trans_refs
        if missing:
            sample = sorted(missing)[:3]
            result.add_issue(Issue(
                rel, None,
                f"画像参照が欠落: {', '.join(sample)}",
            ))
        else:
            result.passed += 1

    return result


def check_askq_json_validity(
    lang: str,
    source_files: Dict[str, str],
    translated_files: Dict[str, str],
    **kw: Any,
) -> CheckResult:
    """AskQuestion JSON ブロックの構文・キー構造チェック"""
    result = CheckResult("askq_json_validity")

    for rel in translated_files:
        if rel not in source_files:
            continue

        src_blocks = _extract_json_blocks(source_files[rel])
        trans_blocks = _extract_json_blocks(translated_files[rel])

        for i, (src_b, trans_b) in enumerate(zip(src_blocks, trans_blocks)):
            result.total += 1

            # パース可能性
            try:
                src_data = json.loads(src_b)
            except json.JSONDecodeError:
                result.passed += 1
                continue

            try:
                trans_data = json.loads(trans_b)
            except json.JSONDecodeError:
                result.add_issue(Issue(
                    rel, None,
                    f"JSON ブロック#{i+1}: パースエラー",
                ))
                continue

            # キー構造の比較（トップレベル）
            if isinstance(src_data, dict) and isinstance(trans_data, dict):
                src_keys = set(src_data.keys())
                trans_keys = set(trans_data.keys())
                missing_keys = src_keys - trans_keys
                if missing_keys:
                    result.add_issue(Issue(
                        rel, None,
                        f"JSON ブロック#{i+1}: キー欠落 {missing_keys}",
                    ))
                    continue

            result.passed += 1

    return result


# ---------------------------------------------------------------------------
# Registry and runner
# ---------------------------------------------------------------------------

CHECK_REGISTRY: Dict[str, Callable[..., CheckResult]] = {
    "frontmatter_integrity": check_frontmatter_integrity,
    "key_coverage": check_key_coverage,
    "table_cell_count": check_table_cell_count,
    "inline_code_preserved": check_inline_code_preserved,
    "image_refs_preserved": check_image_refs_preserved,
    "askq_json_validity": check_askq_json_validity,
}


def run_checks(
    lang: str,
    *,
    check_names: List[str] | None = None,
    source_dir: Path | None = None,
    translated_dir: Path | None = None,
) -> List[CheckResult]:
    """指定言語の MD 品質チェックを実行。

    Returns:
        CheckResult のリスト
    """
    # ソースファイル: commands/ + skills/ (指定 or デフォルト)
    # 翻訳ファイル: dist/{lang}/ から
    trans_base = translated_dir or (DIST_DIR_ROOT / lang)
    translated_files = _load_md_files(trans_base)

    if source_dir:
        source_files = _load_md_files(source_dir)
    else:
        source_files: Dict[str, str] = {}
        for d in (COMMANDS_DIR, SKILLS_DIR):
            source_files.update(_load_md_files(d))

    checks_to_run = check_names or list(CHECK_REGISTRY.keys())
    results: List[CheckResult] = []

    for name in checks_to_run:
        fn = CHECK_REGISTRY.get(name)
        if fn is None:
            r = CheckResult(name)
            r.add_issue(Issue("", None, f"不明なチェック: {name}"))
            results.append(r)
            continue
        results.append(fn(
            lang=lang,
            source_files=source_files,
            translated_files=translated_files,
        ))

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_results(results: List[CheckResult], *, verbose: bool = False) -> int:
    """結果を表示して exit code を返す (0=pass, 1=fail)"""
    has_fail = False

    for r in results:
        icon = {"PASS": "\u2705", "WARN": "\u26a0\ufe0f ", "FAIL": "\u274c"}[r.status]
        print(f"  {icon} {r.name}: {r.status} ({r.passed}/{r.total})")
        if r.status == "FAIL":
            has_fail = True
        if (r.issues and verbose) or r.status == "FAIL":
            for issue in r.issues:
                print(f"     {issue}")

    return 1 if has_fail else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="QA checks for translated MD files"
    )
    parser.add_argument("--lang", nargs="+", required=True,
                        help="Target languages (e.g. en es)")
    parser.add_argument("--checks", default=None,
                        help="Comma-separated check names to run")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output results as JSON")
    parser.add_argument("--verbose", action="store_true",
                        help="Show all issues including warnings")
    args = parser.parse_args()

    check_names = args.checks.split(",") if args.checks else None
    exit_code = 0

    all_results: Dict[str, List[dict]] = {}

    for lang in args.lang:
        if not args.json_output:
            print(f"\n=== MD QA: {lang} ===")
        results = run_checks(lang, check_names=check_names)

        if args.json_output:
            all_results[lang] = [r.to_dict() for r in results]
        else:
            code = _print_results(results, verbose=args.verbose)
            if code != 0:
                exit_code = code

        # JSON モードでも exit code を正しく設定
        if any(r.status == "FAIL" for r in results):
            exit_code = 1

    if args.json_output:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
