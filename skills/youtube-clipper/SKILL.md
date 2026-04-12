---
name: youtube-clipper
description: |
  YouTube/マルチプラットフォーム動画からAIでハイライトを抽出し、
  バイリンガル字幕付きクリップを自動生成するスキル。
  「動画からクリップを切り出して」「ハイライトを抽出」「字幕付きクリップ」等で発動。
triggers:
  - 動画からクリップを切り出して
  - ハイライトを抽出
  - 字幕付きクリップを作成
  - YouTubeからクリップ
  - 動画の見どころを切り抜き
  - youtube-clipper
  - clip highlight
---

# /youtube-clipper - 動画ハイライト抽出 & クリップ生成

## エントリーポイント

```bash
python skills/youtube-clipper/scripts/main.py --url "https://..."
```

## 概要

YouTube/Vimeo/X等の動画から、AIで意味的にハイライトを分析し、
バイリンガル字幕付きのクリップを自動生成します。

## クイックスタート

```bash
# YouTube動画からクリップ抽出
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://www.youtube.com/watch?v=xxxxx"

# ローカル動画にも対応
python skills/youtube-clipper/scripts/clipper.py \
  --file /path/to/local.mp4

# 自動選択モード（スコア0.8以上のチャプターを自動抽出）
python skills/youtube-clipper/scripts/clipper.py \
  --url "https://..." --auto-select "score>0.8"
```

## ワークフロー

```text
入力（URL or ローカルファイル）
  ↓
Step 1: 動画DL + 字幕取得（字幕なし → Gemini音声認識）
  ↓
Step 2: AIチャプター分析（セマンティック分割 + 要約 + スコア）
  ↓
Step 3: ユーザーがハイライト選択（番号/自然言語/スコアフィルタ）
  ↓
Step 4: クリップ抽出 + 字幕翻訳 + 焼き込み
  ↓
出力: clips/ + chapters.json + SNSサマリー
```

## パラメータ

| パラメータ | デフォルト | 説明 |
|-----------|----------|------|
| `--url` | - | YouTube/Vimeo/X等のURL |
| `--file` | - | ローカル動画ファイル |
| `--output` | `output/clips/` | 出力ディレクトリ |
| `--resolution` | `1080` | 動画品質（720/1080/best） |
| `--target-lang` | `ja` | 翻訳先言語 |
| `--burn-subtitles` | false | 字幕焼き込み |
| `--auto-select` | - | 自動選択条件（`score>0.8`, `all`） |
| `--chapters-only` | false | チャプター分析のみ（クリップ抽出しない） |

## 出力構造

```text
output/clips/YYYYMMDD_HHMMSS_{video_id}/
├── metadata.json
├── chapters.json
├── subtitles/
│   ├── original.srt
│   └── translated_ja.srt
├── clips/
│   ├── clip_01/
│   │   ├── clip_01.mp4
│   │   ├── clip_01_subtitled.mp4
│   │   ├── original.srt
│   │   ├── translated_ja.srt
│   │   ├── bilingual.srt
│   │   └── summary.json
│   └── ...
└── remotion_input.json
```

## 対応プラットフォーム

YouTube, Vimeo, X/Twitter, ニコニコ動画, Dailymotion等（yt-dlp対応範囲）

## 字幕なし動画

字幕が利用できない場合、FFmpegで音声を抽出し、
Gemini 3.0 Flash Previewで文字起こし + タイムスタンプ生成を行います。

## コスト目安

| 処理 | コスト |
|------|--------|
| 動画DL | $0 |
| Gemini文字起こし（10分動画） | ~$0.02 |
| チャプター分析 | ~$0.01 |
| 字幕翻訳 | ~$0.005 |
| **合計** | **~$0.035/動画** |

## トラブルシューティング

### YouTubeダウンロードが失敗する

ヘッドレスサーバーからはYouTubeのbot検出で弾かれることがあります。
cookieファイルを設定してください:

```bash
# 方法1: cookieファイルを指定
export YTDLP_COOKIES=/path/to/cookies.txt    # Mac/Linux
# Windows (cmd): set YTDLP_COOKIES=C:\path\to\cookies.txt
# Windows (PowerShell): $env:YTDLP_COOKIES = "C:\path\to\cookies.txt"

# 方法2: ブラウザからcookieを取得（ローカルPC向け）
export YTDLP_COOKIES_FROM_BROWSER=chrome    # Mac/Linux
# Windows (cmd): set YTDLP_COOKIES_FROM_BROWSER=chrome
# Windows (PowerShell): $env:YTDLP_COOKIES_FROM_BROWSER = "chrome"
```

cookieファイルの取得方法:
1. ブラウザ拡張「Get cookies.txt LOCALLY」等でYouTubeのcookieをエクスポート
2. Netscape形式のcookies.txtをサーバーにアップロード
3. 環境変数 `YTDLP_COOKIES` にパスを指定

### yt-dlpが見つからない

```bash
uv pip install yt-dlp
```

### FFmpegが見つからない

```bash
sudo apt-get install -y ffmpeg    # Ubuntu/Debian
# macOS: brew install ffmpeg
# Windows: winget install ffmpeg
```

### deno（JSランタイム）が必要と言われる

yt-dlpのYouTube抽出にdeno JSランタイムが必要な場合があります:

```bash
curl -fsSL https://deno.land/install.sh | sh    # Mac/Linux
export PATH="$HOME/.deno/bin:$PATH"    # Mac/Linux
# Windows (PowerShell): irm https://deno.land/install.ps1 | iex
#                       （PATHは自動で設定されます）
```
