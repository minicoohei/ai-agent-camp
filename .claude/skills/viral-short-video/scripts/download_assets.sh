#!/bin/bash
# Viral Short Video - アセットダウンロードスクリプト
# 初回セットアップ時に1回実行してください。
# 依存: yt-dlp, ffmpeg

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/../assets"

GAMEPLAY_DIR="$ASSETS_DIR/gameplay"
HOOKS_DIR="$ASSETS_DIR/hooks"

mkdir -p "$GAMEPLAY_DIR" "$HOOKS_DIR"

# yt-dlp 共通オプション: 1080p以下のMP4、リコード
YT_OPTS=(-S "res:1080,ext:mp4" --recode mp4 --no-playlist --no-overwrites)

echo "=== Viral Short Video: アセットダウンロード ==="
echo ""

# --- ゲームプレイ背景素材 ---
echo "[1/5] Subway Surfers (26min, 縦型HD, No Copyright)..."
if [ ! -f "$GAMEPLAY_DIR/subway_surfers.mp4" ]; then
  yt-dlp "${YT_OPTS[@]}" \
    -o "$GAMEPLAY_DIR/subway_surfers.mp4" \
    "https://www.youtube.com/watch?v=Iot_bB8lKgE" &
else
  echo "  -> 既にダウンロード済み。スキップ"
fi

echo "[2/5] Minecraft Parkour (5min, 縦型2K 60fps, No Copyright)..."
if [ ! -f "$GAMEPLAY_DIR/minecraft.mp4" ]; then
  yt-dlp "${YT_OPTS[@]}" \
    -o "$GAMEPLAY_DIR/minecraft.mp4" \
    "https://www.youtube.com/watch?v=G3gz-p3hgOY" &
else
  echo "  -> 既にダウンロード済み。スキップ"
fi

# --- フックコンピレーション素材 ---
echo "[3/5] Hook: 10 TikTok Hooks You Can Use To Go Viral..."
if [ ! -f "$HOOKS_DIR/hook_viral_10.mp4" ]; then
  yt-dlp "${YT_OPTS[@]}" \
    -o "$HOOKS_DIR/hook_viral_10.mp4" \
    "https://www.youtube.com/watch?v=zIvOY4JTkbs" &
else
  echo "  -> 既にダウンロード済み。スキップ"
fi

echo "[4/5] Hook: This HOOK Combo Will Get You Viral on TikTok..."
if [ ! -f "$HOOKS_DIR/hook_trifecta.mp4" ]; then
  yt-dlp "${YT_OPTS[@]}" \
    -o "$HOOKS_DIR/hook_trifecta.mp4" \
    "https://www.youtube.com/watch?v=VShCOPbSkUs" &
else
  echo "  -> 既にダウンロード済み。スキップ"
fi

echo "[5/5] Hook: This Hook Made \$600K GMV on TikTok Shop..."
if [ ! -f "$HOOKS_DIR/hook_600k_gmv.mp4" ]; then
  yt-dlp "${YT_OPTS[@]}" \
    -o "$HOOKS_DIR/hook_600k_gmv.mp4" \
    "https://www.youtube.com/watch?v=NrV8G0PiRkI" &
else
  echo "  -> 既にダウンロード済み。スキップ"
fi

# 全バックグラウンドジョブの完了を待つ
echo ""
echo "ダウンロード中... (バックグラウンド並列実行)"
wait

echo ""
echo "=== ダウンロード完了 ==="
echo ""
echo "ファイル一覧:"
ls -lh "$GAMEPLAY_DIR"/*.mp4 2>/dev/null || echo "  (gameplay: なし)"
ls -lh "$HOOKS_DIR"/*.mp4 2>/dev/null || echo "  (hooks: なし)"
echo ""
echo "使い方:"
echo "  # ゲームプレイ背景でスプリットスクリーン"
echo "  python skills/video-editor/scripts/compose_video.py --split-screen subway_surfers"
echo ""
echo "  # フックコンピを分析してピークフック抽出"
echo "  python skills/viral-short-video/scripts/generate_viral_script.py --analyze-video hook_viral_10"
