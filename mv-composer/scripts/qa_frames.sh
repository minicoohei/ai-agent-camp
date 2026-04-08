#!/bin/bash
# QA Frame Extractor — remotion render 後に自動実行
# 動画を10等分してフレームを抽出し、レビュー用ディレクトリに保存
#
# Usage: qa_frames.sh <video_path>
# Example: qa_frames.sh out/TaxAccountantDemo_v8.mp4

set -euo pipefail

VIDEO="$1"
if [[ ! -f "$VIDEO" ]]; then
  echo "ERROR: Video not found: $VIDEO"
  exit 1
fi

# 動画名からQAディレクトリ名を生成
BASENAME=$(basename "$VIDEO" .mp4)
QA_DIR="data/qa_${BASENAME}"
mkdir -p "$QA_DIR"

# 動画の長さ取得（秒）
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO" 2>/dev/null | cut -d. -f1)
if [[ -z "$DURATION" || "$DURATION" -lt 2 ]]; then
  echo "ERROR: Could not determine video duration"
  exit 1
fi

# 10等分 + 先頭・末尾のフレームも取得
NUM_SAMPLES=12
rm -f "$QA_DIR"/qa_*.png

echo "Extracting $NUM_SAMPLES QA frames from ${DURATION}s video..."

for i in $(seq 0 $((NUM_SAMPLES - 1))); do
  if [[ $i -eq 0 ]]; then
    T=1
  elif [[ $i -eq $((NUM_SAMPLES - 1)) ]]; then
    T=$((DURATION - 2))
  else
    T=$(( (DURATION * i) / (NUM_SAMPLES - 1) ))
  fi

  OUTFILE="$QA_DIR/qa_$(printf '%02d' $i)_${T}s.png"
  ffmpeg -y -ss "$T" -i "$VIDEO" -frames:v 1 "$OUTFILE" 2>/dev/null
done

COUNT=$(ls "$QA_DIR"/qa_*.png 2>/dev/null | wc -l | tr -d ' ')
echo ""
echo "=== QA Frame Extraction Complete ==="
echo "Video: $VIDEO"
echo "Duration: ${DURATION}s"
echo "Frames: $COUNT files in $QA_DIR"
echo ""
echo "Review checklist:"
echo "  - [ ] 不要な余白がないか（要素が画面の80%以上を占めているか）"
echo "  - [ ] デザイン上未熟な点がないか（フォントサイズ、色彩バランス、余白の均一性）"
echo "  - [ ] 見切れてないか（テキスト・UI要素が画面外にはみ出していないか）"
echo "  - [ ] カクつき・品質劣化がないか（ぼやけ、ノイズ、意図しない黒フレーム）"
echo ""
echo "QA_DIR=$QA_DIR"

ls -la "$QA_DIR"/qa_*.png
