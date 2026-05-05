---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-0-1"]
duration: "約35分"
level: "intermediate"
tags: ["github-actions", "ci-cd", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-1: GitHub Actions Workflow基本・自動化

## 📍 このセッションでやること

**Lesson 11-1: GitHub Actions入門** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GitHub ActionsでCI/CDパイプラインを構築する（自動テスト・デプロイ） |
| 所要時間 | 約35分 |
| 使うスキル | GitHub Actions, YAML ワークフロー |
| 前提条件 | GitHub リポジトリ、Lesson 0-1（gh CLI）完了推奨 |
| 教材ページ | [Module 11: GitHub Actions](https://ai-agent.camp/ja/course/module-11) を並行参照 |

**このセッションの流れ:**
1. ワークフローディレクトリの作成
2. Hello Worldワークフロー
3. Python環境セットアップワークフロー
4. スケジュール実行ワークフロー
5. 複数ジョブのワークフロー

セッション終了時には、push時に自動でテストやデプロイが走るようになっています。

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

## 🚀 Step 1: ワークフローディレクトリの作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ワークフローディレクトリの作成",
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
```
ai-agent-camp プロジェクトに GitHub Actions のワークフローディレクトリを作成してください。

mkdir -p .github/workflows

ディレクトリが作成されたことを確認してください。
```

**期待される結果**: `.github/workflows/` ディレクトリが作成されます。

---

## 🚀 Step 2: Hello Worldワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Hello Worldワークフロー",
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
```
.github/workflows/hello.yml ファイルを作成し、以下の内容を記述してください：

name: Hello World

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest

    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"

      - name: Print Date
        run: date

      - name: Print Environment
        run: |
          echo "GitHub Actor: ${{ github.actor }}"
          echo "GitHub Repository: ${{ github.repository }}"
          echo "GitHub Event: ${{ github.event_name }}"
```

**期待される結果**: YAMLファイルが作成されます。GitHubにプッシュすると自動実行されます。

---

## 🚀 Step 3: Python環境セットアップワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: Python環境セットアップワークフロー",
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
```
.github/workflows/python-ci.yml ファイルを作成し、以下の内容を記述してください：

name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
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
          # uv は自動で最新のパッケージを管理します
          uv add pytest
          if [ -f pyproject.toml ]; then uv sync; fi

      - name: Run simple test
        run: |
          python -c "print('Python CI is working!')"
          python --version
```

**期待される結果**: Python環境のセットアップとテスト実行のワークフローが作成されます。

---

## 🚀 Step 4: スケジュール実行ワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: スケジュール実行ワークフロー",
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
```
.github/workflows/scheduled.yml ファイルを作成し、以下の内容を記述してください：

name: Scheduled Task

on:
  schedule:
    # 毎日 09:00 UTC（日本時間18:00）に実行
    - cron: '0 9 * * *'
  workflow_dispatch:
    inputs:
      task_name:
        description: 'タスク名'
        required: true
        default: 'daily_check'
        type: choice
        options:
          - daily_check
          - weekly_report

jobs:
  scheduled-task:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run scheduled task
        run: |
          echo "Running scheduled task at $(date)"
          echo "Task: ${{ github.event.inputs.task_name || 'daily_check' }}"

      - name: Check files
        run: |
          echo "Repository files:"
          ls -la
```

**期待される結果**: 定期実行と手動トリガー両方に対応したワークフローが作成されます。

---

## 🚀 Step 5: 複数ジョブのワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 複数ジョブのワークフロー",
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
```
.github/workflows/multi-job.yml ファイルを作成し、以下の内容を記述してください：

name: Multi-Job Workflow

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      build_status: ${{ steps.build.outputs.status }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

  test:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Test
        run: |
          echo "Build status: ${{ needs.build.outputs.build_status }}"
          echo "Running tests..."
          echo "Tests passed!"

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy
        run: |
          echo "Deploying to production..."
          echo "Deployment completed!"
```

**期待される結果**: build -> test -> deploy の順序で実行される複数ジョブワークフローが作成されます。

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
      {"id": "trouble_1", "label": "Workflow file invalid"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Command not found"},
      {"id": "trouble_4", "label": "スケジュール実行が動作しない"}
    ]
  }]
}
```


### トラブル1: 「Workflow file invalid」
**原因**: YAML構文エラー
**解決プロンプト**:
```
YAMLファイルの構文をチェックしてください。
インデントは2スペースで統一されているか確認してください。
コロンの後にスペースがあるか確認してください。
```

### トラブル2: 「Permission denied」
**原因**: スクリプトに実行権限がない
**解決プロンプト**:
```
ワークフロー内で chmod +x script.sh を実行するステップを追加してください。
```

### トラブル3: 「Command not found」
**原因**: 必要なプログラムがインストールされていない
**解決プロンプト**:
```
actions/setup-python や actions/setup-node などのセットアップアクションを追加してください。
必要なパッケージをインストールするステップを追加してください。
```

### トラブル4: スケジュール実行が動作しない
**原因**: Cronの設定ミス、またはデフォルトブランチで実行されていない
**解決プロンプト**:
```
cron式が正しいか確認してください（UTC時間で指定）。
ワークフローがデフォルトブランチ（main）に存在するか確認してください。
workflow_dispatch で手動実行して動作を確認してください。
```

---

## ✅ チェックポイント
- [ ] .github/workflows/ ディレクトリがある
- [ ] hello.yml が作成されている
- [ ] python-ci.yml が作成されている
- [ ] scheduled.yml が作成されている
- [ ] multi-job.yml が作成されている
- [ ] GitHubでワークフローが表示される


---

## 📋 成果物プレビュー

### 期待される出力
```
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

```
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-11-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-11-2
- finish → 終了
