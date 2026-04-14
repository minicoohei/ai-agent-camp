---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2", "start-8-3"]
duration: "約35分"
level: "intermediate"
tags: ["data", "visualization", "dashboard", "matplotlib"]
---

# 🎓 Lesson 8-4: データ可視化とダッシュボード作成

## 📍 このセッションでやること

**Lesson 8-4: 可視化とダッシュボード** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | matplotlib / seaborn でグラフを作成し、ダッシュボードを構築する |
| 所要時間 | 約35分 |
| 使うスキル | data-analyst, 可視化ライブラリ |
| 前提条件 | Lesson 8-1〜Lesson 8-3 完了、BigQuery接続済み |
| 教材ページ | [Module 8: データ分析](https://ai-agent.camp/ja/course/module-8) を並行参照 |

**このセッションの流れ:**
1. 各種グラフの作成
2. 複数グラフの組み合わせ
3. ダッシュボードの完成とレポート出力

セッション終了時には、分析レポートやダッシュボードが作成できるようになっています。

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

## 🔧 Step 0: 環境準備（日本語フォント設定 & データ準備）

グラフで日本語を正しく表示するため、最初にフォントを設定します。以下のコードをスクリプトの冒頭に追加してください：

```python
import matplotlib
import matplotlib.pyplot as plt

# 日本語フォント設定（OS を自動検出）
import platform
_system = platform.system()
if _system == "Darwin":
    matplotlib.rcParams['font.family'] = 'Hiragino Sans'
elif _system == "Windows":
    matplotlib.rcParams['font.family'] = 'MS Gothic'
else:
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
```

### BigQuery に接続できない場合のフォールバック

GCP認証がうまくいかない場合でも、サンプルデータを使ってレッスンを進められます。以下のようにローカルの DataFrame を作成してください：

```python
import pandas as pd

# Shakespeare風サンプルデータ（BigQuery不要）
sample_data = pd.DataFrame({
    'corpus': ['hamlet', 'macbeth', 'othello', 'kinglear', 'tempest',
               'juliuscaesar', 'romeoand', 'midsummer', 'merchantof', 'twelfthnight'],
    'unique_words': [4828, 3896, 3885, 3766, 3309, 3032, 3000, 2930, 2892, 2780],
    'total_words': [32446, 18314, 27602, 27619, 17780, 20876, 25689, 17121, 22152, 20890]
})

# 時系列サンプルデータ（GA4風）
import numpy as np
dates = pd.date_range('2021-01-01', periods=10, freq='D')
sample_timeseries = pd.DataFrame({
    'date': dates,
    'event_count': np.random.randint(500, 2000, size=10)
})
```

> **💡 ヒント**: BigQuery接続済みの方はそのままクエリを実行してください。接続できない方は上記サンプルデータで代替できます。

---

## 🚀 Step 1: 基本的な棒グラフの作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 基本的な棒グラフの作成",
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
BigQueryのShakespeareデータセットを使って、
作品別のユニーク単語数を横棒グラフで可視化してください。

クエリ:
SELECT corpus, COUNT(DISTINCT word) as unique_words
FROM bigquery-public-data.samples.shakespeare
GROUP BY corpus
ORDER BY unique_words DESC
LIMIT 10

グラフの要件:
- 横棒グラフ（barh）
- タイトル: 「Shakespeare作品別のユニーク単語数」
- X軸ラベル: 「ユニーク単語数」
- 高解像度（dpi=150）で保存

出力先: ~/ai-agent-camp/output/chart-4-4-bar.png
```

**期待される結果**: 横棒グラフが生成され、ファイルに保存されます。

---

## 🚀 Step 2: 時系列データの折れ線グラフ

時系列トレンドを可視化します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 時系列データの折れ線グラフ",
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
GA4データの日別イベント数を折れ線グラフで可視化してください。

期間: 2021-01-01 から 2021-01-10

グラフの要件:
- 折れ線グラフ（line）+ マーカー
- X軸: 日付
- Y軸: イベント数
- グリッド線を追加
- タイトル: 「日別イベント数推移」
- 高解像度（dpi=150）で保存

出力先: ~/ai-agent-camp/output/chart-4-4-line.png
```

**期待される結果**: 時系列の折れ線グラフが生成されます。

---

## 🚀 Step 3: 分布のヒストグラム

データの分布を確認するヒストグラムを作成します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 分布のヒストグラム",
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
Shakespeareデータセットの単語出現回数の分布を
ヒストグラムで可視化してください。

条件:
- 出現回数が0より大きく100未満の単語
- ビン数: 50

グラフの要件:
- ヒストグラム
- X軸: 「単語の出現回数」
- Y軸: 「頻度」
- タイトル: 「単語出現回数の分布」
- 縦軸にグリッド線
- 高解像度（dpi=150）で保存

出力先: ~/ai-agent-camp/output/chart-4-4-hist.png
```

**期待される結果**: 出現回数の分布を示すヒストグラムが生成されます。

---

## 🚀 Step 4: 散布図と相関分析

2変数の関係を散布図で可視化します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 散布図と相関分析",
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
Shakespeare作品の「ユニーク単語数」と「総単語数」の
関係を散布図で可視化してください。

グラフの要件:
- 散布図
- X軸: ユニーク単語数
- Y軸: 総単語数
- 各点に作品名のラベルを追加
- グリッド線
- 高解像度（dpi=150）で保存

出力先: ~/ai-agent-camp/output/chart-4-4-scatter.png
```

**期待される結果**: 相関関係を示す散布図が生成されます。

---

## 🚀 Step 5: ダッシュボードの作成

複数のグラフを1つの画像にまとめます：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: ダッシュボードの作成",
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
Module 8で作成したグラフを組み合わせて、
4分割のダッシュボードを作成してください。

配置:
┌────────────────┬────────────────┐
│  棒グラフ      │  折れ線グラフ  │
│ (カテゴリ集計) │ (時系列トレンド)│
├────────────────┼────────────────┤
│  散布図        │  ヒストグラム  │
│ (相関分析)     │ (分布)         │
└────────────────┴────────────────┘

サイズ: 16x12インチ
全体タイトル: 「GA4 & Shakespeare データ分析ダッシュボード」
高解像度（dpi=150）で保存

出力先: ~/ai-agent-camp/output/dashboard-4-4.png
```

**期待される結果**: 4つのグラフが配置されたダッシュボード画像が生成されます。

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
      {"id": "trouble_1", "label": "グラフが表示されない"},
      {"id": "trouble_2", "label": "日本語が文字化けする"},
      {"id": "trouble_3", "label": "メモリエラーが発生"},
      {"id": "trouble_4", "label": "グラフの見た目が良くない"}
    ]
  }]
}
```


### トラブル1: 「グラフが表示されない」
**原因**: matplotlibのバックエンド設定
**解決プロンプト**:
```text
matplotlibのバックエンドを確認してください。
ファイル保存用に 'Agg' バックエンドに切り替える方法を教えてください。
```

### トラブル2: 「日本語が文字化けする」
**原因**: 日本語フォントが設定されていない
**解決プロンプト**:
```text
matplotlibで日本語を正しく表示するための
フォント設定方法を教えてください。
macOS用の設定をお願いします。
```

### トラブル3: 「メモリエラーが発生」
**原因**: データ量が多すぎる
**解決プロンプト**:
```text
大量のデータをプロットする際のメモリ最適化方法を教えてください。
サンプリングや集計による対処法を説明してください。
```

### トラブル4: 「グラフの見た目が良くない」
**原因**: デフォルトのスタイル設定
**解決プロンプト**:
```text
seabornでグラフのスタイルを改善する方法を教えてください。
プレゼン向けの見やすいスタイル設定をお願いします。
```

---

## ✅ チェックポイント
- [ ] 基本的な棒グラフを作成できた
- [ ] 時系列データを折れ線グラフで表現できた
- [ ] ヒストグラムで分布を可視化できた
- [ ] 散布図で2変数の関係を分析できた
- [ ] 複数のグラフをダッシュボードにまとめられた
- [ ] 高解像度（dpi=150以上）で保存できた

---

## 🛠️ トラブルシューティング

- グラフが表示されない
- 日本語フォントが崩れる
- メモリエラーが出る

### グラフが表示されない
matplotlib のバックエンドを確認し、必要なら `Agg` に切り替えて保存してください。

### 日本語フォントが崩れる
日本語フォント設定を追加し、フォント名の優先順位を調整してください。

### メモリエラーが出る
データをサンプリングするか、事前集計してから可視化してください。

### seaborn と matplotlib の使い分け
- **matplotlib**: 細かいカスタマイズが必要な場合や、ダッシュボードで複数グラフを `subplot` で配置する場合に最適
- **seaborn**: 統計的な可視化（ヒートマップ、ペアプロット、箱ひげ図など）を少ないコードで綺麗に作りたい場合に最適。`sns.set_theme(style='whitegrid')` で見た目を一括改善できる
- 両方を組み合わせることも可能。seaborn で描画し、matplotlib で軸ラベルやタイトルを調整するのが一般的なパターン

---

## 📚 グラフタイプの選び方

| グラフタイプ | 用途 | 例 |
|-------------|------|-----|
| 棒グラフ | カテゴリ間の比較 | 国別売上、部門別人数 |
| 折れ線グラフ | 時系列トレンド | 日別売上推移 |
| 散布図 | 2変数の関係 | 価格 vs 売上数 |
| ヒストグラム | 分布の確認 | 年齢分布 |
| 円グラフ | 構成比 | シェア率 |
| ヒートマップ | 2次元データの密度 | 相関行列 |

---

## 🎉 Module 8 完了！

おめでとうございます！以下のスキルを習得しました：
- BigQueryへの接続と認証
- 探索的データ分析（EDA）の実行
- Marimoでの対話型分析
- 様々なグラフタイプの作成
- ダッシュボードの構築


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-9-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-9-1
- finish → 終了
