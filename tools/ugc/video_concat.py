"""
動画クリップの連結モジュール

FFmpegのxfadeフィルターを使ったクロスフェード付き連結と、
シンプルなconcat demuxerによる連結をサポート。
音声ストリームがある場合は acrossfade で自動結合する。
"""

import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg が見つかりません。")


def _get_duration(video_path: str) -> float:
    """動画の長さ（秒）を取得"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def _has_audio(video_path: str) -> bool:
    """動画に音声ストリームがあるか判定"""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return bool(result.stdout.strip())


def concat_simple(clips: list[str], output_path: str) -> None:
    """concat demuxerによるシンプルな連結（トランジションなし）"""
    _ensure_ffmpeg()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for clip in clips:
            f.write(f"file '{Path(clip).resolve().as_posix()}'\n")
        list_path = f.name

    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", list_path,
            "-c", "copy",
            output_path,
        ]
        subprocess.run(cmd, check=True)
    finally:
        os.unlink(list_path)


def concat_with_crossfade(
    clips: list[str],
    output_path: str,
    transition: str = "fade",
    transition_duration: float = 0.5,
) -> None:
    """xfadeフィルターによるクロスフェード付き連結（音声自動検出）

    入力クリップに音声がある場合は acrossfade で音声も結合する。
    音声がない場合は映像のみ結合する。

    Args:
        clips: 動画ファイルパスのリスト（2本以上）
        output_path: 出力先パス
        transition: トランジション種類
            fade, dissolve, wipeleft, wiperight, wipeup, wipedown,
            slideleft, slideright, slideup, slidedown, smoothleft, smoothright
        transition_duration: トランジション時間（秒）
    """
    _ensure_ffmpeg()

    if len(clips) < 2:
        if len(clips) == 1:
            shutil.copy2(clips[0], output_path)
            return
        raise ValueError("クリップが1本もありません")

    # 音声の有無を検出（全クリップに音声がある場合のみ音声を結合）
    has_all_audio = all(_has_audio(c) for c in clips)

    if has_all_audio:
        # 音声ありの場合は concat_with_audio に委譲
        concat_with_audio(clips, output_path, transition, transition_duration)
        return

    # 音声なし: 映像のみ結合（従来のロジック）
    durations = [_get_duration(c) for c in clips]

    # 2本の場合はシンプルなxfade
    if len(clips) == 2:
        offset = durations[0] - transition_duration
        cmd = [
            "ffmpeg", "-y",
            "-i", clips[0],
            "-i", clips[1],
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-preset", "fast",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        return

    # 3本以上: 逐次xfadeチェーン
    inputs = []
    for clip in clips:
        inputs.extend(["-i", clip])

    # filter_complexを構築
    filters = []
    offset = durations[0] - transition_duration
    filters.append(
        f"[0:v][1:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[v1]"
    )

    for i in range(2, len(clips)):
        prev_label = f"v{i-1}"
        out_label = f"v{i}" if i < len(clips) - 1 else "vout"
        offset = sum(durations[:i+1]) - (i * transition_duration) - durations[i]
        filters.append(
            f"[{prev_label}][{i}:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[{out_label}]"
        )

    filter_complex = ";".join(filters)
    final_label = "vout" if len(clips) > 2 else f"v{len(clips)-1}"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{final_label}]",
        "-c:v", "libx264", "-preset", "fast",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def concat_with_audio(
    clips: list[str],
    output_path: str,
    transition: str = "fade",
    transition_duration: float = 0.5,
) -> None:
    """音声付きクリップの連結（映像xfade + 音声acrossfade）

    映像にxfadeトランジション、音声にacrossfadeを適用して連結する。
    """
    _ensure_ffmpeg()

    if len(clips) < 2:
        if len(clips) == 1:
            shutil.copy2(clips[0], output_path)
            return
        raise ValueError("クリップが1本もありません")

    durations = [_get_duration(c) for c in clips]

    if len(clips) == 2:
        offset = durations[0] - transition_duration
        cmd = [
            "ffmpeg", "-y",
            "-i", clips[0],
            "-i", clips[1],
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[v];"
            f"[0:a][1:a]acrossfade=d={transition_duration}[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        return

    # 3本以上: 逐次処理（中間ファイル方式、安定性重視）
    work_dir = Path(tempfile.mkdtemp(prefix="concat_"))
    try:
        current = clips[0]
        for i in range(1, len(clips)):
            out = str(work_dir / f"step_{i}.mp4")
            dur = _get_duration(current)
            offset = dur - transition_duration
            cmd = [
                "ffmpeg", "-y",
                "-i", current,
                "-i", clips[i],
                "-filter_complex",
                f"[0:v][1:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[v];"
                f"[0:a][1:a]acrossfade=d={transition_duration}[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "fast",
                "-c:a", "aac",
                out,
            ]
            subprocess.run(cmd, check=True)
            current = out
        shutil.copy2(current, output_path)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
