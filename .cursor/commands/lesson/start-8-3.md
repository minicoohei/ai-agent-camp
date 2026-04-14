---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2"]
duration: "約40分"
level: "intermediate"
tags: ["data", "marimo", "dashboard", "visualization"]
---

# 🎓 Lesson 8-3: Marimoノートブックで対話型分析

## 📍 このセッションでやること

**Lesson 8-3: Marimoで対話型ダッシュボード** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | MarimoでBigQueryデータのリアクティブなダッシュボードを構築する |
| 所要時間 | 約40分 |
| 使うスキル | data-analyst, Marimo |
| 前提条件 | Lesson 8-1・Lesson 8-2 完了、BigQuery接続済み |
| 教材ページ | [Module 8: データ分析](https://ai-agent.camp/ja/course/module-8) を並行参照 |

**このセッションの流れ:**
1. Marimo環境のセットアップ
2. BigQueryデータの読み込みと可視化
3. フィルタ・グラフの動的更新

セッション終了時には、対話型の分析ノートが作成できるようになっています。

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

## 🚀 Step 1: Marimoのインストールと起動

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Marimoのインストールと起動",
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
Marimoの環境をセットアップしてください。

1. Marimoがインストールされているか確認
2. 必要なパッケージ（altair, pandas）も確認
3. インストールされていなければインストール

インストール後、動作確認のためにバージョンを表示してください。
```

**期待される結果**: Marimoと関連パッケージがインストールされ、バージョンが表示されます。

---

## 🚀 Step 2: 新しいMarimoノートブックの作成

GA4分析用のノートブックを作成します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 新しいMarimoノートブックの作成",
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
GA4データ分析用のMarimoノートブックを作成してください。

ファイル: ~/ai-agent-camp/notebooks/ga4_analysis_dashboard.py

初期セルの内容:
1. ライブラリのインポート（marimo, pandas, altair, bigquery）
2. BigQueryクライアントの初期化
3. タイトルとダッシュボードの説明

Marimoを起動してブラウザで開く手順も教えてください。
```

**期待される結果**: ノートブックファイルが作成され、起動コマンドが案内されます。

---

## 🚀 Step 3: インタラクティブなUIコンポーネントの追加

フィルタ用のUIコンポーネントを追加します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: インタラクティブなUIコンポーネントの追加",
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
Marimoノートブックにインタラクティブなフィルタを追加してください。

追加するUIコンポーネント:
1. 日付範囲選択（開始日、終了日のテキストボックス）
2. イベント種別ドロップダウン（ALL, view_item, add_to_cart, purchase）
3. 表示件数スライダー（5〜50件）

各コンポーネントのコードを生成してください。
```

**期待される結果**: 各UIコンポーネントのMarimoコードが生成されます。

---

## 🚀 Step 4: リアクティブなデータ取得

UIコンポーネントの値に応じてデータを取得するセルを作成します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: リアクティブなデータ取得",
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
Marimoのキャッシュ機能を使って、
選択した日付範囲のGA4データを取得するセルを作成してください。

要件:
- @mo.cache デコレータでキャッシュを有効化
- 日付範囲（date_start, date_end）をパラメータとして受け取る
- 日別のイベント数、ユニークユーザー数を取得
- 結果をDataFrameで返す

コードを生成してください。
```

**期待される結果**: キャッシュ付きのデータ取得関数が生成されます。

---

## 🚀 Step 5: Altairでグラフを作成

データを可視化するグラフを追加します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: Altairでグラフを作成",
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
Altairを使って以下のグラフを作成するMarimoセルを生成してください。

1. 日別イベント数の折れ線グラフ
   - X軸: 日付
   - Y軸: イベント数
   - ツールチップ: 日付、イベント数、ユーザー数

2. イベント種別の棒グラフ
   - X軸: イベント数
   - Y軸: イベント名（降順）
   - 色: 割合に応じたグラデーション

各グラフをmo.ui.altair_chart()でラップしてください。
```

**期待される結果**: インタラクティブなAltairグラフのコードが生成されます。

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
      {"id": "trouble_1", "label": "Marimoが起動しない"},
      {"id": "trouble_2", "label": "セルが更新されない（リアクティビティの問題）"},
      {"id": "trouble_3", "label": "BigQueryクエリが遅い"},
      {"id": "trouble_4", "label": "グラフが表示されない"}
    ]
  }]
}
```


### トラブル1: 「Marimoが起動しない」
**原因**: インストールが不完全
**解決プロンプト**:
```
Marimoを再インストールしてください。
pip install --upgrade marimo

インストール後、marimo --version で確認してください。
```

### トラブル2: 「セルが更新されない（リアクティビティの問題）」
**原因**: 変数名の重複
**解決プロンプト**:
```
Marimoの変数命名ルールを教えてください。
セルごとに異なる接尾辞（_fetch, _prep, _dyn など）を
使う方法を説明してください。
```

### トラブル3: 「BigQueryクエリが遅い」
**原因**: キャッシュが効いていない
**解決プロンプト**:
```
Marimoの@mo.cacheデコレータの正しい使い方を教えてください。
キャッシュをクリアする方法も教えてください。
```

### トラブル4: 「グラフが表示されない」
**原因**: Altairのエンコーディングエラー
**解決プロンプト**:
```
Altairグラフが表示されないエラーを診断してください。
データフレームの型とグラフのエンコーディングが
一致しているか確認してください。
```

---

## ✅ チェックポイント
- [ ] Marimoが起動できた
- [ ] BigQueryクライアントが初期化できた
- [ ] 日付入力フィールドが動作した
- [ ] ドロップダウンフィルタが動作した
- [ ] スライダーが動作した
- [ ] キャッシュ機能（@mo.cache）が動作した
- [ ] Altairグラフが動的に更新された
- [ ] 複数のセルが連動して更新されることを確認した

---

## 📚 Marimoの重要な機能

### 変数命名ルール
| 目的 | 接尾辞 | 例 |
|------|------|----|
| データ取得 | `_fetch` | `df_daily_fetch` |
| 前処理 | `_prep` | `df_events_prep` |
| 動的フィルタ | `_dyn` | `chart_events_dyn` |
| 統計計算 | `_calc` | `total_events_calc` |

### よく使うUIコンポーネント
```python
mo.ui.text(...)       # テキスト入力
mo.ui.dropdown(...)   # ドロップダウン
mo.ui.slider(...)     # スライダー
mo.ui.table(...)      # テーブル表示
mo.ui.altair_chart()  # グラフ表示
```


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-8-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-8-4
- finish → 終了
