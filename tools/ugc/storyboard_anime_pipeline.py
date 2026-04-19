#!/usr/bin/env python3
"""
Storyboard Anime Pipeline - 絵コンテからアニメ動画を生成

テキストシナリオ → 絵コンテ16フレーム → I2V動画化 → トランジション付き結合 → BGM追加

コスト最適化モード（--cost-optimize）:
  A-roll: 指定数のシーンのみI2V動画化（Kling/Veo）
  B-roll: 残りは Ken Burns 効果で擬似動画化（$0）

使用例:
    # 標準モード（全フレームI2V）
    python -m ugc.storyboard_anime_pipeline \
        --scenario "少女が魔法の森で冒険する物語" \
        --style anime --engine kling

    # コスト最適化（A-roll 4本 + B-roll 12本）
    python -m ugc.storyboard_anime_pipeline \
        --scenario "少女が魔法の森で冒険する物語" \
        --style anime --engine kling \
        --cost-optimize --aroll-count 4

    # BGM付き
    python -m ugc.storyboard_anime_pipeline \
        --scenario "カフェの日常" \
        --style modern_clean --engine kling \
        --bgm ./bgm.mp3
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

def run_storyboard_anime(
    scenario: str,
    style: str = "anime",
    engine_name: str = "kling",
    aspect_ratio: str = "16:9",
    character: Optional[str] = None,
    num_scenes: int = 8,
    clip_duration: int = 10,
    transition: str = "fade",
    transition_duration: float = 0.5,
    cost_optimize: bool = False,
    aroll_count: int = 4,
    bgm_path: Optional[str] = None,
    bgm_volume: float = 0.20,
    output_dir: str = "output/ugc/storyboard_anime",
) -> dict:
    """絵コンテアニメ動画を生成

    Args:
        scenario: ストーリーのテキスト
        style: ビジュアルスタイル（anime, modern_clean, vibrant_ugc, animal_crossing等）
        engine_name: I2Vエンジン（kling, veo）
        aspect_ratio: アスペクト比
        character: キャラクター説明（省略時はシナリオから推定）
        num_scenes: シーン数（デフォルト8）
        clip_duration: 各クリップの長さ（秒）
        transition: トランジション種類
        transition_duration: トランジション時間
        cost_optimize: コスト最適化モード（A-roll + B-roll）
        aroll_count: A-rollシーン数（cost_optimize時）
        bgm_path: BGMファイル
        bgm_volume: BGM音量
        output_dir: 出力先

    Returns:
        結果dict
    """
    from bootcamp_utils import get_client
    from ugc.engines import get_engine, generate_with_fallback
    from ugc.video_concat import concat_simple, concat_with_crossfade
    from ugc.audio_post import mix_bgm, mix_bgm_no_audio
    from ugc.ken_burns import generate_broll
    from ugc.video_qa import validate_video_output

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir) / timestamp
    out.mkdir(parents=True, exist_ok=True)
    frames_dir = out / "frames"
    clips_dir = out / "clips"
    frames_dir.mkdir(exist_ok=True)
    clips_dir.mkdir(exist_ok=True)

    client = get_client()
    if not client:
        raise EnvironmentError("GEMINI_API_KEY が設定されていません")

    total_cost = 0.0
    steps = []

    # ----- Step 1: シーン分解 -----
    print(f"\n{'='*50}")
    print(f"Step 1/{5 if not bgm_path else 6}: シーン分解 ({num_scenes}シーン)")

    scene_prompt = f"""以下のシナリオを{num_scenes}シーンに分解してください。
各シーンについて以下をJSON配列で返してください:
- scene_number: シーン番号
- description: シーンの視覚的な説明（英語、画像生成プロンプト向け）
- camera: カメラワーク（zoom_in, pan_left, pan_right, tilt_up, static等）
- mood: 雰囲気（calm, dramatic, energetic, mysterious等）
- is_key_scene: 重要シーンかどうか（true/false）

シナリオ: {scenario}

JSONのみを返してください（```json等は不要）。"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=scene_prompt,
    )

    try:
        scenes_text = response.text.strip()
        if scenes_text.startswith("```"):
            scenes_text = scenes_text.split("\n", 1)[1].rsplit("```", 1)[0]
        scenes = json.loads(scenes_text)
    except (json.JSONDecodeError, Exception) as e:
        print(f"  Warning: JSON解析失敗、デフォルトシーン生成: {e}")
        scenes = [
            {"scene_number": i + 1, "description": f"Scene {i+1} of the story",
             "camera": "static", "mood": "neutral", "is_key_scene": i < aroll_count}
            for i in range(num_scenes)
        ]

    scenes_path = out / "scenes.json"
    with open(scenes_path, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
    steps.append({"step": "scenes", "count": len(scenes)})
    print(f"  -> {len(scenes)}シーン分解完了")

    # ----- Step 2: フレーム画像生成 -----
    print(f"\nStep 2: フレーム画像生成 (Gemini Image)")

    frame_paths = []
    for i, scene in enumerate(scenes):
        frame_path = str(frames_dir / f"frame_{i:03d}.png")
        desc = scene.get("description", f"Scene {i+1}")
        mood = scene.get("mood", "neutral")

        img_prompt = f"{desc}. {style} style art, {mood} mood, high quality illustration"
        if character:
            img_prompt = f"{character}. {img_prompt}"

        try:
            from nanobanana import generate_image as gen_img
            gen_img(
                client=client,
                prompt=img_prompt,
                output_path=frame_path,
                aspect_ratio=aspect_ratio,
            )
            frame_paths.append(frame_path)
            print(f"  -> Frame {i+1}/{len(scenes)}: {frame_path}")
        except Exception as e:
            print(f"  -> Frame {i+1} failed: {e}")

    steps.append({"step": "frames", "count": len(frame_paths)})

    # ----- Step 3: A-roll / B-roll 分類 & 動画生成 -----
    print(f"\nStep 3: 動画クリップ生成")

    if cost_optimize:
        # A-roll: 重要シーンのみI2V
        key_scenes = [i for i, s in enumerate(scenes) if s.get("is_key_scene", False)]
        if len(key_scenes) < aroll_count:
            # 不足分は先頭から追加
            remaining = [i for i in range(len(scenes)) if i not in key_scenes]
            key_scenes.extend(remaining[:aroll_count - len(key_scenes)])
        key_scenes = sorted(key_scenes[:aroll_count])

        aroll_indices = set(key_scenes)
        print(f"  Cost-optimize ON: A-roll={len(aroll_indices)}本, B-roll={len(scenes)-len(aroll_indices)}本")
    else:
        aroll_indices = set(range(len(scenes)))
        print(f"  Full mode: 全{len(scenes)}本をI2V")

    clip_paths = []
    ken_burns_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right", "slow_zoom", "pan_down"]

    for i in range(len(frame_paths)):
        clip_path = str(clips_dir / f"clip_{i:03d}.mp4")

        if i in aroll_indices:
            # A-roll: I2V (with fallback)
            print(f"  [A-roll] Clip {i+1}: {engine_name} I2V...")
            try:
                result = generate_with_fallback(
                    engine_name=engine_name,
                    avatar_image=frame_paths[i],
                    script=scenes[i].get("description", ""),
                    output_path=clip_path,
                    duration=min(clip_duration, 10) if engine_name == "kling" else min(clip_duration, 8),
                )
                total_cost += result.cost
                clip_paths.append(clip_path)
                print(f"    -> ${result.cost:.2f} (engine={result.engine})")
            except Exception as e:
                print(f"    -> I2V failed, fallback to Ken Burns: {e}")
                effect = ken_burns_effects[i % len(ken_burns_effects)]
                generate_broll(frame_paths[i], clip_path, duration=clip_duration, effect=effect)
                clip_paths.append(clip_path)
        else:
            # B-roll: Ken Burns
            effect = ken_burns_effects[i % len(ken_burns_effects)]
            print(f"  [B-roll] Clip {i+1}: Ken Burns ({effect})")
            generate_broll(frame_paths[i], clip_path, duration=clip_duration, effect=effect)
            clip_paths.append(clip_path)

    steps.append({"step": "clips", "count": len(clip_paths), "cost": total_cost})

    # ----- Step 4: クリップ結合 -----
    print(f"\nStep 4: クリップ結合 (transition={transition})")
    joined_path = str(out / "joined.mp4")

    if len(clip_paths) >= 2:
        try:
            concat_with_crossfade(clip_paths, joined_path,
                                  transition=transition,
                                  transition_duration=transition_duration)
        except Exception as e:
            print(f"  xfade failed, fallback to simple concat: {e}")
            concat_simple(clip_paths, joined_path)
    elif clip_paths:
        import shutil
        shutil.copy2(clip_paths[0], joined_path)

    steps.append({"step": "concat", "path": joined_path})
    print(f"  -> {joined_path}")

    # ----- Step 5: BGM追加 -----
    final_path = str(out / "final.mp4")
    if bgm_path and Path(bgm_path).exists():
        print(f"\nStep 5: BGM追加")
        try:
            mix_bgm_no_audio(joined_path, bgm_path, final_path, bgm_volume=bgm_volume)
            print(f"  -> {final_path}")
        except Exception as e:
            print(f"  -> BGMスキップ: {e}")
            import shutil
            shutil.copy2(joined_path, final_path)
    else:
        import shutil
        shutil.copy2(joined_path, final_path)
        if bgm_path:
            print(f"\nStep 5: BGMスキップ（ファイルなし: {bgm_path}）")

    steps.append({"step": "final", "path": final_path})

    # ----- QA検証 -----
    print(f"\nQA検証:")
    expect_audio = bool(bgm_path and Path(bgm_path).exists())
    qa_result = validate_video_output(final_path, expect_audio=expect_audio)
    steps.append({"step": "qa", "result": qa_result})

    # ----- Summary -----
    summary = {
        "scenario": scenario,
        "style": style,
        "engine": engine_name,
        "num_scenes": len(scenes),
        "cost_optimize": cost_optimize,
        "aroll_count": len(aroll_indices) if cost_optimize else len(scenes),
        "broll_count": len(scenes) - len(aroll_indices) if cost_optimize else 0,
        "video_path": final_path,
        "total_cost": total_cost,
        "timestamp": timestamp,
        "steps": steps,
    }

    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Storyboard Anime Pipeline Complete!")
    print(f"  Video: {final_path}")
    print(f"  Scenes: {len(scenes)} ({len(aroll_indices)} A-roll + {len(scenes) - len(aroll_indices)} B-roll)")
    print(f"  Cost: ${total_cost:.2f}")
    print(f"  Output: {out}")
    print(f"{'='*50}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Storyboard Anime Pipeline")
    parser.add_argument("--scenario", "-s", required=True, help="ストーリーのテキスト")
    parser.add_argument("--style", default="anime",
                        choices=["anime", "modern_clean", "vibrant_ugc", "animal_crossing",
                                 "watercolor", "pixel_art", "cinematic_live"])
    parser.add_argument("--engine", "-e", default="kling", choices=["kling", "veo"])
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--character", "-c", help="キャラクター説明")
    parser.add_argument("--num-scenes", type=int, default=8)
    parser.add_argument("--clip-duration", type=int, default=10)
    parser.add_argument("--transition", default="fade",
                        choices=["fade", "dissolve", "wipeleft", "slideright"])
    parser.add_argument("--cost-optimize", action="store_true",
                        help="A-roll + B-roll コスト最適化モード")
    parser.add_argument("--aroll-count", type=int, default=4,
                        help="A-rollシーン数（cost-optimize時）")
    parser.add_argument("--bgm", help="BGMファイルパス")
    parser.add_argument("--bgm-volume", type=float, default=0.20)
    parser.add_argument("--output-dir", "-o", default="output/ugc/storyboard_anime")

    args = parser.parse_args()

    run_storyboard_anime(
        scenario=args.scenario,
        style=args.style,
        engine_name=args.engine,
        aspect_ratio=args.aspect_ratio,
        character=args.character,
        num_scenes=args.num_scenes,
        clip_duration=args.clip_duration,
        transition=args.transition,
        cost_optimize=args.cost_optimize,
        aroll_count=args.aroll_count,
        bgm_path=args.bgm,
        bgm_volume=args.bgm_volume,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
