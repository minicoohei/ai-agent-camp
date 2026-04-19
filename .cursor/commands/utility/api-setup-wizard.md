---
description: "API設定ガイド統合（各種サービスのセットアップ一覧）"
aliases: ["api-setup", "setup-api"]
category: "setup"
duration: "約5分"
prerequisites: ["Cursor をインストール済み", "ai-agent-camp フォルダを開いている"]
level: "beginner"
tags: ["setup", "api", "guide"]
---

# API Setup Wizard - 設定ガイド統合

各種API（Google, Notion, Slack, Fal.AI, Gemini 等）の設定を一元管理します。

## かんたんセットアップ（推奨）

以下のコマンドをCursorのチャット欄に入力するだけで、AIが対話形式でセットアップを行います。

| コマンド | 対象サービス | 説明 |
|----------|-------------|------|
| `/setup-gemini` | Gemini API | 画像生成・テキスト生成に必要（必須） |
| `/setup-github` | GitHub | リポジトリ操作・Actions に必要（推奨） |
| `/setup-slack` | Slack API | Slack 検索・タスク管理に必要 |
| `/check-setup` | 全体チェック | 全APIの設定状況を一括確認 |

## 対応サービス

| サービス | 説明 | 設定方法 |
|----------|------|---------|
| `gemini` | Google Gemini 生成AI | `/setup-gemini` を実行 |
| `google` | Gmail, Calendar, Drive, Sheets, Slides | `/setup-google-api` を実行 |
| `notion` | Notion ページ・データベース | `.env` に `NOTION_API_KEY` を直接記入 |
| `slack` | Slack ワークスペース | `/setup-slack` を実行 |
| `fal` | Fal.AI 画像・動画生成 | `.env` に `FAL_KEY` を直接記入 |
| `heygen` | HeyGen AIアバター動画 | `.env` に `HEYGEN_API_KEY` を直接記入 |
| `elevenlabs` | ElevenLabs TTS（音声合成） | `.env` に `ELEVENLABS_API_KEY` を直接記入 |
| `typefully` | Typefully X（旧Twitter）投稿管理 | `.env` に `TYPEFULLY_API_KEY` を直接記入 |

## 設定状況の確認

全APIの設定状況を確認するには、Cursorのチャット欄に以下を入力してください:

```text
/check-setup
```

AIが全項目を自動チェックし、未設定のAPIと設定済みのAPIをレポート表示します。

## 関連コマンド

- `/setup-gemini` - Gemini API セットアップ（AIがブラウザを開いてガイド）
- `/setup-slack` - Slack API セットアップ（AIがブラウザを開いてガイド）
- `/setup-github` - GitHub 認証セットアップ
- `/check-setup` - 環境の総合チェック
- `/setup-google-api` - Google API専用セットアップ（OAuth認証フロー）
- `/gmail-account-setup` - Gmail複数アカウント設定
