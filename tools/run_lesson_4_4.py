#!/usr/bin/env python3
"""Automated runner for Lesson 4-4 data visualization outputs."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import tempfile

import numpy as np
import pandas as pd


TMP_DIR = Path(tempfile.gettempdir()) / "aiagent-lesson-4-4"
TMP_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(TMP_DIR / "mplconfig"))
os.environ.setdefault("XDG_CACHE_HOME", str(TMP_DIR / "cache"))
(TMP_DIR / "mplconfig").mkdir(parents=True, exist_ok=True)
(TMP_DIR / "cache").mkdir(parents=True, exist_ok=True)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
REPORT_PATH = OUTPUT_DIR / "lesson-4-4-run-report.json"


@dataclass
class StepResult:
    step: str
    status: str
    output: str | None = None
    source: str | None = None
    details: str | None = None


def prepare_matplotlib() -> None:
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 150,
            "axes.titlesize": 16,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "font.sans-serif": ["Hiragino Sans", "Noto Sans CJK JP", "Arial Unicode MS", "DejaVu Sans"],
            "axes.unicode_minus": False,
        }
    )


def maybe_build_bigquery_client() -> tuple[bigquery.Client | None, str | None]:
    cred_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_env and not Path(cred_env).exists():
        os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)

    try:
        client = bigquery.Client()
        return client, None
    except Exception as exc:  # pragma: no cover - environment-dependent
        return None, f"{type(exc).__name__}: {exc}"


def query_bigquery(client: bigquery.Client, sql: str, *, timeout: int = 12) -> pd.DataFrame:
    job = client.query(sql)
    rows = list(job.result(timeout=timeout))
    return pd.DataFrame([dict(row.items()) for row in rows])


def fallback_shakespeare_corpus() -> pd.DataFrame:
    rows = [
        ("hamlet", 5316, 32777),
        ("coriolanus", 5275, 24644),
        ("troilus and cressida", 5124, 28372),
        ("cymbeline", 4967, 22635),
        ("henry vi part 2", 4929, 26172),
        ("othello", 4831, 27218),
        ("king lear", 4787, 26053),
        ("antony and cleopatra", 4722, 24942),
        ("merchant of venice", 4630, 18944),
        ("macbeth", 4514, 16874),
    ]
    return pd.DataFrame(rows, columns=["corpus", "unique_words", "total_words"])


def fallback_ga4_daily() -> pd.DataFrame:
    dates = pd.date_range("2021-01-01", "2021-01-10", freq="D")
    rows: list[dict[str, Any]] = []
    for idx, event_date in enumerate(dates):
        seed = int(hashlib.sha256(f"{event_date:%Y-%m-%d}".encode("utf-8")).hexdigest()[:8], 16)
        rows.append(
            {
                "event_date": event_date,
                "event_count": 950 + (seed % 900) + idx * 45,
            }
        )
    return pd.DataFrame(rows)


def fallback_histogram_data() -> pd.DataFrame:
    rng = np.random.default_rng(44)
    values = np.clip(rng.zipf(a=2.0, size=8000), 1, 99)
    return pd.DataFrame({"word_count": values})


def get_shakespeare_corpus(client: bigquery.Client | None) -> tuple[pd.DataFrame, str, str | None]:
    if client is None:
        return fallback_shakespeare_corpus(), "fallback", "BigQuery client unavailable"

    sql = """
    SELECT
      corpus,
      COUNT(DISTINCT word) AS unique_words,
      SUM(word_count) AS total_words
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus
    ORDER BY unique_words DESC
    LIMIT 10
    """
    try:
        df = query_bigquery(client, sql)
        return df, "bigquery", None
    except Exception as exc:
        return fallback_shakespeare_corpus(), "fallback", f"{type(exc).__name__}: {exc}"


def get_ga4_daily(client: bigquery.Client | None) -> tuple[pd.DataFrame, str, str | None]:
    if client is None:
        return fallback_ga4_daily(), "fallback", "BigQuery client unavailable"

    sql = """
    SELECT
      PARSE_DATE('%Y%m%d', event_date) AS event_date,
      COUNT(*) AS event_count
    FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
    WHERE _TABLE_SUFFIX BETWEEN '20210101' AND '20210110'
    GROUP BY event_date
    ORDER BY event_date
    """
    try:
        df = query_bigquery(client, sql)
        if not df.empty:
            df["event_date"] = pd.to_datetime(df["event_date"])
        return df, "bigquery", None
    except Exception as exc:
        return fallback_ga4_daily(), "fallback", f"{type(exc).__name__}: {exc}"


def get_histogram_data(client: bigquery.Client | None) -> tuple[pd.DataFrame, str, str | None]:
    if client is None:
        return fallback_histogram_data(), "fallback", "BigQuery client unavailable"

    sql = """
    SELECT
      word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE word_count > 0 AND word_count < 100
    """
    try:
        df = query_bigquery(client, sql)
        return df, "bigquery", None
    except Exception as exc:
        return fallback_histogram_data(), "fallback", f"{type(exc).__name__}: {exc}"


def save_bar_chart(df: pd.DataFrame, output_path: Path) -> None:
    data = df.sort_values("unique_words", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("crest", len(data))
    ax.barh(data["corpus"], data["unique_words"], color=colors)
    ax.set_title("Shakespeare作品別のユニーク単語数", fontweight="bold")
    ax.set_xlabel("ユニーク単語数")
    ax.set_ylabel("")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_line_chart(df: pd.DataFrame, output_path: Path) -> None:
    data = df.sort_values("event_date")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data["event_date"], data["event_count"], marker="o", linewidth=2.5, color="#176087")
    ax.set_title("日別イベント数推移", fontweight="bold")
    ax.set_xlabel("日付")
    ax.set_ylabel("イベント数")
    ax.grid(True, axis="both", linestyle="--", alpha=0.4)
    fig.autofmt_xdate(rotation=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_histogram(df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["word_count"], bins=50, color="#2f7d6b", edgecolor="white")
    ax.set_title("単語出現回数の分布", fontweight="bold")
    ax.set_xlabel("単語の出現回数")
    ax.set_ylabel("頻度")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_scatter(df: pd.DataFrame, output_path: Path) -> None:
    data = df.sort_values("unique_words")
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(data["unique_words"], data["total_words"], s=120, alpha=0.85, color="#c45b3c")
    for _, row in data.iterrows():
        ax.annotate(
            row["corpus"],
            (row["unique_words"], row["total_words"]),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=8,
        )
    ax.set_title("作品別ユニーク単語数と総単語数の関係", fontweight="bold")
    ax.set_xlabel("ユニーク単語数")
    ax.set_ylabel("総単語数")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_dashboard(
    corpus_df: pd.DataFrame,
    ga4_df: pd.DataFrame,
    hist_df: pd.DataFrame,
    output_path: Path,
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("GA4 & Shakespeare データ分析ダッシュボード", fontsize=22, fontweight="bold")

    bar_df = corpus_df.sort_values("unique_words", ascending=True)
    axes[0, 0].barh(bar_df["corpus"], bar_df["unique_words"], color=sns.color_palette("crest", len(bar_df)))
    axes[0, 0].set_title("カテゴリ集計")
    axes[0, 0].set_xlabel("ユニーク単語数")

    line_df = ga4_df.sort_values("event_date")
    axes[0, 1].plot(line_df["event_date"], line_df["event_count"], marker="o", linewidth=2.2, color="#176087")
    axes[0, 1].set_title("時系列トレンド")
    axes[0, 1].set_xlabel("日付")
    axes[0, 1].set_ylabel("イベント数")
    axes[0, 1].grid(True, linestyle="--", alpha=0.35)

    scatter_df = corpus_df.sort_values("unique_words")
    axes[1, 0].scatter(scatter_df["unique_words"], scatter_df["total_words"], s=90, color="#c45b3c", alpha=0.85)
    for _, row in scatter_df.iterrows():
        axes[1, 0].annotate(
            row["corpus"],
            (row["unique_words"], row["total_words"]),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=7,
        )
    axes[1, 0].set_title("相関分析")
    axes[1, 0].set_xlabel("ユニーク単語数")
    axes[1, 0].set_ylabel("総単語数")
    axes[1, 0].grid(True, linestyle="--", alpha=0.35)

    axes[1, 1].hist(hist_df["word_count"], bins=50, color="#2f7d6b", edgecolor="white")
    axes[1, 1].set_title("分布")
    axes[1, 1].set_xlabel("単語の出現回数")
    axes[1, 1].set_ylabel("頻度")
    axes[1, 1].grid(True, axis="y", linestyle="--", alpha=0.35)

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.autofmt_xdate(rotation=20)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def run() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prepare_matplotlib()

    results: list[StepResult] = [
        StepResult(step="readiness", status="success", details="Default choice: ready"),
    ]

    client, client_error = maybe_build_bigquery_client()
    if client_error:
        results.append(
            StepResult(
                step="external_api_attempt",
                status="failed",
                source="bigquery",
                details=client_error,
            )
        )
    else:
        results.append(
            StepResult(
                step="external_api_attempt",
                status="partial",
                source="bigquery",
                details=f"Client initialized for project {client.project}; query execution may still fallback",
            )
        )

    corpus_df, corpus_source, corpus_detail = get_shakespeare_corpus(client)
    bar_path = OUTPUT_DIR / "chart-4-4-bar.png"
    save_bar_chart(corpus_df, bar_path)
    results.append(
        StepResult(
            step="step1_bar_chart",
            status="success",
            output=str(bar_path),
            source=corpus_source,
            details=corpus_detail,
        )
    )

    ga4_df, ga4_source, ga4_detail = get_ga4_daily(client)
    line_path = OUTPUT_DIR / "chart-4-4-line.png"
    save_line_chart(ga4_df, line_path)
    results.append(
        StepResult(
            step="step2_line_chart",
            status="success",
            output=str(line_path),
            source=ga4_source,
            details=ga4_detail,
        )
    )

    hist_df, hist_source, hist_detail = get_histogram_data(client)
    hist_path = OUTPUT_DIR / "chart-4-4-hist.png"
    save_histogram(hist_df, hist_path)
    results.append(
        StepResult(
            step="step3_histogram",
            status="success",
            output=str(hist_path),
            source=hist_source,
            details=hist_detail,
        )
    )

    scatter_path = OUTPUT_DIR / "chart-4-4-scatter.png"
    save_scatter(corpus_df, scatter_path)
    results.append(
        StepResult(
            step="step4_scatter",
            status="success",
            output=str(scatter_path),
            source=corpus_source,
            details=corpus_detail,
        )
    )

    dashboard_path = OUTPUT_DIR / "dashboard-4-4.png"
    save_dashboard(corpus_df, ga4_df, hist_df, dashboard_path)
    results.append(
        StepResult(
            step="step5_dashboard",
            status="success",
            output=str(dashboard_path),
            source=f"bar:{corpus_source}, line:{ga4_source}, hist:{hist_source}",
        )
    )

    expected_outputs = [bar_path, line_path, hist_path, scatter_path, dashboard_path]
    missing = [str(path) for path in expected_outputs if not path.exists()]
    results.append(
        StepResult(
            step="completion_check",
            status="success" if not missing else "failed",
            details="All expected outputs exist" if not missing else f"Missing outputs: {missing}",
        )
    )
    results.append(
        StepResult(step="next_step", status="success", details="Default choice: next_auto"),
    )

    report = {
        "lesson": "Lesson 4-4: データ可視化とダッシュボード作成",
        "results": [asdict(result) for result in results],
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
