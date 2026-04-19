---
name: youtube-uploader
description: "YouTube Data API v3 を使用した動画アップロードスキル。 Shorts自動検出、UTMリンク自動挿入、予約投稿に対応。 「YouTube投稿」「動画アップロード」「Shorts投稿」等で発動。"
triggers:
  - YouTubeに投稿
  - 動画をアップロード
  - Shorts投稿
  - YouTube動画を公開
  - 予約投稿を設定
  - youtube-uploader
  - YouTube upload
---

# YouTube Uploader Skill

YouTube Data API v3 を使用した動画アップロード。Shorts自動検出、UTMリンク自動挿入対応。

## Trigger Words
- YouTube, YouTube投稿, 動画アップロード, Shorts投稿, YouTube Shorts

## Usage

```bash
# 基本アップロード（dry-run）
python scripts/gtm/upload_youtube.py --file video.mp4 --title "タイトル" --description "説明" --dry-run

# Shorts投稿
python scripts/gtm/upload_youtube.py --file short.mp4 --title "AI活用Tips" --shorts --dry-run

# 予約投稿
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --schedule "2026-03-20T09:00:00Z" --dry-run

# タグ付き
python scripts/gtm/upload_youtube.py --file video.mp4 --title "..." --tags "AI,エージェント,ノーコード" --dry-run
```

## Arguments

| 引数 | 必須 | デフォルト | 説明 |
|------|------|-----------|------|
| `--file` | Yes | - | 動画ファイルパス |
| `--title` | Yes | - | 動画タイトル |
| `--description` | No | - | 説明文（UTMリンク自動追加） |
| `--tags` | No | - | カンマ区切りタグ |
| `--category` | No | 27 | カテゴリID（27=教育） |
| `--privacy` | No | private | private/unlisted/public |
| `--shorts` | No | false | Shorts強制モード |
| `--language` | No | ja | 動画言語 |
| `--schedule` | No | - | 予約投稿（ISO 8601） |
| `--credentials` | No | env | YouTube認証JSONパス |
| `--dry-run` | No | false | アップロードしない |

## Features

- **Shorts自動検出**: 縦型(h>w) かつ60秒以下 → 自動でShorts扱い
- **UTMリンク自動挿入**: 説明文にai-agent.campリンクがなければ自動追加
- **Resumable Upload**: 10MBチャンクで安定アップロード
- **ログ保存**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencies

- `google-api-python-client`, `google-auth` (アップロード時)
- `ffprobe` (Shorts検出時、オプション)
