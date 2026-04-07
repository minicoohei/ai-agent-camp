---
description: "When the user says /start-11-2 — Module 11 Lesson 11-2: GitHub Actions Secrets設定・Google連携"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-11-1"]
duration: "約35分"
level: "intermediate"
tags: ["github-actions", "secrets", "google-api"]
---

# 🎓 Lesson 11-2: GitHub Actions Secrets設定・Google連携

## 📍 このセッションでやること

**Lesson 11-2: GitHub ActionsとAPI連携** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub ActionsでSecretsを利用し、Google API連携の自動データ取得・処理パイプラインを構築する |
| 所要時間 | 約35分 |
| 使うスキル | GitHub Actions, Repository Secrets, Google API |
| 前提条件 | Lesson 11-1 完了、GitHub リポジトリ |
| 教材ページ | [Module 11: GitHub Actions](https://ai-agent.camp/ja/course/module-11) を並行参照 |

**このセッションの流れ:**
1. Repository Secretsの設定
2. ワークフローからAPIの呼び出し
3. 自動データ取得・処理の実行

セッション終了時には、Secretsを利用した安全なAPI連携パイプラインが動くようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 前提条件の確認を実行)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Repository Secretsの設定

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Repository Secretsの設定",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
GitHub Repository Secretsの設定手順を教えてください。
設定場所: リポジトリ > Settings > Secrets and variables > Actions
以下のSecretを設定する想定です：
- GOOGLE_CREDENTIALS（サービスアカウントキー）
- SLACK_WEBHOOK（通知用）
```

**期待される結果**: Secretsの設定手順が説明されます。実際の設定はGitHub Web UIで行います。

---

## 🚀 Step 2: Google認証ワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Google認証ワークフロー",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:

> **推奨**: 可能であれば Workload Identity Federation (OIDC) を優先してください。  
> サービスアカウントキーを使う場合は、JSON を1行に圧縮（minify）して Secrets に保存すると崩れにくくなります。

```yaml
.github/workflows/google-auth.yml ファイルを作成し、以下の内容を記述してください：

name: Google API Integration

on:
  workflow_dispatch:
    inputs:
      operation:
        description: '実行する操作'
        required: true
        default: 'test'
        type: choice
        options:
          - test
          - fetch_data
          - update_sheet

jobs:
  google-operation:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install google-auth google-auth-oauthlib google-api-python-client

      - name: Create credentials file
        run: |
          printf '%s' '${{ secrets.GOOGLE_CREDENTIALS }}' > credentials.json
          chmod 600 credentials.json

      - name: Test Google auth
        if: github.event.inputs.operation == 'test'
        run: |
          python -c "
          from google.oauth2 import service_account
          import json

          try:
              creds = service_account.Credentials.from_service_account_file('credentials.json')
              print('Google認証成功!')
              print(f'サービスアカウント: {creds.service_account_email}')
          except Exception as e:
              print(f'認証エラー: {e}')
              exit(1)
          "

      - name: Cleanup credentials
        if: always()
        run: rm -f credentials.json
```

**期待される結果**: Google認証を安全に行うワークフローが作成されます。

---

## 🚀 Step 3: データ取得パイプライン

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: データ取得パイプライン",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
.github/workflows/data-pipeline.yml ファイルを作成し、以下の内容を記述してください：

name: Data Pipeline

on:
  schedule:
    - cron: '0 1 * * *'  # 毎日 01:00 UTC
  workflow_dispatch:

jobs:
  data-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pandas requests

      - name: Step 1 - Fetch data
        run: |
          python -c "
          import json
          from datetime import datetime

          # サンプルデータ生成（実際はAPIから取得）
          data = {
              'timestamp': datetime.now().isoformat(),
              'records': [
                  {'id': 1, 'value': 100},
                  {'id': 2, 'value': 200},
                  {'id': 3, 'value': 300}
              ]
          }

          with open('data.json', 'w') as f:
              json.dump(data, f)

          print('データ取得完了')
          "

      - name: Step 2 - Process data
        run: |
          python -c "
          import json
          import pandas as pd

          with open('data.json', 'r') as f:
              data = json.load(f)

          df = pd.DataFrame(data['records'])
          df['processed_at'] = data['timestamp']

          summary = {
              'total_records': len(df),
              'sum_value': int(df['value'].sum()),
              'avg_value': float(df['value'].mean())
          }

          with open('summary.json', 'w') as f:
              json.dump(summary, f)

          print(f'処理完了: {summary}')
          "

      - name: Step 3 - Save results
        run: |
          mkdir -p output
          mv data.json output/
          mv summary.json output/
          echo "Results saved to output/"
          ls -la output/

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: pipeline-results-${{ github.run_number }}
          path: output/
          retention-days: 7
```

**期待される結果**: データ取得、処理、保存のパイプラインが作成されます。

---

## 🚀 Step 4: 通知付きワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 通知付きワークフロー",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
.github/workflows/notify.yml ファイルを作成し、以下の内容を記述してください：

name: Pipeline with Notification

on:
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build-and-notify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

      - name: Run tests
        id: test
        run: |
          echo "Running tests..."
          echo "Tests passed!"

      - name: Send success notification
        if: success()
        run: |
          echo "Sending success notification..."
          # Slack Webhookが設定されている場合
          # curl -X POST -H 'Content-type: application/json' \
          #   --data '{"text":"Pipeline成功: ${{ github.repository }}"}' \
          #   ${{ secrets.SLACK_WEBHOOK }}
          echo "Notification: Pipeline completed successfully!"

      - name: Send failure notification
        if: failure()
        run: |
          echo "Sending failure notification..."
          echo "Notification: Pipeline failed!"

      - name: Summary
        if: always()
        run: |
          echo "## Workflow Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Repository**: ${{ github.repository }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Branch**: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Actor**: ${{ github.actor }}" >> $GITHUB_STEP_SUMMARY
          echo "- **Status**: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**期待される結果**: ビルド完了後に通知を送信するワークフローが作成されます。

---

## 🚀 Step 5: マトリックスビルド

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: マトリックスビルド",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
.github/workflows/matrix.yml ファイルを作成し、以下の内容を記述してください：

name: Matrix Build

on:
  workflow_dispatch:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
      fail-fast: false

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: |
          python --version
          echo "OS: ${{ matrix.os }}"
          echo "Python: ${{ matrix.python-version }}"

      - name: Run tests
        run: |
          python -c "print('Test passed on ${{ matrix.os }} with Python ${{ matrix.python-version }}')"
```

**期待される結果**: 複数OS・複数Pythonバージョンで同時テストを行うワークフローが作成されます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "Invalid credentials"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Secretが参照できない"},
      {"id": "trouble_4", "label": "アーティファクトがアップロードされない"}
    ]
  }]
}
```


### トラブル1: 「Invalid credentials」
**原因**: Secret値が間違っている、またはJSON形式が不正
**解決プロンプト**:
```text
GOOGLE_CREDENTIALSのSecret値を確認してください。
JSONファイルの内容全体をコピーして設定してください。
改行や空白が正しく含まれているか確認してください。
```

### トラブル2: 「Permission denied」
**原因**: サービスアカウントの権限不足
**解決プロンプト**:
```text
Google Cloud Consoleでサービスアカウントの権限を確認してください。
必要なAPIが有効になっているか確認してください。
IAMロールが適切に設定されているか確認してください。
```

### トラブル3: Secretが参照できない
**原因**: Secret名のタイポ、またはSecretが設定されていない
**解決プロンプト**:
```text
GitHubリポジトリのSettings > Secrets and variables > ActionsでSecret名を確認してください。
secrets.SECRET_NAME の形式で参照しているか確認してください。
```

### トラブル4: アーティファクトがアップロードされない
**原因**: パスが存在しない、またはファイルサイズ超過
**解決プロンプト**:
```text
path で指定したディレクトリが存在するか確認してください。
ファイルサイズが制限（500MB）を超えていないか確認してください。
```

---

## ✅ チェックポイント
- [ ] Repository Secretsの設定手順を理解している
- [ ] google-auth.yml が作成されている
- [ ] data-pipeline.yml が作成されている
- [ ] notify.yml が作成されている
- [ ] matrix.yml が作成されている
- [ ] Secretを安全に扱う方法を理解している


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 .github/workflows/
└── {workflow}.yml  (GitHub Actionsワークフロー)
```

### 確認コマンド
```bash
# ワークフローファイルの一覧
ls -la .github/workflows/

# ファイル内容を確認
cat .github/workflows/{workflow}.yml

# GitHub上の実行状況を確認
gh run list --limit 5
```

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```text
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-1
- finish → 終了
