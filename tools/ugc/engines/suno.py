"""
Suno Music Generation Engine (via fal.ai)

fal.aiのCassetteMusic（Suno互換）またはSunoモデルを使用してAI音楽を生成する。

使い方:
    from tools.ugc.engines.suno import generate_music
    result = generate_music(
        prompt="明るいポップソング、前向きな歌詞",
        duration=60,
    )
    print(result)  # MusicResult(audio_path="...", duration=60, cost=...)
"""

import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class MusicResult:
    audio_path: str
    duration: float
    cost: float
    lyrics: Optional[str] = None
    title: Optional[str] = None


def generate_music(
    prompt: str,
    output_path: Optional[str] = None,
    duration: int = 60,
    instrumental: bool = False,
) -> MusicResult:
    """fal.ai経由でAI音楽を生成

    Args:
        prompt: 音楽の説明（ジャンル、雰囲気、歌詞など）
        output_path: 出力先パス（省略時は自動生成）
        duration: 曲の長さ（秒）
        instrumental: インストゥルメンタルのみ

    Returns:
        MusicResult
    """
    import fal_client

    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        raise EnvironmentError("FAL_KEY が設定されていません")

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3", prefix="suno_")
        os.close(fd)

    # CassetteMusic (fal.ai の音楽生成モデル)
    # 対応エンドポイントが変更される場合があるため、複数のフォールバックを用意
    endpoints = [
        "cassetteai/music-gen",
        "fal-ai/stable-audio",
    ]

    result = None
    last_error = None

    for endpoint in endpoints:
        try:
            capped_duration = min(duration, 180)  # 最大3分
            if "cassette" in endpoint:
                fal_result = fal_client.subscribe(
                    endpoint,
                    arguments={
                        "prompt": prompt,
                        "duration": capped_duration,
                        "instrumental": instrumental,
                    },
                )
            else:
                fal_result = fal_client.subscribe(
                    endpoint,
                    arguments={
                        "prompt": prompt,
                        "seconds_total": capped_duration,
                    },
                )

            # 結果からURLを取得
            audio_url = None
            if isinstance(fal_result, dict):
                audio_url = fal_result.get("audio_url") or fal_result.get("audio", {}).get("url")
                if not audio_url and "output" in fal_result:
                    audio_url = fal_result["output"].get("url")

            if audio_url:
                # ダウンロード
                import urllib.request
                urllib.request.urlretrieve(audio_url, output_path)
                cost = _estimate_cost(capped_duration, endpoint)
                result = MusicResult(
                    audio_path=output_path,
                    duration=duration,
                    cost=cost,
                    lyrics=fal_result.get("lyrics"),
                    title=fal_result.get("title"),
                )
                break

        except Exception as e:
            last_error = e
            continue

    if result is None:
        raise RuntimeError(f"音楽生成に失敗しました: {last_error}")

    return result


def _estimate_cost(duration: int, endpoint: str) -> float:
    """コスト推定"""
    if "cassette" in endpoint:
        return 0.10 * (duration / 30)  # ~$0.10/30秒
    elif "stable-audio" in endpoint:
        return 0.05 * (duration / 30)
    return 0.10


def generate_music_with_lyrics(
    lyrics: str,
    genre: str = "pop",
    mood: str = "upbeat",
    output_path: Optional[str] = None,
    duration: int = 60,
) -> MusicResult:
    """歌詞付きの音楽を生成

    Args:
        lyrics: 歌詞テキスト
        genre: ジャンル（pop, rock, electronic, classical等）
        mood: 雰囲気（upbeat, calm, energetic, melancholic等）
        output_path: 出力先
        duration: 曲の長さ（秒）

    Returns:
        MusicResult
    """
    prompt = f"{genre} song, {mood} mood. Lyrics: {lyrics}"
    return generate_music(
        prompt=prompt,
        output_path=output_path,
        duration=duration,
        instrumental=False,
    )
