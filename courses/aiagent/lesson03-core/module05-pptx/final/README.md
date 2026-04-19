# module05-pptx 完成例

## 概要

PowerPointファイルの構造解析・テキスト抽出・自動生成の3ステップを実践した完成例です。python-pptxライブラリによるプログラマティックなスライド操作を含みます。

## 成果物一覧

| ファイル | 種類 | 説明 |
|----------|------|------|
| `output/structure-analysis.json` | JSON | PPTX構造解析結果（スライド数、レイアウト、テキスト、フォント情報） |
| `output/extracted-text.md` | Markdown | 全スライドのテキスト抽出結果 |
| `output/generated-presentation.pptx` | PPTX | 自動生成した10スライドの提案書 |

## 解説

### 構造解析（structure-analysis.json）
- 全10スライドの構造情報をJSON形式で出力
- 各スライドのレイアウト名、シェイプの種類、位置、サイズ
- テキストフレーム内のフォント情報（名前、サイズ、太字フラグ）

### テキスト抽出（extracted-text.md）
- 全スライドのテキストをMarkdown形式で整理
- スライド番号ごとにセクション分け
- 箇条書き形式で可読性を確保

### 自動生成プレゼン（generated-presentation.pptx）
- 「AIエージェント活用提案書」として10スライドを自動生成
- タイトルスライド + 9枚のコンテンツスライド
- ブランドカラー（#1565C0）を適用
- フォントサイズ: タイトル28pt、本文18pt

## 使用ツール

- python-pptx ライブラリ
- pptx-analyzer スキル（`tools/pptx_ops.py`）

## 学習ポイント

1. python-pptx による PPTX ファイルの読み書き
2. スライドレイアウトとプレースホルダーの仕組み
3. テキストフレーム、段落、ランの階層構造
4. フォント・色・配置の書式設定
