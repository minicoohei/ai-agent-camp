"""
i18n_images.py - Course Image Translation Tool

Translates text in course images using Gemini API.

Two modes:
  1. --classify-only: Scan images, classify them, extract text (OCR), save manifest
  2. Default: Read manifest and translate images to target language(s)

Usage:
  uv run python tools/i18n_images.py --classify-only
  uv run python tools/i18n_images.py --lang en es
  uv run python tools/i18n_images.py --lang en --skip-existing --batch-size 10
  uv run python tools/i18n_images.py --lang en --dry-run --verbose
"""

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_flash_model, get_image_model
from i18n_common import ROOT_DIR, get_language_name, require_gemini_client

load_runtime_env()


# パス定数
IMAGES_DIR = ROOT_DIR / "course" / "assets" / "images"
LOCALES_DIR = ROOT_DIR / "course" / "locales"
DIST_DIR = ROOT_DIR / "course" / "dist"
DEFAULT_MANIFEST_PATH = LOCALES_DIR / "image_manifest.json"

# 対応画像拡張子
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# API レート制限の待機時間（秒）
API_DELAY = 2.0

# 分類カテゴリ
VALID_CATEGORIES = {"text-heavy", "annotated", "decorative", "chart"}

def scan_images(images_dir: Path) -> list[str]:
    """画像ディレクトリを再帰的にスキャンし、相対パスのリストを返す"""
    image_paths = []
    for ext in IMAGE_EXTENSIONS:
        for img_path in sorted(images_dir.rglob(f"*{ext}")):
            rel = img_path.relative_to(images_dir)
            image_paths.append(str(rel))
    # SVG は画像生成APIでは扱えないのでスキップ
    return sorted(set(image_paths))


def classify_single_image(
    client, image_path: Path, verbose: bool = False
) -> dict:
    """
    Gemini Vision API で画像を分類し、テキストを抽出する。

    Returns:
        {
            "category": "text-heavy" | "annotated" | "decorative" | "chart",
            "texts": ["extracted", "text", "items"],
            "needs_translation": bool
        }
    """
    if verbose:
        print(f"  Analyzing: {image_path.name}")

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"  ERROR: Cannot open image {image_path}: {e}")
        return {
            "category": "decorative",
            "texts": [],
            "needs_translation": False,
            "error": str(e),
        }

    prompt = """Analyze this image and respond in JSON format only (no markdown fences).

1. Classify the image into ONE of these categories:
   - "text-heavy": Contains significant readable text (titles, paragraphs, labels, descriptions)
   - "annotated": Contains annotations like arrows, callouts, numbered markers overlaid on a screenshot or diagram
   - "chart": Contains charts, graphs, flowcharts, diagrams with some text labels
   - "decorative": Mostly visual/decorative with little or no text (icons, photos, illustrations, logos)

2. Extract ALL visible text from the image (OCR). Include every piece of text you can read, even small labels. For Japanese text, keep the original Japanese.

3. Determine if this image needs translation:
   - true: if it contains readable text in any language that conveys meaning
   - false: if it's purely decorative, or contains only universal symbols/numbers/code

Respond with ONLY this JSON (no explanation, no code fences):
{"category": "<category>", "texts": ["<text1>", "<text2>", ...], "needs_translation": <true|false>}"""

    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[img, prompt],
        )

        raw_text = response.text.strip()
        # JSON パース（コードフェンスが付いている場合の対応）
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            # 先頭と末尾のフェンスを除去
            json_lines = []
            in_fence = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                    continue
                json_lines.append(line)
            raw_text = "\n".join(json_lines).strip()

        result = json.loads(raw_text)

        # バリデーション
        category = result.get("category", "decorative")
        if category not in VALID_CATEGORIES:
            category = "decorative"

        texts = result.get("texts", [])
        if not isinstance(texts, list):
            texts = []
        texts = [str(t) for t in texts if t]

        needs_translation = result.get("needs_translation", False)
        if not isinstance(needs_translation, bool):
            needs_translation = bool(needs_translation)

        return {
            "category": category,
            "texts": texts,
            "needs_translation": needs_translation,
        }

    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse error for {image_path.name}: {e}")
        if verbose:
            print(f"  Raw response: {raw_text[:200]}")
        return {
            "category": "decorative",
            "texts": [],
            "needs_translation": False,
            "error": f"JSON parse error: {e}",
        }
    except Exception as e:
        print(f"  ERROR: API call failed for {image_path.name}: {e}")
        return {
            "category": "decorative",
            "texts": [],
            "needs_translation": False,
            "error": str(e),
        }


def classify_images(
    client,
    images_dir: Path,
    manifest_path: Path,
    batch_size: int = 5,
    verbose: bool = False,
    dry_run: bool = False,
) -> dict:
    """
    全画像を分類してマニフェストを生成・保存する。

    Returns:
        manifest dict
    """
    image_paths = scan_images(images_dir)
    total = len(image_paths)
    print(f"\nFound {total} images in {images_dir}")

    if dry_run:
        print("\n[DRY RUN] Would classify the following images:")
        for p in image_paths:
            print(f"  - {p}")
        return {}

    manifest = {}
    errors = 0
    needs_translation_count = 0

    for idx, rel_path in enumerate(image_paths, 1):
        abs_path = images_dir / rel_path
        category_label = ""

        print(f"Classifying {idx}/{total}: {rel_path}", end="")

        result = classify_single_image(client, abs_path, verbose=verbose)
        manifest[rel_path] = result
        category_label = f" [{result['category']}]"

        if result.get("error"):
            errors += 1
            print(f"{category_label} ERROR")
        else:
            if result["needs_translation"]:
                needs_translation_count += 1
            print(
                f"{category_label} texts={len(result['texts'])} "
                f"translate={'yes' if result['needs_translation'] else 'no'}"
            )

        # レート制限対策
        if idx < total:
            time.sleep(API_DELAY)

    # マニフェスト保存
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Classification complete!")
    print(f"  Total images: {total}")
    print(f"  Needs translation: {needs_translation_count}")
    print(f"  No translation needed: {total - needs_translation_count - errors}")
    print(f"  Errors: {errors}")
    print(f"  Manifest saved to: {manifest_path}")
    print(f"{'='*60}\n")

    return manifest


def load_manifest(manifest_path: Path) -> dict:
    """マニフェストファイルを読み込む"""
    if not manifest_path.exists():
        print(f"ERROR: Manifest not found: {manifest_path}")
        print("Run with --classify-only first to generate the manifest.")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def translate_single_image(
    client,
    source_path: Path,
    output_path: Path,
    lang: str,
    texts: list[str],
    category: str,
    verbose: bool = False,
    retry: bool = True,
) -> bool:
    """
    1枚の画像を翻訳する。

    Args:
        client: Gemini API client
        source_path: 元画像のパス
        output_path: 出力先パス
        lang: 翻訳先言語コード
        texts: 元画像から抽出されたテキスト一覧
        category: 画像カテゴリ
        verbose: 詳細出力
        retry: 失敗時にリトライするか

    Returns:
        成功したら True
    """
    lang_name = get_language_name(lang)

    try:
        input_image = Image.open(source_path)
    except Exception as e:
        print(f"  ERROR: Cannot open source image: {e}")
        return False

    # テキストマッピングの構成（プロンプトに含める）
    text_list = ""
    if texts:
        text_list = "\n".join(f"  - \"{t}\"" for t in texts)
        text_list = f"\n\nOriginal texts found in the image:\n{text_list}"

    # カテゴリに応じたプロンプト調整
    if category == "chart":
        extra_instruction = (
            "This is a chart/diagram. Translate all text labels, axis labels, "
            "legend entries, and titles. Preserve the chart structure, colors, "
            "and data exactly as they are."
        )
    elif category == "annotated":
        extra_instruction = (
            "This is an annotated screenshot. Translate all annotation text, "
            "callout labels, and any visible UI text. Keep all arrows, boxes, "
            "circles, and other annotation markers in their exact positions."
        )
    else:
        extra_instruction = (
            "Translate all visible text content while maintaining the exact "
            "same visual hierarchy and emphasis."
        )

    prompt = (
        f"Edit this image to replace all Japanese text with {lang_name} text. "
        f"Keep the exact same layout, colors, design, fonts, and visual structure. "
        f"Only change the text language from Japanese to {lang_name}. "
        f"{extra_instruction}"
        f"{text_list}"
    )

    if verbose:
        print(f"  Prompt: {prompt[:150]}...")

    # アスペクト比を取得
    width, height = input_image.size
    aspect_ratio = width / height
    if aspect_ratio > 1.9:
        ar_str = "21:9"
    elif aspect_ratio > 1.5:
        ar_str = "16:9"
    elif aspect_ratio > 1.2:
        ar_str = "4:3"
    elif aspect_ratio > 0.9:
        ar_str = "1:1"
    elif aspect_ratio > 0.7:
        ar_str = "3:4"
    else:
        ar_str = "9:16"

    attempt = 0
    max_attempts = 2 if retry else 1

    while attempt < max_attempts:
        attempt += 1
        try:
            response = client.models.generate_content(
                model=get_image_model(),
                contents=[prompt, input_image],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio=ar_str,
                    ),
                ),
            )

            # レスポンスから画像を抽出
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.inline_data:
                        result_image = types.Part.as_image(part)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        result_image.save(output_path)
                        return True

            if attempt < max_attempts:
                print(f"  WARNING: No image in response, retrying...")
                time.sleep(API_DELAY)
            else:
                print(f"  ERROR: No image data in response after {max_attempts} attempts")
                return False

        except Exception as e:
            if attempt < max_attempts:
                print(f"  WARNING: API error (attempt {attempt}): {e}, retrying...")
                time.sleep(API_DELAY)
            else:
                print(f"  ERROR: API call failed after {max_attempts} attempts: {e}")
                return False

    return False


def copy_image(source_path: Path, output_path: Path) -> bool:
    """画像をそのままコピーする（翻訳不要な画像用）"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, output_path)
        return True
    except Exception as e:
        print(f"  ERROR: Failed to copy {source_path}: {e}")
        return False


def translate_images(
    client,
    manifest: dict,
    images_dir: Path,
    languages: list[str],
    batch_size: int = 5,
    skip_existing: bool = False,
    verbose: bool = False,
    dry_run: bool = False,
) -> dict:
    """
    マニフェストに基づいて全画像を翻訳する。

    Returns:
        結果サマリーの dict
    """
    results = {}

    for lang in languages:
        lang_name = get_language_name(lang)
        output_base = DIST_DIR / lang / "assets" / "images"

        print(f"\n{'='*60}")
        print(f"Translating images to {lang_name} ({lang})")
        print(f"Output directory: {output_base}")
        print(f"{'='*60}\n")

        total = len(manifest)
        translated = 0
        copied = 0
        skipped = 0
        errors = 0

        items = list(manifest.items())

        for idx, (rel_path, info) in enumerate(items, 1):
            source_path = images_dir / rel_path
            output_path = output_base / rel_path
            needs_translation = info.get("needs_translation", False)
            category = info.get("category", "decorative")
            texts = info.get("texts", [])

            # 元ファイルが存在するか確認
            if not source_path.exists():
                print(f"  SKIP {idx}/{total}: {rel_path} (source not found)")
                errors += 1
                continue

            # 既存ファイルのスキップ
            if skip_existing and output_path.exists():
                if verbose:
                    print(f"  SKIP {idx}/{total}: {rel_path} (already exists)")
                skipped += 1
                continue

            if needs_translation:
                action = "translate"
                label = f"[{category}] -> {lang}"
            else:
                action = "copy"
                label = "[copy]"

            if dry_run:
                print(f"  [DRY RUN] {idx}/{total}: {rel_path} {label}")
                continue

            print(f"Processing {idx}/{total}: {rel_path} {label}", end="")

            if needs_translation:
                success = translate_single_image(
                    client=client,
                    source_path=source_path,
                    output_path=output_path,
                    lang=lang,
                    texts=texts,
                    category=category,
                    verbose=verbose,
                )
                if success:
                    translated += 1
                    print(f" -> OK")
                else:
                    errors += 1
                    print(f" -> FAILED")

                # レート制限対策
                time.sleep(API_DELAY)
            else:
                success = copy_image(source_path, output_path)
                if success:
                    copied += 1
                    print(f" -> copied")
                else:
                    errors += 1
                    print(f" -> FAILED")

        results[lang] = {
            "total": total,
            "translated": translated,
            "copied": copied,
            "skipped": skipped,
            "errors": errors,
        }

        print(f"\n{'='*60}")
        print(f"Results for {lang_name} ({lang}):")
        print(f"  Total images: {total}")
        print(f"  Translated: {translated}")
        print(f"  Copied (no translation needed): {copied}")
        print(f"  Skipped (already exists): {skipped}")
        print(f"  Errors: {errors}")
        print(f"  Output directory: {output_base}")
        print(f"{'='*60}\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Translate text in course images using Gemini API. "
            "Use --classify-only to generate the image manifest, "
            "then run without it to translate images."
        ),
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        help="Target language code(s) (e.g., en es fr). Required unless --classify-only.",
    )
    parser.add_argument(
        "--classify-only",
        action="store_true",
        help="Only classify images and generate manifest (no translation).",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST_PATH),
        help=f"Path to image manifest JSON. Default: {DEFAULT_MANIFEST_PATH}",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of images to process in a batch (for progress display). Default: 5",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip images that already have translated versions.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including prompts and API responses.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making any API calls or file changes.",
    )

    args = parser.parse_args()
    manifest_path = Path(args.manifest)

    # バリデーション
    if not args.classify_only and not args.lang:
        parser.error("--lang is required unless --classify-only is specified.")

    # dry-run 以外では API クライアントが必要
    client = None
    if not args.dry_run:
        client = require_gemini_client()

    # 画像ディレクトリの存在確認
    if not IMAGES_DIR.exists():
        print(f"ERROR: Images directory not found: {IMAGES_DIR}")
        sys.exit(1)

    if args.classify_only:
        # 分類モード
        print(f"Mode: Classification only")
        print(f"Images directory: {IMAGES_DIR}")
        print(f"Manifest output: {manifest_path}")
        classify_images(
            client=client,
            images_dir=IMAGES_DIR,
            manifest_path=manifest_path,
            batch_size=args.batch_size,
            verbose=args.verbose,
            dry_run=args.dry_run,
        )
    else:
        # 翻訳モード
        if args.dry_run:
            # dry-run ではマニフェストが無くてもスキャンで代用
            if manifest_path.exists():
                manifest = load_manifest(manifest_path)
            else:
                print(
                    "WARNING: Manifest not found. "
                    "In dry-run mode, listing all images as needing classification."
                )
                image_paths = scan_images(IMAGES_DIR)
                manifest = {
                    p: {
                        "category": "unknown",
                        "texts": [],
                        "needs_translation": True,
                    }
                    for p in image_paths
                }
        else:
            # マニフェストが無ければ自動生成
            if not manifest_path.exists():
                print(
                    "Manifest not found. Running classification first...\n"
                )
                manifest = classify_images(
                    client=client,
                    images_dir=IMAGES_DIR,
                    manifest_path=manifest_path,
                    batch_size=args.batch_size,
                    verbose=args.verbose,
                    dry_run=False,
                )
            else:
                manifest = load_manifest(manifest_path)

        lang_names = [
            f"{get_language_name(l)} ({l})" for l in args.lang
        ]
        print(f"Mode: Translation")
        print(f"Target languages: {', '.join(lang_names)}")
        print(f"Manifest: {manifest_path}")
        print(f"Total images in manifest: {len(manifest)}")
        if args.skip_existing:
            print(f"Skipping existing translations: yes")

        translate_images(
            client=client,
            manifest=manifest,
            images_dir=IMAGES_DIR,
            languages=args.lang,
            batch_size=args.batch_size,
            skip_existing=args.skip_existing,
            verbose=args.verbose,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
