---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "約25分"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "claude-code", "codex", "ai", "automation", "code-review"]
---

# 🎓 Lesson 11-4: Claude Code / Codex / Cursor を GitHub Actions で呼ぶ

## 📍 このセッションでやること

**Lesson 11-4: AI CLI を GitHub Actions で呼ぶ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Claude Code CLI / Codex CLI を GitHub Actions ワークフロー内で実行し、コードレビューや PR 自動生成を行う |
| 所要時間 | 約25分 |
| 使うスキル | GitHub Actions, Claude Code CLI, Codex CLI, gh CLI |
| 前提条件 | Lesson 11-2 完了（Secrets 設定の理解） |

**このセッションの流れ:**
1. AI CLI ツールの概要と利用パターン
2. Claude Code をワークフローで実行
3. PR 自動レビューワークフローの作成
4. Codex CLI のワークフロー実行
5. 実践演習: Issue → AI 実装 → PR 自動作成パイプライン

セッション終了時には、AI CLI ツールを GitHub Actions で活用するワークフローが構築されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## 🎯 準備チェック

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
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 11-2 完了確認。API キーの準備状況確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: AI CLI ツールの概要

```json
{
  "title": "🚀 Step 1: AI CLI ツールの概要",
  "questions": [{
    "id": "step_action",
    "prompt": "GitHub Actions で使える AI CLI ツールの概要を確認します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "各ツールの違いを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

| ツール | コマンド | API キー | 主な用途 |
|--------|---------|---------|---------|
| Claude Code | `claude -p "prompt"` | `ANTHROPIC_API_KEY` | コードレビュー、実装、分析 |
| Codex CLI | `codex -q "prompt"` | `OPENAI_API_KEY` | コード生成、修正、質問応答 |

**GitHub Actions での共通パターン:**
```yaml
# API キーは必ず Secrets 経由で渡す
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Secrets に設定する API キー:**
- `ANTHROPIC_API_KEY`: Claude Code 用（Anthropic コンソールで取得）
- `OPENAI_API_KEY`: Codex 用（OpenAI コンソールで取得）

**期待される結果**: 各ツールの違いと必要な設定を理解する。

---

## 🚀 Step 2: Claude Code をワークフローで実行

```json
{
  "title": "🚀 Step 2: Claude Code ワークフロー",
  "questions": [{
    "id": "step_action",
    "prompt": "Claude Code CLI を GitHub Actions で実行するワークフローを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "claude CLI のオプションを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/claude-review.yml` を作成:

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      prompt:
        description: 'Claude に送るプロンプト'
        type: string
        default: 'このリポジトリのコード品質を分析してください'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Code review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
            PROMPT="以下の diff をレビューしてください。問題点、改善提案、良い点をまとめてください:\n\n$DIFF"
          else
            PROMPT="${{ inputs.prompt }}"
          fi
          claude -p "$PROMPT" --output-format text > review_result.txt

      - name: Post review comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review_result.txt', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## 🤖 Claude Code Review\n\n${review}`
            });
```

**ポイント:**
- `claude -p` でプロンプトを直接渡す（非対話モード）
- PR トリガーでは `git diff` を渡してレビュー
- `actions/github-script` でレビュー結果を PR コメントに投稿

**期待される結果**: PR 作成時に Claude Code が自動レビューし、コメントを投稿する。

---

## 🚀 Step 3: PR 自動レビューワークフロー

```json
{
  "title": "🚀 Step 3: PR 自動レビュー",
  "questions": [{
    "id": "step_action",
    "prompt": "PR の変更内容を分析し、構造化されたレビューコメントを投稿するワークフローを強化します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "レビュー観点を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

レビュープロンプトを強化:

```yaml
      - name: Run structured review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
          cat <<'PROMPT' > /tmp/review_prompt.txt
          以下の diff をレビューしてください。

          ## レビュー観点
          1. **バグリスク**: 潜在的なバグやエッジケース
          2. **セキュリティ**: 脆弱性やシークレットのハードコード
          3. **パフォーマンス**: 非効率な処理やN+1問題
          4. **可読性**: 命名、構造、コメントの適切さ
          5. **テスト**: テストカバレッジの不足

          ## 出力形式
          各観点について「✅ 問題なし」または「⚠️ 要確認: 具体的な指摘」で回答してください。

          ## Diff
          PROMPT
          echo "$DIFF" >> /tmp/review_prompt.txt
          claude -p "$(cat /tmp/review_prompt.txt)" --output-format text > review_result.txt
```

**期待される結果**: 構造化されたレビューコメントが PR に投稿される。

---

## 🚀 Step 4: Codex CLI のワークフロー実行

```json
{
  "title": "🚀 Step 4: Codex CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "Codex CLI を GitHub Actions で実行するワークフローを作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Codex CLI のオプションを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/codex-task.yml` を作成:

```yaml
name: Codex Task Runner
on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Codex に実行させるタスク'
        type: string
        required: true

jobs:
  codex-run:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Run Codex
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -q "${{ inputs.task }}" --approval-mode full-auto
          
      - name: Check for changes
        id: changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Create PR with changes
        if: steps.changes.outputs.has_changes == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCH="codex/auto-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          git add -A
          git commit -m "feat: Codex による自動実装 — ${{ inputs.task }}"
          git push origin "$BRANCH"
          gh pr create \
            --title "🤖 Codex: ${{ inputs.task }}" \
            --body "Codex CLI による自動実装です。\n\nタスク: ${{ inputs.task }}" \
            --base main
```

**ポイント:**
- `--approval-mode full-auto` で完全自動実行
- 変更があれば自動的に PR を作成
- `GITHUB_TOKEN` は GitHub が自動提供

**期待される結果**: `gh workflow run` でタスクを指定すると、Codex が実装して PR を作成する。

---

## 🚀 Step 5: 実践演習 — Issue → AI 実装 → PR パイプライン

```json
{
  "title": "🚀 Step 5: 実践演習",
  "questions": [{
    "id": "step_action",
    "prompt": "Issue が作成されたら AI が自動実装して PR を作成するパイプラインを構築します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Issue トリガーの仕組みを確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`.github/workflows/ai-implement.yml` を作成:

```yaml
name: AI Auto-Implement
on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: contains(github.event.issue.labels.*.name, 'ai-implement')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Implement from issue
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          TITLE="${{ github.event.issue.title }}"
          BODY="${{ github.event.issue.body }}"
          claude -p "以下の Issue を実装してください:\n\nタイトル: $TITLE\n\n内容:\n$BODY" \
            --output-format text > implementation_log.txt

      - name: Create PR
        if: ${{ success() }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            BRANCH="ai/issue-${{ github.event.issue.number }}"
            git checkout -b "$BRANCH"
            git add -A
            git commit -m "feat: #${{ github.event.issue.number }} の AI 実装"
            git push origin "$BRANCH"
            gh pr create \
              --title "🤖 AI実装: ${{ github.event.issue.title }}" \
              --body "Closes #${{ github.event.issue.number }}\n\nClaude Code による自動実装です。" \
              --base main
          fi
```

**テスト手順:**
1. Issue を作成（例: 「README に Contributing セクションを追加」）
2. `ai-implement` ラベルを付与
3. ワークフローが自動実行 → PR が作成される

**期待される結果**: ラベル付き Issue から自動的に PR が生成される。

---

## ⚠️ よくあるトラブルと解決方法

```json
{
  "title": "⚠️ トラブルシューティング",
  "questions": [{
    "id": "trouble",
    "prompt": "問題が発生しましたか？",
    "options": [
      {"id": "trouble_1", "label": "API キーのエラー"},
      {"id": "trouble_2", "label": "claude / codex コマンドが見つからない"},
      {"id": "trouble_3", "label": "PR 作成の権限エラー"},
      {"id": "trouble_4", "label": "レビューコメントが投稿されない"}
    ]
  }]
}
```

### トラブル1: 「API キーのエラー」
**原因**: Secrets に API キーが設定されていない、またはキーが無効。
**解決プロンプト**:
```text
GitHub リポジトリの Settings → Secrets and variables → Actions で ANTHROPIC_API_KEY が設定されているか確認してください。キーは sk-ant- で始まる文字列です。
```

### トラブル2: 「claude / codex コマンドが見つからない」
**原因**: npm install が失敗している。
**解決プロンプト**:
```text
ワークフローのログで npm install ステップのエラーを確認してください。Node.js バージョンが 18 以上であることを確認してください。
```

### トラブル3: 「PR 作成の権限エラー」
**原因**: `permissions` の設定が不足。
**解決プロンプト**:
```text
ワークフローの permissions に contents: write と pull-requests: write が含まれているか確認してください。リポジトリの Settings → Actions → General → Workflow permissions で「Read and write permissions」が有効か確認してください。
```

### トラブル4: 「レビューコメントが投稿されない」
**原因**: `actions/github-script` のスクリプトにエラーがある、または pull-requests: write 権限がない。
**解決プロンプト**:
```text
ワークフローのログで actions/github-script ステップのエラーを確認してください。review_result.txt が空の場合はClaude Codeの実行結果を確認してください。
```

---

## ✅ チェックポイント

- [ ] Claude Code CLI がワークフロー内で実行できる
- [ ] PR トリガーでレビューコメントが投稿される
- [ ] Codex CLI がワークフロー内で実行できる
- [ ] Issue → AI 実装 → PR のパイプラインが動作する
- [ ] API キーが Secrets に安全に保存されている

---

## 📋 成果物プレビュー

**作成されるワークフロー:**
```text
.github/workflows/
├── claude-review.yml      # PR 自動レビュー
├── codex-task.yml         # Codex タスク実行
└── ai-implement.yml       # Issue → AI 実装 → PR
```

---

## ➡️ 次のステップ

```json
{
  "title": "➡️ 次のステップ",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_auto", "label": "Lesson 11-5（デプロイ・ファイル生成）に進む → /start-11-5"},
      {"id": "review_module", "label": "このレッスンの成果物を確認したい"},
      {"id": "finish", "label": "今日はここまで"}
    ]
  }]
}
```
