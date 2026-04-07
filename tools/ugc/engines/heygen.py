"""
HeyGen エンジン

HeyGen APIを使用してアバター動画を生成する。
スマホを持ったテンプレートあり、安定した品質。
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


# HeyGen API エンドポイント
HEYGEN_API_BASE_V1 = "https://api.heygen.com/v1"
HEYGEN_API_BASE_V2 = "https://api.heygen.com/v2"

# 推定コスト（クレジット制のため概算）
HEYGEN_COST_PER_SECOND = 0.05  # 概算


class HeyGenEngine(BaseEngine):
    """
    HeyGen エンジン
    
    特徴:
    - 画像 + 音声 → リップシンク動画
    - スマホを持ったテンプレートあり
    - 安定した品質
    - 約$1〜2/30秒
    """
    
    name = "heygen"
    requires_tts = True
    
    def __init__(self):
        super().__init__()
        self.api_key = self._get_env_var("HEYGEN_API_KEY")
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
    
    def validate_api_key(self) -> None:
        """APIキーの存在確認"""
        if not os.environ.get("HEYGEN_API_KEY"):
            raise EnvironmentError(
                "HEYGEN_API_KEY が設定されていません。\n"
                "https://app.heygen.com/settings で取得してください。"
            )
    
    def generate(
        self,
        avatar_image: str,
        script: str,
        audio_file: Optional[str] = None,
        output_path: Optional[str] = None,
        voice_id: Optional[str] = None,
        avatar_id: Optional[str] = None,
        **kwargs
    ) -> VideoResult:
        """
        HeyGenで動画を生成する
        
        Args:
            avatar_image: アバター画像のパス（現在はビルトインアバター使用のため無視）
            script: スクリプト（HeyGenの場合、TTSを使うかaudio_fileを使う）
            audio_file: 音声ファイルのパス（指定時はこちらを使用）
            output_path: 出力先パス
            voice_id: HeyGenのボイスID（audio_fileがない場合に使用）
            avatar_id: HeyGenのビルトインアバターID（指定なしの場合はデフォルト）
            
        Returns:
            VideoResult: 生成結果
        """
        print(f"🎬 HeyGen 動画生成中...")
        
        # デフォルトのビルトインアバター（日本人女性風）
        if avatar_id is None:
            avatar_id = "Kristin_public_2_20240108"  # 自然な女性アバター
        
        print(f"   アバターID: {avatar_id}")
        
        try:
            # 音声URLを準備
            if audio_file:
                # 外部URLにアップロード（tmpfiles.org経由）
                audio_url = self._upload_to_tmpfiles(audio_file)
                print(f"   音声アップロード完了")
                use_audio = True
            else:
                audio_url = None
                use_audio = False
            
            # 動画生成リクエスト
            video_id = self._create_video_with_avatar(
                avatar_id=avatar_id,
                script=script,
                audio_url=audio_url,
                voice_id=voice_id,
                use_audio=use_audio,
            )
            
            print(f"   動画生成開始 (ID: {video_id})")
            
            # 完了を待機
            video_url = self._wait_for_video(video_id)
            
            # 動画をダウンロード
            if output_path is None:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    output_path = tmp.name
            else:
                self._ensure_output_dir(output_path)
            
            self._download_video(video_url, output_path)
            
            # 動画の長さを取得
            duration = self._get_video_duration(output_path)
            cost = self.estimate_cost(duration)
            
            print(f"✅ HeyGen 動画生成完了: {output_path}")
            print(f"   長さ: {duration:.1f}秒, 推定コスト: ${cost:.2f}")
            
            return VideoResult(
                video_path=output_path,
                video_url=video_url,
                duration=duration,
                cost=cost,
                engine=self.name,
                metadata={
                    "video_id": video_id,
                    "avatar_id": avatar_id,
                    "audio_url": audio_url,
                }
            )
            
        except Exception as e:
            print(f"❌ HeyGen エラー: {e}")
            raise
    
    def estimate_cost(self, duration_seconds: float) -> float:
        """コストを見積もる（概算）"""
        return duration_seconds * HEYGEN_COST_PER_SECOND
    
    def _upload_to_tmpfiles(self, path_or_url: str) -> str:
        """
        tmpfiles.orgにファイルをアップロードしてURLを取得
        
        Returns:
            ファイルのURL
        """
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        
        from pathlib import Path
        
        print(f"   ファイルをアップロード中: {path_or_url}")
        
        filename = Path(path_or_url).name
        
        with open(path_or_url, "rb") as f:
            file_content = f.read()
        
        response = requests.post(
            "https://tmpfiles.org/api/v1/upload",
            files={"file": (filename, file_content)},
        )
        
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "success":
            raise ValueError(f"アップロードエラー: {data}")
        
        # tmpfiles.orgのURLを直接リンクに変換
        file_url = data.get("data", {}).get("url", "")
        file_url = file_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
        
        print(f"   アップロード完了: {file_url}")
        return file_url
    
    def _create_video_with_avatar(
        self,
        avatar_id: str,
        script: str,
        audio_url: Optional[str] = None,
        voice_id: Optional[str] = None,
        use_audio: bool = False,
    ) -> str:
        """ビルトインアバターを使用して動画生成リクエストを送信"""
        url = f"{HEYGEN_API_BASE_V2}/video/generate"
        
        # リクエストボディを構築
        if use_audio and audio_url:
            # 外部音声ファイルを使用
            payload = {
                "video_inputs": [{
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "avatar_style": "normal",
                    },
                    "voice": {
                        "type": "audio",
                        "audio_url": audio_url,
                    },
                }],
                "dimension": {
                    "width": 720,
                    "height": 1280,
                },
            }
        else:
            # HeyGenのTTSを使用
            payload = {
                "video_inputs": [{
                    "character": {
                        "type": "avatar",
                        "avatar_id": avatar_id,
                        "avatar_style": "normal",
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script,
                        "voice_id": voice_id or "1bd001e7e50f421d891986aad5158bc8",  # 日本語女性ボイス
                    },
                }],
                "dimension": {
                    "width": 720,
                    "height": 1280,
                },
            }
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        # エラー時にレスポンス内容を表示
        if response.status_code != 200:
            print(f"   HeyGen API Error: {response.status_code}")
            print(f"   Response: {response.text}")
        
        response.raise_for_status()
        data = response.json()
        
        if data.get("error"):
            raise ValueError(f"動画生成エラー: {data['error']}")
        
        return data.get("data", {}).get("video_id", "")
    
    def _wait_for_video(self, video_id: str, timeout: int = 600) -> str:
        """動画の生成完了を待機"""
        url = f"{HEYGEN_API_BASE_V1}/video_status.get"
        
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"動画生成がタイムアウトしました ({timeout}秒)")
            
            response = requests.get(
                url,
                headers=self.headers,
                params={"video_id": video_id},
            )
            response.raise_for_status()
            data = response.json()
            
            status = data.get("data", {}).get("status", "")
            
            if status == "completed":
                video_url = data.get("data", {}).get("video_url", "")
                if video_url:
                    return video_url
                raise ValueError("動画URLが取得できませんでした")
            
            elif status == "failed":
                error = data.get("data", {}).get("error", "不明なエラー")
                raise ValueError(f"動画生成失敗: {error}")
            
            # 進捗表示
            progress = data.get("data", {}).get("progress", 0)
            print(f"   進捗: {progress}%", end="\r")
            
            time.sleep(5)
    
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
    
    def list_voices(self) -> list:
        """利用可能なボイス一覧を取得"""
        url = f"{HEYGEN_API_BASE_V2}/voices"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        return data.get("data", {}).get("voices", [])


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="HeyGen 動画生成")
    parser.add_argument("image", help="アバター画像のパスまたはURL")
    parser.add_argument("--audio", "-a", help="音声ファイルのパス")
    parser.add_argument("--script", "-s", help="スクリプト（音声なしの場合）")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--list-voices", action="store_true", help="ボイス一覧を表示")
    
    args = parser.parse_args()
    
    engine = HeyGenEngine()
    
    if args.list_voices:
        voices = engine.list_voices()
        print("利用可能なボイス:")
        for voice in voices[:20]:  # 最初の20件
            print(f"  {voice.get('voice_id')}: {voice.get('name')}")
    else:
        if not args.audio and not args.script:
            parser.error("--audio または --script が必要です")
        
        result = engine.generate(
            avatar_image=args.image,
            script=args.script or "",
            audio_file=args.audio,
            output_path=args.output,
        )
        
        print(f"\n結果:")
        print(f"  動画: {result.video_path}")
        print(f"  長さ: {result.duration:.1f}秒")
        print(f"  推定コスト: ${result.cost:.2f}")
