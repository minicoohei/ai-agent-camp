"""
グリーンスクリーン合成モジュール

OpenCVを使用して動画の緑色領域にスクリーンショットを合成する。
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


# グリーンスクリーン検出のHSV範囲（調整可能）
GREEN_HSV_LOWER = (35, 80, 80)
GREEN_HSV_UPPER = (85, 255, 255)


def detect_green_region(frame: np.ndarray) -> Tuple[np.ndarray, Optional[Tuple[int, int, int, int]]]:
    """
    フレーム内の緑色領域を検出する
    
    Args:
        frame: BGR形式のフレーム
        
    Returns:
        (マスク, バウンディングボックス (x, y, w, h) or None)
    """
    # 遅延インポート（numpy/cv2互換性問題回避）
    import cv2
    import numpy as np

    # BGRからHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 緑色領域のマスクを作成
    lower = np.array(GREEN_HSV_LOWER)
    upper = np.array(GREEN_HSV_UPPER)
    mask = cv2.inRange(hsv, lower, upper)
    
    # ノイズ除去（モルフォロジー変換）
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return mask, None
    
    # 最大の輪郭を取得
    largest_contour = max(contours, key=cv2.contourArea)
    
    # 面積が小さすぎる場合はスキップ
    area = cv2.contourArea(largest_contour)
    frame_area = frame.shape[0] * frame.shape[1]
    if area < frame_area * 0.01:  # フレームの1%未満
        return mask, None
    
    # バウンディングボックスを取得
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    return mask, (x, y, w, h)


def composite_frame(
    frame: np.ndarray,
    screenshot: np.ndarray,
    mask: np.ndarray,
    bbox: Tuple[int, int, int, int],
    padding: int = 5,
) -> np.ndarray:
    """
    フレームにスクリーンショットを合成する
    
    Args:
        frame: 元フレーム (BGR)
        screenshot: 合成するスクリーンショット (BGR)
        mask: 緑色領域のマスク
        bbox: バウンディングボックス (x, y, w, h)
        padding: パディング（ピクセル）
        
    Returns:
        合成されたフレーム
    """
    x, y, w, h = bbox
    
    # パディングを適用
    x = max(0, x + padding)
    y = max(0, y + padding)
    w = max(1, w - padding * 2)
    h = max(1, h - padding * 2)
    
    # スクリーンショットをリサイズ
    resized_screenshot = cv2.resize(screenshot, (w, h), interpolation=cv2.INTER_AREA)
    
    # 合成用のマスクを作成（緑色領域のみ）
    roi_mask = mask[y:y+h, x:x+w]
    
    # マスクを3チャンネルに拡張
    roi_mask_3ch = cv2.merge([roi_mask, roi_mask, roi_mask])
    
    # フレームのROIを取得
    roi = frame[y:y+h, x:x+w]
    
    # マスクを使って合成
    # マスク部分（緑色）にスクリーンショットを配置
    result_roi = np.where(roi_mask_3ch > 0, resized_screenshot, roi)
    
    # 結果をフレームに戻す
    result = frame.copy()
    result[y:y+h, x:x+w] = result_roi
    
    return result


def composite_video(
    video_path: str,
    screenshot_path: str,
    output_path: Optional[str] = None,
    green_lower: Optional[Tuple[int, int, int]] = None,
    green_upper: Optional[Tuple[int, int, int]] = None,
    show_preview: bool = False,
    backend: str = "auto",
) -> str:
    """
    動画のグリーンスクリーン部分にスクリーンショットを合成する
    
    Args:
        video_path: 入力動画のパス
        screenshot_path: スクリーンショットのパス
        output_path: 出力動画のパス（Noneの場合は自動生成）
        green_lower: 緑色検出の下限HSV値
        green_upper: 緑色検出の上限HSV値
        show_preview: プレビューウィンドウを表示するか
        
    Returns:
        出力動画のパス
    """
    if backend not in {"auto", "cv2", "ffmpeg"}:
        raise ValueError(f"backend は auto/cv2/ffmpeg のいずれかを指定してください: {backend}")

    if backend == "ffmpeg":
        return composite_video_ffmpeg(
            video_path=video_path,
            screenshot_path=screenshot_path,
            output_path=output_path,
        )

    try:
        import cv2  # noqa: F401
        import numpy as np  # noqa: F401
        return _composite_video_cv2(
            video_path=video_path,
            screenshot_path=screenshot_path,
            output_path=output_path,
            green_lower=green_lower,
            green_upper=green_upper,
            show_preview=show_preview,
        )
    except Exception as e:
        if backend == "cv2":
            raise
        print(f"⚠️ OpenCV合成に失敗: {e}")
        print("   ffmpegベースの合成にフォールバックします")
        return composite_video_ffmpeg(
            video_path=video_path,
            screenshot_path=screenshot_path,
            output_path=output_path,
        )


def _composite_video_cv2(
    video_path: str,
    screenshot_path: str,
    output_path: Optional[str] = None,
    green_lower: Optional[Tuple[int, int, int]] = None,
    green_upper: Optional[Tuple[int, int, int]] = None,
    show_preview: bool = False,
) -> str:
    import cv2
    import numpy as np

    global GREEN_HSV_LOWER, GREEN_HSV_UPPER

    if green_lower is not None:
        GREEN_HSV_LOWER = tuple(green_lower)
    if green_upper is not None:
        GREEN_HSV_UPPER = tuple(green_upper)

    # 出力パスを決定
    if output_path is None:
        input_stem = Path(video_path).stem
        output_path = str(Path(video_path).parent / f"{input_stem}_composited.mp4")
    else:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"🎬 グリーンスクリーン合成中...")
    print(f"   入力動画: {video_path}")
    print(f"   スクリーンショット: {screenshot_path}")

    # 動画を開く
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"動画を開けません: {video_path}")

    # 動画のプロパティを取得
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"   解像度: {width}x{height}, FPS: {fps:.1f}, フレーム数: {total_frames}")

    # スクリーンショットを読み込み
    screenshot = cv2.imread(screenshot_path)
    if screenshot is None:
        raise ValueError(f"スクリーンショットを読み込めません: {screenshot_path}")

    # 出力動画のライターを作成
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    composited_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 緑色領域を検出
        mask, bbox = detect_green_region(frame)

        if bbox is not None:
            # 合成
            frame = composite_frame(frame, screenshot, mask, bbox)
            composited_count += 1

        # 出力
        out.write(frame)

        # プレビュー
        if show_preview:
            cv2.imshow("Preview", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frame_count += 1

        # 進捗表示
        if frame_count % 30 == 0:
            progress = frame_count / total_frames * 100
            print(f"   進捗: {progress:.1f}% ({frame_count}/{total_frames})", end="\r")

    # リソースを解放
    cap.release()
    out.release()
    if show_preview:
        cv2.destroyAllWindows()

    print(f"\n✅ 合成完了: {output_path}")
    print(f"   合成フレーム数: {composited_count}/{frame_count}")

    return output_path


def composite_video_ffmpeg(
    video_path: str,
    screenshot_path: str,
    output_path: Optional[str] = None,
) -> str:
    """ffmpegのcolorkeyで合成（OpenCV非依存）"""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg が見つかりません。OpenCVかffmpegを用意してください。")

    if output_path is None:
        input_stem = Path(video_path).stem
        output_path = str(Path(video_path).parent / f"{input_stem}_composited.mp4")
    else:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"🎬 ffmpeg合成中...")
    print(f"   入力動画: {video_path}")
    print(f"   スクリーンショット: {screenshot_path}")

    filter_complex = (
        "[1:v][0:v]scale2ref[bg][vid];"
        "[vid]colorkey=0x00FF00:0.3:0.2[fg];"
        "[bg][fg]overlay=0:0:format=auto"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", screenshot_path,
        "-filter_complex", filter_complex,
        "-map", "0:a?",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ ffmpeg合成完了: {output_path}")
    return output_path


def preview_green_detection(
    video_path: str,
    frame_number: int = 0,
    save_path: Optional[str] = None,
) -> None:
    """
    緑色検出のプレビューを表示/保存する
    
    Args:
        video_path: 動画のパス
        frame_number: 確認するフレーム番号
        save_path: 保存先パス（Noneの場合は表示のみ）
    """
    import cv2
    import numpy as np

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("フレームを読み込めません")
        return
    
    mask, bbox = detect_green_region(frame)
    
    # デバッグ画像を作成
    debug_frame = frame.copy()
    
    # マスクを可視化（緑色で表示）
    mask_colored = np.zeros_like(frame)
    mask_colored[:, :, 1] = mask  # 緑チャンネルにマスクを設定
    debug_frame = cv2.addWeighted(debug_frame, 0.7, mask_colored, 0.3, 0)
    
    # バウンディングボックスを描画
    if bbox is not None:
        x, y, w, h = bbox
        cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(debug_frame, f"Green: {w}x{h}", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    if save_path:
        cv2.imwrite(save_path, debug_frame)
        print(f"プレビュー保存: {save_path}")
    else:
        cv2.imshow("Green Detection Preview", debug_frame)
        print("Qキーで終了")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="グリーンスクリーン合成")
    parser.add_argument("video", help="入力動画のパス")
    parser.add_argument("screenshot", help="スクリーンショットのパス")
    parser.add_argument("--output", "-o", help="出力動画のパス")
    parser.add_argument("--preview", "-p", action="store_true", help="プレビュー表示")
    parser.add_argument("--debug-frame", "-d", type=int, default=None,
                       help="指定フレームの検出をデバッグ表示")
    
    args = parser.parse_args()
    
    if args.debug_frame is not None:
        preview_green_detection(args.video, args.debug_frame)
    else:
        composite_video(
            video_path=args.video,
            screenshot_path=args.screenshot,
            output_path=args.output,
            show_preview=args.preview,
        )
