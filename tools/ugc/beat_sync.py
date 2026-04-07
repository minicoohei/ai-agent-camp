"""
Beat Sync Module - 音楽のビート解析と動画同期

librosa を使用して音楽ファイルのビート・テンポ・セクションを解析し、
動画のシーン切替タイミングを生成する。

依存: pip install librosa

使い方:
    from tools.ugc.beat_sync import analyze_beats, generate_beat_timeline

    beats = analyze_beats("music.mp3")
    timeline = generate_beat_timeline(beats, num_scenes=8)
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class BeatAnalysis:
    """ビート解析結果"""
    tempo: float
    beat_times: list[float] = field(default_factory=list)
    downbeat_times: list[float] = field(default_factory=list)
    duration: float = 0.0
    sections: list[dict] = field(default_factory=list)


@dataclass
class SceneTimestamp:
    """シーン切替タイムスタンプ"""
    scene_index: int
    start_time: float
    end_time: float
    duration: float
    beat_count: int
    is_chorus: bool = False


def analyze_beats(audio_path: str) -> BeatAnalysis:
    """音楽ファイルのビート解析

    Args:
        audio_path: 音楽ファイルパス（MP3, WAV等）

    Returns:
        BeatAnalysis
    """
    try:
        import librosa
    except ImportError:
        raise ImportError(
            "librosa が必要です。インストール: pip install librosa"
        )

    # 音声読み込み
    y, sr = librosa.load(audio_path, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)

    # テンポとビート検出
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # ダウンビート検出（強拍）
    # 4拍子を仮定して4拍ごとにダウンビート
    downbeat_times = [beat_times[i] for i in range(0, len(beat_times), 4)]

    # セクション推定（エネルギーベース）
    sections = _estimate_sections(y, sr, duration)

    return BeatAnalysis(
        tempo=float(tempo) if hasattr(tempo, '__float__') else float(tempo[0]) if hasattr(tempo, '__getitem__') else 120.0,
        beat_times=beat_times,
        downbeat_times=downbeat_times,
        duration=duration,
        sections=sections,
    )


def _estimate_sections(y, sr, duration: float) -> list[dict]:
    """エネルギーに基づくセクション推定"""
    import librosa
    import numpy as np

    # RMSエネルギーを計算
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr)

    # 簡易セクション分割（エネルギーの変化点）
    # 10秒ウィンドウでエネルギーの平均を計算
    window_sec = 10
    window_frames = int(window_sec * sr / 512)

    sections = []
    current_start = 0.0
    current_energy = "low"

    for i in range(0, len(rms), window_frames):
        segment_rms = np.mean(rms[i:i + window_frames])
        energy = "high" if segment_rms > np.median(rms) else "low"

        if energy != current_energy and i > 0:
            t = float(times[min(i, len(times) - 1)])
            sections.append({
                "start": current_start,
                "end": t,
                "energy": current_energy,
                "label": "chorus" if current_energy == "high" else "verse",
            })
            current_start = t
            current_energy = energy

    # 最後のセクション
    sections.append({
        "start": current_start,
        "end": duration,
        "energy": current_energy,
        "label": "chorus" if current_energy == "high" else "verse",
    })

    return sections


def generate_beat_timeline(
    analysis: BeatAnalysis,
    num_scenes: int = 8,
    min_scene_duration: float = 3.0,
) -> list[SceneTimestamp]:
    """ビート解析からシーン切替タイムラインを生成

    Args:
        analysis: ビート解析結果
        num_scenes: シーン数
        min_scene_duration: 最小シーン長（秒）

    Returns:
        シーンタイムスタンプのリスト
    """
    duration = analysis.duration
    beats = analysis.beat_times
    sections = analysis.sections

    if not beats:
        # ビートなしの場合は均等分割
        scene_duration = duration / num_scenes
        return [
            SceneTimestamp(
                scene_index=i,
                start_time=i * scene_duration,
                end_time=(i + 1) * scene_duration,
                duration=scene_duration,
                beat_count=0,
            )
            for i in range(num_scenes)
        ]

    # ダウンビートを基準にシーン分割
    downbeats = analysis.downbeat_times
    if len(downbeats) < num_scenes:
        downbeats = beats

    # 目標シーン長
    target_duration = duration / num_scenes

    scenes = []
    current_start = 0.0
    scene_idx = 0

    for db_time in downbeats:
        if scene_idx >= num_scenes - 1:
            break

        elapsed = db_time - current_start
        if elapsed >= target_duration * 0.8 and elapsed >= min_scene_duration:
            # このダウンビートでシーン切替
            beat_count = len([b for b in beats if current_start <= b < db_time])
            is_chorus = any(
                s.get("label") == "chorus" and s["start"] <= current_start < s["end"]
                for s in sections
            )
            scenes.append(SceneTimestamp(
                scene_index=scene_idx,
                start_time=current_start,
                end_time=db_time,
                duration=db_time - current_start,
                beat_count=beat_count,
                is_chorus=is_chorus,
            ))
            current_start = db_time
            scene_idx += 1

    # 最後のシーン
    beat_count = len([b for b in beats if current_start <= b < duration])
    scenes.append(SceneTimestamp(
        scene_index=scene_idx,
        start_time=current_start,
        end_time=duration,
        duration=duration - current_start,
        beat_count=beat_count,
        is_chorus=False,
    ))

    # シーン数が足りない場合は均等分割で補完
    while len(scenes) < num_scenes:
        longest = max(scenes, key=lambda s: s.duration)
        idx = scenes.index(longest)
        mid = longest.start_time + longest.duration / 2
        # 分割
        first_half = SceneTimestamp(
            scene_index=longest.scene_index,
            start_time=longest.start_time,
            end_time=mid,
            duration=mid - longest.start_time,
            beat_count=longest.beat_count // 2,
            is_chorus=longest.is_chorus,
        )
        second_half = SceneTimestamp(
            scene_index=longest.scene_index + 1,
            start_time=mid,
            end_time=longest.end_time,
            duration=longest.end_time - mid,
            beat_count=longest.beat_count - longest.beat_count // 2,
            is_chorus=longest.is_chorus,
        )
        scenes[idx] = first_half
        scenes.insert(idx + 1, second_half)

    # インデックスを振り直し
    for i, scene in enumerate(scenes):
        scene.scene_index = i

    return scenes[:num_scenes]


def save_analysis(analysis: BeatAnalysis, output_path: str) -> None:
    """ビート解析結果をJSONに保存"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(asdict(analysis), f, ensure_ascii=False, indent=2)


def save_timeline(timeline: list[SceneTimestamp], output_path: str) -> None:
    """タイムラインをJSONに保存"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(s) for s in timeline], f, ensure_ascii=False, indent=2)
