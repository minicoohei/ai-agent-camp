---
name: gslides-parser
description: |
  Google Slides の構造を GAS 経由でパースし、YAML マッピングを出力するスキル。
  「スライドをパースして」「スライドの構造を解析」「YAMLマッピング作成」等のリクエストで発動。
  pptx-converter 互換のセマンティック解析 + プレースホルダー付与。
triggers:
  - gslides-parser
  - スライドパース
  - スライド構造解析
  - YAMLマッピング
  - Google Slides解析
  - gslides
---

# /gslides-parser - Google Slides パーサー

Google Slides プレゼンテーションの構造を GAS 経由でパースし、pptx-converter 互換のマッピング YAML を出力する。

## 前提条件

```bash
# clasp のインストール（未インストールの場合）
npm install -g @google/clasp

# Google アカウントでログイン
clasp login

# Google Apps Script API を有効化
# https://script.google.com/home/usersettings
```

## クイックスタート

```bash
# 1. GAS プロジェクト初期設定（初回のみ）
python skills/gslides-parser/scripts/gslides_parser.py setup

# 2. GAS エディタで一度手動実行して権限を付与
npx @google/clasp open --cwd skills/gslides-parser/gas/

# 3. パース実行
python skills/gslides-parser/scripts/gslides_parser.py analyze \
  1ZVAI8Cjts1N44lYXgoCoZXfb0gz7BAx7A1A5-bhapvQ \
  -o output/slides/mapping.yaml
```

## サブコマンド

| コマンド | 説明 |
|---------|------|
| `setup` | GAS プロジェクト初期設定（clasp create + push） |
| `analyze <id>` | プレゼンテーションをパース → YAML 出力 |
| `json <id>` | GAS パース結果の JSON だけ出力 |

## オプション

### analyze

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `-o, --output` | 出力 YAML パス | `output/slides/gslides_<id>_<timestamp>.yaml` |
| `--no-gemini` | Gemini セマンティック解析を無効化 | false |
| `--skip-push` | clasp push をスキップ | false |

### json

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `-o, --output` | 出力 JSON パス | stdout |
| `--skip-push` | clasp push をスキップ | false |

## 出力 YAML スキーマ（pptx-converter 互換）

```yaml
source: "Google Slides: プレゼン名"
presentation_id: "1ZVAI8..."
presentation_url: "https://docs.google.com/presentation/d/1ZVAI8.../edit"
generated_at: "2026-02-10T12:00:00"
slide_width_pt: 720
slide_height_pt: 405

slides:
  - slide_number: 1
    object_id: "p6"
    layout: "TITLE"
    elements:
      - id: "g1234abcd"
        type: text
        role: title
        hint: "メインタイトル。"
        position: { left: 36, top: 150, width: 648, height: 80 }
        style: { font: "Noto Sans JP", size: 36, bold: true, color: "333333" }
        value: "タイトルテキスト"
        placeholder: "{{slide_1_title}}"

placeholders:
  - key: "{{slide_1_title}}"
    type: text
    role: title
    current: "タイトルテキスト"
```

## 処理フロー

```
[ユーザー] → python gslides_parser.py analyze <id>
                    │
        ┌───────────┴───────────┐
        │  1. clasp push        │  GAS コードを反映
        │     (gas/ → GAS)      │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │  2. clasp run         │  parsePresentation() 実行
        │     parsePresentation │  → JSON 構造を返す
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │  3. gas_to_yaml.py    │  セマンティック解析
        │     JSON → YAML 変換  │  + プレースホルダー付与
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │  4. YAML 出力         │  pptx-converter 互換
        └───────────┘
```

## GAS パーサーがパースする要素

| 要素タイプ | 抽出情報 |
|-----------|---------|
| **Shape (テキスト)** | テキスト、スタイル(font/size/bold/color)、プレースホルダー判定、塗りつぶし色 |
| **Image** | ソースURL、コンテンツURL、リンク |
| **Table** | 全セルテキスト、行列数、ヘッダー検出、セルスタイル |
| **Group** | 子要素の再帰的パース |
| **SheetsChart** | スプレッドシートID、チャートID |
| **Line** | 線種、太さ、色 |
| **WordArt** | レンダリングテキスト |
| **Video** | ソース、URL、動画ID |

## セマンティック解析

ヒューリスティックで以下のロールを自動判定:

- **テキスト**: title, subtitle, heading, body, caption, label, footnote, page_number, bullet_list
- **画像**: hero_image, logo, icon, photo, decorative, background
- **テーブル**: data_table, comparison_table, schedule_table
- **チャート**: revenue_chart, trend_chart, comparison_chart
- **シェイプ**: accent_decoration, callout, divider, background_shape
- **グループ**: process_flow, feature_cards, step_diagram

## トラブルシューティング

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `Not logged in` | clasp 未ログイン | `npx @google/clasp login` |
| `Script API disabled` | GAS API 無効 | [GAS API 設定](https://script.google.com/home/usersettings) で有効化 |
| `PERMISSION_DENIED` | OAuth スコープ未承認 | GAS エディタで一度手動実行して権限付与 |
| `Function not found` | push 未完了 | `npx @google/clasp push --force` |
| タイムアウト | 大きなプレゼン | GAS エディタから直接実行 |

## 関連スキル

- **gslides-creator**: パース結果の YAML を使ってテンプレートから新スライドを作成
- **pptx-converter**: PPTX ファイルの同等機能（extract → build → convert）
- **gas-clasp-ops**: clasp プロジェクト管理
