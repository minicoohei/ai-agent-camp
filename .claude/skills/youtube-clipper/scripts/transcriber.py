"""
transcriber.py - 字幕なし動画の音声文字起こし

FFmpegで音声抽出 → Gemini 3.0 Flash Preview で文字起こし + SRT生成
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# bootcamp_utils をインポート
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client


def extract_audio(video_path: Path, output_path: Path = None) -> Path:
    """FFmpegで動画から音声を抽出（mp3形式）"""
    if output_path is None:
        output_path = video_path.with_suffix(".mp3")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",  # 映像なし
        "-acodec", "libmp3lame",
        "-ab", "128k",
        "-ar", "16000",  # 16kHz（音声認識に最適）
        str(output_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        raise RuntimeError("音声抽出がタイムアウトしました（300秒）。動画が長すぎる可能性があります。")
    if result.returncode != 0:
        raise RuntimeError(f"音声抽出失敗: {result.stderr[:500]}")
    return output_path


def transcribe_with_gemini(
    audio_path: Path,
    source_lang: str = "auto",
) -> list:
    """Gemini 3.0 Flash Preview で音声を文字起こし

    Returns:
        list: [{"start": "00:00:05,000", "end": "00:00:10,000", "text": "..."}, ...]
    """
    client = get_client()
    if not client:
        raise RuntimeError("GEMINI_API_KEY が設定されていません")

    # 音声ファイルをアップロード
    audio_file = client.files.upload(file=str(audio_path))

    lang_hint = f"ソース言語は{source_lang}です。" if source_lang != "auto" else "言語を自動検出してください。"

    prompt = f"""以下の音声ファイルを文字起こししてください。
{lang_hint}

重要なルール:
1. タイムスタンプ付きで出力してください
2. SRT形式のタイムスタンプを使用: HH:MM:SS,mmm
3. 各セグメントは3-10秒程度の自然な区切りにしてください
4. 無音区間はスキップしてください
5. 結果はJSON配列で返してください

出力形式（JSONのみ、他のテキストは不要）:
[
  {{"start": "00:00:01,000", "end": "00:00:05,500", "text": "こんにちは、今日は...", "lang": "ja"}},
  {{"start": "00:00:06,000", "end": "00:00:12,000", "text": "AIエージェントについて...", "lang": "ja"}}
]"""

    model = os.environ.get("GEMINI_TRANSCRIBE_MODEL", "gemini-3-flash-preview")
    try:
        response = client.models.generate_content(
            model=model,
            contents=[
                prompt,
                audio_file,
            ],
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API呼び出し失敗: {e}") from e

    # JSON抽出
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        segments = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Gemini応答のJSON解析失敗: {e}\n応答テキスト: {text[:500]}"
        ) from e
    return segments


def segments_to_srt(segments: list, output_path: Path) -> Path:
    """セグメントリストをSRTファイルに変換"""
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{seg['start']} --> {seg['end']}")
        lines.append(seg["text"])
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def transcribe_video(
    video_path: Path,
    output_dir: Path,
    source_lang: str = "auto",
) -> dict:
    """動画を文字起こしし、SRTファイルを生成

    Returns:
        dict: {"srt_path": Path, "segments": list, "detected_lang": str}
    """
    # 音声抽出
    audio_path = output_dir / "audio.mp3"
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    extract_audio(video_path, audio_path)

    # Gemini文字起こし
    segments = transcribe_with_gemini(audio_path, source_lang)

    # 言語検出
    detected_lang = segments[0].get("lang", "unknown") if segments else "unknown"

    # SRT生成
    srt_path = output_dir / "original.srt"
    segments_to_srt(segments, srt_path)

    # 一時音声ファイル削除
    audio_path.unlink(missing_ok=True)

    return {
        "srt_path": srt_path,
        "segments": segments,
        "detected_lang": detected_lang,
        "segment_count": len(segments),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="動画音声文字起こし（Gemini）")
    parser.add_argument("video", help="動画ファイルパス")
    parser.add_argument("-o", "--output", default=None, help="出力ディレクトリ")
    parser.add_argument("--lang", default="auto", help="ソース言語ヒント")
    args = parser.parse_args()

    video_path = Path(args.video)
    output_dir = Path(args.output) if args.output else video_path.parent / "subtitles"

    result = transcribe_video(video_path, output_dir, args.lang)
    print(json.dumps({
        "srt_path": str(result["srt_path"]),
        "detected_lang": result["detected_lang"],
        "segment_count": result["segment_count"],
    }, ensure_ascii=False, indent=2))
