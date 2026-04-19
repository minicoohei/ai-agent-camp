"""
downloader.py - マルチプラットフォーム動画ダウンローダー

yt-dlpラッパー。YouTube/Vimeo/X等から動画+字幕を取得。
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


def find_ytdlp() -> str:
    """yt-dlp実行パスを検出"""
    for p in ["/home/ubuntu/.local/bin/yt-dlp", "yt-dlp"]:
        try:
            subprocess.run([p, "--version"], capture_output=True, check=True)
            return p
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    raise FileNotFoundError("yt-dlp が見つかりません。pip install yt-dlp を実行してください。")


_YTDLP = None


def _get_ytdlp() -> str:
    """遅延初期化でyt-dlpパスを取得"""
    global _YTDLP
    if _YTDLP is None:
        _YTDLP = find_ytdlp()
    return _YTDLP


def _common_args() -> list:
    """共通引数を返す。cookie + リモートコンポーネント対応。"""
    args = ["--remote-components", "ejs:github"]
    cookies = os.environ.get("YTDLP_COOKIES")
    if cookies and Path(cookies).exists():
        args += ["--cookies", cookies]
    else:
        browser = os.environ.get("YTDLP_COOKIES_FROM_BROWSER")
        if browser:
            args += ["--cookies-from-browser", browser]
    return args


def _validate_url(url: str) -> str:
    """URLの基本バリデーション"""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"無効なURL（http/httpsで始まる必要があります）: {url}")
    return url


def get_video_info(url: str) -> dict:
    """動画メタ情報を取得（ダウンロードしない）"""
    url = _validate_url(url)
    cmd = [_get_ytdlp(), "--dump-json", "--no-download"] + _common_args() + [url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"動画情報の取得に失敗: {result.stderr[:500]}")
    info = json.loads(result.stdout)
    return {
        "id": info.get("id", "unknown"),
        "title": info.get("title", ""),
        "channel": info.get("channel", info.get("uploader", "")),
        "duration": info.get("duration", 0),
        "url": url,
        "platform": info.get("extractor", "unknown"),
        "description": info.get("description", "")[:500],
        "subtitles_available": list(info.get("subtitles", {}).keys()),
        "auto_subtitles_available": list(info.get("automatic_captions", {}).keys()),
    }


def download_video(
    url: str,
    output_dir: Path,
    resolution: int = 1080,
) -> Path:
    """動画をダウンロード"""
    url = _validate_url(url)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(output_dir / "video.%(ext)s")

    cmd = [
        _get_ytdlp(),
        "-f", f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]/best",
        "--merge-output-format", "mp4",
        "-o", output_template,
        "--no-playlist",
    ] + _common_args() + [url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"動画ダウンロード失敗: {result.stderr[:500]}")

    # ダウンロードされたファイルを検索
    video_files = list(output_dir.glob("video.*"))
    if not video_files:
        raise FileNotFoundError(f"ダウンロードされた動画が見つかりません: {output_dir}")
    return video_files[0]


def download_subtitles(
    url: str,
    output_dir: Path,
    languages: Optional[list] = None,
) -> dict:
    """字幕をダウンロード。利用可能な字幕を自動検出。

    Returns:
        dict: {"lang_code": Path("subtitle_file.srt"), ...}
    """
    url = _validate_url(url)
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = {}

    # まず手動字幕を試行
    lang_str = ",".join(languages) if languages else "ja,en,zh"
    cmd = [
        _get_ytdlp(),
        "--write-sub",
        "--sub-lang", lang_str,
        "--sub-format", "srt/best",
        "--convert-subs", "srt",
        "--skip-download",
        "-o", str(output_dir / "sub"),
    ] + _common_args() + [url]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    # 手動字幕が取れなければ自動字幕
    srt_files = list(output_dir.glob("sub.*.srt"))
    if not srt_files:
        cmd = [
            _get_ytdlp(),
            "--write-auto-sub",
            "--sub-lang", lang_str,
            "--sub-format", "srt/best",
            "--convert-subs", "srt",
            "--skip-download",
            "-o", str(output_dir / "sub"),
        ] + _common_args() + [url]
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        srt_files = list(output_dir.glob("sub.*.srt"))

    for f in srt_files:
        # sub.en.srt → en
        parts = f.stem.split(".")
        if len(parts) >= 2:
            lang = parts[-1]
        else:
            lang = "unknown"
        downloaded[lang] = f

    return downloaded


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="動画ダウンローダー")
    parser.add_argument("url", help="動画URL")
    parser.add_argument("-o", "--output", default="output/clips/test", help="出力先")
    parser.add_argument("-r", "--resolution", type=int, default=1080)
    parser.add_argument("--subs-only", action="store_true", help="字幕のみ取得")
    args = parser.parse_args()

    out = Path(args.output)
    print(json.dumps(get_video_info(args.url), ensure_ascii=False, indent=2))

    if not args.subs_only:
        vpath = download_video(args.url, out, args.resolution)
        print(f"動画: {vpath}")

    subs = download_subtitles(args.url, out / "subtitles")
    print(f"字幕: {subs}")
