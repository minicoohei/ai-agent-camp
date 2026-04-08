#!/usr/bin/env python3
"""
講義動画生成パイプライン

HTMLの講義コンテンツから、Remotion + Veo3/Fabric/Viduを使用して
講義動画を自動生成する。

使用例:
    # Fabricエンジンで生成
    python generate_lecture.py \
        --html https://ai-agent.camp/ja/course/foundation/llm-basics \
        --engine fabric \
        --output output/lecture/llm-basics/

    # Veo3で生成
    python generate_lecture.py \
        --html https://ai-agent.camp/ja/course/foundation/llm-basics \
        --engine veo \
        --output output/lecture/llm-basics/
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# スクリプトのディレクトリをパスに追加
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
sys.path.insert(0, str(SCRIPT_DIR.parent.parent))
from runtime_env import load_runtime_env

load_runtime_env(SCRIPT_DIR.parent.parent.parent)

from scripts.html_parser import parse_html, content_to_dict
from scripts.script_generator import generate_script, generate_script_with_llm


def create_output_dir(base_dir: str) -> Path:
    """出力ディレクトリを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(base_dir) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_tts(
    script_segments: List[dict],
    output_dir: Path,
    voice: str = "default",
) -> List[Path]:
    """
    スクリプトセグメントからTTS音声を生成
    
    Args:
        script_segments: スクリプトセグメントのリスト
        output_dir: 出力ディレクトリ
        voice: 声のプリセット
        
    Returns:
        List[Path]: 生成された音声ファイルのパスリスト
    """
    try:
        from ugc.tts import generate_speech
    except ImportError:
        print("⚠️ TTS module not found. Using placeholder audio.")
        return []
    
    audio_files = []
    
    for i, segment in enumerate(script_segments):
        narration = segment.get("narration", "")
        if not narration:
            continue
        
        audio_path = output_dir / f"segment_{i:03d}.mp3"
        print(f"   生成中: {segment.get('section_title', f'Segment {i}')}...")
        
        try:
            generate_speech(
                text=narration,
                output_path=str(audio_path),
                voice=voice,
            )
            audio_files.append(audio_path)
        except Exception as e:
            print(f"   ⚠️ TTS生成エラー: {e}")
    
    return audio_files


def generate_presenter_video(
    script: dict,
    audio_files: List[Path],
    output_dir: Path,
    engine: str = "fabric",
    avatar_path: Optional[str] = None,
    resolution: str = "720p",
) -> List[Path]:
    """
    プレゼンター動画を生成
    
    Args:
        script: 講義スクリプト
        audio_files: 音声ファイルのリスト
        output_dir: 出力ディレクトリ
        engine: 動画生成エンジン (fabric/veo/vidu)
        avatar_path: アバター画像のパス
        resolution: 解像度
        
    Returns:
        List[Path]: 生成された動画ファイルのパスリスト
    """
    try:
        from ugc.engines import get_engine
    except ImportError:
        print("⚠️ Engine module not found.")
        return []
    
    video_files = []
    segments = script.get("segments", [])
    
    # アバター画像を準備
    if not avatar_path:
        avatar_path = str(output_dir / "avatar.png")
        _generate_avatar(avatar_path)
    
    engine_instance = get_engine(engine)
    
    for i, (segment, audio_file) in enumerate(zip(segments, audio_files)):
        if not audio_file or not audio_file.exists():
            continue
        
        video_path = output_dir / f"presenter_{i:03d}.mp4"
        print(f"   生成中: {segment.get('section_title', f'Segment {i}')}...")
        
        try:
            if engine == "veo":
                # Veo3は音声も生成するため、スクリプトのみ渡す
                result = engine_instance.generate(
                    avatar_image=avatar_path,
                    script=segment.get("narration", ""),
                    output_path=str(video_path),
                    resolution=resolution,
                    duration=min(segment.get("duration", 60), 8),  # Veo3は最大8秒
                )
            else:
                # Fabric/Viduは音声ファイルが必要
                result = engine_instance.generate(
                    avatar_image=avatar_path,
                    script=segment.get("narration", ""),
                    audio_file=str(audio_file),
                    output_path=str(video_path),
                    resolution=resolution,
                )
            
            video_files.append(video_path)
            
        except Exception as e:
            print(f"   ⚠️ 動画生成エラー: {e}")
    
    return video_files


def _generate_avatar(output_path: str) -> None:
    """アバター画像を生成"""
    try:
        from nanobanana import generate_image as generate_avatar_image
        from bootcamp_utils import get_client
        
        prompt = """
A friendly, professional-looking person in their 30s, 
facing the camera with a warm smile.
Clean, modern background suitable for educational content.
Upper body shot, well-lit, high quality.
        """.strip()
        
        client = get_client()
        if client:
            generate_avatar_image(
                client=client,
                prompt=prompt,
                output_path=output_path,
                aspect_ratio="16:9",
            )
            print(f"✅ アバター画像生成完了: {output_path}")
        else:
            print("⚠️ GEMINI_API_KEY未設定。デフォルトアバターを使用")
    except Exception as e:
        print(f"⚠️ アバター生成エラー: {e}")


def generate_remotion_config(
    script: dict,
    output_dir: Path,
) -> Path:
    """
    Remotion用の設定ファイルを生成
    
    Args:
        script: 講義スクリプト
        output_dir: 出力ディレクトリ
        
    Returns:
        Path: 生成された設定ファイルのパス
    """
    config = {
        "title": script.get("title", "講義"),
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "segments": [],
    }
    
    for i, segment in enumerate(script.get("segments", [])):
        config["segments"].append({
            "id": i,
            "title": segment.get("section_title", ""),
            "narration": segment.get("narration", ""),
            "slideType": segment.get("slide_type", "content"),
            "duration": segment.get("duration", 60),
            "visualNotes": segment.get("visual_notes", ""),
            "transition": segment.get("transition", "fade"),
        })
    
    config_path = output_dir / "remotion_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Remotion設定ファイル生成: {config_path}")
    return config_path


def compose_final_video(
    slides_video: Optional[Path],
    presenter_videos: List[Path],
    output_path: Path,
    presenter_position: str = "right",
) -> Path:
    """
    スライド動画とプレゼンター動画を合成
    
    Args:
        slides_video: スライド動画のパス
        presenter_videos: プレゼンター動画のパスリスト
        output_path: 出力パス
        presenter_position: プレゼンターの位置 (left/right/bottom)
        
    Returns:
        Path: 合成された動画のパス
    """
    if not presenter_videos:
        print("⚠️ プレゼンター動画がありません。スライドのみ出力")
        if slides_video and slides_video.exists():
            import shutil
            shutil.copy(slides_video, output_path)
        return output_path
    
    # プレゼンター動画を結合
    concat_list = output_path.parent / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for video in presenter_videos:
            if video.exists():
                f.write(f"file '{video.resolve().as_posix()}'\n")
    
    presenter_combined = output_path.parent / "presenter_combined.mp4"
    
    try:
        # FFmpegで結合
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(presenter_combined),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ プレゼンター動画結合完了: {presenter_combined}")
        
        # スライド動画がある場合は合成
        if slides_video and slides_video.exists():
            _overlay_videos(slides_video, presenter_combined, output_path, presenter_position)
        else:
            import shutil
            shutil.copy(presenter_combined, output_path)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpegエラー: {e}")
        # フォールバック: 最初のプレゼンター動画をコピー
        if presenter_videos and presenter_videos[0].exists():
            import shutil
            shutil.copy(presenter_videos[0], output_path)
    
    return output_path


def _overlay_videos(
    background: Path,
    foreground: Path,
    output: Path,
    position: str,
) -> None:
    """2つの動画を重ね合わせる"""
    # 位置に応じたオーバーレイフィルタ
    if position == "right":
        overlay_filter = "overlay=main_w-overlay_w-20:main_h-overlay_h-20"
    elif position == "left":
        overlay_filter = "overlay=20:main_h-overlay_h-20"
    else:  # bottom
        overlay_filter = "overlay=(main_w-overlay_w)/2:main_h-overlay_h-20"
    
    # プレゼンター動画をリサイズしてオーバーレイ
    cmd = [
        "ffmpeg", "-y",
        "-i", str(background),
        "-i", str(foreground),
        "-filter_complex",
        f"[1:v]scale=480:-1[fg];[0:v][fg]{overlay_filter}",
        "-c:a", "copy",
        str(output),
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 動画合成完了: {output}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 合成エラー: {e}")
        import shutil
        shutil.copy(background, output)


def main():
    parser = argparse.ArgumentParser(
        description="講義動画生成パイプライン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # HTMLから講義動画を生成
  python generate_lecture.py --html https://ai-agent.camp/ja/course/foundation/llm-basics

  # Veo3エンジンで生成
  python generate_lecture.py --html https://ai-agent.camp/ja/course/foundation/llm-basics --engine veo

  # スクリプトのみ生成（動画生成なし）
  python generate_lecture.py --html https://ai-agent.camp/ja/course/foundation/llm-basics --script-only
        """
    )
    
    # 入力
    parser.add_argument("--html", "-i", required=True,
                       help="講義HTMLファイルのパス")
    
    # 出力
    parser.add_argument("--output", "-o", default="output/lecture",
                       help="出力ディレクトリ")
    
    # エンジン
    parser.add_argument("--engine", "-e", default="fabric",
                       choices=["fabric", "veo", "vidu"],
                       help="動画生成エンジン")
    
    # オプション
    parser.add_argument("--voice", "-v", default="default",
                       help="TTSの声")
    parser.add_argument("--avatar", "-a",
                       help="アバター画像のパス")
    parser.add_argument("--resolution", "-r", default="720p",
                       choices=["720p", "1080p"],
                       help="解像度")
    parser.add_argument("--presenter-position", "-p", default="right",
                       choices=["left", "right", "bottom"],
                       help="プレゼンターの位置")
    parser.add_argument("--style", "-s", default="friendly",
                       choices=["friendly", "formal", "casual"],
                       help="話し方のスタイル")
    
    # フラグ
    parser.add_argument("--script-only", action="store_true",
                       help="スクリプトのみ生成（動画生成なし）")
    parser.add_argument("--use-llm", action="store_true",
                       help="LLMを使用してスクリプトを生成")
    parser.add_argument("--skip-tts", action="store_true",
                       help="TTS生成をスキップ")
    parser.add_argument("--skip-presenter", action="store_true",
                       help="プレゼンター動画生成をスキップ")
    
    args = parser.parse_args()
    
    # HTMLファイルの存在確認
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"❌ HTMLファイルが見つかりません: {html_path}")
        sys.exit(1)
    
    # 出力ディレクトリを作成
    output_dir = create_output_dir(args.output)
    print(f"📁 出力ディレクトリ: {output_dir}")
    
    # Step 1: HTMLをパース
    print("\n📝 Step 1: HTMLコンテンツを抽出")
    content = parse_html(str(html_path))
    content_dict = content_to_dict(content)
    
    content_path = output_dir / "content.json"
    with open(content_path, "w", encoding="utf-8") as f:
        json.dump(content_dict, f, ensure_ascii=False, indent=2)
    print(f"   コンテンツ保存: {content_path}")
    print(f"   セクション数: {len(content.sections)}")
    
    # Step 2: スクリプト生成
    print("\n📝 Step 2: 講義スクリプトを生成")
    if args.use_llm:
        script = generate_script_with_llm(content_dict, args.style)
    else:
        script = generate_script(content_dict, args.style)
    
    script_dict = script.to_dict()
    script_path = output_dir / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_dict, f, ensure_ascii=False, indent=2)
    print(f"   スクリプト保存: {script_path}")
    print(f"   セグメント数: {len(script.segments)}")
    print(f"   合計時間: {script.total_duration}秒 ({script.total_duration // 60}分{script.total_duration % 60}秒)")
    
    if args.script_only:
        print("\n✅ スクリプト生成完了（--script-only が指定されたため動画生成をスキップ）")
        return
    
    # Step 3: Remotion設定を生成
    print("\n📝 Step 3: Remotion設定を生成")
    remotion_config = generate_remotion_config(script_dict, output_dir)
    
    # Step 4: TTS音声を生成
    audio_files = []
    if not args.skip_tts:
        print("\n🎤 Step 4: TTS音声を生成")
        audio_dir = output_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        audio_files = generate_tts(script_dict["segments"], audio_dir, args.voice)
        print(f"   生成された音声ファイル: {len(audio_files)}")
    
    # Step 5: プレゼンター動画を生成
    presenter_videos = []
    if not args.skip_presenter and audio_files:
        print(f"\n🎬 Step 5: プレゼンター動画を生成 ({args.engine})")
        presenter_dir = output_dir / "presenter"
        presenter_dir.mkdir(exist_ok=True)
        presenter_videos = generate_presenter_video(
            script_dict,
            audio_files,
            presenter_dir,
            engine=args.engine,
            avatar_path=args.avatar,
            resolution=args.resolution,
        )
        print(f"   生成された動画ファイル: {len(presenter_videos)}")
    
    # Step 6: 最終動画を合成
    print("\n🎬 Step 6: 最終動画を合成")
    final_video = output_dir / "lecture_video.mp4"
    compose_final_video(
        slides_video=None,  # Remotion動画（別途生成が必要）
        presenter_videos=presenter_videos,
        output_path=final_video,
        presenter_position=args.presenter_position,
    )
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print("📊 結果サマリー")
    print(f"{'='*60}")
    print(f"タイトル: {content.title}")
    print(f"セクション数: {len(content.sections)}")
    print(f"合計時間: {script.total_duration}秒 ({script.total_duration // 60}分{script.total_duration % 60}秒)")
    print(f"出力ディレクトリ: {output_dir}")
    if final_video.exists():
        print(f"最終動画: {final_video}")
    print(f"\n✅ 完了!")


if __name__ == "__main__":
    main()
