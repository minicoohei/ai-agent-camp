---
name: fact-checker
description: "Skill that automatically extracts factual claims (numbers, dates, proper nouns, statistics) from articles and verifies them through web search. Triggered by requests like 'fact-check this,' 'verify the facts,' 'confirm the sources,' etc. Outputs a report with confidence scores."
version: 1.0.0
author: ai-agent-camp
dependencies:
  - google-genai>=1.0.0
  - pyyaml>=6.0
  - python-dotenv>=0.19.0
triggers:
  - fact-checker
  - ファクトチェック
  - 事実確認
  - 裏付け確認
  - 情報の真偽
  - fact check
---

## Trigger Words
"Fact check," "verify facts," "confirm sources," "verify information"

# Fact Checker - Fact-Checking Agent

## Overview

A skill that automatically extracts factual claims from articles and documents and verifies them through web search.
It uses the Gemini API to extract claims as structured data, then performs grounding searches to verify each claim.
Finally, it outputs a Markdown report with confidence scores.

## Claim Categories

| Category | Key | Description | Example |
|----------|-----|-------------|---------|
| **Numbers & Statistics** | `numbers` | Claims containing numbers | "The market size is $50 billion," "15% growth rate" |
| **Dates & Timeline** | `dates` | Descriptions related to dates or timelines | "Announced in 2024," "10 years since founding" |
| **Proper Nouns** | `names` | People, organizations, product names | "OpenAI CEO Sam Altman" |
| **Causation** | `causation` | Claims of the type "X caused Y" | "The spread of AI changed employment structures" |
| **Citations & Sources** | `citations` | Accuracy of existing citations and sources | "According to a Gartner study..." |

## Verification Levels

| Verdict | Meaning | Criteria |
|---------|---------|----------|
| Verified | Corroborated by multiple reliable sources | 2+ independent sources agree |
| Needs Review | Partially matches, or information may be outdated | Only 1 source, or minor numerical discrepancy |
| Discrepancy | Found contradicting information from sources | Clearly contradicts reliable sources |
| Unverifiable | No corroboration found through search | Cannot be confirmed as public information |

## Quick Start

```bash
# Fact-check an entire article
python skills/fact-checker/scripts/fact_checker.py --input article.md

# Check only numbers & statistics
python skills/fact-checker/scripts/fact_checker.py --input article.md --category numbers

# Detailed mode with specified output
python skills/fact-checker/scripts/fact_checker.py --input article.md --output report.md --depth thorough

# Test mode (no API required, runs with sample article)
python skills/fact-checker/scripts/fact_checker.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input, -i | Yes* | - | Input file path (Markdown/text) |
| --output, -o | No | `output/fact_report_{timestamp}.md` | Output report path |
| --category, -c | No | `all` | Check target category: `all`, `numbers`, `dates`, `names`, `causation`, `citations` |
| --depth, -d | No | `quick` | Verification depth: `quick` (fast, major claims only), `thorough` (all claims in detail) |
| --test | No | false | Test mode (no API required, runs with sample article) |

*`--input` is not required when using `--test`

## Output Format

A Markdown report is generated:

```markdown
# Fact Check Report

**Target file**: article.md
**Verification date**: 2026-02-12 15:30:00
**Verification depth**: quick

## Summary
- Claims detected: 12
- Verified: 7
- Needs Review: 3
- Discrepancy: 1
- Unverifiable: 1

## Details

### Claim 1: "The AI market size will reach $190 billion by 2025"
- **Category**: Numbers & Statistics
- **Verdict**: Needs Review
- **Confidence**: 65%
- **Reason**: Numbers slightly differ from latest data. Multiple sources show range of $184-200 billion
- **Sources**:
  - [Statista - AI Market Size](https://example.com/source1)
  - [Grand View Research](https://example.com/source2)

### Claim 2: "OpenAI was founded in San Francisco in 2015"
- **Category**: Proper Nouns / Dates & Timeline
- **Verdict**: Verified
- **Confidence**: 95%
- **Reason**: Confirmed by multiple official sources
- **Sources**:
  - [Wikipedia - OpenAI](https://example.com/source3)
  - [OpenAI Official Website](https://example.com/source4)
```

## Processing Flow

1. **Read article**: Load the input file (Markdown/text)
2. **Extract claims**: Use Gemini API to extract factual claims as structured JSON
3. **Generate search queries**: Create optimal search queries for each claim
4. **Execute verification**: Verify each claim using Gemini's grounding search
5. **Generate report**: Output verification results as a Markdown report

## Environment Setup

### Required: Gemini API Key

```bash
# Add to .env
GEMINI_API_KEY=your_api_key_here
# or
GOOGLE_API_KEY=your_api_key_here
```

### Dependencies

```txt
google-genai>=1.0.0
pyyaml>=6.0
python-dotenv>=0.19.0
```

## Usage Examples

```bash
# Fact-check a blog post
python skills/fact-checker/scripts/fact_checker.py \
  --input docs/blog-post.md --depth thorough

# Check only numbers in a news article
python skills/fact-checker/scripts/fact_checker.py \
  --input news_article.txt --category numbers

# Check proper nouns and dates in a press release
python skills/fact-checker/scripts/fact_checker.py \
  --input press_release.md --category names --output output/press_check.md

# Test run (no API key required)
python skills/fact-checker/scripts/fact_checker.py --test
```

## Related Skills

- **article-writer**: Article writing skill (can be used for fact-checking after creation)
- **proofreading-agent**: Proofreading agent (grammar and expression checking)
- **seo-audit**: SEO audit (complementary for content accuracy verification)
