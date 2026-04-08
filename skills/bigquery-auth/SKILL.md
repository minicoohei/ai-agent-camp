---
name: bigquery-auth
description: GCPプロジェクト単位でBigQuery認証を設定。gcloud設定プロファイルで複数プロジェクトを安全に分離管理。「BigQueryに繋ぎたい」「{プロジェクト名}のデータを見たい」と言うだけで認証をガイド。
---

## トリガーワード
「BigQuery認証」「BQ繋ぎたい」「データ分析の認証」「gcloud認証」

# BigQuery Authentication (Project-based)

GCPプロジェクト単位でgcloud設定プロファイルを作成し、BigQuery認証を行うスキルです。

## Workflow

1. ユーザーが「BigQuery使いたい」「{プロジェクト}のデータを見たい」等と言う
2. **GCPプロジェクトIDを確認**（必須）
3. 既存の設定プロファイルを確認
4. 必要に応じて新規プロファイルを作成
5. ブラウザ認証をガイド
6. 接続テストを実行

## 認証手順

### Step 1: 設定プロファイル確認

```bash
gcloud config configurations list
```

既存プロファイルを表示し、目的のプロジェクト用があるか確認。

### Step 2: プロファイル作成（新規の場合）

```bash
# プロファイル作成
gcloud config configurations create {PROFILE_NAME}

# プロジェクト設定
gcloud config set project {PROJECT_ID}
```

### Step 3: gcloud認証

```bash
# メイン認証（ブラウザが開く）
gcloud auth login

# Python SDK用認証（ブラウザが開く）
gcloud auth application-default login --quiet
```

**注意**: 両方のコマンドでブラウザ認証が必要です。

### Step 4: 認証確認

```bash
# 現在のプロファイル確認
gcloud config configurations list

# プロジェクト確認
gcloud config get-value project

# ADCトークン確認
gcloud auth application-default print-access-token
```

### Step 5: BigQuery接続テスト

```python
import os
# 環境変数競合を回避
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"接続成功！{len(datasets)}個のデータセット")
```

## プロファイル切り替え

```bash
# プロファイル一覧
gcloud config configurations list

# 切り替え
gcloud config configurations activate {PROFILE_NAME}
```

## 登録済みプロファイル（テンプレート）

### ADC認証（gcloud login）

| プロファイル | プロジェクトID | アカウント | 用途 |
|-------------|---------------|-----------|------|
| `default` | {YOUR_PROJECT_ID} | {YOUR_EMAIL} | デフォルト |
| `{PROFILE_2}` | {PROJECT_ID_2} | {EMAIL_2} | 分析用 |

> 自分のプロジェクト情報に置き換えてください。

### サービスアカウント認証（外部プロジェクト）

| プロファイル | プロジェクトID | キーファイル | 用途 |
|-------------|---------------|-------------|------|
| `{SA_PROFILE}` | {SA_PROJECT_ID} | `~/.gcp/{SA_KEY_FILE}.json` | 外部プロジェクト分析 |

## サービスアカウント認証の使い方

外部プロジェクトにサービスアカウントで接続する場合：

```python
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# サービスアカウントキーで認証
credentials = service_account.Credentials.from_service_account_file(
    os.path.expanduser("~/.gcp/{SA_KEY_FILE}.json")
)

# BigQueryクライアント作成
client = bigquery.Client(
    project="{SA_PROJECT_ID}",
    credentials=credentials
)

# 接続テスト
datasets = list(client.list_datasets())
print(f"接続成功！{len(datasets)}個のデータセット")
```

## トラブルシューティング

| エラー | 原因 | 対処法 |
|--------|------|--------|
| File xxx was not found | GOOGLE_APPLICATION_CREDENTIALS が無効 | `unset GOOGLE_APPLICATION_CREDENTIALS` |
| Reauthentication needed | 認証期限切れ | 再度認証実行 |
| Permission denied | BigQuery権限なし | IAM設定を確認 |

## 重要な注意事項

### 環境変数の競合

`GOOGLE_APPLICATION_CREDENTIALS` 環境変数が設定されている場合、ADCより優先されます。
Pythonコードで以下を実行して回避：

```python
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
```

### marimo notebook使用時

`.cursor/rules/notebook.mdc` のルールに従い：
1. 作業開始前に「どのGCPプロジェクトで作業しますか？」と確認
2. `gcloud config configurations list` でプロファイル一覧を表示
3. 必要に応じてプロファイルを切り替え

## Requirements

- Google Cloud SDK (`gcloud`) インストール済み
- ブラウザでGoogleアカウントにログイン可能
- 対象プロジェクトへのBigQuery閲覧権限
