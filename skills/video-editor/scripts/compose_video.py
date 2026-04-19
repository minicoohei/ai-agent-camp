"""
Video Composer - scenes.json + フレーム画像/動画 → 最終動画
ffmpegベースでサンドボックスでも動作する。
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional


# ffmpegパス（静的バイナリ）
FFMPEG = os.environ.get("FFMPEG_PATH", str(Path(__file__).parents[3] / ".bin" / "ffmpeg"))

# TikTok仕様
TIKTOK_WIDTH = 1080
TIKTOK_HEIGHT = 1920
FPS = 30

# フォントパス候補
FONT_PATHS = [
    str(Path(__file__).parents[3] / ".lib" / "NotoSansCJKjp-Bold.otf"),
    # Linux
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    # macOS
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    # Windows
    "C:/Windows/Fonts/msgothic.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/arialbd.ttf",
]


def find_font() -> str:
    """利用可能なフォントを探す"""
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            return fp
    # フォールバック: fc-listで探す (Windows以外)
    if platform.system() != "Windows":
        try:
            result = subprocess.run(["fc-list", ":style=Bold", "-f", "%{file}\n"],
                                    capture_output=True, text=True, timeout=5)
            for line in result.stdout.strip().split("\n"):
                if "Noto" in line and "CJK" in line:
                    return line.strip()
                if "Noto" in line:
                    return line.strip()
            # 最初に見つかったBoldフォント
            lines = result.stdout.strip().split("\n")
            if lines and lines[0]:
                return lines[0].strip()
        except Exception:
            pass
    return ""


def run_ffmpeg(args: List[str], desc: str = "") -> bool:
    """ffmpegコマンド実行"""
    cmd = [FFMPEG] + args
    if desc:
        print(f"  🎬 {desc}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"    ❌ エラー: {result.stderr[-200:]}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print(f"    ❌ タイムアウト")
        return False


def parse_timestamp(ts: str) -> tuple:
    """タイムスタンプ "0:00-0:02" を秒に変換"""
    start_str, end_str = ts.split("-")
    def to_sec(t):
        parts = t.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    return to_sec(start_str), to_sec(end_str)


def break_japanese_text(text: str, max_chars: int = 7) -> str:
    """日本語テキストを改行"""
    if len(text) <= max_chars:
        return text
    # 改行ポイントを探す
    break_chars = "、。！？　 …のをにはでがと"
    best_break = max_chars
    for j in range(max_chars, max(0, max_chars - 3), -1):
        if j < len(text) and text[j] in break_chars:
            best_break = j + 1
            break
    line1 = text[:best_break]
    line2 = text[best_break:best_break + max_chars]
    return f"{line1}\n{line2}" if line2 else line1


def create_clip_from_image(
    image_path: Path,
    output_path: Path,
    duration: float,
    motion_type: str = "static",
    frame_index: int = 0
) -> bool:
    """画像から動画クリップを作成"""
    if motion_type == "ken_burns":
        # ズームイン or パンレフト（交互）
        if frame_index % 2 == 0:
            vf = (f"scale={TIKTOK_WIDTH}:{TIKTOK_HEIGHT}:force_original_aspect_ratio=increase,"
                  f"crop={TIKTOK_WIDTH}:{TIKTOK_HEIGHT},"
                  f"zoompan=z='min(zoom+0.001,1.15)':d={int(duration*FPS)}:"
                  f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                  f"s={TIKTOK_WIDTH}x{TIKTOK_HEIGHT}:fps={FPS}")
        else:
            vf = (f"scale={int(TIKTOK_WIDTH*1.1)}:{int(TIKTOK_HEIGHT*1.1)}:force_original_aspect_ratio=increase,"
                  f"crop={TIKTOK_WIDTH}:{TIKTOK_HEIGHT},"
                  f"zoompan=z='1.1':d={int(duration*FPS)}:"
                  f"x='if(eq(on,1),0,x+1)':y='ih/2-(ih/zoom/2)':"
                  f"s={TIKTOK_WIDTH}x{TIKTOK_HEIGHT}:fps={FPS}")
    else:
        vf = f"scale={TIKTOK_WIDTH}:{TIKTOK_HEIGHT}:force_original_aspect_ratio=increase,crop={TIKTOK_WIDTH}:{TIKTOK_HEIGHT}"

    return run_ffmpeg([
        "-y", "-loop", "1", "-i", str(image_path),
        "-vf", vf,
        "-t", str(duration), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(output_path)
    ], f"F{frame_index} ({motion_type}) {duration}s")


def get_video_resolution(video_path: Path) -> tuple:
    """動画の解像度を取得"""
    result = subprocess.run(
        [FFMPEG, "-i", str(video_path)],
        capture_output=True, text=True, timeout=10
    )
    import re
    match = re.search(r'(\d{3,4})x(\d{3,4})', result.stderr)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 0, 0


def normalize_i2v_clip(
    input_path: Path,
    output_path: Path,
    duration: float,
    target_width: int = TIKTOK_WIDTH,
    target_height: int = TIKTOK_HEIGHT
) -> bool:
    """i2V動画をターゲット解像度に正規化"""
    src_w, src_h = get_video_resolution(input_path)
    src_aspect = src_w / src_h if src_h > 0 else 1
    target_aspect = target_width / target_height
    
    # アスペクト比が近い場合はそのままスケール+クロップ
    if abs(src_aspect - target_aspect) < 0.15:
        return run_ffmpeg([
            "-y", "-i", str(input_path),
            "-vf", f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
                   f"crop={target_width}:{target_height}",
            "-t", str(duration), "-r", str(FPS),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(output_path)
        ], f"i2Vスケール {src_w}x{src_h}→{target_width}x{target_height}")
    
    # アスペクト比が大きく異なる場合はぼかし背景
    print(f"    ⚠️ アスペクト比不一致 ({src_w}x{src_h} → {target_width}x{target_height})、ぼかし背景適用")
    return run_ffmpeg([
        "-y", "-i", str(input_path),
        "-filter_complex",
        f"[0:v]split=2[bg][fg];"
        f"[bg]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},boxblur=20:20[bgblur];"
        f"[fg]scale={target_width}:-1:force_original_aspect_ratio=decrease[fgscaled];"
        f"[bgblur][fgscaled]overlay=(W-w)/2:(H-h)/2[out]",
        "-map", "[out]",
        "-t", str(duration), "-r", str(FPS),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(output_path)
    ], f"i2Vぼかし背景 {src_w}x{src_h}→{target_width}x{target_height}")


def generate_ass_subtitle(
    text: str,
    duration: float,
    position: str = "center",
    style: str = "bold",
    font_name: str = "Noto Sans CJK JP"
) -> str:
    """ASS字幕ファイルの内容を生成"""
    display_text = break_japanese_text(text)
    # ASS改行
    display_text = display_text.replace("\n", "\\N")

    font_size = 64 if style == "bold" else (48 if style == "subtitle" else 40)
    border_w = 3 if style == "bold" else 2

    # MarginV で位置調整 (画面下からの距離)
    margin_v = {
        "top": TIKTOK_HEIGHT - int(TIKTOK_HEIGHT * 0.22),
        "center": int(TIKTOK_HEIGHT * 0.35),  # 下から35% = 上から65%あたり
        "bottom": int(TIKTOK_HEIGHT * 0.22),
    }.get(position, int(TIKTOK_HEIGHT * 0.35))

    # ASS alignment: 2 = bottom center
    alignment = 2

    end_time = f"0:00:{duration:05.2f}"

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {TIKTOK_WIDTH}
PlayResY: {TIKTOK_HEIGHT}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,{border_w},2,{alignment},40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{end_time},Caption,,0,0,0,,{{\\fad(200,200)}}{display_text}
"""
    return ass_content


def add_captions_to_clip(
    input_path: Path,
    output_path: Path,
    text: str,
    font_path: str,
    position: str = "center",
    style: str = "bold",
    duration: float = 2.0
) -> bool:
    """ASS字幕でキャプションを焼き込み"""
    if not text:
        return run_ffmpeg(["-y", "-i", str(input_path), "-c", "copy", str(output_path)])

    # フォント名を取得
    font_basename = Path(font_path).stem if font_path else "Noto Sans CJK JP"
    # OTF/TTFファイル名からフォント名を推測
    font_name_map = {
        "NotoSansCJKjp-Bold": "Noto Sans CJK JP",
        "DejaVuSans-Bold": "DejaVu Sans",
    }
    font_name = font_name_map.get(font_basename, font_basename)
    
    # ASS字幕ファイル生成
    ass_content = generate_ass_subtitle(text, duration, position, style, font_name)
    ass_path = output_path.with_suffix(".ass")
    ass_path.write_text(ass_content, encoding="utf-8")

    # fontsdir指定でカスタムフォントを読み込ませる
    fonts_dir = str(Path(font_path).parent) if font_path else ""
    vf = f"ass={ass_path}:fontsdir={fonts_dir}" if fonts_dir else f"ass={ass_path}"
    
    return run_ffmpeg([
        "-y", "-i", str(input_path),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(output_path)
    ], f"キャプション追加(ASS)")


def generate_i2v_clips(
    storyboard_dir: Path,
    scenes: List[Dict],
    aspect_ratio: str = "9:16",
    resolution: str = "480p"
) -> Dict[int, Path]:
    """
    i2Vが必要なフレームのクリップをfal.aiで生成
    
    Args:
        storyboard_dir: 絵コンテディレクトリ
        scenes: シーンリスト
        aspect_ratio: 動画のアスペクト比 ("9:16", "16:9", "1:1")
        resolution: 解像度 ("480p", "720p")
    
    Returns:
        {frame_number: video_path} の辞書
    """
    import time
    
    fal_key = os.environ.get("FAL_KEY", "")
    if not fal_key:
        print("⚠️ FAL_KEY未設定。i2Vクリップをスキップ")
        return {}
    
    frames_dir = storyboard_dir / "frames"
    video_dir = storyboard_dir / "video"
    video_dir.mkdir(parents=True, exist_ok=True)
    
    # i2Vが必要なフレームを特定
    i2v_scenes = [s for s in scenes if s.get("motion_type") == "i2v"]
    if not i2v_scenes:
        return {}
    
    print(f"\n🎬 i2V動画生成: {len(i2v_scenes)}フレーム (aspect_ratio={aspect_ratio}, resolution={resolution})")
    
    # 既に生成済みのクリップをスキップ
    jobs = {}
    for scene in i2v_scenes:
        fn = scene["frame_number"]
        frame_num = f"{fn:02d}"
        output_file = video_dir / f"frame_{frame_num}_i2v.mp4"
        
        if output_file.exists() and output_file.stat().st_size > 1000:
            print(f"  ✅ F{fn}: 生成済みスキップ")
            jobs[fn] = {"path": output_file, "done": True}
            continue
        
        # フレーム画像をアップロード
        img_path = _find_frame(frames_dir, frame_num)
        if not img_path:
            print(f"  ❌ F{fn}: フレーム画像なし")
            continue
        
        import urllib.request
        # catbox.moeにアップロード
        print(f"  📤 F{fn}: アップロード中...")
        upload_result = subprocess.run(
            ["curl", "-s", "-F", "reqtype=fileupload",
             "-F", f"fileToUpload=@{img_path}",
             "https://catbox.moe/user/api.php"],
            capture_output=True, text=True, timeout=30
        )
        img_url = upload_result.stdout.strip()
        if not img_url.startswith("http"):
            print(f"  ❌ F{fn}: アップロード失敗")
            continue
        
        # fal.ai i2Vジョブ投入
        import json as json_mod
        headers = {
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json"
        }
        payload = json_mod.dumps({
            "image_url": img_url,
            "prompt": "Smooth natural movement, consistent character, cinematic quality",
            "num_frames": 81,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "enable_safety_checker": False
        }).encode()
        
        req = urllib.request.Request(
            "https://queue.fal.run/fal-ai/wan-i2v",
            data=payload, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json_mod.loads(resp.read())
                request_id = result.get("request_id", "")
                if request_id:
                    print(f"  🚀 F{fn}: ジョブ投入 ({request_id[:8]}...)")
                    jobs[fn] = {"request_id": request_id, "path": output_file, "done": False}
                else:
                    print(f"  ❌ F{fn}: ジョブ投入失敗")
        except Exception as e:
            print(f"  ❌ F{fn}: {e}")
    
    # ポーリング
    import urllib.request
    import json as json_mod
    pending = {fn: j for fn, j in jobs.items() if not j.get("done")}
    while pending:
        time.sleep(10)
        for fn, job in list(pending.items()):
            try:
                req = urllib.request.Request(
                    f"https://queue.fal.run/fal-ai/wan-i2v/requests/{job['request_id']}/status",
                    headers={"Authorization": f"Key {fal_key}"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    status_data = json_mod.loads(resp.read())
                    status = status_data.get("status", "UNKNOWN")
                
                if status == "COMPLETED":
                    # 結果取得
                    req2 = urllib.request.Request(
                        f"https://queue.fal.run/fal-ai/wan-i2v/requests/{job['request_id']}",
                        headers={"Authorization": f"Key {fal_key}"}
                    )
                    with urllib.request.urlopen(req2, timeout=30) as resp2:
                        result_data = json_mod.loads(resp2.read())
                        video_url = result_data.get("video", {}).get("url", "")
                    
                    if video_url:
                        urllib.request.urlretrieve(video_url, str(job["path"]))
                        size_kb = job["path"].stat().st_size // 1024
                        print(f"  ✅ F{fn}: 完了 ({size_kb}KB)")
                        job["done"] = True
                        del pending[fn]
                    else:
                        print(f"  ❌ F{fn}: 動画URL取得失敗")
                        del pending[fn]
                elif status == "FAILED":
                    print(f"  ❌ F{fn}: 生成失敗")
                    del pending[fn]
                else:
                    print(f"  ⏳ F{fn}: {status}")
            except Exception as e:
                print(f"  ⚠️ F{fn}: ポーリングエラー: {e}")
    
    return {fn: j["path"] for fn, j in jobs.items() if j.get("done") and j["path"].exists()}


def compose_video(
    storyboard_dir: Path,
    output_path: Path,
    with_captions: bool = True,
    audio_path: Optional[Path] = None,
    aspect_ratio: str = "9:16",
    generate_i2v: bool = False,
    i2v_resolution: str = "480p"
) -> Optional[Path]:
    """
    メイン: scenes.json + フレーム → 最終動画
    """
    scenes_path = storyboard_dir / "scenes.json"
    frames_dir = storyboard_dir / "frames"
    video_dir = storyboard_dir / "video"
    work_dir = storyboard_dir / "video" / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    if not scenes_path.exists():
        print(f"❌ scenes.json not found: {scenes_path}")
        return None

    with open(scenes_path) as f:
        data = json.load(f)

    scenes = data["scenes"]
    
    # i2Vクリップ生成（必要な場合）
    if generate_i2v:
        generate_i2v_clips(storyboard_dir, scenes, aspect_ratio, i2v_resolution)
    
    font_path = find_font() if with_captions else ""
    if with_captions and not font_path:
        print("⚠️ フォントが見つかりません。キャプションなしで続行")
        with_captions = False
    else:
        print(f"🔤 フォント: {font_path}")

    print(f"\n📋 {len(scenes)}シーンを処理中...")
    clip_paths = []

    for scene in scenes:
        fn = scene["frame_number"]
        frame_num = f"{fn:02d}"
        start_sec, end_sec = parse_timestamp(scene["timestamp"])
        duration = end_sec - start_sec
        motion_type = scene.get("motion_type", "static")
        text_overlay = scene.get("text_overlay", {})
        narration = scene.get("narration", "")

        print(f"\n🎞️ フレーム {fn}: [{motion_type}] {duration}s")

        # Step 1: 素材クリップ作成
        raw_clip = work_dir / f"raw_{frame_num}.mp4"

        if motion_type == "i2v":
            i2v_path = video_dir / f"frame_{frame_num}_i2v.mp4"
            if i2v_path.exists():
                normalize_i2v_clip(i2v_path, raw_clip, duration)
            else:
                print(f"    ⚠️ i2V動画なし: {i2v_path} → 静止画で代替")
                img = _find_frame(frames_dir, frame_num)
                if img:
                    create_clip_from_image(img, raw_clip, duration, "static", fn)
        else:
            img = _find_frame(frames_dir, frame_num)
            if img:
                create_clip_from_image(img, raw_clip, duration, motion_type, fn)

        if not raw_clip.exists():
            print(f"    ❌ クリップ作成失敗 → スキップ")
            continue

        # Step 2: キャプション追加
        if with_captions:
            caption_text = text_overlay.get("main_text", "") or narration
            if caption_text:
                captioned_clip = work_dir / f"cap_{frame_num}.mp4"
                position = text_overlay.get("position", "center")
                style = text_overlay.get("style", "bold")
                add_captions_to_clip(raw_clip, captioned_clip, caption_text, font_path, position, style, duration)
                if captioned_clip.exists():
                    clip_paths.append(captioned_clip)
                    continue

        clip_paths.append(raw_clip)

    if not clip_paths:
        print("❌ 有効なクリップがありません")
        return None

    # Step 3: 全クリップ結合
    print(f"\n🔗 {len(clip_paths)}クリップを結合中...")
    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w") as f:
        for cp in clip_paths:
            f.write(f"file '{cp.resolve()}'\n")

    # 中間出力
    merged = work_dir / "merged.mp4"
    run_ffmpeg([
        "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
        str(merged)
    ], "結合")

    if not merged.exists():
        print("❌ 結合失敗")
        return None

    # Step 4: 音声合成（オプション）
    if audio_path and audio_path.exists():
        print(f"🔊 音声合成: {audio_path}")
        run_ffmpeg([
            "-y", "-i", str(merged), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(output_path)
        ], "音声合成")
    else:
        # 音声なし → そのまま出力
        import shutil
        shutil.move(str(merged), str(output_path))

    if output_path.exists():
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ 完成: {output_path} ({size_mb:.1f}MB)")
        return output_path
    else:
        print("❌ 出力ファイル作成失敗")
        return None


def _find_frame(frames_dir: Path, frame_num: str) -> Optional[Path]:
    """フレーム画像を探す（jpg優先、なければpng）"""
    for ext in [".jpg", ".png"]:
        p = frames_dir / f"frame_{frame_num}{ext}"
        if p.exists():
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Video Composer - ffmpegベース動画結合")
    parser.add_argument("--storyboard-dir", "-d", required=True, help="絵コンテディレクトリ")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--captions", action="store_true", default=True, help="キャプション追加")
    parser.add_argument("--no-captions", action="store_true", help="キャプションなし")
    parser.add_argument("--audio", "-a", help="音声ファイルパス")
    parser.add_argument("--aspect-ratio", "-ar", default="9:16",
                        choices=["9:16", "16:9", "1:1"],
                        help="アスペクト比（デフォルト: 9:16）")
    parser.add_argument("--generate-i2v", action="store_true",
                        help="i2Vクリップを自動生成（FAL_KEY必要）")
    parser.add_argument("--i2v-resolution", default="480p",
                        choices=["480p", "720p"],
                        help="i2V解像度（デフォルト: 480p）")
    args = parser.parse_args()

    # アスペクト比に応じた解像度設定
    RESOLUTIONS = {
        "9:16": (1080, 1920),
        "16:9": (1920, 1080),
        "1:1": (1080, 1080),
    }
    global TIKTOK_WIDTH, TIKTOK_HEIGHT
    TIKTOK_WIDTH, TIKTOK_HEIGHT = RESOLUTIONS.get(args.aspect_ratio, (1080, 1920))

    storyboard_dir = Path(args.storyboard_dir)
    output_path = Path(args.output) if args.output else storyboard_dir / "video" / "final_tiktok.mp4"

    compose_video(
        storyboard_dir=storyboard_dir,
        output_path=output_path,
        with_captions=not args.no_captions,
        audio_path=Path(args.audio) if args.audio else None,
        aspect_ratio=args.aspect_ratio,
        generate_i2v=args.generate_i2v,
        i2v_resolution=args.i2v_resolution
    )


if __name__ == "__main__":
    main()
