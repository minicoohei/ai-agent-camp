"""
UGC動画生成エンジン

- VeoEngine: Google Veo 3.1（プロンプトベース）
- FabricEngine: VEED Fabric 1.0（高品質リップシンク）
- HeyGenEngine: HeyGen（安定、スマホテンプレあり）
- LongCatEngine: LongCat（画像+音声→リップシンク、全体動き付き）
- KlingEngine: Kling 2.6 Pro（高品質動画生成）
- ViduEngine: Vidu（高品質、長尺対応）[未実装]
"""

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Optional

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
    "get_engine",
    "generate_with_fallback",
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

# エンジン障害時のフォールバックチェーン
ENGINE_FALLBACK = {
    "fabric": ["kling", "veo"],
    "kling": ["fabric", "veo"],
    "veo": ["kling"],
    "heygen": ["kling", "fabric"],
    "longcat": ["kling"],
    "vidu": ["kling"],
}


def get_engine(name: str) -> BaseEngine:
    """エンジン名からエンジンインスタンスを取得"""
    if name not in ENGINE_MAP:
        raise ValueError(f"Unknown engine: {name}. Available: {list(ENGINE_MAP.keys())}")
    return ENGINE_MAP[name]()


def generate_with_fallback(
    engine_name: str,
    avatar_image: str,
    script: str,
    audio_file: Optional[str] = None,
    output_path: Optional[str] = None,
    timeout: float = 600,
    **kwargs,
) -> VideoResult:
    """指定エンジンで生成し、失敗時はフォールバックチェーンで再試行する

    Args:
        engine_name: 使用するエンジン名
        avatar_image: アバター画像パス
        script: 台本テキスト
        audio_file: TTS 音声ファイルパス
        output_path: 出力先パス
        timeout: タイムアウト秒数
        **kwargs: エンジン固有オプション

    Returns:
        VideoResult: 生成結果（result.engine にどのエンジンが使われたか記録）
    """
    chain = [engine_name] + ENGINE_FALLBACK.get(engine_name, [])
    last_error = None

    for name in chain:
        try:
            print(f"  エンジン: {name} で生成開始...")
            engine = get_engine(name)
            # timeout を強制するため ThreadPoolExecutor 経由で呼び出す
            # （stalled な engine.generate() が fallback chain をブロックしないように）
            # NOTE: context manager を使わない — shutdown(wait=True) がタイムアウト後もブロックするため
            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(
                engine.generate,
                avatar_image=avatar_image,
                script=script,
                audio_file=audio_file,
                output_path=output_path,
                **kwargs,
            )
            try:
                result = future.result(timeout=timeout)
            except FuturesTimeoutError:
                executor.shutdown(wait=False, cancel_futures=True)
                raise
            else:
                executor.shutdown(wait=False)
            result.engine = name
            if name != engine_name:
                print(f"  フォールバック成功: {engine_name} → {name}")
            return result
        except FuturesTimeoutError:
            last_error = RuntimeError(f"{name} timeout after {timeout}s")
            print(f"  エンジン {name} タイムアウト: {timeout}秒")
            time.sleep(2)
            continue
        except Exception as e:
            last_error = e
            print(f"  エンジン {name} 失敗: {e}")
            # API 制限回避のため少し待機
            time.sleep(2)
            continue

    raise RuntimeError(
        f"全エンジンが失敗しました (chain: {chain}): {last_error}"
    )
