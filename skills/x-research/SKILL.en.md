---
name: x-research
version: 1.0.0
author: ai-agent-camp
description: "Performs real-time search on X (Twitter) to collect and analyze tweets about a topic. Outputs search results as structured reports (Markdown + JSON + TXT). Triggered by 'Search on X', 'Look up on Twitter', 'Analyze tweets', etc."
triggers:
  - Search on X
  - Look up on Twitter
  - Analyze tweets
  - Check reactions on X
  - SNS research
  - Research trends
  - x-research
  - search tweets
dependencies:
  - requests>=2.28.0
  - python-dotenv>=0.19.0
---

# X Research - X (Twitter) Real-time Search & Analysis

## Description

Uses the X API v2 Recent Search endpoint to search, collect, and analyze real-time tweets about a specified topic.
Ranks retrieved tweets by engagement, and outputs structured reports including hashtag analysis, time-series distribution, and shared URL lists
in Markdown + JSON + plain text formats.

## Quick Start

```bash
# Basic search
python skills/x-research/scripts/x_research.py --topic "generative AI"

# Search in English, exclude retweets
python skills/x-research/scripts/x_research.py --topic "Claude AI" --lang en --no-retweets

# Last 3 days, sorted by relevance
python skills/x-research/scripts/x_research.py --topic "OpenAI" --days 3 --sort relevancy
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic, -t | Yes | - | Search topic/keyword |
| --query, -q | No | auto | Custom search query (specify directly instead of topic) |
| --lang, -l | No | ja | Language filter: ja, en, all |
| --days, -d | No | 7 | Search period (days, max 7) |
| --sort, -s | No | relevancy | Sort: relevancy, recency |
| --no-retweets | No | false | Exclude retweets |
| --no-replies | No | false | Exclude replies |
| --media-only | No | false | Media-attached tweets only |
| --from-user | No | - | Tweets from specific user only |
| --min-likes | No | 0 | Minimum likes (post-fetch filter) |
| --max-results, -m | No | 50 | Max results per page (max 100) |
| --max-pages | No | 3 | Max pages |
| --top-n | No | 10 | Number of top tweets to display |
| --output, -o | No | output/x-research/ | Output directory |
| --session | No | auto | Session name (used in output folder name) |
| --dry-run | No | false | Display query only without executing |
| --raw-json | No | false | Output raw API response to stderr |

## Query Syntax Guide

When specifying directly with `--query`, X API v2 search operators can be used:

| Operator | Example | Description |
|----------|---------|-------------|
| keyword | `generative AI` | Basic keyword search |
| "phrase" | `"Claude Code"` | Exact phrase match |
| from: | `from:OpenAI` | Posts from specific user |
| to: | `to:username` | Mentions to specific user |
| -is:retweet | `-is:retweet` | Exclude retweets |
| -is:reply | `-is:reply` | Exclude replies |
| has:media | `has:media` | Media-attached only |
| has:links | `has:links` | Link-attached only |
| lang: | `lang:ja` | Language specification |
| #hashtag | `#AI` | Hashtag search |
| OR | `AI OR artificial intelligence` | OR search |
| -keyword | `-ads` | Exclude keyword |

## Output Format

Three files are generated in `output/x-research/YYYYMMDD_HHMMSS_{topic}/`:

1. **`{topic}_report.md`** - Markdown report
   - Summary statistics (tweet count, unique users, total likes, etc.)
   - Top tweets (by engagement)
   - Hashtag analysis
   - Time-series distribution
   - Shared URL list

2. **`{topic}_data.json`** - Structured JSON
   - Metadata (query, parameters, generation timestamp)
   - Statistics
   - All tweet data (text, metrics, author info)

3. **`{topic}_raw.txt`** - Plain text summary

## Usage Examples

```bash
# Search for "generative AI" in Japanese (default settings)
python skills/x-research/scripts/x_research.py --topic "generative AI"

# Search for "Claude" in English, exclude retweets/replies
python skills/x-research/scripts/x_research.py \
  --topic "Claude AI" --lang en --no-retweets --no-replies

# Search posts from specific user
python skills/x-research/scripts/x_research.py \
  --topic "AI" --from-user AnthropicAI --lang en

# Media-attached tweets only, last 3 days
python skills/x-research/scripts/x_research.py \
  --topic "AI art" --media-only --days 3 --lang en

# Advanced search with custom query
python skills/x-research/scripts/x_research.py \
  --query '"Claude Code" OR "Cursor AI" -is:retweet lang:en' --topic "AI IDE"

# Dry-run to verify query
python skills/x-research/scripts/x_research.py \
  --topic "test" --no-retweets --lang ja --dry-run
```

## Environment Setup

### Required: X Bearer Token

```bash
# Add to .env
X_BEARER_TOKEN=your_bearer_token_here
```

How to obtain:
1. Visit [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. Create a project/app
3. Obtain Bearer Token
4. Add `X_BEARER_TOKEN=...` to `.env` file

### API Limits

| Plan | Search Limit | Period |
|------|-------------|--------|
| Free | Not available | - |
| Basic ($100/month) | 60 requests/15 min | Last 7 days |
| Pro ($5,000/month) | 300 requests/15 min | Last 7 days |

## Output Example

```
=== Output Complete ===
  Markdown: output/x-research/20260210_053000_generativeAI/generativeAI_report.md
  JSON:     output/x-research/20260210_053000_generativeAI/generativeAI_data.json
  Text:     output/x-research/20260210_053000_generativeAI/generativeAI_raw.txt

--- Summary ---
  Tweet count:     30
  Unique authors:  28
  Total likes:     1,234
  Total retweets:  56
  Total replies:   12
  Period:          2026-02-03 ~ 2026-02-10
```

## Dependencies

```text
requests>=2.28.0
python-dotenv>=0.19.0
```
