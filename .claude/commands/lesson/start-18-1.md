---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "25分"
category: "lesson"
prerequisites: []
level: "intermediate"
tags: ["pm", "interview", "customer-needs"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-1: 顧客インタビュー & ニーズ収集

## 📍 このセッションでやること

**Lesson 18-1: 顧客インタビュー & ニーズ収集** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | AIが顧客役になりインタビューシミュレーション。ペルソナ定義、ニーズ抽出を行う |
| 所要時間 | 約25分 |
| 使うスキル | pm-toolkit スキル, 選択肢付きの対話フロー |
| 前提条件 | ai-agent-camp を開いている |
| 教材ページ | [Module 18: PM & システム要件定義](https://ai-agent.camp/ja/course/module-18) を並行参照 |

**このセッションの流れ:**
1. TaskFlowプロジェクトの概要を確認
2. AIとの顧客インタビューシミュレーション
3. インタビュー結果の構造化（ペルソナ、ニーズ、ペインポイント）
4. customer-needs.md の生成・レビュー

セッション終了時には、TaskFlowの顧客ニーズ分析ドキュメントが完成しています。

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

## 🚀 Step 1: TaskFlowプロジェクトの紹介

まず、このモジュール全体を通して作る「TaskFlow」の概要を確認しましょう。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: TaskFlow プロジェクト概要",
  "questions": [{
    "id": "taskflow_intro",
    "prompt": "TaskFlowについて確認しましょう。どこから始めますか？",
    "options": [
      {"id": "overview", "label": "TaskFlowの概要を教えて"},
      {"id": "skip", "label": "概要は知っている、インタビューに進む"},
      {"id": "context", "label": "このモジュール全体の流れを知りたい"}
    ]
  }]
}
```

**TaskFlow とは:**
```text
TaskFlow は中小企業向けのタスク管理Webアプリケーションです。

【コンセプト】
- チーム全員の「今日やること」が一目でわかる
- AIが優先度を提案し、タスクの見落としを防ぐ
- シンプルだが、成長企業に必要な機能を備える

【想定ターゲット】
- 社員数10～100名の企業
- 現在Excel/スプレッドシートでタスク管理している
- 既存ツール（Trello, Asana等）は高機能すぎて使いこなせない

このモジュールでは、TaskFlowの「企画 → 設計 → 実装 → テスト → 運用」を
全20レッスンで体験します。
```

**期待される結果**: TaskFlowの概要が理解できます。

---

## 🚀 Step 2: 顧客インタビューの準備

AIが顧客役になってインタビューシミュレーションを行います。まずインタビュー対象を選びましょう。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: インタビュー対象の選択",
  "questions": [
    {
      "id": "persona_type",
      "prompt": "インタビューする顧客タイプを選んでください（AIがその役を演じます）",
      "options": [
        {"id": "pm", "label": "プロジェクトマネージャー（35歳、IT企業）"},
        {"id": "sales_mgr", "label": "営業部長（42歳、製造業）"},
        {"id": "startup_ceo", "label": "スタートアップCEO（29歳、SaaS企業）"},
        {"id": "hr", "label": "人事担当（31歳、コンサル会社）"}
      ]
    },
    {
      "id": "interview_style",
      "prompt": "インタビュー形式を選んでください",
      "options": [
        {"id": "structured", "label": "構造化インタビュー（質問リスト準備済み）"},
        {"id": "semi", "label": "半構造化（テーマだけ決めて自由に）"},
        {"id": "guided", "label": "ガイド付き（AIが質問を提案してくれる）"}
      ]
    }
  ]
}
```

**選択後**: 選んだペルソナとインタビュー形式でシミュレーションを開始します。

---

## 🚀 Step 3: インタビューシミュレーション実行

AIが選択した顧客役として応答します。以下のテーマで質問していきましょう。

**インタビューガイド:**
```text
以下のテーマで顧客（AI）にインタビューしてください:

1. 【現状把握】今のタスク管理方法は？何を使っている？
2. 【課題】一番困っていることは？具体的なエピソードは？
3. 【理想像】どうなったら嬉しい？理想の状態は？
4. 【優先度】最も改善したい点を3つ挙げるなら？
5. 【制約】予算感、導入時期、必須条件は？

AIは選択したペルソナとして、リアルな回答をします。
5～10往復のやり取りを行ってください。
```

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: インタビュー進行",
  "questions": [{
    "id": "interview_status",
    "prompt": "インタビューの進捗はどうですか？",
    "options": [
      {"id": "continue", "label": "まだ質問がある、続ける"},
      {"id": "enough", "label": "十分聞けた、整理に進む"},
      {"id": "help", "label": "何を聞けばいいかわからない"},
      {"id": "restart", "label": "別のペルソナで最初からやり直す"}
    ]
  }]
}
```

(continue → インタビュー続行)
(enough → Step 4へ)
(help → 質問例を提示)
(restart → Step 2に戻る)

**期待される結果**: 5～10往復のインタビューが完了します。

---

## 🚀 Step 4: インタビュー結果の構造化

インタビュー内容を分析し、ドキュメントにまとめます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 結果の整理方法",
  "questions": [{
    "id": "output_format",
    "prompt": "アウトプットの形式を選んでください",
    "options": [
      {"id": "full", "label": "フル分析（ペルソナ + ニーズ + ペインポイント + 機会）"},
      {"id": "persona_focus", "label": "ペルソナ定義を中心に"},
      {"id": "needs_focus", "label": "ニーズ一覧を中心に"},
      {"id": "auto", "label": "AIにお任せ"}
    ]
  }]
}
```

**生成するドキュメント:**
```text
以下の内容で output/pm/customer-needs.md を生成してください:

# 顧客ニーズ分析: TaskFlow

## 1. インタビュー概要
- 対象: {ペルソナ情報}
- 実施日: {今日の日付}
- 形式: {選択した形式}

## 2. ペルソナ定義
### プライマリペルソナ
- 名前（仮名）:
- 年齢:
- 職種:
- 会社規模:
- ITリテラシー:
- 現在の課題:

## 3. 発見したニーズ（優先度順）
| # | ニーズ | 種別 | 優先度 | 根拠（発言） |
|---|--------|------|--------|------------|

## 4. ペインポイント
1.
2.
3.

## 5. 機会（Opportunities）
-

## 6. 次のステップへの示唆
- 要求資料に反映すべきポイント
- PRDで深堀りすべきテーマ

mkdir -p output/pm && ファイルを output/pm/customer-needs.md に保存
```

**期待される結果**: `output/pm/customer-needs.md` が生成されます。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "AIの顧客役が不自然な回答をする"},
      {"id": "trouble_2", "label": "インタビューで何を聞けばいいかわからない"},
      {"id": "trouble_3", "label": "ニーズの整理方法がわからない"},
      {"id": "trouble_4", "label": "出力ファイルが生成されない"}
    ]
  }]
}
```

### トラブル1: AIの顧客役が不自然
**解決策**: 「もっとリアルに、具体的なエピソードを交えて答えてください」と指示すると改善します。「予算は月1万円まで」のような具体的な制約を追加しても良いです。

### トラブル2: 何を聞けばいいかわからない
**解決策**: Step 3のインタビューガイド（5つのテーマ）に沿って質問してください。各テーマで2問ずつ聞けば十分です。

### トラブル3: ニーズの整理方法がわからない
**解決策**: 「インタビュー内容をもとに、ニーズを優先度順に整理してください」とAIに指示すれば自動整理されます。

### トラブル4: 出力ファイルが生成されない
**解決策**: `output/pm/` ディレクトリが存在するか確認してください。なければ `mkdir -p output/pm` で作成します。

---

## ✅ チェックポイント
- [ ] TaskFlowプロジェクトの概要を理解した
- [ ] AIとの顧客インタビューを5往復以上実施した
- [ ] ペルソナが1人以上定義されている
- [ ] ニーズが3つ以上抽出されている
- [ ] ペインポイントが明確になっている
- [ ] `output/pm/customer-needs.md` が生成されている


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── stakeholder-map.md  (ステークホルダーマップ)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/stakeholder-map.md

# 冒頭を確認（最初の30行）
head -30 output/pm/stakeholder-map.md
```

> 💡 全文を確認: `cat output/pm/stakeholder-map.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```text
output/pm/customer-needs.md の内容を確認し、ペルソナ定義・ニーズ一覧・ペインポイントが
すべて埋まっているかチェックしてください。
```

**期待される結果**: ドキュメントの完成度が確認されます。

---

## ➡️ 次のステップ

これでLesson 18-1は完了です。次はインタビュー結果をもとに要求資料を作成します。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のレッスン（要求資料作成）を開始"},
      {"id": "next_window", "label": "新しいウィンドウで /start-18-2 を開始"},
      {"id": "review", "label": "もう一度顧客ニーズを見直す"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

- next_auto → /start-18-2 を実行
- next_window → 新しいウィンドウで /start-18-2
- review → customer-needs.md を再表示
- finish → 終了
