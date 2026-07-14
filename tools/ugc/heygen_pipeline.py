"""
HeyGen + ElevenLabs + Nano Banana Pro 統合パイプライン

スクリーンショットを埋め込んだアバター画像を生成し、
ElevenLabsで音声を作成、HeyGenでリップシンク動画を生成する。

使用例:
    # Quick: 既存画像+テキストから動画生成
    python -m ugc.heygen_pipeline quick \
        --text "このアプリを紹介します..." \
        --image avatar.png \
        --output output.mp4

    # Full: スクショからフルパイプライン
    python -m ugc.heygen_pipeline full \
        --topic "AIアプリの紹介" \
        --screenshot app.png \
        --output output.mp4
"""

import argparse
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from .engines.base import VideoResult

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))
from runtime_env import load_runtime_env

load_runtime_env(Path(__file__).resolve().parents[2])

# 遅延インポート用
_bootcamp_utils = None
_nanobanana = None


def _get_bootcamp_utils():
    """bootcamp_utilsを遅延インポート"""
    global _bootcamp_utils
    if _bootcamp_utils is None:
        from bootcamp_utils import get_client, get_flash_model, get_image_model
        _bootcamp_utils = (get_client, get_flash_model, get_image_model)
    return _bootcamp_utils


def _get_nanobanana():
    """nanobananaを遅延インポート"""
    global _nanobanana
    if _nanobanana is None:
        from nanobanana import edit_image, generate_image
        _nanobanana = {"edit_image": edit_image, "generate_image": generate_image}
    return _nanobanana


# デフォルト出力ディレクトリ
DEFAULT_OUTPUT_DIR = Path("output/ugc_heygen")

# アバタースタイルプリセット
AVATAR_STYLES = {
    "friendly": "A friendly young person in their 20s with a natural, warm smile",
    "professional": "A professional-looking person in business casual attire with confident posture",
    "energetic": "An energetic young influencer with trendy fashion and dynamic expression",
    "casual": "A relaxed young person in casual clothes with approachable demeanor",
}

# プロンプトテンプレート
AVATAR_PROMPT_TEMPLATE = """
{avatar_style}, holding a smartphone toward the camera.
The smartphone screen displays the exact content from the reference image provided.
The person is looking at the camera with an engaging expression.
Setting: {setting}.
Style: Realistic, natural, high quality portrait suitable for video content.
Aspect ratio: 9:16 (vertical/portrait orientation for TikTok/Reels).
"""


def generate_avatar_with_screenshot(
    screenshot_path: str,
    avatar_style: str = "friendly",
    setting: str = "casual indoor room with warm natural lighting",
    output_path: Optional[str] = None,
    aspect_ratio: str = "9:16",
) -> str:
    """
    Nano Banana Proでスクリーンショットを持ったアバター画像を生成
    
    Args:
        screenshot_path: スクリーンショット画像のパス
        avatar_style: アバタースタイル（プリセット名またはカスタム説明）
        setting: 背景設定の説明
        output_path: 出力先パス（Noneの場合は自動生成）
        aspect_ratio: アスペクト比
        
    Returns:
        生成された画像のパス
    """
    get_client, _, _ = _get_bootcamp_utils()
    nanobanana = _get_nanobanana()
    
    client = get_client()
    if not client:
        raise EnvironmentError("GEMINI_API_KEY が設定されていません")
    
    # スクリーンショットの存在確認
    screenshot_path = Path(screenshot_path)
    if not screenshot_path.exists():
        raise FileNotFoundError(f"スクリーンショットが見つかりません: {screenshot_path}")
    
    # アバタースタイルを取得（プリセットまたはカスタム）
    style_description = AVATAR_STYLES.get(avatar_style, avatar_style)
    
    # プロンプトを構築
    prompt = AVATAR_PROMPT_TEMPLATE.format(
        avatar_style=style_description,
        setting=setting,
    ).strip()
    
    # 出力パスを決定
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = DEFAULT_OUTPUT_DIR / "avatars"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"avatar_{timestamp}.png"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 アバター画像生成中（Nano Banana Pro）...")
    print(f"   スクリーンショット: {screenshot_path}")
    print(f"   スタイル: {avatar_style}")
    
    try:
        # edit_imageでスクリーンショットを参照しながら生成
        success = nanobanana["edit_image"](
            client=client,
            input_image_paths=[screenshot_path],
            prompt=prompt,
            output_path=output_path,
            aspect_ratio=aspect_ratio,
            force_aspect_ratio=True,  # 縦長を強制
        )
        
        if success:
            print(f"✅ アバター画像生成完了: {output_path}")
            return str(output_path)
        else:
            raise RuntimeError("画像生成に失敗しました")
            
    except Exception as e:
        print(f"❌ アバター画像生成エラー: {e}")
        raise


def generate_heygen_video(
    text: str,
    avatar_image: str,
    output_path: Optional[str] = None,
    voice: str = "japanese_female",
    voice_id: Optional[str] = None,
) -> "VideoResult":
    """
    ElevenLabs + HeyGenでリップシンク動画を生成
    
    Args:
        text: 話す内容（スクリプト）
        avatar_image: アバター画像のパス
        output_path: 出力動画のパス
        voice: ElevenLabsの声プリセット
        voice_id: ElevenLabsのボイスID（指定時はvoiceを上書き）
        
    Returns:
        VideoResult: 生成結果
    """
    from .engines.heygen import HeyGenEngine
    from .tts import generate_speech
    
    # アバター画像の存在確認
    avatar_path = Path(avatar_image)
    if not avatar_path.exists():
        raise FileNotFoundError(f"アバター画像が見つかりません: {avatar_image}")
    
    # 出力パスを決定
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = DEFAULT_OUTPUT_DIR / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / f"video_{timestamp}.mp4")
    else:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # 一時ファイル用ディレクトリ
    temp_dir = Path(output_path).parent / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    print(f"🎬 HeyGen動画生成パイプライン開始")
    print(f"   スクリプト: {text[:50]}..." if len(text) > 50 else f"   スクリプト: {text}")
    print()
    
    # Step 1: ElevenLabsで音声生成
    print("📢 Step 1: 音声生成（ElevenLabs）")
    audio_path = str(temp_dir / "narration.mp3")
    generate_speech(
        text=text,
        output_path=audio_path,
        voice=voice,
        voice_id=voice_id,
    )
    print()
    
    # Step 2: HeyGenでリップシンク動画生成
    print("🎥 Step 2: リップシンク動画生成（HeyGen）")
    engine = HeyGenEngine()
    result = engine.generate(
        avatar_image=avatar_image,
        script=text,
        audio_file=audio_path,
        output_path=output_path,
    )
    
    print()
    print(f"✅ 動画生成完了!")
    print(f"   出力: {result.video_path}")
    print(f"   長さ: {result.duration:.1f}秒")
    print(f"   推定コスト: ${result.cost:.2f}")
    
    return result


def full_pipeline(
    topic: str,
    screenshot_path: str,
    avatar_style: str = "friendly",
    setting: str = "casual indoor room with warm natural lighting",
    platform: Literal["tiktok", "youtube_shorts", "instagram"] = "tiktok",
    voice: str = "japanese_female",
    output_path: Optional[str] = None,
    skip_avatar_generation: bool = False,
    existing_avatar: Optional[str] = None,
) -> "VideoResult":
    """
    フルパイプライン: スクショからリップシンク動画まで一気に生成
    
    1. Gemini Flashでスクリプト生成
    2. Nano Banana Proでアバター画像生成
    3. ElevenLabsで音声生成
    4. HeyGenでリップシンク動画生成
    
    Args:
        topic: 動画のトピック（スクリプト自動生成用）
        screenshot_path: スクリーンショット画像のパス
        avatar_style: アバタースタイル
        setting: 背景設定
        platform: プラットフォーム（スクリプト生成用）
        voice: ElevenLabsの声プリセット
        output_path: 出力動画のパス
        skip_avatar_generation: アバター生成をスキップ
        existing_avatar: 既存のアバター画像パス（skip_avatar_generation時に使用）
        
    Returns:
        VideoResult: 生成結果
    """
    from .script_generator import generate_ugc_script
    
    # 出力ディレクトリを決定
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_path:
        output_dir = Path(output_path).parent
        final_output = output_path
    else:
        output_dir = DEFAULT_OUTPUT_DIR / timestamp
        final_output = str(output_dir / "final_video.mp4")
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🚀 HeyGen + ElevenLabs + Nano Banana Pro フルパイプライン")
    print("=" * 60)
    print(f"   トピック: {topic}")
    print(f"   プラットフォーム: {platform}")
    print(f"   出力先: {output_dir}")
    print()
    
    # Step 1: スクリプト生成
    print("📝 Step 1: スクリプト生成（Gemini Flash）")
    script = generate_ugc_script(
        topic=topic,
        platform=platform,
        language="ja",
    )
    
    # スクリプトを保存
    script_path = output_dir / "script.txt"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    print(f"   スクリプト保存: {script_path}")
    print()
    
    # Step 2: アバター画像生成
    if skip_avatar_generation and existing_avatar:
        print("⏭️ Step 2: アバター生成スキップ（既存画像を使用）")
        avatar_path = existing_avatar
    else:
        print("🎨 Step 2: アバター画像生成（Nano Banana Pro）")
        avatar_path = generate_avatar_with_screenshot(
            screenshot_path=screenshot_path,
            avatar_style=avatar_style,
            setting=setting,
            output_path=str(output_dir / "avatar.png"),
        )
    print()
    
    # Step 3 & 4: 音声生成 + 動画生成
    result = generate_heygen_video(
        text=script,
        avatar_image=avatar_path,
        output_path=final_output,
        voice=voice,
    )
    
    print()
    print("=" * 60)
    print("🎉 フルパイプライン完了!")
    print(f"   出力ディレクトリ: {output_dir}")
    print(f"   最終動画: {result.video_path}")
    print(f"   合計コスト: ${result.cost:.2f}")
    print("=" * 60)
    
    return result


def main():
    """CLIエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="HeyGen + ElevenLabs + Nano Banana Pro 統合パイプライン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="サブコマンド")
    
    # quick サブコマンド
    quick_parser = subparsers.add_parser(
        "quick",
        help="既存画像+テキストから動画を生成",
    )
    quick_parser.add_argument(
        "--text", "-t",
        required=True,
        help="話す内容（スクリプト）",
    )
    quick_parser.add_argument(
        "--image", "-i",
        required=True,
        help="アバター画像のパス",
    )
    quick_parser.add_argument(
        "--output", "-o",
        help="出力動画のパス",
    )
    quick_parser.add_argument(
        "--voice", "-v",
        default="japanese_female",
        choices=["japanese_female", "japanese_male", "energetic", "calm"],
        help="声のプリセット",
    )
    
    # avatar サブコマンド（画像のみ生成）
    avatar_parser = subparsers.add_parser(
        "avatar",
        help="スクリーンショットからアバター画像のみ生成",
    )
    avatar_parser.add_argument(
        "--screenshot", "-s",
        required=True,
        help="スクリーンショット画像のパス",
    )
    avatar_parser.add_argument(
        "--style",
        default="friendly",
        choices=list(AVATAR_STYLES.keys()),
        help="アバタースタイル",
    )
    avatar_parser.add_argument(
        "--setting",
        default="casual indoor room with warm natural lighting",
        help="背景設定の説明",
    )
    avatar_parser.add_argument(
        "--output", "-o",
        help="出力画像のパス",
    )
    
    # full サブコマンド
    full_parser = subparsers.add_parser(
        "full",
        help="フルパイプライン（スクショ→スクリプト→アバター→動画）",
    )
    full_parser.add_argument(
        "--topic", "-t",
        required=True,
        help="動画のトピック（スクリプト自動生成用）",
    )
    full_parser.add_argument(
        "--screenshot", "-s",
        required=True,
        help="スクリーンショット画像のパス",
    )
    full_parser.add_argument(
        "--style",
        default="friendly",
        choices=list(AVATAR_STYLES.keys()),
        help="アバタースタイル",
    )
    full_parser.add_argument(
        "--platform", "-p",
        default="tiktok",
        choices=["tiktok", "youtube_shorts", "instagram"],
        help="プラットフォーム",
    )
    full_parser.add_argument(
        "--voice", "-v",
        default="japanese_female",
        choices=["japanese_female", "japanese_male", "energetic", "calm"],
        help="声のプリセット",
    )
    full_parser.add_argument(
        "--output", "-o",
        help="出力動画のパス",
    )
    full_parser.add_argument(
        "--existing-avatar",
        help="既存のアバター画像を使用（アバター生成をスキップ）",
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "quick":
        generate_heygen_video(
            text=args.text,
            avatar_image=args.image,
            output_path=args.output,
            voice=args.voice,
        )
    
    elif args.command == "avatar":
        generate_avatar_with_screenshot(
            screenshot_path=args.screenshot,
            avatar_style=args.style,
            setting=args.setting,
            output_path=args.output,
        )
    
    elif args.command == "full":
        skip_avatar = args.existing_avatar is not None
        full_pipeline(
            topic=args.topic,
            screenshot_path=args.screenshot,
            avatar_style=args.style,
            platform=args.platform,
            voice=args.voice,
            output_path=args.output,
            skip_avatar_generation=skip_avatar,
            existing_avatar=args.existing_avatar,
        )


if __name__ == "__main__":
    main()
