---
name: style-analyzer
description: "Reads multiple existing texts by the user, extracts writing style features (sentence ending patterns, sentence length, kanji/hiragana ratio, tone, conjunction tendencies), and generates a style profile. Triggered by requests like 'Analyze writing style', 'Mimic this writing', 'Learn writing style', etc."
triggers:
  - Analyze writing style
  - Learn writing style
  - Mimic this writing
  - Extract writing style
  - Tone analysis
  - style-analyzer
  - style profile
---

## Trigger Words
"Style analysis", "Tone analysis", "Writing style", "Text style"

# Style Analyzer - Writing Style Analysis & Profile Generation

Reads multiple text files written by the user, quantitatively extracts writing style features, and generates a style profile (YAML format). The generated profile can be used for reproducing the writing style in text generation or for checking style consistency.

## Features

1. **Sentence ending pattern analysis**: Determines polite form (desu/masu), plain form (da/dearu), or mixed
2. **Sentence length analysis**: Average, shortest, and longest character count per sentence
3. **Character type ratio**: Occurrence ratio of kanji, hiragana, katakana, ASCII, and symbols
4. **Conjunction analysis**: Tallies types and frequencies of conjunctions used
5. **Paragraph structure**: Calculates average number of sentences per paragraph
6. **Noun-ending detection**: Measures frequency of sentences ending with nouns
7. **Punctuation patterns**: Determines full-width/half-width punctuation usage
8. **Modifier analysis**: Estimates density of modifiers and adverbs
9. **Colloquial/formal balance**: Estimates ratio of colloquial vs. literary expressions

## Usage

```bash
# Basic usage (specify multiple files)
python scripts/style_analyzer.py --input "article1.md" --input "article2.md"

# Specify output destination
python scripts/style_analyzer.py --input "article1.md" --input "article2.md" --output style_profile.yaml

# Analyze 3+ files
python scripts/style_analyzer.py \
  --input "blog_post_1.md" \
  --input "blog_post_2.md" \
  --input "report.txt" \
  --output my_style.yaml

# Test mode (generate sample profile)
python scripts/style_analyzer.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes* | - | Path to text/Markdown file for analysis (multiple allowed) |
| --output | No | output/style_profile.yaml | Output YAML file path |
| --test | No | false | Test mode: generates sample profile and exits |

\* `--input` is not required when using `--test`

## Analysis Items

### Sentence Ending Patterns (sentence_endings)

| Classification | Matching Patterns | Example |
|----------------|-------------------|---------|
| desu_masu | desu, masu, deshita, mashita, masen, deshou | Polite form |
| da_dearu | da, dearu, deatta, datta, dewanai | Plain/academic form |
| other | Interrogative, exclamatory, noun-ending, etc. | Questions, emphasis |

### Character Type Ratio (char_ratios)

Ratio of each character type calculated based on Unicode ranges:

- **Kanji**: U+4E00 - U+9FFF, U+3400 - U+4DBF
- **Hiragana**: U+3040 - U+309F
- **Katakana**: U+30A0 - U+30FF
- **ASCII**: U+0020 - U+007E
- **Other**: Everything else (symbols, emoji, etc.)

### Conjunctions (conjunctions)

Main conjunctions detected:

| Category | Conjunctions |
|----------|-------------|
| Consequential | dakara, shitagatte, sonotame, sorede, yueni |
| Adversative | shikashi, daga, tokoroga, keredomo, nimokakawarazu, ippode |
| Parallel/Additive | mata, sarani, soshite, kuwaete, soreni, sonoueni |
| Explanatory/Supplementary | tsumari, sunawachi, yousuruni, nazenara, toiunomo |
| Transitional | sate, tokorode, dewa, soredewa, chinamini |
| Contrastive | mushiro, gyakuni, hantaini, sorenishite |
| Exemplary | tatoeba, gutaitekiniwa, iwaba |

### Noun-ending (taigen_dome)

Detects patterns where sentences end with a noun or noun phrase.

### Punctuation Patterns (punctuation)

| Pattern Name | Period | Comma |
|-------------|--------|-------|
| standard | Japanese period | Japanese comma |
| academic | Full-width period | Full-width comma |
| mixed | Mixed | Mixed |

## Output Format

Style profile in YAML format:

```yaml
style_profile:
  generated_at: "2026-02-12T10:30:00+09:00"
  source_files:
    - path: "article1.md"
      chars: 2450
    - path: "article2.md"
      chars: 3120
  total_chars: 5570
  total_sentences: 142
  total_paragraphs: 28

  sentence_endings:
    desu_masu: 0.72
    da_dearu: 0.18
    other: 0.10
    dominant_style: "desu_masu"

  sentence_length:
    average: 39.2
    median: 35.0
    min: 8
    max: 98
    std_dev: 15.4

  char_ratios:
    kanji: 0.31
    hiragana: 0.48
    katakana: 0.08
    ascii: 0.06
    other: 0.07

  conjunctions:
    total_count: 34
    per_sentence: 0.24
    top_5:
      - word: "mata"
        count: 8
      - word: "shikashi"
        count: 6
      - word: "soshite"
        count: 5
      - word: "sarani"
        count: 4
      - word: "tsumari"
        count: 3

  paragraph_structure:
    avg_sentences_per_paragraph: 5.1

  taigen_dome:
    frequency: 0.07
    count: 10

  punctuation:
    period_style: "Japanese period"
    comma_style: "Japanese comma"
    pattern: "standard"

  modifiers:
    density: 0.12
    common_adverbs:
      - "hijou-ni (very)"
      - "tokuni (especially)"
      - "jissaini (actually)"

  colloquial_formal_balance:
    colloquial_ratio: 0.25
    formal_ratio: 0.75
    assessment: "Slightly literary-leaning"
```

## Examples

### Blog Article Style Analysis

```bash
python scripts/style_analyzer.py \
  --input "blog/2026-01-intro.md" \
  --input "blog/2026-01-review.md" \
  --input "blog/2026-02-tips.md" \
  --output output/blog_style.yaml
```

Output example (stdout):

```
=== Style Analyzer - Writing Style Report ===

Files analyzed: 3
Total characters: 8,420
Total sentences: 215

--- Sentence Ending Patterns ---
  Polite form (desu/masu): 78.1%
  Plain form (da/dearu): 12.6%
  Other: 9.3%
  -> Dominant style: Polite form (desu/masu)

--- Sentence Length ---
  Average: 39.2 chars  Median: 35.0 chars
  Min: 5 chars  Max: 102 chars

--- Character Type Ratio ---
  Kanji: 30.5%  Hiragana: 48.2%  Katakana: 8.1%

--- Top 5 Conjunctions ---
  mata(12) shikashi(8) soshite(7) sarani(5) tsumari(4)

--- Noun-ending ---
  Usage rate: 6.5% (14/215 sentences)

Profile saved to: output/blog_style.yaml
```

### Test Mode

```bash
python scripts/style_analyzer.py --test
```

Generates a sample profile without input files to confirm the output format.

## Requirements

- Python 3.8+
- No external libraries required (runs on standard library only)

## Related Skills

- **article-writer**: Loads the style profile to generate articles reproducing the writing style
- **copy-editing**: Uses the profile for style consistency checks and proofreading
