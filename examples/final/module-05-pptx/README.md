# Module 5: PPTX操作 - 成果物（Final）

PowerPointファイルの解析、生成、編集の例です。

## 学習目標
- PPTXファイルの構造を解析できる
- プログラムでスライドを生成できる
- テンプレートを活用した自動生成ができる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `pptx_structure.json` | JSON | PPTX構造解析結果 |
| `generated_presentation.pptx` | PPTX | 自動生成プレゼン |
| `template_info.json` | JSON | テンプレート情報 |
| `analysis_script.py` | スクリプト | 解析スクリプト |
| `generator_script.py` | スクリプト | 生成スクリプト |

## PPTX構造

```
┌─────────────────────────────────────────────────────────┐
│  PowerPoint ファイル構造                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Presentation                                           │
│  ├── Slide Masters（スライドマスター）                   │
│  │   └── Slide Layouts（レイアウト）                    │
│  │       ├── Title Slide                               │
│  │       ├── Title and Content                         │
│  │       ├── Section Header                            │
│  │       └── ...                                       │
│  │                                                     │
│  ├── Slides（スライド）                                 │
│  │   ├── Slide 1                                       │
│  │   │   ├── Shapes（シェイプ）                        │
│  │   │   │   ├── Title                                │
│  │   │   │   ├── Body                                 │
│  │   │   │   ├── Image                                │
│  │   │   │   └── Table                                │
│  │   │   └── Notes（ノート）                           │
│  │   └── ...                                          │
│  │                                                     │
│  └── Theme（テーマ）                                   │
│      ├── Colors                                        │
│      ├── Fonts                                         │
│      └── Effects                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### PPTX構造解析
```bash
uv run python tools/pptx_ops.py analyze \
  --input data/presentations/sample.pptx \
  --output examples/final/module-05-pptx/pptx_structure.json
```

### スライド生成
```bash
uv run python tools/pptx_ops.py generate \
  --template data/templates/corporate.pptx \
  --content data/content/presentation_data.json \
  --output examples/final/module-05-pptx/generated_presentation.pptx
```

### テンプレート情報抽出
```bash
uv run python tools/pptx_ops.py extract-template \
  --input data/templates/corporate.pptx \
  --output examples/final/module-05-pptx/template_info.json
```

## 解析スクリプト例

```python
#!/usr/bin/env python3
"""PPTX構造解析スクリプト"""
from pptx import Presentation
from pptx.util import Inches, Pt
import json

def analyze_pptx(pptx_path):
    """PPTXファイルを解析"""
    prs = Presentation(pptx_path)
    
    analysis = {
        'metadata': {
            'slide_count': len(prs.slides),
            'slide_width': prs.slide_width,
            'slide_height': prs.slide_height,
        },
        'slides': [],
        'layouts': [],
        'fonts': set()
    }
    
    # スライド解析
    for i, slide in enumerate(prs.slides, 1):
        slide_info = {
            'number': i,
            'layout': slide.slide_layout.name,
            'shapes': []
        }
        
        for shape in slide.shapes:
            shape_info = {
                'name': shape.name,
                'type': str(shape.shape_type),
                'has_text': shape.has_text_frame
            }
            
            if shape.has_text_frame:
                shape_info['text'] = shape.text[:100]
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.name:
                            analysis['fonts'].add(run.font.name)
            
            if shape.has_table:
                shape_info['table'] = {
                    'rows': len(shape.table.rows),
                    'cols': len(shape.table.columns)
                }
            
            slide_info['shapes'].append(shape_info)
        
        analysis['slides'].append(slide_info)
    
    # レイアウト一覧
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            analysis['layouts'].append(layout.name)
    
    analysis['fonts'] = list(analysis['fonts'])
    
    return analysis

if __name__ == "__main__":
    import sys
    result = analyze_pptx(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 生成スクリプト例

```python
#!/usr/bin/env python3
"""PPTX生成スクリプト"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN

def create_presentation(content_data, template_path=None):
    """プレゼンテーションを生成"""
    if template_path:
        prs = Presentation(template_path)
    else:
        prs = Presentation()
    
    # タイトルスライド
    title_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_layout)
    slide.shapes.title.text = content_data['title']
    slide.placeholders[1].text = content_data['subtitle']
    
    # コンテンツスライド
    content_layout = prs.slide_layouts[1]
    for section in content_data['sections']:
        slide = prs.slides.add_slide(content_layout)
        slide.shapes.title.text = section['title']
        
        body = slide.placeholders[1]
        tf = body.text_frame
        
        for point in section['points']:
            p = tf.add_paragraph()
            p.text = point
            p.level = 0
    
    return prs

# コンテンツデータ例
content = {
    'title': 'AIエージェント活用研修',
    'subtitle': '2025年版',
    'sections': [
        {
            'title': 'はじめに',
            'points': [
                'AIエージェントとは',
                '本研修の目的',
                '学習の流れ'
            ]
        },
        {
            'title': 'Module 1: バナー生成',
            'points': [
                'banner-creatorスキル',
                'プラットフォーム別サイズ',
                '実践演習'
            ]
        }
    ]
}
```

## 解析結果JSON例

```json
{
  "metadata": {
    "slide_count": 10,
    "slide_width": 9144000,
    "slide_height": 5143500
  },
  "slides": [
    {
      "number": 1,
      "layout": "Title Slide",
      "shapes": [
        {
          "name": "Title 1",
          "type": "PLACEHOLDER",
          "has_text": true,
          "text": "プレゼンテーションタイトル"
        },
        {
          "name": "Subtitle 2",
          "type": "PLACEHOLDER",
          "has_text": true,
          "text": "サブタイトル"
        }
      ]
    }
  ],
  "layouts": [
    "Title Slide",
    "Title and Content",
    "Section Header",
    "Two Content",
    "Comparison",
    "Title Only",
    "Blank"
  ],
  "fonts": ["Meiryo", "Arial", "Calibri"]
}
```

## チェックリスト

- [ ] PPTXファイルが読み込める
- [ ] スライド構造が解析できる
- [ ] テキスト・画像・表を抽出できる
- [ ] 新規スライドを生成できる
- [ ] テンプレートを活用できる

## 関連レッスン

- `/start-5-1`: PPTX解析
- `/start-5-2`: PPTX生成

## 参考リンク

- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [PowerPoint レイアウト一覧](https://support.microsoft.com/ja-jp/office/powerpoint-slides)
