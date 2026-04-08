"""
Ken Burns効果モジュール（B-roll用）

静止画にズーム・パン効果を付けて擬似動画化する。
A-roll（I2V動画）のコストを削減するためのB-roll生成用。

使い方:
    from tools.ugc.ken_burns import generate_broll
    generate_broll("frame.png", "broll.mp4", duration=10, effect="zoom_in")
"""

import shutil
import subprocess
from typing import Optional


def _ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg が見つかりません。")


# 効果プリセット: (zoom_start, zoom_end, x_expr, y_expr)
# zoompan filter: z=ズーム率, x/y=表示領域の左上座標
EFFECTS = {
    "zoom_in": {
        "z": "'min(zoom+0.0015,1.5)'",
        "x": "'iw/2-(iw/zoom/2)'",
        "y": "'ih/2-(ih/zoom/2)'",
    },
    "zoom_out": {
        "z": "'if(eq(on,1),1.5,max(zoom-0.0015,1.0))'",
        "x": "'iw/2-(iw/zoom/2)'",
        "y": "'ih/2-(ih/zoom/2)'",
    },
    "pan_left": {
        "z": "'1.3'",
        "x": "'iw*0.3-iw*0.3*on/(25*{duration})'",
        "y": "'ih/2-(ih/zoom/2)'",
    },
    "pan_right": {
        "z": "'1.3'",
        "x": "'iw*0.0+iw*0.3*on/(25*{duration})'",
        "y": "'ih/2-(ih/zoom/2)'",
    },
    "slow_zoom": {
        "z": "'min(zoom+0.0008,1.25)'",
        "x": "'iw/2-(iw/zoom/2)'",
        "y": "'ih/2-(ih/zoom/2)'",
    },
    "pan_down": {
        "z": "'1.2'",
        "x": "'iw/2-(iw/zoom/2)'",
        "y": "'ih*0.0+ih*0.2*on/(25*{duration})'",
    },
    "pan_up": {
        "z": "'1.2'",
        "x": "'iw/2-(iw/zoom/2)'",
        "y": "'ih*0.2-ih*0.2*on/(25*{duration})'",
    },
}


def generate_broll(
    image_path: str,
    output_path: str,
    duration: float = 10.0,
    effect: str = "zoom_in",
    width: int = 1920,
    height: int = 1080,
    fps: int = 25,
) -> None:
    """静止画からKen Burns効果付きのB-roll動画を生成

    Args:
        image_path: 入力画像パス
        output_path: 出力動画パス（MP4）
        duration: 動画の長さ（秒）
        effect: 効果名（zoom_in, zoom_out, pan_left, pan_right,
                slow_zoom, pan_down, pan_up）
        width: 出力動画の幅
        height: 出力動画の高さ
        fps: フレームレート
    """
    _ensure_ffmpeg()

    if effect not in EFFECTS:
        raise ValueError(
            f"未対応の効果: {effect}。利用可能: {', '.join(EFFECTS.keys())}"
        )

    params = EFFECTS[effect]
    total_frames = int(fps * duration)

    # durationプレースホルダを実際の値に置換
    z_expr = params["z"].format(duration=duration)
    x_expr = params["x"].format(duration=duration)
    y_expr = params["y"].format(duration=duration)

    zoompan_filter = (
        f"zoompan=z={z_expr}:x={x_expr}:y={y_expr}"
        f":d={total_frames}:s={width}x{height}:fps={fps}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", zoompan_filter,
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        output_path,
    ]
    subprocess.run(cmd, check=True)


def generate_broll_batch(
    images: list[dict],
    output_dir: str,
    default_duration: float = 10.0,
    default_effect: str = "zoom_in",
    width: int = 1920,
    height: int = 1080,
) -> list[str]:
    """複数画像のB-rollを一括生成

    Args:
        images: [{"path": "image.png", "effect": "zoom_in", "duration": 10}, ...]
            effectとdurationは省略可。
        output_dir: 出力先ディレクトリ
        default_duration: デフォルトの動画長さ
        default_effect: デフォルトの効果
        width: 出力動画の幅
        height: 出力動画の高さ

    Returns:
        生成された動画パスのリスト
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    outputs = []
    for i, img in enumerate(images):
        path = img["path"]
        effect = img.get("effect", default_effect)
        duration = img.get("duration", default_duration)
        out = os.path.join(output_dir, f"broll_{i:03d}.mp4")
        generate_broll(path, out, duration=duration, effect=effect,
                       width=width, height=height)
        outputs.append(out)
    return outputs
