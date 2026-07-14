---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "約10分"
prerequisites: []
level: "beginner"
tags: ["setup", "tool-selection", "cursor", "claude-code", "codex"]
nonInteractiveMode: deferred
---
# Lesson 0-8: ツール選択ガイド

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Cursor / Claude Code / Codex の特徴を理解し、自分に合ったツールを選ぶ |
| 所要時間 | 約10分 |
| 前提条件 | なし（最初に受講可能） |
| 教材ページ | （本レッスンは前提条件なし。セットアップは選択後の各レッスンで案内します） |

> **ヒント**: どのツールを選んでも、本コースの全レッスンを受講できます。迷ったらまず Cursor から始めるのがおすすめです。

---

## 判断フローチャート

以下のフローチャートで、自分に合ったツールを見つけましょう。

```mermaid
flowchart TD
    A[AIコーディングツールを選びたい] --> B{GUI が好き？}
    B -->|はい| C[Cursor がおすすめ]
    B -->|いいえ| D{CLI に慣れている？}
    D -->|いいえ| C
    D -->|はい| E{どのAIエコシステムを使いたい？}
    E -->|Anthropic / Claude| F[Claude Code がおすすめ]
    E -->|OpenAI / GPT| G[Codex がおすすめ]
    E -->|どちらでも / わからない| F

    C --> H[/start-0-1 へ進む]
    F --> I[/start-0-7 へ進む]
    G --> J[/start-0-6 へ進む]
```

---

## ツール比較表

| 項目 | Cursor | Claude Code | Codex |
|------|--------|------------|-------|
| インターフェース | GUI (VS Code ベース) | CLI | CLI |
| AI モデル | Claude / GPT / Gemini | Claude | GPT |
| 料金体系 | Pro $20/月, Pro+ $60/月, Ultra $200/月 | Pro $20/月, Max $100/月 or API従量課金 | Pro $10/月, Pro+ $39/月, Business $19/ユーザー月 |
| 学習コスト | 低い（VS Code ベース） | 中程度 | 中程度 |
| 強み | 視覚的、拡張機能豊富 | コンテキスト理解、自律実行 | サンドボックス、安全性 |
| 本コースとの相性 | ★★★ 最もスムーズ | ★★★ フル対応 | ★★☆ スキル経由 |

> ※ 料金は変更される可能性があります。各公式サイトで最新情報をご確認ください。

---

## ユースケース別おすすめ

### 初心者・非エンジニアの方

**Cursor** をおすすめします。

- VS Code ベースの使い慣れた GUI で操作できる
- ファイルツリーやエディタが視覚的にわかりやすい
- 拡張機能が豊富で、必要な機能を簡単に追加できる
- 本コースのコマンド（`/start-X-X`）がそのまま使える

### ターミナル作業が多い方

**Claude Code** をおすすめします。

- ターミナルから直接 AI に指示を出せる
- プロジェクト全体のコンテキストを自動で把握する
- 自律的にファイルを読み書きし、コマンドを実行する
- CLAUDE.md でプロジェクトルールを定義できる

### セキュリティを重視する方

**Codex** をおすすめします。

- サンドボックス環境でコードを安全に実行する
- ネットワークアクセスを制限した状態で動作可能
- OpenAI のセキュリティ基盤を活用できる

### 複数ツールの併用

複数ツールの併用も可能です。例えば：

- **Cursor + Claude Code**: GUI で確認しながら CLI で自律実行
- **Cursor + Codex**: GUI メインで、安全な実行が必要な場面で Codex を使用

---

## 各ツールのセットアップへの導線

**AskQuestionの設定:**
```json
{
  "title": "ツールを選択してセットアップへ進む",
  "questions": [{
    "id": "tool_choice",
    "prompt": "どのツールでコースを始めますか？",
    "options": [
      {"id": "cursor", "label": "Cursor（GUI・初心者おすすめ）→ /start-0-1 へ"},
      {"id": "claude_code", "label": "Claude Code（CLI・自律実行）→ /start-0-7 へ"},
      {"id": "codex", "label": "Codex（CLI・サンドボックス）→ /start-0-6 へ"},
      {"id": "more_info", "label": "もう少し詳しく知りたい"}
    ]
  }]
}
```

(cursor → /start-0-1 を案内)
(claude_code → /start-0-7 を案内)
(codex → /start-0-6 を案内)
(more_info → 上記の比較表とユースケースを再表示)

---

## 実行コマンド

```text
/start-0-8
```

このレッスンはツール選択のガイドです。以下の AskQuestion で選択肢を提示し、回答に応じてセットアップレッスンへ誘導します。

**AskQuestionの設定:**
```json
{
  "title": "ツール選択ガイドを開始",
  "questions": [{
    "id": "start_action",
    "prompt": "ツール選択ガイドを始めます。何をしますか？",
    "options": [
      {"id": "compare", "label": "3つのツールを比較する"},
      {"id": "flowchart", "label": "フローチャートで診断する"},
      {"id": "already_decided", "label": "既に使うツールを決めている"}
    ]
  }]
}
```

(compare → ツール比較表とユースケースを表示)
(flowchart → 判断フローチャートを表示)
(already_decided → 各ツールのセットアップへの導線セクションへ)

---

## 期待される出力例

```text
ツール選択ガイド

あなたの回答に基づくおすすめ:
  → Cursor（GUI・初心者おすすめ）

次のステップ: /start-0-1 を実行してセットアップを始めましょう
```

---

## よくあるトラブル

- どのツールを選べばいいかわからない → フローチャートに沿って回答するか、迷ったら Cursor を選択
- 途中でツールを変更したくなった → いつでも別のセットアップレッスン（/start-0-1, /start-0-7, /start-0-6）を実行可能
- AIの応答が止まる → 「続きを表示して」と入力

---

## チェックポイント

- [ ] 3つのツール（Cursor / Claude Code / Codex）の違いを理解した
- [ ] 自分に合ったツールを選んだ
- [ ] 選んだツールのセットアップレッスンへ進む準備ができた

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "ツール選択ガイドを確認しました。次に何をしますか？",
    "options": [
      {"id": "cursor_setup", "label": "Cursor のセットアップを始める（/start-0-1）"},
      {"id": "claude_setup", "label": "Claude Code のセットアップを始める（/start-0-7）"},
      {"id": "codex_setup", "label": "Codex のセットアップを始める（/start-0-6）"},
      {"id": "overview", "label": "コース全体を確認する（/overview）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(cursor_setup → /start-0-1 を案内)
(claude_setup → /start-0-7 を案内)
(codex_setup → /start-0-6 を案内)
(overview → /overview を案内)
(finish → 「お疲れさまでした。いつでもセットアップレッスンを始められます」と表示)
