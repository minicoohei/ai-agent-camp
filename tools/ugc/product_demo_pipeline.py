#!/usr/bin/env python3
"""
Product Demo Pipeline - プロダクト紹介動画の簡易パイプライン

ugc_factory.py のロジックを簡略化し、BGM追加機能を付加したラッパー。
グリーンスクリーンのスマホにアプリスクショを合成した紹介動画を生成する。

使用例:
    # 基本（Fabricエンジン）
    python -m ugc.product_demo_pipeline \
        --product "AI研修プラットフォーム" \
        --screenshot ./app.png

    # Klingエンジン + BGM付き
    python -m ugc.product_demo_pipeline \
        --product "タスク管理アプリ" \
        --screenshot ./app.png \
        --engine kling --bgm ./assets/bgm/upbeat.mp3

    # 既存アバター画像を使用
    python -m ugc.product_demo_pipeline \
        --product "ECサイト" \
        --screenshot ./app.png \
        --avatar ./my_avatar.png
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

_tools_dir = Path(__file__).resolve().parent.parent  # tools/
sys.path.insert(0, str(_tools_dir))

from runtime_env import load_runtime_env

load_runtime_env(_tools_dir.parent)  # project root



def run_product_demo(
    product: str,
    screenshot_path: str,
    engine_name: str = "fabric",
    platform: str = "tiktok",
    duration: int = 30,
    voice: str = "default",
    resolution: str = "480p",
    avatar_path: Optional[str] = None,
    bgm_path: Optional[str] = None,
    bgm_volume: float = 0.15,
    output_dir: str = "output/ugc/product_demo",
) -> dict:
    """プロダクト紹介動画を生成

    Args:
        product: 製品名
        screenshot_path: アプリのスクリーンショット
        engine_name: 動画エンジン（fabric, kling, veo, longcat）
        platform: ターゲット（tiktok, youtube_shorts, instagram）
        duration: 動画の長さ（秒）
        voice: 音声プリセット
        resolution: 解像度（480p, 720p）
        avatar_path: 既存アバター画像（省略時は自動生成）
        bgm_path: BGMファイルパス（省略時はBGMなし）
        bgm_volume: BGMの音量（0.0-1.0）
        output_dir: 出力先ディレクトリ

    Returns:
        結果のdict（video_path, cost, duration等）
    """
    from ugc import generate_ugc_script, generate_speech, composite_video
    from ugc.engines import get_engine
    from ugc.audio_post import mux_audio, mix_bgm

    # 出力ディレクトリ
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir) / timestamp
    out.mkdir(parents=True, exist_ok=True)

    total_cost = 0.0
    steps_log = []

    # ----- Step 1: 台本生成 -----
    print(f"\n{'='*50}")
    print(f"Step 1/6: 台本生成 ({product})")
    topic = f"{product}の紹介。このアプリ/サービスの魅力を伝えるUGC動画の台本。"
    script = generate_ugc_script(
        topic=topic,
        platform=platform,
        duration=duration,
    )
    script_path = out / "script.txt"
    script_path.write_text(script, encoding="utf-8")
    steps_log.append({"step": "script", "path": str(script_path)})
    print(f"  -> {script_path}")

    # ----- Step 2: アバター画像 -----
    print(f"\nStep 2/6: アバター画像")
    if avatar_path and Path(avatar_path).exists():
        current_avatar = avatar_path
        print(f"  -> 既存画像を使用: {avatar_path}")
    else:
        current_avatar = str(out / "avatar.png")
        # ugc_factory.py の generate_avatar と同じロジック
        from nanobanana import generate_image as gen_img
        from bootcamp_utils import get_client
        client = get_client()
        if not client:
            raise EnvironmentError("GEMINI_API_KEY が設定されていません")

        avatar_prompt = (
            "A friendly young person in their 20s holding a smartphone toward the camera. "
            "The smartphone screen displays a solid bright green color (#00FF00) for chroma key. "
            "Natural enthusiastic expression, casual indoor setting with good lighting. "
            "The smartphone is clearly visible, showing the screen to the viewer. Realistic photo style."
        )
        try:
            gen_img(client=client, prompt=avatar_prompt, output_path=current_avatar, aspect_ratio="9:16")
        except Exception as e:
            raise RuntimeError(f"アバター画像の生成に失敗しました: {e}") from e
        print(f"  -> 生成完了: {current_avatar}")
    steps_log.append({"step": "avatar", "path": current_avatar})

    # ----- Step 3: TTS音声生成 -----
    engine = get_engine(engine_name)
    audio_path = None

    if engine.requires_tts:
        print(f"\nStep 3/6: TTS音声生成 (ElevenLabs)")
        audio_path = str(out / "speech.mp3")
        generate_speech(text=script, output_path=audio_path, voice=voice)
        steps_log.append({"step": "tts", "path": audio_path})
        print(f"  -> {audio_path}")
    else:
        print(f"\nStep 3/6: TTS スキップ ({engine_name}はネイティブ音声)")

    # ----- Step 4: 動画生成 -----
    print(f"\nStep 4/6: 動画生成 ({engine_name})")
    raw_video = str(out / "raw_video.mp4")

    kwargs = {
        "avatar_image": current_avatar,
        "script": script,
        "output_path": raw_video,
    }
    if audio_path:
        kwargs["audio_file"] = audio_path
    if engine_name == "kling":
        kwargs["duration"] = min(duration, 10)
    elif engine_name == "veo":
        kwargs["duration"] = min(duration, 8)
        kwargs["resolution"] = resolution
    else:
        kwargs["resolution"] = resolution

    result = engine.generate(**kwargs)
    total_cost += result.cost
    steps_log.append({"step": "video", "path": result.video_path, "cost": result.cost})
    print(f"  -> {result.video_path} (${result.cost:.2f})")

    # ----- Step 5: グリーンスクリーン合成 -----
    print(f"\nStep 5/6: グリーンスクリーン合成")
    composited_path = str(out / "composited.mp4")
    try:
        composite_video(
            video_path=result.video_path,
            screenshot_path=screenshot_path,
            output_path=composited_path,
            backend="ffmpeg",
        )
        current_video = composited_path
        print(f"  -> {composited_path}")
    except Exception as e:
        print(f"  -> 合成スキップ: {e}")
        current_video = result.video_path
    steps_log.append({"step": "composite", "path": current_video})

    # ----- Step 6: BGM追加（オプション） -----
    if bgm_path and Path(bgm_path).exists():
        print(f"\nStep 6/6: BGM追加")
        final_path = str(out / "final.mp4")
        try:
            mix_bgm(current_video, bgm_path, final_path, bgm_volume=bgm_volume)
            current_video = final_path
            print(f"  -> {final_path}")
        except Exception as e:
            print(f"  -> BGMスキップ: {e}")
    else:
        print(f"\nStep 6/6: BGMスキップ（ファイル未指定）")
        # 最終ファイル名を統一
        final_path = str(out / "final.mp4")
        import shutil
        shutil.copy2(current_video, final_path)
        current_video = final_path

    steps_log.append({"step": "final", "path": current_video})

    # ----- Result -----
    summary = {
        "product": product,
        "engine": engine_name,
        "video_path": current_video,
        "duration": result.duration,
        "cost": total_cost,
        "timestamp": timestamp,
        "steps": steps_log,
    }

    summary_path = out / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Product Demo Pipeline Complete!")
    print(f"  Video: {current_video}")
    print(f"  Duration: {result.duration:.1f}s")
    print(f"  Cost: ${total_cost:.2f}")
    print(f"  Output: {out}")
    print(f"{'='*50}")

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Product Demo Pipeline - プロダクト紹介動画生成",
    )
    parser.add_argument("--product", "-p", required=True, help="製品/サービス名")
    parser.add_argument("--screenshot", "-s", required=True, help="スクリーンショット画像")
    parser.add_argument("--engine", "-e", default="fabric",
                        choices=["fabric", "kling", "veo", "longcat"],
                        help="動画エンジン (default: fabric)")
    parser.add_argument("--platform", default="tiktok",
                        choices=["tiktok", "youtube_shorts", "instagram"])
    parser.add_argument("--duration", "-d", type=int, default=30)
    parser.add_argument("--voice", "-v", default="default")
    parser.add_argument("--resolution", "-r", default="480p", choices=["480p", "720p"])
    parser.add_argument("--avatar", "-a", help="既存アバター画像パス")
    parser.add_argument("--bgm", help="BGMファイルパス")
    parser.add_argument("--bgm-volume", type=float, default=0.15)
    parser.add_argument("--output-dir", "-o", default="output/ugc/product_demo")

    args = parser.parse_args()

    if not Path(args.screenshot).exists():
        print(f"Error: スクリーンショットが見つかりません: {args.screenshot}")
        sys.exit(1)

    run_product_demo(
        product=args.product,
        screenshot_path=args.screenshot,
        engine_name=args.engine,
        platform=args.platform,
        duration=args.duration,
        voice=args.voice,
        resolution=args.resolution,
        avatar_path=args.avatar,
        bgm_path=args.bgm,
        bgm_volume=args.bgm_volume,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
