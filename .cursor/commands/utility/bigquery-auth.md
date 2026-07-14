---
nonInteractiveMode: incompatible
---

# BigQuery Auth - プロジェクト単位のBigQuery認証

このコマンドは、Cursor Browserを使用して、GCPプロジェクト単位でBigQuery認証を設定します。gcloud設定プロファイルを活用して複数プロジェクトを安全に管理します。

## 機能

- **プロジェクト分離**: gcloud設定プロファイルで複数GCPプロジェクトを安全に管理
- **ブラウザ認証**: Google Cloud Consoleでの認証をガイド
- **application-default credentials**: Python SDKから使用可能な認証情報を取得
- **環境変数対応**: 既存の`GOOGLE_APPLICATION_CREDENTIALS`との競合を回避

## 実行手順

### Phase 1: パラメータの確認

ユーザーの入力から以下の情報を確認してください：

1. **GCPプロジェクトID**（必須）:
   - 例: `my-project-123`, `my-gcp-project`

2. **プロファイル名**（任意、デフォルト: プロジェクトIDから自動生成）:
   - 例: `my-profile`, `my-dev`, `default`

3. **Googleアカウント**（任意、ユーザーが選択）

### Phase 2: 既存の設定プロファイル確認

```bash
gcloud config configurations list
```

既存のプロファイルを表示し、以下を確認：
- 目的のプロジェクト用プロファイルが既に存在するか
- 現在アクティブなプロファイルは何か

**ユーザーに案内:**
```
【既存の設定プロファイル一覧】
NAME     IS_ACTIVE  ACCOUNT                     PROJECT
default  True       user@example.com            my-project
...

目的のプロジェクト用プロファイルはありますか？
- 「新規作成」: 新しいプロファイルを作成
- 「{プロファイル名}」: 既存プロファイルを使用
```

### Phase 3: 設定プロファイルの作成（新規の場合）

```bash
# 新しいプロファイルを作成
gcloud config configurations create {PROFILE_NAME}

# プロジェクトIDを設定
gcloud config set project {PROJECT_ID}
```

### Phase 4: ブラウザ認証（Cursor Browser）

#### ステップ1: gcloud auth login

```bash
gcloud auth login
```

ブラウザが開いたら、`browser_snapshot`でページ状態を確認。

**ユーザーに案内:**
```
【Googleアカウント認証】
ブラウザが開きました。
1. 使用するGoogleアカウントを選択してください
2. 「Google Cloud SDK」へのアクセスを許可してください
3. 「このウィンドウは閉じてかまいません」と表示されれば完了

認証完了したら「完了」と入力してください。
```

#### ステップ2: application-default credentials

```bash
gcloud auth application-default login --quiet
```

再度ブラウザが開いたら認証を案内。

**ユーザーに案内:**
```
【Application Default Credentials認証】
ブラウザが開きました。
1. 同じGoogleアカウントを選択してください
2. 「Google Auth Library」へのアクセスを許可してください
3. 完了メッセージが表示されれば成功

認証完了したら「完了」と入力してください。
```

### Phase 5: 認証確認

```bash
# 認証状態確認
gcloud auth list

# プロジェクト確認
gcloud config get-value project

# ADCトークン確認（エラーにならなければOK）
gcloud auth application-default print-access-token 2>/dev/null && echo "✅ ADC認証OK" || echo "❌ ADC認証失敗"
```

### Phase 6: BigQuery接続テスト

```python
# 環境変数をクリアしてからテスト
import os
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

from google.cloud import bigquery
client = bigquery.Client(project="{PROJECT_ID}")
datasets = list(client.list_datasets())
print(f"接続成功！{len(datasets)}個のデータセットが見つかりました")
```

### Phase 7: 完了報告

**ユーザーに報告:**
```
【BigQuery認証完了】

✅ 設定プロファイル: {PROFILE_NAME}
✅ プロジェクト: {PROJECT_ID}
✅ アカウント: {ACCOUNT}
✅ BigQuery接続: 成功

📋 プロファイル切り替えコマンド:
   gcloud config configurations activate {PROFILE_NAME}

⚠️ 注意: 環境変数 GOOGLE_APPLICATION_CREDENTIALS が設定されている場合、
   Pythonコードで `del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]` を
   実行するか、unset してから使用してください。
```

## 使用例

### 基本的な使用
```
/bigquery-auth my-gcp-project
```

### プロファイル名を指定
```
/bigquery-auth my-dev-project --profile my-dev
```

### プロファイルの切り替え
```
/bigquery-auth --switch my-profile
```

## 利用可能なGCPプロファイル（参考）

| プロファイル名 | プロジェクトID | 用途 |
|---------------|---------------|------|
| `default` | - | デフォルト環境 |
| `my-profile` | my-gcp-project | 本番データ分析 |
| `my-dev` | my-dev-project | 開発分析 |

## トラブルシューティング

### エラー: "File xxx was not found"
- 環境変数 `GOOGLE_APPLICATION_CREDENTIALS` が無効なパスを指している
- 解決: `unset GOOGLE_APPLICATION_CREDENTIALS` または Pythonで削除

### エラー: "Reauthentication is needed"
- 認証期限切れ
- 解決: 再度 `/bigquery-auth {PROJECT_ID}` を実行

### エラー: "User does not have permission"
- BigQueryへのアクセス権限がない
- 解決: GCPコンソールでIAM権限を確認

## 注意事項

- **プロファイル切り替え忘れ防止**: 作業前に `gcloud config configurations list` で現在のプロファイルを確認
- **環境変数の競合**: `GOOGLE_APPLICATION_CREDENTIALS` が設定されている場合、ADCより優先される
- **marimo notebook使用時**: notebook.mdcのルールに従い、必ずGCP環境を確認してから作業開始
