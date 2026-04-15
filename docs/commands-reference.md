# コマンドリファレンス完全ガイド

**対応コマンド数**: 134個（レッスンコマンド107個 + cursor-workshop 4個 + ユーティリティコマンド27個）

最終更新: 2026年3月20日

---

## 目次

1. [クイックスタート](#クイックスタート)
2. [レッスンコマンド (107個 + cursor-workshop 4個)](#レッスンコマンド-107個--cursor-workshop-4個)
3. [ユーティリティコマンド (27個)](#ユーティリティコマンド-27個)
4. [コマンド実行方法](#コマンド実行方法)
5. [トラブルシューティング](#トラブルシューティング)

---

## クイックスタート

### 初めての学習開始

このドキュメントの主対象は **Cursor の slash command** です。  
Codex と Claude Code では同じ lesson id を使いますが、入口が異なります。

| ツール | 学習開始の入口 |
| --- | --- |
| Cursor | `/check-setup` → `/start-*` |
| Codex | `aiagent-check-setup` → `aiagent-lesson-runner start-*` |
| Claude Code | `CLAUDE.md` を起点に lesson 導線へ進む |

### よく使うコマンド TOP 10

| # | コマンド | 用途 | 難易度 |
|---|---------|------|--------|
| 1 | `/check-setup` | Cursor での環境セットアップ確認 | 初心者 |
| 2 | `/start-0-1` | 最初の lesson 開始 | 初心者 |
| 3 | `/create-banner` | SNSバナー生成 | 初心者 |
| 4 | `/generate-diagram` | 図表・インフォグラフィック生成 | 初心者 |
| 5 | `/nanobanana` | 画像生成・編集 | 初心者 |
| 6 | `/screenshot-analyzer` | スクリーンショット解析 | 初級 |
| 7 | `/bigquery-auth` | BigQuery認証 | 中級 |
| 8 | `/generate-slide` | スライド生成 | 初級 |
| 9 | `/pptx-ops` | PowerPoint操作 | 中級 |
| 10 | `/overview` | プロジェクト構造可視化 | 中級 |

---

## レッスンコマンド (107個 + cursor-workshop 4個)

基礎から応用まで段階的に学習できるコマンド群です。**Module 0 ～ 18** に分類されています（Module 17 は欠番）。

### Module 0: セットアップ (8個)

初期環境構築用コマンド（`start-0-1` ～ `start-0-8`）

#### `/start-0-1` - 最初の lesson 開始
- **難易度**: 初心者
- **実行時間**: 1-2分
- **機能**: lesson 0-1 の開始。詳細な setup 確認は tool ごとの入口から行う
- **使用例**: `/start-0-1`

#### `/start-0-2` - 拡張機能インストール
- **難易度**: 初心者
- **実行時間**: 5-10分
- **機能**: Playwright, Python パッケージのインストール

#### `/start-0-3` - Gemini API設定
- **難易度**: 初心者
- **前提条件**: Google アカウント
- **必要情報**: GEMINI_API_KEY

#### `/start-0-4` - Slack API設定
- **難易度**: 初心者
- **前提条件**: Slack ワークスペース管理権限
- **設定項目**: Bot Token, Channel IDs

#### `/start-0-5` - セキュリティ設定確認
- **難易度**: 初心者
- **実行時間**: 2-3分
- **確認項目**: API キー安全性, 環境変数, .gitignore

#### `/start-0-6` - Codex CLI セットアップ
#### `/start-0-7` - Claude Code セットアップ
#### `/start-0-8` - ツール選択ガイド（Cursor / Claude Code / Codex）

---

### Module 1: バナー・画像生成 (3個)

`start-1-1` ～ `start-1-3`

#### `/start-1-1` - バナー生成入門
- **学習内容**: バナーサイズの種類, プラットフォーム別の違い, デザイン原則

#### `/start-1-2` - 応用バナー（Instagram, Facebook）
- **学習内容**: プラットフォーム別最適化, ストーリーズ vs フィード

#### `/start-1-3` - nanobanana画像編集
- **学習内容**: 画像フォーマット変換, サイズ調整, エフェクト

---

### Module 2: 図表・フロー作成 (3個)

`start-2-1` ～ `start-2-3`

#### `/start-2-1` - フロー図生成
#### `/start-2-2` - インフォグラフィック作成
#### `/start-2-3` - プレゼン資料向け図表作成

---

### Module 3: チュートリアル作成 (6個)

`start-3-1` ～ `start-3-6`

| コマンド | 説明 |
|---------|------|
| `/start-3-1` | スクリーンショット分析基礎 |
| `/start-3-2` | エラー診断の応用 |
| `/start-3-3` | チュートリアル自動生成 |
| `/start-3-4` | スクリーンショットに注釈追加 |
| `/start-3-5` | 複数スクリーンショットの一括分析 |
| `/start-3-6` | 操作マニュアル生成（総合演習） |

---

### Module 4: データ分析 (4個)

`start-4-1` ～ `start-4-4`

| コマンド | 説明 |
|---------|------|
| `/start-4-1` | BigQuery接続と認証設定 |
| `/start-4-2` | EDA（探索的データ分析）の実行 |
| `/start-4-3` | Marimoノートブックで対話型分析 |
| `/start-4-4` | データ可視化とダッシュボード作成 |

---

### Module 5: PPTX解析・編集 (2個)

`start-5-1` ～ `start-5-2`

| コマンド | 説明 |
|---------|------|
| `/start-5-1` | PPTX解析（構造分析、テンプレート抽出） |
| `/start-5-2` | PPTX編集と自動生成 |

---

### Module 6: Slack検索・分析 (2個)

`start-6-1` ～ `start-6-2`

| コマンド | 説明 |
|---------|------|
| `/start-6-1` | Slackメッセージのキーワード拡張検索 |
| `/start-6-2` | SlackメッセージからTODOとタスクを抽出 |

---

### Module 7: 動画生成 (8個)

`start-7-1` ～ `start-7-8`

| コマンド | 説明 |
|---------|------|
| `/start-7-1` | 動画フレーム分析 |
| `/start-7-2` | 動画AIエンジンの全体像（fal.ai） |
| `/start-7-3` | プロダクト紹介動画（グリーンスクリーン + スクショ合成） |
| `/start-7-4` | 絵コンテからアニメ動画生成（Kling/Veo3） |
| `/start-7-5` | スライド解説動画（HTML解析 + TTS） |
| `/start-7-6` | ミュージックビデオ作成（Suno + ビート同期） |
| `/start-7-7` | YouTube Clipper で動画ハイライト抽出 |
| `/start-7-8` | Clipper × Remotion でマーケ素材を自動生成 |

---

### Module 8: GAS自動化 (3個)

`start-8-1` ～ `start-8-3`

| コマンド | 説明 |
|---------|------|
| `/start-8-1` | Clasp基本・GASプロジェクト管理 |
| `/start-8-2` | Google Calendar API連携・イベント自動化 |
| `/start-8-3` | Google Sheets自動化・データ処理レポート |

---

### Module 9: GitHub Actions (2個)

`start-9-1` ～ `start-9-2`

| コマンド | 説明 |
|---------|------|
| `/start-9-1` | GitHub Actions Workflow基本・自動化 |
| `/start-9-2` | GitHub Actions Secrets設定・Google連携 |

---

### Module 10: Notion連携 (2個)

`start-10-1` ～ `start-10-2`

| コマンド | 説明 |
|---------|------|
| `/start-10-1` | Notion MCP接続とセットアップ |
| `/start-10-2` | Notionデータベース操作 |

---

### Module 11: エージェント開発 (13個)

`start-11-1` ～ `start-11-13`

| コマンド | 説明 |
|---------|------|
| `/start-11-1` | カスタムCommand作成基本 |
| `/start-11-2` | Skill作成基本（共通 skills/ ディレクトリ） |
| `/start-11-3` | Rules設定（Cursor Rules）とAI行動制御 |
| `/start-11-4` | SubAgent統合 - 複数エージェントの連携 |
| `/start-11-5` | 総合演習（全機能統合） |
| `/start-11-6` | スキル設計の基礎（Anthropicベストプラクティス） |
| `/start-11-7` | SKILL.md の実装（議事録スキル開発） |
| `/start-11-8` | テストとイテレーション（スキル品質改善） |
| `/start-11-9` | 5つの設計パターン（スキル設計の応用） |
| `/start-11-10` | 既存Skill/Commandの構造理解と分析 |
| `/start-11-11` | 自分のワークフロー用Command作成 |
| `/start-11-12` | SKILL.md駆動のスキル開発 |
| `/start-11-13` | テスト・デバッグ・イテレーション |

---

### Module 12: マーケティング (4個)

`start-12-1` ～ `start-12-4`

| コマンド | 説明 |
|---------|------|
| `/start-12-1` | X投稿 & バナー作成 |
| `/start-12-2` | SEO調査 & キーワード戦略 |
| `/start-12-3` | コピーライティング |
| `/start-12-4` | Pencil MCPでデザインモックアップ |

---

### Module 13: LP/HP制作 (5個)

`start-13-1` ～ `start-13-5`

| コマンド | 説明 |
|---------|------|
| `/start-13-1` | LP制作 - 訴求の整理 |
| `/start-13-2` | LP制作 - ワイヤーフレーム作成 |
| `/start-13-3` | LP制作 - Pencilデザインファイル作成 |
| `/start-13-4` | LP制作 - 実際に動くLP作成 |
| `/start-13-5` | LP制作 - Vercelデプロイ |

---

### Module 14: PM & 要件定義 (20個)

`start-14-1` ～ `start-14-20`

| コマンド | 説明 |
|---------|------|
| `/start-14-1` | 顧客インタビュー & ニーズ収集 |
| `/start-14-2` | 要求資料の作成 |
| `/start-14-3` | PRD作成（Working Backwards方式） |
| `/start-14-4` | 3種レビュー（Devil's Advocate / セキュリティ等） |
| `/start-14-5` | 要件定義書の作成（IPA準拠） |
| `/start-14-6` | ユースケース記述 & シーケンス図 |
| `/start-14-7` | 画面遷移図 & ワイヤーフレーム |
| `/start-14-8` | DB設計（ER図 & エンティティ仕様書） |
| `/start-14-9` | システム構成図 & API設計 |
| `/start-14-10` | WBS & ガントチャート |
| `/start-14-11` | Notion連携（要件トラッカーDB） |
| `/start-14-12` | UIデザイン（Pencil MCP） |
| `/start-14-13` | HTML + Tailwind CSS プロトタイプ実装 |
| `/start-14-14` | Playwright E2Eテスト |
| `/start-14-15` | テスト計画書 & テストケース生成 |
| `/start-14-16` | 単体テスト実施（pytest） |
| `/start-14-17` | 結合テスト実施 |
| `/start-14-18` | 会議体設計 & 議事録分析 |
| `/start-14-19` | marimo ダッシュボード |
| `/start-14-20` | 総合演習（カプストーン） |

---

### Module 15: メール自動化 (8個)

`start-15-1` ～ `start-15-8`

| コマンド | 説明 |
|---------|------|
| `/start-15-1` | Gmail セットアップ - gogcli 認証とメール同期 |
| `/start-15-2` | 受信メール分析 & タスク抽出 |
| `/start-15-3` | gogcli でメール送信 - 新規・返信・添付 |
| `/start-15-4` | メールシーケンス設計 - ドリップキャンペーン |
| `/start-15-5` | メール自動化ワークフロー - GitHub Actions & 総合演習 |
| `/start-15-6` | Resend 登録 & ドメイン設定 - Vercel DNS 自動設定 |
| `/start-15-7` | APIキー作成 & Resend CLI で初回メール送信 |
| `/start-15-8` | Resend Sequence & CLI でドリップキャンペーン自動化 |

---

### Module 16: 記事作成 (7個)

`start-16-1` ～ `start-16-7`

| コマンド | 説明 |
|---------|------|
| `/start-16-1` | 記事企画 - テーマ決定・アウトライン生成 |
| `/start-16-2` | 文体学習 - スタイルプロファイル作成 |
| `/start-16-3` | 記事執筆 - スタイル適用ドラフト作成 |
| `/start-16-4` | 挿絵計画と生成 - nanobanana + PlantUML |
| `/start-16-5` | 校閲 - 校閲エージェントによるレビュー |
| `/start-16-6` | ファクトチェック - 事実検証エージェント |
| `/start-16-7` | 並列実行と仕上げ - 複数記事の同時処理 |

---

### Module 18: AI秘書 Google Workspace (7個)

`start-18-1` ～ `start-18-7`

| コマンド | 説明 |
|---------|------|
| `/start-18-1` | gogcli認証セットアップ |
| `/start-18-2` | Gmail検索・閲覧 |
| `/start-18-3` | Google Calendar操作 |
| `/start-18-4` | Google Calendar 予定登録・管理 |
| `/start-18-5` | Google Drive操作 |
| `/start-18-6` | Google Sheets操作 |
| `/start-18-7` | AI秘書ワークフロー統合 |

---

### その他のレッスンコマンド

#### セキュリティ・確認系
- `/check-setup` - Cursor でのセットアップ状態確認
- `/check-security` - セキュリティ設定確認
- `/exercise-review` - 応用演習レビュー

## 他ツールでの読み替え

- `Cursor` ではこのドキュメントの slash command をそのまま使う
- `Codex` では `/check-setup` を `aiagent-check-setup`、`/start-0-1` を `aiagent-lesson-runner start-0-1` と読み替える
- `Claude Code` では `CLAUDE.md` と Claude 側の lesson 導線を入口にし、lesson id 自体は同じ `start-*` を使う

## 他ツールでの読み替え

- `Cursor` ではこのドキュメントの slash command をそのまま使う
- `Codex` では `/check-setup` を `aiagent-check-setup`、`/start-0-1` を `aiagent-lesson-runner start-0-1` と読み替える
- `Claude Code` では `CLAUDE.md` と Claude 側の lesson 導線を入口にし、lesson id 自体は同じ `start-*` を使う

---

## ユーティリティコマンド (27個)

日常的によく使うツール系コマンド

### 画像・バナー生成 (4個)

#### `/create-banner` - SNSバナー/クリエイティブ生成

**説明**: 各種SNS・広告プラットフォーム向けバナー生成

**対応プラットフォーム**:
- X (Twitter): 1200x675, 800x418
- Facebook: 1200x630, 1080x1920
- Instagram: 1080x1080, 1080x1920
- PRタイムズ: 1200x630
- YouTube: 1280x720
- LINE: 1040x1040
- Web広告: 1200x628, 300x600

**パラメータ**:
```
--platform       対象プラットフォーム（必須）
--message        メインメッセージ（必須）
--sub-copy       サブコピー（オプション）
--cta            Call to Action（オプション）
--tone           professional, casual, pop, elegant, urgent, minimal, tech, natural
--color-scheme   warm, cool, mono, pastel, vivid, dark, HEXコード
--font-style     gothic, mincho, handwritten, bold, script, geometric
--brand-name     ブランド名（オプション）
--with-copy      投稿用コピーも生成するか
--variants       生成バリエーション数
--session        セッション名
--output         出力先パス
```

**使用例**:
```bash
/create-banner --platform x_post --message "新製品発表" --tone professional --with-copy

/create-banner --platform instagram_feed --message "夏セール" --tone pop --color-scheme vivid

/create-banner --platform youtube --message "チュートリアル"
```

**出力**: `docs/generated/banners/{日付}_{セッション}/`

---

#### `/nanobanana` - AI画像生成・編集

**説明**: Gemini API を使用した画像生成・編集

**パラメータ**:
```
--prompt         生成・編集内容（必須）
--input          編集対象の画像ファイル（オプション）
--style          realistic, anime, illustration, art, photo, sketch
--size           256x256, 512x512, 1024x1024, 1024x768, 768x1024
--quality        draft, normal, high
```

**使用例**:
```bash
/nanobanana --prompt "青い空を背景にした商品写真" --style realistic

/nanobanana --input photo.jpg --prompt "明度を上げて、暖色系に変更"
```

---

#### `/generate-diagram` - 図表・インフォグラフィック生成

**説明**: テキストトピックから図表生成

**対応図表種類**: infographic, flow, comparison, hierarchy, timeline, network

**使用例**:
```bash
/generate-diagram --topic "ユーザー登録フロー" --type flow --style professional

/generate-diagram --topic "売上成長推移" --type timeline
```

---

#### `/annotate-screenshot` - スクショに注釈追加

**説明**: スクリーンショットに手書き風の注釈を追加

**機能**: 赤枠, 矢印, 吹き出し, テキスト注釈, ハイライト

---

### スクリーンショット分析 (3個)

#### `/screenshot-analyzer` - スクリーンショット解析統合ツール

**説明**: スクリーンショット分析・エラー検出・マニュアル生成

**機能**: エラー画面診断, UIコンポーネント認識, OCR, チュートリアル生成

---

#### `/capture-tutorial` - スクショからチュートリアル生成

**説明**: 複数スクショから操作チュートリアル生成

---

#### `/video-frame-reader` - 動画キーフレーム抽出

**説明**: 動画からキーフレーム抽出・分析

---

### データ処理・ドキュメント (7個)

#### `/bigquery-auth` - BigQuery認証設定

**説明**: GCP プロジェクト単位の BigQuery 認証設定

#### `/pptx-ops` - PowerPoint 操作

**説明**: PowerPoint ファイルの操作・編集

#### `/pptx-template` - PPTX テンプレート操作

**説明**: PPTX テンプレート管理・カスタマイズ

#### `/excel-ops` - Excel 操作

**説明**: Excel ファイルの読み込み・編集・出力

#### `/pdf-editor` - PDF ページエディタ

**説明**: PDF ファイルの結合・分割・ページ操作

#### `/fetch-slides` - Google Slides 取得

**説明**: Google Slides から情報取得・エクスポート

#### `/notion-fetch` - Notion 連携

**説明**: Notion データベース・ページ取得

---

### API・Google 関連 (6個)

#### `/gmail-account-setup` - Gmail アカウント設定

**説明**: Gmail API 認証設定

#### `/google-account-setup` - Google アカウント設定

**説明**: Google Calendar/Drive API 認証

#### `/setup-google-api` - Google API 設定ガイド

**説明**: MCP 連携用 Google API セットアップ

#### `/api-setup-wizard` - API セットアップウィザード

**説明**: 各種 API の統合セットアップガイド

#### `/gmail-pending-replies` - Gmail 未返信抽出

**説明**: 未返信メール一覧を自動抽出

---

### 補助コマンド (5個)

#### `/overview` - プロジェクト構造可視化

**説明**: serena MCP を活用してプロジェクト構造を可視化

**機能**:
- ファイル・関数一覧表示
- PlantUML 形式で構造図生成
- 不足機能の特定
- HTML レポート出力

**パラメータ**:
```
--directory      分析対象ディレクトリ
--format         plantuml, wbs, all
--output         出力パス
```

**使用例**:
```bash
/overview

/overview --directory src/ --format plantuml

/overview --directory scripts/ --output docs/overview.html
```

---

#### `/guide` - 次のアクション提示

**説明**: 現在の進捗に基づく次のアクション提示

#### `/tutor` - 学習コンテンツ生成

**説明**: 指定トピックの学習教材自動生成

#### `/generate-slide` - スライド生成

**説明**: テーマから Google Slides を自動生成

#### `/notebooklm` - NotebookLM

**説明**: NotebookLM API を活用した対話型分析

---

## コマンド実行方法

### 基本的な実行方法

#### 方法 1: スラッシュコマンド（推奨）

```bash
/コマンド名 [オプション]
```

#### 方法 2: Python スクリプト直接実行

```bash
uv run python tools/コマンド名.py [オプション]
```

#### 方法 3: Bash スクリプト経由

```bash
bash .claude/scripts/run_command.sh コマンド名 [オプション]
```

### パラメータの指定方法

#### 必須パラメータ

```bash
/create-banner --platform x_post --message "テキスト"
```

#### オプショナルパラメータ

```bash
/create-banner --platform x_post --message "テキスト" --tone professional --with-copy
```

#### JSON 形式

```bash
/command --config '{"key1": "value1", "key2": "value2"}'
```

### 出力確認方法

#### ログ確認

```bash
tail -f logs/execution.log
cat logs/execution.log | grep "Completed"
```

#### 出力ファイル確認

```bash
ls -lt docs/generated/
ls -lht docs/generated/ | head -1
```

---

## トラブルシューティング

### よくあるエラー

#### "コマンドが見つかりません"

```
Error: Command 'コマンド名' not found
```

**対処方法**:
```bash
# Cursor command 一覧確認
ls .cursor/commands/lesson/ | grep コマンド名 || true
ls .cursor/commands/utility/ | grep コマンド名 || true

# Codex は skills と lesson runner を使う
cat AGENTS.md
```

---

#### "API キーが設定されていません"

```
Error: GEMINI_API_KEY (or GOOGLE_API_KEY) not found
```

**対処方法**:
```bash
# 入力欄を .env.local に作成
uv run python tools/credential_manager.py prepare-dotenv GEMINI_API_KEY

# 保存後に Credential Store へ移行
uv run python tools/credential_manager.py import-dotenv GEMINI_API_KEY --delete

# 状態確認
uv run python tools/credential_manager.py status
```

---

#### "Python モジュールが見つかりません"

```
ModuleNotFoundError: No module named 'pillow'
```

**対処方法**:
```bash
uv add pillow requests beautifulsoup4 playwright
uv sync
playwright install chromium
```

---

#### "スクリプト実行権限なし"

```
Error: Permission denied
```

**対処方法**:
```bash
chmod +x tools/banner_creator.py
chmod +x .claude/scripts/*.sh
```

---

### パフォーマンス問題

#### コマンド実行が遅い

**原因と対処**:
1. API レート制限: 数分待機後に再実行
2. ネットワーク遅延: `ping google.com`
3. リソース不足: `top -l 1 | head -20`

---

#### メモリ不足エラー

```bash
killall python
killall node
/process-data --batch-size 10
```

---

### API・認証エラー

#### "認証に失敗しました"

```bash
gcloud auth application-default print-access-token
```

---

#### "レート制限エラー"

```bash
/command --retry-delay 5 --max-retries 3
/command --queue --batch 10
```

---

### デバッグ方法

#### 詳細ログを出力

```bash
/create-banner --debug
/command --log-level DEBUG
/command --log-file debug.log
```

#### 実行内容の確認

```bash
/command --dry-run
/command --confirm
```

---

## FAQ

### Q1: 複数のコマンドを連続実行したい

```text
Cursor:
/check-setup -> /start-0-3 -> /create-banner

Codex:
aiagent-check-setup -> aiagent-lesson-runner start-0-3 -> 対応するローカルツール実行
```

---

### Q2: コマンドの出力を別ツールに渡したい

```bash
/command --output-format json > output.json
cat output.json | jq '.results | length'
```

---

### Q3: 環境ごとに異なる設定を使いたい

```text
秘密情報は .env.local に保存し、必要なら Credential Store に移す。
環境差分を切り替える前に、現在の tool の安全ガイドを確認する。
```

---

### Q4: バッチ処理したい

```bash
# CSVから一括処理
while IFS=, read platform message; do
  /create-banner --platform "$platform" --message "$message"
done < banners.csv
```

---

## 参考リンク

- [Claude Code 公式ドキュメント](https://claude.com/claude-code)
- [ai-agent-camp GitHub](https://github.com/minicoohei/ai-agent-camp)
- [Codex Guide](./codex-guide.md)
- [Skills リファレンス](./skills-reference.md)
- [トラブルシューティング](./troubleshoot.md)

---

**ドキュメント更新履歴**

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2026-03-20 | 2.0.0 | Module番号リネーム反映。107レッスン + cursor-workshop 4個。Module 12-18 追加 |
| 2026-03-20 | 1.1.0 | 3ツール共通の入口説明に更新 |
| 2026-02-02 | 1.0.0 | 初版作成（83コマンド網羅） |
