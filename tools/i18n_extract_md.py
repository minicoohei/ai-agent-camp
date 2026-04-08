"""
i18n MD Text Extraction & Translation Tool

Markdownファイル（commands, skills）からテキストを抽出し、翻訳用JSONを生成する。
- .cursor/commands/, .claude/commands/ のレッスンコマンド
- skills/*/SKILL.md のスキル定義

使い方:
  uv run python tools/i18n_extract_md.py                         # ja.json を生成
  uv run python tools/i18n_extract_md.py --dry-run                # 統計のみ表示
  uv run python tools/i18n_extract_md.py --check                  # ja.json と実ファイルの差分検出
  uv run python tools/i18n_extract_md.py --translate               # ja/en/es.json を生成
  uv run python tools/i18n_extract_md.py --translate --lang ko     # ja/ko.json を生成
  uv run python tools/i18n_extract_md.py --scope commands          # commands のみ
  uv run python tools/i18n_extract_md.py --scope skills            # skills のみ
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from i18n_common import (
    ROOT_DIR,
    MD_LOCALES_DIR,
    LANGUAGE_NAMES,
    find_command_md_files,
    find_skill_md_files,
    require_gemini_client,
    get_language_name,
)

# 翻訳時に保持すべき技術用語
TECHNICAL_TERMS = [
    "Claude Code", "Claude", "Cursor", "BigQuery", "Google Cloud",
    "GitHub Actions", "GitHub", "Slack", "Notion", "Google Apps Script",
    "GAS", "API", "LLM", "AI", "PPTX", "PDF", "CSV", "JSON", "HTML",
    "CSS", "JavaScript", "Python", "Node.js", "Git", "Docker",
    "PlantUML", "UML", "Gemini", "Tailwind", "Bootstrap",
    "Vercel", "Playwright", "E2E", "EDA", "PRD", "WBS",
    "Nano Banana", "NotebookLM", "aiagent-base",
    "marimo", "gogcli", "clasp", "npm", "pip", "uv",
    "Codex", "Remotion", "MCP", "Supabase",
]

DEFAULT_TRANSLATE_LANGS = ["en", "es"]

# YAML frontmatter 内で翻訳対象とするフィールド
TRANSLATABLE_FM_FIELDS = {"description", "duration", "prerequisites"}

# AskQuestion JSON 内で翻訳対象とするキー
ASKQ_TRANSLATABLE_KEYS = {"title", "label", "prompt", "description"}

# インラインコードの正規表現
INLINE_CODE_RE = re.compile(r"`([^`]+)`")

# 画像の正規表現
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")

# テーブルセパレータ行の正規表現
TABLE_SEP_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")


# =============================================================================
# ステートマシンベースの MD パーサー
# =============================================================================

class _State:
    INIT = "init"
    FRONTMATTER = "frontmatter"
    BODY = "body"
    CODE_BLOCK = "code_block"
    ASKQ_JSON = "askq_json"


def _protect_inline_code(text: str) -> Tuple[str, Dict[str, str]]:
    """インラインコードを {{code_N}} プレースホルダーに置換。

    Returns:
        (置換後テキスト, {placeholder: original_code})
    """
    codes: Dict[str, str] = {}
    counter = [0]

    def replacer(m):
        key = f"{{{{code_{counter[0]}}}}}"
        codes[key] = m.group(0)
        counter[0] += 1
        return key

    protected = INLINE_CODE_RE.sub(replacer, text)
    return protected, codes


def _restore_inline_code(text: str, codes: Dict[str, str]) -> str:
    """プレースホルダーを元のインラインコードに復元"""
    result = text
    for placeholder, original in codes.items():
        result = result.replace(placeholder, original)
    return result


def _extract_askq_keys(json_text: str, prefix: str) -> Dict[str, str]:
    """AskQuestion JSON から翻訳対象キーを抽出。

    2つのスキーマをサポート:
    A) {"title":..., "questions":[{"prompt":..., "options":[{"label":...}]}]}
    B) {"type":"AskQuestion", "question":..., "description":..., "options":[{"label":...}]}
    """
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return {}

    keys: Dict[str, str] = {}

    if not isinstance(data, dict):
        return keys

    # --- Schema B: {"type":"AskQuestion", "question":..., "options":[...]} ---
    # 学習者に表示される全テキストフィールドを抽出
    _SCHEMA_B_TEXT_FIELDS = ("question", "description", "title", "hint", "helpText", "context")
    if data.get("type") == "AskQuestion" or ("question" in data and "options" in data and "questions" not in data):
        for field in _SCHEMA_B_TEXT_FIELDS:
            if field in data and isinstance(data[field], str):
                keys[f"{prefix}.{field}"] = data[field]
        for oi, opt in enumerate(data.get("options", [])):
            if not isinstance(opt, dict):
                continue
            for opt_field in ("label", "description"):
                if opt_field in opt and isinstance(opt[opt_field], str):
                    keys[f"{prefix}.options.{oi}.{opt_field}"] = opt[opt_field]
        return keys

    # --- Schema A: {"title":..., "questions":[{"prompt":..., "options":[...]}]} ---
    if "title" in data and isinstance(data["title"], str):
        keys[f"{prefix}.title"] = data["title"]

    questions = data.get("questions", [])
    if isinstance(questions, list):
        for qi, q in enumerate(questions):
            if not isinstance(q, dict):
                continue
            if "prompt" in q and isinstance(q["prompt"], str):
                keys[f"{prefix}.questions.{qi}.prompt"] = q["prompt"]
            for oi, opt in enumerate(q.get("options", [])):
                if isinstance(opt, dict) and "label" in opt:
                    keys[f"{prefix}.questions.{qi}.options.{oi}.label"] = opt["label"]
                if isinstance(opt, dict) and "description" in opt:
                    keys[f"{prefix}.questions.{qi}.options.{oi}.description"] = opt["description"]

    return keys


def _is_askq_json(text: str) -> bool:
    """JSON テキストが AskQuestion ブロックかどうかを判定"""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    if not isinstance(data, dict):
        return False
    # Schema A: {"title":..., "questions":[...]}
    if "questions" in data and isinstance(data.get("questions"), list):
        return True
    # Schema B: {"type":"AskQuestion", ...} or {"question":..., "options":[...]}
    if data.get("type") == "AskQuestion":
        return True
    if "question" in data and "options" in data:
        return True
    return False


def _parse_frontmatter_value(value, key_prefix: str) -> Dict[str, str]:
    """frontmatter のフィールド値をキー付き辞書に変換"""
    keys: Dict[str, str] = {}
    if isinstance(value, str) and value.strip():
        keys[key_prefix] = value.strip()
    elif isinstance(value, list):
        for i, item in enumerate(value):
            if isinstance(item, str) and item.strip():
                keys[f"{key_prefix}.{i}"] = item.strip()
    return keys


def _parse_yaml_frontmatter(lines: List[str]) -> Dict[str, str]:
    """簡易 YAML frontmatter パーサー（翻訳対象フィールドのみ）"""
    import yaml
    text = "\n".join(lines)
    try:
        data = yaml.safe_load(text)
    except Exception:
        return {}

    if not isinstance(data, dict):
        return {}

    keys: Dict[str, str] = {}
    for field in TRANSLATABLE_FM_FIELDS:
        if field in data:
            keys.update(_parse_frontmatter_value(data[field], f"frontmatter.{field}"))
    return keys


def extract_texts_from_md(content: str) -> Dict[str, str]:
    """Markdown コンテンツからテキストを抽出してキー付き辞書を返す"""
    lines = content.split("\n")
    state = _State.INIT
    fm_lines: List[str] = []
    code_buffer: List[str] = []
    askq_counter = 0

    keys: Dict[str, str] = {}
    counters: Dict[str, int] = {}

    # AskQuestion の検出用: 直近の非空行に "AskQuestion" を含んでいたか
    prev_line_is_askq_hint = False

    def _next_key(tag: str) -> str:
        count = counters.get(tag, 0)
        counters[tag] = count + 1
        return f"body.{tag}.{count}"

    def _add_text(tag: str, text: str) -> None:
        """テキストをキーに追加（インラインコード保護済み）"""
        text = text.strip()
        if not text or len(text) < 2:
            return
        # 純粋な記号/数字のみはスキップ
        if re.match(r'^[\d\s\-\.\,\;\:\!\?\#\@\%\&\*\(\)\[\]\{\}\/\\]+$', text):
            return
        protected, _ = _protect_inline_code(text)
        keys[_next_key(tag)] = protected

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- INIT → FRONTMATTER ---
        if state == _State.INIT:
            if line.strip() == "---":
                state = _State.FRONTMATTER
                i += 1
                continue
            # frontmatter なし → BODY へ
            state = _State.BODY
            continue  # 同じ行を BODY で処理

        # --- FRONTMATTER ---
        elif state == _State.FRONTMATTER:
            if line.strip() == "---":
                keys.update(_parse_yaml_frontmatter(fm_lines))
                state = _State.BODY
                i += 1
                continue
            fm_lines.append(line)

        # --- CODE_BLOCK ---
        elif state == _State.CODE_BLOCK:
            if line.strip().startswith("```"):
                state = _State.BODY
                prev_line_is_askq_hint = False
            # コードブロック内は何もしない

        # --- ASKQ_JSON ---
        elif state == _State.ASKQ_JSON:
            if line.strip().startswith("```"):
                json_text = "\n".join(code_buffer)
                prefix = f"body.askq.{askq_counter}"
                askq_counter += 1
                askq_keys = _extract_askq_keys(json_text, prefix)
                keys.update(askq_keys)
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
                    # ヒント検出済み → AskQuestion JSON として処理
                    if prev_line_is_askq_hint:
                        state = _State.ASKQ_JSON
                        code_buffer = []
                        i += 1
                        continue
                    # ヒントなしでも JSON 内容から AskQuestion を判定
                    # 先読みして内容に AskQuestion/questions/options があるか確認
                    peek_lines = []
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("```"):
                        peek_lines.append(lines[j])
                        j += 1
                    peek_text = "\n".join(peek_lines)
                    if _is_askq_json(peek_text):
                        state = _State.ASKQ_JSON
                        code_buffer = []
                        i += 1
                        continue
                state = _State.CODE_BLOCK
                i += 1
                continue

            # AskQuestion ヒント検出（空行ではリセットしない）
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
                _add_text(f"h{level}", text)
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

                for ci, cell in enumerate(cells):
                    if cell and len(cell) >= 2:
                        protected, _ = _protect_inline_code(cell)
                        keys[f"body.table.{table_idx}.r{row_idx}.c{ci}"] = protected

                counters[f"_table_{table_idx}_row"] = row_idx + 1
                # テーブル終了判定: 次の行がテーブルでなければカウントアップ
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
                if text:
                    _add_text("blockquote", text)
                i += 1
                continue

            # リスト項目
            list_match = re.match(r"^(\s*[-*+]|\s*\d+\.)\s+(.*)", stripped)
            if list_match:
                text = list_match.group(2).strip()
                # チェックボックス保持
                checkbox_match = re.match(r"^\[[ xX]\]\s*(.*)", text)
                if checkbox_match:
                    text = checkbox_match.group(1).strip()
                if text:
                    _add_text("li", text)
                i += 1
                continue

            # 画像の alt テキスト
            img_match = IMAGE_RE.search(stripped)
            if img_match and img_match.group(1):
                alt_text = img_match.group(1).strip()
                if alt_text and len(alt_text) >= 2:
                    keys[_next_key("img_alt")] = alt_text
                # 画像のみの行なら段落扱いしない
                remaining = IMAGE_RE.sub("", stripped).strip()
                if not remaining:
                    i += 1
                    continue

            # 段落テキスト
            _add_text("p", stripped)

        i += 1

    return keys


# =============================================================================
# ファイル列挙・一括抽出
# =============================================================================

def _relative_path(filepath: Path) -> str:
    """プロジェクトルートからの相対パスを文字列で返す"""
    try:
        return str(filepath.relative_to(ROOT_DIR))
    except ValueError:
        return str(filepath)


def extract_all(
    files: List[Path],
) -> Dict[str, Dict[str, str]]:
    """全 MD ファイルからテキストを抽出"""
    data: Dict[str, Dict[str, str]] = {}
    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [WARN] Failed to read {filepath}: {e}", file=sys.stderr)
            continue
        keys = extract_texts_from_md(content)
        if keys:
            rel = _relative_path(filepath)
            data[rel] = keys
    return data


# =============================================================================
# 翻訳
# =============================================================================

def _build_md_translation_prompt(
    texts: Dict[str, str], target_lang: str, lang_name: str
) -> str:
    """MD テキスト翻訳用プロンプト"""
    terms_list = ", ".join(TECHNICAL_TERMS[:30])
    return f"""You are a professional translator. Translate the following JSON values from Japanese to {lang_name}.

RULES:
1. Translate ONLY the values, keep the keys exactly as they are.
2. DO NOT translate technical terms: {terms_list}, and similar tool/product names.
3. Preserve {{{{code_N}}}} placeholders exactly as-is (e.g. {{{{code_0}}}}, {{{{code_1}}}}). These are inline code references.
4. Preserve Markdown formatting: **, *, #, -, |, >, [ ], numbering.
5. Do NOT translate file paths, command names starting with /, or URLs.
6. Return ONLY valid JSON, no markdown code fences, no explanation.

Input JSON:
{json.dumps(texts, ensure_ascii=False, indent=2)}

Output the translated JSON:"""


def translate_batch(
    client,
    texts: Dict[str, str],
    target_lang: str,
    model: str,
) -> Dict[str, str]:
    """テキストのバッチを翻訳"""
    lang_name = get_language_name(target_lang)
    prompt = _build_md_translation_prompt(texts, target_lang, lang_name)

    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
        )
        response_text = response.text.strip()

        if response_text.startswith("```"):
            resp_lines = response_text.split("\n")
            if resp_lines[0].startswith("```"):
                resp_lines = resp_lines[1:]
            if resp_lines and resp_lines[-1].strip() == "```":
                resp_lines = resp_lines[:-1]
            response_text = "\n".join(resp_lines)

        return json.loads(response_text)
    except (json.JSONDecodeError, Exception) as e:
        print(f"  [WARN] Batch translation failed: {e}", file=sys.stderr)
        return texts


def translate_file_texts(
    client,
    texts: Dict[str, str],
    target_lang: str,
    model: str,
    batch_size: int = 50,
) -> Dict[str, str]:
    """1ファイル分のテキストをバッチに分割して翻訳"""
    items = list(texts.keys())
    translated = {}

    for i in range(0, len(items), batch_size):
        batch_keys = items[i : i + batch_size]
        batch = {k: texts[k] for k in batch_keys}
        result = translate_batch(client, batch, target_lang, model)
        translated.update(result)

        if i + batch_size < len(items):
            time.sleep(1)

    return translated


def translate_all(
    ja_data: Dict[str, Dict[str, str]],
    target_langs: List[str],
    model: str,
    batch_size: int = 50,
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """全ファイル・全言語を翻訳"""
    client = require_gemini_client()
    results: Dict[str, Dict[str, Dict[str, str]]] = {}
    total_files = len(ja_data)

    for lang in target_langs:
        lang_name = get_language_name(lang)
        print(f"\n--- Translating to {lang_name} ({lang}) ---")
        results[lang] = {}

        for idx, (file_path, texts) in enumerate(ja_data.items(), 1):
            print(f"  [{idx}/{total_files}] {file_path} ({len(texts)} keys)")
            translated = translate_file_texts(client, texts, lang, model, batch_size=batch_size)
            results[lang][file_path] = translated

            if idx < total_files:
                time.sleep(0.5)

    return results


# =============================================================================
# 統計・チェック
# =============================================================================

def print_stats(data: Dict[str, Dict[str, str]]) -> None:
    """抽出統計を表示"""
    total_keys = sum(len(v) for v in data.values())
    print(f"\n=== MD i18n Extraction Stats ===")
    print(f"Files: {len(data)}")
    print(f"Total keys: {total_keys}")

    # カテゴリ別集計
    categories = {"frontmatter": 0, "heading": 0, "paragraph": 0,
                  "table": 0, "list": 0, "blockquote": 0, "askq": 0, "other": 0}
    for file_keys in data.values():
        for key in file_keys:
            if key.startswith("frontmatter."):
                categories["frontmatter"] += 1
            elif re.match(r"body\.h\d\.", key):
                categories["heading"] += 1
            elif key.startswith("body.p."):
                categories["paragraph"] += 1
            elif key.startswith("body.table."):
                categories["table"] += 1
            elif key.startswith("body.li."):
                categories["list"] += 1
            elif key.startswith("body.blockquote."):
                categories["blockquote"] += 1
            elif key.startswith("body.askq."):
                categories["askq"] += 1
            else:
                categories["other"] += 1

    for cat, count in categories.items():
        if count > 0:
            print(f"  {cat}: {count}")


def _same_scope(existing_key: str, scoped_data: Dict[str, Dict[str, str]]) -> bool:
    """既存キーがスコープ内のファイルと同じパス接頭辞を持つか判定"""
    if not scoped_data:
        return False
    # scoped_data のパス接頭辞を収集（例: ".cursor/commands", "skills"）
    prefixes = set()
    for k in scoped_data:
        parts = k.split("/")
        if len(parts) >= 2:
            prefixes.add("/".join(parts[:2]))
        else:
            prefixes.add(parts[0])
    # existing_key が同じ接頭辞を持つか
    for prefix in prefixes:
        if existing_key.startswith(prefix):
            return True
    return False


def check_drift(data: Dict[str, Dict[str, str]], scoped: bool = False) -> int:
    """ja.json と実ファイルの差分を検出。差分があれば非ゼロを返す。

    scoped=True の場合、data に含まれるファイルのみ比較（他スコープは無視）。
    """
    ja_path = MD_LOCALES_DIR / "ja.json"
    if not ja_path.exists():
        print(f"[ERROR] {ja_path} が存在しません。まず抽出を実行してください。")
        return 1

    existing = json.loads(ja_path.read_text(encoding="utf-8"))

    # スコープモード: data に含まれるファイルだけを比較対象にする
    if scoped:
        compare_files = set(data.keys())
    else:
        compare_files = set(data.keys()) | set(existing.keys())

    added_files = set(data.keys()) - set(existing.keys())
    if scoped:
        # スコープ内のファイルだけで削除検出（スコープ外は無視）
        scoped_existing = {k for k in existing if k in data or _same_scope(k, data)}
        removed_files = scoped_existing - set(data.keys())
    else:
        removed_files = set(existing.keys()) - set(data.keys())
    changed_files = []

    for file_key in set(data.keys()) & set(existing.keys()):
        new_keys = set(data[file_key].keys())
        old_keys = set(existing[file_key].keys())
        if new_keys != old_keys:
            changed_files.append(file_key)
            continue
        for k in new_keys:
            if data[file_key][k] != existing[file_key].get(k):
                changed_files.append(file_key)
                break

    if not added_files and not removed_files and not changed_files:
        print("[OK] ja.json is up to date.")
        return 0

    print("[DRIFT DETECTED]")
    if added_files:
        print(f"  New files: {len(added_files)}")
        for f in sorted(added_files)[:5]:
            print(f"    + {f}")
    if removed_files:
        print(f"  Removed files: {len(removed_files)}")
        for f in sorted(removed_files)[:5]:
            print(f"    - {f}")
    if changed_files:
        print(f"  Changed files: {len(changed_files)}")
        for f in sorted(changed_files)[:5]:
            print(f"    ~ {f}")
    return 1


# =============================================================================
# CLI
# =============================================================================

def _merge_locale_data(
    existing_path: Path,
    new_data: Dict[str, Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    """既存の locale JSON に new_data をマージして返す。

    new_data に含まれるファイルは上書き、含まれないファイルは既存を維持。
    ただし、new_data と同じスコープ（パス接頭辞）のファイルで new_data に
    含まれないものは削除する（スコープ内の削除ファイルのパージ）。
    """
    if existing_path.exists():
        try:
            existing = json.loads(existing_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = {}
    else:
        existing = {}

    # スコープ内の古いエントリをパージ
    merged = {}
    for k, v in existing.items():
        if _same_scope(k, new_data) and k not in new_data:
            continue  # スコープ内だが new_data にない → 削除されたファイル
        merged[k] = v

    merged.update(new_data)
    return merged


def _get_files(scope: Optional[str]) -> List[Path]:
    """スコープに応じたファイルリストを返す"""
    if scope == "commands":
        return find_command_md_files()
    elif scope == "skills":
        return find_skill_md_files()
    else:
        return find_command_md_files() + find_skill_md_files()


def main():
    parser = argparse.ArgumentParser(description="MD i18n text extraction & translation")
    parser.add_argument("--dry-run", action="store_true", help="Show stats only, don't write files")
    parser.add_argument("--check", action="store_true", help="Check if ja.json is up to date")
    parser.add_argument("--translate", action="store_true", help="Translate to target languages")
    parser.add_argument("--lang", nargs="+", default=DEFAULT_TRANSLATE_LANGS, help="Target languages")
    parser.add_argument("--scope", choices=["commands", "skills"], help="Limit to commands or skills")
    parser.add_argument("--model", default=None, help="Gemini model override")
    parser.add_argument("--batch-size", type=int, default=50, help="Translation batch size")
    args = parser.parse_args()

    # Gemini モデル
    model = args.model
    if model is None:
        try:
            from bootcamp_utils import get_flash_model
            model = get_flash_model()
        except Exception:
            model = "gemini-2.0-flash"

    # ファイル列挙
    files = _get_files(args.scope)
    if not files:
        print("[WARN] No MD files found.")
        return

    print(f"Scanning {len(files)} MD files...")

    # 抽出
    data = extract_all(files)
    print_stats(data)

    scoped = args.scope is not None

    # --check モード
    if args.check:
        sys.exit(check_drift(data, scoped=scoped))

    # --dry-run: ここで終了
    if args.dry_run:
        return

    # ja.json 保存（スコープ指定時はマージ保存）
    MD_LOCALES_DIR.mkdir(parents=True, exist_ok=True)
    ja_path = MD_LOCALES_DIR / "ja.json"
    save_data = _merge_locale_data(ja_path, data) if scoped else data
    ja_path.write_text(
        json.dumps(save_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nSaved: {ja_path}")

    # --translate
    if args.translate:
        results = translate_all(data, args.lang, model, batch_size=args.batch_size)
        for lang, lang_data in results.items():
            lang_path = MD_LOCALES_DIR / f"{lang}.json"
            save_lang = _merge_locale_data(lang_path, lang_data) if scoped else lang_data
            lang_path.write_text(
                json.dumps(save_lang, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            total_keys = sum(len(v) for v in lang_data.values())
            print(f"Saved: {lang_path} ({total_keys} keys)")


if __name__ == "__main__":
    main()
