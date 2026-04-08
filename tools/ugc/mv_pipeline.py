#!/usr/bin/env python3
"""
Music Video Pipeline - AI音楽生成 + ビート同期 + シーン動画化

AI楽曲生成 → ビート解析 → 歌詞→シーンプロンプト → フレーム画像生成 → I2V/Ken Burns → ビート同期結合

使用例:
    # ポップソングMV
    python -m ugc.mv_pipeline \
        --prompt "明るいポップソング、前向きな歌詞" \
        --style anime --engine kling

    # 既存の楽曲でMV
    python -m ugc.mv_pipeline \
        --music ./my_song.mp3 \
        --style cinematic_live --engine kling

    # インストのみ + コスト最適化
    python -m ugc.mv_pipeline \
        --prompt "electronic ambient music" \
        --instrumental \
        --cost-optimize --aroll-count 3
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

_tools_dir = Path(__file__).resolve().parent.parent  # tools/
sys.path.insert(0, str(_tools_dir))

from runtime_env import load_runtime_env

load_runtime_env(_tools_dir.parent)  # project root


def run_mv_pipeline(
    prompt: Optional[str] = None,
    music_path: Optional[str] = None,
    style: str = "anime",
    engine_name: str = "kling",
    num_scenes: int = 8,
    aspect_ratio: str = "16:9",
    instrumental: bool = False,
    cost_optimize: bool = False,
    aroll_count: int = 4,
    output_dir: str = "output/ugc/mv",
) -> dict:
    """ミュージックビデオを生成

    Args:
        prompt: 音楽生成プロンプト（music_pathがない場合）
        music_path: 既存の音楽ファイル
        style: ビジュアルスタイル
        engine_name: I2Vエンジン
        num_scenes: シーン数
        aspect_ratio: アスペクト比
        instrumental: インストのみ
        cost_optimize: コスト最適化
        aroll_count: A-rollシーン数
        output_dir: 出力先

    Returns:
        結果dict
    """
    from bootcamp_utils import get_client

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = Path(output_dir) / timestamp
    out.mkdir(parents=True, exist_ok=True)

    client = get_client()
    if not client:
        raise EnvironmentError("GEMINI_API_KEY が設定されていません")

    total_cost = 0.0
    steps = []

    # ----- Step 1: 楽曲の準備 -----
    print(f"\n{'='*50}")
    print(f"Step 1: 楽曲の準備")

    if music_path and Path(music_path).exists():
        final_music = str(out / "music.mp3")
        shutil.copy2(music_path, final_music)
        print(f"  -> 既存楽曲使用: {music_path}")
        lyrics = None
    elif prompt:
        print(f"  -> AI楽曲生成中...")
        try:
            from ugc.engines.suno import generate_music
            music_result = generate_music(
                prompt=prompt,
                output_path=str(out / "music.mp3"),
                duration=60,
                instrumental=instrumental,
            )
            final_music = music_result.audio_path
            total_cost += music_result.cost
            lyrics = music_result.lyrics
            print(f"  -> 楽曲生成完了: ${music_result.cost:.2f}")
        except Exception as e:
            print(f"  -> AI楽曲生成失敗: {e}")
            print(f"  -> 音楽ファイルなしで映像のみ生成します")
            final_music = None
            lyrics = None
    else:
        raise ValueError("--prompt または --music のいずれかを指定してください")

    steps.append({"step": "music", "path": final_music, "cost": total_cost})

    # ----- Step 2: ビート解析 -----
    print(f"\nStep 2: ビート解析")

    timeline = None
    if final_music:
        try:
            from ugc.beat_sync import analyze_beats, generate_beat_timeline, save_analysis, save_timeline

            analysis = analyze_beats(final_music)
            save_analysis(analysis, str(out / "beat_analysis.json"))
            print(f"  -> テンポ: {analysis.tempo:.1f} BPM")
            print(f"  -> ビート数: {len(analysis.beat_times)}")
            print(f"  -> セクション数: {len(analysis.sections)}")

            timeline = generate_beat_timeline(analysis, num_scenes=num_scenes)
            save_timeline(timeline, str(out / "timeline.json"))
            print(f"  -> {len(timeline)}シーンのタイムライン生成")
        except ImportError:
            print("  -> librosa未インストール。均等分割で代替します。")
            print("     インストール: pip install librosa")
        except Exception as e:
            print(f"  -> ビート解析失敗: {e}. 均等分割で代替します。")

    steps.append({"step": "beat_analysis", "scenes": len(timeline) if timeline else num_scenes})

    # ----- Step 3: シーンプロンプト生成 -----
    print(f"\nStep 3: シーンプロンプト生成 (Gemini)")

    lyrics_context = f"\n歌詞: {lyrics}" if lyrics else ""
    scene_prompt = f"""以下の音楽の雰囲気に合うミュージックビデオのシーンを{num_scenes}シーン分考えてください。

音楽の説明: {prompt or "既存の楽曲"}
スタイル: {style}
{lyrics_context}

各シーンについてJSON配列で返してください:
- scene_number: シーン番号
- description: シーンの視覚的な説明（英語、画像生成プロンプト向け）
- mood: 雰囲気（verse=落ち着き、chorus=ダイナミック、bridge=抽象的）
- camera: カメラワーク（zoom_in, pan_left, pan_right, tilt_up, static等）
- is_key_scene: 重要シーンかどうか（chorus部分はtrue）
- visual_type: 映像タイプ（narrative=物語, abstract=抽象, landscape=風景, performance=パフォーマンス）

JSONのみを返してください。"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=scene_prompt,
    )

    try:
        scenes_text = response.text.strip()
        if scenes_text.startswith("```"):
            scenes_text = scenes_text.split("\n", 1)[1].rsplit("```", 1)[0]
        scenes = json.loads(scenes_text)
    except Exception as e:
        print(f"  Warning: JSON解析失敗: {e}")
        scenes = [
            {"scene_number": i + 1,
             "description": f"Scene {i+1} of the music video, {style} style",
             "mood": "verse" if i % 2 == 0 else "chorus",
             "camera": "static",
             "is_key_scene": i % 2 == 1,
             "visual_type": "narrative"}
            for i in range(num_scenes)
        ]

    with open(out / "scenes.json", "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=2)
    steps.append({"step": "scenes", "count": len(scenes)})
    print(f"  -> {len(scenes)}シーン生成完了")

    # ----- Step 4: フレーム画像生成 -----
    print(f"\nStep 4: フレーム画像生成 (Gemini Image)")

    from nanobanana import generate_image as gen_img

    frames_dir = out / "frames"
    frames_dir.mkdir(exist_ok=True)
    frame_paths = []

    for i, scene in enumerate(scenes):
        frame_path = str(frames_dir / f"frame_{i:03d}.png")
        desc = scene.get("description", f"Scene {i+1}")
        mood = scene.get("mood", "neutral")
        vis_type = scene.get("visual_type", "narrative")

        img_prompt = f"Music video scene: {desc}. {style} style art, {mood} mood, {vis_type} visual, high quality cinematic"

        try:
            gen_img(
                client=client,
                prompt=img_prompt,
                output_path=frame_path,
                aspect_ratio=aspect_ratio,
            )
            frame_paths.append(frame_path)
            print(f"  -> Frame {i+1}/{len(scenes)}")
        except Exception as e:
            print(f"  -> Frame {i+1} failed: {e}")

    steps.append({"step": "frames", "count": len(frame_paths)})

    # ----- Step 5: 動画クリップ生成 -----
    print(f"\nStep 5: 動画クリップ生成")

    from ugc.engines import get_engine
    from ugc.ken_burns import generate_broll

    clips_dir = out / "clips"
    clips_dir.mkdir(exist_ok=True)

    # シーンごとの長さを決定
    if timeline:
        scene_durations = [t.duration for t in timeline]
    else:
        avg_duration = 60.0 / num_scenes  # 60秒を均等分割
        scene_durations = [avg_duration] * num_scenes

    # A-roll / B-roll 分類
    if cost_optimize:
        key_scenes = [i for i, s in enumerate(scenes) if s.get("is_key_scene", False)]
        if len(key_scenes) < aroll_count:
            remaining = [i for i in range(len(scenes)) if i not in key_scenes]
            key_scenes.extend(remaining[:aroll_count - len(key_scenes)])
        aroll_indices = set(sorted(key_scenes[:aroll_count]))
        print(f"  Cost-optimize: A-roll={len(aroll_indices)}, B-roll={len(scenes)-len(aroll_indices)}")
    else:
        aroll_indices = set(range(len(scenes)))

    engine = get_engine(engine_name)
    clip_paths = []
    ken_burns_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right", "slow_zoom", "pan_down"]

    for i in range(len(frame_paths)):
        clip_path = str(clips_dir / f"clip_{i:03d}.mp4")
        original_dur = scene_durations[i] if i < len(scene_durations) else 8.0
        dur = max(3.0, min(original_dur, 10.0))  # 3-10秒にクランプ
        if dur != original_dur:
            print(f"  注意: Scene {i+1} duration clamped {original_dur:.1f}s → {dur:.1f}s")

        if i in aroll_indices:
            print(f"  [A-roll] Clip {i+1}: {engine_name} I2V ({dur:.1f}s)...")
            try:
                result = engine.generate(
                    avatar_image=frame_paths[i],
                    script=scenes[i].get("description", ""),
                    output_path=clip_path,
                    duration=int(dur),
                )
                total_cost += result.cost
                clip_paths.append(clip_path)
            except Exception as e:
                print(f"    -> I2V failed, Ken Burns fallback: {e}")
                effect = ken_burns_effects[i % len(ken_burns_effects)]
                generate_broll(frame_paths[i], clip_path, duration=dur, effect=effect)
                clip_paths.append(clip_path)
        else:
            camera = scenes[i].get("camera", "zoom_in") if i < len(scenes) else "zoom_in"
            effect = camera if camera in ken_burns_effects else ken_burns_effects[i % len(ken_burns_effects)]
            print(f"  [B-roll] Clip {i+1}: Ken Burns ({effect}, {dur:.1f}s)")
            generate_broll(frame_paths[i], clip_path, duration=dur, effect=effect)
            clip_paths.append(clip_path)

    steps.append({"step": "clips", "count": len(clip_paths), "cost": total_cost})

    # ----- Step 6: ビート同期結合 -----
    print(f"\nStep 6: ビート同期結合")

    from ugc.video_concat import concat_with_crossfade, concat_simple

    joined_path = str(out / "joined.mp4")
    if len(clip_paths) >= 2:
        try:
            concat_with_crossfade(clip_paths, joined_path, transition="fade", transition_duration=0.3)
        except Exception as e:
            print(f"  xfade failed, simple concat: {e}")
            concat_simple(clip_paths, joined_path)
    elif clip_paths:
        shutil.copy2(clip_paths[0], joined_path)

    steps.append({"step": "concat", "path": joined_path})

    # ----- Step 7: 音楽ミックス -----
    print(f"\nStep 7: 音楽ミックス")
    final_path = str(out / "final.mp4")

    if final_music:
        from ugc.audio_post import mix_bgm_no_audio
        try:
            mix_bgm_no_audio(joined_path, final_music, final_path, bgm_volume=1.0)
            print(f"  -> {final_path}")
        except Exception as e:
            print(f"  -> ミックス失敗: {e}")
            shutil.copy2(joined_path, final_path)
    else:
        shutil.copy2(joined_path, final_path)

    steps.append({"step": "final", "path": final_path})

    # ----- Summary -----
    summary = {
        "prompt": prompt or "(既存楽曲)",
        "style": style,
        "engine": engine_name,
        "num_scenes": len(scenes),
        "cost_optimize": cost_optimize,
        "aroll_count": len(aroll_indices) if cost_optimize else len(scenes),
        "music_path": final_music,
        "video_path": final_path,
        "total_cost": total_cost,
        "timestamp": timestamp,
        "steps": steps,
    }

    with open(out / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Music Video Pipeline Complete!")
    print(f"  Video: {final_path}")
    print(f"  Scenes: {len(scenes)} ({len(aroll_indices)} A-roll + {len(scenes) - len(aroll_indices)} B-roll)")
    print(f"  Cost: ${total_cost:.2f}")
    print(f"  Output: {out}")
    print(f"{'='*50}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Music Video Pipeline")
    parser.add_argument("--prompt", "-p", help="音楽生成プロンプト")
    parser.add_argument("--music", "-m", help="既存の音楽ファイル")
    parser.add_argument("--style", default="anime",
                        choices=["anime", "modern_clean", "vibrant_ugc", "cinematic_live",
                                 "watercolor", "pixel_art", "abstract"])
    parser.add_argument("--engine", "-e", default="kling", choices=["kling", "veo"])
    parser.add_argument("--num-scenes", type=int, default=8)
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--instrumental", action="store_true", help="インストのみ")
    parser.add_argument("--cost-optimize", action="store_true")
    parser.add_argument("--aroll-count", type=int, default=4)
    parser.add_argument("--output-dir", "-o", default="output/ugc/mv")

    args = parser.parse_args()

    if not args.prompt and not args.music:
        parser.error("--prompt または --music のいずれかを指定してください")

    run_mv_pipeline(
        prompt=args.prompt,
        music_path=args.music,
        style=args.style,
        engine_name=args.engine,
        num_scenes=args.num_scenes,
        aspect_ratio=args.aspect_ratio,
        instrumental=args.instrumental,
        cost_optimize=args.cost_optimize,
        aroll_count=args.aroll_count,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
