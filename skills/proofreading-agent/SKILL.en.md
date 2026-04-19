---
name: proofreading-agent
description: "A Japanese article proofreading agent. Checks for typos, grammar, expression consistency, and readability, outputting correction suggestions as inline annotations. Triggered by requests like 'Proofread this', 'Check the text', 'Check for typos', 'Review the article'."
triggers:
  - Proofread this
  - Check the text
  - Check for typos
  - Review the article
  - Polish the writing
  - Copyedit this
  - proofreading-agent
---

## Trigger Words
"Proofread", "Check text", "Typos", "Polish", "Copyedit"

# Proofreading Agent - Japanese Article Proofreading Agent

An agent that systematically proofreads Japanese articles. Inspired by the "Seven Sweeps" copy editing methodology, it uses **Five Sweeps** optimized for Japanese content to review articles from multiple angles.

## Five Sweeps

Proofreading is performed in the following 5 stages. Each sweep can be run independently, allowing focused review on specific categories.

### 1. Accuracy Check

Detects character-level errors.

- **Typos**: Kanji conversion mistakes, typing errors
- **Okurigana errors**: Incorrect verb/adjective inflection suffixes
- **Homophone misuse**: Confusion between words that sound alike
- **Proper noun misspellings**: Accuracy of product names, personal names, organization names

### 2. Grammar Check

Verifies grammatical correctness.

- **Subject-predicate mismatch**: Disagreement between subject and predicate
- **Particle misuse**: Incorrect use of Japanese particles
- **Honorific consistency**: Mixing of different politeness levels
- **Modifier-modified relationship errors**: Issues with modifying word connections
- **Tense inconsistency**: Mixing of past and present tense

### 3. Consistency Check

Confirms notation consistency throughout the article.

- **Notation variations**: Inconsistent spelling of the same word
- **Sentence ending consistency**: Mixing of formal and informal styles
- **Number notation**: Mixing full-width and half-width characters
- **Symbol consistency**: Types of brackets, punctuation
- **Abbreviation consistency**: Full spelling on first use

### 4. Readability Check

Evaluates text readability.

- **Sentence length**: Detection of sentences exceeding 80 characters
- **Difficult kanji**: Use of kanji that are hard for general readers
- **Redundant expressions**: Simplification of verbose phrases
- **Double negatives**: Simplification of double negative constructions
- **Excessive passive voice**: Suggestions for active voice rewriting
- **Excessive katakana**: Flagging where Japanese equivalents suffice

### 5. Structure Check

Reviews overall article structure and logical flow.

- **Paragraph logical connections**: Connections between preceding and following paragraphs
- **Duplicate content**: Unnecessary repetition of the same information
- **Information gaps**: Insufficient explanations, unnecessary information
- **Heading hierarchy**: Appropriateness of heading levels
- **Introduction-conclusion alignment**: Correspondence between opening problem statement and conclusion

## Usage

```bash
# Full sweep proofreading (default)
python scripts/proofreading_agent.py --input article.md --output review.md

# Run specific sweeps only
python scripts/proofreading_agent.py --input article.md --sweep accuracy
python scripts/proofreading_agent.py --input article.md --sweep grammar
python scripts/proofreading_agent.py --input article.md --sweep consistency
python scripts/proofreading_agent.py --input article.md --sweep readability
python scripts/proofreading_agent.py --input article.md --sweep structure

# Specify style profile
python scripts/proofreading_agent.py --input article.md --style style_profile.yaml

# Severity filter (show only high)
python scripts/proofreading_agent.py --input article.md --severity high

# Test mode (no API required, runs with sample text)
python scripts/proofreading_agent.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes* | - | File path to proofread (Markdown/text). Not required in --test mode |
| --output | No | output/review_{timestamp}.md | Proofreading results output destination |
| --sweep | No | all | Sweep to run: all, accuracy, grammar, consistency, readability, structure |
| --style | No | - | Style profile (YAML) path |
| --severity | No | medium | Minimum severity to display: low, medium, high |
| --test | No | false | Test mode (sample text verification without API) |

## Style Profile (YAML)

Customize rules according to article type.

```yaml
# style_profile.yaml example
name: "Technical Blog"
tone: "desu/masu"  # Formal Japanese style
terminology:
  preferred:
    - { term: "server", reject: ["svr"] }
    - { term: "user", reject: ["usr"] }
    - { term: "interface", reject: ["i/f"] }
  domain_terms:
    - "API"
    - "SDK"
    - "CI/CD"
rules:
  max_sentence_length: 80
  number_style: "half-width"
  punctuation: "comma-period"
```

## Output Format

### Inline Annotations

Annotations are inserted directly at the relevant locations in the original text.

```markdown
This runs on a svr[Proofread: "svr" → "server" (Reason: Notation variation. "server" is the primary notation in this article)] application. Data can be saved using the save function[Proofread: "can be saved using the save function" → "can be saved" (Reason: Redundant expression)].
```

### Summary Report

Statistics are output at the end of the proofreading results.

```markdown
---
## Proofreading Summary

### Detection Count
| Category | Count |
|----------|-------|
| Accuracy (typos) | 3 |
| Grammar | 2 |
| Consistency (notation variations) | 5 |
| Readability | 4 |
| Structure | 1 |
| **Total** | **15** |

### Readability Score: 72/100
- Average sentence length: 42 characters (appropriate)
- Difficult kanji ratio: 3% (slightly high)
- Redundant expressions: 4 locations

### By Severity
| Severity | Count |
|----------|-------|
| HIGH | 3 |
| MEDIUM | 8 |
| LOW | 4 |

### Top 5 Critical Fixes
1. [HIGH] L12: Homophone misuse
2. [HIGH] L34: Subject and predicate do not agree
3. [HIGH] L56: Notation variation (5 instances)
4. [MEDIUM] L23: Sentence exceeds 120 characters
5. [MEDIUM] L45: Redundant expression
```

## Readability Score Calculation

The readability score (0-100) is calculated from the following elements.

| Element | Points | Criteria |
|---------|--------|----------|
| Average sentence length | 30 pts | 40 chars or less: 30, 60 or less: 20, 80 or less: 10, above: 0 |
| Kanji ratio | 20 pts | 20-35%: 20, 35-45%: 15, other: 10 |
| Redundancy ratio | 20 pts | 0%: 20, reduced proportionally |
| Paragraph appropriateness | 15 pts | 3-5 sentences per paragraph: 15, other: reduced |
| Conjunction appropriateness | 15 pts | Clear connections between paragraphs: 15 |

## Requirements

- **API Key**: GEMINI_API_KEY or GOOGLE_API_KEY (environment variable or .env)
- **Python Packages**: google-genai, pyyaml, python-dotenv

## Related Skills

- **document-processor**: Integrated processing of PDF/PPTX/Excel
- **pptx-analyzer**: PowerPoint slide structure analysis
- **screenshot-analyzer**: Information extraction from screenshots
