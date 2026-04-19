#!/usr/bin/env python3
"""Extract keyframes from video files with duplicate removal and optimization."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("Error: Pillow and numpy are required. Install with:")
    print("  pip install Pillow numpy")
    sys.exit(1)


def extract_all_frames(video_path: str, temp_dir: str, scale: float) -> list[str]:
    """Extract frames from video using ffmpeg at 1fps."""
    output_pattern = os.path.join(temp_dir, "frame_%04d.jpg")
    scale_filter = f"scale=iw*{scale}:ih*{scale}"
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vf", f"fps=1,{scale_filter}",
        "-q:v", "2",
        output_pattern,
        "-y", "-loglevel", "error"
    ]
    subprocess.run(cmd, check=True)
    frames = sorted(Path(temp_dir).glob("frame_*.jpg"))
    return [str(f) for f in frames]


def compute_histogram(image_path: str) -> np.ndarray:
    """Compute normalized color histogram for an image."""
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    hist_r = np.histogram(arr[:, :, 0], bins=32, range=(0, 256))[0]
    hist_g = np.histogram(arr[:, :, 1], bins=32, range=(0, 256))[0]
    hist_b = np.histogram(arr[:, :, 2], bins=32, range=(0, 256))[0]
    hist = np.concatenate([hist_r, hist_g, hist_b]).astype(float)
    total = hist.sum()
    if total > 0:
        hist /= total
    return hist


def histogram_similarity(h1: np.ndarray, h2: np.ndarray) -> float:
    """Compute histogram intersection similarity (0-1)."""
    return float(np.minimum(h1, h2).sum())


def filter_keyframes(frame_paths: list[str], threshold: float) -> list[str]:
    """Remove duplicate frames based on histogram similarity."""
    if not frame_paths:
        return []

    keyframes = [frame_paths[0]]
    prev_hist = compute_histogram(frame_paths[0])

    for path in frame_paths[1:]:
        curr_hist = compute_histogram(path)
        similarity = histogram_similarity(prev_hist, curr_hist)
        if similarity < threshold:
            keyframes.append(path)
            prev_hist = curr_hist

    return keyframes


def save_keyframes(keyframe_paths: list[str], output_dir: str, quality: int) -> list[str]:
    """Save keyframes to output directory with specified quality."""
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    for i, path in enumerate(keyframe_paths, 1):
        img = Image.open(path)
        out_path = os.path.join(output_dir, f"key_{i:04d}.jpg")
        img.save(out_path, "JPEG", quality=quality)
        saved.append(out_path)
    return saved


def estimate_tokens(image_paths: list[str]) -> int:
    """Estimate token count for images (rough: ~200 tokens per image at low res)."""
    return len(image_paths) * 200


def main():
    parser = argparse.ArgumentParser(description="Extract keyframes from video")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("-t", "--threshold", type=float, default=0.85,
                        help="Similarity threshold (higher = more frames kept)")
    parser.add_argument("-q", "--quality", type=int, default=30,
                        help="JPEG quality (1-100)")
    parser.add_argument("-s", "--scale", type=float, default=0.3,
                        help="Resize scale")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: <video_name>_keyframes/)")
    args = parser.parse_args()

    video_path = args.video
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)

    # Default output directory
    if args.output is None:
        video_name = Path(video_path).stem
        output_dir = str(Path(video_path).parent / f"{video_name}_keyframes")
    else:
        output_dir = args.output

    print(f"Extracting frames from: {video_path}")
    print(f"Settings: threshold={args.threshold}, quality={args.quality}, scale={args.scale}")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract all frames at 1fps
        all_frames = extract_all_frames(video_path, temp_dir, args.scale)
        print(f"Extracted {len(all_frames)} frames at 1fps")

        # Filter duplicates
        keyframes = filter_keyframes(all_frames, args.threshold)
        print(f"Filtered to {len(keyframes)} keyframes (removed {len(all_frames) - len(keyframes)} duplicates)")

        # Save keyframes
        saved_paths = save_keyframes(keyframes, output_dir, args.quality)

    # Get image size
    if saved_paths:
        img = Image.open(saved_paths[0])
        image_size = f"{img.width}x{img.height}"
    else:
        image_size = "N/A"

    # Estimate tokens
    total_tokens = estimate_tokens(saved_paths)

    # Output result as JSON
    result = {
        "keyframe_count": len(saved_paths),
        "image_size": image_size,
        "total_tokens": total_tokens,
        "cost_usd_opus": round(total_tokens * 0.015 / 1000, 4),
        "cost_usd_sonnet": round(total_tokens * 0.003 / 1000, 4),
        "cost_usd_haiku": round(total_tokens * 0.001 / 1000, 4),
        "files": [os.path.abspath(p) for p in saved_paths]
    }

    print(f"\nOutput directory: {output_dir}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
