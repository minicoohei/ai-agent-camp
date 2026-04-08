#!/usr/bin/env python3
"""
Extract keyframes from video files.
Removes duplicate frames and saves compressed images.
"""

import argparse
import subprocess
import tempfile
import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np


def calculate_similarity(img1_path: str, img2_path: str) -> float:
    """Calculate similarity between two images (0-1, where 1 is identical)."""
    img1 = Image.open(img1_path).convert('L')
    img2 = Image.open(img2_path).convert('L')

    size = (200, 400)
    img1 = img1.resize(size, Image.Resampling.LANCZOS)
    img2 = img2.resize(size, Image.Resampling.LANCZOS)

    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    arr1_norm = arr1 - arr1.mean()
    arr2_norm = arr2 - arr2.mean()

    numerator = np.sum(arr1_norm * arr2_norm)
    denominator = np.sqrt(np.sum(arr1_norm**2) * np.sum(arr2_norm**2))

    if denominator == 0:
        return 1.0

    return max(0, numerator / denominator)


def compress_and_save(src_path: Path, dest_path: Path, quality: int, scale: float) -> Path:
    """Compress and save image."""
    img = Image.open(src_path)

    if scale != 1.0:
        new_size = (int(img.width * scale), int(img.height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    dest_jpg = dest_path.with_suffix('.jpg')
    img.save(dest_jpg, 'JPEG', quality=quality, optimize=True)

    return dest_jpg


def extract_frames_with_ffmpeg(video_path: str, output_dir: Path) -> bool:
    """Extract all frames from video using ffmpeg."""
    output_pattern = output_dir / "frame_%04d.png"

    cmd = [
        "ffmpeg", "-i", video_path,
        "-vsync", "0",
        str(output_pattern),
        "-y", "-hide_banner", "-loglevel", "error"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def get_video_info(video_path: str) -> dict:
    """Get video information."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}

    return json.loads(result.stdout)


def extract_keyframes(
    video_path: str,
    output_dir: str,
    similarity_threshold: float = 0.85,
    quality: int = 30,
    scale: float = 0.3
) -> dict:
    """
    Extract keyframes from video.

    Returns:
        dict: Extraction result information
    """
    video_path = Path(video_path).resolve()
    if not video_path.exists():
        return {"error": f"Video file not found: {video_path}"}
    if not video_path.is_file():
        return {"error": f"Not a file: {video_path}"}

    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract all frames to temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Extract frames with ffmpeg
        if not extract_frames_with_ffmpeg(str(video_path), temp_path):
            return {"error": "Failed to extract frames with ffmpeg"}

        frames = sorted(temp_path.glob("frame_*.png"))

        if not frames:
            return {"error": "No frames found"}

        total_frames = len(frames)

        # Extract keyframes
        keyframes = [frames[0]]
        last_keyframe = frames[0]

        for frame in frames[1:]:
            similarity = calculate_similarity(str(last_keyframe), str(frame))
            if similarity < similarity_threshold:
                keyframes.append(frame)
                last_keyframe = frame

        if keyframes[-1] != frames[-1]:
            keyframes.append(frames[-1])

        # Compress and save
        saved_files = []
        total_size = 0

        for i, frame in enumerate(keyframes, start=1):
            dest = output_path / f"key_{i:04d}.jpg"
            saved_path = compress_and_save(frame, dest, quality=quality, scale=scale)
            size_kb = saved_path.stat().st_size / 1024
            total_size += size_kb
            saved_files.append(str(saved_path))

        # Get image dimensions
        sample_img = Image.open(saved_files[0])
        img_width, img_height = sample_img.width, sample_img.height

        # Token calculation (1000x1000 = 1,000,000px -> 1300 tokens)
        pixels_per_image = img_width * img_height
        tokens_per_image = int(pixels_per_image / 1_000_000 * 1300)
        total_tokens = tokens_per_image * len(keyframes)

        # Cost calculation (input token price: $/1M tokens)
        cost_opus = total_tokens * 15 / 1_000_000
        cost_sonnet = total_tokens * 3 / 1_000_000
        cost_haiku = total_tokens * 1 / 1_000_000

        return {
            "video_path": str(video_path),
            "output_dir": str(output_path),
            "total_frames": total_frames,
            "keyframe_count": len(keyframes),
            "reduction_rate": round((1 - len(keyframes) / total_frames) * 100, 1),
            "image_size": f"{img_width}x{img_height}",
            "total_size_kb": round(total_size, 1),
            "total_size_mb": round(total_size / 1024, 2),
            "tokens_per_image": tokens_per_image,
            "total_tokens": total_tokens,
            "cost_usd_opus": round(cost_opus, 3),
            "cost_usd_sonnet": round(cost_sonnet, 3),
            "cost_usd_haiku": round(cost_haiku, 4),
            "files": saved_files,
            "settings": {
                "similarity_threshold": similarity_threshold,
                "quality": quality,
                "scale": scale
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Extract keyframes from video")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("-o", "--output", default=None, help="Output directory")
    parser.add_argument("-t", "--threshold", type=float, default=0.85, help="Similarity threshold (default: 0.85)")
    parser.add_argument("-q", "--quality", type=int, default=30, help="JPEG quality (default: 30)")
    parser.add_argument("-s", "--scale", type=float, default=0.3, help="Resize scale (default: 0.3)")

    args = parser.parse_args()

    # Default output directory
    if args.output is None:
        video_path = Path(args.video)
        args.output = str(video_path.parent / f"{video_path.stem}_keyframes")

    result = extract_keyframes(
        video_path=args.video,
        output_dir=args.output,
        similarity_threshold=args.threshold,
        quality=args.quality,
        scale=args.scale
    )

    # JSON output
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
