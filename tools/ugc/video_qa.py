"""
動画出力のバリデーションモジュール

ffprobe で最終出力を検証し、品質チェック用フレームを抽出する。
各パイプラインの最終ステップで呼び出す。
"""

import json
import subprocess
import shutil
from pathlib import Path
from typing import Optional


class VideoQAError(Exception):
    """動画品質チェックエラー"""
    pass


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg が見つかりません。")


def validate_video_output(
    video_path: str,
    expect_audio: bool = True,
    min_duration: float = 1.0,
    max_duration: float = 600.0,
) -> dict:
    """最終出力動画を検証する

    Args:
        video_path: 検証する動画ファイルのパス
        expect_audio: 音声ストリームを期待するか
        min_duration: 最小尺（秒）
        max_duration: 最大尺（秒）

    Returns:
        検証結果 dict: {status, duration, has_video, has_audio, resolution, issues}

    Raises:
        VideoQAError: 致命的な問題がある場合
    """
    _ensure_ffmpeg()

    path = Path(video_path)
    if not path.exists():
        raise VideoQAError(f"ファイルが存在しません: {video_path}")

    if path.stat().st_size == 0:
        raise VideoQAError(f"ファイルサイズが0です: {video_path}")

    # ffprobe でストリーム情報を取得
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=index,codec_type,codec_name,width,height,duration,r_frame_rate",
        "-show_entries", "format=duration,size,bit_rate",
        "-of", "json",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise VideoQAError(f"ffprobe 失敗: {result.stderr[:200]}")

    probe = json.loads(result.stdout)
    streams = probe.get("streams", [])
    fmt = probe.get("format", {})

    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    has_video = len(video_streams) > 0
    has_audio = len(audio_streams) > 0
    duration = float(fmt.get("duration", 0))

    resolution = ""
    if video_streams:
        vs = video_streams[0]
        resolution = f"{vs.get('width', '?')}x{vs.get('height', '?')}"

    issues = []

    if not has_video:
        issues.append("映像ストリームがありません")

    if expect_audio and not has_audio:
        issues.append("音声ストリームがありません（expect_audio=True）")

    if duration < min_duration:
        issues.append(f"尺が短すぎます: {duration:.1f}s < {min_duration}s")

    if duration > max_duration:
        issues.append(f"尺が長すぎます: {duration:.1f}s > {max_duration}s")

    status = "PASS" if not issues else "FAIL"

    result_dict = {
        "status": status,
        "path": str(video_path),
        "duration": round(duration, 2),
        "has_video": has_video,
        "has_audio": has_audio,
        "resolution": resolution,
        "file_size_mb": round(path.stat().st_size / (1024 * 1024), 2),
        "issues": issues,
    }

    if issues:
        print(f"  QA {status}: {video_path}")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print(f"  QA PASS: {video_path} ({duration:.1f}s, {resolution}, audio={'yes' if has_audio else 'no'})")

    return result_dict


def extract_qa_frames(
    video_path: str,
    count: int = 6,
    output_dir: Optional[str] = None,
) -> list[str]:
    """等間隔でフレームを抽出し、品質チェック用に保存する

    Args:
        video_path: 動画ファイルのパス
        count: 抽出フレーム数
        output_dir: 保存先ディレクトリ（None の場合は動画と同じディレクトリ/qa_frames/）

    Returns:
        抽出したフレーム画像パスのリスト
    """
    _ensure_ffmpeg()

    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(f"動画ファイルが見つかりません: {video_path}")

    if output_dir is None:
        out_dir = path.parent / "qa_frames"
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 動画の尺を取得
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        video_path,
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    duration = float(probe_result.stdout.strip())

    frames = []
    for i in range(count):
        timestamp = duration * (i + 0.5) / count
        frame_path = str(out_dir / f"qa_frame_{i:02d}.jpg")
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{timestamp:.2f}",
            "-i", video_path,
            "-frames:v", "1",
            "-q:v", "2",
            frame_path,
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        frames.append(frame_path)

    print(f"  QA フレーム {count}枚抽出: {out_dir}")
    return frames
