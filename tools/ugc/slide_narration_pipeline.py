#!/usr/bin/env python3
"""
Slide Narration Pipeline - スライド解説動画を生成

HTML/スライド画像 → Remotion風アニメーション → TTS音声 → プレゼンター合成

既存の lecture_video/generate_lecture.py をベースに、
スライド解説動画に特化したパイプラインを提供する。

使用例:
    # HTMLから自動生成
    python -m ugc.slide_narration_pipeline \
        --html https://ai-agent.camp/ja/course/module-1 \
        --engine fabric --resolution 720p

    # スライド画像から生成
    python -m ugc.slide_narration_pipeline \
        --slides ./slides/ \
        --topic "AIエージェント入門" \
        --engine kling

    # 台本のみ生成（動画なし）
    python -m ugc.slide_narration_pipeline \
        --html https://ai-agent.camp/ja/course/module-1 \
        --script-only
"""

import argparse
import json
import os
import subprocess
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

_tools_dir = Path(__file__).resolve().parent.parent  # tools/
sys.path.insert(0, str(_tools_dir))

from runtime_env import load_runtime_env

load_runtime_env(_tools_dir.parent)  # project root

def run_slide_narration(
    html_path: Optional[str] = None,
    slides_dir: Optional[str] = None,
    topic: str = "AI活用講座",
    engine_name: str = "fabric",
    resolution: str = "720p",
    voice: str = "default",
    style: str = "friendly",
    presenter_position: str = "right",
    script_only: bool = False,
    use_llm: bool = True,
    bgm_path: Optional[str] = None,
    bgm_volume: float = 0.12,
    output_dir: str = "output/ugc/slide_narration",
) -> dict:
    """スライド解説動画を生成

    Args:
        html_path: HTML教材ファイルパス
        slides_dir: スライド画像ディレクトリ（HTMLの代替）
        topic: トピック名（slides_dir使用時）
        engine_name: 動画エンジン（fabric, kling, veo）
        resolution: 解像度（720p, 1080p）
        voice: TTS音声
        style: 台本スタイル（friendly, formal, casual）
        presenter_position: プレゼンター位置（right, left, bottom）
        script_only: 台本のみ生成
        use_llm: LLMで台本生成
        bgm_path: BGMファイル
        bgm_volume: BGM音量
        output_dir: 出力先

    Returns:
        結果dict
    """
    from bootcamp_utils import get_client

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir) / timestamp
    out.mkdir(parents=True, exist_ok=True)

    total_cost = 0.0
    steps = []

    # ----- Step 1: コンテンツ解析 -----
    print(f"\n{'='*50}")
    print(f"Step 1: コンテンツ解析")

    if html_path:
        # HTMLから解析
        sys.path.insert(0, str(Path(__file__).parent / "lecture_video" / "scripts"))
        from html_parser import parse_html, content_to_dict
        content = parse_html(html_path)
        content_dict = content_to_dict(content)
        topic = content_dict.get("title", topic)
        print(f"  -> HTML解析完了: {topic}")
        print(f"  -> セクション数: {len(content_dict.get('sections', []))}")
    elif slides_dir:
        # スライド画像から構造生成
        slides = sorted(Path(slides_dir).glob("*.png")) + sorted(Path(slides_dir).glob("*.jpg"))
        content_dict = {
            "title": topic,
            "sections": [
                {
                    "title": f"スライド {i+1}",
                    "text": "",
                    "slide_image": str(s),
                    "content_type": "content",
                    "duration": 30,
                }
                for i, s in enumerate(slides)
            ],
        }
        print(f"  -> スライド画像: {len(slides)}枚")
    else:
        raise ValueError("--html または --slides のいずれかを指定してください")

    steps.append({"step": "parse", "topic": topic, "sections": len(content_dict.get("sections", []))})

    # ----- Step 2: 台本生成 -----
    print(f"\nStep 2: 台本生成 (style={style})")

    client = get_client()

    if use_llm and client:
        # Gemini で自然な台本を生成
        sections_text = json.dumps(content_dict.get("sections", []), ensure_ascii=False, indent=2)
        if len(sections_text) > 3000:
            print(f"  注意: セクション情報を3000文字に切り詰めました（元: {len(sections_text)}文字）")
        script_prompt = f"""以下のスライド内容について、{style}な話し言葉で解説台本を作成してください。

トピック: {topic}

セクション情報:
{sections_text[:3000]}

各セクションについて以下をJSON配列で返してください:
- section_title: セクション名
- narration: ナレーションテキスト（自然な話し言葉、30-60秒分）
- duration: 推定秒数
- visual_notes: スライドの視覚的要素メモ

JSONのみを返してください（```json等は不要）。"""

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=script_prompt,
        )
        try:
            script_text = response.text.strip()
            if script_text.startswith("```"):
                script_text = script_text.split("\n", 1)[1].rsplit("```", 1)[0]
            script_segments = json.loads(script_text)
        except Exception as e:
            print(f"  Warning: LLM台本生成失敗、フォールバック: {e}")
            script_segments = [
                {"section_title": s.get("title", f"Section {i+1}"),
                 "narration": s.get("text", "この部分について解説します。"),
                 "duration": s.get("duration", 30),
                 "visual_notes": ""}
                for i, s in enumerate(content_dict.get("sections", []))
            ]
    else:
        sys.path.insert(0, str(Path(__file__).parent / "lecture_video" / "scripts"))
        from script_generator import generate_script
        script_obj = generate_script(content_dict, style)
        script_segments = [
            {"section_title": seg.section_title,
             "narration": seg.narration,
             "duration": seg.duration,
             "visual_notes": seg.visual_notes}
            for seg in script_obj.segments
        ]

    script_path = out / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_segments, f, ensure_ascii=False, indent=2)

    # テキスト版も保存
    with open(out / "script.txt", "w", encoding="utf-8") as f:
        for seg in script_segments:
            f.write(f"## {seg['section_title']}\n")
            f.write(f"{seg['narration']}\n\n")

    steps.append({"step": "script", "segments": len(script_segments)})
    print(f"  -> {len(script_segments)}セグメントの台本生成完了")

    if script_only:
        summary = {
            "topic": topic,
            "style": style,
            "script_path": str(script_path),
            "segments": len(script_segments),
            "timestamp": timestamp,
            "steps": steps,
        }
        with open(out / "summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\n台本のみ生成完了: {script_path}")
        return summary

    # ----- Step 3: TTS音声生成 (narration-qa 統合) -----
    print(f"\nStep 3: TTS音声生成 (ElevenLabs + narration-qa)")

    from ugc.narration_qa import qa_and_retry

    audio_paths = []
    for i, seg in enumerate(script_segments):
        audio_path = str(out / f"audio_{i:03d}.mp3")
        try:
            audio_path = qa_and_retry(
                text=seg["narration"],
                output_path=audio_path,
                voice=voice,
            )
            audio_paths.append(audio_path)
            print(f"  -> Audio {i+1}/{len(script_segments)}: {audio_path}")
        except Exception as e:
            print(f"  -> Audio {i+1} failed: {e}")

    steps.append({"step": "tts", "count": len(audio_paths)})

    # ----- Step 4: プレゼンター動画生成 -----
    print(f"\nStep 4: プレゼンター動画生成 ({engine_name})")

    from ugc.engines import get_engine, generate_with_fallback
    from ugc.video_qa import validate_video_output
    from nanobanana import generate_image as gen_img

    # アバター画像生成
    avatar_path = str(out / "avatar.png")
    try:
        gen_img(
            client=client,
            prompt="Professional Japanese female presenter, business casual, friendly smile, upper body, plain background, high quality photo",
            output_path=avatar_path,
            aspect_ratio="9:16",
        )
        print(f"  -> Avatar: {avatar_path}")
    except Exception as e:
        print(f"  -> Avatar generation failed: {e}")
        avatar_path = None

    presenter_clips = []
    for i, audio_path in enumerate(audio_paths):
        clip_path = str(out / f"presenter_{i:03d}.mp4")
        if avatar_path:
            try:
                result = generate_with_fallback(
                    engine_name=engine_name,
                    avatar_image=avatar_path,
                    script=script_segments[i]["narration"] if i < len(script_segments) else "",
                    audio_file=audio_path,
                    output_path=clip_path,
                )
                total_cost += result.cost
                presenter_clips.append(clip_path)
                print(f"  -> Presenter {i+1}: ${result.cost:.2f} (engine={result.engine})")
            except Exception as e:
                print(f"  -> Presenter {i+1} failed: {e}")
        else:
            print(f"  -> Presenter {i+1} skipped (no avatar)")

    steps.append({"step": "presenter", "count": len(presenter_clips), "cost": total_cost})

    # ----- Step 5: スライド画像生成（HTMLからの場合） -----
    print(f"\nStep 5: スライド画像生成")

    slide_images = []
    if slides_dir:
        slide_images = [str(s) for s in sorted(Path(slides_dir).glob("*.png")) + sorted(Path(slides_dir).glob("*.jpg"))]
    else:
        # HTMLからスライド画像を生成
        for i, seg in enumerate(script_segments):
            slide_path = str(out / f"slide_{i:03d}.png")
            title = seg.get("section_title", f"Section {i+1}")
            notes = seg.get("visual_notes", "")
            try:
                gen_img(
                    client=client,
                    prompt=f"Clean presentation slide design, title: '{title}', {notes}, modern minimalist style, white background, professional typography, 16:9",
                    output_path=slide_path,
                    aspect_ratio="16:9",
                )
                slide_images.append(slide_path)
                print(f"  -> Slide {i+1}: {slide_path}")
            except Exception as e:
                print(f"  -> Slide {i+1} failed: {e}")

    steps.append({"step": "slides", "count": len(slide_images)})

    # ----- Step 6: 最終合成 -----
    print(f"\nStep 6: 最終合成")
    final_path = str(out / "final.mp4")

    if presenter_clips:
        # プレゼンタークリップを結合
        from ugc.video_concat import concat_simple
        joined_presenter = str(out / "presenter_joined.mp4")
        if len(presenter_clips) >= 2:
            concat_simple(presenter_clips, joined_presenter)
        elif presenter_clips:
            shutil.copy2(presenter_clips[0], joined_presenter)

        # スライド画像がある場合はオーバーレイ合成
        if slide_images:
            # スライド画像からKen Burnsで背景動画を作成
            from ugc.ken_burns import generate_broll
            from ugc.video_concat import concat_with_crossfade

            bg_clips = []
            for i, img in enumerate(slide_images):
                bg_clip = str(out / f"bg_{i:03d}.mp4")
                duration = script_segments[i].get("duration", 30) if i < len(script_segments) else 30
                generate_broll(img, bg_clip, duration=duration, effect="slow_zoom")
                bg_clips.append(bg_clip)

            bg_joined = str(out / "bg_joined.mp4")
            if len(bg_clips) >= 2:
                try:
                    concat_with_crossfade(bg_clips, bg_joined, transition="fade", transition_duration=0.5)
                except Exception:
                    concat_simple(bg_clips, bg_joined)
            elif bg_clips:
                shutil.copy2(bg_clips[0], bg_joined)

            # プレゼンターを右下にオーバーレイ
            if shutil.which("ffmpeg"):
                pos_map = {
                    "right": "overlay=W-w-20:H-h-20",
                    "left": "overlay=20:H-h-20",
                    "bottom": "overlay=(W-w)/2:H-h-20",
                }
                overlay_filter = pos_map.get(presenter_position, pos_map["right"])
                cmd = [
                    "ffmpeg", "-y",
                    "-i", bg_joined,
                    "-i", joined_presenter,
                    "-filter_complex",
                    f"[1:v]scale=iw/3:ih/3[pip];[0:v][pip]{overlay_filter}[v]",
                    "-map", "[v]", "-map", "1:a?",
                    "-c:v", "libx264", "-preset", "fast",
                    "-c:a", "aac",
                    "-shortest",
                    final_path,
                ]
                try:
                    subprocess.run(cmd, check=True)
                    print(f"  -> Composited: {final_path}")
                except Exception as e:
                    print(f"  -> Composite failed, using presenter only: {e}")
                    shutil.copy2(joined_presenter, final_path)
            else:
                shutil.copy2(joined_presenter, final_path)
        else:
            shutil.copy2(joined_presenter, final_path)
    else:
        print("  -> プレゼンタークリップなし")
        # スライドのみの場合
        if slide_images:
            from ugc.ken_burns import generate_broll
            from ugc.video_concat import concat_simple as cs
            bg_clips = []
            for i, img in enumerate(slide_images):
                bg_clip = str(out / f"bg_{i:03d}.mp4")
                generate_broll(img, bg_clip, duration=30, effect="slow_zoom")
                bg_clips.append(bg_clip)
            if bg_clips:
                cs(bg_clips, final_path)

    # ----- BGM追加 -----
    if bgm_path and Path(bgm_path).exists():
        print(f"\nStep 7: BGM追加")
        from ugc.audio_post import mix_bgm
        final_with_bgm = str(out / "final_with_bgm.mp4")
        try:
            mix_bgm(final_path, bgm_path, final_with_bgm, bgm_volume=bgm_volume)
            final_path = final_with_bgm
            print(f"  -> {final_path}")
        except Exception as e:
            print(f"  -> BGMスキップ: {e}")

    steps.append({"step": "final", "path": final_path})

    # ----- QA検証 -----
    print(f"\nQA検証:")
    qa_result = validate_video_output(final_path, expect_audio=bool(audio_paths))
    steps.append({"step": "qa", "result": qa_result})

    # ----- Summary -----
    summary = {
        "topic": topic,
        "engine": engine_name,
        "resolution": resolution,
        "style": style,
        "segments": len(script_segments),
        "presenter_clips": len(presenter_clips),
        "slide_images": len(slide_images),
        "video_path": final_path,
        "total_cost": total_cost,
        "timestamp": timestamp,
        "steps": steps,
    }

    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Slide Narration Pipeline Complete!")
    print(f"  Video: {final_path}")
    print(f"  Segments: {len(script_segments)}")
    print(f"  Cost: ${total_cost:.2f}")
    print(f"  Output: {out}")
    print(f"{'='*50}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Slide Narration Pipeline")
    parser.add_argument("--html", help="HTML教材ファイルパス")
    parser.add_argument("--slides", help="スライド画像ディレクトリ")
    parser.add_argument("--topic", "-t", default="AI活用講座", help="トピック名")
    parser.add_argument("--engine", "-e", default="fabric", choices=["fabric", "kling", "veo"])
    parser.add_argument("--resolution", default="720p", choices=["720p", "1080p"])
    parser.add_argument("--voice", default="default")
    parser.add_argument("--style", default="friendly", choices=["friendly", "formal", "casual"])
    parser.add_argument("--presenter-position", default="right", choices=["right", "left", "bottom"])
    parser.add_argument("--script-only", action="store_true", help="台本のみ生成")
    parser.add_argument("--no-llm", action="store_true", help="LLM台本生成を無効化")
    parser.add_argument("--bgm", help="BGMファイルパス")
    parser.add_argument("--bgm-volume", type=float, default=0.12)
    parser.add_argument("--output-dir", "-o", default="output/ugc/slide_narration")

    args = parser.parse_args()

    if not args.html and not args.slides:
        parser.error("--html または --slides のいずれかを指定してください")

    run_slide_narration(
        html_path=args.html,
        slides_dir=args.slides,
        topic=args.topic,
        engine_name=args.engine,
        resolution=args.resolution,
        voice=args.voice,
        style=args.style,
        presenter_position=args.presenter_position,
        script_only=args.script_only,
        use_llm=not args.no_llm,
        bgm_path=args.bgm,
        bgm_volume=args.bgm_volume,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
