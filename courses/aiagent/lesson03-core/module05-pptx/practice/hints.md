# python-pptx のヒント

## 基本操作

### プレゼンテーション作成

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
```

### スライド追加

```python
# レイアウトの選択
# 0: Title Slide, 1: Title and Content, 5: Blank, 6: Title Only
layout = prs.slide_layouts[1]  # Title and Content
slide = prs.slides.add_slide(layout)
```

### テキスト設定

```python
# タイトル
title = slide.shapes.title
title.text = "スライドタイトル"

# 本文
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "1行目のテキスト"

# 段落追加
p = tf.add_paragraph()
p.text = "2行目のテキスト"
p.level = 1  # インデントレベル
```

### 書式設定

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

run = p.runs[0]
run.font.size = Pt(18)
run.font.bold = True
run.font.color.rgb = RGBColor(0x15, 0x65, 0xC0)  # #1565C0
```

### テキストボックス追加

```python
from pptx.util import Inches

txBox = slide.shapes.add_textbox(
    Inches(1), Inches(2),   # 位置 (left, top)
    Inches(8), Inches(1)    # サイズ (width, height)
)
tf = txBox.text_frame
tf.text = "テキストボックスの内容"
```

## 構造解析

```python
prs = Presentation("sample.pptx")

for i, slide in enumerate(prs.slides):
    print(f"--- Slide {i+1} ---")
    print(f"Layout: {slide.slide_layout.name}")

    for shape in slide.shapes:
        print(f"  Shape: {shape.shape_type}, Name: {shape.name}")
        print(f"  Position: left={shape.left}, top={shape.top}")
        print(f"  Size: width={shape.width}, height={shape.height}")

        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                print(f"  Text: {para.text}")
                for run in para.runs:
                    print(f"    Font: {run.font.name}, Size: {run.font.size}")
```

## テーブル追加

```python
rows, cols = 4, 3
table = slide.shapes.add_table(rows, cols, Inches(1), Inches(2), Inches(8), Inches(3)).table

# ヘッダー
table.cell(0, 0).text = "項目"
table.cell(0, 1).text = "現状"
table.cell(0, 2).text = "目標"

# データ
table.cell(1, 0).text = "売上"
table.cell(1, 1).text = "1,000万円"
table.cell(1, 2).text = "1,500万円"
```
