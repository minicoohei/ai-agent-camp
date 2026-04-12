---
name: article-writer
description: "An article writing skill that generates outlines from themes, applies style profiles, and outputs Markdown articles. Supports automatic illustration marker insertion and style unification via style-analyzer profiles. Triggered by requests like 'write an article', 'create a blog post', 'generate article from theme', etc."
triggers:
  - article-writer
  - write an article
  - create blog post
  - generate article from theme
  - article writing
  - create outline
  - Markdown article
  - 記事を書いて
  - ブログ作成
---

# Article Writer - AI Article Writing Engine

Automatically generates structured Markdown articles simply by entering a theme. Supports tone unification through style profiles and automatic insertion of illustration markers, producing consistent, high-quality articles.

## Workflow

```
Theme input -> Outline generation -> Style application -> Section writing -> Illustration marker insertion -> Consistency check -> Markdown output
```

1. **Theme analysis and outline generation**: Automatically designs section structure, headings, and key points from the theme
2. **Style profile loading**: Style (tone, sentence endings, vocabulary level, etc.) can be specified via YAML file
3. **Section-by-section draft writing**: Generates each section via Gemini API following the outline
4. **Automatic illustration marker insertion**: Automatically places insertion points for figures/images as HTML comments
5. **Overall consistency check**: Verifies style and terminology consistency and outputs final Markdown

## Usage

```bash
# Basic article generation
python scripts/article_writer.py --theme "How to Use AI Agents" --output output/article.md

# With style profile
python scripts/article_writer.py --theme "How to Use AI Agents" --style style_profile.yaml --output output/article.md

# With target audience
python scripts/article_writer.py --theme "How to Use AI Agents" --audience "Non-engineer business professionals" --style style_profile.yaml

# Specify word count and section count
python scripts/article_writer.py --theme "Introduction to Data Analysis" --word-count 5000 --sections 7

# Disable illustration markers
python scripts/article_writer.py --theme "Project Management" --illustrations none

# Test mode (no API call)
python scripts/article_writer.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --theme | Yes | - | Article theme/topic |
| --style | No | - | Path to style profile YAML file |
| --audience | No | - | Target audience (e.g., "Non-engineer business professionals") |
| --output | No | auto | Output file path (default: output/article_{timestamp}.md) |
| --word-count | No | 3000 | Target word count |
| --sections | No | auto | Number of sections (auto determines from theme) |
| --illustrations | No | auto | Illustration markers: auto (auto-insert) / manual (position only) / none (none) |
| --test | No | false | Test mode (generates sample article without API calls) |

## Illustration Marker Format

Illustration insertion points are indicated in the article using the following HTML comment format. Actual images can be generated with subsequent skills (nanobanana, diagram-generator, etc.).

```html
<!-- illustration: type=diagram description="Flow diagram: AI agent processing steps" -->

<!-- illustration: type=image description="Person using AI in a modern office" -->
```

| type | Description | Recommended Skill |
|------|-------------|-------------------|
| diagram | Flowcharts, architecture diagrams, UML diagrams | diagram-generator |
| image | Photo-style, illustrations, concept images | nanobanana |
| chart | Graphs, data visualizations | data-analyst |
| screenshot | UI screen captures | screenshot-annotator |

## Style Profile Format

Style is specified via YAML file (can be auto-generated with the style-analyzer skill).

```yaml
tone: professional        # professional / casual / academic / friendly
formality: high            # high / medium / low
sentence_ending: desu-masu  # desu-masu / da-dearu / mixed
vocabulary_level: general   # general / technical / simple
paragraph_length: medium    # short / medium / long
use_examples: true
use_metaphors: false
target_audience: "Business professionals"
brand_voice: "Trustworthy and easy to understand"
avoid_words:
  - "basically"
  - "honestly"
preferred_expressions:
  - "specifically"
  - "for example"
```

## Output Format

Article file in Markdown format. Output with the following structure.

```markdown
# Article Title

> Lead paragraph (article summary/introduction)

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- ...

## Section 1

Body text...

<!-- illustration: type=diagram description="..." -->

## Section 2

Body text...

<!-- illustration: type=image description="..." -->

## Conclusion

Conclusion text...
```

## Parallel Execution

When generating articles for multiple themes simultaneously, multiple agents can be launched for parallel processing.

```bash
# Parallel execution for multiple themes
python scripts/article_writer.py --theme "AI Applications" --output output/ai.md &
python scripts/article_writer.py --theme "DX Promotion" --output output/dx.md &
wait
```

## Requirements

- **API Key**: Set GEMINI_API_KEY or GOOGLE_API_KEY as environment variable
- **Python packages**: google-genai, pyyaml, python-dotenv

## Related Skills

| Skill | Integration |
|-------|-------------|
| **style-analyzer** | Auto-generates style profile from reference text -> pass to --style |
| **proofreading-agent** | Proofreading and revision of generated articles |
| **fact-checker** | Verifies factual accuracy in articles |
| **nanobanana** | Generates actual images from illustration markers (type=image) |
| **diagram-generator** | Generates flow diagrams etc. from illustration markers (type=diagram) |
