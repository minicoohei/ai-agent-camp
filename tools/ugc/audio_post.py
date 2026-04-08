"""
音声の後処理ユーティリティ

- 動画から音声抽出
- 音声の差し替え（mux）
- Demucsによるボーカル除去
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg が見つかりません。")


def extract_audio(video_path: str, audio_path: str) -> None:
    """動画から音声を抽出（WAV）"""
    _ensure_ffmpeg()
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        audio_path,
    ]
    subprocess.run(cmd, check=True)


def mux_audio(video_path: str, audio_path: str, output_path: str) -> None:
    """動画に音声を合成"""
    _ensure_ffmpeg()
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def remove_vocals_from_video(video_path: str, output_path: str) -> None:
    """
    Demucsでボーカル除去して動画に反映する
    """
    _ensure_ffmpeg()
    if shutil.which("demucs") is None:
        raise RuntimeError("demucs が見つかりません。pip install demucs が必要です。")

    work_dir = Path(tempfile.mkdtemp(prefix="demucs_"))
    audio_path = str(work_dir / "audio.wav")
    extract_audio(video_path, audio_path)

    demucs_out = work_dir / "separated"
    cmd = [
        "demucs",
        "--two-stems", "vocals",
        "-o", str(demucs_out),
        audio_path,
    ]
    subprocess.run(cmd, check=True)

    no_vocals = next(demucs_out.rglob("no_vocals.*"), None)
    if not no_vocals:
        raise RuntimeError("no_vocals 音声が見つかりません")

    mux_audio(video_path, str(no_vocals), output_path)


def apply_wav2lip(
    video_path: str,
    audio_path: str,
    output_path: str,
    wav2lip_dir: Optional[str] = None,
    checkpoint_path: Optional[str] = None,
    face_enhance: bool = False,
) -> None:
    """
    Wav2Lipでリップシンクを適用する
    """
    if not wav2lip_dir:
        wav2lip_dir = os.environ.get("WAV2LIP_DIR")
    if not checkpoint_path:
        checkpoint_path = os.environ.get("WAV2LIP_CHECKPOINT")

    if not wav2lip_dir or not Path(wav2lip_dir).exists():
        raise RuntimeError("WAV2LIP_DIR が未設定、またはディレクトリが存在しません。")
    if not checkpoint_path or not Path(checkpoint_path).exists():
        raise RuntimeError("WAV2LIP_CHECKPOINT が未設定、またはファイルが存在しません。")

    inference_py = Path(wav2lip_dir) / "inference.py"
    if not inference_py.exists():
        raise RuntimeError(f"inference.py が見つかりません: {inference_py}")

    cmd = [
        "python",
        str(inference_py),
        "--checkpoint_path", str(checkpoint_path),
        "--face", video_path,
        "--audio", audio_path,
        "--outfile", output_path,
    ]
    if face_enhance:
        cmd.append("--face_enhance")

    subprocess.run(cmd, check=True, cwd=wav2lip_dir)


def download_file(url: str, output_path: str) -> None:
    """URLからファイルをダウンロード"""
    _ensure_ffmpeg()
    cmd = [
        "ffmpeg",
        "-y",
        "-i", url,
        "-c", "copy",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def mix_bgm(
    video_path: str,
    bgm_path: str,
    output_path: str,
    bgm_volume: float = 0.15,
) -> None:
    """動画にBGMを重ねる（元音声を維持しつつBGMをミックス）

    Args:
        video_path: 元の動画ファイル（音声付き）
        bgm_path: BGM音声ファイル（MP3/WAV/AAC）
        output_path: 出力先の動画ファイル
        bgm_volume: BGMの音量（0.0-1.0, デフォルト0.15で控えめ）
    """
    _ensure_ffmpeg()
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[1:a]volume={bgm_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def mix_bgm_no_audio(
    video_path: str,
    bgm_path: str,
    output_path: str,
    bgm_volume: float = 0.5,
) -> None:
    """音声なし動画にBGMを追加する

    Args:
        video_path: 音声なしの動画ファイル
        bgm_path: BGM音声ファイル
        output_path: 出力先の動画ファイル
        bgm_volume: BGMの音量（0.0-1.0）
    """
    _ensure_ffmpeg()
    # 動画の長さを事前に取得（shell substitution を避ける）
    probe_result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True, check=True,
    )
    video_duration = probe_result.stdout.strip()
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[1:a]volume={bgm_volume},atrim=duration={video_duration}[bgm]",
        "-map", "0:v",
        "-map", "[bgm]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def apply_musetalk(
    video_path: str,
    audio_path: str,
    output_path: str,
) -> None:
    """
    fal.aiのMuseTalkでリップシンクを適用する
    """
    try:
        import fal_client
    except ImportError:
        raise ImportError("fal-client パッケージがインストールされていません: pip install fal-client")

    # ローカルファイルはFal.aiにアップロード
    if video_path.startswith(("http://", "https://")):
        video_url = video_path
    else:
        video_url = fal_client.upload_file(video_path)

    if audio_path.startswith(("http://", "https://")):
        audio_url = audio_path
    else:
        audio_url = fal_client.upload_file(audio_path)

    result = fal_client.subscribe(
        "fal-ai/musetalk",
        arguments={
            "video_url": video_url,
            "audio_url": audio_url,
        },
        with_logs=True,
    )

    video_url_out = (
        result.get("video", {}).get("url")
        or result.get("video_url")
        or result.get("output", {}).get("url")
    )
    if not video_url_out:
        raise ValueError(f"MuseTalkの出力URLが取得できませんでした: {result}")

    download_file(video_url_out, output_path)
