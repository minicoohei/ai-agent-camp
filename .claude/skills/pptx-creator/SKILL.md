---
name: pptx-creator
description: |
  トピックを入力するだけで、テンプレートのデザインを維持した .pptx を自動生成するスキル。
  「プレゼンを作って」「スライド生成」「PPTX作成」「提案資料を作成」等のリクエストで発動。
triggers:
  - プレゼンを作って
  - スライド生成
  - PPTX作成
  - 提案資料を作成
  - pptx-creator
  - PowerPoint作成
  - デッキを作って
---

# /pptx-creator — PPTX プレゼンテーション自動生成 v2

トピックを入力するだけで、テンプレートのデザインを維持した編集可能な .pptx ファイルを自動生成します。
生成後に画像エクスポート + Gemini Vision 品質検証が可能です。

## トリガー

以下のようなリクエストで発動:
- 「プレゼン作って」「スライド生成」「PPTX作成」「デッキ生成」
- 「〜についてのプレゼンを作って」
- 「提案資料を作成」「報告書スライドを生成」

## 仕組み

1. **Gemini Flash** でトピックから構造化アウトライン（YAML）を生成
2. テンプレート PPTX のデザイン（マスター/テーマ/フォント）を維持
3. **レイアウトPH注入** + **リッチ要素コード生成** のハイブリッドで高品質スライド生成
4. **画像エクスポート** + **Gemini Vision 品質レビュー**（`--verify`）

## テンプレート

| テンプレート | サイズ | フォント | 特徴 |
|-------------|--------|---------|------|
| `simple` | 13.333" x 7.5" | 游ゴシック | シンプル・汎用、PH注入方式 |
| `standard` | 20.0" x 11.25" | Noto Sans JP + Futura | 本格デザイン、code_gen方式 |

## スライドタイプ（11種）

| タイプ | 説明 |
|--------|------|
| `title` | 表紙スライド（中央タイトル + サブタイトル + アクセントライン） |
| `section` | セクション区切り（番号 + タイトル + アクセントバー） |
| `content` | 箇条書きコンテンツ（タイトルバー + 箇条書き） |
| `key_message` | 1つの主要メッセージを大きく中央表示 |
| `two_column` | 2列レイアウト（角丸カード内に左右コンテンツ） |
| `comparison` | 左右比較（ヘッダーバー + 箇条書き） |
| `agenda` | 番号付きアジェンダ（円番号 + 区切り線） |
| `closing` | 締めスライド（Thank you + アクセントライン） |
| `kpi_dashboard` | KPIカード表示（3-4個、角丸カード + 変化率） |
| `process_flow` | プロセスフロー（番号付き円 + 矢印 + 説明） |
| `table` | テーブル表示（ヘッダー行アクセント + 交互背景） |

## 使い方

### トピックからPPTX生成

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "AI活用提案" \
  --template simple \
  -o output/slides/proposal.pptx
```

### 生成 + 品質検証（推奨）

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "Q1業績報告" \
  --template standard \
  --slides 10 \
  --verify \
  -o output/slides/q1_report.pptx
```

### アウトラインのみ生成（ドライラン）

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "新規事業計画" \
  --dry-run \
  --save-outline /tmp/outline.yaml
```

### 画像エクスポート単体

```bash
python skills/pptx-creator/scripts/export_to_images.py \
  output/slides/proposal.pptx \
  -o output/slides/proposal_images/
```

### 品質レビュー単体

```bash
python skills/pptx-creator/scripts/quality_reviewer.py \
  output/slides/proposal_images/ \
  --threshold 7.0
```

## パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `--topic` | *1 | - | プレゼンのトピック |
| `--outline` | *1 | - | 既存アウトラインYAMLパス |
| `--template` | No | simple | テンプレート名 (simple/standard) |
| `--output` / `-o` | No | 自動生成 | 出力PPTXパス |
| `--slides` / `-n` | No | 8 | スライド枚数 |
| `--audience` | No | business | 対象聴衆 |
| `--language` / `-l` | No | ja | 出力言語 (ja/en) |
| `--save-outline` | No | - | アウトラインYAML保存先 |
| `--dry-run` | No | false | アウトライン生成のみ |
| `--verify` | No | false | 生成後に画像エクスポート + 品質検証 |
| `--verify-threshold` | No | 7.0 | 品質検証の合格スコア閾値 |

*1: `--topic` と `--outline` は排他必須

## テンプレート配置

```text
skills/pptx-creator/templates/
├── simple/template.pptx      ← ICHIBAN_SIMPLE_PPTXtemplate_游ゴシック.pptx
└── standard/template.pptx    ← template_basic.pptx
```

## 依存関係

- Python 3.8+
- `python-pptx` — PPTX操作
- `google-genai` — Gemini API
- `pyyaml` — YAML処理
- `python-dotenv` — 環境変数
- `libreoffice` — 画像エクスポート（--verify 使用時）
- `poppler-utils` — PDF→PNG変換（--verify 使用時）
- 環境変数: `GEMINI_API_KEY` または `GOOGLE_API_KEY`

## エージェント向け実行手順

ユーザーが「プレゼンを作って」等のリクエストをした場合:

1. トピックと要件をヒアリング
2. 以下のコマンドを実行:

```bash
python skills/pptx-creator/scripts/pptx_creator.py \
  --topic "<ユーザーのトピック>" \
  --template simple \
  --slides <枚数> \
  --verify \
  -o output/slides/<ファイル名>.pptx
```

3. 品質チェック結果を確認
4. 不合格の場合はアウトラインを修正して再生成
5. 出力ファイルパスをユーザーに伝達

## Overview

トピックを入力するだけで、テンプレートのデザインを維持した編集可能な .pptx ファイルを自動生成するスキルです。Gemini Flash でアウトライン（YAML）を生成し、11種類のスライドタイプに対応。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| API key not found | `GEMINI_API_KEY` または `GOOGLE_API_KEY` を環境変数に設定 |
| Template not found | `skills/pptx-creator/templates/` にテンプレートファイルが配置されているか確認 |
| LibreOffice not found | `--verify` 使用時は `libreoffice` のインストールが必要 |

## Success Criteria

- [ ] 指定枚数のスライドを含む .pptx ファイルが生成されている
- [ ] `--verify` 指定時に品質スコアが閾値以上である
- [ ] テンプレートのフォント・カラースキームが維持されている

## Usage

上記「使い方」セクションを参照。基本例:

```bash
python skills/pptx-creator/scripts/pptx_creator.py --topic "AI活用提案" --template simple --verify -o output/slides/proposal.pptx
```
