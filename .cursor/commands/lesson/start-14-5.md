---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "30分"
prerequisites: ["start-14-4"]
level: "intermediate"
tags: ["article", "proofreading"]
---

# 🎓 Lesson 14-5: 校閲 - 校閲エージェントによるレビュー

## 📍 このセッションでやること

**Lesson 14-5: 校閲 - 校閲エージェントによるレビュー** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 校閲エージェントで記事を5つの観点からレビューし、修正を反映する |
| 所要時間 | 約30分 |
| 使うスキル | proofreading-agent |
| 前提条件 | Gemini APIキー設定済み、Lesson 14-4（挿絵付きドラフト）完了済み |
| 教材ページ | [Module 14: 記事作成](https://ai-agent.camp/ja/course/module-14) を並行参照 |

**このセッションの流れ:**
1. 校閲の5つのSweep（観点）を理解する
2. proofreading-agentで全Sweepを実行する
3. レビュー結果を確認し、修正を反映する

セッション終了時には、5つの観点で校閲済みの記事ドラフトが完成しています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

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

## 🚀 Step 1: 校閲の5つのSweepを理解する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 校閲の5つの観点を理解する",
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
校閲エージェントが使う5つのSweep（レビュー観点）について教えてください。

1. 正確性 Sweep: 事実、データ、固有名詞の正確さ
2. 文法 Sweep: 文法、句読点、誤字脱字の検出
3. 一貫性 Sweep: 用語統一、表記揺れ、スタイルの一貫性
4. 読みやすさ Sweep: 文の長さ、構造の複雑さ、専門用語の使いすぎ
5. 構成 Sweep: 論理的な流れ、段落の長さ、導入と結論のバランス

各Sweepの具体的なチェック項目と、よくある指摘パターンを教えてください。
```

**期待される結果**: 5つのSweepの詳細なチェック項目と、よくある指摘例が説明されます。

---

## 🚀 Step 2: proofreading-agentで全Sweep実行

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 校閲を実行する",
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
proofreading-agentスキルを使って、記事ドラフトの校閲を実行してください。

実行コマンド:
python skills/proofreading-agent/scripts/proofreading_agent.py --input output/article-16-4-with-images.md --output output/article-16-5-review.json

対象ファイル: output/article-16-4-with-images.md

全5つのSweepを実行してください：
1. 正確性 Sweep
2. 文法 Sweep
3. 一貫性 Sweep
4. 読みやすさ Sweep
5. 構成 Sweep

各Sweepの結果を以下の形式で出力してください：
- 指摘箇所（行番号・該当テキスト）
- 問題の種類（Sweep名）
- 重要度（高/中/低）
- 修正提案

結果をoutput/article-16-5-review.jsonに保存してください。
```

**期待される結果**: 5つのSweepの校閲結果がJSON形式で出力され、全ての指摘事項がリスト化されます。

---

## 🚀 Step 3: レビュー結果の確認と修正反映

Codex では通常チャットで選択肢を提示しながらで修正の適用方法を選びます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 修正を反映する",
  "questions": [{
    "id": "apply_method",
    "prompt": "修正をどのように適用しますか？",
    "options": [
      {"id": "auto_all", "label": "全修正を自動適用する"},
      {"id": "one_by_one", "label": "1件ずつ確認して適用する"},
      {"id": "summary_only", "label": "サマリーだけ確認する"}
    ]
  }]
}
```

**「全修正を自動適用する」の場合:**
入力内容:
```text
output/article-16-5-review.jsonの指摘事項を全て記事に反映してください。

対象ファイル: output/article-16-4-with-images.md
修正済みファイル: output/article-16-5-proofread.md

修正内容のサマリーも出力してください：
- 修正件数（Sweep別）
- 重要度別の内訳
- 主な修正内容
```

**「1件ずつ確認して適用する」の場合:**
```text
output/article-16-5-review.jsonの指摘事項を重要度の高い順に1件ずつ表示し、
適用するかどうか確認させてください。
各指摘に対して「適用/スキップ/修正を変更」を選べるようにしてください。
```

**「サマリーだけ確認する」の場合:**
```text
output/article-16-5-review.jsonの校閲結果のサマリーを表示してください。
Sweep別の指摘件数と、重要度「高」の指摘のみ一覧表示してください。
```

**期待される結果**: 校閲の修正が記事に反映され、修正済みドラフトが保存されます。

---

## ⚠️ よくあるトラブルと解決方法

Codex では通常チャットで選択肢を提示しながらでトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "指摘が多すぎて対処しきれない"},
      {"id": "trouble_2", "label": "的外れな指摘がある"},
      {"id": "trouble_3", "label": "修正を適用したら文章が不自然になった"},
      {"id": "trouble_4", "label": "校閲結果ファイルが生成されない"}
    ]
  }]
}
```


### トラブル1: 「指摘が多すぎて対処しきれない」
**原因**: ドラフトの品質が低い、または校閲の基準が厳しすぎる
**解決プロンプト**:
```text
まず重要度「高」の指摘のみ対処してください。
重要度「中」「低」は次回のイテレーションで対応しましょう。
重要度「高」の指摘だけをフィルタして表示してください。
```

### トラブル2: 「的外れな指摘がある」
**原因**: 文脈を考慮しない機械的なチェック
**解決プロンプト**:
```text
的外れな指摘は無視して構いません。
「スキップ」を選んで次の指摘に進んでください。
意図的な表現（文体の特徴、修辞的な表現）は校閲の対象外です。
```

### トラブル3: 「修正を適用したら文章が不自然になった」
**原因**: 文脈を無視した局所的な修正
**解決プロンプト**:
```text
修正後の文章が不自然な場合は、前後の文脈を含めて再調整してください。
修正前の文章に戻すことも可能です：
output/article-16-4-with-images.md（修正前）を参照してください。
```

### トラブル4: 「校閲結果ファイルが生成されない」
**原因**: 入力ファイルが見つからない
**解決プロンプト**:
```bash
入力ファイルのパスを確認してください：
ls output/article-16-4-with-images.md
ファイルが存在しない場合は、Lesson 14-4（/start-14-4）を先に完了してください。
```

---

## ✅ チェックポイント
- [ ] 校閲の5つのSweep（正確性/文法/一貫性/読みやすさ/構成）を理解した
- [ ] proofreading-agentで全Sweepを実行できた
- [ ] レビュー結果を確認し、修正方針を決定した
- [ ] 修正を反映した校閲済みドラフトをoutput/に保存した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── article-14-5-*.md  (記事ドキュメント)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/article-14-5-*.md

# 冒頭を確認（最初の30行）
head -30 output/article-14-5-*.md
```

> 💡 全文を確認: `cat output/article-14-5-*.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

Codex では通常チャットで選択肢を提示しながらで選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-14-6）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-14-6
- finish → 終了
