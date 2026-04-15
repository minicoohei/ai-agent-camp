# 演習: PPTX 解析・自動生成

![PPTX自動化ワークフロー](images/exercise-hero.png)

## 概要

PowerPoint ファイル（.pptx）の構造解析と自動生成を行う演習です。
python-pptx を使い、既存スライドの解析とテンプレートからの自動生成を実践します。

## 前提条件

- Python 3.8 以上
- python-pptx パッケージ

```bash
uv add python-pptx
```

## タスク

### タスク1: PPTX 構造解析

`data/sample-presentation.pptx` を解析し、以下の情報を抽出してください。

```python
from pptx import Presentation

prs = Presentation("data/sample-presentation.pptx")
for i, slide in enumerate(prs.slides):
    print(f"Slide {i+1}: {slide.slide_layout.name}")
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(f"  Text: {shape.text_frame.text[:50]}")
```

**抽出項目:**
- スライド数とレイアウト名
- 各スライドのテキスト内容
- 画像・図形の有無
- フォント情報（名前、サイズ、色）

**成果物:** 構造解析結果を JSON ファイルに出力

### タスク2: テキスト抽出

全スライドからテキストを抽出し、Markdown 形式でまとめてください。

**成果物:** 抽出したテキストの Markdown ファイル

### タスク3: プレゼン自動生成

`data/content-outline.md` の構成案をもとに、10スライドのプレゼンテーションを自動生成してください。

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
# スライド追加、テキスト設定、書式設定...
prs.save("output/generated-presentation.pptx")
```

**要件:**
- タイトルスライド + 9枚のコンテンツスライド
- 見出し + 本文のレイアウト
- ブランドカラー（#1565C0）の使用
- フッターにページ番号

## 完了条件

- [ ] PPTX構造解析結果がJSON形式で出力されている
- [ ] テキストがMarkdown形式で抽出されている
- [ ] 10スライドのプレゼンが自動生成されている
- [ ] 生成されたPPTXが正常に開ける

## ヒント

- `hints.md` に python-pptx の基本操作をまとめています
- `data/content-outline.md` にスライド構成案があります
- `data/update-data.csv` に差し替え用の数値データがあります
