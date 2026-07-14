---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-6-2"]
duration: "約20分"
level: "intermediate"
tags: ["agent", "skill-design", "best-practices"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-1: スキル設計の基礎

## 📍 このセッションでやること

**Lesson 7-1: スキル設計の基礎** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Anthropicのスキル設計ベストプラクティスを理解し、議事録スキルのユースケース定義書を作成する |
| 所要時間 | 約20分 |
| 使うスキル | なし（設計・概念理解のレッスン） |
| 前提条件 | Lesson 6-2 完了推奨（Skills基礎の知識） |
| 教材ページ | [Module 7: Skill/Commands](https://ai-agent.camp/ja/course/module-7) を並行参照 |

**このセッションの流れ:**
1. スキルの3カテゴリを理解する
2. Progressive Disclosure（段階的情報開示）を学ぶ
3. 議事録スキルのユースケースを定義する
4. 成功基準を設定する

セッション終了時には、議事録スキル（meeting-notes-summarizer）のユースケース定義書が完成しています。

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

## 🚀 Step 1: スキルの3カテゴリを理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: スキルの3カテゴリを理解する",
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

Anthropicのスキルガイドでは3つのカテゴリが定義されています：

1. **Document Creation** — ドキュメント生成・編集（例: 議事録、レポート、契約書）
2. **Workflow Automation** — 繰り返し作業の自動化（例: コードレビュー、デプロイ、テスト）
3. **MCP Enhancement** — MCPサーバーの拡張（例: API連携、データ取得、外部サービス統合）

入力内容:
```text
スキルの3カテゴリ（Document Creation / Workflow Automation / MCP Enhancement）について、
それぞれの特徴と具体例を説明してください。
私たちが作る「議事録スキル」はどのカテゴリに該当しますか？
```

**期待される結果**: 3カテゴリの理解と、議事録スキルが「Document Creation」に該当することの確認。

---

## 🚀 Step 2: Progressive Disclosure を学ぶ

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Progressive Disclosure を学ぶ",
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

スキルは3段階で情報を開示します：

1. **メタデータ**（name + description）— 常にコンテキスト内（約100語）
2. **SKILL.md 本文** — トリガー時に読み込み（5,000語以下推奨）
3. **バンドルリソース**（scripts/, references/）— 必要時のみ読み込み

入力内容:
```text
Progressive Disclosure（段階的情報開示）の3段階について、
議事録スキルの場合を例に具体的に説明してください：

- 第1段階（メタデータ）: どんな name と description を設定するか
- 第2段階（SKILL.md本文）: どんな手順・ガイドラインを記述するか
- 第3段階（バンドルリソース）: scripts/ や references/ に何を配置するか

各段階のトークンコストも意識して、簡潔に設計してください。
```

**期待される結果**: 3段階の具体的な内容設計と、各段階のコンテキストウィンドウへの影響の理解。

---

## 🚀 Step 3: 議事録スキルのユースケースを定義する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 議事録スキルのユースケースを定義する",
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

ユースケース定義には以下を含めます：
- スキル名とカテゴリ
- トリガーフレーズ（いつ発動するか）
- 入力と出力
- 既存スキルとの差別化

入力内容:
```text
「議事録まとめスキル（meeting-notes-summarizer）」のユースケース定義書を作成してください。

以下の項目を含めてください：

## ユースケース定義書

| 項目 | 内容 |
|------|------|
| スキル名 | meeting-notes-summarizer |
| カテゴリ | Document Creation |
| 目的 | 会議テキスト/メモから構造化された議事録を自動生成 |

### トリガーフレーズ（いつ発動するか）
- 正しく発動すべきフレーズ: 5個以上
- 発動すべきでないフレーズ: 3個以上

### 入力仕様
- 入力形式（テキスト、ファイル等）
- 必須情報と任意情報

### 出力仕様
- 出力形式（Markdown）
- 必須セクション（参加者、議題、決定事項、アクション項目、次回予定）

### 既存スキルとの差別化
- check-inbox、slack-search、document-processor との違い
```

**期待される結果**: ユースケース定義書が完成し、スキルの全体像が明確になる。

---

## 🚀 Step 4: 成功基準を設定する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 成功基準を設定する",
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

定量・定性の両面から成功基準を設定します。

入力内容:
```text
議事録スキル（meeting-notes-summarizer）の成功基準を定義してください。

### 定量メトリクス
- トリガー精度（正しく発動する率 / 誤発動しない率）
- 出力完全性（必須セクションの充足率）
- 処理速度（レスポンスタイム）

### 定性メトリクス
- 出力の読みやすさ
- アクション項目の具体性
- 参加者の正確な特定

### テストケース
- 最小テスト: 3人の短い会議（5分）のメモ
- 標準テスト: 10人の定例会議（60分）の議事録
- 最大テスト: 英語混在の長時間ワークショップのメモ
```

**期待される結果**: 定量・定性の成功基準とテストケースが定義される。

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
      {"id": "trouble_1", "label": "カテゴリの分類が分からない"},
      {"id": "trouble_2", "label": "トリガーフレーズが思いつかない"},
      {"id": "trouble_3", "label": "既存スキルとの違いが不明確"},
      {"id": "trouble_4", "label": "成功基準が抽象的すぎる"}
    ]
  }]
}
```

### トラブル1: カテゴリの分類が分からない
**原因**: スキルが複数のカテゴリにまたがるケース
**解決プロンプト**:
```text
このスキルの主要な目的は何ですか？最も重要な機能に基づいて1つのカテゴリを選んでください。
複数カテゴリの要素がある場合、メインカテゴリを1つ決めてサブカテゴリとして注記します。
```

### トラブル2: トリガーフレーズが思いつかない
**原因**: ユーザーの使用シーンが不明確
**解決プロンプト**:
```text
このスキルを使いたいシーンを5つ想像してください。
各シーンでユーザーが最初にAIに言いそうな言葉がトリガーフレーズです。
```

### トラブル3: 既存スキルとの違いが不明確
**原因**: 機能の重複範囲が曖昧
**解決プロンプト**:
```text
既存スキル（check-inbox, slack-search, document-processor）の
SKILL.md を読み、それぞれの「目的」と「出力形式」を比較してください。
```

### トラブル4: 成功基準が抽象的すぎる
**原因**: 具体的な数値目標がない
**解決プロンプト**:
```text
「良い議事録」を10点満点で採点するなら、各項目に何点配分しますか？
その配点が成功基準の優先度になります。
```

---

## ✅ チェックポイント
- [ ] スキルの3カテゴリ（Document Creation / Workflow Automation / MCP Enhancement）を理解した
- [ ] Progressive Disclosure の3段階を理解した
- [ ] 議事録スキルのユースケース定義書を作成した
- [ ] トリガーフレーズ（正・誤）を定義した
- [ ] 定量・定性の成功基準を設定した
- [ ] テストケースを3種定義した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 skills/{skill_name}/
├── SKILL.md  (スキル定義)
├── scripts/    (実行スクリプト)
└── tests/      (テストファイル)
```

### 確認コマンド
```bash
# スキルのディレクトリ構造を確認
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# SKILL.md の冒頭を確認
head -30 skills/{skill_name}/SKILL.md
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-7-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-7-2
- finish → 終了
