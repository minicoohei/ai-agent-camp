---
nonInteractiveMode: compliant
---

# PPTXテンプレート操作

PowerPointファイルのフォーマットを抽出してYAMLテンプレート化し、テキストだけを差し替えた新しいスライドを生成するツールです。

## 概要

このツールは2つのスクリプトで構成されています：

1. **pptx_ops.py extract-template** - PPTXからテンプレートを抽出
2. **pptx_ops.py create** - テンプレートから新しいPPTXを生成

## ワークフロー

```text
[元PPTX] → [Extractor] → [template.yaml] + [screenshots/]
                              ↓
                         [data.yaml]
                              ↓
[template.yaml] + [data.yaml] → [Generator] → [新PPTX]
```

## 使用方法

### 1. テンプレート抽出

既存のPPTXファイルからフォーマット情報を抽出します。

```bash
# 基本的なテンプレート抽出
uv run python tools/pptx_ops.py extract-template sample.pptx --output template.yaml

# 特定のスライドのみ抽出
uv run python tools/pptx_ops.py extract-template sample.pptx --slide 1 --output slide1_template.yaml

# スクリーンショットも生成（LibreOffice必要）
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --screenshot-dir ./screenshots

# プレースホルダー変換をスキップ（元テキストをそのまま保持）
uv run python tools/pptx_ops.py extract-template sample.pptx \
    --output template.yaml \
    --no-placeholder
```

### 2. ファイル情報確認

PPTXファイルの構造を確認します。

```bash
uv run python tools/pptx_ops.py analyze sample.pptx
```

### 3. プレースホルダー一覧

テンプレート内のプレースホルダー（置換可能な変数）を確認します。

```bash
uv run python tools/pptx_ops.py placeholders template.yaml
```

### 4. データテンプレート作成

テンプレートに対応する空のデータファイルを生成します。

```bash
uv run python tools/pptx_ops.py create-data template.yaml --output data.yaml
```

### 5. 新しいPPTX生成

テンプレートとデータから新しいPPTXを生成します。

```bash
uv run python tools/pptx_ops.py generate template.yaml data.yaml --output output.pptx
```

## テンプレートYAMLの構造

```yaml
source_file: sample.pptx
slide_width: 12192000  # EMU (914400 EMU = 1 inch)
slide_height: 6858000
slides:
  - index: 1
    layout_name: Blank
    screenshot: slide_1.png
    shapes:
      - id: shape_1
        name: "Title 1"
        type: text_box
        position:
          left: 457200
          top: 274638
          width: 8229600
          height: 1143000
        content:
          word_wrap: true
          paragraphs:
            - text: "{{title}}"
              original_text: "元のタイトル"
              style:
                font_name: "Meiryo UI"
                font_size: 44
                font_bold: true
                font_color: "000000"
                alignment: center
        fill:
          type: solid
          color: "FFFFFF"
```

## データYAMLの例

```yaml
# template.yaml の {{placeholder}} に対応する値を定義
title: "新しいタイトル"
subtitle: "サブタイトル"
image_path: "./images/new_image.png"
cell_0_1: "表のセル値"
```

## 対応するシェイプタイプ

| タイプ | 説明 | 抽出情報 |
|--------|------|----------|
| text_box | テキストボックス | 位置、サイズ、テキスト、フォントスタイル、配置 |
| picture | 画像 | 位置、サイズ、画像パス（プレースホルダー化） |
| table | テーブル | 位置、サイズ、行数、列数、セル内容、セルスタイル |
| auto_shape | 図形 | 位置、サイズ、塗りつぶし色、線色、テキスト |
| placeholder | プレースホルダー | 位置、サイズ、タイプ、テキスト |
| group | グループ | 子シェイプの再帰抽出 |

## スクリーンショット生成

スクリーンショット自動生成には以下が必要です：

```bash
# macOS
brew install poppler
uv add pdf2image
brew install --cask libreoffice

# Windows
# poppler: https://github.com/oschwartz10612/poppler-windows からダウンロードしPATHに追加
uv add pdf2image
# LibreOffice: winget install --id TheDocumentFoundation.LibreOffice
```

既存のスクリーンショットを使用する場合は `--no-generate-screenshot` オプションを指定します。

## 使用例：定型スライドの量産

1. 元となるフォーマット済みPPTXを用意

2. テンプレートを抽出
   ```bash
   uv run python tools/pptx_ops.py extract-template format_sample.pptx \
       --output my_template.yaml
   ```

3. プレースホルダーを確認
   ```bash
   uv run python tools/pptx_ops.py placeholders my_template.yaml
   ```

4. データファイルを作成
   ```bash
   uv run python tools/pptx_ops.py create-data my_template.yaml \
       --output my_data.yaml
   ```

5. データを編集して値を入力
   ```yaml
   # my_data.yaml
   title: "2026年第1四半期レポート"
   author: "営業部"
   date: "2026-01-16"
   ```

6. 新しいPPTXを生成
   ```bash
   uv run python tools/pptx_ops.py generate my_template.yaml my_data.yaml \
       --output Q1_report.pptx
   ```

## 前提条件

- Python 3.8以上
- 必須ライブラリ: `python-pptx`, `pyyaml`
- オプション: `pdf2image`, `Pillow`（スクリーンショット生成用）
- オプション: LibreOffice（PDF変換用）

```bash
uv add python-pptx pyyaml pdf2image Pillow
```

## 注意事項

- EMU（English Metric Units）: 914,400 EMU = 1インチ
- テーマ色は直接のRGB変換ができないため `theme:XXX` として出力されます
- グループ化されたシェイプは子シェイプとして個別に抽出されます
- 複雑なアニメーションや遷移効果は保持されません
