# BigQuery セットアップガイド

Google BigQueryに接続してデータ分析を行うための設定手順です。

---

## 概要

| 項目 | 内容 |
|------|------|
| サービス名 | Google BigQuery |
| 用途 | 大規模データの分析・可視化 |
| 無料枠 | 1TB/月のクエリ、10GBのストレージ |
| 必要時間 | 約15分 |

---

## 前提条件

- Google Cloud アカウント
- 請求先アカウントの設定（無料枠でも必要）
- gcloud CLI のインストール

---

## ステップ1: gcloud CLI のインストール

### macOS

```bash
# Homebrew でインストール
brew install google-cloud-sdk
```

### Windows

[Google Cloud SDK インストーラー](https://cloud.google.com/sdk/docs/install) をダウンロードして実行

### Linux

```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
tar -xf google-cloud-cli-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
```

### インストール確認

```bash
gcloud --version
```

---

## ステップ2: gcloud 初期設定

```bash
# 初期化
gcloud init

# 認証
gcloud auth login

# プロジェクト設定
gcloud config set project YOUR_PROJECT_ID
```

---

## ステップ3: 設定プロファイルの作成

複数のプロジェクトを扱う場合、プロファイルで管理します。

### プロファイル作成

```bash
# 新しいプロファイルを作成
gcloud config configurations create my-profile

# プロジェクトを設定
gcloud config set project my-gcp-project

# リージョンを設定
gcloud config set compute/region asia-northeast1

# アカウントを設定
gcloud config set account your-email@example.com
```

### プロファイル一覧の確認

```bash
gcloud config configurations list
```

出力例:
```
NAME        IS_ACTIVE  ACCOUNT                      PROJECT           COMPUTE_DEFAULT_ZONE  COMPUTE_DEFAULT_REGION
default     False      user@example.com             -                 -                     -
my-profile  True       user@example.com             my-gcp-project    -                     asia-northeast1
my-dev      False      user@example.com             my-dev-project    -                     asia-northeast1
```

### プロファイルの切り替え

```bash
gcloud config configurations activate my-profile
```

---

## ステップ4: Application Default Credentials の設定

BigQueryクライアントライブラリが使用する認証情報を設定します。

```bash
# 認証
gcloud auth application-default login

# ブラウザが開くので、Googleアカウントでログイン
# 権限を許可
```

認証情報は以下に保存されます：
- macOS/Linux: `~/.config/gcloud/application_default_credentials.json`
- Windows: `%APPDATA%\gcloud\application_default_credentials.json`

---

## ステップ5: BigQuery APIの有効化

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを選択
3. 「APIとサービス」>「ライブラリ」
4. 「BigQuery API」を検索して「有効にする」

または、コマンドで有効化：

```bash
gcloud services enable bigquery.googleapis.com
```

---

## ステップ6: 動作確認

### bq コマンドで確認

```bash
# テーブル一覧
bq ls project_id:dataset_name

# クエリ実行
bq query --use_legacy_sql=false \
  'SELECT COUNT(*) FROM `project_id.dataset.table`'
```

### Python で確認

```python
from google.cloud import bigquery

# クライアント作成
client = bigquery.Client()

# クエリ実行
query = """
SELECT COUNT(*) as count
FROM `bigquery-public-data.samples.shakespeare`
"""

results = client.query(query).result()
for row in results:
    print(f"Count: {row.count}")
```

---

## 利用可能なプロファイル

このプロジェクトで設定済みのプロファイル：

| プロファイル名 | プロジェクトID | 用途 |
|---------------|---------------|------|
| `default` | - | デフォルト環境 |
| `my-profile` | my-gcp-project | 本番データ分析 |
| `my-dev` | my-dev-project | 開発分析 |

---

## クエリのベストプラクティス

### パーティション条件を必ず指定

```sql
-- パーティションフィルタは必須
SELECT *
FROM `project.dataset.table`
WHERE _PARTITIONTIME >= '2025-01-01'
  AND _PARTITIONTIME < '2025-02-01'
```

### 重複除去パターン

```sql
WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY post.xPostId
            ORDER BY _PARTITIONTIME DESC
        ) as row_num
    FROM `project.dataset.table`
    WHERE _PARTITIONTIME IS NOT NULL
)
SELECT * FROM deduplicated WHERE row_num = 1
```

### コスト見積もり

```bash
# ドライラン（実行せずにバイト数を確認）
bq query --use_legacy_sql=false --dry_run \
  'SELECT * FROM `bigquery-public-data.samples.shakespeare`'
```

---

## 料金と制限

### 無料枠

| 項目 | 制限 |
|------|------|
| クエリ | 1 TB/月 |
| ストレージ | 10 GB |
| ストリーミング挿入 | 10 GB/月 |

### 料金（無料枠超過時）

| 項目 | 料金 |
|------|------|
| クエリ | $5.00 / TB |
| ストレージ | $0.02 / GB / 月 |
| ストリーミング | $0.01 / 200 MB |

> 最新の料金は [BigQuery Pricing](https://cloud.google.com/bigquery/pricing) を確認してください。

---

## トラブルシューティング

### 認証エラー

```
google.auth.exceptions.DefaultCredentialsError
```

**解決策**:
```bash
# 再認証
gcloud auth application-default login
```

### 権限エラー

```
Access Denied: Permission denied
```

**解決策**:
1. 必要なロールを確認
   - `roles/bigquery.dataViewer` - データ読み取り
   - `roles/bigquery.jobUser` - クエリ実行
2. IAM設定で権限を付与

### プロジェクトが見つからない

```
Not found: Project xxx
```

**解決策**:
```bash
# プロジェクト一覧を確認
gcloud projects list

# プロジェクトを再設定
gcloud config set project correct-project-id
```

### クエリがタイムアウト

**解決策**:
1. `LIMIT` を追加して結果を制限
2. パーティション条件を追加
3. 必要なカラムのみを選択

---

## Pythonでの利用

### 必要なパッケージ

```bash
uv add google-cloud-bigquery pandas db-dtypes
```

### 基本的な使用方法

```python
from google.cloud import bigquery
import pandas as pd

# クライアント作成
client = bigquery.Client()

# クエリ実行
query = """
SELECT *
FROM `bigquery-public-data.samples.shakespeare`
LIMIT 100
"""

# DataFrameとして取得
df = client.query(query).to_dataframe()
print(df.head())
```

### プロジェクトを明示的に指定

```python
# 特定のプロジェクトを使用
client = bigquery.Client(project='my-gcp-project')
```

---

## 使用するスキル

以下のスキルでBigQueryを使用します：

- `data-analyst` - EDA・可視化・ノートブック作成
- `bigquery-auth` - 認証設定サポート

---

## 次のステップ

- [NOTION_API_SETUP.md](./NOTION_API_SETUP.md) - Notion API設定
- [Module 4: データ分析](https://ai-agent.camp/ja/course/module-4) - データ分析の学習
- [data-analyst スキル](../../skills/data-analyst/SKILL.md) - 詳細な使用方法
