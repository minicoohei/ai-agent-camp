#!/usr/bin/env python3
"""
quality_reviewer.py — Gemini Vision による PPTX スライド品質レビュー

各スライド画像を Gemini Vision API で分析し、プロフェッショナル品質チェックを実施。

Usage:
  python quality_reviewer.py slide_images_dir/
  python quality_reviewer.py slide_images_dir/ --threshold 7
"""

import argparse
import json
import sys
from pathlib import Path

# bootcamp_utils を tools/ から import
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))

REVIEW_PROMPT = """あなたはプロフェッショナルなコンサルティングファーム（McKinsey, BCG, Bain レベル）の
スライドデザインレビュアーです。以下の観点でこのスライド画像を評価してください。

## 評価項目（各10点満点）

1. **レイアウト** (layout_score): 余白バランス、要素配置の整合性、視線誘導
2. **タイポグラフィ** (typography_score): フォント統一性、サイズ階層、可読性
3. **色使い** (color_score): カラーパレット統一性、コントラスト、アクセント色の効果
4. **情報設計** (info_design_score): 1スライド1メッセージ原則、情報密度、構造化
5. **プロフェッショナル度** (professional_score): 全体の完成度、コンサルクオリティ

## 出力形式（JSON のみ）

```json
{
  "layout_score": 8,
  "typography_score": 7,
  "color_score": 9,
  "info_design_score": 8,
  "professional_score": 8,
  "overall_score": 8.0,
  "issues": ["具体的な問題点1", "問題点2"],
  "suggestions": ["改善提案1", "改善提案2"]
}
```

overall_score は5項目の平均値（小数点1桁）で計算してください。
JSON ブロック以外のテキストは出力しないでください。
"""


def review_slide(image_path, client, model):
    """1枚のスライド画像をレビュー"""
    import re

    image_path = Path(image_path)
    if not image_path.exists():
        return {"error": f"Image not found: {image_path}"}

    # 画像を読み込み
    with open(image_path, "rb") as f:
        image_data = f.read()

    import base64
    b64_image = base64.b64encode(image_data).decode("utf-8")

    # Determine mime type
    suffix = image_path.suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
    mime_type = mime_map.get(suffix, "image/png")

    response = client.models.generate_content(
        model=model,
        contents=[
            {
                "role": "user",
                "parts": [
                    {"inline_data": {"mime_type": mime_type, "data": b64_image}},
                    {"text": REVIEW_PROMPT},
                ],
            }
        ],
    )

    text = response.text
    # Extract JSON
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        json_text = text.strip()

    try:
        result = json.loads(json_text)
    except json.JSONDecodeError:
        result = {"error": f"JSON parse failed: {text[:200]}"}

    return result


def review_all_slides(images_dir, threshold=7.0):
    """ディレクトリ内の全スライド画像をレビュー"""
    try:
        from bootcamp_utils import get_client, get_flash_model
    except ImportError:
        raise RuntimeError("bootcamp_utils not found. GEMINI_API_KEY を設定してください。") from None

    client = get_client()
    if client is None:
        raise RuntimeError("GEMINI_API_KEY or GOOGLE_API_KEY が未設定です。") from None

    model = get_flash_model()
    images_dir = Path(images_dir)

    image_files = sorted(
        [f for f in images_dir.iterdir()
         if f.suffix.lower() in (".png", ".jpg", ".jpeg")]
    )

    if not image_files:
        print(f"画像ファイルが見つかりません: {images_dir}", file=sys.stderr)
        return {"passed": False, "reviews": [], "average_score": 0, "total_slides": 0, "failed_count": 0, "threshold": threshold, "summary": "No images found"}

    reviews = []
    total_score = 0.0
    failed_slides = []

    print(f"\n{'='*60}")
    print(f"スライド品質レビュー ({len(image_files)} 枚)")
    print(f"合格基準: overall_score >= {threshold}")
    print(f"{'='*60}\n")

    for i, img in enumerate(image_files):
        print(f"[{i+1}/{len(image_files)}] Reviewing: {img.name} ... ", end="", flush=True)
        try:
            result = review_slide(img, client, model)
            result["file"] = img.name
            score = result.get("overall_score", 0)
            total_score += score

            if score < threshold:
                failed_slides.append(result)
                print(f"FAIL ({score:.1f}/10)")
            else:
                print(f"PASS ({score:.1f}/10)")

            reviews.append(result)
        except Exception as e:
            print(f"ERROR: {e}")
            reviews.append({"file": img.name, "error": str(e)})

    avg_score = total_score / len(image_files) if image_files else 0
    passed = len(failed_slides) == 0

    print(f"\n{'='*60}")
    print(f"結果: {'PASS' if passed else 'FAIL'}")
    print(f"平均スコア: {avg_score:.1f}/10")
    print(f"不合格スライド: {len(failed_slides)}/{len(image_files)}")
    print(f"{'='*60}")

    if failed_slides:
        print("\n不合格スライドの詳細:")
        for r in failed_slides:
            print(f"\n  {r.get('file', '?')} (score: {r.get('overall_score', 0):.1f})")
            for issue in r.get("issues", []):
                print(f"    - {issue}")
            for suggestion in r.get("suggestions", []):
                print(f"    → {suggestion}")

    return {
        "passed": passed,
        "average_score": round(avg_score, 1),
        "total_slides": len(image_files),
        "failed_count": len(failed_slides),
        "threshold": threshold,
        "reviews": reviews,
    }


def main():
    parser = argparse.ArgumentParser(description="スライド品質レビュー（Gemini Vision）")
    parser.add_argument("images_dir", type=str, help="スライド画像ディレクトリ")
    parser.add_argument("--threshold", "-t", type=float, default=7.0,
                        help="合格スコア閾値 (default: 7.0)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="レビュー結果JSONの保存先")
    args = parser.parse_args()

    result = review_all_slides(args.images_dir, args.threshold)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nレビュー結果保存: {out_path}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
