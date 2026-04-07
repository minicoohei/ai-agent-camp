"""
Video Analyzer - TikTok/YouTube動画を分析してテンプレート化
URL → ダウンロード → フレーム抽出 → STT → Vision分析 → テンプレートJSON

対応プラットフォーム:
  - TikTok (https://www.tiktok.com/... / https://vt.tiktok.com/...)
  - YouTube (https://www.youtube.com/watch?v=... / https://youtu.be/... / YouTube Shorts)
  - Instagram Reels
  - その他 yt-dlp が対応するプラットフォーム
"""

import argparse
import json
import math
import os
import subprocess
import sys
import base64
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# ツールパス
YTDLP = os.environ.get("YTDLP_PATH", str(Path(__file__).parents[3] / ".bin" / "yt-dlp"))
FFMPEG = os.environ.get("FFMPEG_PATH", str(Path(__file__).parents[3] / ".bin" / "ffmpeg"))


def download_video(url: str, output_dir: Path) -> Optional[Path]:
    """yt-dlpで動画をダウンロード（TikTok / YouTube / Instagram等対応）"""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "source.mp4"
    
    print(f"📥 ダウンロード中: {url}")
    result = subprocess.run([
        YTDLP,
        "-f", "best[ext=mp4]/best",
        "--no-playlist",
        "-o", str(output_file),
        "--no-check-certificates",
        url
    ], capture_output=True, text=True, timeout=120)
    
    if result.returncode != 0:
        print(f"  ❌ ダウンロード失敗: {result.stderr[-300:]}")
        # mp4以外で保存された場合を探す
        for f in output_dir.glob("source.*"):
            if f.suffix in ['.mp4', '.webm', '.mkv']:
                return f
        return None
    
    if output_file.exists():
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"  ✅ {size_mb:.1f}MB")
        return output_file
    return None


def get_video_info(video_path: Path) -> Dict:
    """ffmpegで動画情報を取得"""
    import re
    result = subprocess.run(
        [FFMPEG, "-i", str(video_path)],
        capture_output=True, text=True, timeout=10
    )
    info = {"duration": 0, "width": 0, "height": 0, "fps": 30}
    
    dur_match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if dur_match:
        h, m, s = dur_match.groups()
        info["duration"] = int(h) * 3600 + int(m) * 60 + float(s)
    
    res_match = re.search(r"(\d{3,4})x(\d{3,4})", result.stderr)
    if res_match:
        info["width"] = int(res_match.group(1))
        info["height"] = int(res_match.group(2))
    
    fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", result.stderr)
    if fps_match:
        info["fps"] = float(fps_match.group(1))
    
    return info


def extract_frames(video_path: Path, output_dir: Path, fps: float = 1.0) -> List[Path]:
    """動画からフレームを抽出"""
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎞️ フレーム抽出中 ({fps}fps)...")
    subprocess.run([
        FFMPEG, "-y", "-i", str(video_path),
        "-vf", f"fps={fps}",
        "-q:v", "2",
        str(frames_dir / "frame_%03d.jpg")
    ], capture_output=True, timeout=60)
    
    frames = sorted(frames_dir.glob("frame_*.jpg"))
    print(f"  ✅ {len(frames)}フレーム抽出")
    return frames


def extract_audio(video_path: Path, output_dir: Path) -> Optional[Path]:
    """動画から音声を抽出"""
    audio_path = output_dir / "audio.mp3"
    print(f"🔊 音声抽出中...")
    result = subprocess.run([
        FFMPEG, "-y", "-i", str(video_path),
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        str(audio_path)
    ], capture_output=True, timeout=60)
    
    if audio_path.exists() and audio_path.stat().st_size > 100:
        print(f"  ✅ {audio_path.stat().st_size // 1024}KB")
        return audio_path
    print(f"  ⚠️ 音声なし")
    return None


def transcribe_audio(audio_path: Path) -> Dict:
    """Gemini APIで音声文字起こし（Whisperフォールバック付き）"""
    # まずOpenAI Whisper試行
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if not openai_key:
        env_file = Path(__file__).parents[3] / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("OPENAI_API_KEY"):
                    openai_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if openai_key:
        print(f"🎤 Whisper STT実行中...")
        result = subprocess.run([
            "curl", "-s",
            "-H", f"Authorization: Bearer {openai_key}",
            "-F", f"file=@{audio_path}",
            "-F", "model=whisper-1",
            "-F", "language=ja",
            "-F", "response_format=verbose_json",
            "-F", "timestamp_granularities[]=segment",
            "https://api.openai.com/v1/audio/transcriptions"
        ], capture_output=True, text=True, timeout=120)
        try:
            data = json.loads(result.stdout)
            if "segments" in data:
                segments = data.get("segments", [])
                text = data.get("text", "")
                print(f"  ✅ {len(segments)}セグメント、{len(text)}文字")
                return {"text": text, "segments": segments}
        except Exception:
            pass
    
    # Gemini Audio STTフォールバック
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_key:
        env_file = Path(__file__).parents[3] / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("GEMINI_API_KEY"):
                    gemini_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not gemini_key:
        print("  ⚠️ API KEY未設定、STTスキップ")
        return {"text": "", "segments": []}
    
    print(f"🎤 Gemini Audio STT実行中...")
    
    # 音声をbase64エンコード
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={gemini_key}"
    payload = json.dumps({
        "contents": [{
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "audio/mpeg",
                        "data": audio_b64
                    }
                },
                {
                    "text": """この音声を日本語で文字起こししてください。
タイムスタンプ付きのセグメントに分割してください。

JSON形式で出力:
```json
{
  "text": "全体のテキスト",
  "segments": [
    {"start": 0.0, "end": 3.5, "text": "最初のセグメント"},
    {"start": 3.5, "end": 7.2, "text": "次のセグメント"}
  ]
}
```
JSONのみ出力してください。"""
                }
            ]
        }],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 4096}
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text.strip())
        segments = data.get("segments", [])
        full_text = data.get("text", "")
        print(f"  ✅ {len(segments)}セグメント、{len(full_text)}文字")
        return {"text": full_text, "segments": segments}
    except Exception as e:
        print(f"  ❌ Gemini STTエラー: {e}")
        return {"text": "", "segments": []}


def analyze_frames_vision(frames: List[Path], video_info: Dict) -> List[Dict]:
    """Gemini Vision APIでフレーム分析"""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        env_file = Path(__file__).parents[3] / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("GEMINI_API_KEY"):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    
    if not api_key:
        print("  ⚠️ GEMINI_API_KEY未設定、Vision分析スキップ")
        return []
    
    print(f"👁️ Vision分析中 ({len(frames)}フレーム)...")
    
    # フレームを間引き（最大16枚）
    step = max(1, len(frames) // 16)
    selected = frames[::step][:16]
    
    # 全フレームをbase64エンコード
    parts = []
    for i, fp in enumerate(selected):
        with open(fp, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": b64
            }
        })
    
    prompt = f"""この{len(selected)}枚のフレームはTikTok/YouTube動画から1秒ごとに抽出したものです。
動画の長さは{video_info['duration']:.1f}秒、解像度は{video_info['width']}x{video_info['height']}です。

各フレームについて以下を分析してください：

1. **ショットタイプ**: close_up / medium / wide / overhead / screen_recording
2. **被写体**: 何が映っているか簡潔に
3. **テロップ/テキスト**: 画面上のテキスト内容、位置（top/center/bottom）、おおよそのサイズ、色、スタイル
4. **動き/トランジション**: 前のフレームからの変化（cut/fade/swipe/zoom/none）
5. **BGM/エネルギー**: 画面の雰囲気から推測（high/medium/low）

また、動画全体について：
- **構成パターン**: hook→problem→solution→demo→CTA など
- **ペーシング**: fast/medium/slow
- **テロップスタイルの一貫性**: フォント、色、位置のパターン
- **推定カテゴリ**: product_demo / tutorial / storytelling / before_after / reaction / vlog / ad

JSON形式で出力してください：
```json
{{
  "frames": [
    {{
      "frame_index": 0,
      "timestamp_sec": 0,
      "shot_type": "...",
      "subject": "...",
      "text_overlay": {{
        "text": "...",
        "position": "top/center/bottom",
        "style": "bold/subtitle/minimal/none",
        "color": "#FFFFFF",
        "has_stroke": true
      }},
      "transition_from_prev": "cut/fade/swipe/zoom/none",
      "energy": "high/medium/low"
    }}
  ],
  "summary": {{
    "category": "...",
    "structure": "hook → ... → CTA",
    "pacing": "fast/medium/slow",
    "caption_style": "テロップスタイルの要約",
    "key_techniques": ["technique1", "technique2"]
  }}
}}
```
JSONのみ出力してください。"""
    
    parts.append({"text": prompt})
    
    # Gemini API呼び出し
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192}
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # JSON抽出
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        analysis = json.loads(text.strip())
        print(f"  ✅ {len(analysis.get('frames', []))}フレーム分析完了")
        return analysis
    except Exception as e:
        print(f"  ❌ Vision分析エラー: {e}")
        return {}


def build_template(
    url: str,
    video_info: Dict,
    stt_result: Dict,
    vision_analysis: Dict,
    output_dir: Path
) -> Path:
    """分析結果からテンプレートJSONを生成"""
    print(f"\n📋 テンプレート生成中...")
    
    frames_analysis = vision_analysis.get("frames", [])
    summary = vision_analysis.get("summary", {})
    segments = stt_result.get("segments", [])
    
    # STTセグメントとフレームを時間で紐付け
    scenes = []
    
    if frames_analysis:
        for i, frame in enumerate(frames_analysis):
            ts_sec = frame.get("timestamp_sec", i)
            
            # 対応するSTTセグメントを探す
            narration = ""
            for seg in segments:
                seg_start = seg.get("start", 0)
                seg_end = seg.get("end", 0)
                if seg_start <= ts_sec + 0.5 < seg_end:
                    narration = seg.get("text", "")
                    break
            
            # 次のフレームまでの時間 = シーン長
            if i + 1 < len(frames_analysis):
                next_ts = frames_analysis[i + 1].get("timestamp_sec", ts_sec + 3)
            else:
                next_ts = video_info["duration"]
            scene_duration = max(1.0, next_ts - ts_sec)
            
            start_min = int(ts_sec // 60)
            start_sec = int(ts_sec % 60)
            end_total = ts_sec + scene_duration
            end_min = int(end_total // 60)
            end_sec = int(end_total % 60)
            
            scene = {
                "frame_number": i + 1,
                "timestamp": f"{start_min}:{start_sec:02d}-{end_min}:{end_sec:02d}",
                "duration": round(scene_duration, 1),
                "narration": narration,
                "text_overlay": frame.get("text_overlay", {}),
                "visual": {
                    "shot_type": frame.get("shot_type", "medium"),
                    "subject": frame.get("subject", ""),
                    "transition_to_next": frame.get("transition_from_prev", "cut"),
                },
                "motion_type": "i2v",  # デフォルトi2V
                "energy": frame.get("energy", "medium"),
            }
            scenes.append(scene)
    else:
        # Vision分析なし、STTだけでシーン構築
        for i, seg in enumerate(segments):
            start = seg.get("start", 0)
            end = seg.get("end", start + 3)
            start_min = int(start // 60)
            start_sec = int(start % 60)
            end_min = int(end // 60)
            end_sec = int(end % 60)
            
            scenes.append({
                "frame_number": i + 1,
                "timestamp": f"{start_min}:{start_sec:02d}-{end_min}:{end_sec:02d}",
                "duration": round(end - start, 1),
                "narration": seg.get("text", ""),
                "text_overlay": {"main_text": "", "position": "center", "style": "bold"},
                "visual": {"shot_type": "medium", "subject": ""},
                "motion_type": "i2v",
                "energy": "medium",
            })
    
    template = {
        "source_url": url,
        "duration": video_info["duration"],
        "resolution": f"{video_info['width']}x{video_info['height']}",
        "scenes": scenes,
        "summary": {
            "total_scenes": len(scenes),
            "avg_scene_duration": round(video_info["duration"] / max(1, len(scenes)), 1),
            "full_transcript": stt_result.get("text", ""),
            **summary,
        }
    }
    
    template_path = output_dir / "template.json"
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    
    print(f"✅ テンプレート保存: {template_path}")
    print(f"   {len(scenes)}シーン, {video_info['duration']:.1f}秒")
    if summary:
        print(f"   カテゴリ: {summary.get('category', '不明')}")
        print(f"   構成: {summary.get('structure', '不明')}")
        print(f"   テロップ: {summary.get('caption_style', '不明')}")
    
    return template_path


def analyze_video(url: str, output_dir: Path) -> Optional[Path]:
    """メイン: URL → 分析 → テンプレート生成
    
    TikTok、YouTube、Instagram Reels等のURLに対応。
    yt-dlpがサポートするプラットフォームであればダウンロード可能。
    """
    print(f"\n{'='*60}")
    print(f"🔍 動画分析: {url}")
    print(f"{'='*60}\n")
    
    work_dir = output_dir / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. ダウンロード（yt-dlp: TikTok / YouTube / Instagram等対応）
    video_path = download_video(url, work_dir)
    if not video_path:
        print("❌ ダウンロード失敗")
        return None
    
    # 2. 動画情報取得
    video_info = get_video_info(video_path)
    print(f"📊 {video_info['duration']:.1f}秒, {video_info['width']}x{video_info['height']}")
    
    # 3. フレーム抽出
    frames = extract_frames(video_path, work_dir)
    
    # 4. 音声抽出 + STT
    audio_path = extract_audio(video_path, work_dir)
    stt_result = {"text": "", "segments": []}
    if audio_path:
        stt_result = transcribe_audio(audio_path)
    
    # 5. Vision分析
    vision_analysis = analyze_frames_vision(frames, video_info)
    
    # 6. テンプレート生成
    template_path = build_template(url, video_info, stt_result, vision_analysis, output_dir)
    
    print(f"\n✅ 分析完了: {template_path}")
    print(f"   💡 Playbook蓄積は video-playbook スキルを使用してください:")
    print(f"   python skills/video-playbook/scripts/manage_playbook.py --add -t {template_path}")
    
    return template_path


def main():
    parser = argparse.ArgumentParser(
        description="TikTok/YouTube動画分析 → テンプレート化\n"
                    "対応: TikTok, YouTube, YouTube Shorts, Instagram Reels等",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # TikTok動画を分析
  python analyze_video.py --url "https://www.tiktok.com/@user/video/123456"
  
  # YouTube動画を分析  
  python analyze_video.py --url "https://www.youtube.com/watch?v=XXXXX"
  
  # YouTube Shortsを分析
  python analyze_video.py --url "https://youtube.com/shorts/XXXXX"
  
  # 複数URLをバッチ分析
  python analyze_video.py --urls-file urls.txt --output output/templates/
"""
    )
    parser.add_argument("--url", "-u", help="動画URL（TikTok / YouTube / Instagram等）")
    parser.add_argument("--urls-file", "-f", help="URLリストファイル（1行1URL）")
    parser.add_argument("--output", "-o", default="output/templates", help="出力ディレクトリ")
    args = parser.parse_args()
    
    if args.url:
        output_dir = Path(args.output)
        # URLからディレクトリ名を生成
        safe_name = args.url.split("/")[-1][:30].replace("?", "_")
        analyze_video(args.url, output_dir / safe_name)
    elif args.urls_file:
        urls = Path(args.urls_file).read_text(encoding="utf-8").strip().split("\n")
        for i, url in enumerate(urls):
            url = url.strip()
            if not url or url.startswith("#"):
                continue
            output_dir = Path(args.output) / f"video_{i+1:03d}"
            analyze_video(url, output_dir)
    else:
        print("❌ --url または --urls-file を指定してください")
        print("   例: python analyze_video.py --url 'https://www.youtube.com/watch?v=XXXXX'")
        sys.exit(1)


if __name__ == "__main__":
    main()
