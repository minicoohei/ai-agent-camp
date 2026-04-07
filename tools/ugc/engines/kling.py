"""
Kling 2.6 Pro エンジン

Fal.ai経由でKling 2.6 Pro Image-to-Video APIを呼び出し、
画像から動画を生成する（音声生成は任意）。
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

import requests

import sys

TOOLS_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS_DIR))
from runtime_env import load_runtime_env

from .base import BaseEngine, VideoResult

load_runtime_env(TOOLS_DIR.parent)


# Kling 2.6 Pro の料金（$/秒）
KLING_COST_PER_SECOND = {
    "audio_off": 0.07,
    "audio_on": 0.14,
}


class KlingEngine(BaseEngine):
    """
    Kling 2.6 Pro エンジン

    特徴:
    - 画像 → 動画（Image-to-Video）
    - 5秒 or 10秒の固定長
    - 音声生成は任意（生成オンで倍額）
    """

    name = "kling"
    requires_tts = False

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
        """Kling 2.6の許可されたdurationに正規化（5, 10秒のみ）"""
        allowed = [5, 10]
        return min(allowed, key=lambda x: abs(x - duration))

    def generate(
        self,
        avatar_image: str,
        script: str,
        audio_file: Optional[str] = None,
        output_path: Optional[str] = None,
        duration: int = 10,
        generate_audio: bool = False,
        **kwargs,
    ) -> VideoResult:
        """
        Kling 2.6 Proで動画を生成する

        Args:
            avatar_image: 参照画像のパスまたはURL（必須）
            script: スクリプト（プロンプトに組み込む）
            audio_file: 未使用（Klingはネイティブ音声生成のみ）
            output_path: 出力先パス
            duration: 動画の長さ（秒、5 or 10）
            generate_audio: 音声生成を有効にするか

        Returns:
            VideoResult: 生成結果
        """
        if not avatar_image:
            raise ValueError("Kling 2.6 Pro には参照画像が必要です")

        try:
            import fal_client
        except ImportError:
            raise ImportError("fal-client パッケージがインストールされていません: pip install fal-client")

        original_duration = duration
        duration = self._normalize_duration(duration)
        if original_duration != duration:
            print(f"⚠️ duration {original_duration}s → {duration}s に調整（Kling制限: 5/10秒）")

        print(
            f"🎬 Kling 2.6 Pro 動画生成中... "
            f"(duration={duration}s, audio={'on' if generate_audio else 'off'})"
        )

        # スクリプトを短くプレビュー化（過度に長い場合の安全策）
        script_preview = script[:240] + "..." if len(script) > 240 else script

        prompt = self._build_prompt(script_preview)

        image_url = self._ensure_url(avatar_image)

        result = fal_client.subscribe(
            "fal-ai/kling-video/v2.6/pro/image-to-video",
            arguments={
                "prompt": prompt,
                "start_image_url": image_url,
                "generate_audio": generate_audio,
                "duration": duration,
            },
            with_logs=True,
            on_queue_update=self._on_queue_update,
        )

        video_url = result.get("video", {}).get("url")
        if not video_url:
            raise ValueError(f"動画URLが取得できませんでした: {result}")

        if output_path is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                output_path = tmp.name
        else:
            self._ensure_output_dir(output_path)

        self._download_video(video_url, output_path)

        # 依存ライブラリに影響されないよう、要求したdurationを使用
        actual_duration = float(duration)
        cost = self.estimate_cost(actual_duration, generate_audio)

        print(f"✅ Kling 2.6 Pro 動画生成完了: {output_path}")
        print(f"   長さ: {actual_duration:.1f}秒, コスト: ${cost:.2f}")

        return VideoResult(
            video_path=output_path,
            video_url=video_url,
            duration=actual_duration,
            cost=cost,
            engine=self.name,
            metadata={
                "prompt": prompt,
                "image_url": image_url,
                "generate_audio": generate_audio,
                "requested_duration": duration,
            },
        )

    def estimate_cost(self, duration_seconds: float, generate_audio: bool = False) -> float:
        """コストを見積もる（秒課金）"""
        rate = KLING_COST_PER_SECOND["audio_on" if generate_audio else "audio_off"]
        return duration_seconds * rate

    def _build_prompt(self, script_preview: str) -> str:
        """Kling用のプロンプトを構築"""
        prompt = f"""
A friendly young person in their 20s presenting a smartphone to the viewer.
The person actively shows and tilts the phone screen toward the camera, demonstrating the content on screen.
The smartphone screen displays a solid bright green color (#00FF00) for chroma key compositing.
Natural body language with moderate gestures - occasionally pointing at the screen, nodding, and making eye contact.
The person speaks engagingly: "{script_preview}"
Smooth camera-facing phone movements, UGC demo-style presentation.
"""
        return prompt.strip()

    def _ensure_url(self, path_or_url: str) -> str:
        """パスをURLに変換（必要に応じてアップロード）"""
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        try:
            import fal_client
            return fal_client.upload_file(path_or_url)
        except Exception as e:
            raise ValueError(f"ファイルのアップロードに失敗: {e}")

    def _on_queue_update(self, update):
        """キュー更新時のコールバック"""
        if hasattr(update, "status"):
            print(f"   ステータス: {update.status}", end="\r")
        if hasattr(update, "logs") and update.logs:
            for log in update.logs:
                if hasattr(log, "message"):
                    print(f"   {log.message}")

    def _download_video(self, url: str, output_path: str) -> None:
        """動画をダウンロード"""
        print("   動画をダウンロード中...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def _get_video_duration(self, video_path: str) -> float:
        """動画の長さを取得"""
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(video_path)
            duration = clip.duration
            clip.close()
            return duration
        except Exception:
            pass

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
