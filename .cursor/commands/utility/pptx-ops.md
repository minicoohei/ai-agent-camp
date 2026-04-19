# PowerPoint Operations - PPTX操作

python-pptxを使用してPowerPointファイルの読み取り・書き込み・分析を行います。

## 機能

- スライドの読み取り・Markdown変換
- プレゼンテーション構造の分析
- テンプレート抽出
- 新規PPTXファイルの作成

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **コマンド**: read / to-markdown / analyze / extract-template / create
- **ファイルパス**: PPTXファイルのパス
- **スライド番号**: 特定スライドを指定する場合
- **出力先**: ファイルパス（省略時は画面表示）

### Step 2: ツールの実行

```bash
# 読み取り
uv run python tools/pptx_ops.py read <file.pptx>

# Markdown変換
uv run python tools/pptx_ops.py to-markdown <file.pptx>

# 構造分析
uv run python tools/pptx_ops.py analyze <file.pptx>

# テンプレート抽出
uv run python tools/pptx_ops.py extract-template <file.pptx> --output template.json

# 作成
uv run python tools/pptx_ops.py create template.json --output new.pptx
```

### Step 3: 結果の表示

出力されたデータをユーザーに提示します。

## オプション

### read コマンド

| オプション | 説明 |
|------------|------|
| `--slide INT` / `-s` | 特定スライド番号（1-indexed） |
| `--format TEXT` / `-f` | 出力形式: text / json |

### to-markdown コマンド

| オプション | 説明 |
|------------|------|
| `--output PATH` / `-o` | 出力ファイルパス |

### extract-template コマンド

| オプション | 説明 |
|------------|------|
| `--output PATH` / `-o` | 出力JSONファイルパス |

### create コマンド

| オプション | 説明 |
|------------|------|
| `--output PATH` / `-o` | 出力PPTXファイルパス（必須） |

## 使用例

### ファイル読み取り

```
/pptx-ops read presentation.pptx
```

### 特定スライドを読み取り

```
/pptx-ops read presentation.pptx --slide 3
```

### Markdownに変換

```
/pptx-ops to-markdown presentation.pptx -o slides.md
```

### プレゼンテーション分析

```
/pptx-ops analyze presentation.pptx --format json
```

### テンプレート抽出

```
/pptx-ops extract-template template.pptx --output my_template.json
```

### テンプレートから新規作成

```
/pptx-ops create my_template.json --output new_presentation.pptx
```

## 出力形式

### read（テキスト形式）

```
=== Slide 1 ===
Shapes: 5

Text content:
  - プレゼンテーションタイトル
  - サブタイトル
  - 作成者: 田中太郎

Notes: ここにスピーカーノートが表示されます...
```

### to-markdown

```markdown
# presentation.pptx

**Slides**: 10

---

## 目次

1. [プレゼンテーションタイトル](#slide-1)
2. [概要](#slide-2)
...

---

## Slide 1 {#slide-1}

### プレゼンテーションタイトル

サブタイトル

> **Speaker Notes:**
> ここにスピーカーノートが表示されます
```

### analyze

```
📊 Analysis Report: presentation.pptx
==================================================
Slides: 10
Total text length: 2500 characters
Layouts used: ['Title Slide', 'Title and Content', 'Blank']

Shape types:
  MSO_SHAPE_TYPE.PLACEHOLDER (14): 28
  MSO_SHAPE_TYPE.TEXT_BOX (17): 5
  MSO_SHAPE_TYPE.PICTURE (13): 3

Slides overview:
  1. Title Slide (3 shapes)
  2. Title and Content (5 shapes)
  3. Title and Content (4 shapes)
```

### extract-template

```json
{
  "source_file": "presentation.pptx",
  "slide_width": 9144000,
  "slide_height": 6858000,
  "layouts": [
    {
      "name": "Title Slide",
      "placeholders": [...]
    }
  ],
  "slides": [
    {
      "index": 1,
      "layout_name": "Title Slide",
      "content_structure": [...]
    }
  ]
}
```

## テンプレートJSON形式（create用）

```json
{
  "slides": [
    {
      "title": "スライドタイトル",
      "content": [
        "箇条書き1",
        "箇条書き2",
        "箇条書き3"
      ],
      "notes": "スピーカーノート"
    }
  ]
}
```

## 前提条件

python-pptxライブラリが必要です：

```bash
uv add python-pptx
```

## 関連コマンド

- `/excel-ops` - Excel操作
- `/fetch-slides` - Google Slides取得
- `/generate-slide` - スライド画像の生成
