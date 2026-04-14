---
description: "Lesson command"
duration: "約15分"
prerequisites: ["Googleアカウントを持っている", "ブラウザが使える"]
level: "beginner"
tags: ["setup", "bigquery", "gcp", "gcloud"]
---

# BigQuery / GCP 認証セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-bigquery` を実行して進捗を表示
2. gcloud CLI の既存インストールを自動検出:
   - `gcloud --version` を実行
   - gcloud CLI がインストール済み＆認証済みの場合、Step 4（接続テスト）へスキップ
   - 未インストールの場合、Step 1 から開始

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | gcloud CLI をインストールし、Application Default Credentials (ADC) で認証して、BigQuery でSQLクエリを実行できるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Googleアカウントを持っていること、ブラウザが使えること |
| 操作レベル | CLIコマンド少数 + ブラウザ認証（AIが手順を案内） |

**このセッションの流れ:**
1. gcloud CLI をインストールする（AIが手順を案内）
2. Googleアカウントでログインする（ブラウザが自動で開く）
3. GCPプロジェクトを設定する（AIが案内）
4. Application Default Credentials を設定する（コマンド1つ）
5. BigQuery 接続テスト（AIが自動実行）

> **料金について**: BigQuery は月1TBまでのクエリが無料です。研修では公開データセットを使うのでほぼ無料です。無料枠を超える前にGoogleから通知が届きます。
>
> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready -> Step 1へ)
(check_prereq -> 「Googleアカウントでブラウザにログインできれば準備OKです。BigQueryの料金は月1TBまで無料なので、研修での利用はほぼ無料です」と案内)
(different_lesson -> モジュール一覧を表示)

---

## Step 1: gcloud CLI のインストール

**AIが実行すること:**
1. OSを自動判定する（Mac / Windows / Linux）
2. `gcloud --version` を実行して既にインストール済みか確認する
3. インストール済みの場合は Step 2 へスキップ
4. 未インストールの場合、OS に応じたインストール手順を案内する

**Mac（Homebrew推奨）:**
```bash
brew install google-cloud-sdk
```

**Mac（Homebrew が使えない場合）/ Windows:**
ブラウザでインストーラーをダウンロード:
```bash
# Mac:
open https://cloud.google.com/sdk/docs/install
# Windows:
start https://cloud.google.com/sdk/docs/install
```

**インストール後の確認:**
```bash
gcloud --version
```

**AskQuestionの設定:**
```json
{
  "title": "Step 1: gcloud CLI のインストール",
  "questions": [{
    "id": "install_status",
    "prompt": "gcloud CLI のインストール状況を教えてください:",
    "options": [
      {"id": "installed", "label": "インストールしました（または既にインストール済み）"},
      {"id": "homebrew_issue", "label": "Homebrewが使えない（Mac）"},
      {"id": "windows_help", "label": "Windowsで手順がわからない"},
      {"id": "install_error", "label": "インストール中にエラーが出た"}
    ]
  }]
}
```

(installed -> `gcloud --version` で確認後、Step 2 へ)
(homebrew_issue -> 「ブラウザで https://cloud.google.com/sdk/docs/install を開いて、macOS用のインストーラーをダウンロードしてください。ダウンロードしたファイルを展開して、./install.sh を実行すればインストールできます」と案内)
(windows_help -> 「ブラウザで https://cloud.google.com/sdk/docs/install を開いて、Windows用のインストーラー（.exe）をダウンロードしてください。ダウンロードしたファイルをダブルクリックして、画面の指示に従ってインストールしてください。インストール後、新しいターミナル（コマンドプロンプト or PowerShell）を開いてください」と案内)
(install_error -> エラーメッセージを確認して原因を特定。PATH が通っていない場合は `source ~/.zshrc` や新しいターミナルを開くよう案内)

---

## Step 2: GCP プロジェクト設定

**AIが実行すること:**
1. `gcloud auth login` を実行してブラウザでGoogle認証を開始する
2. ブラウザが自動で開き、Googleアカウントでのログインを促す

```bash
gcloud auth login
```

**ブラウザ認証の手順をユーザーに案内:**

```text
ブラウザが自動で開きます。以下の手順で認証してください:

┌─────────────────────────────────────────────────────────────┐
│ 1. ブラウザでGoogleアカウントを選択してログイン             │
│ 2. 「Google Cloud SDK がアクセスをリクエストしています」    │
│    → 「許可」をクリック                                     │
│ 3. 「認証が完了しました」と表示されたらブラウザを閉じてOK   │
│ 4. ターミナルに戻ると認証成功のメッセージが表示されます     │
└─────────────────────────────────────────────────────────────┘
```

**認証完了後、プロジェクトを設定する:**
```bash
# 既存プロジェクト一覧を表示
gcloud projects list

# プロジェクトを設定（PROJECT_IDは実際のIDに置き換え）
gcloud config set project PROJECT_ID
```

**AskQuestionの設定:**
```json
{
  "title": "Step 2: GCP プロジェクト設定",
  "questions": [{
    "id": "auth_status",
    "prompt": "ブラウザでGoogleアカウント認証が完了しましたか？",
    "options": [
      {"id": "auth_done", "label": "認証が完了しました！"},
      {"id": "browser_not_open", "label": "ブラウザが開かない"},
      {"id": "auth_denied", "label": "認証画面でエラーが出た"},
      {"id": "no_project", "label": "GCPプロジェクトがない（新規作成したい）"}
    ]
  }]
}
```

(auth_done -> `gcloud projects list` でプロジェクト一覧を表示。既存プロジェクトがあれば `gcloud config set project PROJECT_ID` を案内して Step 3 へ)
(browser_not_open -> 「ターミナルに表示されたURLをコピーして、ブラウザのアドレスバーに貼り付けてください」と案内)
(auth_denied -> 「ブラウザのシークレットモード/プライベートブラウジングで試してみてください。会社のアカウントでブロックされている場合は、個人のGoogleアカウントで試してください」と案内)
(no_project -> 「GCPプロジェクトを新規作成しましょう。以下のコマンドを実行します: `gcloud projects create PROJECT_ID --name="プロジェクト名"` （PROJECT_IDは英数字とハイフンで任意の名前を設定できます。例: `my-bigquery-lab`）。または https://console.cloud.google.com で新規プロジェクトを作成することもできます」と案内)

---

## Step 3: Application Default Credentials (ADC) 設定

**AIが実行すること:**

1. ADC を設定するコマンドを実行:
```bash
gcloud auth application-default login
```

2. ブラウザが再度開き、ADC用の認証情報を作成する（Step 2 と同様にブラウザで認証）

**ユーザーに案内するメッセージ:**
```text
もう一度ブラウザが開きます。これはPythonなどのアプリケーションから
BigQueryに接続するための認証情報（ADC）を作成するためです。

┌─────────────────────────────────────────────────────────────┐
│ 1. ブラウザでGoogleアカウントを選択してログイン             │
│ 2. 「許可」をクリック                                       │
│ 3. ターミナルに「Credentials saved to file: ...」と          │
│    表示されれば成功です                                      │
└─────────────────────────────────────────────────────────────┘
```

3. ADC 設定完了後、BigQuery API を有効化する:
```bash
gcloud services enable bigquery.googleapis.com
```

**AskQuestionの設定:**
```json
{
  "title": "Step 3: ADC 設定",
  "questions": [{
    "id": "adc_status",
    "prompt": "ADC 認証とBigQuery API の有効化が完了しましたか？",
    "options": [
      {"id": "adc_done", "label": "「Credentials saved to file」と表示されました！"},
      {"id": "adc_browser_issue", "label": "ブラウザ認証がうまくいかない"},
      {"id": "api_enable_error", "label": "BigQuery API の有効化でエラーが出た"},
      {"id": "adc_what", "label": "ADCとは何ですか？"}
    ]
  }]
}
```

(adc_done -> Step 4 へ)
(adc_browser_issue -> 「Step 2 と同じ手順でブラウザ認証してください。うまくいかない場合はターミナルに表示されたURLをコピーしてブラウザに貼り付けてください」と案内)
(api_enable_error -> 「エラーメッセージを確認します。'permission denied' の場合、プロジェクトのオーナー権限が必要です。https://console.cloud.google.com/apis/library/bigquery.googleapis.com にアクセスして手動で有効化することもできます」と案内)
(adc_what -> 「ADC (Application Default Credentials) は、Pythonスクリプトなどのアプリケーションが自動的にGCPの認証情報を見つけるための仕組みです。一度設定すれば、コード内でAPIキーを指定する必要がなく、安全にBigQueryに接続できます」と説明)

---

## Step 4: BigQuery 接続テスト

**AIが自動で実行すること:**

1. 必要パッケージのインストール確認:
```bash
pip install google-cloud-bigquery
```

2. BigQuery 接続テストを実行:
```python
from google.cloud import bigquery

client = bigquery.Client()
query = "SELECT COUNT(*) as cnt FROM `bigquery-public-data.samples.shakespeare`"
result = client.query(query).result()
for row in result:
    print(f"接続成功！ Shakespeare dataset: {row.cnt} rows")
```

3. テスト結果に応じてAskQuestionを表示:

**テスト成功時:**
```text
BigQuery の接続テストが成功しました！

テスト結果: 公開データセット（Shakespeare）へのクエリが正常に実行されました。
これで BigQuery でのSQL実行、データ分析、EDA が使えるようになりました。
```

**テスト失敗時のAskQuestion:**
```json
{
  "title": "テスト結果: エラーが発生しました",
  "questions": [{
    "id": "test_error",
    "prompt": "BigQuery 接続テストでエラーが発生しました。考えられる原因を確認しましょう。",
    "options": [
      {"id": "retry", "label": "もう一度テストする"},
      {"id": "reauth", "label": "認証をやり直す（Step 2に戻る）"},
      {"id": "show_error", "label": "エラーの詳細を見たい"},
      {"id": "skip_test", "label": "テストをスキップして先に進む"}
    ]
  }]
}
```

(retry -> テストを再実行)
(reauth -> Step 2に戻る)
(show_error -> エラーメッセージを表示して原因と解決方法を案内)
(skip_test -> 「接続テストはスキップしました。後で /check-setup で確認できます」と案内)

---

## よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_install", "label": "gcloud CLI のインストールでエラーが出る"},
      {"id": "trouble_auth", "label": "ブラウザ認証が失敗する"},
      {"id": "trouble_project", "label": "GCPプロジェクトがない／選択できない"},
      {"id": "trouble_api", "label": "BigQuery API が有効化できない"},
      {"id": "trouble_permission", "label": "「permission denied」エラーが出る"},
      {"id": "trouble_package", "label": "google-cloud-bigquery パッケージのエラー"},
      {"id": "trouble_cost", "label": "料金が心配"},
      {"id": "trouble_other", "label": "その他のエラー"}
    ]
  }]
}
```

### トラブル1: gcloud CLI のインストールエラー
**原因**: Homebrew の問題、PATH が通っていない、権限不足
**AIが行うこと**:
1. `which gcloud` でインストール状況を確認
2. Homebrew でエラーの場合は `brew doctor` を実行して問題を特定
3. PATH が通っていない場合は `source ~/.zshrc` や新しいターミナルを開くよう案内
4. それでも解決しない場合はブラウザからの手動インストールを案内

### トラブル2: ブラウザ認証が失敗する
**原因**: ブラウザが開かない、会社のセキュリティポリシー、アカウント権限
**AIが行うこと**:
1. ターミナルに表示されたURLを手動でブラウザに貼り付けるよう案内
2. シークレットモードでの認証を提案
3. `gcloud auth login --no-launch-browser` でURL手動入力方式を案内

### トラブル3: GCPプロジェクトがない
**原因**: 初めてGCPを使う場合
**AIの案内**: 「`gcloud projects create my-bigquery-lab --name="BigQuery Lab"` でプロジェクトを作成できます。または https://console.cloud.google.com にアクセスして、画面上部の『プロジェクトを選択』> 『新しいプロジェクト』から作成できます」

### トラブル4: BigQuery API が有効化できない
**原因**: プロジェクトのオーナー権限がない、課金が有効になっていない
**AIが行うこと**:
1. `gcloud services enable bigquery.googleapis.com` を再実行
2. エラーメッセージを確認し、課金有効化が必要な場合は https://console.cloud.google.com/billing を案内
3. 権限問題の場合はプロジェクトオーナーに権限付与を依頼するよう案内

### トラブル5: 「permission denied」エラー
**原因**: ADC が正しく設定されていない、BigQuery API が無効、プロジェクト権限不足
**AIが行うこと**:
1. `gcloud auth application-default print-access-token` でADCの状態を確認
2. ADC が設定されていない場合は `gcloud auth application-default login` を再実行
3. `gcloud services list --enabled` でBigQuery APIが有効か確認

### トラブル6: google-cloud-bigquery パッケージのエラー
**原因**: パッケージ未インストール、バージョン不一致
**AIが行うこと**: `pip install google-cloud-bigquery` を自動実行。venv が壊れている場合は `bash tools/scripts/setup.sh` で再作成を案内

### トラブル7: 料金が心配
**AIの案内**: 「BigQueryは月1TBまでのクエリが無料です。研修で使う公開データセットへのアクセスも無料です。無料枠を超える前にGoogleから通知が届きます。研修レベルの利用であれば無料枠で十分です」

### トラブル8: その他のエラー
**AIが行うこと**: エラーメッセージの内容を確認し、原因を特定して解決方法を案内する

---

## チェックポイント
- [ ] gcloud CLI がインストールされている
- [ ] Googleアカウントで認証が完了している
- [ ] GCPプロジェクトが設定されている
- [ ] Application Default Credentials が設定されている
- [ ] BigQuery API が有効化されている
- [ ] BigQuery 接続テストが成功した

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "BigQuery / GCP 認証のセットアップが完了しました！次はどうしますか？",
    "options": [
      {"id": "try_bigquery", "label": "BigQuery接続と認証設定を学ぶ（/start-8-1）"},
      {"id": "try_eda", "label": "EDAを実行してみる（/start-8-2）"},
      {"id": "setup_other", "label": "他のセットアップに進む（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- try_bigquery -> /start-8-1 を案内
- try_eda -> /start-8-2 を案内
- setup_other -> /start-0-1 を案内
- finish -> 終了

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-bigquery` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/start-8-1` でBigQuery接続と認証設定を学びましょう」
