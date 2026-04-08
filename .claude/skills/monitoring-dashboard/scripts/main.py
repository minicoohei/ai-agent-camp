"""
Monitoring Dashboard - プロジェクトモニタリングダッシュボード生成ツール

marimo Run Mode を使って、プロジェクト進捗・テスト結果・要件トレーサビリティを
可視化するダッシュボードノートブック（.py）を生成します。

Usage:
    python main.py --data-source data.json --dashboard-type progress --output output/pm/dashboard.py
    python main.py --data-source data.csv --dashboard-type test --title "テスト結果"
    python main.py --data-source data.json --dashboard-type integrated
"""

import argparse
import json
import sys
import textwrap
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

DEFAULT_OUTPUT = ROOT_DIR / "output" / "pm" / "dashboard.py"

# Dashboard type → generator mapping
DASHBOARD_TYPES = ["progress", "test", "traceability", "integrated"]


def generate_progress_notebook(data_path: str, title: str) -> str:
    """プロジェクト進捗ダッシュボードの marimo ノートブックを生成"""
    return textwrap.dedent(f'''\
        import marimo

        app = marimo.App(width="medium")


        @app.cell
        def _():
            import marimo as mo
            import pandas as pd
            import plotly.express as px
            import json
            from pathlib import Path
            return json, mo, pd, px, Path


        @app.cell
        def _(json, pd, Path):
            data_path = Path("{data_path}")
            if data_path.suffix == ".csv":
                df = pd.read_csv(data_path)
            else:
                with open(data_path, encoding="utf-8") as f:
                    raw = json.load(f)
                df = pd.DataFrame(raw.get("tasks", raw))
            return (df,)


        @app.cell
        def _(mo):
            mo.md("# {title}")
            return


        @app.cell
        def _(df, mo):
            total = len(df)
            completed = len(df[df.get("progress", df.get("status", "")) == 100]) if "progress" in df.columns else 0
            in_progress = len(df[df["status"] == "in_progress"]) if "status" in df.columns else 0
            mo.md(f"""
            | Metric | Value |
            |--------|-------|
            | Total Tasks | **{{total}}** |
            | Completed | **{{completed}}** |
            | In Progress | **{{in_progress}}** |
            | Completion Rate | **{{completed/total*100:.1f if total > 0 else 0}}%** |
            """)
            return


        @app.cell
        def _(df, px, mo):
            if "progress" in df.columns and "name" in df.columns:
                fig = px.bar(
                    df, x="name", y="progress",
                    color=df.get("phase", None) if "phase" in df.columns else None,
                    title="Task Progress"
                )
                fig.update_layout(xaxis_tickangle=-45)
                mo.ui.plotly(fig)
            return


        @app.cell
        def _(df, px, mo):
            if "phase" in df.columns:
                phase_df = df.groupby("phase").agg(
                    avg_progress=("progress", "mean"),
                    count=("progress", "count")
                ).reset_index()
                fig = px.bar(phase_df, x="phase", y="avg_progress", text="count",
                             title="Phase-level Progress")
                mo.ui.plotly(fig)
            return


        if __name__ == "__main__":
            app.run()
    ''')


def generate_test_notebook(data_path: str, title: str) -> str:
    """テスト結果ダッシュボードの marimo ノートブックを生成"""
    return textwrap.dedent(f'''\
        import marimo

        app = marimo.App(width="medium")


        @app.cell
        def _():
            import marimo as mo
            import pandas as pd
            import plotly.express as px
            import json
            from pathlib import Path
            return json, mo, pd, px, Path


        @app.cell
        def _(json, pd, Path):
            data_path = Path("{data_path}")
            with open(data_path, encoding="utf-8") as f:
                raw = json.load(f)
            suites = raw.get("suites", [])
            rows = []
            for suite in suites:
                for test in suite.get("tests", []):
                    rows.append({{**test, "suite": suite["name"]}})
            df = pd.DataFrame(rows)
            return (df,)


        @app.cell
        def _(mo):
            mo.md("# {title}")
            return


        @app.cell
        def _(df, mo):
            total = len(df)
            passed = len(df[df["status"] == "passed"])
            failed = len(df[df["status"] == "failed"])
            skipped = len(df[df["status"] == "skipped"]) if "skipped" in df["status"].values else 0
            mo.md(f"""
            | Metric | Value |
            |--------|-------|
            | Total Tests | **{{total}}** |
            | Passed | **{{passed}}** |
            | Failed | **{{failed}}** |
            | Skipped | **{{skipped}}** |
            | Pass Rate | **{{passed/total*100:.1f if total > 0 else 0}}%** |
            """)
            return


        @app.cell
        def _(df, px, mo):
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            fig = px.pie(status_counts, values="count", names="status",
                         title="Test Results Distribution",
                         color="status",
                         color_discrete_map={{"passed": "#22c55e", "failed": "#ef4444", "skipped": "#eab308"}})
            mo.ui.plotly(fig)
            return


        @app.cell
        def _(df, px, mo):
            suite_summary = df.groupby(["suite", "status"]).size().reset_index(name="count")
            fig = px.bar(suite_summary, x="suite", y="count", color="status",
                         title="Results by Test Suite",
                         color_discrete_map={{"passed": "#22c55e", "failed": "#ef4444", "skipped": "#eab308"}})
            mo.ui.plotly(fig)
            return


        if __name__ == "__main__":
            app.run()
    ''')


def generate_traceability_notebook(data_path: str, title: str) -> str:
    """要件トレーサビリティダッシュボードの marimo ノートブックを生成"""
    return textwrap.dedent(f'''\
        import marimo

        app = marimo.App(width="medium")


        @app.cell
        def _():
            import marimo as mo
            import pandas as pd
            import plotly.express as px
            import json
            from pathlib import Path
            return json, mo, pd, px, Path


        @app.cell
        def _(json, pd, Path):
            data_path = Path("{data_path}")
            with open(data_path, encoding="utf-8") as f:
                raw = json.load(f)
            requirements = raw.get("requirements", raw)
            df = pd.DataFrame(requirements)
            return (df,)


        @app.cell
        def _(mo):
            mo.md("# {title}")
            return


        @app.cell
        def _(df, px, mo):
            if "status" in df.columns:
                status_counts = df["status"].value_counts().reset_index()
                status_counts.columns = ["status", "count"]
                fig = px.pie(status_counts, values="count", names="status",
                             title="Requirements Status Distribution")
                mo.ui.plotly(fig)
            return


        @app.cell
        def _(df, mo):
            if "test_coverage" in df.columns:
                untested = df[df["test_coverage"] == False]
                if len(untested) > 0:
                    mo.md("## Untested Requirements")
                    mo.ui.table(untested)
                else:
                    mo.md("## All requirements have test coverage")
            return


        if __name__ == "__main__":
            app.run()
    ''')


def generate_integrated_notebook(data_path: str, title: str) -> str:
    """統合ダッシュボードの marimo ノートブックを生成"""
    return textwrap.dedent(f'''\
        import marimo

        app = marimo.App(width="medium")


        @app.cell
        def _():
            import marimo as mo
            import pandas as pd
            import plotly.express as px
            import json
            from pathlib import Path
            return json, mo, pd, px, Path


        @app.cell
        def _(json, pd, Path):
            data_path = Path("{data_path}")
            if data_path.suffix == ".csv":
                raw = {{"tasks": pd.read_csv(data_path).to_dict("records")}}
            else:
                with open(data_path, encoding="utf-8") as f:
                    raw = json.load(f)
            tasks_df = pd.DataFrame(raw.get("tasks", []))
            test_rows = []
            for suite in raw.get("suites", []):
                for test in suite.get("tests", []):
                    test_rows.append({{**test, "suite": suite["name"]}})
            tests_df = pd.DataFrame(test_rows) if test_rows else pd.DataFrame()
            req_df = pd.DataFrame(raw.get("requirements", []))
            return tasks_df, tests_df, req_df


        @app.cell
        def _(mo):
            mo.md("# {title}")
            return


        @app.cell
        def _(tasks_df, tests_df, req_df, mo):
            sections = []
            if len(tasks_df) > 0:
                total = len(tasks_df)
                done = len(tasks_df[tasks_df.get("progress", tasks_df.get("status", "")) == 100]) if "progress" in tasks_df.columns else 0
                sections.append(f"- Tasks: **{{total}}** ({{done}} completed)")
            if len(tests_df) > 0:
                passed = len(tests_df[tests_df["status"] == "passed"])
                sections.append(f"- Tests: **{{len(tests_df)}}** ({{passed}} passed)")
            if len(req_df) > 0:
                sections.append(f"- Requirements: **{{len(req_df)}}**")
            mo.md("## Summary\\n" + "\\n".join(sections))
            return


        @app.cell
        def _(tasks_df, px, mo):
            if len(tasks_df) > 0 and "progress" in tasks_df.columns:
                fig = px.bar(tasks_df, x="name", y="progress", title="Task Progress")
                fig.update_layout(xaxis_tickangle=-45)
                mo.ui.plotly(fig)
            return


        @app.cell
        def _(tests_df, px, mo):
            if len(tests_df) > 0:
                status_counts = tests_df["status"].value_counts().reset_index()
                status_counts.columns = ["status", "count"]
                fig = px.pie(status_counts, values="count", names="status",
                             title="Test Results",
                             color_discrete_map={{"passed": "#22c55e", "failed": "#ef4444", "skipped": "#eab308"}})
                mo.ui.plotly(fig)
            return


        if __name__ == "__main__":
            app.run()
    ''')


GENERATORS = {
    "progress": generate_progress_notebook,
    "test": generate_test_notebook,
    "traceability": generate_traceability_notebook,
    "integrated": generate_integrated_notebook,
}


def main():
    parser = argparse.ArgumentParser(
        description="Monitoring Dashboard - marimo ダッシュボードノートブック生成"
    )
    parser.add_argument(
        "--data-source", required=True,
        help="データファイルのパス（JSON or CSV）"
    )
    parser.add_argument(
        "--dashboard-type", default="integrated",
        choices=DASHBOARD_TYPES,
        help="ダッシュボード種別 (default: integrated)"
    )
    parser.add_argument(
        "--output", default=None,
        help=f"出力ファイルパス (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--title", default="Project Dashboard",
        help="ダッシュボードタイトル (default: Project Dashboard)"
    )
    args = parser.parse_args()

    # Resolve paths
    data_path = Path(args.data_source).resolve()
    if not data_path.exists():
        print(f"Error: Data source not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else DEFAULT_OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate notebook
    generator = GENERATORS[args.dashboard_type]
    notebook_content = generator(str(data_path), args.title)

    output_path.write_text(notebook_content, encoding="utf-8")
    print(f"Dashboard notebook generated: {output_path}")
    print(f"Run with: marimo run {output_path}")


if __name__ == "__main__":
    main()
