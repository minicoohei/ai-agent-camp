---
name: data-analyst
description: "BigQuery/Snowflake接続、EDA、可視化、Marimoノートブック作成を行うサブエージェント。 データ分析関連の4つのルール（data_analysis, visualization, notebook, marimo_variable_naming）を統合。 「データ分析して」「BigQueryに接続」「EDAを実行」「Marimoで分析」等のリクエストで発動。"
triggers:
  - データ分析
  - BigQuery
  - Snowflake
  - EDA
  - 探索的データ分析
  - 可視化
  - グラフを作成
  - Marimo
  - ノートブック
---

# Data Analyst サブエージェント

BigQuery/Snowflake接続、EDA、可視化、Marimoノートブック作成を専用コンテキストで実行するサブエージェント。

## 目的

データ分析処理をメインエージェントのコンテキストから分離し：
- 4つの関連ルールをサブエージェント内に統合（約1500-3000トークン削減）
- 分析結果のサマリーのみを返却
- GCP認証フローの統合

## 統合ルール

このサブエージェントは以下の4つのルールの内容を内包しています：
1. `data_analysis.mdc` - データ分析の基本原則
2. `visualization.mdc` - 可視化の品質基準
3. `notebook.mdc` - Marimo Notebook利用ルール
4. `marimo_variable_naming.mdc` - Marimo変数命名ルール

---

# Part 1: データ分析の基本原則

## 分析プロセス

1. **目的の明確化**: 分析開始前に目的・ゴール・仮説を記述
2. **データ品質の確保**: 完全性・正確性・一貫性を確認、欠損・異常値・重複の処理方針を説明
3. **バイアスと因果**: 主観的バイアスを排除、相関と因果を混同しない
4. **分析対象の理解**: カラム意味・単位・収集元・更新頻度を把握

## ファイル整理

```
data/
├── raw/           # 元データ（上書き禁止）
├── intermediate/  # 中間処理データ
├── feature/       # 特徴量データ
└── output/        # 最終出力
```

**命名規則**: `{source}__{target}__{granularity}__{date}.parquet`
例: `bq__sales__daily__2025-03-01.parquet`

## EDA（探索的データ分析）

- YData Profiling (`ydata-profiling`) やAutoViz (`autoviz`) を活用
- Marimoでインタラクティブに探索
- 1つのグラフに情報を詰め込みすぎない

---

# Part 2: 可視化の品質基準

## 必須ルール

| ルール | 説明 |
|--------|------|
| 意味のあるラベル | index番号使用禁止、ユーザー名/日付/カテゴリ名を使用 |
| 適切なグラフタイプ | 棒グラフ（比較）、折れ線（時系列）、ヒートマップ（2次元）|
| 日本語ラベル | 専門知識なしで理解できるように |
| 数値ラベル表示 | 棒の上に「1,791件」等を表示 |
| タイトル/軸ラベル/凡例 | 必須 |
| 高解像度 | 300 DPI以上 |

## グラフタイプ選択

| データ | 推奨グラフ |
|--------|----------|
| カテゴリ比較 | 棒グラフ |
| 時系列 | 折れ線グラフ |
| 2次元データ | ヒートマップ |
| 内訳 | 積み上げグラフ |
| 長いラベル | 横棒グラフ |

## matplotlib設定

```python
import matplotlib
matplotlib.use('Agg')  # GUIなしで動作
import matplotlib.pyplot as plt

# 日本語フォント設定
plt.rcParams['font.family'] = 'Hiragino Sans'
```

---

# Part 3: Marimo Notebook ルール

## 基本ルール

1. **Marimoを使用**: Jupyter Notebookは使用しない
2. **分析目的を明記**: 最初のセルに記載
3. **仮想環境の使用**: uv を使用
4. **エラー対応**: 原因と再発防止策をNotebookに追記

## 進捗表示（tqdm）

```python
from tqdm import tqdm

# 時間のかかる処理には必ず進捗表示
for item in tqdm(items, desc="処理中", unit="item"):
    process(item)
    time.sleep(0.5)
```

## BigQuery重複除去（必須）

```sql
WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY post.xPostId ORDER BY _PARTITIONTIME DESC) as row_num
    FROM `project.dataset.table`
    WHERE _PARTITIONTIME IS NOT NULL
)
SELECT * FROM deduplicated WHERE row_num = 1
```

---

# Part 4: Marimo変数命名ルール

## 🚨 重要な制約

Marimoでは**変数の再定義が禁止**。異なるセル間で同じ変数名を使用するとエラー。

## 命名パターン

### セル固有の接尾辞

| セルの目的 | 推奨接尾辞 | 例 |
|----------|---------|---|
| データ取得 | `_fetch`, `_load` | `df_fetch`, `result_load` |
| 前処理 | `_prep`, `_clean` | `data_prep`, `values_clean` |
| 統計分析 | `_stat`, `_calc` | `mean_stat`, `corr_calc` |
| 可視化（静的） | `_static`, `_plot` | `fig_static`, `ax_plot` |
| 可視化（動的） | `_dyn`, `_inter` | `net_dyn`, `chart_inter` |
| モデル学習 | `_train`, `_fit` | `model_train`, `scaler_fit` |
| 評価 | `_eval`, `_test` | `score_eval`, `pred_test` |

### 正しい例

```python
# ✅ 良い例（セルごとに固有の接尾辞）
@app.cell
def _(data):
    fig_overview, axes_overview = plt.subplots(2, 2)
    for idx_ov, ax_ov in enumerate(axes_overview.flatten()):
        ax_ov.plot(data[idx_ov])
    return fig_overview, axes_overview

@app.cell
def _(data):
    fig_detail, axes_detail = plt.subplots(3, 3)
    return fig_detail, axes_detail
```

## 変数Lintチェック

```bash
# 編集前後で実行し、再定義が0件であることを確認
python scripts/lint_marimo_vars.py <path>
```

---

# GCP認証

## 作業開始前の確認

```bash
# 設定プロファイル一覧
gcloud config configurations list

# プロファイル切り替え
gcloud config configurations activate <profile_name>

# 認証
gcloud auth application-default login
```

## 利用可能なプロファイル

| プロファイル名 | プロジェクトID | 用途 |
|---------------|---------------|------|
| `default` | - | デフォルト環境 |
| `my-profile` | my-gcp-project | 本番データ分析 |
| `my-dev` | my-dev-project | 開発分析 |

---

# サブエージェント呼び出しパターン

メインエージェントは以下のパターンでこのサブエージェントを呼び出す：

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Data analysis",
    prompt="""
    このスキルを読んで実行してください: skills/data-analyst/SKILL.md
    
    タスク: {ユーザーの指示}
    データソース: {BigQuery / Snowflake / CSV等}
    分析目的: {EDA / 可視化 / レポート作成等}
    
    分析結果のサマリーを返却してください。
    """
)
```

---

# 返却フォーマット

```yaml
status: success
analysis_type: EDA
data_source: BigQuery (my-dev-project)
summary:
  total_rows: 150000
  columns: 25
  date_range: "2025-01-01 ~ 2025-12-31"
  key_findings:
    - "日別投稿数は平均1,200件/日"
    - "ピーク時間帯は12:00-13:00"
    - "週末は平日比30%減少"
visualizations:
  - path: reports/daily_posts.png
    description: "日別投稿数推移"
  - path: reports/hourly_heatmap.png
    description: "時間帯別ヒートマップ"
notebook:
  path: notebooks/eda_analysis.py
  status: "作成完了"
```

---

# 依存関係

```txt
marimo>=0.5.0
pandas>=2.0.0
plotly>=5.0.0
matplotlib>=3.7.0
google-cloud-bigquery>=3.0.0
ydata-profiling>=4.0.0
tqdm>=4.65.0
```

---

# ユースケース

1. **BigQuery EDA**: テーブル構造把握、基本統計、分布確認
2. **時系列分析**: トレンド、季節性、異常値検出
3. **コホート分析**: ユーザーセグメント、リテンション
4. **可視化レポート**: ダッシュボード、プレゼン資料
5. **Marimoノートブック作成**: インタラクティブ分析環境構築

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| GCP認証エラー | `gcloud auth application-default login` を実行 |
| BigQueryテーブルが見つからない | `gcloud config configurations list` でプロファイルを確認し適切なものに切り替え |
| Marimo変数再定義エラー | `python scripts/lint_marimo_vars.py <path>` で重複変数を確認・修正 |

## Success Criteria

- [ ] 分析結果のサマリー（YAML形式）が返却されている
- [ ] 可視化グラフに日本語ラベル・タイトル・凡例が含まれている
- [ ] 出力ファイルが `data/output/` または `reports/` に保存されている

## Overview

BigQuery/Snowflake接続、EDA（探索的データ分析）、可視化、Marimoノートブック作成を専用コンテキストで実行するサブエージェントスキルです。データ分析・可視化・Notebook作成の4つのルールを統合し、分析結果のサマリーのみを返却します。

## Usage

上記「サブエージェント呼び出しパターン」および「GCP認証」セクションを参照。基本的な実行例:

```bash
# Marimo ノートブックで分析を開始
marimo edit notebooks/eda_analysis.py

# 変数Lintチェック
python scripts/lint_marimo_vars.py notebooks/eda_analysis.py
```
