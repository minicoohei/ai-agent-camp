"""
i18n HTML Build Tool

日本語ソースHTMLと翻訳JSONから、各言語版HTMLを生成する。
- course/locales/{lang}.json の翻訳を適用
- course/dist/{lang}/ にHTML・CSS・画像を出力
- 言語切替UIをナビゲーションに挿入
- CSSフォントを言語別に調整

使い方:
  uv run python tools/i18n_build.py --lang en es          # EN/ES版を生成
  uv run python tools/i18n_build.py --lang en --verbose    # 詳細出力
  uv run python tools/i18n_build.py --lang en es --clean   # 既存を削除して再生成
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from i18n_common import COURSE_DIR, LOCALES_DIR, DIST_DIR, find_html_files

# 言語別フォント設定
FONT_OVERRIDES = {
    "en": "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
    "es": "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
}

# 言語表示名
LANG_LABELS = {
    "ja": "JA",
    "en": "EN",
    "es": "ES",
    "zh": "ZH",
    "ko": "KO",
}


def load_translations(lang: str) -> Dict[str, Dict[str, str]]:
    """翻訳JSONを読み込む"""
    filepath = LOCALES_DIR / f"{lang}.json"
    if not filepath.exists():
        print(f"  [ERROR] Translation file not found: {filepath}")
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_ja_keys() -> Dict[str, Dict[str, str]]:
    """日本語キーファイルを読み込む"""
    filepath = LOCALES_DIR / "ja.json"
    if not filepath.exists():
        print(f"  [ERROR] Japanese key file not found: {filepath}")
        print("  Run: uv run python tools/i18n_extract.py first")
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_relative_path(from_file: Path, to_base: str, lang: str) -> str:
    """HTMLファイルから言語版ルートへの相対パスを計算"""
    rel = from_file.relative_to(COURSE_DIR)
    depth = len(rel.parts) - 1  # ファイル名を除くディレクトリ深さ
    if depth == 0:
        prefix = ""
    else:
        prefix = "/".join([".."] * depth) + "/"
    return prefix


def build_lang_switcher(html_file: Path, available_langs: List[str]) -> str:
    """言語切替UIのHTML snippetを生成"""
    rel_path = html_file.relative_to(COURSE_DIR)
    depth = len(rel_path.parts) - 1

    # 各言語版へのリンクを計算
    links = []

    # 日本語版（オリジナル）へのリンク
    # dist/{lang}/path/file.html → ../../..（distの外）/path/file.html
    ja_prefix = "/".join([".."] * (depth + 2))  # dist/{lang} の2階層分を追加
    ja_href = f"{ja_prefix}/{rel_path}" if ja_prefix else str(rel_path)
    links.append(f'<a href="{ja_href}" class="lang-btn" data-lang="ja">JA</a>')

    for lang in available_langs:
        label = LANG_LABELS.get(lang, lang.upper())
        # 同じdist/{lang}/内の同じ相対パス
        # 現在のファイルから見た別言語版へのパス
        other_prefix = "/".join([".."] * (depth + 1))  # dist/{lang}のlang部分まで戻る
        other_href = f"{other_prefix}/{lang}/{rel_path}"
        links.append(f'<a href="{other_href}" class="lang-btn" data-lang="{lang}">{label}</a>')

    switcher_html = f"""
    <div class="lang-switcher d-flex align-items-center ms-auto gap-1">
      {" ".join(links)}
    </div>"""
    return switcher_html


def build_lang_switcher_css() -> str:
    """言語切替ボタンのCSS"""
    return """
/* Language Switcher */
.lang-switcher {
    display: flex;
    align-items: center;
    gap: 4px;
}
.lang-switcher .lang-btn {
    display: inline-block;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 600;
    text-decoration: none;
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    transition: all 0.2s;
}
.lang-switcher .lang-btn:hover {
    color: #fff;
    border-color: rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.1);
}
.lang-switcher .lang-btn.active {
    color: #fff;
    background: rgba(255, 255, 255, 0.2);
    border-color: #fff;
}
"""


def apply_translations(
    html_content: str,
    ja_keys: Dict[str, str],
    translations: Dict[str, str],
    lang: str,
    verbose: bool = False,
) -> Tuple[str, int, int]:
    """HTMLコンテンツに翻訳を適用する

    Returns: (translated_html, applied_count, missing_count)
    """
    from bs4 import BeautifulSoup, NavigableString

    soup = BeautifulSoup(html_content, "html.parser")
    applied = 0
    missing = 0

    # 1. <html lang="ja"> → <html lang="{lang}">
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = lang

    # 2. <title> タグ
    if "title" in translations:
        title_tag = soup.find("title")
        if title_tag:
            title_tag.string = translations["title"]
            applied += 1

    # 3. <meta> タグ
    for key, value in translations.items():
        if key.startswith("meta."):
            meta_name = key.split(".", 1)[1]
            meta_tag = soup.find("meta", attrs={"name": meta_name})
            if meta_tag:
                meta_tag["content"] = value
                applied += 1

    # 4. 本文テキスト置換 - ja_keysの値をHTMLから検索して翻訳で置換
    for key, ja_text in ja_keys.items():
        if key in ("title",) or key.startswith("meta."):
            continue  # 既に処理済み

        if key not in translations:
            missing += 1
            continue

        trans_text = translations[key]
        if not trans_text or trans_text == ja_text:
            continue

        # キーからタグ名とインデックスを解析
        # 形式: tag.class.index or tag.index or img[alt].index
        if _apply_key_translation(soup, key, ja_text, trans_text):
            applied += 1
        else:
            # フォールバック: テキスト検索で直接置換（全出現箇所）
            if _apply_text_search_all(soup, ja_text, trans_text):
                applied += 1

    # 5. 属性の全文置換パス（alt, title, aria-label, placeholder）
    for key, ja_text in ja_keys.items():
        if key not in translations:
            continue
        trans_text = translations[key]
        if not trans_text or trans_text == ja_text:
            continue
        # img[alt] 属性も全検索で置換
        for attr_name in ["alt", "title", "aria-label", "placeholder"]:
            for el in soup.find_all(attrs={attr_name: True}):
                if ja_text in el.get(attr_name, ""):
                    el[attr_name] = el[attr_name].replace(ja_text, trans_text)

    return str(soup), applied, missing


def _apply_key_translation(soup, key: str, ja_text: str, trans_text: str) -> bool:
    """キー形式に基づいてHTML要素のテキストを置換"""
    from bs4 import NavigableString

    # img[alt].N 形式
    m = re.match(r'^(\w+)\[(\w+)\]\.(\d+)$', key)
    if m:
        tag_name, attr_name, idx = m.group(1), m.group(2), int(m.group(3))
        elements = soup.find_all(tag_name)
        count = 0
        for el in elements:
            if el.get(attr_name):
                if count == idx:
                    el[attr_name] = trans_text
                    return True
                count += 1
        return False

    # tag.class.N 形式
    m = re.match(r'^(\w+)\.([a-zA-Z][\w\-]*?)\.(\d+)$', key)
    if m:
        tag_name, class_name, idx = m.group(1), m.group(2), int(m.group(3))
        elements = soup.find_all(tag_name, class_=lambda c: c and class_name in c)
        if idx < len(elements):
            el = elements[idx]
            _replace_direct_text(el, ja_text, trans_text)
            return True
        return False

    # tag.N 形式
    m = re.match(r'^(\w+)\.(\d+)$', key)
    if m:
        tag_name, idx = m.group(1), int(m.group(2))
        elements = soup.find_all(tag_name)
        # skip tags inside code/pre/script
        filtered = [
            el for el in elements
            if not any(p.name in {"script", "style", "code", "pre"} for p in el.parents)
        ]
        if idx < len(filtered):
            el = filtered[idx]
            _replace_direct_text(el, ja_text, trans_text)
            return True
        return False

    return False


def _replace_direct_text(element, old_text: str, new_text: str) -> bool:
    """要素の直接テキストを置換（子要素は保持）"""
    from bs4 import NavigableString

    replaced = False
    for child in list(element.children):
        if isinstance(child, NavigableString):
            text = str(child)
            if old_text in text:
                new_child = NavigableString(text.replace(old_text, new_text))
                child.replace_with(new_child)
                replaced = True
            elif text.strip() and text.strip() == old_text.strip():
                new_child = NavigableString(text.replace(text.strip(), new_text))
                child.replace_with(new_child)
                replaced = True

    # 子要素が全くない場合（string属性で直接テキスト）
    if not replaced and element.string and old_text in element.string:
        element.string = element.string.replace(old_text, new_text)
        replaced = True

    return replaced


def _apply_text_search_all(soup, ja_text: str, trans_text: str) -> bool:
    """テキスト検索で全出現箇所を置換（フォールバック）
    5文字未満の短いテキストはスキップ（誤置換防止）"""
    if len(ja_text) < 5:
        return False
    from bs4 import NavigableString

    found = False
    for text_node in soup.find_all(string=re.compile(re.escape(ja_text))):
        if any(p.name in {"script", "style", "code", "pre"} for p in text_node.parents if p.name):
            continue
        new_text = str(text_node).replace(ja_text, trans_text)
        text_node.replace_with(NavigableString(new_text))
        found = True
    return found


def insert_lang_switcher(html_content: str, switcher_html: str, lang: str) -> str:
    """ナビゲーションバーに言語切替UIを挿入（BeautifulSoup DOM操作）"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, "html.parser")
    navs = soup.find_all("nav")
    if not navs:
        return html_content

    nav = navs[-1]  # 最後の<nav>要素

    # switcher HTMLをパースして挿入
    switcher_soup = BeautifulSoup(switcher_html, "html.parser")
    switcher_el = switcher_soup.find(class_="lang-switcher")
    if not switcher_el:
        return html_content

    # 現在の言語ボタンに active クラスを追加
    for btn in switcher_el.find_all("a", class_="lang-btn"):
        if btn.get("data-lang") == lang:
            classes = [c for c in btn.get("class", []) if c != "active"]
            classes.append("active")
            btn["class"] = classes

    nav.append(switcher_el)
    return str(soup)


def copy_assets(lang: str, verbose: bool = False):
    """CSS・画像をdist/{lang}/にコピー"""
    src_assets = COURSE_DIR / "assets"
    dst_assets = DIST_DIR / lang / "assets"

    if not src_assets.exists():
        print(f"  [WARN] Assets directory not found: {src_assets}")
        return

    # CSS コピー + フォント調整
    src_css = src_assets / "css"
    dst_css = dst_assets / "css"
    if src_css.exists():
        dst_css.mkdir(parents=True, exist_ok=True)
        for css_file in src_css.iterdir():
            if css_file.is_file():
                content = css_file.read_text(encoding="utf-8")

                # bootcamp.css のフォント調整
                if css_file.name == "bootcamp.css" and lang in FONT_OVERRIDES:
                    # --font-sans の値を言語別に置換
                    content = re.sub(
                        r"(--font-sans:\s*)'[^;]+;",
                        rf"\g<1>{FONT_OVERRIDES[lang]};",
                        content,
                    )
                    # 言語切替CSSを追加
                    content += "\n" + build_lang_switcher_css()

                (dst_css / css_file.name).write_text(content, encoding="utf-8")
                if verbose:
                    print(f"    CSS: {css_file.name}")

    # 画像コピー（i18n_images.pyが後で翻訳版で上書きする）
    src_images = src_assets / "images"
    dst_images = dst_assets / "images"
    if src_images.exists():
        if dst_images.exists():
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)
        if verbose:
            img_count = sum(1 for _ in dst_images.rglob("*") if _.is_file())
            print(f"    Images: {img_count} files copied")

    # material コピー
    src_material = src_assets / "material"
    dst_material = dst_assets / "material"
    if src_material.exists():
        if dst_material.exists():
            shutil.rmtree(dst_material)
        shutil.copytree(src_material, dst_material)

    # サブディレクトリのアセットコピー（setup/assets など）
    for subdir in COURSE_DIR.iterdir():
        if subdir.is_dir() and subdir.name not in ("assets", "dist", "_templates", "exercises"):
            sub_assets = subdir / "assets"
            if sub_assets.exists():
                dst_sub_assets = DIST_DIR / lang / subdir.name / "assets"
                if dst_sub_assets.exists():
                    shutil.rmtree(dst_sub_assets)
                shutil.copytree(sub_assets, dst_sub_assets)
                if verbose:
                    print(f"    Sub-assets: {subdir.name}/assets copied")


def build_language(
    lang: str,
    ja_keys: Dict[str, Dict[str, str]],
    translations: Dict[str, Dict[str, str]],
    available_langs: List[str],
    verbose: bool = False,
) -> Dict[str, any]:
    """1言語分のHTML生成"""
    html_files = find_html_files()
    lang_dir = DIST_DIR / lang

    stats = {
        "files": 0,
        "applied": 0,
        "missing": 0,
        "errors": [],
    }

    print(f"\n=== Building {lang.upper()} ({len(html_files)} files) ===")

    for html_file in html_files:
        rel_path = html_file.relative_to(COURSE_DIR)
        file_key = str(rel_path).replace("\\", "/")

        # 出力先
        out_file = lang_dir / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        # ソースHTML読み込み
        html_content = html_file.read_text(encoding="utf-8")

        # 翻訳適用
        file_ja = ja_keys.get(file_key, {})
        file_trans = translations.get(file_key, {})

        if file_trans:
            translated, applied, missing = apply_translations(
                html_content, file_ja, file_trans, lang, verbose
            )
            stats["applied"] += applied
            stats["missing"] += missing
        else:
            # 翻訳なし - 最低限lang属性だけ変更
            translated = re.sub(
                r'<html\s+lang="ja"', f'<html lang="{lang}"', html_content
            )
            applied = 0
            missing = len(file_ja)
            stats["missing"] += missing
            if verbose and file_ja:
                print(f"  [WARN] No translations for: {file_key} ({missing} keys)")

        # 言語切替UI挿入
        switcher = build_lang_switcher(html_file, available_langs)
        translated = insert_lang_switcher(translated, switcher, lang)

        # ファイル書き出し
        out_file.write_text(translated, encoding="utf-8")
        stats["files"] += 1

        if verbose:
            print(f"  [{stats['files']:3d}/{len(html_files)}] {file_key} (applied={applied})")

    # アセットコピー
    print(f"  Copying assets...")
    copy_assets(lang, verbose)

    print(f"  Done: {stats['files']} files, {stats['applied']} translations applied, {stats['missing']} missing")
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="i18n HTML Build Tool - 翻訳JSONから各言語版HTMLを生成"
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        required=True,
        help="生成する言語 (例: en es)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=COURSE_DIR,
        help=f"ソースディレクトリ (default: {COURSE_DIR})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DIST_DIR,
        help=f"出力ディレクトリ (default: {DIST_DIR})",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="既存のdist/{lang}を削除してから生成",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="詳細出力",
    )
    args = parser.parse_args()

    # 依存チェック
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: beautifulsoup4 is required. Install with: pip install beautifulsoup4")
        sys.exit(1)

    # ja.json 読み込み
    ja_keys = load_ja_keys()
    if not ja_keys:
        sys.exit(1)

    print(f"Source: {COURSE_DIR}")
    print(f"Output: {DIST_DIR}")
    print(f"Languages: {', '.join(args.lang)}")
    print(f"Japanese keys: {sum(len(v) for v in ja_keys.values())} keys in {len(ja_keys)} files")

    all_stats = {}

    for lang in args.lang:
        # Clean
        if args.clean:
            lang_dir = DIST_DIR / lang
            if lang_dir.exists():
                shutil.rmtree(lang_dir)
                print(f"  Cleaned: {lang_dir}")

        # 翻訳読み込み
        translations = load_translations(lang)
        if not translations:
            print(f"  [SKIP] No translations for {lang}")
            continue

        # ビルド
        stats = build_language(lang, ja_keys, translations, args.lang, args.verbose)
        all_stats[lang] = stats

    # サマリー
    print("\n" + "=" * 60)
    print("BUILD SUMMARY")
    print("=" * 60)
    for lang, stats in all_stats.items():
        print(f"  {lang.upper()}: {stats['files']} files, "
              f"{stats['applied']} applied, {stats['missing']} missing")
    print()


if __name__ == "__main__":
    main()
