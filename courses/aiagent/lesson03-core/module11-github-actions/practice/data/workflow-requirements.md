# ワークフロー要件書

## 要件 1: CI/CD パイプライン

### トリガー
- `push` イベント: main, develop ブランチ
- `pull_request` イベント: main ブランチ向け

### ジョブ構成

#### ジョブ 1: test
- **ランナー**: ubuntu-latest
- **マトリックス**: Node.js 18, 20
- **ステップ**:
  1. リポジトリのチェックアウト
  2. Node.js のセットアップ（マトリックスのバージョン）
  3. `npm ci` で依存関係インストール
  4. `npm test` でテスト実行
  5. テスト結果をアーティファクトとしてアップロード

#### ジョブ 2: build
- **依存**: test ジョブ成功後
- **ステップ**:
  1. リポジトリのチェックアウト
  2. Node.js 20 のセットアップ
  3. `npm ci`
  4. `npm run build`
  5. ビルド成果物をアーティファクトとしてアップロード

#### ジョブ 3: deploy
- **依存**: build ジョブ成功後
- **条件**: main ブランチへの push のみ
- **ステップ**:
  1. ビルドアーティファクトのダウンロード
  2. デプロイスクリプト実行
  3. デプロイ完了通知

---

## 要件 2: 定期データ同期

### トリガー
- `schedule`: cron `0 0 * * *`（UTC 0:00 = JST 9:00）
- `workflow_dispatch`: 手動実行対応（入力パラメータ: sync_target）

### ジョブ構成

#### ジョブ: sync
- **ランナー**: ubuntu-latest
- **ステップ**:
  1. リポジトリのチェックアウト
  2. Python 3.11 セットアップ
  3. 依存関係インストール
  4. データ同期スクリプト実行
  5. 変更があればコミット＆プッシュ
  6. Slack Webhook で結果通知

### 環境変数・Secrets
- `SLACK_WEBHOOK_URL`: Slack 通知用
- `SYNC_API_KEY`: データソース認証用

---

## 要件 3: PR 自動レビュー

### トリガー
- `pull_request` イベント: opened, synchronize

### ジョブ構成

#### ジョブ: review
- **ランナー**: ubuntu-latest
- **ステップ**:
  1. リポジトリのチェックアウト
  2. 変更ファイルの一覧取得
  3. ファイルパスに基づくラベル付与
     - `docs/`, `*.md` → `documentation`
     - `src/frontend/`, `*.tsx` → `frontend`
     - `src/backend/`, `*.py` → `backend`
     - `tests/` → `test`
     - `.github/` → `ci/cd`
  4. PR 本文のテンプレートチェック（## 概要、## テスト計画 が含まれるか）
  5. 変更行数が 500 行を超える場合、警告コメントを投稿
