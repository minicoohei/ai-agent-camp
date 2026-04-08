---
description: "When the user says /start-15-7 — Module 15 Lesson 15-7: YouTube Clipper で動画ハイライト抽出"
duration: 40分
prerequisites: ["FFmpeg", "yt-dlp", "Gemini API キー"]
level: intermediate
tags: ["video", "clipper", "subtitles", "ai-analysis"]
---

# Lesson 15-7: YouTube Clipper — 動画ハイライト抽出

## 学習目標

このレッスンでは、YouTube（や他プラットフォーム）の動画から
AIを使ってハイライトを自動抽出する方法を学びます。

1. 動画のダウンロードと字幕取得
2. AIによるセマンティックチャプター分割
3. 自然言語でのハイライト選択
4. クリップ抽出 + バイリンガル字幕生成
5. 字幕なし動画のGemini音声認識

---

## Step 1: 環境確認

まず必要なツールがインストールされているか確認しましょう。

```bash
yt-dlp --version
ffmpeg -version | head -1
python3 -c "import pysrt; print('pysrt OK')"    # Windowsでは python3 を python に読み替え
```

もし未インストールの場合:
```bash
pip install yt-dlp pysrt
sudo apt-get install ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg または https://ffmpeg.org/download.html からダウンロード
```

---

## Step 2: 動画情報の確認

好きなYouTube動画のURLを用意してください。
まず動画の情報を確認します:

```bash
python skills/youtube-clipper/scripts/downloader.py \
  "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --subs-only
```

出力で以下を確認:
- `subtitles_available`: 手動字幕の言語
- `auto_subtitles_available`: 自動字幕の言語
- `duration`: 動画の長さ

---

## Step 3: Clipperでチャプター分析

チャプター分析のみを実行してみましょう:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --chapters-only
```

AIが動画を意味的なチャプターに分割し、
各チャプターにタイトル、要約、highlight_scoreを付与します。

---

## Step 4: ハイライトクリップの抽出

スコアの高いチャプターをクリップとして抽出:

```bash
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=YOUR_VIDEO_ID" \
  --auto-select "score>0.7" \
  --burn-subtitles
```

`output/clips/` ディレクトリに以下が生成されます:
- 各クリップのMP4
- 元字幕 + 日本語翻訳字幕
- バイリンガルSRT
- SNS投稿用サマリー（JSON）

---

## Step 5: 字幕なし動画の文字起こし（発展）

字幕がない動画でも、Gemini音声認識で対応できます:

```bash
# ローカル動画ファイルで試す
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/video_without_subs.mp4
```

内部的にFFmpegで音声抽出 → Gemini 3.0 Flash Previewで文字起こしが行われます。

---

## 演習課題

1. **基本**: 好きなYouTube動画（5-15分）を選び、クリップを3つ以上抽出してください
2. **応用**: 英語動画のクリップにバイリンガル字幕（英日）を焼き込んでください
3. **発展**: 字幕なしの動画でGemini音声認識を試し、精度を確認してください

---

## 次のステップ

Lesson 15-8 では、抽出したクリップを Remotion でSNS用マーケティング素材に変換する方法を学びます。
