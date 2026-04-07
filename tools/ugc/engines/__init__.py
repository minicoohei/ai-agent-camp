"""
UGC動画生成エンジン

- VeoEngine: Google Veo 3.1（プロンプトベース）
- FabricEngine: VEED Fabric 1.0（高品質リップシンク）
- HeyGenEngine: HeyGen（安定、スマホテンプレあり）
- LongCatEngine: LongCat（画像+音声→リップシンク、全体動き付き）
- KlingEngine: Kling 2.6 Pro（高品質動画生成）
- ViduEngine: Vidu（高品質、長尺対応）[未実装]
"""

from .base import BaseEngine, VideoResult
from .veo import VeoEngine
from .fabric import FabricEngine
from .heygen import HeyGenEngine
from .longcat import LongCatEngine
from .kling import KlingEngine
from .vidu import ViduEngine

__all__ = [
    "BaseEngine",
    "VideoResult",
    "VeoEngine",
    "FabricEngine",
    "HeyGenEngine",
    "LongCatEngine",
    "KlingEngine",
    "ViduEngine",
]

# エンジン名からクラスへのマッピング
ENGINE_MAP = {
    "veo": VeoEngine,
    "fabric": FabricEngine,
    "heygen": HeyGenEngine,
    "longcat": LongCatEngine,
    "kling": KlingEngine,
    "vidu": ViduEngine,
}


def get_engine(name: str) -> BaseEngine:
    """エンジン名からエンジンインスタンスを取得"""
    if name not in ENGINE_MAP:
        raise ValueError(f"Unknown engine: {name}. Available: {list(ENGINE_MAP.keys())}")
    return ENGINE_MAP[name]()
