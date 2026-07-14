---
name: youtube-uploader
description: "YouTube Data API v3 を使用した動画アップロードスキル。 Shorts自動検出、UTMリンク自動挿入、予約投稿に対応。 「YouTube投稿」「動画アップロード」「Shorts投稿」等で発動。"
status: draft
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

## 実装状況

> **Draft:** アップロード用スクリプトは未収録。実装が追加されるまで実行コマンドは提供しない。

## Planned Features

- **Shorts自動検出**: 縦型(h>w) かつ60秒以下 → 自動でShorts扱い
- **UTMリンク自動挿入**: 説明文にai-agent.campリンクがなければ自動追加
- **Resumable Upload**: 10MBチャンクで安定アップロード
- **ログ保存**: `output/gtm/youtube/upload_YYYYMMDD_HHMMSS.json`

## Dependencies

- `google-api-python-client`, `google-auth` (アップロード時)
- `ffprobe` (Shorts検出時、オプション)
