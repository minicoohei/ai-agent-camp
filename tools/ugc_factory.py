#!/usr/bin/env python3
"""
UGC Factory - AI UGC動画自動生成CLI

Veo 3.1、Fabric 1.0、HeyGen、Kling 2.6 Proのエンジンを切り替えて
AI UGC動画を自動生成する統合ツール。

使用例:
    # Fabric 1.0で生成（デフォルト）
    python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine fabric

    # Veo 3.1で生成
    python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine veo

    # HeyGenで生成
    python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine heygen

    # 4つ全部で生成して比較
    python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine all
"""

import argparse
import json
import os
import sys
import tempfile
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env

load_runtime_env()


# モジュールをインポート
from ugc import generate_ugc_script, generate_speech, composite_video
from ugc.audio_post import (
    mux_audio,
    remove_vocals_from_video,
    apply_wav2lip,
    apply_musetalk,
    extract_audio,
)
from ugc.engines import get_engine, ENGINE_MAP, VideoResult

# nanobanana.pyからアバター画像生成をインポート
from nanobanana import generate_image as generate_avatar_image
from bootcamp_utils import get_client


def create_output_dir(base_dir: str = "output/ugc") -> Path:
    """出力ディレクトリを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(base_dir) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_avatar(
    topic: str,
    output_path: str,
    style: str = "default",
) -> str:
    """
    アバター画像を生成する（スマホを持った人物、画面は緑色）
    
    Args:
        topic: トピック（参考用）
        output_path: 出力パス
        style: アバタースタイル
        
    Returns:
        生成された画像のパス
    """
    from ugc.prompts import load_prompts
    
    # プロンプトを取得
    try:
        from ugc import prompts
        prompts_path = Path(__file__).parent / "ugc" / "prompts.json"
        if prompts_path.exists():
            with open(prompts_path, "r", encoding="utf-8") as f:
                prompts_data = json.load(f)
                avatar_prompts = prompts_data.get("avatar_prompts", {})
                prompt = avatar_prompts.get(style, avatar_prompts.get("default", ""))
        else:
            prompt = ""
    except Exception:
        prompt = ""
    
    if not prompt:
        prompt = """
A friendly young person in their 20s holding a smartphone toward the camera.
The smartphone screen displays a solid bright green color (#00FF00) for chroma key compositing.
The person has a natural, enthusiastic expression and is in a casual indoor setting with good lighting.
The smartphone is clearly visible and positioned to show the screen to the viewer.
Realistic photo style.
"""
    
    print(f"🖼️ アバター画像生成中...")
    
    client = get_client()
    if not client:
        raise EnvironmentError("GEMINI_API_KEY が設定されていません")
    
    generate_avatar_image(
        client=client,
        prompt=prompt.strip(),
        output_path=output_path,
        aspect_ratio="9:16",  # 縦長（TikTok/Reels向け）
    )
    
    print(f"✅ アバター画像生成完了: {output_path}")
    return output_path


def run_pipeline(
    topic: str,
    screenshot_path: str,
    engine_name: str,
    output_dir: Path,
    platform: str = "tiktok",
    duration: int = 30,
    voice: str = "default",
    resolution: str = "720p",
    skip_avatar: bool = False,
    avatar_path: Optional[str] = None,
    kling_duration: int = 10,
    kling_audio: bool = False,
    post_audio: bool = False,
    post_audio_file: Optional[str] = None,
    remove_vocals: bool = False,
    lipsync: bool = False,
    lipsync_engine: str = "wav2lip",
    lipsync_audio_file: Optional[str] = None,
    lipsync_dir: Optional[str] = None,
    lipsync_checkpoint: Optional[str] = None,
    lipsync_face_enhance: bool = False,
) -> Optional[VideoResult]:
    """
    単一エンジンでパイプラインを実行
    
    Args:
        topic: トピック
        screenshot_path: スクリーンショットのパス
        engine_name: エンジン名
        output_dir: 出力ディレクトリ
        platform: プラットフォーム
        duration: 動画の長さ（秒）
        voice: 声のプリセット
        resolution: 解像度
        skip_avatar: アバター生成をスキップ
        avatar_path: 既存のアバター画像パス
        
    Returns:
        VideoResult or None
    """
    print(f"\n{'='*60}")
    print(f"🎬 {engine_name.upper()} エンジンで生成開始")
    print(f"{'='*60}")
    
    engine_output = output_dir / engine_name
    engine_output.mkdir(exist_ok=True)
    
    try:
        # Step 1: スクリプト生成
        print("\n📝 Step 1: スクリプト生成")
        script = generate_ugc_script(
            topic=topic,
            platform=platform,
            duration=duration,
        )
        
        # スクリプトを保存
        script_path = engine_output / "script.txt"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
        print(f"   保存: {script_path}")
        
        # Step 2: アバター画像生成（必要な場合）
        if avatar_path and Path(avatar_path).exists():
            print(f"\n🖼️ Step 2: 既存アバター画像を使用: {avatar_path}")
            current_avatar = avatar_path
        elif skip_avatar:
            print(f"\n🖼️ Step 2: アバター生成スキップ")
            current_avatar = None
        else:
            print(f"\n🖼️ Step 2: アバター画像生成")
            current_avatar = str(engine_output / "avatar.png")
            generate_avatar(topic, current_avatar)
        
        # Step 3: エンジン固有の処理
        engine = get_engine(engine_name)
        
        if engine.requires_tts:
            # TTSが必要なエンジン（Fabric, HeyGen）
            print(f"\n🎤 Step 3: 音声生成 (Eleven Labs)")
            audio_path = str(engine_output / "speech.mp3")
            generate_speech(
                text=script,
                output_path=audio_path,
                voice=voice,
            )
            
            print(f"\n🎬 Step 4: 動画生成 ({engine_name})")
            raw_video_path = str(engine_output / "raw_video.mp4")
            result = engine.generate(
                avatar_image=current_avatar or "",
                script=script,
                audio_file=audio_path,
                output_path=raw_video_path,
                resolution=resolution,
            )
        else:
            # TTSが不要なエンジン（Veo, Kling）
            print(f"\n🎬 Step 3: 動画生成 ({engine_name})")
            raw_video_path = str(engine_output / "raw_video.mp4")
            if engine_name == "veo":
                result = engine.generate(
                    avatar_image=current_avatar or "",
                    script=script,
                    output_path=raw_video_path,
                    resolution=resolution,
                    duration=min(duration, 8),  # Veoは最大8秒
                )
            elif engine_name == "kling":
                result = engine.generate(
                    avatar_image=current_avatar or "",
                    script=script,
                    output_path=raw_video_path,
                    duration=kling_duration,
                    generate_audio=kling_audio,
                )
            else:
                result = engine.generate(
                    avatar_image=current_avatar or "",
                    script=script,
                    output_path=raw_video_path,
                    resolution=resolution,
                    duration=duration,
                )
        
        # Step 5: グリーンスクリーン合成
        print(f"\n🖼️ Step 5: グリーンスクリーン合成")
        final_video_path = str(engine_output / "final_video.mp4")
        
        if Path(result.video_path).exists() and Path(screenshot_path).exists():
            try:
                composite_video(
                    video_path=result.video_path,
                    screenshot_path=screenshot_path,
                    output_path=final_video_path,
                    backend="ffmpeg",
                )
                result.video_path = final_video_path
            except Exception as e:
                print(f"   ⚠️ 合成スキップ（エラー）: {e}")
        else:
            print(f"   ⚠️ 合成スキップ（ファイル不足）")

        # Step 6: Klingの後付け音声（TTS）または音声ファイル合成
        last_audio_path = None

        if engine_name == "kling" and (post_audio or post_audio_file):
            if kling_audio:
                print("   ⚠️ Klingの音声生成オンのため、後付け音声は上書きします")
            if post_audio_file:
                audio_path = post_audio_file
                if not Path(audio_path).exists():
                    raise ValueError(f"後付け音声が見つかりません: {audio_path}")
            else:
                print(f"\n🎤 Step 6: 後付け音声生成 (Eleven Labs)")
                audio_path = str(engine_output / "post_speech.mp3")
                generate_speech(
                    text=script,
                    output_path=audio_path,
                    voice=voice,
                )

            post_audio_video = str(engine_output / "post_audio.mp4")
            mux_audio(
                video_path=result.video_path,
                audio_path=audio_path,
                output_path=post_audio_video,
            )
            result.video_path = post_audio_video
            last_audio_path = audio_path

        # Step 7: リップシンク（Wav2Lip / MuseTalk）
        if lipsync:
            if lipsync_engine == "musetalk":
                print(f"\n👄 Step 7: リップシンク (MuseTalk)")
                if lipsync_audio_file:
                    lipsync_audio = lipsync_audio_file
                    if not Path(lipsync_audio).exists():
                        raise ValueError(f"リップシンク音声が見つかりません: {lipsync_audio}")
                else:
                    print(f"   MuseTalk用の音声を生成します (Eleven Labs)")
                    lipsync_audio = str(engine_output / "lipsync_speech.mp3")
                    generate_speech(
                        text=script,
                        output_path=lipsync_audio,
                        voice=voice,
                    )

                lipsync_output = str(engine_output / "lipsync.mp4")
                apply_musetalk(
                    video_path=result.video_path,
                    audio_path=lipsync_audio,
                    output_path=lipsync_output,
                )
                result.video_path = lipsync_output
            else:
                print(f"\n👄 Step 7: リップシンク (Wav2Lip)")
                if lipsync_audio_file:
                    lipsync_audio = lipsync_audio_file
                    if not Path(lipsync_audio).exists():
                        raise ValueError(f"リップシンク音声が見つかりません: {lipsync_audio}")
                elif last_audio_path:
                    lipsync_audio = last_audio_path
                else:
                    # 動画内の音声を抽出して利用
                    lipsync_audio = str(engine_output / "lipsync_audio.wav")
                    extract_audio(result.video_path, lipsync_audio)

                lipsync_output = str(engine_output / "lipsync.mp4")
                apply_wav2lip(
                    video_path=result.video_path,
                    audio_path=lipsync_audio,
                    output_path=lipsync_output,
                    wav2lip_dir=lipsync_dir,
                    checkpoint_path=lipsync_checkpoint,
                    face_enhance=lipsync_face_enhance,
                )
                result.video_path = lipsync_output

        # Step 8: ボーカル除去（Demucs）
        if remove_vocals:
            try:
                no_vocals_video = str(engine_output / "no_vocals.mp4")
                remove_vocals_from_video(result.video_path, no_vocals_video)
                result.video_path = no_vocals_video
            except Exception as e:
                print(f"   ⚠️ ボーカル除去スキップ（エラー）: {e}")
        
        # 結果を保存
        result_path = engine_output / "result.json"
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {engine_name.upper()} 完了!")
        print(f"   動画: {result.video_path}")
        print(f"   長さ: {result.duration:.1f}秒")
        print(f"   コスト: ${result.cost:.2f}")
        
        return result
        
    except Exception as e:
        print(f"\n❌ {engine_name.upper()} エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description="UGC Factory - AI UGC動画自動生成CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # Fabric 1.0で生成
  python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png

  # Veo 3.1で生成
  python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine veo

  # 全エンジンで比較生成
  python ugc_factory.py --topic "このAIアプリで学習効率3倍" --screenshot ./app.png --engine all
        """
    )
    
    # 必須引数
    parser.add_argument("--topic", "-t", required=True, help="動画のトピック/テーマ")
    parser.add_argument("--screenshot", "-s", required=True, help="アプリのスクリーンショット")
    
    # エンジン選択
    parser.add_argument(
        "--engine", "-e",
        default="fabric",
        choices=["fabric", "heygen", "veo", "kling", "all"],
        help="使用するエンジン (default: fabric)"
    )
    
    # オプション
    parser.add_argument("--platform", "-p", default="tiktok",
                       choices=["tiktok", "youtube_shorts", "instagram"],
                       help="ターゲットプラットフォーム")
    parser.add_argument("--duration", "-d", type=int, default=30,
                       help="動画の長さ（秒）")
    parser.add_argument("--voice", "-v", default="default",
                       help="声のプリセット")
    parser.add_argument("--resolution", "-r", default="720p",
                       choices=["480p", "720p"],
                       help="解像度")
    parser.add_argument("--output-dir", "-o", default="output/ugc",
                       help="出力ディレクトリ")
    parser.add_argument("--avatar", "-a", help="既存のアバター画像パス")
    parser.add_argument("--skip-avatar", action="store_true",
                       help="アバター生成をスキップ")
    parser.add_argument("--kling-duration", type=int, default=10,
                       choices=[5, 10], help="Klingの動画長（5 or 10）")
    parser.add_argument("--kling-audio", action="store_true",
                       help="Klingの音声生成を有効化")
    parser.add_argument("--post-audio", action="store_true",
                       help="Klingに後付けで音声を合成（TTS）")
    parser.add_argument("--post-audio-file",
                       help="Klingの後付け音声ファイル（指定時はこちらを使用）")
    parser.add_argument("--remove-vocals", action="store_true",
                       help="ボーカル除去（Demucs）")
    parser.add_argument("--lipsync", action="store_true",
                       help="Wav2Lipでリップシンクを適用")
    parser.add_argument("--lipsync-engine", default="wav2lip",
                       choices=["wav2lip", "musetalk"],
                       help="リップシンクのエンジン (wav2lip/musetalk)")
    parser.add_argument("--lipsync-audio-file",
                       help="リップシンク用音声ファイル（指定時はこちらを使用）")
    parser.add_argument("--lipsync-dir",
                       help="Wav2Lipのディレクトリ（inference.pyがある場所）")
    parser.add_argument("--lipsync-checkpoint",
                       help="Wav2Lipのモデルチェックポイントパス")
    parser.add_argument("--lipsync-face-enhance", action="store_true",
                       help="Wav2Lipのface_enhanceを有効化")
    
    args = parser.parse_args()
    
    # スクリーンショットの存在確認
    if not Path(args.screenshot).exists():
        print(f"❌ スクリーンショットが見つかりません: {args.screenshot}")
        sys.exit(1)
    
    # 出力ディレクトリを作成
    output_dir = create_output_dir(args.output_dir)
    print(f"📁 出力ディレクトリ: {output_dir}")
    
    # 設定を保存
    config = {
        "topic": args.topic,
        "screenshot": args.screenshot,
        "engine": args.engine,
        "platform": args.platform,
        "duration": args.duration,
        "voice": args.voice,
        "resolution": args.resolution,
        "kling_duration": args.kling_duration,
        "kling_audio": args.kling_audio,
        "post_audio": args.post_audio,
        "post_audio_file": args.post_audio_file,
        "remove_vocals": args.remove_vocals,
        "lipsync": args.lipsync,
        "lipsync_engine": args.lipsync_engine,
        "lipsync_audio_file": args.lipsync_audio_file,
        "lipsync_dir": args.lipsync_dir,
        "lipsync_checkpoint": args.lipsync_checkpoint,
        "lipsync_face_enhance": args.lipsync_face_enhance,
        "timestamp": datetime.now().isoformat(),
    }
    with open(output_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # エンジンを決定
    if args.engine == "all":
        engines = list(ENGINE_MAP.keys())
    else:
        engines = [args.engine]
    
    # 各エンジンでパイプラインを実行
    results = {}
    for engine_name in engines:
        result = run_pipeline(
            topic=args.topic,
            screenshot_path=args.screenshot,
            engine_name=engine_name,
            output_dir=output_dir,
            platform=args.platform,
            duration=args.duration,
            voice=args.voice,
            resolution=args.resolution,
            skip_avatar=args.skip_avatar,
            avatar_path=args.avatar,
            kling_duration=args.kling_duration,
            kling_audio=args.kling_audio,
            post_audio=args.post_audio,
            post_audio_file=args.post_audio_file,
            remove_vocals=args.remove_vocals,
            lipsync=args.lipsync,
            lipsync_engine=args.lipsync_engine,
            lipsync_audio_file=args.lipsync_audio_file,
            lipsync_dir=args.lipsync_dir,
            lipsync_checkpoint=args.lipsync_checkpoint,
            lipsync_face_enhance=args.lipsync_face_enhance,
        )
        if result:
            results[engine_name] = result
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print("📊 結果サマリー")
    print(f"{'='*60}")
    
    total_cost = 0
    for engine_name, result in results.items():
        print(f"\n{engine_name.upper()}:")
        print(f"  動画: {result.video_path}")
        print(f"  長さ: {result.duration:.1f}秒")
        print(f"  コスト: ${result.cost:.2f}")
        total_cost += result.cost
    
    if len(results) > 1:
        print(f"\n合計コスト: ${total_cost:.2f}")
    
    print(f"\n📁 出力: {output_dir}")
    print(f"✅ 完了!")


if __name__ == "__main__":
    main()
