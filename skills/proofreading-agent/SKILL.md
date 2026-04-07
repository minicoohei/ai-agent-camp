---
name: proofreading-agent
description: "日本語記事の校閲エージェント。誤字脱字、文法、表現の一貫性、読みやすさをチェックし、修正提案をインライン注釈で出力する。「校閲して」「文章をチェック」「誤字脱字を確認」「記事をレビュー」などのリクエストで使用。"
---

## トリガーワード
「校閲して」「文章チェック」「誤字脱字」「推敲」「校正」

# Proofreading Agent - 日本語記事校閲エージェント

日本語記事を体系的に校閲するエージェントです。コピーエディティングの「Seven Sweeps」手法にインスパイアされ、日本語コンテンツに最適化した **Five Sweeps** で記事を多角的にレビューします。

## Five Sweeps（5段階校閲）

校閲は以下の5段階で実施します。各スイープは独立して実行でき、特定のカテゴリに集中したレビューも可能です。

### 1. 正確性チェック（Accuracy）

文字レベルの誤りを検出します。

- **誤字脱字**: 漢字の変換ミス、タイプミス
- **送り仮名の誤り**: 「行なう」→「行う」、「落し穴」→「落とし穴」
- **同音異義語の誤用**: 「以外」と「意外」、「対象」と「対称」
- **固有名詞の表記ミス**: 製品名、人名、組織名の正確性

### 2. 文法チェック（Grammar）

文法的な正しさを検証します。

- **主述のねじれ**: 主語と述語の不一致
- **助詞の誤用**: 「は」と「が」、「に」と「へ」の使い分け
- **敬語の統一**: 尊敬語・謙譲語・丁寧語の混在
- **係り受けの誤り**: 修飾語と被修飾語の関係
- **時制の不一致**: 過去形と現在形の混在

### 3. 一貫性チェック（Consistency）

記事全体を通した表記の統一性を確認します。

- **表記揺れ**: 「サーバー」と「サーバ」、「ユーザー」と「ユーザ」
- **語尾の統一**: 「です・ます」調と「だ・である」調の混在
- **数字表記**: 全角と半角の混在、「3つ」と「三つ」
- **記号の統一**: 括弧の種類、句読点（、。と，．）
- **略語の統一**: 初出でのフルスペル表記

### 4. 読みやすさチェック（Readability）

文章の読みやすさを評価します。

- **一文の長さ**: 80文字を超える文の検出
- **難読漢字**: 一般読者に難しい漢字の使用
- **冗長表現**: 「することができる」→「できる」
- **二重否定**: 「ないわけではない」→「ある」
- **受身形の多用**: 能動態への書き換え提案
- **カタカナ語の乱用**: 日本語で十分伝わる箇所の指摘

### 5. 構成チェック（Structure）

記事全体の構成と論理展開を確認します。

- **段落の論理的つながり**: 前後の段落間の接続
- **重複内容**: 同じ情報の不要な繰り返し
- **情報の過不足**: 説明不足の箇所、不要な情報
- **見出しの階層**: 見出しレベルの適切さ
- **導入と結論の整合性**: 冒頭の問題提起と結論の対応

## Usage

```bash
# 全スイープで校閲（デフォルト）
python scripts/proofreading_agent.py --input article.md --output review.md

# 特定のスイープのみ実行
python scripts/proofreading_agent.py --input article.md --sweep accuracy
python scripts/proofreading_agent.py --input article.md --sweep grammar
python scripts/proofreading_agent.py --input article.md --sweep consistency
python scripts/proofreading_agent.py --input article.md --sweep readability
python scripts/proofreading_agent.py --input article.md --sweep structure

# スタイルプロファイルを指定
python scripts/proofreading_agent.py --input article.md --style style_profile.yaml

# 重要度フィルタ（high のみ表示）
python scripts/proofreading_agent.py --input article.md --severity high

# テストモード（API不要、サンプルテキストで動作確認）
python scripts/proofreading_agent.py --test
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes* | - | 校閲対象のファイルパス（Markdown/テキスト）。--test 時は不要 |
| --output | No | output/review_{timestamp}.md | 校閲結果の出力先 |
| --sweep | No | all | 実行するスイープ: all, accuracy, grammar, consistency, readability, structure |
| --style | No | - | スタイルプロファイル（YAML）のパス |
| --severity | No | medium | 表示する最低重要度: low, medium, high |
| --test | No | false | テストモード（サンプルテキストで API 不要の動作確認） |

## スタイルプロファイル（YAML）

記事の種類に応じたルールをカスタマイズできます。

```yaml
# style_profile.yaml の例
name: "技術ブログ"
tone: "です・ます"
terminology:
  preferred:
    - { term: "サーバー", reject: ["サーバ"] }
    - { term: "ユーザー", reject: ["ユーザ"] }
    - { term: "インターフェース", reject: ["インタフェース", "インターフェイス"] }
  domain_terms:
    - "API"
    - "SDK"
    - "CI/CD"
rules:
  max_sentence_length: 80
  number_style: "半角"
  punctuation: "、。"
```

## Output Format

### インライン注釈

原文中の該当箇所に直接注釈を挿入します。

```markdown
これはサーバ[校閲: 「サーバ」→「サーバー」（理由: 表記揺れ。記事内で「サーバー」が主要表記）]で動作する
アプリケーションです。データを保存することができます[校閲: 「保存することができます」→「保存できます」（理由: 冗長表現）]。
```

### サマリーレポート

校閲結果の末尾に統計情報を出力します。

```markdown
---
## 校閲サマリー

### 検出件数
| カテゴリ | 件数 |
|---------|------|
| 正確性（誤字脱字） | 3 |
| 文法 | 2 |
| 一貫性（表記揺れ） | 5 |
| 読みやすさ | 4 |
| 構成 | 1 |
| **合計** | **15** |

### 読みやすさスコア: 72/100
- 平均文長: 42文字（適切）
- 難読漢字率: 3%（やや高い）
- 冗長表現: 4箇所

### 重要度別
| 重要度 | 件数 |
|--------|------|
| HIGH | 3 |
| MEDIUM | 8 |
| LOW | 4 |

### 最重要修正 Top 5
1. [HIGH] L12: 「以外」→「意外」（同音異義語の誤用）
2. [HIGH] L34: 主語と述語が一致していない
3. [HIGH] L56: 「サーバ」と「サーバー」の表記揺れ（計5箇所）
4. [MEDIUM] L23: 一文が120文字を超えている
5. [MEDIUM] L45: 「することができる」→「できる」
```

## 読みやすさスコア算出

読みやすさスコア（0-100）は以下の要素から算出します。

| 要素 | 配点 | 基準 |
|------|------|------|
| 平均文長 | 30点 | 40文字以下: 30点、60文字以下: 20点、80文字以下: 10点、それ以上: 0点 |
| 漢字含有率 | 20点 | 20-35%: 20点、35-45%: 15点、それ以外: 10点 |
| 冗長表現率 | 20点 | 0%: 20点、冗長表現の割合に応じて減点 |
| 段落の適切さ | 15点 | 1段落あたり3-5文: 15点、それ以外: 減点 |
| 接続詞の適切さ | 15点 | 段落間の接続が明確: 15点 |

## Requirements

- **API キー**: GEMINI_API_KEY または GOOGLE_API_KEY（環境変数または .env）
- **Python パッケージ**: google-genai, pyyaml, python-dotenv

## Related Skills

- **document-processor**: PDF/PPTX/Excel の統合処理
- **pptx-analyzer**: PowerPoint スライド構造解析
- **screenshot-analyzer**: スクリーンショットから情報抽出
