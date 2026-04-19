"""
Vidu エンジン（プレースホルダー）

Viduは高品質な動画生成エンジン。
現在は未実装。実装予定。
"""

import os
from typing import Optional

from .base import BaseEngine, VideoResult


class ViduEngine(BaseEngine):
    """
    Vidu エンジン
    
    特徴:
    - 高品質な動画生成
    - 長尺動画のサポート
    - 画像 + 音声 → 動画
    
    TODO: 実装予定
    """
    
    name = "vidu"
    requires_tts = True
    
    def __init__(self):
        # API キーの検証はスキップ（未実装のため）
        pass
    
    def validate_api_key(self) -> None:
        """APIキーの存在確認"""
        # TODO: Vidu API キーの検証を実装
        pass
    
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
        Viduで動画を生成する（未実装）
        
        Args:
            avatar_image: アバター画像のパスまたはURL
            script: スクリプト
            audio_file: 音声ファイルのパス
            output_path: 出力先パス
            resolution: 解像度
            
        Returns:
            VideoResult: 生成結果
            
        Raises:
            NotImplementedError: 未実装のため
        """
        raise NotImplementedError(
            "Viduエンジンは現在未実装です。\n"
            "代わりに 'fabric' または 'veo' エンジンを使用してください。\n"
            "実装が完了次第、このメッセージは削除されます。"
        )
    
    def estimate_cost(self, duration_seconds: float, resolution: str = "720p") -> float:
        """コストを見積もる（未実装）"""
        # TODO: Vidu の料金体系に合わせて実装
        return 0.0


if __name__ == "__main__":
    print("Viduエンジンは現在未実装です。")
    print("使用可能なエンジン: fabric, veo, heygen, kling")
