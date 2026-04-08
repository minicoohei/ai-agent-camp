"""
i18n Text Extraction & Translation Tool

HTML教材からテキストを抽出し、翻訳用JSONキーファイルを生成する。
- course/ 配下の全HTMLファイルを解析
- 可視テキストノード（見出し、段落、ラベル、バッジ、alt属性等）を抽出
- ja.json を生成し、--translate フラグで en.json / es.json を Gemini API で翻訳

使い方:
  uv run python tools/i18n_extract.py                    # ja.json を生成
  uv run python tools/i18n_extract.py --dry-run           # 統計のみ表示
  uv run python tools/i18n_extract.py --translate          # ja/en/es.json を生成
  uv run python tools/i18n_extract.py --translate --lang ko # ja/ko.json を生成
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_flash_model
from i18n_common import (
    ROOT_DIR, COURSE_DIR, LOCALES_DIR, EXCLUDE_DIRS,
    LANGUAGE_NAMES, is_excluded, find_html_files,
    require_gemini_client, get_language_name,
)

load_runtime_env()


# テキスト抽出対象タグ
TEXT_TAGS = [
    "title", "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "span", "label", "a", "li", "td", "th",
    "figcaption", "caption", "summary", "legend",
    "dt", "dd", "blockquote", "cite", "small", "strong", "em",
    "button",
]

# テキスト抽出対象属性
TEXT_ATTRS = ["alt", "title", "placeholder", "aria-label"]

# meta タグから抽出する name 属性
META_NAMES = ["description", "keywords"]

# スキップするタグ（中のテキストを無視）
SKIP_TAGS = {"script", "style", "code", "pre", "noscript", "svg", "math"}

# 翻訳時に保持すべき技術用語（翻訳しない）
TECHNICAL_TERMS = [
    "Claude Code", "Claude", "Cursor", "BigQuery", "Google Cloud",
    "GitHub Actions", "GitHub", "Slack", "Notion", "Google Apps Script",
    "GAS", "API", "LLM", "AI", "PPTX", "PDF", "CSV", "JSON", "HTML",
    "CSS", "JavaScript", "Python", "Node.js", "Git", "Docker",
    "PlantUML", "UML", "Gemini", "Tailwind", "Bootstrap",
    "Vercel", "Playwright", "E2E", "EDA", "PRD", "WBS",
    "Nano Banana", "NotebookLM", "aiagent-base",
    "marimo", "gogcli", "clasp", "npm", "pip",
]

# デフォルト翻訳対象言語
DEFAULT_TRANSLATE_LANGS = ["en", "es"]

# =============================================================================
# HTML 解析・テキスト抽出
# =============================================================================


def _get_direct_text(element) -> str:
    """要素の直接テキスト（子要素のテキストを除く）を取得"""
    from bs4 import NavigableString

    texts = []
    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                texts.append(text)
    return " ".join(texts)


def _generate_key(tag_name: str, element, counters: Dict[str, int]) -> str:
    """要素からセマンティックなキーを生成する

    形式: {element}.{class_or_role}.{index}
    例: h1.0, p.lead.0, span.badge.1, a.nav-link.0
    """
    # クラスまたはroleからセマンティックなラベルを取得
    role = element.get("role", "")
    classes = element.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()

    # 優先的に使うクラス名（セマンティックなもの）
    semantic_classes = [
        "lead", "badge", "nav-link", "navbar-brand", "card-title",
        "card-text", "card-header", "card-body", "card-footer",
        "hero-title", "hero-subtitle", "section-title", "module-title",
        "alert", "btn", "breadcrumb-item", "list-group-item",
        "accordion-button", "tab-pane", "modal-title",
    ]

    label = ""
    for sc in semantic_classes:
        if sc in classes:
            label = sc
            break

    if not label and role:
        label = role

    # キー文字列を組み立て
    if label:
        base_key = f"{tag_name}.{label}"
    else:
        base_key = tag_name

    # インデックス付与
    count = counters.get(base_key, 0)
    counters[base_key] = count + 1
    return f"{base_key}.{count}"


def extract_texts_from_html(filepath: Path) -> Dict[str, str]:
    """HTMLファイルからテキストを抽出してキー付き辞書を返す"""
    from bs4 import BeautifulSoup, Comment

    content = filepath.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")

    texts: Dict[str, str] = {}
    counters: Dict[str, int] = {}

    # 1. <title> タグ
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        title_text = title_tag.string.strip()
        if title_text:
            texts["title"] = title_text

    # 2. <meta> タグ（description, keywords）
    for meta_name in META_NAMES:
        meta_tag = soup.find("meta", attrs={"name": meta_name})
        if meta_tag and meta_tag.get("content", "").strip():
            texts[f"meta.{meta_name}"] = meta_tag["content"].strip()

    # 3. 本文テキストノード
    body = soup.find("body")
    if not body:
        return texts

    for element in body.find_all(TEXT_TAGS):
        # スキップ対象タグの中にいる場合は無視
        if any(parent.name in SKIP_TAGS for parent in element.parents):
            continue

        # コメントノードは無視
        if isinstance(element, Comment):
            continue

        # 直接テキストを取得（子要素テキストは子要素自体の処理で拾う）
        direct_text = _get_direct_text(element)
        if not direct_text:
            # 子要素がなく string が設定されている場合
            if element.string and element.string.strip():
                direct_text = element.string.strip()

        if direct_text and len(direct_text) >= 2:
            # 純粋な数字・記号のみはスキップ
            if re.match(r'^[\d\s\-\.\,\;\:\!\?\#\@\%\&\*\(\)\[\]\{\}\/\\]+$', direct_text):
                continue
            # Bootstrap アイコンクラス名のみはスキップ
            if re.match(r'^bi[\s\-]', direct_text):
                continue

            key = _generate_key(element.name, element, counters)
            texts[key] = direct_text

        # 4. テキスト属性（alt, title, placeholder, aria-label）
        for attr in TEXT_ATTRS:
            attr_val = element.get(attr, "").strip()
            if attr_val and len(attr_val) >= 2:
                attr_key_base = f"{element.name}[{attr}]"
                count = counters.get(attr_key_base, 0)
                counters[attr_key_base] = count + 1
                texts[f"{attr_key_base}.{count}"] = attr_val

    # 5. body 直下の img タグ（TEXT_TAGS に含まれない）
    for img in body.find_all("img"):
        if any(parent.name in SKIP_TAGS for parent in img.parents):
            continue
        for attr in ["alt", "title"]:
            attr_val = img.get(attr, "").strip()
            if attr_val and len(attr_val) >= 2:
                attr_key_base = f"img[{attr}]"
                count = counters.get(attr_key_base, 0)
                counters[attr_key_base] = count + 1
                texts[f"{attr_key_base}.{count}"] = attr_val

    return texts


def extract_all(html_files: List[Path]) -> Dict[str, Dict[str, str]]:
    """全HTMLファイルからテキストを抽出"""
    result = {}
    for filepath in html_files:
        rel_path = str(filepath.relative_to(COURSE_DIR))
        texts = extract_texts_from_html(filepath)
        if texts:
            result[rel_path] = texts
    return result


# =============================================================================
# 翻訳（Gemini API）
# =============================================================================

def _build_translation_prompt(
    texts: Dict[str, str], target_lang: str, lang_name: str
) -> str:
    """翻訳用プロンプトを構築"""
    terms_list = ", ".join(TECHNICAL_TERMS[:30])
    return f"""You are a professional translator. Translate the following JSON values from Japanese to {lang_name}.

RULES:
1. Translate ONLY the values, keep the keys exactly as they are.
2. DO NOT translate technical terms: {terms_list}, and similar tool/product names.
3. Preserve any HTML entities (e.g., &amp;, &lt;) and inline HTML markup.
4. Maintain the same tone and formality level as the original.
5. Return ONLY valid JSON, no markdown code fences, no explanation.

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
    prompt = _build_translation_prompt(texts, target_lang, lang_name)

    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
        )
        response_text = response.text.strip()

        # マークダウンコードフェンスを除去
        if response_text.startswith("```"):
            # ```json ... ``` パターン
            lines = response_text.split("\n")
            # 最初と最後の ``` 行を除去
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        return json.loads(response_text)
    except (json.JSONDecodeError, Exception) as e:
        print(f"  [WARN] Batch translation failed: {e}", file=sys.stderr)
        # フォールバック: 原文をそのまま返す
        return texts


def translate_file_texts(
    client,
    texts: Dict[str, str],
    target_lang: str,
    model: str,
    batch_size: int = 50,
) -> Dict[str, str]:
    """1ファイル分のテキストをバッチに分割して翻訳"""
    keys = list(texts.keys())
    translated = {}

    for i in range(0, len(keys), batch_size):
        batch_keys = keys[i : i + batch_size]
        batch = {k: texts[k] for k in batch_keys}
        result = translate_batch(client, batch, target_lang, model)
        translated.update(result)

        # レート制限対策: バッチ間に短い待機
        if i + batch_size < len(keys):
            time.sleep(1)

    return translated


def translate_all(
    ja_data: Dict[str, Dict[str, str]],
    target_langs: List[str],
    model: str,
    batch_size: int = 50,
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """全ファイル・全言語を翻訳

    Returns:
        {lang: {file_path: {key: translated_text}}}
    """
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

            # ファイル間の待機
            if idx < total_files:
                time.sleep(0.5)

    return results


# =============================================================================
# 統計表示
# =============================================================================


def print_stats(data: Dict[str, Dict[str, str]]) -> None:
    """抽出統計を表示"""
    total_files = len(data)
    total_keys = sum(len(v) for v in data.values())
    total_chars = sum(len(text) for texts in data.values() for text in texts.values())

    print("\n=== i18n Extraction Stats ===")
    print(f"  Files scanned:  {total_files}")
    print(f"  Total keys:     {total_keys}")
    print(f"  Total chars:    {total_chars:,}")
    print()

    # ファイル別の内訳（上位10件）
    file_counts = sorted(data.items(), key=lambda x: len(x[1]), reverse=True)
    print("  Top 10 files by key count:")
    for filepath, texts in file_counts[:10]:
        print(f"    {filepath}: {len(texts)} keys")

    # タグ種別の集計
    tag_counts: Dict[str, int] = {}
    for texts in data.values():
        for key in texts:
            # キーの先頭部分（タグ名）を抽出
            tag = key.split(".")[0].split("[")[0]
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print("\n  Keys by element type:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"    {tag}: {count}")


# =============================================================================
# ファイル出力
# =============================================================================


def save_json(data: Dict, filepath: Path) -> None:
    """JSONファイルを保存（UTF-8, pretty-print）"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {filepath}")


# =============================================================================
# CLI
# =============================================================================


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="i18n テキスト抽出・翻訳ツール - HTML教材から翻訳キーを生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  uv run python tools/i18n_extract.py                     # ja.json を生成
  uv run python tools/i18n_extract.py --dry-run            # 統計のみ表示（ファイル書き出しなし）
  uv run python tools/i18n_extract.py --translate           # ja/en/es.json を生成
  uv run python tools/i18n_extract.py --translate --lang ko # ja/ko.json を生成
  uv run python tools/i18n_extract.py --translate --lang en ko zh  # 複数言語指定
        """,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="統計のみ表示し、ファイルを書き出さない",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Gemini API で翻訳を実行する（デフォルト: en, es）",
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        default=None,
        help="翻訳先言語コード（例: en es ko zh）。--translate と併用",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="翻訳に使用するGeminiモデル（デフォルト: gemini-3-flash-preview）",
    )
    def _positive_int(value: str) -> int:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                f"--batch-size は正の整数が必要です（入力値: {value}）"
            )
        return ivalue

    parser.add_argument(
        "--batch-size",
        type=_positive_int,
        default=50,
        help="翻訳バッチサイズ（デフォルト: 50）",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="出力ディレクトリ（デフォルト: course/locales/）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else LOCALES_DIR
    model = args.model or get_flash_model()

    # 1. HTMLファイルの探索
    print(f"Scanning HTML files in: {COURSE_DIR}")
    html_files = find_html_files()
    print(f"  Found {len(html_files)} HTML files")

    if not html_files:
        print("[WARN] No HTML files found.", file=sys.stderr)
        sys.exit(0)

    # 2. テキスト抽出
    print("\nExtracting texts...")
    try:
        from bs4 import BeautifulSoup  # noqa: F401
    except ImportError:
        print(
            "[ERROR] BeautifulSoup4 が必要です: pip install beautifulsoup4",
            file=sys.stderr,
        )
        sys.exit(1)

    ja_data = extract_all(html_files)

    # 3. 統計表示
    print_stats(ja_data)

    if args.dry_run:
        print("\n[DRY RUN] ファイル書き出しをスキップしました。")
        return

    # 4. ja.json 保存
    ja_path = output_dir / "ja.json"
    print(f"\nSaving Japanese source file...")
    save_json(ja_data, ja_path)

    # 5. 翻訳（オプション）
    if args.translate:
        target_langs = args.lang if args.lang else DEFAULT_TRANSLATE_LANGS
        print(f"\nTranslating to: {', '.join(target_langs)}")
        print(f"  Model: {model}")
        print(f"  Batch size: {args.batch_size}")

        translations = translate_all(ja_data, target_langs, model, batch_size=args.batch_size)

        for lang, lang_data in translations.items():
            lang_path = output_dir / f"{lang}.json"
            save_json(lang_data, lang_path)

    print("\nDone!")


if __name__ == "__main__":
    main()
