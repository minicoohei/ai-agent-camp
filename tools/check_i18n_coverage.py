#!/usr/bin/env python3
# i18n coverage checker - detect missing i18n keys for new HTML files
"""i18n coverage check - detect missing i18n support for new HTML files.

Verifies that all HTML files under course/ have corresponding keys
in locale JSON files (en.json, es.json).

Checks:
1. HTML files not registered in ja.json (i18n_extract.py not run)
2. File sections missing in en/es.json
3. Individual keys missing within existing sections

Usage:
    uv run python tools/check_i18n_coverage.py              # Full check
    uv run python tools/check_i18n_coverage.py --lang en     # English only
    uv run python tools/check_i18n_coverage.py --quick       # File-level only (fast)
    uv run python tools/check_i18n_coverage.py --fix-hint    # Show fix commands
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = PROJECT_ROOT / "course"
LOCALES_DIR = COURSE_DIR / "locales"

# i18n対象外のディレクトリ
EXCLUDE_DIRS = {"dist", "assets", "_templates", "exercises"}


def find_html_files() -> list[str]:
    """course/ 配下のHTMLファイルを相対パスで取得（i18n対象のみ）"""
    files = []
    for html_file in sorted(COURSE_DIR.rglob("*.html")):
        rel = html_file.relative_to(COURSE_DIR)
        # 除外ディレクトリをスキップ
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        files.append(str(rel))
    return files


def load_locale(lang: str) -> dict:
    """locale JSONを読み込む"""
    path = LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_coverage(target_langs: list[str], quick: bool = False) -> int:
    """カバレッジチェックを実行。エラー数を返す。"""
    errors = 0

    # HTMLファイル一覧
    html_files = find_html_files()
    ja_data = load_locale("ja")

    print(f"Course HTML files: {len(html_files)}")
    print(f"ja.json sections:  {len(ja_data)}")
    print(f"Target languages:  {', '.join(target_langs)}")
    print()

    # --- Check 1: ja.json に未登録のHTMLファイル ---
    ja_sections = sorted(ja_data.keys())
    unregistered = []
    for html_file in html_files:
        if html_file not in ja_sections:
            unregistered.append(html_file)

    if unregistered:
        print(f"[FAIL] i18n_extract: {len(unregistered)} HTML file(s) not in ja.json")
        for f in unregistered:
            print(f"  - {f} (run: uv run python tools/i18n_extract.py)")
        errors += len(unregistered)
    else:
        print(f"[PASS] i18n_extract: All {len(html_files)} HTML files registered in ja.json")

    # --- Check 2: en/es.json のファイルセクション欠損 ---
    for lang in target_langs:
        lang_data = load_locale(lang)
        if not lang_data:
            print(f"[FAIL] {lang}.json: File not found")
            errors += 1
            continue

        lang_sections = set(lang_data.keys())

        # ファイル単位の欠損
        missing_files = []
        for section in ja_sections:
            if section not in lang_sections:
                missing_files.append(section)

        if missing_files:
            print(f"[FAIL] {lang}.json: {len(missing_files)} file section(s) missing")
            for f in missing_files:
                key_count = len(ja_data.get(f, {}))
                print(f"  - {f} ({key_count} keys)")
            errors += len(missing_files)
        else:
            print(f"[PASS] {lang}.json: All {len(ja_sections)} file sections present")

        if quick:
            continue

        # キー単位の欠損
        missing_keys_total = 0
        files_with_missing = []
        for section in ja_sections:
            if section not in lang_sections:
                continue
            ja_keys = set(ja_data[section].keys())
            lang_keys = set(lang_data[section].keys())
            missing = ja_keys - lang_keys
            if missing:
                missing_keys_total += len(missing)
                files_with_missing.append((section, len(missing), len(ja_keys)))

        if files_with_missing:
            print(
                f"[FAIL] {lang}.json: {missing_keys_total} key(s) missing "
                f"across {len(files_with_missing)} file(s)"
            )
            for f, miss, total in sorted(files_with_missing)[:10]:
                print(f"  - {f}: {miss}/{total} keys missing")
            if len(files_with_missing) > 10:
                print(
                    f"  ... and {len(files_with_missing) - 10} more file(s)"
                )
            errors += missing_keys_total
        else:
            total_keys = sum(len(v) for v in ja_data.values())
            print(f"[PASS] {lang}.json: All {total_keys} keys present (100% coverage)")

    # --- Summary ---
    print()
    if errors > 0:
        print(f"RESULT: FAIL ({errors} error(s))")
        return 1
    else:
        print("RESULT: PASS (all checks passed)")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="i18n カバレッジチェック - HTMLファイルのi18n対応漏れを検出"
    )
    parser.add_argument(
        "--lang", nargs="+", default=["en", "es"],
        help="チェック対象の言語コード（デフォルト: en es）"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="ファイル単位の欠損のみチェック（キー単位スキップ）"
    )
    parser.add_argument(
        "--fix-hint", action="store_true",
        help="修正に必要なコマンドを表示"
    )
    args = parser.parse_args()

    exit_code = check_coverage(args.lang, quick=args.quick)

    if args.fix_hint and exit_code > 0:
        print()
        print("=== Fix Commands ===")
        print("# Step 1: Extract keys from HTML to ja.json")
        print("uv run python tools/i18n_extract.py")
        print()
        print("# Step 2: Translate to en/es (requires GEMINI_API_KEY)")
        print("uv run python tools/i18n_extract.py --translate --lang en es")
        print()
        print("# Step 3: Build translated HTML")
        print("uv run python tools/i18n_build.py --lang en es")
        print()
        print("# Step 4: QA check")
        print("uv run python tools/i18n_check.py --lang en es")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
