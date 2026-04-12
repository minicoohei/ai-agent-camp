---
name: style-analyzer
description: |
  ユーザーの既存文章を複数読み込み、文体特徴（語尾パターン、文の長さ、漢字/ひらがな比率、口調、接続詞傾向）を抽出してスタイルプロファイルを生成する。
  「文体を分析して」「書き方を真似て」「文章のスタイルを学習」等のリクエストで発動。
triggers:
  - 文体を分析
  - 文章のスタイルを学習
  - 書き方を真似て
  - ライティングスタイルを抽出
  - トーン分析
  - style-analyzer
  - style profile
---

## トリガーワード
「文体分析」「トーン分析」「ライティングスタイル」「文章スタイル」

# Style Analyzer - 文体分析・プロファイル生成

ユーザーが書いた複数の文章ファイルを読み込み、文体の特徴を定量的に抽出してスタイルプロファイル（YAML形式）を生成します。生成されたプロファイルは、文体を再現した文章生成や、文体の一貫性チェックに活用できます。

## 機能

1. **語尾パターン分析**: です/ます調、だ/である調、混合型を判定
2. **文長分析**: 一文あたりの平均文字数、最短・最長文字数
3. **文字種比率**: 漢字・ひらがな・カタカナ・ASCII・記号の出現比率
4. **接続詞分析**: 使用される接続詞の種類と頻度を集計
5. **段落構造**: 段落あたりの平均文数を算出
6. **体言止め検出**: 体言止めの使用頻度を計測
7. **句読点パターン**: 全角/半角句読点の使い分けを判定
8. **修飾語分析**: 修飾語・副詞の出現密度を推定
9. **口語/文語バランス**: 口語的表現と文語的表現の比率を推定

## Usage

```bash
# 基本的な使い方（複数ファイルを指定）
python scripts/style_analyzer.py --input "article1.md" --input "article2.md"

# 出力先を指定
python scripts/style_analyzer.py --input "article1.md" --input "article2.md" --output style_profile.yaml

# 3つ以上のファイルを分析
python scripts/style_analyzer.py \
  --input "blog_post_1.md" \
  --input "blog_post_2.md" \
  --input "report.txt" \
  --output my_style.yaml

# テストモード（サンプルプロファイルを生成）
python scripts/style_analyzer.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes* | - | 分析対象のテキスト/Markdownファイルパス（複数指定可） |
| --output | No | output/style_profile.yaml | 出力YAMLファイルのパス |
| --test | No | false | テストモード：サンプルプロファイルを生成して終了 |

\* `--test` 使用時は `--input` は不要

## 分析項目

### 語尾パターン（sentence_endings）

| 分類 | 該当パターン | 例 |
|------|-------------|-----|
| desu_masu | です、ます、でした、ました、ません、でしょう | 「AIは便利です」 |
| da_dearu | だ、である、であった、だった、ではない | 「AIは便利である」 |
| other | 疑問形、感嘆、体言止め等 | 「AIは便利？」「便利なAI。」 |

### 文字種比率（char_ratios）

Unicode範囲に基づいて各文字種の比率を算出:

- **漢字**: U+4E00 - U+9FFF, U+3400 - U+4DBF
- **ひらがな**: U+3040 - U+309F
- **カタカナ**: U+30A0 - U+30FF
- **ASCII**: U+0020 - U+007E
- **その他**: 上記以外（記号・絵文字等）

### 接続詞（conjunctions）

検出対象の主な接続詞:

| カテゴリ | 接続詞 |
|---------|--------|
| 順接 | だから、したがって、そのため、それで、ゆえに |
| 逆接 | しかし、だが、ところが、けれども、にもかかわらず、一方で |
| 並列・累加 | また、さらに、そして、加えて、それに、そのうえ |
| 説明・補足 | つまり、すなわち、要するに、なぜなら、というのも |
| 転換 | さて、ところで、では、それでは、ちなみに |
| 対比 | むしろ、逆に、反対に、それに対して |
| 例示 | たとえば、具体的には、いわば |

### 体言止め（taigen_dome）

文末が名詞・名詞句で終わるパターンを検出（「。」の直前が漢字・カタカナ・ひらがな名詞で終わる場合）。

### 句読点パターン（punctuation）

| パターン名 | 句点 | 読点 |
|-----------|------|------|
| standard | 。 | 、 |
| academic | ．(全角ピリオド) | ，(全角カンマ) |
| mixed | 混合 | 混合 |

## 出力形式

YAML形式のスタイルプロファイル:

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
      - word: "また"
        count: 8
      - word: "しかし"
        count: 6
      - word: "そして"
        count: 5
      - word: "さらに"
        count: 4
      - word: "つまり"
        count: 3

  paragraph_structure:
    avg_sentences_per_paragraph: 5.1

  taigen_dome:
    frequency: 0.07
    count: 10

  punctuation:
    period_style: "。"
    comma_style: "、"
    pattern: "standard"

  modifiers:
    density: 0.12
    common_adverbs:
      - "非常に"
      - "特に"
      - "実際に"

  colloquial_formal_balance:
    colloquial_ratio: 0.25
    formal_ratio: 0.75
    assessment: "やや文語寄り"
```

## Examples

### ブログ記事の文体分析

```bash
python scripts/style_analyzer.py \
  --input "blog/2026-01-intro.md" \
  --input "blog/2026-01-review.md" \
  --input "blog/2026-02-tips.md" \
  --output output/blog_style.yaml
```

出力例（stdout）:

```
=== Style Analyzer - 文体分析レポート ===

分析ファイル数: 3
総文字数: 8,420
総文数: 215

--- 語尾パターン ---
  です/ます調: 78.1%
  だ/である調: 12.6%
  その他: 9.3%
  → 主要スタイル: です/ます調

--- 文長 ---
  平均: 39.2文字  中央値: 35.0文字
  最短: 5文字  最長: 102文字

--- 文字種比率 ---
  漢字: 30.5%  ひらがな: 48.2%  カタカナ: 8.1%

--- 接続詞 TOP5 ---
  また(12) しかし(8) そして(7) さらに(5) つまり(4)

--- 体言止め ---
  使用率: 6.5% (14回/215文)

プロファイル保存先: output/blog_style.yaml
```

### テストモード

```bash
python scripts/style_analyzer.py --test
```

入力ファイルなしでサンプルプロファイルを生成し、出力形式を確認できます。

## Requirements

- Python 3.8+
- 外部ライブラリ不要（標準ライブラリのみで動作）

## Related Skills

- **article-writer**: スタイルプロファイルを読み込んで文体を再現した記事を生成
- **copy-editing**: 文体の一貫性チェックや校正に活用
