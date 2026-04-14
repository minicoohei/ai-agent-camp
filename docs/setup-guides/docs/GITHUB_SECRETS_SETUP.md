# GitHub Secrets セットアップガイド

CI/CDパイプラインやGitHub Actionsで安全にシークレット情報を管理・使用するための設定手順です。

---

## 概要

| 項目 | 内容 |
|------|------|
| 機能 | GitHub Actions 環境変数管理 |
| 用途 | API キー、トークン、認証情報の安全な保管 |
| 対応スコープ | リポジトリ、環境、Organization |
| 必要時間 | 約10分 |

---

## Secrets の種類と選択ガイド

| タイプ | スコープ | 公開性 | 用途 | 推奨度 |
|--------|---------|--------|------|:----:|
| Repository Secret | リポジトリ内のみ | プライベート | 単一リポジトリ用 | O |
| Environment Secret | 特定環境のみ | プライベート | 環境別設定（dev/prod） | OO |
| Organization Secret | Organization全体 | プライベート | 複数リポジトリ共有 | - |

> **推奨**: Repository Secret を使用し、環境による区分が必要な場合は Environment Secret を追加してください。

---

## ステップ1: リポジトリ Secrets の作成

### 1-1. GitHub リポジトリにアクセス

1. GitHub で対象リポジトリを開く
2. 「**Settings**」をクリック（右上のギアアイコン）

> **注意**: リポジトリの管理者権限が必要です。

### 1-2. Secrets メニューを開く

1. 左メニューの「**Secrets and variables**」をクリック
2. 「**Actions**」をクリック

![screenshot-placeholder: GitHub Settings > Secrets and variables > Actions]

---

## ステップ2: 新しい Secret を作成

### 2-1. Secret を追加

1. 「**New repository secret**」をクリック
2. Secret の名前を入力
   - 例: `GEMINI_API_KEY`
   - 例: `SLACK_USER_TOKEN`
   - 命名規則: すべて大文字、アンダースコア区切り

3. Secret の値を貼り付け
4. 「**Add secret**」をクリック

![screenshot-placeholder: New repository secret form]

### 2-2. 設定例

以下のような secrets を一般的に設定します：

```
GEMINI_API_KEY           → Google Gemini APIキー
SLACK_USER_TOKEN         → Slack User Token（推奨）
SLACK_BOT_TOKEN          → Slack Bot Token（レガシー・オプション）
GOOGLE_CREDENTIALS_JSON  → Google OAuth credentials (Base64)
BIGQUERY_PROJECT_ID      → BigQuery Project ID
GITHUB_TOKEN             → GitHub Personal Access Token
```

---

## ステップ3: 環境別 Secrets の設定

本番環境と開発環境で異なる API キーを使用する場合：

### 3-1. Environment の作成

1. 「**Environments**」をクリック
2. 「**New environment**」をクリック
3. 環境名を入力
   - 例: `production`
   - 例: `staging`
   - 例: `development`

4. 「**Configure environment**」をクリック

![screenshot-placeholder: Create new environment]

### 3-2. Environment Secret を作成

1. 「**Environment secrets**」セクションで「**Add secret**」
2. Secret 名と値を入力
3. Repository Secret と同じ名前を使用するのが推奨

### 3-3. Environment の保護ルール設定（オプション）

本番環境の場合、リリースを要求するなど保護ルールを設定：

1. 「**Deployment branches and tags**」セクション
2. 「**Add deployment branch rule**」
3. ルールを設定
   - 例: `main` ブランチのみ
   - 例: 承認者の指定

---

## ステップ4: GitHub Actions ワークフローで Secrets を使用

### 4-1. 基本的な使用方法

`.github/workflows/main.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Repository Secret を使用
      - name: Test with Gemini API
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          python test_gemini.py

      # 複数の Secret を使用
      - name: Run analysis
        env:
          SLACK_USER_TOKEN: ${{ secrets.SLACK_USER_TOKEN }}
          BIGQUERY_PROJECT: ${{ secrets.BIGQUERY_PROJECT_ID }}
        run: |
          python analyze.py
```

### 4-2. 環境別での実行

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production  # 環境指定
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        env:
          API_KEY: ${{ secrets.API_KEY }}  # production 環境の Secret を使用
        run: |
          python deploy.py
```

### 4-3. Secret を含むファイル作成（GitHub Actions内）

```yaml
- name: Create credentials file
  run: |
    echo '${{ secrets.GOOGLE_CREDENTIALS_JSON }}' > credentials.json
```

---

## ステップ5: Secret のベストプラクティス

### 5-1. Secret 値の管理

```yaml
# ❌ ダメな例: ログに出力される
- name: Test
  run: echo ${{ secrets.API_KEY }}

# ✅ 良い例: ログに出力されない
- name: Test
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: python test.py
```

### 5-2. Secret の整理

定期的に不要な Secret を削除：

1. Settings > Secrets and variables > Actions
2. 不要な Secret の横の「Delete」をクリック
3. 確認して削除

### 5-3. Secret のローテーション

セキュリティのため、定期的に Secret 値を更新：

- **APIキー**: 3ヶ月ごと
- **トークン**: 6ヶ月ごと
- **パスワード**: 3ヶ月ごと

### 5-4. .env ファイルとの連携

ローカル開発では `.env` を使用、CI/CD では Secrets を使用：

```python
# 互換性のあるコード
import os
from dotenv import load_dotenv

# ローカル: .env から読み込み
load_dotenv()

# CI/CD: 環境変数から読み込み
api_key = os.getenv("GEMINI_API_KEY")
```

---

## ステップ6: 複数リポジトリでの共有（Organization Secrets）

複数リポジトリで同じ Secret を使用する場合：

### 6-1. Organization Secret 作成

1. Organization トップページにアクセス
2. 「**Settings**」をクリック（右下）
3. 「**Secrets and variables**」> 「**Actions**」
4. 「**New organization secret**」をクリック

### 6-2. リポジトリアクセス権限設定

1. Secret 作成時にリポジトリを選択
   - 「Selected repositories」: 特定リポジトリのみ
   - 「All repositories」: Organization 全体

### 6-3. ワークフローでの使用

Repository Secret と同じ方法で使用可能：

```yaml
env:
  SHARED_API_KEY: ${{ secrets.SHARED_API_KEY }}
```

---

## ステップ7: Secret 値の取得と確認

### 7-1. Secret の確認（1回目の確認）

Secret 作成時のみ確認可能。以降は確認できません。

> **重要**: Secret の値は一度しか表示されません。複数回確認が必要な場合は、事前にメモしてください。

### 7-2. Secret 値の更新

```yaml
# 既存の Secret を更新
1. Settings > Secrets and variables > Actions
2. Secret 名をクリック
3. 「Update」をクリック
4. 新しい値を入力
5. 「Update secret」をクリック
```

### 7-3. Secret が使用されているワークフロー確認

1. Settings > Secrets and variables > Actions
2. Secret 名をクリック
3. 「Used by」セクションを確認

---

## ステップ8: トラブルシューティング

### Secret が認識されない

```
Error: The following errors were encountered when processing your workflow file
```

**解決策**:
1. Secret の名前が正確か確認
   - 大文字・小文字の区別あり
2. YAML ファイルの構文を確認
3. インデントを確認

### ワークフローでログに Secret が出力される

```
##[warning]Unexpected input: 'GEMINI_API_KEY'
```

**解決策**:
1. Secret 名の綴りを確認
2. `env:` セクションでの設定確認
3. `run:` コマンドでログ出力していないか確認

### Secret の値が古い

```
Error: 401 Unauthorized
```

**解決策**:
1. Secret 値が最新か確認
2. APIキーの有効期限を確認
3. Secret を更新して、ワークフローを再実行

### 環境別 Secret が使用されない

```
Error: Secret not found
```

**解決策**:
1. Environment 名が正確か確認
   - ワークフロー: `environment: production`
   - Secret 作成先: `production` 環境
2. Environment Secret が作成されているか確認

---

## セキュリティチェックリスト

- [ ] Secret を `.gitignore` に追加
- [ ] Secret 値をコードに直書きしていない
- [ ] `secrets.*` を使用している
- [ ] ログに Secret が出力されていないか確認
- [ ] 不要な Secret を定期的に削除
- [ ] Secret のアクセス権限を定期的に確認
- [ ] Secret を定期的にローテーション
- [ ] Repository Secret と Environment Secret を使い分け

---

## よく使う Secret リスト

このプロジェクトで設定する Secret の例：

| Secret名 | 値の例 | 用途 | 有効期限 |
|---------|--------|------|---------|
| `GEMINI_API_KEY` | `AIzaSy...` | Gemini API | 無期限 |
| `SLACK_USER_TOKEN` | `xoxp-...` | Slack User Token（推奨） | 無期限 |
| `SLACK_BOT_TOKEN` | `xoxb-...` | Slack Bot Token（レガシー） | 無期限 |
| `GOOGLE_CREDENTIALS_BASE64` | Base64エンコード値 | OAuth認証 | 無期限 |
| `BIGQUERY_PROJECT_ID` | `my-gcp-project` | BigQuery | 無期限 |
| `GITHUB_TOKEN` | `ghp_...` | GitHub API | 設定可能 |

---

## ワークフロー例

### 例1: 複数 Secret を環境変数で使用

```yaml
name: Run Analysis

on: [push, pull_request]

jobs:
  analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run analysis with APIs
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          SLACK_USER_TOKEN: ${{ secrets.SLACK_USER_TOKEN }}
          BIGQUERY_PROJECT: ${{ secrets.BIGQUERY_PROJECT_ID }}
        run: |
          python scripts/analyze.py
```

### 例2: 環境別デプロイ

```yaml
name: Deploy

on:
  push:
    branches: [ main, develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    steps:
      - uses: actions/checkout@v3

      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          python deploy.py
```

### 例3: Google OAuth 認証

```yaml
- name: Setup Google credentials
  run: |
    echo '${{ secrets.GOOGLE_CREDENTIALS_BASE64 }}' | base64 -d > credentials.json

- name: Run Google API script
  env:
    GOOGLE_CREDENTIALS_PATH: ./credentials.json
  run: |
    python scripts/sync_google_data.py
```

---

## 使用するスキル

以下のスキルで GitHub Secrets を使用します：

- `data-analyst` - BigQuery と Google API 認証
- `check-inbox` - Slack/Gmail API 認証
- `slack-search.skill` - Slack API 認証
- `tutorial-generator` - Gemini API 認証

---

## 次のステップ

- [GEMINI_API_SETUP.md](./GEMINI_API_SETUP.md) - Gemini API設定
- [SLACK_TOKEN_SETUP.md](./SLACK_TOKEN_SETUP.md) - Slack Token設定
- [GOOGLE_OAUTH_SETUP.md](./GOOGLE_OAUTH_SETUP.md) - Google OAuth設定
- [BIGQUERY_SETUP.md](./BIGQUERY_SETUP.md) - BigQuery設定
