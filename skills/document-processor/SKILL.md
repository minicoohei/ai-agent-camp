---
name: document-processor
description: |
  PDF/PPTX/Excelファイルの読み取り・編集・分析を行うサブエージェント。
  大きなドキュメントの処理をメインコンテキストから分離し、コンテキスト消費を最適化する。
  「PDFを分析」「PPTXの内容を読んで」「Excelを解析」「スライドを編集」等のリクエストで発動。
triggers:
  - PDFを分析
  - PDFを編集
  - PPTXを分析
  - PPTXを読んで
  - スライドの内容
  - Excelを分析
  - Excelを読んで
  - ドキュメントを処理
---

# Document Processor サブエージェント

PDF/PPTX/Excelファイルの読み取り・編集・分析を専用コンテキストで実行するサブエージェント。

## 目的

大きなドキュメントの処理をメインエージェントのコンテキストから分離し：
- コンテキスト消費を削減（2000-10000トークン削減効果）
- 処理結果のサマリーのみを返却
- 複数ファイルの並列処理が可能

## 対応フォーマット

| フォーマット | 読み取り | 編集 | 分析 |
|------------|:------:|:----:|:----:|
| PDF (.pdf) | ✅ | ✅ | ✅ |
| PowerPoint (.pptx) | ✅ | ✅ | ✅ |
| Excel (.xlsx) | ✅ | ✅ | ✅ |

## 使用可能なスクリプト

### 1. PowerPoint操作 (`tools/pptx_ops.py`)

```bash
# 読み取り
uv run python tools/pptx_ops.py read <file.pptx>

# Markdown変換
uv run python tools/pptx_ops.py to-markdown <file.pptx>

# 構造分析
uv run python tools/pptx_ops.py analyze <file.pptx>

# テンプレート抽出
uv run python tools/pptx_ops.py extract-template <file.pptx> --output template.json

# 新規作成
uv run python tools/pptx_ops.py create <template.json> --output new.pptx
```

### 2. Excel操作 (`tools/excel_ops.py`)

```bash
# 読み取り
uv run python tools/excel_ops.py read <file.xlsx>

# 特定シート読み取り
uv run python tools/excel_ops.py read <file.xlsx> --sheet "Sheet1"

# Markdown変換
uv run python tools/excel_ops.py to-markdown <file.xlsx>

# 分析レポート
uv run python tools/excel_ops.py analyze <file.xlsx>

# 書き込み
uv run python tools/excel_ops.py write <file.xlsx> --data '{"sheet": "Sheet1", "cell": "A1", "value": "Hello"}'
```

### 3. PDF操作 (`tools/pdf_page_editor.py`)

```bash
# テキスト抽出・分析
uv run python tools/pdf_page_editor.py analyze <file.pdf>

# ページ編集
uv run python tools/pdf_page_editor.py edit <file.pdf> --page 1 --changes <changes.yaml>

# 圧縮
uv run python tools/pdf_page_editor.py compress <file.pdf> --output compressed.pdf
```

## サブエージェント呼び出しパターン

メインエージェントは以下のパターンでこのサブエージェントを呼び出す：

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Document analysis",
    prompt="""
    このスキルを読んで実行してください: skills/document-processor/SKILL.md
    
    タスク: {ユーザーの指示}
    対象ファイル: {ファイルパス}
    
    結果はサマリー形式で返却してください。
    """
)
```

## 返却フォーマット

処理結果は以下のサマリー形式で返却：

```yaml
status: success
file: example.pptx
summary:
  total_slides: 10
  key_content:
    - slide_1: "タイトルスライド - プロジェクト概要"
    - slide_2: "目次 - 5項目"
  findings:
    - "テンプレートは16:9アスペクト比"
    - "カラースキーム: 青/白/黒"
output_files:
  - example_structure.json
  - example_structure.txt
```

## 依存関係

```txt
python-pptx>=0.6.21
openpyxl>=3.1.0
pdf2image>=1.16.0
Pillow>=9.0.0
PyMuPDF>=1.21.0
google-generativeai>=0.3.0
```

## ユースケース

1. **PPTX分析**: テンプレート構造の把握、プレースホルダー特定
2. **Excel分析**: データ構造の理解、シート間の関係把握
3. **PDF編集**: テキスト修正、ページ再構築
4. **バッチ処理**: 複数ドキュメントの一括処理

## 注意事項

- 大きなファイル（>50MB）は処理に時間がかかる場合がある
- PDF編集は元ファイルを変更せず、新規ファイルを生成
- 画像の多いPPTXは`--with-images`オプションで画像も抽出可能

## Overview

PDF/PPTX/Excelファイルの読み取り・編集・分析を専用コンテキストで実行するサブエージェントスキルです。大きなドキュメントの処理をメインコンテキストから分離し、処理結果のサマリーのみを返却します。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| python-pptx not installed | `pip install python-pptx` でインストール |
| PDF parsing error | PyMuPDF がインストールされているか確認: `pip install PyMuPDF` |
| File too large (>50MB) | 処理に時間がかかる場合あり。PDF圧縮スキルで事前に軽量化を検討 |

## Success Criteria

- [ ] ドキュメントの内容がサマリー形式（YAML）で返却されている
- [ ] 編集操作時に元ファイルが変更されず新規ファイルが生成されている
- [ ] エラーなく完了している

## Usage

上記「使用可能なスクリプト」セクションを参照。基本例:

```bash
# PPTX読み取り
uv run python tools/pptx_ops.py read presentation.pptx

# Excel分析
uv run python tools/excel_ops.py analyze data.xlsx

# PDF分析
uv run python tools/pdf_page_editor.py analyze document.pdf
```
