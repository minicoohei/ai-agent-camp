"""
Google Veo 3.1 エンジン

Fal.ai経由でGoogle Veo 3.1 APIを呼び出し、
プロンプトベースで動画を生成する。音声も自動生成。
"""

import json
import os
import tempfile
import time
from pathlib import Path
from typing import Optional

import requests

import sys

TOOLS_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS_DIR))
from runtime_env import load_runtime_env

from .base import BaseEngine, VideoResult

load_runtime_env(TOOLS_DIR.parent)


# Veo 3.1 の料金
# 8秒動画で約$4（480p）〜$8（720p）
VEO_COST_PER_8SEC = {
    "480p": 4.0,
    "720p": 8.0,
}


class VeoEngine(BaseEngine):
    """
    Google Veo 3.1 エンジン
    
    特徴:
    - プロンプトベースの動画生成
    - 音声も自動生成（TTS不要）
    - 最高品質
    - 約$12/30秒（720p）
    """
    
    name = "veo"
    requires_tts = False  # Veo 3.1は音声も生成する
    
    def __init__(self):
        super().__init__()
        self.fal_key = self._get_env_var("FAL_KEY")
    
    def validate_api_key(self) -> None:
        """APIキーの存在確認"""
        if not os.environ.get("FAL_KEY"):
            raise EnvironmentError(
                "FAL_KEY が設定されていません。\n"
                "https://fal.ai/dashboard で取得してください。"
            )
    
    @staticmethod
    def _normalize_duration(duration: int) -> int:
        """Veo 3.1の許可されたdurationに正規化（4, 6, 8秒のみ）"""
        allowed = [4, 6, 8]
        # 最も近い許可された値を選択
        return min(allowed, key=lambda x: abs(x - duration))
    
    def generate(
        self,
        avatar_image: str,
        script: str,
        audio_file: Optional[str] = None,
        output_path: Optional[str] = None,
        resolution: str = "720p",
        duration: int = 8,
        avatar_style: str = "friendly young person",
        setting: str = "casual indoor",
        **kwargs
    ) -> VideoResult:
        """
        Veo 3.1で動画を生成する
        
        Args:
            avatar_image: アバター画像のパス（参考用、Veoでは使わない可能性あり）
            script: スクリプト（プロンプトに組み込まれる）
            audio_file: 音声ファイル（Veo 3.1では不要）
            output_path: 出力先パス
            resolution: 解像度 ("480p" or "720p")
            duration: 動画の長さ（秒、最大8秒）
            avatar_style: アバターのスタイル説明
            setting: 背景設定の説明
            
        Returns:
            VideoResult: 生成結果
        """
        try:
            import fal_client
        except ImportError:
            raise ImportError("fal-client パッケージがインストールされていません: pip install fal-client")
        
        # Veo 3.1の許可されたdurationに正規化
        original_duration = duration
        duration = self._normalize_duration(duration)
        if original_duration != duration:
            print(f"⚠️ duration {original_duration}s → {duration}s に調整（Veo制限: 4/6/8秒）")
        
        print(f"🎬 Veo 3.1 動画生成中... (duration={duration}s, resolution={resolution})")
        
        # スクリプトの最初の部分をプレビューとして使用
        script_preview = script[:200] + "..." if len(script) > 200 else script
        
        # プロンプトを構築
        prompt = self._build_prompt(
            script=script,
            script_preview=script_preview,
            avatar_style=avatar_style,
            setting=setting,
            duration=duration,
        )
        
        print(f"   プロンプト: {prompt[:100]}...")
        
        try:
            # アバター画像を参照画像として使用（image-to-video）
            if avatar_image and Path(avatar_image).exists():
                image_url = self._ensure_url(avatar_image)
                result = self._generate_with_image(fal_client, prompt, image_url, duration)
            else:
                # テキストのみで生成
                result = self._generate_text_only(fal_client, prompt, duration)
            
            video_url = result.get("video", {}).get("url")
            if not video_url:
                raise ValueError("動画URLが取得できませんでした")
            
            # 動画をダウンロード
            if output_path is None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    output_path = tmp.name
            else:
                self._ensure_output_dir(output_path)
            
            self._download_video(video_url, output_path)
            
            # 動画の長さを取得
            actual_duration = self._get_video_duration(output_path)
            cost = self.estimate_cost(actual_duration, resolution)
            
            print(f"✅ Veo 3.1 動画生成完了: {output_path}")
            print(f"   長さ: {actual_duration:.1f}秒, コスト: ${cost:.2f}")
            
            return VideoResult(
                video_path=output_path,
                video_url=video_url,
                duration=actual_duration,
                cost=cost,
                engine=self.name,
                metadata={
                    "prompt": prompt,
                    "resolution": resolution,
                    "requested_duration": duration,
                }
            )
            
        except Exception as e:
            print(f"❌ Veo 3.1 エラー: {e}")
            raise
    
    def estimate_cost(self, duration_seconds: float, resolution: str = "720p") -> float:
        """コストを見積もる"""
        # Veo 3.1は8秒単位の料金
        cost_per_8sec = VEO_COST_PER_8SEC.get(resolution, VEO_COST_PER_8SEC["720p"])
        num_8sec_segments = (duration_seconds + 7) // 8  # 切り上げ
        return num_8sec_segments * cost_per_8sec
    
    def _build_prompt(
        self,
        script: str,
        script_preview: str,
        avatar_style: str,
        setting: str,
        duration: int,
    ) -> str:
        """Veo用のプロンプトを構築"""
        # スクリプトから感情を推測
        emotion = self._detect_emotion(script)
        
        prompt = f"""
A {avatar_style} speaking directly to the camera with {emotion} expression, 
holding a smartphone toward the viewer. The smartphone screen displays a solid 
bright green color (#00FF00) for chroma key compositing.

The person is enthusiastically saying: "{script_preview}"

Setting: {setting} with warm, natural lighting.
The person maintains eye contact with the camera, gestures naturally while speaking,
and shows genuine enthusiasm about what they're explaining.

Duration: {duration} seconds.
Style: Realistic, natural conversation, UGC-style content.
"""
        return prompt.strip()
    
    def _detect_emotion(self, script: str) -> str:
        """スクリプトから感情を推測"""
        # 簡易的な感情検出
        positive_words = ["すごい", "最高", "便利", "革命", "変わった", "amazing", "incredible"]
        question_words = ["？", "?", "知ってる", "思う"]
        
        script_lower = script.lower()
        
        if any(word in script for word in positive_words):
            return "excited and enthusiastic"
        elif any(word in script for word in question_words):
            return "curious and engaging"
        else:
            return "friendly and confident"
    
    def _ensure_url(self, path_or_url: str) -> str:
        """パスをURLに変換（必要に応じてアップロード）"""
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        
        try:
            import fal_client
            url = fal_client.upload_file(path_or_url)
            return url
        except Exception as e:
            raise ValueError(f"ファイルのアップロードに失敗: {e}")
    
    def _generate_with_image(self, fal_client, prompt: str, image_url: str, duration: int) -> dict:
        """画像を参照して動画を生成"""
        print(f"   画像参照モードで生成中...")
        
        # Veo 3.1 image-to-video
        result = fal_client.subscribe(
            "fal-ai/veo3",
            arguments={
                "prompt": prompt,
                "image_url": image_url,
                "duration": min(duration, 8),  # 最大8秒
                "aspect_ratio": "9:16",  # 縦長（TikTok/Reels向け）
            },
            with_logs=True,
            on_queue_update=self._on_queue_update,
        )
        return result
    
    def _generate_text_only(self, fal_client, prompt: str, duration: int) -> dict:
        """テキストのみで動画を生成"""
        print(f"   テキストのみモードで生成中...")
        
        result = fal_client.subscribe(
            "fal-ai/veo3",
            arguments={
                "prompt": prompt,
                "duration": min(duration, 8),
                "aspect_ratio": "9:16",
            },
            with_logs=True,
            on_queue_update=self._on_queue_update,
        )
        return result
    
    def _on_queue_update(self, update):
        """キュー更新時のコールバック"""
        if hasattr(update, 'status'):
            print(f"   ステータス: {update.status}", end="\r")
        if hasattr(update, 'logs') and update.logs:
            for log in update.logs:
                if hasattr(log, 'message'):
                    print(f"   {log.message}")
    
    def _download_video(self, url: str, output_path: str) -> None:
        """動画をダウンロード"""
        print(f"   動画をダウンロード中...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def _get_video_duration(self, video_path: str) -> float:
        """動画の長さを取得"""
        # MoviePyを優先的に使用（cv2のnumpy互換性問題回避）
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except Exception:
            pass
        
        # フォールバック: cv2
        try:
            import cv2
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            if fps > 0:
                return frame_count / fps
        except Exception:
            pass
        return 0.0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Veo 3.1 動画生成")
    parser.add_argument("script", help="スクリプト（話す内容）")
    parser.add_argument("--image", "-i", help="参照画像のパス（オプション）")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--duration", "-d", type=int, default=8, help="動画の長さ（秒、最大8）")
    parser.add_argument("--resolution", "-r", default="720p", choices=["480p", "720p"])
    parser.add_argument("--style", default="friendly young person", help="アバターのスタイル")
    parser.add_argument("--setting", default="casual indoor", help="背景設定")
    
    args = parser.parse_args()
    
    engine = VeoEngine()
    result = engine.generate(
        avatar_image=args.image or "",
        script=args.script,
        output_path=args.output,
        duration=args.duration,
        resolution=args.resolution,
        avatar_style=args.style,
        setting=args.setting,
    )
    
    print(f"\n結果:")
    print(f"  動画: {result.video_path}")
    print(f"  長さ: {result.duration:.1f}秒")
    print(f"  コスト: ${result.cost:.2f}")
