---
description: "When the user says /start-8-2 — Module 8 Lesson 8-2: EDA（探索的データ分析）の実行"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1"]
duration: "約30分"
level: "intermediate"
tags: ["data", "bigquery", "eda", "analysis"]
---

# 🎓 Lesson 8-2: EDA（探索的データ分析）の実行

## 📍 このセッションでやること

**Lesson 8-2: BigQueryでEDA** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GA4サンプルデータで探索的データ分析（EDA）を行い、基本統計・欠損値・分布を把握する |
| 所要時間 | 約30分 |
| 使うスキル | data-analyst, BigQuery |
| 前提条件 | Lesson 8-1 完了、BigQuery接続済み |
| 教材ページ | [Module 8: データ分析](https://ai-agent.camp/ja/course/module-8) を並行参照 |

**このセッションの流れ:**
1. データセットの概要把握
2. 基本統計量・欠損値の確認
3. 分布の可視化

セッション終了時には、BigQueryデータの探索ができるようになっています。

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

## 🚀 Step 1: テーブルスキーマの確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: テーブルスキーマの確認",
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
BigQuery公開データセットのGA4テーブル構造を確認してください。

テーブル: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101

表示する情報:
- テーブルの行数
- カラム数
- 各カラムの名前、データ型、説明

主要なカラム（event_timestamp, event_name, user_pseudo_id,
geo.country, device.browser, ecommerce）について詳しく説明してください。
```

**期待される結果**: テーブルのスキーマ情報が整理されて表示されます。

---

## 🚀 Step 2: 基本統計量の計算

データの基本統計量を算出します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 基本統計量の計算",
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
GA4サンプルデータの基本統計量を計算してください。

期間: 2021-01-01 から 2021-01-03

計算する統計:
- 総イベント数
- ユニークユーザー数
- セッション数
- 最も一般的なイベント
- 最初と最後のイベント時刻

結果をわかりやすく表示してください。
```

**期待される結果**: 基本統計量がテーブル形式で表示されます。

---

## 🚀 Step 3: 欠損値の確認

データ品質をチェックするために欠損値を確認します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 欠損値の確認",
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
GA4データの欠損値を確認してください。

対象日: 2021-01-01

確認するカラム:
- user_pseudo_id
- event_name
- geo.country
- device.browser
- ecommerce.purchase_revenue

各カラムの欠損数と欠損率を計算し、
データ品質について考察してください。
```

**期待される結果**: 各カラムの欠損率と、データ品質に関する考察が表示されます。

---

## 🚀 Step 4: カテゴリカルデータの分布確認

イベントや地域の分布を確認します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: カテゴリカルデータの分布確認",
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
GA4データのカテゴリカル変数の分布を分析してください。

1. イベント種別の分布（TOP 15）
   - イベント名、件数、ユニークユーザー数、割合

2. 国別ユーザー分布（TOP 10）
   - 国名、イベント数、ユニークユーザー数、平均売上

3. ブラウザ種別の使用状況（TOP 10）
   - ブラウザ名、イベント数、割合

各分析結果をテーブル形式で表示してください。
```

**期待される結果**: 各カテゴリの分布が整理されたテーブルで表示されます。

---

## 🚀 Step 5: 時系列分析

日別・時間別のトレンドを分析します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 時系列分析",
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
GA4データの時系列分析を行ってください。

期間: 2021-01-01 から 2021-01-10

分析内容:
1. 日別集計
   - 日付、総イベント数、ユニークユーザー数、セッション数、売上

2. 時間帯別の傾向
   - 時間帯（0-23時）ごとのイベント数とユーザー数

結果を表示し、トレンドについて考察してください。
```

**期待される結果**: 時系列データと傾向の考察が表示されます。

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
      {"id": "trouble_1", "label": "クエリがタイムアウトする"},
      {"id": "trouble_2", "label": "Quota exceeded エラー"},
      {"id": "trouble_3", "label": "NULLの扱い方がわからない"},
      {"id": "trouble_4", "label": "ネストされたカラムにアクセスできない"}
    ]
  }]
}
```


### トラブル1: 「クエリがタイムアウトする」
**原因**: データ量が大きすぎる
**解決プロンプト**:
```text
クエリのパフォーマンスを改善してください。
以下の方法を検討:
- 日付範囲を絞る
- LIMIT句を追加
- サンプリングを使用
```

### トラブル2: 「Quota exceeded エラー」
**原因**: BigQueryのクォータを超過
**解決プロンプト**:
```text
BigQueryのクォータエラーが発生しました。
クエリコストを抑える方法を教えてください。
また、現在のクォータ使用状況を確認する方法も教えてください。
```

### トラブル3: 「NULLの扱い方がわからない」
**原因**: NULL値の集計方法が不明
**解決プロンプト**:
```text
BigQueryでNULL値を扱う方法を教えてください。
- COUNTIF でNULLをカウント
- COALESCE でNULLを置換
- NULLIF でNULLに変換
```

### トラブル4: 「ネストされたカラムにアクセスできない」
**原因**: STRUCT型やARRAY型の構文がわからない
**解決プロンプト**:
```text
BigQueryのネストされたカラム（STRUCT型）への
アクセス方法を教えてください。
例: geo.country, device.browser, ecommerce.purchase_revenue
```

---

## ✅ チェックポイント
- [ ] テーブルスキーマを確認できた
- [ ] 基本統計量を算出できた
- [ ] 欠損値を確認できた
- [ ] カテゴリカルデータの分布を確認できた
- [ ] 時系列データを分析できた
- [ ] eコマースデータの特徴を理解できた

---

## 📚 EDAでよく使うパターン

### 分布の確認
```sql
SELECT column_name, COUNT(*) as count
FROM table
GROUP BY column_name
ORDER BY count DESC
```

### 時系列トレンド
```sql
SELECT DATE(timestamp) as date, COUNT(*) as count
FROM table
GROUP BY date
ORDER BY date
```

### 相関分析の準備
```sql
SELECT column_a, column_b, COUNT(*) as count
FROM table
GROUP BY column_a, column_b
```


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```text
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-8-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-8-3
- finish → 終了
