---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-18"]
level: "intermediate"
tags: ["pm", "dashboard", "marimo", "monitoring"]
---

# 🎓 Lesson 18-19: marimo ダッシュボード

| 項目 | 内容 |
|------|------|
| ゴール | marimo Run Modeを使ってTaskFlowプロジェクトの統合ダッシュボードを作成する（ダミーデータ使用） |
| 所要時間 | 約30分 |
| 使うスキル | monitoring-dashboard スキル, data-analyst スキル |
| 前提条件 | Lesson 18-18 完了 |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 Step 1: marimo環境の確認

marimo は Python 上で構築されたリアクティブノートブック環境です。Jupyter とは異なり、セルが依存関係を自動追跡し、変更時に自動再計算します。このレッスンでは、marimo を使ってプロジェクトの統合ダッシュボードを構築します。

```json
{
  "type": "AskQuestion",
  "question": "marimoの経験はありますか？",
  "options": [
    "初めて使う",
    "Jupyter経験あり",
    "marimo経験あり",
    "セットアップだけ手伝って"
  ],
  "multiple": false
}
```

### marimoのセットアップ

選択結果に応じて、以下のコマンドで環境を準備します：

```bash
# Python 3.10以上を確認
python3 --version    # Windowsでは python --version

# marimoのインストール
uv add marimo pandas plotly numpy

# インストール確認
marimo --version
```

**初めて使う方向けの簡易チュートリアル：**
- marimo セルは Python コードを含むテキストフィールド
- セル内の変数変更は自動的に依存する他のセルを更新
- `marimo run` モード：読み取り専用（ダッシュボード配布向け）
- `marimo edit` モード：対話的編集（開発向け）

任意で `marimo tutorial` コマンドで公式チュートリアルを実行できます。

## 📍 Step 2: ダミーデータの読み込み

TaskFlow プロジェクトのダミーデータを確認して、ダッシュボードに表示するデータを準備します。

```json
{
  "type": "AskQuestion",
  "question": "どのデータを使いますか？",
  "options": [
    "WBS進捗データ",
    "テスト結果データ",
    "両方",
    "カスタムデータも追加"
  ],
  "multiple": false
}
```

### データファイルの確認

以下のダミーデータをダッシュボードに使用します（レッスン内にデータ構造を埋め込み済み）：

**dummy-wbs-progress.json** の構造：
```json
{
  "project_id": "taskflow-v1",
  "phases": [
    {
      "phase_name": "企画",
      "start_date": "2024-01-01",
      "planned_end": "2024-02-28",
      "actual_end": "2024-02-25",
      "status": "completed",
      "completion_rate": 100,
      "tasks": 5,
      "completed_tasks": 5
    }
  ],
  "current_phase": "実装",
  "overall_progress": 65,
  "requirements": [
    {"req_id": "REQ-001", "title": "ユーザー認証", "status": "完了", "test_cases": 12},
    {"req_id": "REQ-002", "title": "タスクCRUD", "status": "完了", "test_cases": 20},
    {"req_id": "REQ-003", "title": "通知機能", "status": "完了", "test_cases": 8},
    {"req_id": "REQ-004", "title": "検索・フィルタ", "status": "実装中", "test_cases": 5},
    {"req_id": "REQ-005", "title": "ダッシュボード表示", "status": "実装中", "test_cases": 3},
    {"req_id": "REQ-006", "title": "レポート出力", "status": "保留", "test_cases": 0},
    {"req_id": "REQ-007", "title": "外部API連携", "status": "却下", "test_cases": 0}
  ]
}
```

**dummy-test-results.json** の構造：
```json
{
  "test_execution_date": "2024-07-15",
  "test_suites": [
    {
      "suite_name": "ユーザー認証テスト",
      "total_cases": 12,
      "passed": 11,
      "failed": 1,
      "skipped": 0,
      "success_rate": 91.67
    }
  ],
  "overall_pass_rate": 87.5,
  "failed_tests": [
    {
      "test_id": "TC-AUTH-007",
      "name": "パスワードリセット - 無効トークン処理",
      "error": "Expected status 400, got 500"
    }
  ]
}
```

### データ読み込みコード例

ダッシュボード内でダミーデータを直接定義して使用します（上記の JSON 構造を参照）。

```python
import json
import pandas as pd

# ダミーデータを直接定義（上記の構造を使用）
wbs_data = {
    "project_id": "taskflow-v1",
    "phases": [
        {"phase_name": "企画", "start_date": "2024-01-01", "planned_end": "2024-02-28",
         "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
         "tasks": 5, "completed_tasks": 5},
        # ... 他のフェーズも同様に定義
    ],
    "current_phase": "実装",
    "overall_progress": 65,
    "requirements": [
        {"req_id": "REQ-001", "title": "ユーザー認証", "status": "完了", "test_cases": 12},
        {"req_id": "REQ-002", "title": "タスクCRUD", "status": "完了", "test_cases": 20},
        {"req_id": "REQ-003", "title": "通知機能", "status": "完了", "test_cases": 8},
        {"req_id": "REQ-004", "title": "検索・フィルタ", "status": "実装中", "test_cases": 5},
        {"req_id": "REQ-005", "title": "ダッシュボード表示", "status": "実装中", "test_cases": 3},
        {"req_id": "REQ-006", "title": "レポート出力", "status": "保留", "test_cases": 0},
        {"req_id": "REQ-007", "title": "外部API連携", "status": "却下", "test_cases": 0}
    ]
}

test_data = {
    "test_execution_date": "2024-07-15",
    "test_suites": [
        {"suite_name": "ユーザー認証テスト", "total_cases": 12, "passed": 11,
         "failed": 1, "skipped": 0, "success_rate": 91.67},
        # ... 他のスイートも同様に定義
    ],
    "overall_pass_rate": 87.5,
    "failed_tests": [
        {"test_id": "TC-AUTH-007", "name": "パスワードリセット - 無効トークン処理",
         "error": "Expected status 400, got 500"}
    ]
}

# DataFrame への変換
phases_df = pd.DataFrame(wbs_data["phases"])
test_suites_df = pd.DataFrame(test_data["test_suites"])

print("WBS Progress Data:")
print(phases_df.head())
print("\nTest Results Data:")
print(test_suites_df.head())
```

## 📍 Step 3: 3パネルダッシュボード構成

TaskFlow プロジェクトの主要メトリクスを3つのパネルに分けて表示します。各パネルはプロジェクト管理の異なる側面を可視化します。

```json
{
  "type": "AskQuestion",
  "question": "ダッシュボードのレイアウトを選んでください",
  "options": [
    "3パネル横並び",
    "タブ切替",
    "スクロール型",
    "AIに最適配置を提案してもらう"
  ],
  "multiple": false
}
```

### Panel 1: プロジェクト進捗

プロジェクト全体の進捗状況を複数の視点から表示：

**表示内容：**
- 全体進捗バー（現在65%）
- フェーズ別進捗テーブル（企画100%、設計92%、実装65%、テスト20%）
- 進捗推移チャート（各週の進捗率）
- 遅延アラート（実装フェーズが予定比-3日）

**Plotly コード例：**
```python
import plotly.graph_objects as go
import plotly.express as px

# フェーズ別進捗バー
fig_phase = go.Figure(data=[
    go.Bar(y=['企画', '設計', '実装', 'テスト', '運用'],
           x=[100, 92, 65, 20, 0],
           orientation='h',
           marker=dict(color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']))
])
fig_phase.update_layout(title="フェーズ別進捗",
                        xaxis_title="進捗率 (%)",
                        height=300)

# 全体進捗ゲージ
fig_gauge = go.Figure(data=[
    go.Indicator(mode="gauge+number",
                 value=65,
                 title={'text': "全体進捗"},
                 domain={'x': [0, 1], 'y': [0, 1]},
                 gauge={'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccc"},
                            {'range': [50, 80], 'color': "#ffffcc"},
                            {'range': [80, 100], 'color': "#ccffcc"}]})
])
```

### Panel 2: テスト結果

テスト実行結果と品質メトリクス：

**表示内容：**
- 全体テスト成功率（87.5%）のパイチャート
- テストスイート別結果一覧（成功率、テスト数）
- 失敗テスト一覧（テストID、失敗理由、重要度）
- 品質トレンド（過去4週間の成功率推移）

**Plotly コード例：**
```python
# テスト成功率パイチャート
success_rate = test_data["overall_pass_rate"]
failure_rate = 100 - success_rate

fig_pie = go.Figure(data=[
    go.Pie(labels=['成功', '失敗'],
           values=[success_rate, failure_rate],
           marker=dict(colors=['#2ecc71', '#e74c3c']),
           hole=0.3)
])
fig_pie.update_layout(title="全体テスト成功率")

# テストスイート別バー
fig_suites = px.bar(test_suites_df,
                    x='suite_name',
                    y='success_rate',
                    color='success_rate',
                    color_continuous_scale='RdYlGn',
                    range_color=[70, 100],
                    title="テストスイート別成功率")

# 失敗テスト一覧テーブル
failed_df = pd.DataFrame(test_data["failed_tests"])
```

### Panel 3: 要件トラッカー

要件カバレッジと状態追跡：

**表示内容：**
- 要件ステータス分布（実装済、実装中、保留、却下）
- テストカバレッジ率（全要件の92%が実装・テスト済）
- 要件別テストマッピング（各要件に紐付くテストケース数）
- 高リスク要件フラグ（テストケース0の要件）

**Plotly コード例：**
```python
# 要件ステータス分布
status_counts = {
    '実装済': 42,
    '実装中': 8,
    '保留': 2,
    '却下': 1
}

fig_status = go.Figure(data=[
    go.Bar(x=list(status_counts.keys()),
           y=list(status_counts.values()),
           marker=dict(color=['#2ecc71', '#f39c12', '#3498db', '#95a5a6']))
])
fig_status.update_layout(title="要件ステータス分布",
                        yaxis_title="要件数")

# テストカバレッジ率
coverage = 92
fig_coverage = go.Figure(data=[
    go.Indicator(mode="gauge+number+delta",
                 value=coverage,
                 title={'text': "テストカバレッジ"},
                 gauge={'axis': {'range': [0, 100]},
                        'threshold': {'line': {'color': "red"}, 'thickness': 4, 'value': 80}})
])
```

## 📍 Step 4: marimo runで起動・確認

ダッシュボードの完成版を marimo で実行し、すべてのパネルが正しくレンダリングされることを確認します。

```json
{
  "type": "AskQuestion",
  "question": "起動方法を選んでください",
  "options": [
    "marimo run（読み取り専用）",
    "marimo edit（編集モード）",
    "スクリーンショットで確認"
  ],
  "multiple": false
}
```

### ダッシュボード Python ファイルの構造

`output/pm/dashboard.py` として以下の構造で作成：

```python
import marimo as mo
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

app = mo.App()

# ============= セル1: 環境と依存関係 =============
@app.cell
def environment():
    import sys
    print(f"Python {sys.version}")
    print(f"marimo version: {mo.__version__}")
    return

# ============= セル2: データ定義 =============
@app.cell
def load_data():
    # ダミーデータを直接定義
    wbs_data = {
        "project_id": "taskflow-v1",
        "phases": [
            {"phase_name": "企画", "start_date": "2024-01-01", "planned_end": "2024-02-28",
             "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
             "tasks": 5, "completed_tasks": 5},
            {"phase_name": "設計", "start_date": "2024-03-01", "planned_end": "2024-04-30",
             "actual_end": "2024-04-28", "status": "completed", "completion_rate": 92,
             "tasks": 8, "completed_tasks": 7},
            {"phase_name": "実装", "start_date": "2024-05-01", "planned_end": "2024-07-31",
             "actual_end": None, "status": "in_progress", "completion_rate": 65,
             "tasks": 12, "completed_tasks": 8},
            {"phase_name": "テスト", "start_date": "2024-08-01", "planned_end": "2024-09-15",
             "actual_end": None, "status": "planned", "completion_rate": 20,
             "tasks": 6, "completed_tasks": 1},
            {"phase_name": "運用", "start_date": "2024-09-16", "planned_end": "2024-10-31",
             "actual_end": None, "status": "planned", "completion_rate": 0,
             "tasks": 4, "completed_tasks": 0}
        ],
        "current_phase": "実装",
        "overall_progress": 65,
        "requirements": [
            {"req_id": "REQ-001", "title": "ユーザー認証", "status": "完了", "test_cases": 12},
            {"req_id": "REQ-002", "title": "タスクCRUD", "status": "完了", "test_cases": 20},
            {"req_id": "REQ-003", "title": "通知機能", "status": "完了", "test_cases": 8},
            {"req_id": "REQ-004", "title": "検索・フィルタ", "status": "実装中", "test_cases": 5},
            {"req_id": "REQ-005", "title": "ダッシュボード表示", "status": "実装中", "test_cases": 3},
            {"req_id": "REQ-006", "title": "レポート出力", "status": "保留", "test_cases": 0},
            {"req_id": "REQ-007", "title": "外部API連携", "status": "却下", "test_cases": 0}
        ]
    }

    test_data = {
        "test_execution_date": "2024-07-15",
        "test_suites": [
            {"suite_name": "ユーザー認証テスト", "total_cases": 12, "passed": 11,
             "failed": 1, "skipped": 0, "success_rate": 91.67},
            {"suite_name": "タスク管理テスト", "total_cases": 20, "passed": 17,
             "failed": 2, "skipped": 1, "success_rate": 85.0},
            {"suite_name": "通知テスト", "total_cases": 8, "passed": 7,
             "failed": 1, "skipped": 0, "success_rate": 87.5}
        ],
        "overall_pass_rate": 87.5,
        "failed_tests": [
            {"test_id": "TC-AUTH-007", "name": "パスワードリセット - 無効トークン処理",
             "error": "Expected status 400, got 500"}
        ]
    }

    phases_df = pd.DataFrame(wbs_data["phases"])
    test_suites_df = pd.DataFrame(test_data["test_suites"])

    return wbs_data, test_data, phases_df, test_suites_df

# ============= セル3: Panel 1 - プロジェクト進捗 =============
@app.cell
def panel_progress(wbs_data):
    mo.md(f"""
    # 📊 Panel 1: プロジェクト進捗

    **全体進捗: {wbs_data['overall_progress']}%**

    現在フェーズ: {wbs_data['current_phase']}
    """)

# ============= セル4: Panel 2 - テスト結果 =============
@app.cell
def panel_tests(test_data):
    mo.md(f"""
    # ✅ Panel 2: テスト結果

    **全体成功率: {test_data['overall_pass_rate']}%**

    失敗テスト数: {len(test_data['failed_tests'])}
    """)

# ============= セル5: Panel 3 - 要件トラッカー =============
@app.cell
def panel_requirements(wbs_data):
    total = len(wbs_data.get("requirements", []))
    done = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "完了")
    in_progress = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "実装中")
    coverage = round(done / total * 100) if total > 0 else 0
    mo.md(f"""
    # 📋 Panel 3: 要件トラッカー

    **テストカバレッジ: {coverage}%**

    実装済要件: {done}個
    実装中要件: {in_progress}個
    """)

# ============= セル6: ダッシュボード統合 =============
@app.cell
def dashboard(wbs_data):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    mo.md(f"""
    # 🎯 TaskFlow プロジェクト統合ダッシュボード

    各パネル（Panel 1〜3）が上記のセルで個別に表示されます。

    ---

    **最終更新**: {now}

    **データソース**: ダミーデータ（samples/）
    """)

if __name__ == "__main__":
    app.run()
```

### 実行コマンド

```bash
# 読み取り専用モードで起動（ダッシュボード配布向け）
marimo run output/pm/dashboard.py

# または編集モードで起動（開発・微調整向け）
marimo edit output/pm/dashboard.py
```

### 確認チェックリスト

```json
{
  "type": "AskQuestion",
  "question": "ダッシュボードの起動は成功しましたか？",
  "options": [
    "成功 - すべてのパネルが表示された",
    "一部エラー - 修正が必要",
    "起動失敗 - デバッグサポートが必要",
    "スクリーンショット確認で済む"
  ],
  "multiple": false
}
```

**期待される表示：**
- Panel 1（プロジェクト進捗）：フェーズ別バー、全体進捗ゲージ
- Panel 2（テスト結果）：成功率パイチャート、失敗テスト一覧
- Panel 3（要件トラッカー）：ステータス分布、カバレッジ率

すべてが正常に表示されれば、このレッスンは完了です。

---

## ✅ 成果物

- `output/pm/dashboard.py` - marimo ノートブック形式の統合ダッシュボード

## 🚀 トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| marimoがインストールできない | Python 3.10+ を確認。`uv sync` 後に再試行 |
| データが不足している | レッスン内の埋め込みダミーデータ構造を参照して定義を補完 |
| Plotly グラフが表示されない | `uv add plotly` で最新版をインストール |
| marimo runが起動しない | `marimo edit` で構文エラーを確認 |


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── presentation.md  (プレゼン資料)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/presentation.md

# 冒頭を確認（最初の30行）
head -30 output/pm/presentation.md
```

> 💡 全文を確認: `cat output/pm/presentation.md` で全文表示できます

## ➡️ 次のステップ

→ [Lesson 18-20: 総合演習（カプストーン）](start-18-20.md)
