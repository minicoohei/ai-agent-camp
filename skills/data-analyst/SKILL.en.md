---
name: data-analyst
description: "Sub-agent that performs BigQuery/Snowflake connections, EDA, visualization, and Marimo notebook creation. Integrates four related rules (data_analysis, visualization, notebook, marimo_variable_naming). Triggered by requests like 'analyze data,' 'connect to BigQuery,' 'run EDA,' 'analyze with Marimo,' etc."
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

# Data Analyst Sub-Agent

A sub-agent that executes BigQuery/Snowflake connections, EDA, visualization, and Marimo notebook creation in a dedicated context.

## Purpose

Separate data analysis processing from the main agent's context to:
- Integrate four related rules within the sub-agent (approximately 1500-3000 token reduction)
- Return only analysis result summaries
- Integrate GCP authentication flow

## Integrated Rules

This sub-agent incorporates the contents of the following four rules:
1. `data_analysis.mdc` - Basic principles of data analysis
2. `visualization.mdc` - Visualization quality standards
3. `notebook.mdc` - Marimo Notebook usage rules
4. `marimo_variable_naming.mdc` - Marimo variable naming rules

---

# Part 1: Basic Principles of Data Analysis

## Analysis Process

1. **Clarify the objective**: Document the purpose, goals, and hypotheses before starting the analysis
2. **Ensure data quality**: Verify completeness, accuracy, and consistency; explain handling policies for missing values, outliers, and duplicates
3. **Bias and causation**: Eliminate subjective bias; do not confuse correlation with causation
4. **Understand the analysis target**: Grasp column meanings, units, collection sources, and update frequencies

## File Organization

```
data/
├── raw/           # Original data (do not overwrite)
├── intermediate/  # Intermediate processing data
├── feature/       # Feature data
└── output/        # Final output
```

**Naming convention**: `{source}__{target}__{granularity}__{date}.parquet`
Example: `bq__sales__daily__2025-03-01.parquet`

## EDA (Exploratory Data Analysis)

- Utilize YData Profiling (`ydata-profiling`) and AutoViz (`autoviz`)
- Explore interactively with Marimo
- Avoid cramming too much information into a single chart

---

# Part 2: Visualization Quality Standards

## Required Rules

| Rule | Description |
|------|-------------|
| Meaningful labels | No index numbers; use user names/dates/category names |
| Appropriate chart type | Bar chart (comparison), line chart (time series), heatmap (2D) |
| Japanese labels | Understandable without specialized knowledge |
| Numeric label display | Show "1,791 items" etc. on top of bars |
| Title/axis labels/legend | Required |
| High resolution | 300 DPI or higher |

## Chart Type Selection

| Data | Recommended Chart |
|------|-------------------|
| Category comparison | Bar chart |
| Time series | Line chart |
| 2D data | Heatmap |
| Breakdown | Stacked chart |
| Long labels | Horizontal bar chart |

## matplotlib Configuration

```python
import matplotlib
matplotlib.use('Agg')  # Run without GUI
import matplotlib.pyplot as plt

# Japanese font configuration
plt.rcParams['font.family'] = 'Hiragino Sans'
```

---

# Part 3: Marimo Notebook Rules

## Basic Rules

1. **Use Marimo**: Do not use Jupyter Notebook
2. **Document the analysis purpose**: Include in the first cell
3. **Use virtual environments**: Use uv or venv
4. **Error handling**: Append the cause and prevention measures to the Notebook

## Progress Display (tqdm)

```python
from tqdm import tqdm

# Always display progress for time-consuming operations
for item in tqdm(items, desc="Processing", unit="item"):
    process(item)
    time.sleep(0.5)
```

## BigQuery Deduplication (Required)

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

# Part 4: Marimo Variable Naming Rules

## Important Constraint

In Marimo, **variable redefinition is prohibited**. Using the same variable name across different cells will cause an error.

## Naming Patterns

### Cell-Specific Suffixes

| Cell Purpose | Recommended Suffix | Example |
|-------------|-------------------|---------|
| Data fetching | `_fetch`, `_load` | `df_fetch`, `result_load` |
| Preprocessing | `_prep`, `_clean` | `data_prep`, `values_clean` |
| Statistical analysis | `_stat`, `_calc` | `mean_stat`, `corr_calc` |
| Visualization (static) | `_static`, `_plot` | `fig_static`, `ax_plot` |
| Visualization (dynamic) | `_dyn`, `_inter` | `net_dyn`, `chart_inter` |
| Model training | `_train`, `_fit` | `model_train`, `scaler_fit` |
| Evaluation | `_eval`, `_test` | `score_eval`, `pred_test` |

### Correct Examples

```python
# Good example (unique suffix per cell)
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

## Variable Lint Check

```bash
# Run before and after editing; confirm redefinitions are 0
python scripts/lint_marimo_vars.py <path>
```

---

# GCP Authentication

## Pre-Work Verification

```bash
# List configuration profiles
gcloud config configurations list

# Switch profiles
gcloud config configurations activate <profile_name>

# Authenticate
gcloud auth application-default login
```

## Available Profiles

| Profile Name | Project ID | Purpose |
|-------------|------------|---------|
| `default` | - | Default environment |
| `my-profile` | my-gcp-project | Production data analysis |
| `my-dev` | my-dev-project | Development analysis |

---

# Sub-Agent Invocation Pattern

The main agent invokes this sub-agent using the following pattern:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Data analysis",
    prompt="""
    Read and execute this skill: skills/data-analyst/SKILL.md
    
    Task: {user's instructions}
    Data source: {BigQuery / Snowflake / CSV, etc.}
    Analysis purpose: {EDA / visualization / report generation, etc.}
    
    Return a summary of the analysis results.
    """
)
```

---

# Return Format

```yaml
status: success
analysis_type: EDA
data_source: BigQuery (my-dev-project)
summary:
  total_rows: 150000
  columns: 25
  date_range: "2025-01-01 ~ 2025-12-31"
  key_findings:
    - "Average daily posts: 1,200/day"
    - "Peak hours: 12:00-13:00"
    - "Weekends see 30% decrease compared to weekdays"
visualizations:
  - path: reports/daily_posts.png
    description: "Daily post count trend"
  - path: reports/hourly_heatmap.png
    description: "Hourly heatmap"
notebook:
  path: notebooks/eda_analysis.py
  status: "Creation complete"
```

---

# Dependencies

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

# Use Cases

1. **BigQuery EDA**: Table structure understanding, basic statistics, distribution analysis
2. **Time series analysis**: Trends, seasonality, outlier detection
3. **Cohort analysis**: User segments, retention
4. **Visualization reports**: Dashboards, presentation materials
5. **Marimo notebook creation**: Building interactive analysis environments

## Troubleshooting

| Error | Solution |
|-------|----------|
| GCP authentication error | Run `gcloud auth application-default login` |
| BigQuery table not found | Check profiles with `gcloud config configurations list` and switch to the appropriate one |
| Marimo variable redefinition error | Check and fix duplicate variables with `python scripts/lint_marimo_vars.py <path>` |

## Success Criteria

- [ ] Analysis result summary (YAML format) has been returned
- [ ] Visualization charts include Japanese labels, titles, and legends
- [ ] Output files are saved to `data/output/` or `reports/`

## Overview

A sub-agent skill that executes BigQuery/Snowflake connections, EDA (Exploratory Data Analysis), visualization, and Marimo notebook creation in a dedicated context. It integrates four rules for data analysis, visualization, and notebook creation, returning only analysis result summaries.

## Usage

See the "Sub-Agent Invocation Pattern" and "GCP Authentication" sections above. Basic execution example:

```bash
# Start analysis with a Marimo notebook
marimo edit notebooks/eda_analysis.py

# Variable lint check
python scripts/lint_marimo_vars.py notebooks/eda_analysis.py
```
