---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
duration: "約30分"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["agent", "command", "cursor"]
---

# 🎓 Lesson 6-1: カスタムCommand作成基本

## 📍 このセッションでやること

**Lesson 6-1: カスタムCommand作成基本** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Cursorでカスタムコマンド（.cursor/commands/）を作成し、チームで再利用できるようにする |
| 所要時間 | 約30分 |
| 使うスキル | Cursor Commands, Markdown（YAML frontmatter） |
| 前提条件 | Cursor 利用中、ai-agent-camp を開いている |
| 教材ページ | [Module 6: エージェント開発](https://ai-agent.camp/ja/course/module-6) を並行参照 |

**このセッションの流れ:**
1. コマンドディレクトリ構造の確認
2. シンプルなコマンド作成（project-info, env-check, run-tests）
3. 動作確認

セッション終了時には、自分用・チーム用のコマンドが使えるようになっています。

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

## 🚀 Step 1: コマンドディレクトリ構造の確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: コマンドディレクトリ構造の確認",
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
ai-agent-camp プロジェクトのコマンドディレクトリ構造を確認してください。

以下のディレクトリが存在するか確認：
- .cursor/commands/
- .cursor/commands/lesson/
- .cursor/commands/utility/

存在しない場合は作成してください。
```

**期待される結果**: コマンドディレクトリの構造が確認・作成されます。

---

## 🚀 Step 2: シンプルなコマンド作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: シンプルなコマンド作成",
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
````text
.cursor/commands/project-info.md ファイルを作成し、以下の内容を記述してください：

---
description: "プロジェクト情報を表示"
---

# プロジェクト情報

## 概要
このプロジェクトはAIエージェント開発のベースプラットフォームです。

## ディレクトリ構成
```
ai-agent-camp/
├── .claude/         # Claude Code設定
│   └── skills/      # 再利用可能スキル
├── .cursor/         # Cursor IDE設定
│   └── commands/    # カスタムコマンド
│   └── commands/    # Cursor用カスタムコマンド
├── skills/          # 共通スキルの正本
├── course/          # HTMLコース教材
└── tools/           # Pythonスクリプト
```

## 技術スタック
- AI Framework: Claude 3.5 Sonnet
- Protocol: MCP（Model Context Protocol）
- IDE: Cursor / Claude Code
````

**期待される結果**: `/project-info` コマンドが作成されます。

---

## 🚀 Step 3: 環境チェックコマンド

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 環境チェックコマンド",
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
````text
.cursor/commands/env-check.md ファイルを作成し、以下の内容を記述してください：

---
description: "開発環境の状態をチェック"
---

# 環境チェック

開発環境の状態を確認するコマンドです。

## チェック項目

以下のコマンドを実行して環境を確認してください：

### 1. Node.js バージョン確認
```bash
node --version
```
期待値: v18.x 以上

### 2. Python バージョン確認
```bash
python3 --version    # Windowsでは python --version
```
期待値: Python 3.9 以上

### 3. Git 設定確認
```bash
git config user.name
git config user.email
```

### 4. npm パッケージ確認
```bash
npm list -g --depth=0
```

### 5. pip パッケージ確認
```bash
pip list | head -20
```

## トラブルシューティング
問題がある場合は `/start-0-1` でセットアップを確認してください。
````

**期待される結果**: `/env-check` コマンドが作成されます。

---

## 🚀 Step 4: テスト実行コマンド

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: テスト実行コマンド",
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
````text
.cursor/commands/run-tests.md ファイルを作成し、以下の内容を記述してください：

---
description: "プロジェクトのテストを実行"
---

# テスト実行

プロジェクトのテストを実行するコマンドです。

## Python テスト

### 全テスト実行
```bash
pytest tests/ -v
```

### カバレッジ付きテスト
```bash
pytest tests/ -v --cov=src/ --cov-report=term-missing
```

### 特定のテストファイル実行
```bash
pytest tests/test_specific.py -v
```

## JavaScript テスト（Node.js）

### npm テスト
```bash
npm test
```

### 特定のテストファイル
```bash
npx jest tests/specific.test.js
```

## テスト結果の解釈

- ✅ PASSED: テスト成功
- ❌ FAILED: テスト失敗（エラー内容を確認）
- ⚠️ SKIPPED: スキップされたテスト
- 📊 Coverage: カバレッジ率（目標: 80%以上）
````

**期待される結果**: `/run-tests` コマンドが作成されます。

---

## 🚀 Step 5: コマンドの動作確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: コマンドの動作確認",
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
作成したコマンドの一覧と動作を確認してください：

1. .cursor/commands/ ディレクトリ内のファイルを一覧表示
2. 各コマンドファイルの description を抽出
3. コマンドの命名規則が統一されているか確認

作成されたコマンド：
- /project-info
- /env-check
- /run-tests

それぞれのコマンドが Cursor で認識されるか確認してください。
```

**期待される結果**: 作成したコマンドが正しく認識されていることを確認できます。

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
      {"id": "trouble_1", "label": "コマンドが認識されない"},
      {"id": "trouble_2", "label": "descriptionが表示されない"},
      {"id": "trouble_3", "label": "コマンド内のコードが実行されない"},
      {"id": "trouble_4", "label": "日本語が文字化けする"}
    ]
  }]
}
```


### トラブル1: コマンドが認識されない
**原因**: ファイルパスが間違っている、またはMarkdown形式が不正
**解決プロンプト**:
```text
以下を確認してください：
1. ファイルが .cursor/commands/ ディレクトリにあるか
2. ファイル拡張子が .md か
3. フロントマター（---で囲まれた部分）の形式が正しいか
```

### トラブル2: descriptionが表示されない
**原因**: YAMLフロントマターの構文エラー
**解決プロンプト**:
```text
フロントマターの形式を確認してください：
---
description: "説明文"
---

注意: コロンの後にスペースが必要です。
```

### トラブル3: コマンド内のコードが実行されない
**原因**: コマンドは指示書であり、自動実行されない
**解決プロンプト**:
```text
Cursorコマンドは「テンプレート」として機能します。
コマンド内のコードブロックは、ユーザーがコピー&ペーストするか、
AIに「このコマンドを実行して」と指示する必要があります。
```

### トラブル4: 日本語が文字化けする
**原因**: ファイルエンコーディングがUTF-8でない
**解決プロンプト**:
```text
ファイルがUTF-8で保存されているか確認してください。
Cursorの設定でデフォルトエンコーディングをUTF-8に設定してください。
```

---

## ✅ チェックポイント
- [ ] .cursor/commands/ ディレクトリが存在する
- [ ] project-info.md が作成されている
- [ ] env-check.md が作成されている
- [ ] run-tests.md が作成されている
- [ ] コマンドがCursorで認識される


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── {プロジェクト名}/  (エージェント/コード成果物)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/{プロジェクト名}/

# 冒頭を確認（最初の30行）
head -30 output/{プロジェクト名}/
```

> 💡 全文を確認: `cat output/{プロジェクト名}/` で全文表示できます

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-6-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-6-2
- finish → 終了
