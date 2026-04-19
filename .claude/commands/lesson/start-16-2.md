---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30分"
prerequisites: ["start-16-1"]
level: "beginner"
tags: ["email", "gmail", "check-inbox", "task-extraction"]
---

# 🎓 Lesson 16-2: 受信メール分析 & タスク抽出

## 📍 このセッションでやること

**Lesson 16-2: 受信メール分析 & タスク抽出** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | check-inbox スキルでメールからTODO抽出、優先度判定、返信ドラフト生成 |
| 所要時間 | 約30分 |
| 使うスキル | check-inbox |
| 前提条件 | Lesson 16-1 完了（gogcli認証済み）、Gemini APIキー設定済み |
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. check-inbox スキルの仕組みを理解する
2. メールデータの準備（google-sync 同期）
3. check-inbox でメール分析を実行
4. 優先度付きタスクリストと返信ドラフトを確認

セッション終了時には、受信メールからTODOを自動抽出し、優先度判定と返信ドラフトを生成できるようになっています。

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
      {"id": "previous_lesson", "label": "13-1 をまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: check-inbox の仕組みを理解する

check-inbox スキルは以下の流れで動作します:

```text
google-sync でメール同期 → Markdown ファイルとして保存
    ↓
check-inbox がローカルファイルを読み取り
    ↓
Gemini API で内容を分析
    ↓
優先度判定 + 返信ドラフト生成
```

**ポイント:**
- Gmail API をリアルタイムで叩くのではなく、事前同期したローカルデータを分析
- Gemini 3.0 Flash で高速に文脈を判定

---

## 🚀 Step 2: メールデータの準備

check-inbox はローカルの Markdown ファイルを読み取ります。

**データの有無を確認:**
```bash
ls output/gmail/ 2>/dev/null && echo "データあり" || echo "データなし"
```

データがない場合、gogcli で直接エクスポートします:

```bash
# 最新のメールを取得してMarkdown形式で保存
gog gmail search "is:inbox newer_than:7d" --account <your-email@gmail.com> --max 20 --format json
```

**AskQuestion:**
```json
{
  "title": "📋 メールデータの状態",
  "questions": [{
    "id": "data_status",
    "prompt": "メールデータはありますか？",
    "options": [
      {"id": "exists", "label": "output/gmail/ にデータがある → 次へ"},
      {"id": "export_needed", "label": "データがない → エクスポートを手伝って"},
      {"id": "use_sample", "label": "サンプルデータで試したい"}
    ]
  }]
}
```

---

## 🚀 Step 3: check-inbox でメール分析を実行

**Cursor / Claude Code で以下のプロンプトを実行:**

```text
受信箱をチェックして、返信が必要なメールをリストアップしてください。
優先度をつけて、返信ドラフトも作成してください。
```

または、`skills/check-inbox` スキルを直接呼び出す:

```text
/check-inbox
```

**期待される出力:**
- 返信が必要なメールの一覧（優先度付き）
- 各メールの要約
- 返信ドラフトの提案

---

## 🚀 Step 4: 結果の確認と活用

check-inbox の結果を確認し、実際の業務でどう活用するか検討します。

**AskQuestion:**
```json
{
  "title": "🔍 分析結果の活用",
  "questions": [{
    "id": "usage",
    "prompt": "分析結果をどう活用しますか？",
    "options": [
      {"id": "reply", "label": "返信ドラフトを使ってメール返信したい → 13-3 へ"},
      {"id": "review", "label": "タスクリストを確認・整理したい"},
      {"id": "retry", "label": "別のフィルタで再分析したい"},
      {"id": "next", "label": "次のレッスンに進みたい"}
    ]
  }]
}
```

---

## ⚠️ よくあるトラブルと解決方法

| トラブル | 解決策 |
|---------|--------|
| `GEMINI_API_KEY` エラー | `.env` に Gemini API キーを設定、または `/setup-gemini` を実行 |
| メールデータが見つからない | `output/gmail/` ディレクトリの存在を確認 |
| 分析結果が空 | メールデータの形式を確認（Markdown + YAML フロントマター） |

---

## ✅ チェックポイント

- [ ] check-inbox でメール分析が実行できた
- [ ] 優先度付きタスクリストが生成された
- [ ] 返信ドラフトが提案された


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/email/
├── index.html  (HTMLメール)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/email/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/email/index.html
```

> 💡 HTMLの構造確認: `head -30 output/email/index.html`

---

## ✅ 完了チェック

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-2 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_lesson", "label": "13-3 へ → gogcli でメール送信"},
      {"id": "practice", "label": "もう少し分析を試したい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```
