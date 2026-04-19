"""
VEED Fabric 1.0 エンジン

Fal.ai経由でVEED Fabric 1.0 APIを呼び出し、
画像と音声からリップシンク動画を生成する。
"""

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


# Fabric 1.0 の料金（$/秒）
FABRIC_COST_PER_SECOND = {
    "480p": 0.08,
    "720p": 0.15,
}


class FabricEngine(BaseEngine):
    """
    VEED Fabric 1.0 エンジン
    
    特徴:
    - 画像 + 音声 → リップシンク動画
    - 高精度なリップシンク
    - 480p: $0.08/秒、720p: $0.15/秒
    """
    
    name = "fabric"
    requires_tts = True
    
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
    
    def generate(
        self,
        avatar_image: str,
        script: str,
        audio_file: Optional[str] = None,
        output_path: Optional[str] = None,
        resolution: str = "720p",
        **kwargs
    ) -> VideoResult:
        """
        Fabric 1.0で動画を生成する
        
        Args:
            avatar_image: アバター画像のパスまたはURL
            script: スクリプト（Fabric 1.0では直接使用しない、音声生成用）
            audio_file: 音声ファイルのパス（必須）
            output_path: 出力先パス
            resolution: 解像度 ("480p" or "720p")
            
        Returns:
            VideoResult: 生成結果
        """
        if audio_file is None:
            raise ValueError("Fabric 1.0 には音声ファイルが必要です")
        
        try:
            import fal_client
        except ImportError:
            raise ImportError("fal-client パッケージがインストールされていません: pip install fal-client")
        
        print(f"🎬 Fabric 1.0 動画生成中... (resolution={resolution})")
        
        # 画像と音声をURLに変換（ローカルファイルの場合はアップロード）
        image_url = self._ensure_url(avatar_image)
        audio_url = self._ensure_url(audio_file)
        
        print(f"   画像URL: {image_url[:50]}...")
        print(f"   音声URL: {audio_url[:50]}...")
        
        try:
            # Fabric 1.0 APIを呼び出し
            result = fal_client.subscribe(
                "veed/fabric-1.0",
                arguments={
                    "image_url": image_url,
                    "audio_url": audio_url,
                    "resolution": resolution,
                },
                with_logs=True,
                on_queue_update=self._on_queue_update,
            )
            
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
            duration = self._get_video_duration(output_path)
            cost = self.estimate_cost(duration, resolution)
            
            print(f"✅ Fabric 1.0 動画生成完了: {output_path}")
            print(f"   長さ: {duration:.1f}秒, コスト: ${cost:.2f}")
            
            return VideoResult(
                video_path=output_path,
                video_url=video_url,
                duration=duration,
                cost=cost,
                engine=self.name,
                metadata={
                    "resolution": resolution,
                    "image_url": image_url,
                    "audio_url": audio_url,
                }
            )
            
        except Exception as e:
            print(f"❌ Fabric 1.0 エラー: {e}")
            raise
    
    def estimate_cost(self, duration_seconds: float, resolution: str = "720p") -> float:
        """コストを見積もる"""
        rate = FABRIC_COST_PER_SECOND.get(resolution, FABRIC_COST_PER_SECOND["720p"])
        return duration_seconds * rate
    
    def _ensure_url(self, path_or_url: str) -> str:
        """パスをURLに変換（必要に応じてアップロード）"""
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        
        # ローカルファイルの場合はFal.aiにアップロード
        try:
            import fal_client
            url = fal_client.upload_file(path_or_url)
            return url
        except Exception as e:
            raise ValueError(f"ファイルのアップロードに失敗: {e}")
    
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
    
    parser = argparse.ArgumentParser(description="Fabric 1.0 動画生成")
    parser.add_argument("image", help="アバター画像のパスまたはURL")
    parser.add_argument("audio", help="音声ファイルのパスまたはURL")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--resolution", "-r", default="720p", choices=["480p", "720p"])
    
    args = parser.parse_args()
    
    engine = FabricEngine()
    result = engine.generate(
        avatar_image=args.image,
        script="",
        audio_file=args.audio,
        output_path=args.output,
        resolution=args.resolution,
    )
    
    print(f"\n結果:")
    print(f"  動画: {result.video_path}")
    print(f"  長さ: {result.duration:.1f}秒")
    print(f"  コスト: ${result.cost:.2f}")
