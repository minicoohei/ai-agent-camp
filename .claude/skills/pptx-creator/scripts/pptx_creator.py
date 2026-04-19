#!/usr/bin/env python3
"""
pptx_creator.py — メインCLI: トピック/アウトラインから PPTX を生成

Usage:
  # トピックから生成
  python pptx_creator.py --topic "AI活用提案" --template simple -o output.pptx

  # 既存アウトラインから生成
  python pptx_creator.py --outline outline.yaml --template standard -o deck.pptx

  # アウトラインのみ生成（ドライラン）
  python pptx_creator.py --topic "Q1報告" --dry-run --save-outline outline.yaml

  # 生成 + 画像エクスポート + 品質検証
  python pptx_creator.py --topic "AI活用提案" --template simple --verify
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Ensure scripts/ is on path for sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from outline_generator import generate_outline, save_outline, load_outline
from template_engine import build_presentation, load_catalog


def _run_verify(pptx_path, threshold=7.0):
    """画像エクスポート + 品質検証"""
    from export_to_images import export_pptx_to_images
    from quality_reviewer import review_all_slides

    pptx_path = Path(pptx_path)
    images_dir = pptx_path.parent / f"{pptx_path.stem}_review"

    print("\n[verify] 画像エクスポート中...")
    try:
        images = export_pptx_to_images(pptx_path, images_dir)
        print(f"[verify] {len(images)} 枚の画像を生成")
    except Exception as e:
        print(f"[verify] 画像エクスポート失敗: {e}", file=sys.stderr)
        print("[verify] LibreOffice がインストールされていない可能性があります。", file=sys.stderr)
        print("[verify] sudo apt install libreoffice poppler-utils", file=sys.stderr)
        return None

    print("\n[verify] 品質レビュー中...")
    result = review_all_slides(str(images_dir), threshold)

    # Save review result
    import json
    review_path = pptx_path.parent / f"{pptx_path.stem}_review.json"
    with open(review_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[verify] レビュー結果: {review_path}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="PPTX Creator — トピックからプレゼンテーションを自動生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # トピックから8枚スライド生成
  python pptx_creator.py --topic "AI活用提案" --template simple

  # 12枚、英語、経営層向け
  python pptx_creator.py --topic "Q1 Report" --slides 12 --language en --audience executives

  # アウトラインだけ生成（テンプレート不要）
  python pptx_creator.py --topic "新規事業計画" --dry-run --save-outline plan.yaml

  # 生成 + 品質検証
  python pptx_creator.py --topic "AI活用提案" --template simple --verify
        """,
    )

    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--topic", type=str, help="プレゼンのトピック（Geminiでアウトライン生成）")
    input_group.add_argument("--outline", type=str, help="既存アウトラインYAMLファイルパス")

    # Template
    parser.add_argument(
        "--template", "-t", type=str, default="simple",
        choices=["simple", "standard"],
        help="テンプレート名 (default: simple)",
    )

    # Output
    parser.add_argument("--output", "-o", type=str, default=None, help="出力PPTXファイルパス")

    # Outline generation options
    parser.add_argument("--slides", "-n", type=int, default=8, help="スライド枚数 (default: 8)")
    parser.add_argument("--audience", type=str, default="business", help="対象聴衆 (default: business)")
    parser.add_argument("--language", "-l", type=str, default="ja", choices=["ja", "en"], help="出力言語 (default: ja)")

    # Outline save/dry-run
    parser.add_argument("--save-outline", type=str, default=None, help="アウトラインをYAMLファイルに保存")
    parser.add_argument("--dry-run", action="store_true", help="アウトライン生成のみ（PPTX生成しない）")

    # Verify
    parser.add_argument("--verify", action="store_true", help="生成後に画像エクスポート + 品質検証")
    parser.add_argument("--verify-threshold", type=float, default=7.0, help="品質検証の合格スコア閾値 (default: 7.0)")

    args = parser.parse_args()

    # --- Resolve outline ---
    if args.topic:
        print(f"\n{'='*60}")
        print("PPTX Creator v2")
        print(f"{'='*60}")
        print(f"トピック: {args.topic}")
        print(f"スライド数: {args.slides}")
        print(f"言語: {args.language}")
        print(f"テンプレート: {args.template}")
        if args.verify:
            print(f"品質検証: ON (threshold={args.verify_threshold})")
        print(f"{'='*60}\n")

        print("[1/3] アウトライン生成中...")
        outline = generate_outline(
            topic=args.topic,
            slides_count=args.slides,
            audience=args.audience,
            language=args.language,
        )
        print(f"  → {len(outline.get('slides', []))} スライドのアウトラインを生成")

        for s in outline.get("slides", []):
            st = s.get("slide_type", "?")
            title = s.get("title", "")
            print(f"  [{s.get('slide_number', '?'):2d}] {st:15s} | {title}")

        if args.save_outline:
            save_outline(outline, args.save_outline)

    else:
        print(f"\n[1/3] アウトラインを読み込み中: {args.outline}")
        outline = load_outline(args.outline)
        print(f"  → {len(outline.get('slides', []))} スライド")

    # --- Dry run? ---
    if args.dry_run:
        print("\n[dry-run] アウトライン生成のみ。PPTX は生成しません。")
        if not args.save_outline:
            import yaml
            print("\n--- アウトライン YAML ---")
            print(yaml.dump(outline, allow_unicode=True, default_flow_style=False, sort_keys=False))
        print("完了!")
        return

    # --- Resolve output path ---
    if args.output:
        output_path = args.output
    else:
        catalog = load_catalog()
        output_dir = catalog.get("defaults", {}).get("output_dir", "output/slides")
        project_root = Path(__file__).resolve().parents[3]
        out_dir = project_root / output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = outline.get("title", "presentation").replace(" ", "_")[:30]
        output_path = str(out_dir / f"{safe_title}_{timestamp}.pptx")

    # --- Build PPTX ---
    print(f"\n[2/3] PPTX 生成中... (template: {args.template})")
    try:
        result_path = build_presentation(
            outline=outline,
            template_name=args.template,
            output_path=output_path,
        )
    except FileNotFoundError as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("\nテンプレートPPTXを配置してください:", file=sys.stderr)
        print("  simple:   skills/pptx-creator/templates/simple/template.pptx", file=sys.stderr)
        print("  standard: skills/pptx-creator/templates/standard/template.pptx", file=sys.stderr)
        sys.exit(1)

    # --- Done ---
    print(f"\n[3/3] 完了!")
    print(f"{'='*60}")
    print(f"出力ファイル: {result_path}")
    print(f"スライド数:   {len(outline.get('slides', []))}")
    print(f"テンプレート: {args.template}")
    print(f"{'='*60}\n")

    # --- Verify ---
    if args.verify:
        verify_result = _run_verify(result_path, args.verify_threshold)
        if verify_result and not verify_result["passed"]:
            print(f"\n[verify] 品質基準未達 (avg: {verify_result['average_score']}/10)")
            print("[verify] 改善が必要なスライドがあります。レビュー結果を確認してください。")
            sys.exit(2)
        elif verify_result:
            print(f"\n[verify] 品質チェック合格 (avg: {verify_result['average_score']}/10)")


if __name__ == "__main__":
    main()
