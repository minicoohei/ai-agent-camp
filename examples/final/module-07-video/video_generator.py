#!/usr/bin/env python3
"""
動画生成スクリプト（Final Example）

動画フレーム抽出、絵コンテ生成、動画合成を行います。

必要条件:
- Python 3.9以上
- opencv-python, Pillow
- FFmpeg（動画合成用）

使用方法:
    python video_generator.py extract --input video.mp4 --interval 30
    python video_generator.py storyboard --topic "AIエージェント紹介" --duration 60
    python video_generator.py compose --config config.json --output output.mp4
"""

import os
import sys
import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("Warning: opencv-python がインストールされていません")

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class VideoFrameExtractor:
    """動画フレーム抽出クラス"""
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None
        
        if HAS_CV2 and os.path.exists(video_path):
            self.cap = cv2.VideoCapture(video_path)
    
    def get_video_info(self) -> Dict[str, Any]:
        """動画情報を取得"""
        if self.cap:
            return {
                "file_path": self.video_path,
                "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": self.cap.get(cv2.CAP_PROP_FPS),
                "total_frames": int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "duration_sec": int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) / self.cap.get(cv2.CAP_PROP_FPS))
            }
        else:
            return {
                "file_path": self.video_path,
                "width": 1920,
                "height": 1080,
                "fps": 30,
                "total_frames": 1800,
                "duration_sec": 60,
                "note": "モックデータ"
            }
    
    def extract_frames(self, output_dir: str, interval_sec: int = 30) -> List[str]:
        """フレームを抽出"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted_files = []
        
        if self.cap:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            interval_frames = int(fps * interval_sec)
            
            frame_num = 0
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                if frame_num % interval_frames == 0:
                    time_sec = frame_num / fps
                    filename = f"frame_{frame_num:06d}_{time_sec:.1f}s.png"
                    filepath = output_path / filename
                    cv2.imwrite(str(filepath), frame)
                    extracted_files.append(str(filepath))
                    print(f"  抽出: {filename}")
                
                frame_num += 1
            
            self.cap.release()
        else:
            # モック: ダミーファイル名を返す
            for i in range(5):
                time_sec = i * interval_sec
                filename = f"frame_{i*interval_sec*30:06d}_{time_sec:.1f}s.png"
                extracted_files.append(str(output_path / filename))
            print("  モックモード: 実際のフレームは抽出されません")
        
        return extracted_files
    
    def extract_keyframes(self, output_dir: str, threshold: float = 30.0) -> List[str]:
        """シーン変化に基づいてキーフレームを抽出"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted_files = []
        
        if self.cap and HAS_CV2:
            prev_frame = None
            frame_num = 0
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                if prev_frame is not None:
                    diff = cv2.absdiff(prev_frame, gray)
                    mean_diff = diff.mean()
                    
                    if mean_diff > threshold:
                        time_sec = frame_num / fps
                        filename = f"keyframe_{frame_num:06d}_{time_sec:.1f}s.png"
                        filepath = output_path / filename
                        cv2.imwrite(str(filepath), frame)
                        extracted_files.append(str(filepath))
                        print(f"  キーフレーム抽出: {filename} (diff: {mean_diff:.2f})")
                
                prev_frame = gray
                frame_num += 1
            
            self.cap.release()
        else:
            print("  モックモード: OpenCVが利用できません")
        
        return extracted_files


class StoryboardGenerator:
    """絵コンテ生成クラス"""
    
    def generate(self, topic: str, duration: int, style: str = "professional") -> Dict[str, Any]:
        """絵コンテを生成"""
        # シーン数を計算（15秒ごとに1シーン）
        num_scenes = max(4, duration // 15)
        
        storyboard = {
            "metadata": {
                "title": topic,
                "duration_sec": duration,
                "style": style,
                "created_at": datetime.now().isoformat(),
                "resolution": "1920x1080",
                "fps": 30
            },
            "scenes": []
        }
        
        # シーン生成
        scene_templates = self._get_scene_templates(style)
        scene_duration = duration / num_scenes
        
        for i in range(num_scenes):
            template = scene_templates[i % len(scene_templates)]
            start_time = i * scene_duration
            end_time = (i + 1) * scene_duration
            
            scene = {
                "number": i + 1,
                "start_sec": round(start_time, 1),
                "end_sec": round(end_time, 1),
                "duration_sec": round(scene_duration, 1),
                "type": template["type"],
                "description": template["description"].format(topic=topic),
                "visual": template["visual"],
                "narration": template["narration"].format(topic=topic),
                "transition": template.get("transition", "cut"),
                "notes": template.get("notes", "")
            }
            
            storyboard["scenes"].append(scene)
        
        return storyboard
    
    def _get_scene_templates(self, style: str) -> List[Dict[str, Any]]:
        """スタイル別シーンテンプレート"""
        templates = {
            "professional": [
                {
                    "type": "opening",
                    "description": "{topic} - オープニング",
                    "visual": "ロゴアニメーション、グラデーション背景",
                    "narration": "こんにちは。{topic}についてご紹介します。",
                    "transition": "fade_in"
                },
                {
                    "type": "problem",
                    "description": "課題・問題提起",
                    "visual": "問題を示すイラストまたは写真",
                    "narration": "多くの方が直面している課題があります。",
                    "transition": "slide_left"
                },
                {
                    "type": "solution",
                    "description": "解決策の提示",
                    "visual": "{topic}のデモ画面、機能紹介",
                    "narration": "{topic}がその解決策となります。",
                    "transition": "zoom_in"
                },
                {
                    "type": "features",
                    "description": "機能・特徴の紹介",
                    "visual": "機能リスト、アイコン付き説明",
                    "narration": "主な機能をご紹介します。",
                    "transition": "slide_up"
                },
                {
                    "type": "demo",
                    "description": "デモ・実例",
                    "visual": "実際の操作画面、Before/After",
                    "narration": "実際に使ってみましょう。",
                    "transition": "cut"
                },
                {
                    "type": "cta",
                    "description": "CTA（行動喚起）",
                    "visual": "ロゴ、QRコード、URL",
                    "narration": "ぜひお試しください。",
                    "transition": "fade_out"
                }
            ],
            "casual": [
                {
                    "type": "opening",
                    "description": "{topic} - イントロ",
                    "visual": "明るい背景、ポップなグラフィック",
                    "narration": "やぁ！今日は{topic}について話すよ！",
                    "transition": "bounce"
                },
                {
                    "type": "content",
                    "description": "メインコンテンツ",
                    "visual": "アニメーション、イラスト",
                    "narration": "これがすごいんだ！",
                    "transition": "slide"
                },
                {
                    "type": "ending",
                    "description": "エンディング",
                    "visual": "サブスクライブボタン、SNSリンク",
                    "narration": "チャンネル登録よろしくね！",
                    "transition": "fade"
                }
            ]
        }
        
        return templates.get(style, templates["professional"])
    
    def to_markdown(self, storyboard: Dict[str, Any]) -> str:
        """Markdownに変換"""
        md = f"""# 絵コンテ: {storyboard['metadata']['title']}

## 基本情報

| 項目 | 値 |
|------|-----|
| 尺 | {storyboard['metadata']['duration_sec']}秒 |
| 解像度 | {storyboard['metadata']['resolution']} |
| FPS | {storyboard['metadata']['fps']} |
| スタイル | {storyboard['metadata']['style']} |
| 作成日時 | {storyboard['metadata']['created_at']} |

---

"""
        
        for scene in storyboard["scenes"]:
            md += f"""## シーン {scene['number']}: {scene['type']} ({scene['start_sec']}s - {scene['end_sec']}s)

**説明**: {scene['description']}

**映像**:
{scene['visual']}

**ナレーション**:
> {scene['narration']}

**トランジション**: {scene['transition']}

---

"""
        
        return md


class VideoComposer:
    """動画合成クラス"""
    
    def __init__(self):
        self.ffmpeg_path = "ffmpeg"
    
    def check_ffmpeg(self) -> bool:
        """FFmpegの存在確認"""
        try:
            subprocess.run([self.ffmpeg_path, "-version"], capture_output=True)
            return True
        except FileNotFoundError:
            return False
    
    def compose(self, config: Dict[str, Any], output_path: str) -> bool:
        """動画を合成"""
        if not self.check_ffmpeg():
            print("❌ FFmpegが見つかりません")
            print("  インストール: brew install ffmpeg (macOS)")
            return False
        
        # 設定から各素材を取得
        scenes = config.get("scenes", [])
        audio = config.get("audio", {})
        
        # FFmpegコマンドを構築
        filter_complex = []
        inputs = []
        
        for i, scene in enumerate(scenes):
            if "video" in scene:
                inputs.extend(["-i", scene["video"]])
        
        if audio.get("bgm"):
            inputs.extend(["-i", audio["bgm"]])
        
        if audio.get("narration"):
            inputs.extend(["-i", audio["narration"]])
        
        # 実行（デモ用にコマンド表示のみ）
        cmd = [self.ffmpeg_path] + inputs + ["-y", output_path]
        print(f"\n実行コマンド:\n  {' '.join(cmd)}")
        print("\n※ 実際の合成には適切なフィルター設定が必要です")
        
        return True
    
    def create_slideshow(self, images: List[str], duration_per_image: float, 
                          output_path: str, audio_path: str = None) -> bool:
        """画像からスライドショー動画を作成"""
        if not self.check_ffmpeg():
            return False
        
        # 画像リストファイルを作成
        list_file = Path(output_path).parent / "image_list.txt"
        with open(list_file, 'w') as f:
            for img in images:
                f.write(f"file '{img}'\n")
                f.write(f"duration {duration_per_image}\n")
        
        cmd = [
            self.ffmpeg_path,
            "-f", "concat",
            "-safe", "0",
            "-i", str(list_file),
            "-vsync", "vfr",
            "-pix_fmt", "yuv420p"
        ]
        
        if audio_path:
            cmd.extend(["-i", audio_path, "-shortest"])
        
        cmd.extend(["-y", output_path])
        
        print(f"\nスライドショー作成コマンド:\n  {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ スライドショー作成完了: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ エラー: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="動画生成スクリプト")
    subparsers = parser.add_subparsers(dest="command", help="コマンド")
    
    # extract
    extract_parser = subparsers.add_parser("extract", help="フレーム抽出")
    extract_parser.add_argument("--input", "-i", required=True, help="入力動画")
    extract_parser.add_argument("--output", "-o", default="./frames", help="出力ディレクトリ")
    extract_parser.add_argument("--interval", type=int, default=30, help="抽出間隔（秒）")
    extract_parser.add_argument("--keyframes", action="store_true", help="キーフレームのみ抽出")
    
    # storyboard
    story_parser = subparsers.add_parser("storyboard", help="絵コンテ生成")
    story_parser.add_argument("--topic", "-t", required=True, help="トピック")
    story_parser.add_argument("--duration", "-d", type=int, default=60, help="動画尺（秒）")
    story_parser.add_argument("--style", choices=["professional", "casual"], default="professional")
    story_parser.add_argument("--output", "-o", help="出力ファイル")
    story_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    
    # compose
    compose_parser = subparsers.add_parser("compose", help="動画合成")
    compose_parser.add_argument("--config", "-c", required=True, help="設定JSONファイル")
    compose_parser.add_argument("--output", "-o", required=True, help="出力動画")
    
    # slideshow
    slide_parser = subparsers.add_parser("slideshow", help="スライドショー作成")
    slide_parser.add_argument("--images", "-i", required=True, help="画像ディレクトリ")
    slide_parser.add_argument("--duration", "-d", type=float, default=3.0, help="1画像あたりの秒数")
    slide_parser.add_argument("--audio", "-a", help="BGM音声ファイル")
    slide_parser.add_argument("--output", "-o", required=True, help="出力動画")
    
    args = parser.parse_args()
    
    if args.command == "extract":
        extractor = VideoFrameExtractor(args.input)
        info = extractor.get_video_info()
        
        print("\n動画情報:")
        print(json.dumps(info, ensure_ascii=False, indent=2))
        
        print(f"\nフレーム抽出中... (間隔: {args.interval}秒)")
        
        if args.keyframes:
            files = extractor.extract_keyframes(args.output)
        else:
            files = extractor.extract_frames(args.output, args.interval)
        
        print(f"\n抽出完了: {len(files)}フレーム → {args.output}")
    
    elif args.command == "storyboard":
        generator = StoryboardGenerator()
        storyboard = generator.generate(args.topic, args.duration, args.style)
        
        if args.output:
            if args.format == "markdown":
                content = generator.to_markdown(storyboard)
                output_path = args.output if args.output.endswith(".md") else f"{args.output}.md"
            else:
                content = json.dumps(storyboard, ensure_ascii=False, indent=2)
                output_path = args.output if args.output.endswith(".json") else f"{args.output}.json"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 絵コンテ生成: {output_path}")
        else:
            print(generator.to_markdown(storyboard))
    
    elif args.command == "compose":
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        composer = VideoComposer()
        composer.compose(config, args.output)
    
    elif args.command == "slideshow":
        images_dir = Path(args.images)
        images = sorted([
            str(f) for f in images_dir.glob("*")
            if f.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]
        ])
        
        if not images:
            print(f"❌ 画像が見つかりません: {args.images}")
            return
        
        print(f"画像: {len(images)}枚")
        
        composer = VideoComposer()
        composer.create_slideshow(images, args.duration, args.output, args.audio)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
