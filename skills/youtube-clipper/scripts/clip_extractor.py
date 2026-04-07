"""
clip_extractor.py - FFmpegクリップ抽出 + 字幕焼き込み

チャプター情報に基づいてクリップを切り出し、
オプションで字幕を焼き込んだ動画を生成。
"""

import json
import subprocess
from pathlib import Path


def time_to_seconds(time_str: str) -> float:
    """SRT時間文字列を秒数に変換: "00:05:30,000" → 330.0"""
    time_str = time_str.replace(",", ".")
    parts = time_str.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return float(time_str)


def extract_clip(
    video_path: Path,
    start: str,
    end: str,
    output_path: Path,
) -> Path:
    """FFmpegでクリップを切り出し（キーフレーム単位）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)
    duration = end_sec - start_sec
    if duration <= 0:
        raise ValueError(f"不正な時間範囲: start={start} ({start_sec}s) >= end={end} ({end_sec}s)")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", str(video_path),
        "-t", str(duration),
        "-c", "copy",  # ロスレスコピー
        "-avoid_negative_ts", "make_zero",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        # ロスレスが失敗した場合は再エンコード
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_sec),
            "-i", str(video_path),
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            raise RuntimeError(f"クリップ抽出失敗: {result.stderr[:500]}")

    return output_path


def extract_subtitle_range(
    srt_path: Path,
    start: str,
    end: str,
    output_path: Path,
) -> Path:
    """SRTから指定範囲の字幕を抽出（タイムスタンプ調整済み）"""
    import pysrt

    subs = pysrt.open(str(srt_path), encoding="utf-8")
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end)

    # 時間オフセット（ミリ秒単位）
    offset_ms = int(start_sec * 1000)

    filtered = pysrt.SubRipFile()
    idx = 1
    for sub in subs:
        sub_start_ms = sub.start.ordinal
        sub_end_ms = sub.end.ordinal
        start_ms = int(start_sec * 1000)
        end_ms = int(end_sec * 1000)

        if sub_start_ms < end_ms and sub_end_ms > start_ms:
            new_sub = pysrt.SubRipItem(
                index=idx,
                start=pysrt.SubRipTime(milliseconds=sub_start_ms - offset_ms),
                end=pysrt.SubRipTime(milliseconds=sub_end_ms - offset_ms),
                text=sub.text,
            )
            filtered.append(new_sub)
            idx += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    filtered.save(str(output_path), encoding="utf-8")
    return output_path


def burn_subtitles(
    video_path: Path,
    srt_path: Path,
    output_path: Path,
    font_size: int = 24,
    font_name: str = "Noto Sans CJK JP",
) -> Path:
    """字幕を動画に焼き込み"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # SRTパスのエスケープ（FFmpeg subtitles filter用）
    srt_escaped = str(srt_path).replace(":", "\\:").replace("'", "\\'")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles='{srt_escaped}':force_style='FontSize={font_size},FontName={font_name},PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'",
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "copy",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"字幕焼き込み失敗: {result.stderr[:500]}")

    return output_path


def extract_chapters_as_clips(
    video_path: Path,
    chapters: list,
    original_srt: Path,
    translated_srt: Path,
    output_dir: Path,
    burn_subs: bool = False,
    target_lang: str = "ja",
    skip_bilingual: bool = False,
) -> list:
    """複数チャプターをクリップとして抽出

    Returns:
        list: [{"clip_path": Path, "subtitled_path": Path, ...}, ...]
    """
    results = []

    for ch in chapters:
        clip_id = f"clip_{ch['id']:02d}"
        clip_dir = output_dir / clip_id
        clip_dir.mkdir(parents=True, exist_ok=True)

        # クリップ切り出し
        clip_path = clip_dir / f"{clip_id}.mp4"
        extract_clip(video_path, ch["start"], ch["end"], clip_path)

        # 字幕範囲抽出
        orig_clip_srt = clip_dir / "original.srt"
        trans_clip_srt = clip_dir / f"translated_{target_lang}.srt"

        if original_srt.exists():
            extract_subtitle_range(original_srt, ch["start"], ch["end"], orig_clip_srt)
        if translated_srt.exists():
            extract_subtitle_range(translated_srt, ch["start"], ch["end"], trans_clip_srt)

        # バイリンガルSRT（同一言語時はスキップして字幕重複を防止）
        bilingual_srt = clip_dir / "bilingual.srt"
        if not skip_bilingual and orig_clip_srt.exists() and trans_clip_srt.exists():
            from subtitle_translator import create_bilingual_srt
            create_bilingual_srt(orig_clip_srt, trans_clip_srt, bilingual_srt)

        # 字幕焼き込み
        subtitled_path = None
        if burn_subs and bilingual_srt.exists():
            subtitled_path = clip_dir / f"{clip_id}_subtitled.mp4"
            try:
                burn_subtitles(clip_path, bilingual_srt, subtitled_path)
            except RuntimeError as e:
                print(f"  警告: 字幕焼き込みスキップ ({clip_id}): {e}")
                subtitled_path = None

        # SNSサマリー
        summary = {
            "chapter_id": ch["id"],
            "title": ch["title"],
            "summary": ch["summary"],
            "keywords": ch.get("keywords", []),
            "highlight_score": ch.get("highlight_score", 0),
            "duration_display": f"{ch['start'][:8]} - {ch['end'][:8]}",
            "hashtags": [f"#{kw}" for kw in ch.get("keywords", [])[:5]],
        }
        summary_path = clip_dir / "summary.json"
        summary_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        results.append({
            "clip_id": clip_id,
            "clip_path": str(clip_path),
            "subtitled_path": str(subtitled_path) if subtitled_path else None,
            "original_srt": str(orig_clip_srt) if orig_clip_srt.exists() else None,
            "translated_srt": str(trans_clip_srt) if trans_clip_srt.exists() else None,
            "bilingual_srt": str(bilingual_srt) if bilingual_srt.exists() else None,
            "summary": summary,
        })

        print(f"  {clip_id}: {ch['title']} ({ch['start'][:8]}-{ch['end'][:8]})")

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="クリップ抽出")
    parser.add_argument("video", help="動画ファイル")
    parser.add_argument("--start", required=True, help="開始時間 (HH:MM:SS,mmm)")
    parser.add_argument("--end", required=True, help="終了時間")
    parser.add_argument("-o", "--output", required=True, help="出力パス")
    args = parser.parse_args()

    result = extract_clip(Path(args.video), args.start, args.end, Path(args.output))
    print(f"クリップ: {result}")
