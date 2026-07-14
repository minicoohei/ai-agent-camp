# コマンドリファレンス完全ガイド

**対応コマンド数**: 222個（レッスン 167個 + ユーティリティ 33個 + トップレベル 22個）

最終更新: 2026-07-14

---

## 目次

1. [クイックスタート](#クイックスタート)
2. [コマンド一覧](#コマンド一覧)
3. [コマンド実行方法](#コマンド実行方法)
4. [トラブルシューティング](#トラブルシューティング)
5. [FAQ](#faq)
6. [参考リンク](#参考リンク)

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

<!-- AUTO-GENERATED:commands START -->
## コマンド一覧

`.en.md` / `.es.md` は同じ slash command の翻訳版として重複計上しません。

### レッスンコマンド（167個）

#### Module 0（9個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-content` | 教材コンテンツの初回セットアップ | [`.cursor/commands/lesson/setup-content.md`](../.cursor/commands/lesson/setup-content.md) |
| `/start-0-1` | 環境セットアップ確認 | [`.cursor/commands/lesson/start-0-1.md`](../.cursor/commands/lesson/start-0-1.md) |
| `/start-0-2` | 拡張機能インストール | [`.cursor/commands/lesson/start-0-2.md`](../.cursor/commands/lesson/start-0-2.md) |
| `/start-0-3` | Gemini API設定 | [`.cursor/commands/lesson/start-0-3.md`](../.cursor/commands/lesson/start-0-3.md) |
| `/start-0-4` | Slack API設定 | [`.cursor/commands/lesson/start-0-4.md`](../.cursor/commands/lesson/start-0-4.md) |
| `/start-0-5` | セキュリティ設定確認 | [`.cursor/commands/lesson/start-0-5.md`](../.cursor/commands/lesson/start-0-5.md) |
| `/start-0-6` | Codex CLI セットアップ | [`.cursor/commands/lesson/start-0-6.md`](../.cursor/commands/lesson/start-0-6.md) |
| `/start-0-7` | Claude Code セットアップ | [`.cursor/commands/lesson/start-0-7.md`](../.cursor/commands/lesson/start-0-7.md) |
| `/start-0-8` | ツール選択ガイド | [`.cursor/commands/lesson/start-0-8.md`](../.cursor/commands/lesson/start-0-8.md) |

#### Module 1（3個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-1-1` | バナー生成入門 | [`.cursor/commands/lesson/start-1-1.md`](../.cursor/commands/lesson/start-1-1.md) |
| `/start-1-2` | 応用バナー（Instagram, Facebook） | [`.cursor/commands/lesson/start-1-2.md`](../.cursor/commands/lesson/start-1-2.md) |
| `/start-1-3` | nanobanana画像編集 | [`.cursor/commands/lesson/start-1-3.md`](../.cursor/commands/lesson/start-1-3.md) |

#### Module 2（3個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-2-1` | フロー図生成 | [`.cursor/commands/lesson/start-2-1.md`](../.cursor/commands/lesson/start-2-1.md) |
| `/start-2-2` | インフォグラフィック作成 | [`.cursor/commands/lesson/start-2-2.md`](../.cursor/commands/lesson/start-2-2.md) |
| `/start-2-3` | プレゼン資料向け図表作成 | [`.cursor/commands/lesson/start-2-3.md`](../.cursor/commands/lesson/start-2-3.md) |

#### Module 3（6個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-3-1` | スクリーンショット分析基礎 | [`.cursor/commands/lesson/start-3-1.md`](../.cursor/commands/lesson/start-3-1.md) |
| `/start-3-2` | エラー診断の応用 | [`.cursor/commands/lesson/start-3-2.md`](../.cursor/commands/lesson/start-3-2.md) |
| `/start-3-3` | チュートリアル自動生成 | [`.cursor/commands/lesson/start-3-3.md`](../.cursor/commands/lesson/start-3-3.md) |
| `/start-3-4` | スクリーンショットに注釈追加 | [`.cursor/commands/lesson/start-3-4.md`](../.cursor/commands/lesson/start-3-4.md) |
| `/start-3-5` | 複数スクリーンショットの一括分析 | [`.cursor/commands/lesson/start-3-5.md`](../.cursor/commands/lesson/start-3-5.md) |
| `/start-3-6` | Module 3 総合演習 | [`.cursor/commands/lesson/start-3-6.md`](../.cursor/commands/lesson/start-3-6.md) |

#### Module 4（7個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-4-1` | gogcli認証セットアップ | [`.cursor/commands/lesson/start-4-1.md`](../.cursor/commands/lesson/start-4-1.md) |
| `/start-4-2` | Gmail検索・閲覧 | [`.cursor/commands/lesson/start-4-2.md`](../.cursor/commands/lesson/start-4-2.md) |
| `/start-4-3` | Google Calendar操作 | [`.cursor/commands/lesson/start-4-3.md`](../.cursor/commands/lesson/start-4-3.md) |
| `/start-4-4` | Google Calendar 予定登録・管理 | [`.cursor/commands/lesson/start-4-4.md`](../.cursor/commands/lesson/start-4-4.md) |
| `/start-4-5` | Google Drive操作 | [`.cursor/commands/lesson/start-4-5.md`](../.cursor/commands/lesson/start-4-5.md) |
| `/start-4-6` | Google Sheets操作 | [`.cursor/commands/lesson/start-4-6.md`](../.cursor/commands/lesson/start-4-6.md) |
| `/start-4-7` | AI秘書ワークフロー統合 | [`.cursor/commands/lesson/start-4-7.md`](../.cursor/commands/lesson/start-4-7.md) |

#### Module 5（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-5-1` | PPTX解析 | [`.cursor/commands/lesson/start-5-1.md`](../.cursor/commands/lesson/start-5-1.md) |
| `/start-5-2` | PPTX編集と自動生成 | [`.cursor/commands/lesson/start-5-2.md`](../.cursor/commands/lesson/start-5-2.md) |

#### Module 6（9個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-6-1` | カスタムCommand作成基本 | [`.cursor/commands/lesson/start-6-1.md`](../.cursor/commands/lesson/start-6-1.md) |
| `/start-6-2` | Skill作成基本 | [`.cursor/commands/lesson/start-6-2.md`](../.cursor/commands/lesson/start-6-2.md) |
| `/start-6-3` | Cursor Rules設定 | [`.cursor/commands/lesson/start-6-3.md`](../.cursor/commands/lesson/start-6-3.md) |
| `/start-6-4` | SubAgent統合 | [`.cursor/commands/lesson/start-6-4.md`](../.cursor/commands/lesson/start-6-4.md) |
| `/start-6-5` | 総合演習 - AIエージェント開発統合 | [`.cursor/commands/lesson/start-6-5.md`](../.cursor/commands/lesson/start-6-5.md) |
| `/start-6-6` | スキル設計の基礎 | [`.cursor/commands/lesson/start-6-6.md`](../.cursor/commands/lesson/start-6-6.md) |
| `/start-6-7` | SKILL.md の実装 | [`.cursor/commands/lesson/start-6-7.md`](../.cursor/commands/lesson/start-6-7.md) |
| `/start-6-8` | テストとイテレーション | [`.cursor/commands/lesson/start-6-8.md`](../.cursor/commands/lesson/start-6-8.md) |
| `/start-6-9` | 5つの設計パターン | [`.cursor/commands/lesson/start-6-9.md`](../.cursor/commands/lesson/start-6-9.md) |

#### Module 7（8個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-7-1` | スキル設計の基礎 | [`.cursor/commands/lesson/start-7-1.md`](../.cursor/commands/lesson/start-7-1.md) |
| `/start-7-2` | SKILL.md の実装 | [`.cursor/commands/lesson/start-7-2.md`](../.cursor/commands/lesson/start-7-2.md) |
| `/start-7-3` | テストとイテレーション | [`.cursor/commands/lesson/start-7-3.md`](../.cursor/commands/lesson/start-7-3.md) |
| `/start-7-4` | 5つの設計パターン | [`.cursor/commands/lesson/start-7-4.md`](../.cursor/commands/lesson/start-7-4.md) |
| `/start-7-5` | 既存Skill/Commandの構造理解と分析 | [`.cursor/commands/lesson/start-7-5.md`](../.cursor/commands/lesson/start-7-5.md) |
| `/start-7-6` | 自分のワークフロー用Command作成 | [`.cursor/commands/lesson/start-7-6.md`](../.cursor/commands/lesson/start-7-6.md) |
| `/start-7-7` | SKILL.md駆動のスキル開発 | [`.cursor/commands/lesson/start-7-7.md`](../.cursor/commands/lesson/start-7-7.md) |
| `/start-7-8` | テスト・デバッグ・イテレーション | [`.cursor/commands/lesson/start-7-8.md`](../.cursor/commands/lesson/start-7-8.md) |

#### Module 8（4個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-8-1` | BigQuery接続と認証設定 | [`.cursor/commands/lesson/start-8-1.md`](../.cursor/commands/lesson/start-8-1.md) |
| `/start-8-2` | EDA（探索的データ分析）の実行 | [`.cursor/commands/lesson/start-8-2.md`](../.cursor/commands/lesson/start-8-2.md) |
| `/start-8-3` | Marimoノートブックで対話型分析 | [`.cursor/commands/lesson/start-8-3.md`](../.cursor/commands/lesson/start-8-3.md) |
| `/start-8-4` | データ可視化とダッシュボード作成 | [`.cursor/commands/lesson/start-8-4.md`](../.cursor/commands/lesson/start-8-4.md) |

#### Module 9（3個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-9-1` | User Access Token設定・チャネル取得 | [`.cursor/commands/lesson/start-9-1.md`](../.cursor/commands/lesson/start-9-1.md) |
| `/start-9-2` | メッセージ・スレッド取得 | [`.cursor/commands/lesson/start-9-2.md`](../.cursor/commands/lesson/start-9-2.md) |
| `/start-9-3` | 返信の送信 | [`.cursor/commands/lesson/start-9-3.md`](../.cursor/commands/lesson/start-9-3.md) |

#### Module 10（4個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-10-1` | Clasp基本・GASプロジェクト管理 | [`.cursor/commands/lesson/start-10-1.md`](../.cursor/commands/lesson/start-10-1.md) |
| `/start-10-2` | Google Calendar API連携・イベント自動化 | [`.cursor/commands/lesson/start-10-2.md`](../.cursor/commands/lesson/start-10-2.md) |
| `/start-10-3` | Google Sheets自動化・データ処理レポート | [`.cursor/commands/lesson/start-10-3.md`](../.cursor/commands/lesson/start-10-3.md) |
| `/start-10-4` | GmailAppメール検索・抽出→シート整理 | [`.cursor/commands/lesson/start-10-4.md`](../.cursor/commands/lesson/start-10-4.md) |

#### Module 11（5個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-11-1` | GitHub Actions Workflow基本・自動化 | [`.cursor/commands/lesson/start-11-1.md`](../.cursor/commands/lesson/start-11-1.md) |
| `/start-11-2` | GitHub Actions Secrets設定・Google連携 | [`.cursor/commands/lesson/start-11-2.md`](../.cursor/commands/lesson/start-11-2.md) |
| `/start-11-3` | ニュース取得→メール/Slack配信ワークフロー | [`.cursor/commands/lesson/start-11-3.md`](../.cursor/commands/lesson/start-11-3.md) |
| `/start-11-4` | Claude Code / Codex / Cursor を GitHub Actions で呼ぶ | [`.cursor/commands/lesson/start-11-4.md`](../.cursor/commands/lesson/start-11-4.md) |
| `/start-11-5` | GitHub Actions でデプロイ・ファイル生成 | [`.cursor/commands/lesson/start-11-5.md`](../.cursor/commands/lesson/start-11-5.md) |

#### Module 12（6個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-12-1` | ncliセットアップ・ブラウザ認証 | [`.cursor/commands/lesson/start-12-1.md`](../.cursor/commands/lesson/start-12-1.md) |
| `/start-12-2` | データベース取得・クエリ | [`.cursor/commands/lesson/start-12-2.md`](../.cursor/commands/lesson/start-12-2.md) |
| `/start-12-3` | ファイル取得 | [`.cursor/commands/lesson/start-12-3.md`](../.cursor/commands/lesson/start-12-3.md) |
| `/start-12-4` | ファイル作成・ページ作成 | [`.cursor/commands/lesson/start-12-4.md`](../.cursor/commands/lesson/start-12-4.md) |
| `/start-12-5` | 書き込みと更新 | [`.cursor/commands/lesson/start-12-5.md`](../.cursor/commands/lesson/start-12-5.md) |
| `/start-12-6` | 要約の作成とコメントの返信 | [`.cursor/commands/lesson/start-12-6.md`](../.cursor/commands/lesson/start-12-6.md) |

#### Module 13（5個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-13-1` | 訴求の整理（ヒアリング & コピーライティング） | [`.cursor/commands/lesson/start-13-1.md`](../.cursor/commands/lesson/start-13-1.md) |
| `/start-13-2` | ワイヤーフレーム作成（ASCII + ビジュアルWF） | [`.cursor/commands/lesson/start-13-2.md`](../.cursor/commands/lesson/start-13-2.md) |
| `/start-13-3` | デザインファイル作成（Pencil MCP） | [`.cursor/commands/lesson/start-13-3.md`](../.cursor/commands/lesson/start-13-3.md) |
| `/start-13-4` | 実際に動くLP作成（HTML/CSS/JS） | [`.cursor/commands/lesson/start-13-4.md`](../.cursor/commands/lesson/start-13-4.md) |
| `/start-13-5` | Vercelデプロイ | [`.cursor/commands/lesson/start-13-5.md`](../.cursor/commands/lesson/start-13-5.md) |

#### Module 14（7個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-14-1` | 記事企画 - テーマ決定・アウトライン生成 | [`.cursor/commands/lesson/start-14-1.md`](../.cursor/commands/lesson/start-14-1.md) |
| `/start-14-2` | 文体学習 - スタイルプロファイル作成 | [`.cursor/commands/lesson/start-14-2.md`](../.cursor/commands/lesson/start-14-2.md) |
| `/start-14-3` | 記事執筆 - スタイル適用ドラフト作成 | [`.cursor/commands/lesson/start-14-3.md`](../.cursor/commands/lesson/start-14-3.md) |
| `/start-14-4` | 挿絵計画と生成 - nanobanana + PlantUML | [`.cursor/commands/lesson/start-14-4.md`](../.cursor/commands/lesson/start-14-4.md) |
| `/start-14-5` | 校閲 - 校閲エージェントによるレビュー | [`.cursor/commands/lesson/start-14-5.md`](../.cursor/commands/lesson/start-14-5.md) |
| `/start-14-6` | ファクトチェック - 事実検証エージェント | [`.cursor/commands/lesson/start-14-6.md`](../.cursor/commands/lesson/start-14-6.md) |
| `/start-14-7` | 並列実行と仕上げ - 複数記事の同時処理 | [`.cursor/commands/lesson/start-14-7.md`](../.cursor/commands/lesson/start-14-7.md) |

#### Module 15（13個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-15-1` | 動画フレーム分析 | [`.cursor/commands/lesson/start-15-1.md`](../.cursor/commands/lesson/start-15-1.md) |
| `/start-15-2` | Remotion アニメーション基礎 — スライドシュート風テキストアニメ | [`.cursor/commands/lesson/start-15-2.md`](../.cursor/commands/lesson/start-15-2.md) |
| `/start-15-3` | YouTube Clipper — 動画ハイライト抽出 | [`.cursor/commands/lesson/start-15-3.md`](../.cursor/commands/lesson/start-15-3.md) |
| `/start-15-4` | Clipper × Remotion — マーケ素材自動生成 | [`.cursor/commands/lesson/start-15-4.md`](../.cursor/commands/lesson/start-15-4.md) |
| `/start-15-5` | 動画AIエンジン概要 | [`.cursor/commands/lesson/start-15-5.md`](../.cursor/commands/lesson/start-15-5.md) |
| `/start-15-6` | Storyboard Anime Video | [`.cursor/commands/lesson/start-15-6.md`](../.cursor/commands/lesson/start-15-6.md) |
| `/start-15-7` | Music Video | [`.cursor/commands/lesson/start-15-7.md`](../.cursor/commands/lesson/start-15-7.md) |
| `/start-15-8` | Slide Narration Video | [`.cursor/commands/lesson/start-15-8.md`](../.cursor/commands/lesson/start-15-8.md) |
| `/start-15-9` | Product Demo Video | [`.cursor/commands/lesson/start-15-9.md`](../.cursor/commands/lesson/start-15-9.md) |
| `/start-15-10` | 記事からSNS紹介動画 | [`.cursor/commands/lesson/start-15-10.md`](../.cursor/commands/lesson/start-15-10.md) |
| `/start-15-11` | Remotionで思い通りの動きにするには | [`.cursor/commands/lesson/start-15-11.md`](../.cursor/commands/lesson/start-15-11.md) |
| `/start-15-12` | Remotion + SRTキャプション | [`.cursor/commands/lesson/start-15-12.md`](../.cursor/commands/lesson/start-15-12.md) |
| `/start-15-13` | アニメーションとスライドショー | [`.cursor/commands/lesson/start-15-13.md`](../.cursor/commands/lesson/start-15-13.md) |

#### Module 16（8個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-16-1` | Gmail セットアップ - gogcli 認証とメール同期 | [`.cursor/commands/lesson/start-16-1.md`](../.cursor/commands/lesson/start-16-1.md) |
| `/start-16-2` | 受信メール分析 & タスク抽出 | [`.cursor/commands/lesson/start-16-2.md`](../.cursor/commands/lesson/start-16-2.md) |
| `/start-16-3` | gogcli でメール送信 | [`.cursor/commands/lesson/start-16-3.md`](../.cursor/commands/lesson/start-16-3.md) |
| `/start-16-4` | メールシーケンス設計 | [`.cursor/commands/lesson/start-16-4.md`](../.cursor/commands/lesson/start-16-4.md) |
| `/start-16-5` | メール自動化ワークフロー | [`.cursor/commands/lesson/start-16-5.md`](../.cursor/commands/lesson/start-16-5.md) |
| `/start-16-6` | Resend 登録 & ドメイン設定 | [`.cursor/commands/lesson/start-16-6.md`](../.cursor/commands/lesson/start-16-6.md) |
| `/start-16-7` | APIキー作成 & 初回メール送信 | [`.cursor/commands/lesson/start-16-7.md`](../.cursor/commands/lesson/start-16-7.md) |
| `/start-16-8` | Resend Sequence & CLI でドリップキャンペーン | [`.cursor/commands/lesson/start-16-8.md`](../.cursor/commands/lesson/start-16-8.md) |

#### Module 17（5個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-17-1` | X投稿 & バナー作成 | [`.cursor/commands/lesson/start-17-1.md`](../.cursor/commands/lesson/start-17-1.md) |
| `/start-17-2` | SEO調査 & キーワード戦略 | [`.cursor/commands/lesson/start-17-2.md`](../.cursor/commands/lesson/start-17-2.md) |
| `/start-17-3` | コピーライティング | [`.cursor/commands/lesson/start-17-3.md`](../.cursor/commands/lesson/start-17-3.md) |
| `/start-17-4` | Pencil MCPでデザインモックアップ | [`.cursor/commands/lesson/start-17-4.md`](../.cursor/commands/lesson/start-17-4.md) |
| `/start-17-5` | Typefully で X/Threads 投稿自動化 | [`.cursor/commands/lesson/start-17-5.md`](../.cursor/commands/lesson/start-17-5.md) |

#### Module 18（20個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-18-1` | 顧客インタビュー & ニーズ収集 | [`.cursor/commands/lesson/start-18-1.md`](../.cursor/commands/lesson/start-18-1.md) |
| `/start-18-2` | 要求資料の作成 | [`.cursor/commands/lesson/start-18-2.md`](../.cursor/commands/lesson/start-18-2.md) |
| `/start-18-3` | PRD作成（Working Backwards方式） | [`.cursor/commands/lesson/start-18-3.md`](../.cursor/commands/lesson/start-18-3.md) |
| `/start-18-4` | 3種レビュー | [`.cursor/commands/lesson/start-18-4.md`](../.cursor/commands/lesson/start-18-4.md) |
| `/start-18-5` | 要件定義書の作成 | [`.cursor/commands/lesson/start-18-5.md`](../.cursor/commands/lesson/start-18-5.md) |
| `/start-18-6` | ユースケース記述 & シーケンス図 | [`.cursor/commands/lesson/start-18-6.md`](../.cursor/commands/lesson/start-18-6.md) |
| `/start-18-7` | 画面遷移図 & ワイヤーフレーム | [`.cursor/commands/lesson/start-18-7.md`](../.cursor/commands/lesson/start-18-7.md) |
| `/start-18-8` | DB設計 | [`.cursor/commands/lesson/start-18-8.md`](../.cursor/commands/lesson/start-18-8.md) |
| `/start-18-9` | システム構成図 & API設計 | [`.cursor/commands/lesson/start-18-9.md`](../.cursor/commands/lesson/start-18-9.md) |
| `/start-18-10` | WBS & ガントチャート | [`.cursor/commands/lesson/start-18-10.md`](../.cursor/commands/lesson/start-18-10.md) |
| `/start-18-11` | Notion連携 | [`.cursor/commands/lesson/start-18-11.md`](../.cursor/commands/lesson/start-18-11.md) |
| `/start-18-12` | UIデザイン（Pencil MCP） | [`.cursor/commands/lesson/start-18-12.md`](../.cursor/commands/lesson/start-18-12.md) |
| `/start-18-13` | HTML + Tailwind CSS プロトタイプ | [`.cursor/commands/lesson/start-18-13.md`](../.cursor/commands/lesson/start-18-13.md) |
| `/start-18-14` | Playwright E2Eテスト | [`.cursor/commands/lesson/start-18-14.md`](../.cursor/commands/lesson/start-18-14.md) |
| `/start-18-15` | テスト計画書 & テストケース生成 | [`.cursor/commands/lesson/start-18-15.md`](../.cursor/commands/lesson/start-18-15.md) |
| `/start-18-16` | 単体テスト実施 | [`.cursor/commands/lesson/start-18-16.md`](../.cursor/commands/lesson/start-18-16.md) |
| `/start-18-17` | 結合テスト実施 | [`.cursor/commands/lesson/start-18-17.md`](../.cursor/commands/lesson/start-18-17.md) |
| `/start-18-18` | 会議体設計 & 議事録分析 | [`.cursor/commands/lesson/start-18-18.md`](../.cursor/commands/lesson/start-18-18.md) |
| `/start-18-19` | marimo ダッシュボード | [`.cursor/commands/lesson/start-18-19.md`](../.cursor/commands/lesson/start-18-19.md) |
| `/start-18-20` | 総合演習（カプストーン） | [`.cursor/commands/lesson/start-18-20.md`](../.cursor/commands/lesson/start-18-20.md) |

#### Module 19（3個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-m365cli` | M365 CLI セットアップ | [`.cursor/commands/lesson/setup-m365cli.md`](../.cursor/commands/lesson/setup-m365cli.md) |
| `/start-19-1` | Microsoft Office連携(Outlook) 入門 | [`.cursor/commands/lesson/start-19-1.md`](../.cursor/commands/lesson/start-19-1.md) |
| `/start-19-2` | フォルダ・ルール・カテゴリ | [`.cursor/commands/lesson/start-19-2.md`](../.cursor/commands/lesson/start-19-2.md) |

#### Module 20（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-freee` | Freee MCP セットアップ | [`.cursor/commands/lesson/setup-freee.md`](../.cursor/commands/lesson/setup-freee.md) |
| `/start-20-1` | Freee/MoneyForward連携 入門 | [`.cursor/commands/lesson/start-20-1.md`](../.cursor/commands/lesson/start-20-1.md) |

#### Module 21（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-figma` | Figma + Serendie デザインシステム MCP セットアップ | [`.cursor/commands/lesson/setup-figma.md`](../.cursor/commands/lesson/setup-figma.md) |
| `/start-21-1` | Figma 連携 入門 | [`.cursor/commands/lesson/start-21-1.md`](../.cursor/commands/lesson/start-21-1.md) |

#### Module 22（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-discord` | Discord Bot + Claude Code Channels 公式 plugin セットアップ | [`.cursor/commands/lesson/setup-discord.md`](../.cursor/commands/lesson/setup-discord.md) |
| `/start-22-1` | Discord 連携 入門 | [`.cursor/commands/lesson/start-22-1.md`](../.cursor/commands/lesson/start-22-1.md) |

#### Module 23（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-line-harness` | line-harness-oss + Cloudflare デプロイ | [`.cursor/commands/lesson/setup-line-harness.md`](../.cursor/commands/lesson/setup-line-harness.md) |
| `/start-23-1` | LINE 公式アカウント運用 入門 | [`.cursor/commands/lesson/start-23-1.md`](../.cursor/commands/lesson/start-23-1.md) |

#### Module 24（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-salesforce` | Salesforce CLI (sf) セットアップ | [`.cursor/commands/lesson/setup-salesforce.md`](../.cursor/commands/lesson/setup-salesforce.md) |
| `/start-24-1` | Salesforce CLI 連携 入門 | [`.cursor/commands/lesson/start-24-1.md`](../.cursor/commands/lesson/start-24-1.md) |

#### Module 25（2個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/setup-google-ads` | Google Ads API セットアップ | [`.cursor/commands/lesson/setup-google-ads.md`](../.cursor/commands/lesson/setup-google-ads.md) |
| `/start-25-1` | Google Ads 連携 入門 | [`.cursor/commands/lesson/start-25-1.md`](../.cursor/commands/lesson/start-25-1.md) |

#### Module 29（4個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/start-29-1` | slide-forge APIキー不要デモ | [`.cursor/commands/lesson/start-29-1.md`](../.cursor/commands/lesson/start-29-1.md) |
| `/start-29-2` | 議事録から本番生成・5問 | [`.cursor/commands/lesson/start-29-2.md`](../.cursor/commands/lesson/start-29-2.md) |
| `/start-29-3` | revise で既存ジョブを修正 | [`.cursor/commands/lesson/start-29-3.md`](../.cursor/commands/lesson/start-29-3.md) |
| `/start-29-4` | 実画像の自動取得 fetch-assets | [`.cursor/commands/lesson/start-29-4.md`](../.cursor/commands/lesson/start-29-4.md) |

#### 共通・セットアップ（21個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/check-security` | セキュリティ設定確認 | [`.cursor/commands/lesson/check-security.md`](../.cursor/commands/lesson/check-security.md) |
| `/check-setup` | 環境の自動チェック | [`.cursor/commands/lesson/check-setup.md`](../.cursor/commands/lesson/check-setup.md) |
| `/exercise-review` | 応用演習レビュー | [`.cursor/commands/lesson/exercise-review.md`](../.cursor/commands/lesson/exercise-review.md) |
| `/setup-bigquery` | BigQuery / GCP 認証セットアップ | [`.cursor/commands/lesson/setup-bigquery.md`](../.cursor/commands/lesson/setup-bigquery.md) |
| `/setup-clasp` | Google Apps Script CLI (clasp) セットアップ | [`.cursor/commands/lesson/setup-clasp.md`](../.cursor/commands/lesson/setup-clasp.md) |
| `/setup-elevenlabs` | ElevenLabs API セットアップ | [`.cursor/commands/lesson/setup-elevenlabs.md`](../.cursor/commands/lesson/setup-elevenlabs.md) |
| `/setup-extensions` | 拡張機能の自動セットアップ | [`.cursor/commands/lesson/setup-extensions.md`](../.cursor/commands/lesson/setup-extensions.md) |
| `/setup-fal` | fal.ai API セットアップ | [`.cursor/commands/lesson/setup-fal.md`](../.cursor/commands/lesson/setup-fal.md) |
| `/setup-gemini` | Gemini API セットアップ | [`.cursor/commands/lesson/setup-gemini.md`](../.cursor/commands/lesson/setup-gemini.md) |
| `/setup-github` | GitHub アカウント設定とリポジトリ作成 | [`.cursor/commands/lesson/setup-github.md`](../.cursor/commands/lesson/setup-github.md) |
| `/setup-gogcli` | gogcli (Google Workspace CLI) セットアップ | [`.cursor/commands/lesson/setup-gogcli.md`](../.cursor/commands/lesson/setup-gogcli.md) |
| `/setup-notion` | Notion CLI (ncli) + Hosted MCP セットアップ（OAuth 統一） | [`.cursor/commands/lesson/setup-notion.md`](../.cursor/commands/lesson/setup-notion.md) |
| `/setup-pencil` | Pencil MCP セットアップ | [`.cursor/commands/lesson/setup-pencil.md`](../.cursor/commands/lesson/setup-pencil.md) |
| `/setup-remotion` | Remotion セットアップ | [`.cursor/commands/lesson/setup-remotion.md`](../.cursor/commands/lesson/setup-remotion.md) |
| `/setup-security` | セキュリティ設定の自動セットアップ | [`.cursor/commands/lesson/setup-security.md`](../.cursor/commands/lesson/setup-security.md) |
| `/setup-slack` | Slack API セットアップ | [`.cursor/commands/lesson/setup-slack.md`](../.cursor/commands/lesson/setup-slack.md) |
| `/setup-start` | 研修環境セットアップ | [`.cursor/commands/lesson/setup-start.md`](../.cursor/commands/lesson/setup-start.md) |
| `/setup-typefully` | Typefully API セットアップ | [`.cursor/commands/lesson/setup-typefully.md`](../.cursor/commands/lesson/setup-typefully.md) |
| `/setup-vercel` | Vercel CLI セットアップ | [`.cursor/commands/lesson/setup-vercel.md`](../.cursor/commands/lesson/setup-vercel.md) |
| `/setup-x-api` | X (Twitter) API セットアップ | [`.cursor/commands/lesson/setup-x-api.md`](../.cursor/commands/lesson/setup-x-api.md) |
| `/verify-module` | [モジュール番号] | [`.cursor/commands/lesson/verify-module.md`](../.cursor/commands/lesson/verify-module.md) |

### ユーティリティコマンド（33個）

| コマンド | 説明 | 定義 |
|---|---|---|
| `/annotate-screenshot` | Annotate Screenshot with Nano Banana Pro | [`.cursor/commands/utility/annotate-screenshot.md`](../.cursor/commands/utility/annotate-screenshot.md) |
| `/api-setup-wizard` | API設定ガイド統合（各種サービスのセットアップ一覧） | [`.cursor/commands/utility/api-setup-wizard.md`](../.cursor/commands/utility/api-setup-wizard.md) |
| `/bigquery-auth` | BigQuery Auth - プロジェクト単位のBigQuery認証 | [`.cursor/commands/utility/bigquery-auth.md`](../.cursor/commands/utility/bigquery-auth.md) |
| `/capture-tutorial` | Capture Tutorial - スクリーンショットから操作チュートリアル生成 | [`.cursor/commands/utility/capture-tutorial.md`](../.cursor/commands/utility/capture-tutorial.md) |
| `/create-banner` | Create Banner - 広告バナー/クリエイティブ生成 | [`.cursor/commands/utility/create-banner.md`](../.cursor/commands/utility/create-banner.md) |
| `/excel-ops` | Excel Operations - Excel操作 | [`.cursor/commands/utility/excel-ops.md`](../.cursor/commands/utility/excel-ops.md) |
| `/extract-tasks` | Extract Tasks - タスク抽出 | [`.cursor/commands/utility/extract-tasks.md`](../.cursor/commands/utility/extract-tasks.md) |
| `/fetch-slides` | Fetch Slides - Google Slides取得 | [`.cursor/commands/utility/fetch-slides.md`](../.cursor/commands/utility/fetch-slides.md) |
| `/generate-diagram` | Generate Diagram with Nano Banana Pro | [`.cursor/commands/utility/generate-diagram.md`](../.cursor/commands/utility/generate-diagram.md) |
| `/generate-plantuml-diagram` | Generate PlantUML Diagram with Nano Banana Pro | [`.cursor/commands/utility/generate-plantuml-diagram.md`](../.cursor/commands/utility/generate-plantuml-diagram.md) |
| `/generate-slide` | Generate Lecture Slide with Nano Banana Pro | [`.cursor/commands/utility/generate-slide.md`](../.cursor/commands/utility/generate-slide.md) |
| `/gmail-account-setup` | Gmail アカウント セットアップ | [`.cursor/commands/utility/gmail-account-setup.md`](../.cursor/commands/utility/gmail-account-setup.md) |
| `/gmail-pending-replies` | Gmail Pending Replies - メール未返信抽出 | [`.cursor/commands/utility/gmail-pending-replies.md`](../.cursor/commands/utility/gmail-pending-replies.md) |
| `/google-account-setup` | Google アカウント セットアップ（Calendar/Drive用） | [`.cursor/commands/utility/google-account-setup.md`](../.cursor/commands/utility/google-account-setup.md) |
| `/guide` | 次のアクション提示 | [`.cursor/commands/utility/guide.md`](../.cursor/commands/utility/guide.md) |
| `/install-plugins` | 外部プラグインからスキルをインストール | [`.cursor/commands/utility/install-plugins.md`](../.cursor/commands/utility/install-plugins.md) |
| `/nanobanana` | Nano Banana Pro 画像生成・編集 | [`.cursor/commands/utility/nanobanana.md`](../.cursor/commands/utility/nanobanana.md) |
| `/notebooklm` | API notebooks | [`.cursor/commands/utility/notebooklm.md`](../.cursor/commands/utility/notebooklm.md) |
| `/notion-fetch` | Notion Fetch - Notion連携 | [`.cursor/commands/utility/notion-fetch.md`](../.cursor/commands/utility/notion-fetch.md) |
| `/overview` | プロジェクト構造可視化 | [`.cursor/commands/utility/overview.md`](../.cursor/commands/utility/overview.md) |
| `/pdf-editor` | PDF Page Editor | [`.cursor/commands/utility/pdf-editor.md`](../.cursor/commands/utility/pdf-editor.md) |
| `/pptx-ops` | PowerPoint Operations - PPTX操作 | [`.cursor/commands/utility/pptx-ops.md`](../.cursor/commands/utility/pptx-ops.md) |
| `/pptx-template` | PPTXテンプレート操作 | [`.cursor/commands/utility/pptx-template.md`](../.cursor/commands/utility/pptx-template.md) |
| `/screenshot-analyzer` | Screenshot Analyzer - スクリーンショット解析統合ツール | [`.cursor/commands/utility/screenshot-analyzer.md`](../.cursor/commands/utility/screenshot-analyzer.md) |
| `/setup-google-api` | Setup Google API for MCP - Google API設定ガイド | [`.cursor/commands/utility/setup-google-api.md`](../.cursor/commands/utility/setup-google-api.md) |
| `/slide-forge` | Slide Forge — 骨子からスライドを作る | [`.cursor/commands/utility/slide-forge.md`](../.cursor/commands/utility/slide-forge.md) |
| `/sync-skills` | スキルをグローバル・他プロジェクトに同期 | [`.cursor/commands/utility/sync-skills.md`](../.cursor/commands/utility/sync-skills.md) |
| `/tools-index` | Tools Index - ツール一覧 | [`.cursor/commands/utility/tools-index.md`](../.cursor/commands/utility/tools-index.md) |
| `/tutor` | 学習コンテンツ生成 | [`.cursor/commands/utility/tutor.md`](../.cursor/commands/utility/tutor.md) |
| `/update-material` | 元リポジトリ（upstream）から最新の教材を取り込む | [`.cursor/commands/utility/update-material.md`](../.cursor/commands/utility/update-material.md) |
| `/update-plugins` | インストール済み外部スキルを更新 | [`.cursor/commands/utility/update-plugins.md`](../.cursor/commands/utility/update-plugins.md) |
| `/update-skills` | upstream からスキルの最新版を取り込む | [`.cursor/commands/utility/update-skills.md`](../.cursor/commands/utility/update-skills.md) |
| `/video-frame-reader` | Video Frame Reader - 動画キーフレーム抽出 | [`.cursor/commands/utility/video-frame-reader.md`](../.cursor/commands/utility/video-frame-reader.md) |

### トップレベルコマンド（22個）

| コマンド | Module | 説明 | 定義 |
|---|---:|---|---|
| `/cursor-daisuki` | — | 研修スタート - コース教材を自動で開く | [`.cursor/commands/cursor-daisuki.md`](../.cursor/commands/cursor-daisuki.md) |
| `/env-check` | — | 開発環境の状態をチェック | [`.cursor/commands/env-check.md`](../.cursor/commands/env-check.md) |
| `/module-18-calendar` | Module 18 | Module 18 Lesson 4-2 — Calendar（calendar_ops / gog calendar）をプロンプトで支援 | [`.cursor/commands/module-18-calendar.md`](../.cursor/commands/module-18-calendar.md) |
| `/module-18-drive` | Module 18 | Module 18 Lesson 4-4 — Google Drive（drive_ops / gog drive）をプロンプトで支援 | [`.cursor/commands/module-18-drive.md`](../.cursor/commands/module-18-drive.md) |
| `/module-18-gas` | Module 18 | Module 18 Lesson 4-6 — GAS × clasp 統合をプロンプトで支援 | [`.cursor/commands/module-18-gas.md`](../.cursor/commands/module-18-gas.md) |
| `/module-18-gcp-appendix` | Module 18 | スラッシュ /module-18-gcp-appendix — Module 18 — GCP を自分で運用する（コンソール手順のチェックリスト） | [`.cursor/commands/module-18-gcp-appendix.md`](../.cursor/commands/module-18-gcp-appendix.md) |
| `/module-18-gcp-quick` | Module 18 | スラッシュ /module-18-gcp-quick — Module 18 Lesson 4-1 — ai-agent-camp 同梱 OAuth で gog 認証まで（ターミナル手入力不要） | [`.cursor/commands/module-18-gcp-quick.md`](../.cursor/commands/module-18-gcp-quick.md) |
| `/module-18-gmail` | Module 18 | Module 18 Lesson 4-3 — Gmail（gmail_ops / gog gmail）をプロンプトで支援 | [`.cursor/commands/module-18-gmail.md`](../.cursor/commands/module-18-gmail.md) |
| `/module-18-google-auth` | Module 18 | スラッシュ /module-18-google-auth — Module 18 Lesson 4-1 — Google 認証（gog auth）と Gmail/Calendar 動作確認を支援 | [`.cursor/commands/module-18-google-auth.md`](../.cursor/commands/module-18-google-auth.md) |
| `/module-18-sheets` | Module 18 | Module 18 Lesson 4-5 — Google Sheets（sheets_ops）をプロンプトで支援 | [`.cursor/commands/module-18-sheets.md`](../.cursor/commands/module-18-sheets.md) |
| `/module-24-exercise` | Module 24 | When the user says /module-24-exercise — Module 24 演習チェックリスト（SOQL / CSV / メタデータ） | [`.cursor/commands/module-24-exercise.md`](../.cursor/commands/module-24-exercise.md) |
| `/module-24-metadata-deploy` | Module 24 | When the user says /module-24-metadata-deploy — Module 24 — Sandbox へメタデータ deploy | [`.cursor/commands/module-24-metadata-deploy.md`](../.cursor/commands/module-24-metadata-deploy.md) |
| `/module-24-metadata-retrieve` | Module 24 | When the user says /module-24-metadata-retrieve — Module 24 — Apex / Flow / Layout を retrieve | [`.cursor/commands/module-24-metadata-retrieve.md`](../.cursor/commands/module-24-metadata-retrieve.md) |
| `/module-24-soql` | Module 24 | When the user says /module-24-soql — Module 24 SOQL — sf data query で Account / Opportunity を取得 | [`.cursor/commands/module-24-soql.md`](../.cursor/commands/module-24-soql.md) |
| `/next_lesson` | — | 完了チェックして次のレッスンへ進む | [`.cursor/commands/next_lesson.md`](../.cursor/commands/next_lesson.md) |
| `/project-info` | — | プロジェクト情報を表示 | [`.cursor/commands/project-info.md`](../.cursor/commands/project-info.md) |
| `/run-tests` | — | プロジェクトのテストを実行 | [`.cursor/commands/run-tests.md`](../.cursor/commands/run-tests.md) |
| `/setup-api-key` | — | APIキー・トークンを安全に設定する手順を案内する（初学者向け） | [`.cursor/commands/setup-api-key.md`](../.cursor/commands/setup-api-key.md) |
| `/start-cursor-bootcamp` | — | 研修スタート - コース教材を自動で開く | [`.cursor/commands/start-cursor-bootcamp.md`](../.cursor/commands/start-cursor-bootcamp.md) |
| `/研修をスタート` | — | 研修スタート - コース教材を自動で開く | [`.cursor/commands/研修をスタート.md`](../.cursor/commands/研修をスタート.md) |
| `/研修を始めたい` | — | 研修スタート - コース教材を自動で開く | [`.cursor/commands/研修を始めたい.md`](../.cursor/commands/研修を始めたい.md) |
| `/研修開始` | — | 研修スタート - コース教材を自動で開く | [`.cursor/commands/研修開始.md`](../.cursor/commands/研修開始.md) |
<!-- AUTO-GENERATED:commands END -->

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
