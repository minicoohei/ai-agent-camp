"""
UGC Factory - AI動画生成モジュール

Veo 3.1、Fabric 1.0、HeyGenの3つのエンジンを切り替えて使える
AI UGC動画生成ツール群。

HeyGen + ElevenLabs + Nano Banana Pro の統合パイプラインも提供。
"""

from .script_generator import generate_ugc_script
from .tts import generate_speech

# composite_videoは遅延インポート（cv2/numpy互換性問題回避）
def composite_video(*args, **kwargs):
    """グリーンスクリーン合成（遅延インポート）"""
    from .compositor import composite_video as _composite_video
    return _composite_video(*args, **kwargs)


# HeyGen パイプライン関数（遅延インポート）
def generate_avatar_with_screenshot(*args, **kwargs):
    """Nano Banana Proでスクショ埋め込みアバター画像を生成（遅延インポート）"""
    from .heygen_pipeline import generate_avatar_with_screenshot as _func
    return _func(*args, **kwargs)


def generate_heygen_video(*args, **kwargs):
    """ElevenLabs + HeyGenでリップシンク動画を生成（遅延インポート）"""
    from .heygen_pipeline import generate_heygen_video as _func
    return _func(*args, **kwargs)


def heygen_full_pipeline(*args, **kwargs):
    """HeyGenフルパイプライン: スクショ→アバター→音声→動画（遅延インポート）"""
    from .heygen_pipeline import full_pipeline as _func
    return _func(*args, **kwargs)


__all__ = [
    "generate_ugc_script",
    "generate_speech", 
    "composite_video",
    # HeyGen パイプライン
    "generate_avatar_with_screenshot",
    "generate_heygen_video",
    "heygen_full_pipeline",
]
