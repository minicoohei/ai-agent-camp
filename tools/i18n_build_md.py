"""
i18n MD Build Tool

翻訳済みMDファイルを生成する。
- locales/md/ja.json (ソースキー) + locales/md/{lang}.json (翻訳) を読み込み
- ソースMDの該当箇所を翻訳テキストで置換
- dist/{lang}/ にディレクトリ構造を保持して出力

使い方:
  uv run python tools/i18n_build_md.py --lang en es          # EN/ES版を生成
  uv run python tools/i18n_build_md.py --lang en --verbose    # 詳細出力
  uv run python tools/i18n_build_md.py --lang en --clean      # 既存を削除して再生成
  uv run python tools/i18n_build_md.py --dry-run --lang en    # 統計のみ(書き込みなし)
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

_tools_dir = str(Path(__file__).resolve().parent)
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)

try:
    from i18n_common import ROOT_DIR, MD_LOCALES_DIR, DIST_DIR_ROOT, get_language_name
except ImportError:
    from tools.i18n_common import ROOT_DIR, MD_LOCALES_DIR, DIST_DIR_ROOT, get_language_name

try:
    from i18n_extract_md import (
        _State, _protect_inline_code, _restore_inline_code,
        _extract_askq_keys,
        INLINE_CODE_RE, TABLE_SEP_RE, IMAGE_RE,
        TRANSLATABLE_FM_FIELDS, ASKQ_TRANSLATABLE_KEYS, _is_askq_json,
    )
except ImportError:
    from tools.i18n_extract_md import (
        _State, _protect_inline_code, _restore_inline_code,
        _extract_askq_keys,
        INLINE_CODE_RE, TABLE_SEP_RE, IMAGE_RE,
        TRANSLATABLE_FM_FIELDS, ASKQ_TRANSLATABLE_KEYS, _is_askq_json,
    )

# URL内の /ja/ を /{lang}/ に書き換える正規表現
JA_URL_RE = re.compile(r"(/ja/)")


# =============================================================================
# ロード
# =============================================================================

def load_locale(lang: str) -> Dict[str, Dict[str, str]]:
    """locales/md/{lang}.json を読み込む"""
    path = MD_LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        print(f"[ERROR] {path} が見つかりません。", file=sys.stderr)
        print(f"  まず: uv run python tools/i18n_extract_md.py --translate --lang {lang}", file=sys.stderr)
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] {path} の JSON パースに失敗: {e}", file=sys.stderr)
        return {}


# =============================================================================
# AskQuestion JSON 置換
# =============================================================================

def _replace_askq_json(json_text: str, translations: Dict[str, str], prefix: str) -> Tuple[str, int]:
    """AskQuestion JSON 内の翻訳対象フィールドを置換して返す。

    translations はフラットキー (prefix.title, prefix.questions.0.prompt, ...) → 翻訳テキスト。

    Returns:
        (replaced_json_text, applied_count)
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return json_text, 0

    if not isinstance(data, dict):
        return json_text, 0

    changed = 0
    _SCHEMA_B_TEXT_FIELDS = ("question", "description", "title", "hint", "helpText", "context")

    # Schema B
    if data.get("type") == "AskQuestion" or ("question" in data and "options" in data and "questions" not in data):
        for field in _SCHEMA_B_TEXT_FIELDS:
            key = f"{prefix}.{field}"
            if key in translations and field in data:
                data[field] = translations[key]
                changed += 1
        for oi, opt in enumerate(data.get("options", [])):
            if not isinstance(opt, dict):
                continue
            for opt_field in ("label", "description"):
                key = f"{prefix}.options.{oi}.{opt_field}"
                if key in translations and opt_field in opt:
                    opt[opt_field] = translations[key]
                    changed += 1
        if changed == 0:
            return json_text, 0
        return json.dumps(data, ensure_ascii=False, indent=2), changed

    # Schema A
    title_key = f"{prefix}.title"
    if title_key in translations and "title" in data:
        data["title"] = translations[title_key]
        changed += 1

    for qi, q in enumerate(data.get("questions", [])):
        if not isinstance(q, dict):
            continue
        prompt_key = f"{prefix}.questions.{qi}.prompt"
        if prompt_key in translations and "prompt" in q:
            q["prompt"] = translations[prompt_key]
            changed += 1
        for oi, opt in enumerate(q.get("options", [])):
            if not isinstance(opt, dict):
                continue
            for opt_field in ("label", "description"):
                key = f"{prefix}.questions.{qi}.options.{oi}.{opt_field}"
                if key in translations and opt_field in opt:
                    opt[opt_field] = translations[key]
                    changed += 1

    if changed == 0:
        return json_text, 0
    return json.dumps(data, ensure_ascii=False, indent=2), changed


# =============================================================================
# YAML frontmatter 置換
# =============================================================================

def _replace_frontmatter(fm_lines: List[str], translations: Dict[str, str]) -> List[str]:
    """frontmatter の翻訳対象フィールドを置換。

    簡易YAML書き換え: フィールド名を検出して値を差し替え。
    複雑なYAML構造は想定しない(リストは `- item` 形式のみ)。
    """
    text = "\n".join(fm_lines)
    try:
        data = yaml.safe_load(text)
    except Exception:
        return fm_lines

    if not isinstance(data, dict):
        return fm_lines

    result_lines = list(fm_lines)

    for field in TRANSLATABLE_FM_FIELDS:
        if field not in data:
            continue

        value = data[field]
        if isinstance(value, str):
            key = f"frontmatter.{field}"
            if key not in translations:
                continue
            trans = translations[key]
            # 行を検索して置換
            for li, line in enumerate(result_lines):
                if line.startswith(f"{field}:"):
                    # json.dumps で YAML 互換の安全なクォート文字列を生成
                    result_lines[li] = f'{field}: {json.dumps(trans, ensure_ascii=False)}'
                    break

        elif isinstance(value, list):
            # リスト: [item1, item2] 形式 or - item 形式
            for li, line in enumerate(result_lines):
                if line.startswith(f"{field}:"):
                    # インライン配列形式 ["item1", "item2"]
                    if "[" in line:
                        items = []
                        for idx, item in enumerate(value):
                            key = f"frontmatter.{field}.{idx}"
                            trans = translations.get(key, item)
                            items.append(json.dumps(trans, ensure_ascii=False))
                        result_lines[li] = f'{field}: [{", ".join(items)}]'
                    else:
                        # ブロック形式 - 後続行を書き換え
                        for idx, item in enumerate(value):
                            key = f"frontmatter.{field}.{idx}"
                            trans = translations.get(key, item)
                            target_li = li + 1 + idx
                            if target_li < len(result_lines):
                                indent = re.match(r"^(\s*)-\s+", result_lines[target_li])
                                if indent:
                                    pfx = indent.group(1)
                                    result_lines[target_li] = f'{pfx}- {json.dumps(trans, ensure_ascii=False)}'
                    break

    return result_lines


# =============================================================================
# MD ビルド (ステートマシン置換)
# =============================================================================

def apply_translations_to_md(
    content: str,
    translations: Dict[str, str],
    lang: str,
    verbose: bool = False,
) -> Tuple[str, int, int]:
    """ソース MD に翻訳を適用して返す。

    抽出時と同じステートマシンで走査し、キーカウンタで翻訳を対応づける。

    Returns:
        (translated_md, applied_count, missing_count)
    """
    lines = content.split("\n")
    state = _State.INIT
    fm_lines: List[str] = []
    fm_start = -1
    fm_end = -1
    code_buffer: List[str] = []
    code_start = -1
    askq_counter = 0

    counters: Dict[str, int] = {}
    applied = 0
    missing = 0

    output_lines = list(lines)
    # AskQ JSON 置換で行数が変わった場合のオフセット
    line_offset = 0

    # AskQuestion 検出用
    prev_line_is_askq_hint = False

    def _next_key(tag: str) -> str:
        count = counters.get(tag, 0)
        counters[tag] = count + 1
        return f"body.{tag}.{count}"

    def _should_skip_text(text: str) -> bool:
        """抽出時にスキップされるテキストか判定"""
        text = text.strip()
        if not text or len(text) < 2:
            return True
        if re.match(r'^[\d\s\-\.\,\;\:\!\?\#\@\%\&\*\(\)\[\]\{\}\/\\]+$', text):
            return True
        return False

    def _translate_text(key: str, original: str, line_idx: int) -> Optional[str]:
        """キーに対応する翻訳テキストを取得。インラインコード復元込み。"""
        nonlocal applied, missing
        if key not in translations:
            missing += 1
            return None
        trans = translations[key]
        # プレースホルダーを復元: 翻訳テキスト内の {{code_N}} を元のコードに戻す
        _, codes = _protect_inline_code(original)
        if codes:
            trans = _restore_inline_code(trans, codes)
        applied += 1
        return trans

    def _rewrite_urls(text: str) -> str:
        """URL 内の /ja/ を /{lang}/ に書き換え"""
        return JA_URL_RE.sub(lambda m: f"/{lang}/", text)

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- INIT → FRONTMATTER ---
        if state == _State.INIT:
            if line.strip() == "---":
                state = _State.FRONTMATTER
                fm_start = i + 1
                i += 1
                continue
            state = _State.BODY
            continue

        # --- FRONTMATTER ---
        elif state == _State.FRONTMATTER:
            if line.strip() == "---":
                fm_end = i
                # frontmatter 置換
                replaced_fm = _replace_frontmatter(fm_lines, translations)
                for fi, fm_line in enumerate(replaced_fm):
                    output_lines[fm_start + line_offset + fi] = fm_line
                # 適用/欠損カウント
                try:
                    fm_data = yaml.safe_load("\n".join(fm_lines))
                except Exception:
                    fm_data = {}
                if isinstance(fm_data, dict):
                    for field in TRANSLATABLE_FM_FIELDS:
                        if field not in fm_data:
                            continue
                        val = fm_data[field]
                        if isinstance(val, str) and val.strip():
                            key = f"frontmatter.{field}"
                            if key in translations:
                                applied += 1
                            else:
                                missing += 1
                        elif isinstance(val, list):
                            for idx, item in enumerate(val):
                                if isinstance(item, str) and item.strip():
                                    key = f"frontmatter.{field}.{idx}"
                                    if key in translations:
                                        applied += 1
                                    else:
                                        missing += 1
                state = _State.BODY
                i += 1
                continue
            fm_lines.append(line)

        # --- CODE_BLOCK ---
        elif state == _State.CODE_BLOCK:
            if line.strip().startswith("```"):
                state = _State.BODY
                prev_line_is_askq_hint = False

        # --- ASKQ_JSON ---
        elif state == _State.ASKQ_JSON:
            if line.strip().startswith("```"):
                json_text = "\n".join(code_buffer)
                prefix = f"body.askq.{askq_counter}"
                askq_counter += 1

                # AskQ キー総数を算出して missing を計上
                askq_total_keys = len(_extract_askq_keys(json_text, prefix))
                replaced_json, askq_applied = _replace_askq_json(json_text, translations, prefix)
                if askq_applied > 0:
                    # コードバッファ行を置換
                    replaced_lines = replaced_json.split("\n")
                    oc_start = code_start + line_offset
                    oc_end = i + line_offset
                    output_lines[oc_start:oc_end] = replaced_lines
                    line_offset += len(replaced_lines) - (i - code_start)
                    applied += askq_applied
                missing += max(0, askq_total_keys - askq_applied)

                code_buffer = []
                state = _State.BODY
                prev_line_is_askq_hint = False
            else:
                code_buffer.append(line)

        # --- BODY ---
        elif state == _State.BODY:
            stripped = line.strip()

            # コードフェンス開始
            if stripped.startswith("```"):
                lang_hint = stripped[3:].strip().lower()
                if lang_hint == "json":
                    if prev_line_is_askq_hint:
                        # ヒントがあっても実際の JSON 構造を検証
                        peek_lines = []
                        j = i + 1
                        while j < len(lines) and not lines[j].strip().startswith("```"):
                            peek_lines.append(lines[j])
                            j += 1
                        peek_text = "\n".join(peek_lines)
                        if _is_askq_json(peek_text):
                            state = _State.ASKQ_JSON
                            code_buffer = []
                            code_start = i + 1
                            i += 1
                            continue
                    # 先読みで AskQuestion 判定
                    peek_lines = []
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("```"):
                        peek_lines.append(lines[j])
                        j += 1
                    peek_text = "\n".join(peek_lines)
                    if _is_askq_json(peek_text):
                        state = _State.ASKQ_JSON
                        code_buffer = []
                        code_start = i + 1
                        i += 1
                        continue
                state = _State.CODE_BLOCK
                i += 1
                continue

            # AskQuestion ヒント検出
            if stripped:
                prev_line_is_askq_hint = "askquestion" in stripped.lower()

            # 水平線
            if re.match(r"^-{3,}\s*$", stripped) or re.match(r"^\*{3,}\s*$", stripped):
                i += 1
                continue

            # 空行
            if not stripped:
                i += 1
                continue

            # 見出し
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                if not _should_skip_text(text):
                    key = _next_key(f"h{level}")
                    trans = _translate_text(key, text, i)
                    if trans is not None:
                        trans = _rewrite_urls(trans)
                        # 元の行のインデント保持
                        leading = line[:len(line) - len(line.lstrip())]
                        output_lines[i + line_offset] = f"{leading}{'#' * level} {trans}"
                i += 1
                continue

            # テーブルセパレータ
            if TABLE_SEP_RE.match(stripped):
                i += 1
                continue

            # テーブル行
            if stripped.startswith("|") and stripped.endswith("|"):
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                table_idx = counters.get("_table", 0)
                row_idx = counters.get(f"_table_{table_idx}_row", 0)

                new_cells = []
                for ci, cell in enumerate(cells):
                    if cell and len(cell) >= 2:
                        key = f"body.table.{table_idx}.r{row_idx}.c{ci}"
                        if key in translations:
                            _, codes = _protect_inline_code(cell)
                            trans = translations[key]
                            if codes:
                                trans = _restore_inline_code(trans, codes)
                            trans = _rewrite_urls(trans)
                            new_cells.append(f" {trans} ")
                            applied += 1
                        else:
                            new_cells.append(f" {cell} ")
                            # 抽出側と同じ基準 (cell and len(cell) >= 2) で missing 計上
                            missing += 1
                    else:
                        new_cells.append(f" {cell} ")

                output_lines[i + line_offset] = "|" + "|".join(new_cells) + "|"

                counters[f"_table_{table_idx}_row"] = row_idx + 1
                next_i = i + 1
                if next_i < len(lines):
                    next_stripped = lines[next_i].strip()
                    if not (next_stripped.startswith("|") and next_stripped.endswith("|")):
                        counters["_table"] = table_idx + 1
                else:
                    counters["_table"] = table_idx + 1

                i += 1
                continue

            # ブロック引用
            if stripped.startswith(">"):
                text = stripped.lstrip(">").strip()
                if text and not _should_skip_text(text):
                    key = _next_key("blockquote")
                    trans = _translate_text(key, text, i)
                    if trans is not None:
                        trans = _rewrite_urls(trans)
                        leading = line[:len(line) - len(line.lstrip())]
                        output_lines[i + line_offset] = f"{leading}> {trans}"
                i += 1
                continue

            # リスト項目
            list_match = re.match(r"^(\s*[-*+]|\s*\d+\.)\s+(.*)", stripped)
            if list_match:
                marker = list_match.group(1)
                text = list_match.group(2).strip()
                checkbox_prefix = ""
                checkbox_match = re.match(r"^\[[ xX]\]\s*(.*)", text)
                if checkbox_match:
                    checkbox_prefix = text[:text.index("]") + 1] + " "
                    text = checkbox_match.group(1).strip()
                if text and not _should_skip_text(text):
                    key = _next_key("li")
                    trans = _translate_text(key, text, i)
                    if trans is not None:
                        trans = _rewrite_urls(trans)
                        leading = line[:len(line) - len(line.lstrip())]
                        output_lines[i + line_offset] = f"{leading}{marker} {checkbox_prefix}{trans}"
                i += 1
                continue

            # 画像 alt
            img_match = IMAGE_RE.search(stripped)
            if img_match and img_match.group(1):
                alt_text = img_match.group(1).strip()
                if alt_text and len(alt_text) >= 2:
                    key = _next_key("img_alt")
                    if key in translations:
                        trans = _rewrite_urls(translations[key])
                        # alt テキストだけ置換
                        oi = i + line_offset
                        new_line = output_lines[oi].replace(
                            f"![{img_match.group(1)}]",
                            f"![{trans}]",
                            1,
                        )
                        output_lines[oi] = new_line
                        applied += 1
                    else:
                        missing += 1
                remaining = IMAGE_RE.sub("", stripped).strip()
                if not remaining:
                    i += 1
                    continue

            # 段落
            if not _should_skip_text(stripped):
                key = _next_key("p")
                trans = _translate_text(key, stripped, i)
                if trans is not None:
                    trans = _rewrite_urls(trans)
                    leading = line[:len(line) - len(line.lstrip())]
                    output_lines[i + line_offset] = f"{leading}{trans}"

        i += 1

    # 全体の URL 書き換え (frontmatter 内や見逃し箇所)
    result = "\n".join(output_lines)
    result = JA_URL_RE.sub(lambda m: f"/{lang}/", result)
    return result, applied, missing


# =============================================================================
# ファイル出力
# =============================================================================

def _resolve_output_path(file_key: str, lang: str) -> Path:
    """file_key (相対パス) から dist/{lang}/ 配下の出力パスを算出"""
    return DIST_DIR_ROOT / lang / file_key


def build_lang(
    lang: str,
    ja_data: Dict[str, Dict[str, str]],
    lang_data: Dict[str, Dict[str, str]],
    clean: bool = False,
    verbose: bool = False,
    dry_run: bool = False,
) -> Tuple[int, int, int, int]:
    """1言語分のビルドを実行。

    Returns: (files_built, total_applied, total_missing, skipped)
    """
    lang_name = get_language_name(lang)
    lang_dist = DIST_DIR_ROOT / lang
    print(f"\n=== Building {lang_name} ({lang}) ===")

    if clean and lang_dist.exists() and not dry_run:
        shutil.rmtree(lang_dist)
        print(f"  Cleaned: {lang_dist}")

    files_built = 0
    total_applied = 0
    total_missing = 0
    skipped = 0

    for file_key, ja_keys in ja_data.items():
        # 翻訳データ取得
        file_translations = lang_data.get(file_key, {})
        if not file_translations:
            skipped += 1
            if verbose:
                print(f"  [SKIP] {file_key} — no translations")
            continue

        # ソース MD 読み込み
        source_path = ROOT_DIR / file_key
        if not source_path.exists():
            skipped += 1
            if verbose:
                print(f"  [SKIP] {file_key} — source not found")
            continue

        content = source_path.read_text(encoding="utf-8")

        # 翻訳適用
        translated, applied_count, missing_count = apply_translations_to_md(
            content, file_translations, lang, verbose=verbose,
        )

        total_applied += applied_count
        total_missing += missing_count

        if dry_run:
            files_built += 1
            if verbose:
                print(f"  [DRY] {file_key} — {applied_count} applied, {missing_count} missing")
            continue

        # 出力
        output_path = _resolve_output_path(file_key, lang)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(translated, encoding="utf-8")
        files_built += 1

        if verbose:
            print(f"  [OK] {file_key} — {applied_count} applied, {missing_count} missing")

    return files_built, total_applied, total_missing, skipped


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Build translated MD files from locale JSON")
    parser.add_argument("--lang", nargs="+", required=True, help="Target languages (e.g. en es)")
    parser.add_argument("--clean", action="store_true", help="Remove existing dist/{lang}/ before build")
    parser.add_argument("--verbose", action="store_true", help="Show per-file details")
    parser.add_argument("--dry-run", action="store_true", help="Show stats without writing files")
    args = parser.parse_args()

    # ja.json ロード
    ja_data = load_locale("ja")
    if not ja_data:
        sys.exit(1)

    for lang in args.lang:
        lang_data = load_locale(lang)
        if not lang_data:
            print(f"[WARN] Skipping {lang} — no locale file", file=sys.stderr)
            continue

        files_built, total_applied, total_missing, skipped = build_lang(
            lang, ja_data, lang_data,
            clean=args.clean,
            verbose=args.verbose,
            dry_run=args.dry_run,
        )

        mode = "[DRY RUN] " if args.dry_run else ""
        print(f"\n{mode}--- {get_language_name(lang)} ({lang}) Summary ---")
        print(f"  Files built: {files_built}")
        print(f"  Keys applied: {total_applied}")
        print(f"  Keys missing: {total_missing}")
        print(f"  Files skipped: {skipped}")


if __name__ == "__main__":
    main()
