"""
LongCat + ElevenLabs + Nano Banana Pro + クロマキー 統合パイプライン

ワークフロー:
1. Nano Banana Pro: グリーンスクリーン付きアバター画像を生成
2. ElevenLabs: 音声を生成
3. LongCat: 画像+音声→リップシンク動画（全体動き付き）
4. FFmpeg: グリーン部分をスクリーンショットに置換（クロマキー合成）

使用例:
    python -m ugc.longcat_pipeline full \
        --text "このアプリを紹介します..." \
        --screenshot app.png \
        --output output.mp4
"""

import argparse
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))
from runtime_env import load_runtime_env

load_runtime_env(Path(__file__).resolve().parents[2])

# 遅延インポート用
_nanobanana = None


def _get_nanobanana():
    """nanobananaを遅延インポート"""
    global _nanobanana
    if _nanobanana is None:
        from nanobanana import edit_image, generate_image
        _nanobanana = {"edit_image": edit_image, "generate_image": generate_image}
    return _nanobanana


# デフォルト出力ディレクトリ
DEFAULT_OUTPUT_DIR = Path("output/ugc_longcat")

# グリーンスクリーン付きアバターのプロンプト
GREENSCREEN_AVATAR_PROMPT = """
A friendly young woman in her 20s with a natural smile, holding a smartphone toward the camera.
The smartphone screen is solid BRIGHT GREEN (RGB: 0, 255, 0) - pure green screen for chroma key compositing.
The person is looking at the camera with an engaging expression.
Setting: Casual indoor room with warm natural lighting.
Style: Realistic, natural, high quality portrait suitable for video content.
The green screen on the phone must be perfectly flat, bright, and uniform green color.
Aspect ratio: 9:16 (vertical/portrait orientation for TikTok/Reels).
"""


def generate_greenscreen_avatar(
    output_path: Optional[str] = None,
    custom_prompt: Optional[str] = None,
) -> str:
    """
    Nano Banana Proでグリーンスクリーン付きアバター画像を生成
    
    Args:
        output_path: 出力先パス
        custom_prompt: カスタムプロンプト（Noneの場合はデフォルト使用）
        
    Returns:
        生成された画像のパス
    """
    nanobanana = _get_nanobanana()
    
    print("🎨 グリーンスクリーン付きアバター画像を生成中...")
    
    prompt = custom_prompt or GREENSCREEN_AVATAR_PROMPT
    
    if output_path is None:
        output_dir = DEFAULT_OUTPUT_DIR / "temp"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"avatar_greenscreen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    
    # Nano Banana Pro で画像生成
    result = nanobanana["generate_image"](
        prompt=prompt,
        aspect_ratio="9:16",
        output_path=output_path,
    )
    
    print(f"✅ アバター画像生成完了: {output_path}")
    return output_path


def chromakey_composite(
    video_path: str,
    screenshot_path: str,
    output_path: str,
    green_color: str = "0x00FF00",
    similarity: float = 0.3,
    blend: float = 0.1,
) -> str:
    """
    FFmpegでクロマキー合成（グリーン部分をスクリーンショットに置換）
    
    Args:
        video_path: 入力動画パス
        screenshot_path: スクリーンショット画像パス
        output_path: 出力動画パス
        green_color: クロマキー対象の色（16進数）
        similarity: 色の類似度閾値（0.0-1.0、大きいほど広い範囲）
        blend: エッジのブレンド量
        
    Returns:
        出力動画のパス
    """
    print(f"🎬 クロマキー合成中...")
    print(f"   動画: {video_path}")
    print(f"   スクリーンショット: {screenshot_path}")
    
    # FFmpegでクロマキー合成
    # 1. 動画からグリーン部分を透明化
    # 2. スクリーンショットを下にオーバーレイ
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,           # 動画入力
        "-i", screenshot_path,      # スクリーンショット入力
        "-filter_complex",
        # スクリーンショットを適切なサイズにスケール
        f"[1:v]scale=iw*0.4:-1[screenshot];"
        # 動画のグリーン部分を透明化
        f"[0:v]chromakey={green_color}:{similarity}:{blend}[fg];"
        # スクリーンショットを背景として配置（右下）
        f"[0:v][screenshot]overlay=W*0.55:H*0.35[bg];"
        # 前景（透明化した動画）を重ねる
        f"[bg][fg]overlay=0:0",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "copy",
        output_path,
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ クロマキー合成完了: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpegエラー: {e.stderr}")
        raise


def generate_longcat_video(
    avatar_image: str,
    audio_file: str,
    output_path: str,
    motion_prompt: str = "Natural talking head movement with subtle gestures",
) -> str:
    """
    LongCatでリップシンク動画を生成
    
    Args:
        avatar_image: アバター画像パス
        audio_file: 音声ファイルパス
        output_path: 出力動画パス
        motion_prompt: 動きのプロンプト
        
    Returns:
        生成された動画のパス
    """
    from .engines.longcat import LongCatEngine
    
    engine = LongCatEngine()
    result = engine.generate(
        avatar_image=avatar_image,
        script="",
        audio_file=audio_file,
        output_path=output_path,
        prompt=motion_prompt,
    )
    
    return result.video_path


def full_pipeline(
    text: str,
    screenshot_path: str,
    output_path: str,
    voice: str = "japanese_female",
    avatar_prompt: Optional[str] = None,
    motion_prompt: str = "Natural talking and presenting smartphone app with hand gestures",
) -> str:
    """
    フルパイプライン: グリーンスクリーンアバター → 音声 → LongCat → クロマキー合成
    
    Args:
        text: ナレーションテキスト
        screenshot_path: スクリーンショット画像パス
        output_path: 最終出力動画パス
        voice: 音声スタイル
        avatar_prompt: カスタムアバタープロンプト
        motion_prompt: 動きのプロンプト
        
    Returns:
        最終動画のパス
    """
    from .tts import generate_speech
    
    print("=" * 50)
    print("🎬 LongCat フルパイプライン開始")
    print("=" * 50)
    
    # 出力ディレクトリを準備
    output_dir = Path(output_path).parent
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: グリーンスクリーン付きアバター画像を生成
    print("\n📸 Step 1: グリーンスクリーン付きアバター画像生成")
    avatar_path = generate_greenscreen_avatar(
        output_path=str(temp_dir / "avatar_greenscreen.png"),
        custom_prompt=avatar_prompt,
    )
    
    # Step 2: 音声を生成
    print("\n📢 Step 2: 音声生成（ElevenLabs）")
    audio_path = str(temp_dir / "narration.mp3")
    generate_speech(
        text=text,
        output_path=audio_path,
        voice=voice,
    )
    print(f"✅ 音声生成完了: {audio_path}")
    
    # Step 3: LongCatでリップシンク動画を生成
    print("\n🎥 Step 3: LongCat動画生成")
    raw_video_path = str(temp_dir / "raw_video.mp4")
    generate_longcat_video(
        avatar_image=avatar_path,
        audio_file=audio_path,
        output_path=raw_video_path,
        motion_prompt=motion_prompt,
    )
    
    # Step 4: クロマキー合成
    print("\n🎨 Step 4: クロマキー合成")
    final_video = chromakey_composite(
        video_path=raw_video_path,
        screenshot_path=screenshot_path,
        output_path=output_path,
    )
    
    print("\n" + "=" * 50)
    print(f"✅ パイプライン完了!")
    print(f"   出力: {final_video}")
    print("=" * 50)
    
    return final_video


def quick_generate(
    text: str,
    avatar_image: str,
    output_path: str,
    voice: str = "japanese_female",
    motion_prompt: str = "Natural talking head movement with subtle gestures",
) -> str:
    """
    クイック生成: 既存アバター画像 + テキスト → 動画
    
    Args:
        text: ナレーションテキスト
        avatar_image: アバター画像パス
        output_path: 出力動画パス
        voice: 音声スタイル
        motion_prompt: 動きのプロンプト
        
    Returns:
        生成された動画のパス
    """
    from .tts import generate_speech
    
    print("=" * 50)
    print("🎬 LongCat クイック動画生成")
    print("=" * 50)
    
    # 出力ディレクトリを準備
    output_dir = Path(output_path).parent
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: 音声を生成
    print("\n📢 Step 1: 音声生成（ElevenLabs）")
    audio_path = str(temp_dir / "narration.mp3")
    generate_speech(
        text=text,
        output_path=audio_path,
        voice=voice,
    )
    print(f"✅ 音声生成完了: {audio_path}")
    
    # Step 2: LongCatで動画生成
    print("\n🎥 Step 2: LongCat動画生成")
    generate_longcat_video(
        avatar_image=avatar_image,
        audio_file=audio_path,
        output_path=output_path,
        motion_prompt=motion_prompt,
    )
    
    print("\n" + "=" * 50)
    print(f"✅ 完了: {output_path}")
    print("=" * 50)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description="LongCat + クロマキー パイプライン")
    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")
    
    # Quick: 既存画像から動画生成
    quick_parser = subparsers.add_parser("quick", help="既存アバター画像から動画生成")
    quick_parser.add_argument("--text", "-t", required=True, help="ナレーションテキスト")
    quick_parser.add_argument("--image", "-i", required=True, help="アバター画像パス")
    quick_parser.add_argument("--output", "-o", required=True, help="出力動画パス")
    quick_parser.add_argument("--voice", "-v", default="japanese_female", help="音声スタイル")
    quick_parser.add_argument("--motion", "-m", default="Natural talking head movement", help="動きのプロンプト")
    
    # Full: フルパイプライン
    full_parser = subparsers.add_parser("full", help="フルパイプライン（グリーンスクリーン→LongCat→クロマキー）")
    full_parser.add_argument("--text", "-t", required=True, help="ナレーションテキスト")
    full_parser.add_argument("--screenshot", "-s", required=True, help="スクリーンショット画像パス")
    full_parser.add_argument("--output", "-o", required=True, help="出力動画パス")
    full_parser.add_argument("--voice", "-v", default="japanese_female", help="音声スタイル")
    full_parser.add_argument("--avatar-prompt", help="カスタムアバタープロンプト")
    full_parser.add_argument("--motion", "-m", default="Natural talking and presenting app", help="動きのプロンプト")
    
    # Avatar: グリーンスクリーンアバター生成のみ
    avatar_parser = subparsers.add_parser("avatar", help="グリーンスクリーンアバター画像生成")
    avatar_parser.add_argument("--output", "-o", help="出力画像パス")
    avatar_parser.add_argument("--prompt", "-p", help="カスタムプロンプト")
    
    # Chromakey: クロマキー合成のみ
    chroma_parser = subparsers.add_parser("chromakey", help="クロマキー合成のみ")
    chroma_parser.add_argument("--video", "-v", required=True, help="入力動画パス")
    chroma_parser.add_argument("--screenshot", "-s", required=True, help="スクリーンショット画像パス")
    chroma_parser.add_argument("--output", "-o", required=True, help="出力動画パス")
    
    args = parser.parse_args()
    
    if args.command == "quick":
        quick_generate(
            text=args.text,
            avatar_image=args.image,
            output_path=args.output,
            voice=args.voice,
            motion_prompt=args.motion,
        )
    elif args.command == "full":
        full_pipeline(
            text=args.text,
            screenshot_path=args.screenshot,
            output_path=args.output,
            voice=args.voice,
            avatar_prompt=args.avatar_prompt,
            motion_prompt=args.motion,
        )
    elif args.command == "avatar":
        generate_greenscreen_avatar(
            output_path=args.output,
            custom_prompt=args.prompt,
        )
    elif args.command == "chromakey":
        chromakey_composite(
            video_path=args.video,
            screenshot_path=args.screenshot,
            output_path=args.output,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
