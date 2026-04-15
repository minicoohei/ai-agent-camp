---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video/chapter.yaml"
duration: 40分
prerequisites: ["start-15-2"]
level: intermediate
tags: ["video", "clipper", "subtitles", "ai-analysis"]
---

# Lesson 15-3: YouTube Clipper — 動画ハイライト抽出

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
uv add yt-dlp pysrt
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

## 無音区間の検出と修正

抽出したクリップから不要な無音区間を検出・除去します。

```bash
# 無音区間を検出（-50dB以下が2秒以上続く箇所）
ffmpeg -i output/clips/clip_01.mp4 -af silencedetect=noise=-50dB:d=2 -f null - 2>&1 | grep "silence_"

# 無音区間を自動除去
ffmpeg -i output/clips/clip_01.mp4 -af silenceremove=start_periods=1:start_silence=2:start_threshold=-50dB:stop_periods=-1:stop_silence=2:stop_threshold=-50dB output/clips/clip_01_trimmed.mp4
```

> **パラメータの調整**: `noise=-50dB` は環境に応じて `-40dB`〜`-55dB` に調整。`d=2` は2秒以上の無音を検出する閾値。

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

## QA: /video-frame-reader で出力を検証

クリップ抽出後、品質を確認します。

入力内容:
```text
/video-frame-reader

抽出したクリップ動画のキーフレームを確認してください。

■ 対象: output/clips/ 内の生成されたMP4ファイル
■ 確認項目:
- クリップの開始・終了が自然か（発話の途中で切れていないか）
- 字幕とシーン内容が一致しているか
- 画質が十分か
```

---

## 次のステップ

Lesson 15-4 では、抽出したクリップを Remotion でSNS用マーケティング素材に変換する方法を学びます。
