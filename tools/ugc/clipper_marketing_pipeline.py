#!/usr/bin/env python3
"""
clipper_marketing_pipeline.py - Clipper × Remotion 統合パイプライン

YouTube URL → Clipper → ハイライト選択 → Remotion → SNS素材

Usage:
    python clipper_marketing_pipeline.py --url "https://youtube.com/watch?v=xxx"
    python clipper_marketing_pipeline.py --url "..." --batch-render short,quote
    python clipper_marketing_pipeline.py --url "..." --auto-select "score>0.8" --batch-render short,quote,summary
"""

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# パス設定
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(__file__).resolve().parents[2]
CLIPPER_DIR = ROOT_DIR / ".claude" / "skills" / "youtube-clipper" / "scripts"

sys.path.insert(0, str(CLIPPER_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from remotion_render import render_video, batch_render, TEMPLATES


def run_pipeline(
    url: str = None,
    file_path: str = None,
    output_base: str = "output/clips",
    resolution: int = 1080,
    target_lang: str = "ja",
    burn_subtitles: bool = False,
    auto_select: str = None,
    batch_templates: list = None,
    brand: str = "cursorbootcamp",
) -> dict:
    """統合パイプライン実行"""
    try:
        return _run_pipeline_inner(
            url=url, file_path=file_path, output_base=output_base,
            resolution=resolution, target_lang=target_lang,
            burn_subtitles=burn_subtitles, auto_select=auto_select,
            batch_templates=batch_templates, brand=brand,
        )
    except Exception:
        logger.exception("パイプライン実行中にエラーが発生しました")
        raise


def _run_pipeline_inner(
    url: str = None,
    file_path: str = None,
    output_base: str = "output/clips",
    resolution: int = 1080,
    target_lang: str = "ja",
    burn_subtitles: bool = False,
    auto_select: str = None,
    batch_templates: list = None,
    brand: str = "cursorbootcamp",
) -> dict:
    """統合パイプライン内部実装"""
    # Clipperインポート（遅延）
    from clipper import run_clipper

    # === Phase 1: Clipper ===
    logger.info("Phase 1: YouTube Clipper — 動画ハイライト抽出")
    print("\n" + "=" * 70)
    print("  PHASE 1: YouTube Clipper — 動画ハイライト抽出")
    print("=" * 70)

    clipper_result = run_clipper(
        url=url,
        file_path=file_path,
        output_base=output_base,
        resolution=resolution,
        target_lang=target_lang,
        burn_subtitles=burn_subtitles,
        auto_select=auto_select,
    )

    if not clipper_result.get("clips"):
        logger.warning("クリップが生成されませんでした")
        print("\n  クリップが生成されませんでした。")
        return clipper_result

    # === Phase 2: Remotion レンダリング ===
    if batch_templates:
        logger.info("Phase 2: Remotion — マーケ素材レンダリング (templates=%s)", batch_templates)
        print("\n" + "=" * 70)
        print("  PHASE 2: Remotion — マーケ素材レンダリング")
        print("=" * 70)

        remotion_input = Path(clipper_result["remotion_input_path"])
        render_results = []

        for clip in clipper_result["clips"]:
            clip_id = clip["clip_id"]
            print(f"\n  [{clip_id}] {clip['summary']['title']}")

            results = batch_render(
                remotion_input,
                batch_templates,
                clip_id=clip_id,
                brand=brand,
            )
            render_results.extend(results)

            for r in results:
                status = "OK" if r["status"] == "ok" else "ERROR"
                print(f"    {r['template']:10s} [{status}] {r.get('path', r.get('error', ''))}")

        clipper_result["marketing_renders"] = render_results

        # SNS投稿ドラフト生成
        session_dir = Path(clipper_result["session_dir"])
        drafts = generate_post_drafts(clipper_result, batch_templates)
        drafts_path = session_dir / "post_drafts.json"
        drafts_path.write_text(
            json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        clipper_result["post_drafts_path"] = str(drafts_path)

    # === 完了サマリー ===
    print("\n" + "=" * 70)
    print("  完了サマリー")
    print("=" * 70)
    print(f"  セッション: {clipper_result['session_dir']}")
    print(f"  クリップ数: {len(clipper_result['clips'])}")
    if batch_templates:
        ok = sum(1 for r in render_results if r["status"] == "ok")
        print(f"  レンダリング: {ok}/{len(render_results)} 成功")
        print(f"  SNS投稿ドラフト: {clipper_result.get('post_drafts_path', 'N/A')}")
    logger.info("パイプライン完了: clips=%d", len(clipper_result["clips"]))

    return clipper_result


def generate_post_drafts(result: dict, templates: list) -> list:
    """各クリップ×テンプレートのSNS投稿ドラフトを生成"""
    drafts = []
    metadata = result.get("metadata", {})
    source_title = metadata.get("title", "")

    platform_map = {
        "short": ["tiktok", "instagram_reels", "youtube_shorts"],
        "quote": ["twitter", "linkedin"],
        "summary": ["youtube", "blog"],
        "blog": ["blog"],
        "training": ["internal"],
        "square": ["instagram_feed"],
    }

    for clip in result.get("clips", []):
        summary = clip.get("summary", {})
        title = summary.get("title", "")
        desc = summary.get("summary", "")
        keywords = summary.get("keywords", [])
        hashtags = [f"#{kw}" for kw in keywords[:5]]

        for tmpl in templates:
            platforms = platform_map.get(tmpl, [tmpl])
            for platform in platforms:
                draft = {
                    "clip_id": clip["clip_id"],
                    "template": tmpl,
                    "platform": platform,
                    "title": title,
                    "text": f"{title}\n\n{desc[:200]}",
                    "hashtags": hashtags + ["#CursorBootcamp"],
                    "source": source_title,
                    "source_url": metadata.get("url", ""),
                }
                drafts.append(draft)

    return drafts


def main():
    parser = argparse.ArgumentParser(
        description="Clipper × Remotion 統合パイプライン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # YouTube動画からSNSショート動画を自動生成
  python clipper_marketing_pipeline.py \\
    --url "https://youtube.com/watch?v=xxx" \\
    --auto-select "score>0.8" \\
    --batch-render short,quote

  # 全テンプレートでバッチレンダリング
  python clipper_marketing_pipeline.py \\
    --url "..." \\
    --auto-select all \\
    --batch-render short,quote,summary,blog,training
        """,
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="動画URL")
    source.add_argument("--file", help="ローカル動画ファイル")

    parser.add_argument("-o", "--output", default="output/clips", help="出力ベースディレクトリ")
    parser.add_argument("-r", "--resolution", type=int, default=1080)
    parser.add_argument("--target-lang", default="ja")
    parser.add_argument("--burn-subtitles", action="store_true")
    parser.add_argument("--auto-select", default=None, help='自動選択 ("all", "score>0.8")')
    parser.add_argument("--batch-render", default=None, help="テンプレート (short,quote,summary)")
    parser.add_argument("--brand", default="cursorbootcamp")

    args = parser.parse_args()

    batch_templates = None
    if args.batch_render:
        batch_templates = [t.strip() for t in args.batch_render.split(",")]

    result = run_pipeline(
        url=args.url,
        file_path=args.file,
        output_base=args.output,
        resolution=args.resolution,
        target_lang=args.target_lang,
        burn_subtitles=args.burn_subtitles,
        auto_select=args.auto_select,
        batch_templates=batch_templates,
        brand=args.brand,
    )

    print("\n--- Result JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
