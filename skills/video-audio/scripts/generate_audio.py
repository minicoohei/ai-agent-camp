"""
Video Audio Generator - ElevenLabs TTS でナレーション音声を生成
scenes.json の narration フィールドから音声ファイルを生成する。
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import List, Dict, Optional

# ffmpegパス
FFMPEG = os.environ.get("FFMPEG_PATH", str(Path(__file__).parents[3] / ".bin" / "ffmpeg"))

# ElevenLabs API
ELEVENLABS_API = "https://api.elevenlabs.io/v1"

# 日本語ボイスエイリアス
VOICE_ALIASES = {
    "akari": "EkK6wL8GaH8IgBZTTDGJ",
    "miyu": "EnLxjGl88dNO1Jv6AZk2",
    "kaori": "G3EZ8O36A0x9lmeOtr0f",
    "fumi": "PmgfHCGeS5b7sH90BOOJ",
    "masa": "StTDrGrPSyfaHGmzwXbj",
    "mitsuki": "gARvXPexe5VF3cKZBian",
    "custom": "YOUR_VOICE_ID",
    "sakura": "RBnMinrYKeccY3vaUxlZ",
    "otani": "3JDquces8E8bkmvbh6Bc",
    "shohei": "8FuuqoKHuM48hIEwni5e",
    # English voices
    "liam": "TX3LPaxmHKxFdv7VOQHJ",
    "sarah": "EXAVITQu4vr4xnSDxMaL",
    "alice": "Xb7hH8MSUJpSbSDYk0k2",
}


def resolve_voice_id(voice: str) -> str:
    """ボイス名/エイリアスをIDに解決"""
    return VOICE_ALIASES.get(voice.lower(), voice)


def get_api_key() -> str:
    """ElevenLabs API キーを取得"""
    key = os.environ.get("ELEVEN_API_KEY", "")
    if not key:
        # .envから読む
        env_file = Path(__file__).parents[3] / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("ELEVEN_API_KEY"):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def generate_tts(
    text: str,
    voice_id: str,
    output_path: Path,
    api_key: str,
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    speed: float = 1.0,
) -> bool:
    """ElevenLabs TTS API で音声生成"""
    url = f"{ELEVENLABS_API}/text-to-speech/{voice_id}"
    
    payload = json.dumps({
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "speed": speed,
        }
    }).encode("utf-8")
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(resp.read())
            return output_path.exists() and output_path.stat().st_size > 100
    except Exception as e:
        print(f"  ❌ TTS エラー: {e}")
        return False


def get_audio_duration(path: Path) -> float:
    """ffmpegで音声ファイルの長さを取得"""
    try:
        result = subprocess.run(
            [FFMPEG, "-i", str(path), "-f", "null", "-"],
            capture_output=True, text=True, timeout=10
        )
        import re
        match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", result.stderr)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
    except Exception:
        pass
    # フォールバック: ファイルサイズから推定 (128kbps MP3)
    return path.stat().st_size / (128 * 1000 / 8)


def generate_silence(output_path: Path, duration: float) -> bool:
    """無音ファイルを生成"""
    return subprocess.run(
        [FFMPEG, "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
         "-t", str(duration), "-c:a", "libmp3lame", "-q:a", "9",
         str(output_path)],
        capture_output=True, timeout=10
    ).returncode == 0


def concat_audio(files: List[Path], output_path: Path) -> bool:
    """複数の音声ファイルを結合"""
    concat_file = output_path.parent / "concat_audio.txt"
    with open(concat_file, "w") as f:
        for fp in files:
            f.write(f"file '{fp.resolve()}'\n")
    
    result = subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-c:a", "libmp3lame", "-q:a", "2", str(output_path)],
        capture_output=True, text=True, timeout=60
    )
    concat_file.unlink(missing_ok=True)
    return result.returncode == 0


def parse_timestamp(ts: str) -> tuple:
    """タイムスタンプ "0:00-0:02" を秒に変換"""
    start_str, end_str = ts.split("-")
    def to_sec(t):
        parts = t.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    return to_sec(start_str), to_sec(end_str)


def generate_audio(
    storyboard_dir: Path,
    voice: str = "akari",
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    speed: float = 1.0,
    per_scene: bool = False,
    silence_gap: float = 0.3,
    output_path: Optional[Path] = None,
) -> Optional[Path]:
    """メイン: scenes.json からナレーション音声を生成"""
    
    api_key = get_api_key()
    if not api_key:
        print("❌ ELEVEN_API_KEY が設定されていません")
        return None
    
    voice_id = resolve_voice_id(voice)
    
    scenes_path = storyboard_dir / "scenes.json"
    if not scenes_path.exists():
        print(f"❌ scenes.json が見つかりません: {scenes_path}")
        return None
    
    with open(scenes_path) as f:
        data = json.load(f)
    
    scenes = data["scenes"]
    audio_dir = storyboard_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # ナレーションのあるシーンを処理
    narration_scenes = [s for s in scenes if s.get("narration", "").strip()]
    if not narration_scenes:
        print("⚠️ ナレーションのあるシーンがありません")
        return None
    
    print(f"🎙️ {len(narration_scenes)}/{len(scenes)} シーンにナレーションあり")
    print(f"🔊 ボイス: {voice} ({voice_id[:8]}...)")
    
    timestamps = {"scenes": []}
    audio_files = []
    current_time = 0.0
    
    for scene in scenes:
        fn = scene["frame_number"]
        narration = scene.get("narration", "").strip()
        start_sec, end_sec = parse_timestamp(scene["timestamp"])
        scene_duration = end_sec - start_sec
        
        frame_num = f"{fn:02d}"
        frame_audio = audio_dir / f"frame_{frame_num}.mp3"
        
        if not narration:
            # ナレーションなし → 無音
            if not per_scene:
                silence_path = audio_dir / f"silence_{frame_num}.mp3"
                generate_silence(silence_path, scene_duration)
                audio_files.append(silence_path)
                timestamps["scenes"].append({
                    "frame_number": fn,
                    "start": current_time,
                    "end": current_time + scene_duration,
                    "duration": scene_duration,
                    "text": "",
                    "has_audio": False,
                })
                current_time += scene_duration
            continue
        
        print(f"  🎤 F{fn}: 「{narration[:30]}{'...' if len(narration) > 30 else ''}」")
        
        # TTS生成
        success = generate_tts(
            text=narration,
            voice_id=voice_id,
            output_path=frame_audio,
            api_key=api_key,
            model=model,
            stability=stability,
            similarity_boost=similarity_boost,
            speed=speed,
        )
        
        if not success:
            print(f"    ❌ 生成失敗、スキップ")
            if not per_scene:
                silence_path = audio_dir / f"silence_{frame_num}.mp3"
                generate_silence(silence_path, scene_duration)
                audio_files.append(silence_path)
                current_time += scene_duration
            continue
        
        audio_duration = get_audio_duration(frame_audio)
        size_kb = frame_audio.stat().st_size // 1024
        print(f"    ✅ {audio_duration:.1f}s ({size_kb}KB)")
        
        # シーンの長さに合わせて調整
        # 音声がシーンより短い場合は無音パディング
        # 音声がシーンより長い場合はそのまま（動画側で調整）
        effective_duration = max(audio_duration, scene_duration)
        
        timestamps["scenes"].append({
            "frame_number": fn,
            "start": current_time,
            "end": current_time + effective_duration,
            "duration": effective_duration,
            "audio_duration": audio_duration,
            "scene_duration": scene_duration,
            "text": narration,
            "has_audio": True,
        })
        
        if not per_scene:
            audio_files.append(frame_audio)
            # シーン間の無音ギャップ
            if silence_gap > 0:
                gap_path = audio_dir / f"gap_{frame_num}.mp3"
                generate_silence(gap_path, silence_gap)
                audio_files.append(gap_path)
                current_time += effective_duration + silence_gap
            else:
                current_time += effective_duration
        
        # API レート制限対策
        time.sleep(0.5)
    
    timestamps["total_duration"] = current_time
    
    # タイムスタンプ保存
    ts_path = audio_dir / "timestamps.json"
    with open(ts_path, "w", encoding="utf-8") as f:
        json.dump(timestamps, f, ensure_ascii=False, indent=2)
    print(f"\n📋 タイムスタンプ: {ts_path}")
    
    if per_scene:
        print(f"✅ {len([s for s in timestamps['scenes'] if s.get('has_audio')])} フレームの音声を生成")
        return audio_dir
    
    # 結合
    if not audio_files:
        print("❌ 音声ファイルがありません")
        return None
    
    final_path = output_path or audio_dir / "narration.mp3"
    print(f"\n🔗 {len(audio_files)} ファイルを結合中...")
    
    if concat_audio(audio_files, final_path):
        total_duration = get_audio_duration(final_path)
        size_kb = final_path.stat().st_size // 1024
        print(f"✅ 完成: {final_path} ({total_duration:.1f}s, {size_kb}KB)")
        
        # クリーンアップ（gapとsilenceファイル）
        for f in audio_dir.glob("gap_*.mp3"):
            f.unlink(missing_ok=True)
        for f in audio_dir.glob("silence_*.mp3"):
            f.unlink(missing_ok=True)
        
        return final_path
    else:
        print("❌ 結合失敗")
        return None


def main():
    parser = argparse.ArgumentParser(description="ElevenLabs TTS ナレーション生成")
    parser.add_argument("--storyboard-dir", "-d", required=True, help="絵コンテディレクトリ")
    parser.add_argument("--voice", "-v", default="akari", help="ボイス名/ID (default: akari)")
    parser.add_argument("--model", "-m", default="eleven_multilingual_v2", help="TTSモデル")
    parser.add_argument("--stability", type=float, default=0.5, help="安定性 (0-1)")
    parser.add_argument("--similarity", type=float, default=0.75, help="類似度ブースト (0-1)")
    parser.add_argument("--speed", type=float, default=1.0, help="再生速度")
    parser.add_argument("--per-scene", action="store_true", help="フレームごと個別出力")
    parser.add_argument("--silence-gap", type=float, default=0.3, help="シーン間の無音（秒）")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    args = parser.parse_args()
    
    generate_audio(
        storyboard_dir=Path(args.storyboard_dir),
        voice=args.voice,
        model=args.model,
        stability=args.stability,
        similarity_boost=args.similarity,
        speed=args.speed,
        per_scene=args.per_scene,
        silence_gap=args.silence_gap,
        output_path=Path(args.output) if args.output else None,
    )


if __name__ == "__main__":
    main()
