---
name: monitoring-dashboard
description: |
  marimoダッシュボード・プロジェクト進捗可視化に使用。
  「ダッシュボードを作って」「進捗を可視化して」「テスト結果を表示して」等のリクエストで発動。
triggers:
  - ダッシュボードを作って
  - 進捗を可視化して
  - テスト結果を表示して
  - monitoring-dashboard
  - プロジェクト進捗ダッシュボード
  - モニタリング
---

# Monitoring Dashboard - プロジェクトモニタリングダッシュボード

marimo Run Mode を使って、プロジェクト進捗・テスト結果・要件トレーサビリティを可視化するダッシュボードを生成します。

## Workflow

1. データソース（JSON/CSV）を指定
2. ダッシュボードのレイアウトを選択（進捗/テスト/統合）
3. marimo ノートブック（.py）を自動生成
4. `marimo run` で起動し、ブラウザで確認

## Dashboard Types

### 1. プロジェクト進捗ダッシュボード

WBS進捗データから以下を可視化:
- タスク完了率（全体/フェーズ別）
- バーンダウンチャート
- 担当者別負荷（ワークロード）
- 遅延タスクアラート

**データ形式:** `dummy-wbs-progress.json`
```json
{
  "tasks": [
    {
      "id": "WBS-001",
      "name": "タスク名",
      "phase": "Phase A",
      "assignee": "担当者",
      "progress": 75,
      "start_date": "2025-01-01",
      "due_date": "2025-01-15",
      "status": "in_progress"
    }
  ]
}
```

### 2. テスト結果ダッシュボード

テスト実行結果から以下を可視化:
- テストスイート別 成功/失敗/スキップ率
- テストカバレッジ推移
- 失敗テスト一覧（重要度順）
- テスト実行時間分析

**データ形式:** `dummy-test-results.json`
```json
{
  "suites": [
    {
      "name": "スイート名",
      "tests": [
        {
          "id": "TC-001",
          "name": "テスト名",
          "status": "passed",
          "duration_ms": 150,
          "severity": "high"
        }
      ]
    }
  ]
}
```

### 3. 要件トレーサビリティダッシュボード

要件→設計→テストの追跡:
- 要件カバレッジマトリクス
- 未テスト要件のハイライト
- 要件ステータス分布（円グラフ）

## marimo ノートブック構造

```python
import marimo as mo
import pandas as pd
import plotly.express as px
import json

app = mo.App()

@app.cell
def load_data():
    """データ読み込み"""
    with open("path/to/data.json") as f:
        data = json.load(f)
    return pd.DataFrame(data["tasks"])

@app.cell
def progress_chart(df):
    """進捗チャート"""
    fig = px.bar(df, x="name", y="progress", color="phase",
                 title="タスク進捗率")
    mo.ui.plotly(fig)

@app.cell
def summary_metrics(df):
    """サマリーメトリクス"""
    total = len(df)
    completed = len(df[df["progress"] == 100])
    mo.md(f"""
    ## プロジェクトサマリー
    - 総タスク数: **{total}**
    - 完了: **{completed}**
    - 完了率: **{completed/total*100:.1f}%**
    """)
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| data_source | Yes | - | データファイルのパス（JSON/CSV） |
| dashboard_type | No | integrated | ダッシュボード種別（progress/test/traceability/integrated） |
| output | No | output/pm/dashboard.py | 出力ファイルパス |
| title | No | Project Dashboard | ダッシュボードタイトル |

## Output Format

marimo ノートブック（.py）を生成:
- `output/pm/dashboard.py` — `marimo run output/pm/dashboard.py` で起動

## Requirements

- Python 3.10+
- marimo (`pip install marimo`)
- pandas (`pip install pandas`)
- plotly (`pip install plotly`)

## Example

```
monitoring-dashboardスキルを使って、ダミーデータからプロジェクト統合ダッシュボードを作成してください。
データ: 任意の進捗 JSON または CSV
→ output/pm/dashboard.py が生成される → marimo run で起動
```
