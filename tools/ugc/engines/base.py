"""
UGC動画生成エンジンの基底クラス
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VideoResult:
    """動画生成結果"""
    video_path: str
    video_url: Optional[str] = None
    duration: float = 0.0
    cost: float = 0.0
    engine: str = ""
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseEngine(ABC):
    """動画生成エンジンの基底クラス"""
    
    name: str = "base"
    requires_tts: bool = True  # TTSが必要かどうか
    
    def __init__(self):
        self.validate_api_key()
    
    @abstractmethod
    def validate_api_key(self) -> None:
        """APIキーの存在確認"""
        pass
    
    @abstractmethod
    def generate(
        self,
        avatar_image: str,
        script: str,
        audio_file: Optional[str] = None,
        output_path: Optional[str] = None,
        **kwargs
    ) -> VideoResult:
        """
        動画を生成する
        
        Args:
            avatar_image: アバター画像のパスまたはURL
            script: スクリプト（台本）
            audio_file: 音声ファイルのパス（Veoでは不要）
            output_path: 出力先パス
            **kwargs: エンジン固有のオプション
            
        Returns:
            VideoResult: 生成結果
        """
        pass
    
    def estimate_cost(self, duration_seconds: float) -> float:
        """コストを見積もる（サブクラスでオーバーライド）"""
        return 0.0
    
    def _ensure_output_dir(self, output_path: str) -> Path:
        """出力ディレクトリを確保"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    
    def _get_env_var(self, name: str, required: bool = True) -> Optional[str]:
        """環境変数を取得"""
        value = os.environ.get(name)
        if required and not value:
            raise EnvironmentError(f"環境変数 {name} が設定されていません")
        return value
