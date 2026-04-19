---
name: gslides-creator
description: "テンプレートから Google Slides を作成するスキル。 「Google Slidesを作って」「スライド生成」「プレゼン作成」等のリクエストで発動。 GAS + clasp CLI でテンプレートコピー・コンテンツ書き換え・ゼロからのデッキ生成を行う。"
triggers:
  - gslides-creator
  - Google Slides作成
  - スライド生成
  - プレゼン作成
  - テンプレートからスライド
  - gslides
---

# /gslides-creator - Google Slides クリエーター

テンプレートからGoogle Slidesを作成、またはゼロからデッキを生成する。

## 前提条件

```bash
# clasp ログイン済み
clasp login

# GAS API 有効化
# https://script.google.com/home/usersettings

# gslides-parser が設定済み（convert コマンドで使用）
python skills/gslides-parser/scripts/gslides_parser.py setup
```

## クイックスタート

```bash
# 1. GAS プロジェクト初期設定（初回のみ）
python skills/gslides-creator/scripts/gslides_creator.py setup

# 2. テンプレートから新トピックで作成
python skills/gslides-creator/scripts/gslides_creator.py convert \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  --topic "エンジニア向け Claude Code 実践講座" \
  --title "Claude Code 実践講座"

# 3. ゼロからデッキ生成
python skills/gslides-creator/scripts/gslides_creator.py deck \
  --topic "2026年Q1営業報告" --slides 10 --style corporate
```

## サブコマンド

| コマンド | 説明 |
|---------|------|
| `setup` | GAS プロジェクト初期設定 |
| `convert <template_id> --topic "..."` | テンプレートコピー → Gemini で書き換え |
| `build <template_id> --data data.yaml` | テンプレートコピー → YAML データで精密書き換え |
| `deck --topic "..."` | ゼロからデッキ生成（Gemini アウトライン） |

## convert — テンプレート書き換え

テンプレートをコピーし、Gemini で新トピックに合わせたコンテンツを生成して `replaceAllText` で一括置換。

```bash
python gslides_creator.py convert TEMPLATE_ID \
  --topic "新しいトピック" \
  --title "新しいタイトル"
```

処理フロー:
1. gslides-parser でテンプレート構造を解析
2. Gemini Flash でプレースホルダーの新コンテンツ生成
3. GAS `convertPresentation()` でテンプレートコピー + replaceAllText
4. 新しい Google Slides URL を出力

## build — 精密書き換え

マッピング YAML に基づいて要素単位でテキスト・スタイル・位置を書き換え。

```bash
# 1. gslides-parser でマッピング取得
python gslides_parser.py analyze TEMPLATE_ID -o mapping.yaml

# 2. データ YAML を作成（手動 or Gemini）
# 3. ビルド
python gslides_creator.py build TEMPLATE_ID \
  --data data.yaml --title "新しいプレゼン"
```

データ YAML 形式:
```yaml
slides:
  - slide_number: 1
    elements:
      - id: "g123abc"
        value: "新しいタイトルテキスト"
        style:
          font: "Noto Sans JP"
          size: 36
          bold: true
      - id: "g456def"
        value: "新しい本文テキスト"
```

## deck — ゼロからデッキ生成

Gemini でアウトラインを生成し、GAS でスライドを構築。

```bash
python gslides_creator.py deck \
  --topic "AI活用提案" \
  --slides 10 \
  --style corporate \
  --save-outline outline.yaml

# テンプレートのテーマを継承する場合
python gslides_creator.py deck \
  --topic "Q1報告" \
  --template TEMPLATE_ID \
  --style minimal
```

### スタイル

| スタイル | 説明 |
|---------|------|
| `corporate` | ブルー系ビジネス（デフォルト） |
| `minimal` | モノトーン + 赤アクセント |

### スライドタイプ（自動選択）

| タイプ | 説明 |
|--------|------|
| title | タイトルスライド |
| section | セクション区切り |
| content | 箇条書き |
| key_message | 主要メッセージ |
| two_column | 2列レイアウト |
| comparison | 比較（左右） |
| agenda | アジェンダ |
| closing | 締めスライド |
| kpi_dashboard | KPI カード |
| process_flow | プロセスフロー |
| table | テーブル |

## GAS 関数一覧

| 関数 | ファイル | 説明 |
|------|---------|------|
| `convertPresentation()` | convertSlides.js | テンプレートコピー + replaceAllText |
| `listPlaceholders()` | convertSlides.js | プレースホルダー一覧取得 |
| `buildPresentation()` | buildSlides.js | 要素単位の詳細書き換え |
| `createDeck()` | deckSlides.js | ゼロからデッキ生成 |
| `createDeckFromTemplate()` | deckSlides.js | テンプレートベースのデッキ生成 |

## 関連スキル

- **gslides-parser**: Google Slides の構造をパースしてマッピング YAML を生成
- **pptx-creator**: PPTX 版の同等機能（Gemini → YAML → PPTX）
- **pptx-converter**: PPTX テンプレート変換
- **gas-clasp-ops**: clasp プロジェクト管理
