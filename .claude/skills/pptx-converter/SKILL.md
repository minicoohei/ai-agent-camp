---
name: pptx-converter
description: "PPTXテンプレート変換 & ゼロからデッキ生成。テーマ・アニメーション・SmartArtを保持してコンテンツを書き換え。 「PPTX変換」「スライド作成」「パワポ書き換え」「デッキ生成」等のリクエストで発動。"
triggers:
  - PPTX変換
  - スライド作成
  - パワポ書き換え
  - デッキ生成
  - pptx-converter
  - PowerPoint変換
  - テンプレートを使ってスライド作成
version: 1.0.0
author: CursorBootcamp
dependencies:
  - python: 3.8+
  - packages: ["python-pptx", "pyyaml", "lxml", "google-generativeai", "python-dotenv", "Pillow"]
---

## トリガーワード
「PPTX変換」「スライド作成」「パワポ書き換え」「デッキ生成」「PowerPoint」

# PPTX Converter

PowerPointファイルのテンプレート変換とゼロからのデッキ生成ツール。

## 機能

### 1. convert - テンプレート変換（1コマンド完結）
元PPTXをコピーして、全要素をGeminiで意味解析し、新トピックに合わせてコンテンツを自動書き換え。

```bash
python skills/pptx-converter/scripts/pptx_converter.py convert \
    source.pptx \
    --topic "2026年Q1営業報告" \
    -o output/slides/q1_report.pptx
```

**保持されるもの:** スライドマスター、テーマカラー、フォント定義、アニメーション、トランジション、SmartArt構造、レイアウト配置

### 2. extract - マッピングYAML生成
元PPTXの全要素を抽出・意味解析し、座標-要素マッピングYAMLを生成。手動確認・編集用。

```bash
python skills/pptx-converter/scripts/pptx_converter.py extract \
    source.pptx \
    -o mapping.yaml
```

### 3. build - マッピング + データ → PPTX
手動編集したデータYAMLで要素を書き換え。

```bash
python skills/pptx-converter/scripts/pptx_converter.py build \
    source.pptx \
    mapping.yaml \
    --data data.yaml \
    -o output.pptx
```

### 4. deck - ゼロからデッキ生成
トピックからGeminiでアウトライン生成 → PPTX自動作成。

```bash
python skills/pptx-converter/scripts/pptx_converter.py deck \
    --topic "AIエージェント活用提案" \
    --type proposal \
    --style corporate \
    -o output/slides/proposal.pptx
```

**deck オプション:**
- `--type`: auto / presentation / proposal / report / educational / pitch
- `--style`: corporate / creative / minimal / academic
- `--slides N`: スライド枚数（0=AI決定）
- `--audience`: 対象者
- `--outline-only`: アウトラインYAMLのみ出力

## 対応要素タイプ

| タイプ | 抽出 | 書き換え | 備考 |
|--------|:----:|:--------:|------|
| テキスト | o | o | スタイル（フォント・色・太字等）完全保持 |
| チャート | o | o | chart.replace_data() でデータのみ差し替え |
| テーブル | o | o | セルスタイル保持、行列内容のみ差し替え |
| 画像 | o | o | デフォルト保持、個別に差し替え指定可能 |
| 図形 | o | o | 図形内テキストの差し替え |
| グループ | o | o | 子要素を再帰的に処理（深さ3まで） |
| SmartArt | o | 部分 | テキストノードのみXML直接操作で差し替え |

## マッピングYAML構造

```yaml
source: "source.pptx"
generated_at: "2026-02-09T15:30:00"
slide_width: 12192000
slide_height: 6858000

slides:
  - slide_number: 1
    layout: "Title Slide"
    elements:
      - id: 2
        name: "Title 1"
        type: text
        role: title
        hint: "メインタイトル。15-25文字。"
        position: { left: 457200, top: 274638, width: 8229600, height: 1143000 }
        style: { font: "Meiryo UI", size: 36, bold: true, color: "2563EB" }
        value: "2025年度 営業戦略"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "2025年度 営業戦略"
```

## ワークフロー判断

- **テンプレートPPTXがある** → `convert`（1コマンド完結）
- **マッピングを手動確認したい** → `extract` → YAML編集 → `build`
- **ゼロから作成** → `deck`

## 環境変数

- `GEMINI_API_KEY` or `GOOGLE_API_KEY`: Gemini API キー（必須）
- `GEMINI_FLASH_MODEL`: テキスト処理モデル（デフォルト: gemini-2.5-flash）
