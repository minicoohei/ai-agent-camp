---
description: "When the user says /start-7-4 — Module 7 Lesson 7-4: 5つの設計パターン（スキル設計の応用）"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-3"]
duration: "約20分"
level: "advanced"
tags: ["agent", "design-patterns", "architecture"]
---

# 🎓 Lesson 7-4: 5つの設計パターン

## 📍 このセッションでやること

**Lesson 7-4: 5つの設計パターン** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | スキル設計の5つのパターンを学び、議事録スキルに Iterative Refinement パターンを適用する |
| 所要時間 | 約20分 |
| 使うスキル | meeting-notes-summarizer（Lesson 7-2, 7-3で作成・改善済み） |
| 前提条件 | Lesson 7-3 完了（テスト・改善済みスキル） |
| 教材ページ | [Module 7: Skill/Commands](https://ai-agent.camp/ja/course/module-7) を並行参照 |

**このセッションの流れ:**
1. Sequential Workflow パターン
2. Multi-MCP Coordination パターン
3. Iterative Refinement パターン
4. Context-aware Tool Selection パターン
5. Domain-specific Intelligence パターン
6. 議事録スキルへの Iterative Refinement 適用（実践演習）

セッション終了時には、5つの設計パターンを理解し、議事録スキルに Iterative Refinement パターンを実際に適用できています。

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
(check_prereq → 前提条件の確認を実行: Lesson 7-3 完了済みか、meeting-notes-summarizer スキルが `skills/meeting-notes-summarizer/` に存在するか確認)
(view_html → 教材ページURL https://ai-agent.camp/ja/course/module-7 を案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Sequential Workflow パターン（順次処理）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Sequential Workflow パターン（順次処理）",
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

**概念**: タスクを定義された順序で実行し、各ステップの出力が次のステップの入力になるパターンです。
処理が直線的で予測可能なため、デバッグしやすく、各ステップを独立してテストできます。

**議事録スキルでの適用例:**
テキスト受取 → 参加者抽出 → 議題特定 → 決定事項整理 → アクション項目抽出 → Markdown出力

入力内容:
```
Sequential Workflow パターンを議事録スキルに適用した場合の処理フローを設計してください。

各ステップの入力・出力を明確にし、前のステップの出力が次のステップの入力になることを示してください：
1. テキスト受取・前処理
2. 参加者抽出
3. 議題・トピック特定
4. 決定事項の整理
5. アクション項目抽出（担当者・期限付き）
6. Markdown議事録の生成
```

**期待される結果**: 6ステップの処理フローが設計され、各ステップの入力・出力が明確に定義される。

---

## 🚀 Step 2: Multi-MCP Coordination パターン（複数ツール連携）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Multi-MCP Coordination パターン（複数ツール連携）",
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

**概念**: 複数のツールやスキルを連携させて、単独では実現できない複雑なタスクを達成するパターンです。
各ツールの強みを活かし、データの受け渡しとエラーハンドリングを設計することが重要です。

**議事録スキルでの適用例:**
Slack検索でチャンネルの会議ログを取得 → 議事録スキルで構造化 → Notion DBに保存

入力内容:
```
Multi-MCP Coordination パターンで、以下の3つのスキルを連携させる設計を考えてください：

1. slack-search（Slack検索） → 特定チャンネルの会議ログを取得
2. meeting-notes-summarizer（議事録生成） → ログを構造化された議事録に変換
3. notion-db（Notion連携） → 議事録をNotionデータベースに保存

各スキル間のデータの受け渡し方法と、エラー発生時のフォールバック処理を設計してください。
```

**期待される結果**: 3つのスキルの連携フローが設計され、スキル間のデータ形式・受け渡し方法・エラー時のフォールバックが明確になる。

---

## 🚀 Step 3: Iterative Refinement パターン（反復改善）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: Iterative Refinement パターン（反復改善）",
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

**概念**: ドラフト生成 → レビュー → 改善 → 再レビューのサイクルで品質を向上させるパターンです。
1回の生成で完璧を目指すのではなく、反復的に品質を高めていくアプローチです。

**議事録スキルでの適用例:**
初回ドラフト生成 → 自己レビュー（不足チェック） → 改善版生成 → 最終確認

入力内容:
```
Iterative Refinement パターンを議事録スキルに組み込む方法を設計してください：

1. 初回ドラフト: 入力テキストから議事録を生成
2. セルフレビュー: 以下の観点で自己チェック
   - 全参加者が含まれているか
   - アクション項目に担当者と期限があるか
   - 決定事項が明確か
3. 改善版: レビュー結果に基づいて議事録を修正
4. 最終確認: 改善前後の差分を表示

この仕組みを SKILL.md にどう記述するか、具体的なプロンプト構造を示してください。
```

**期待される結果**: Iterative Refinement の4ステップが設計され、SKILL.md への記述方法と具体的なプロンプト構造が明確になる。

---

## 🚀 Step 4: Context-aware Tool Selection パターン（文脈判断）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: Context-aware Tool Selection パターン（文脈判断）",
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

**概念**: 入力の文脈やコンテキストに応じて、異なる処理パスを選択するパターンです。
入力の種類を自動判定し、最適なハンドラーにルーティングします。

**議事録スキルでの適用例:**
入力形式の自動検出 → 適切なハンドラーへのルーティング

入力内容:
```
Context-aware Tool Selection パターンを議事録スキルに適用してください。

入力形式に応じて処理を分岐する設計：
- テキスト入力 → そのまま議事録化
- 音声文字起こしテキスト → ノイズ除去→議事録化
- チャットログ形式 → 発言者ごとの整理→議事録化
- 箇条書きメモ → 構造推定→議事録化

各分岐の判定条件と、分岐先の処理の違いを設計してください。
```

**期待される結果**: 4つの入力形式の判定条件が定義され、各形式に適した前処理フローが設計される。

---

## 🚀 Step 5: Domain-specific Intelligence パターン（専門知識埋込）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: Domain-specific Intelligence パターン（専門知識埋込）",
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

**概念**: ドメイン固有の専門知識をスキルに埋め込むことで、汎用的なAIでは実現できない精度と品質を達成するパターンです。
会議ドメインの知識（会議タイプ、テンプレート、用語）をスキルに組み込みます。

**議事録スキルでの適用例:**
会議タイプの自動判定 → タイプ別テンプレート選択 → 業界用語の解釈 → フォローアップ推奨

入力内容:
```
Domain-specific Intelligence パターンで、会議ドメインの専門知識を
議事録スキルに埋め込む方法を設計してください：

1. 会議タイプの自動判定（定例会議/ブレスト/レビュー/意思決定会議）
2. 各タイプに適した議事録テンプレートの選択
3. 業界用語・略語の解釈ルール
4. フォローアップアクションの推奨パターン

これを SKILL.md の references/ にどう配置するか、具体的なファイル構成を示してください。
```

**期待される結果**: 会議ドメインの専門知識の構造化と、references/ ディレクトリへの配置設計が完成する。

---

## 🚀 Step 6: 実践演習 — Iterative Refinement パターンの適用

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 6: 実践演習 — Iterative Refinement パターンの適用",
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

Step 3 で設計した Iterative Refinement パターンを、実際に meeting-notes-summarizer の SKILL.md に組み込みます。
これまでの設計を実装に落とし込む実践演習です。

入力内容:
```
Lesson 7-2 で作成した meeting-notes-summarizer の SKILL.md を修正し、
Iterative Refinement パターンを組み込んでください。

具体的な変更点：
1. ワークフローに「セルフレビュー」ステップを追加
2. レビューチェックリスト（5項目以上）を追加
3. 改善ループの条件（いつ改善を止めるか）を定義
4. 修正前後の diff を表示して変更点を確認

変更後、サンプルデータで動作確認してください。
```

**期待される結果**: meeting-notes-summarizer の SKILL.md に Iterative Refinement パターンが組み込まれ、セルフレビュー・改善ループが機能することを確認できる。

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
      {"id": "trouble_1", "label": "パターンの違いが理解できない"},
      {"id": "trouble_2", "label": "複数パターンの組み合わせが分からない"},
      {"id": "trouble_3", "label": "SKILL.md の修正でスキルが壊れた"},
      {"id": "trouble_4", "label": "Iterative Refinement で無限ループになる"}
    ]
  }]
}
```

### トラブル1: パターンの違いが理解できない
**原因**: 5つのパターンの概念が似ているように感じるケース
**解決プロンプト**:
```
各パターンを1行で要約した比較表を作成してください：

| パターン | 一言で言うと | 議事録スキルでの例 |
|----------|-------------|-------------------|
| Sequential Workflow | 順番に処理する | テキスト→抽出→整理→出力 |
| Multi-MCP Coordination | 複数ツールを連携させる | Slack→議事録→Notion |
| Iterative Refinement | 繰り返し改善する | ドラフト→レビュー→修正 |
| Context-aware Tool Selection | 入力に応じて分岐する | 形式判定→適切な処理 |
| Domain-specific Intelligence | 専門知識を埋め込む | 会議タイプ別テンプレート |
```

### トラブル2: 複数パターンの組み合わせが分からない
**原因**: パターンの組み合わせ方法が不明確
**解決プロンプト**:
```
Sequential Workflow + Iterative Refinement の組み合わせ例を示してください。

例: Sequential Workflow の各ステップ内で Iterative Refinement を適用する
1. テキスト受取・前処理
2. 参加者抽出 → セルフレビュー → 改善
3. 議題特定 → セルフレビュー → 改善
4. 決定事項整理 → セルフレビュー → 改善
5. アクション項目抽出 → セルフレビュー → 改善
6. Markdown出力

各ステップでの改善ポイントを具体的に説明してください。
```

### トラブル3: SKILL.md の修正でスキルが壊れた
**原因**: SKILL.md の構文エラーや必須セクションの欠落
**解決プロンプト**:
```
以下の手順で復旧してください：
1. git diff で変更箇所を確認
   git diff skills/meeting-notes-summarizer/SKILL.md
2. 問題がある場合は変更を元に戻す
   cp skills/meeting-notes-summarizer/SKILL.md.backup skills/meeting-notes-summarizer/SKILL.md
3. 修正を再度、慎重に適用する
```

### トラブル4: Iterative Refinement で無限ループになる
**原因**: 改善ループの終了条件が定義されていない
**解決プロンプト**:
```
改善ループを最大2回に制限してください。SKILL.md に以下を追加します：

## 改善ループの制限
- 最大改善回数: 2回
- 終了条件: 以下のいずれかを満たした場合
  1. レビューチェックリストの全項目がOK
  2. 改善回数が2回に達した
  3. 前回と改善内容に変化がない
- 2回改善しても問題が残る場合は、残課題リストとして出力に付記する
```

---

## ✅ チェックポイント
- [ ] Sequential Workflow パターンの処理フローを理解した
- [ ] Multi-MCP Coordination の連携設計ができた
- [ ] Iterative Refinement のレビュー・改善サイクルを理解した
- [ ] Context-aware Tool Selection の分岐設計ができた
- [ ] Domain-specific Intelligence の専門知識埋込を理解した
- [ ] 議事録スキルに Iterative Refinement パターンを実際に適用した
- [ ] 修正後のスキルが正しく動作することを確認した


---

## 📋 成果物プレビュー

### 期待される出力
```
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

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これはスキルマスターシリーズの最終レッスンです。おめでとうございます！

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "back_to_module", "label": "Module 7 の他のレッスンに戻る"},
      {"id": "course_top", "label": "ホームに戻る（コーストップを開く）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- back_to_module → Module 7 のレッスン一覧を表示（/start-7-1 〜 /start-7-8）
- course_top → ブラウザで https://ai-agent.camp/ja/course を開く
- finish → 終了
