---
name: content-optimizer
version: 1.0.0
author: ai-agent-camp
description: "A planner skill to support content A/B testing and self-improvement loops. Covers the full cycle of market trend research -> hypothesis generation -> experiment design -> metrics collection -> analysis and improvement. Triggered by requests like 'optimize content', 'improve posts', 'create post ideas from trend analysis', 'improve engagement', etc."
triggers:
  - content-optimizer
  - optimize content
  - improve posts
  - trend analysis
  - improve engagement
  - content improvement loop
  - Typefully
  - content optimization
  - コンテンツを最適化
  - 投稿を改善
---

# Content Performance Optimizer - Content Self-Improvement Loop

## Description

Collects market data from 5 sources (X, Google Search, Google Trends, Reddit/HN, competitor accounts),
performs integrated analysis with LLM, and automatically generates hypotheses and A/B variants.
Registers generated post variants as drafts in Typefully, measures post-publication performance, and learns,
enabling a continuous self-improvement cycle for content.

## Workflow Overview

```
1. Market research -> 2. Hypothesis generation -> 3. Variant creation -> 4. Post (Typefully) -> 5. Metrics collection -> 6. Analysis & learning -> Back to 1.
```

## Quick Start

```bash
# Hypothesis generation (end-to-end: trend research -> hypotheses -> variants)
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "AI agents" --channel x_twitter

# Metrics collection (post-publication performance measurement)
python skills/content-optimizer/scripts/collect_metrics.py --tweet-ids "123,456" --experiment-id exp-001

# Dry run (no API calls)
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "SaaS" --dry-run
```

## Script List

| Script | Purpose |
|--------|---------|
| hypothesis_generator.py | Market research -> hypothesis generation -> variant creation |
| collect_metrics.py | Tweet metrics collection and variant comparison |
| typefully_client.py | Typefully API v2 client |

## hypothesis_generator.py Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic, -t | Yes | - | Research topic |
| --channel, -c | No | x_twitter | Channel: x_twitter, email, linkedin |
| --competitors | No | - | Competitor accounts (comma-separated) |
| --lang, -l | No | ja | Language: ja, en, all |
| --days, -d | No | 7 | Research period |
| --num-hypotheses | No | 5 | Number of hypotheses to generate |
| --auto-draft | No | false | Auto-create drafts in Typefully |
| --output, -o | No | output/content-optimizer/ | Output destination |
| --dry-run | No | false | Preview without API calls |
| --test | No | false | Self-test |

## collect_metrics.py Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --tweet-ids | No | - | Tweet IDs for metrics retrieval (comma-separated) |
| --username | No | - | Retrieve user's recent posts |
| --experiment-id | No | - | Link and compare by experiment ID |
| --days-after | No | 3 | Days of metrics to retrieve after posting |
| --output, -o | No | output/content-optimizer/ | Output destination |
| --test | No | false | Self-test |

## Data Sources

| Source | API | Data Retrieved | Environment Variable |
|--------|-----|----------------|---------------------|
| X (Twitter) | X API v2 Recent Search | Viral posts (top engagement) | X_BEARER_TOKEN |
| Google Search | Gemini Google Search grounding | Trending articles, best practices | GEMINI_API_KEY |
| Google Trends | Gemini grounding | Search volume trends, rising topics | GEMINI_API_KEY |
| Reddit / HN | Reddit JSON API + HN Algolia API | Community discussions, sentiment | Not required |
| Competitor accounts | X API v2 User Tweets | Competitor's high-performance posts | X_BEARER_TOKEN |

## Output Format

```
output/content-optimizer/hypotheses/YYYYMMDD_HHMMSS_{topic}/
├── market_report.md       # Trend report
├── hypotheses.yaml        # Hypothesis list (prioritized)
├── experiment_design.yaml # Experiment design document
├── raw_data.json          # Raw data from all sources
└── drafts/                # A/B variant post drafts
    ├── variant_a.md
    └── variant_b.md
```

## Environment Setup

### Required Environment Variables

```bash
# Add to .env
X_BEARER_TOKEN=your_x_bearer_token_here   # X API v2 search and user retrieval
GEMINI_API_KEY=your_gemini_api_key_here   # Google Search grounding + LLM analysis
```

### Optional Environment Variables

```bash
TYPEFULLY_API_KEY=your_typefully_key_here  # When using --auto-draft option
```

### How to Obtain

- **X_BEARER_TOKEN**: Obtain after creating a project at [X Developer Portal](https://developer.x.com/en/portal/dashboard) (Basic plan or above)
- **GEMINI_API_KEY**: Obtain at [Google AI Studio](https://aistudio.google.com/apikey) (free)
- **TYPEFULLY_API_KEY**: Obtain at [Typefully Settings](https://typefully.com/settings/integrations) API section

## How to Use the Self-Improvement Loop

1. Use `hypothesis_generator.py` for trend analysis -> hypotheses -> variant generation
2. Post A/B variants via Typefully (manual or `--auto-draft` flag)
3. After 2-3 days, measure performance with `collect_metrics.py`
4. Generate next hypotheses based on results (learning accumulates)

## Usage Examples

```bash
# Generate hypotheses about AI agents for X (Japanese)
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "AI agents" --channel x_twitter --lang ja

# Also research competitor accounts and auto-register variants to Typefully
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "SaaS" --competitors "user_a,user_b" --auto-draft

# Generate 5 hypotheses for LinkedIn content in English
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "productivity" --channel linkedin --lang en --num-hypotheses 5

# Collect metrics for specified tweet IDs
python skills/content-optimizer/scripts/collect_metrics.py \
  --tweet-ids "1234567890,0987654321" --experiment-id exp-001

# Retrieve and analyze user's recent posts
python skills/content-optimizer/scripts/collect_metrics.py \
  --username myaccount --days-after 7

# Dry run to check what data would be retrieved
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "generative AI" --dry-run
```

## Dependencies

```text
requests>=2.28.0
python-dotenv>=0.19.0
pyyaml>=6.0
google-genai>=0.5.0
```

## Related Skills

- `x-research` -- X search data collection
- `ab-test-setup` -- Detailed experiment design framework
- `social-content` -- SNS content strategy
- `content-strategy` -- Content planning
- `analytics-tracking` -- Metrics measurement
