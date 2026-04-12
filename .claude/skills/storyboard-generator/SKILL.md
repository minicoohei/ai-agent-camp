---
name: storyboard-generator
description: |
  AI UGC動画用の絵コンテを自動生成するスキル。1枚シート生成→切り出しでキャラクター一貫性を保証。
  「絵コンテを作って」「ストーリーボード生成」「UGC動画の流れを作って」等のリクエストで発動。
triggers:
  - 絵コンテを作って
  - ストーリーボード生成
  - UGC動画の流れを作って
  - 動画の絵コンテ
  - シーン構成を作成
  - storyboard-generator
  - storyboard
---

# Storyboard Generator (UGC絵コンテ生成)

AI UGC動画制作のための絵コンテ作成ツール。**1枚のシート画像として全フレームを一括生成→切り出し**により、キャラクター一貫性を保証します。

## 生成モード

### 🟢 sheet（デフォルト・推奨）
- 全フレームを**1枚の絵コンテシート**として一括生成
- 1回のAPI呼び出しで全フレーム → **キャラ一貫性◎**
- 生成後にグリッドを個別フレームに切り出し
- 速度・コスト・一貫性すべて優位

### 🔴 individual（旧方式）
- 1フレームずつ個別に生成
- キャラクター参照画像で一貫性を保とうとするが限界あり
- フォールバック用途

## 機能

### 1. キャラクター設計
- キャラクター詳細プロンプトから基準画像を生成
- 既存のキャラクター画像を参照画像として使用可能
- sheetモードでは参照画像をシート生成時に渡して一貫性を強化

### 2. 絵コンテ生成
- シナリオから4/8/16コマのシーン説明を自動生成（Gemini Flash）
- sheetモード: 1枚のグリッド画像として生成→自動切り出し
- individualモード: 1フレームずつ生成→グリッド合成
- 自動リサイズ（デフォルト540px幅、JPG圧縮）

### 3. ナレーション＆テキストオーバーレイ指示
- 各フレームにナレーション台本（日本語）を自動生成
- テキストオーバーレイの内容・位置・スタイルを指定
- scenes.jsonにnarration, text_overlay フィールドで出力

### 4. 動画化方式の自動判定（motion_type）
- **static**: テキスト主体 → 静止画のまま
- **ken_burns**: 風景/静的構図 → ズーム/パンで十分（i2V不要）
- **motion_graphics**: UI遷移/テキストアニメ → Remotionで十分（i2V不要）
- **i2v**: 人物動作/表情変化 → fal.ai wan-i2v等のi2V変換が必要
- コスト最適化: i2Vが本当に必要なシーンのみi2V指定

### 5. 動画生成連携
- 絵コンテから任意のStartFrame/EndFrameを選択
- fal.ai（wan-i2v）でImage-to-Video生成
- カメラワーク指定対応

## Usage

```bash
# 🟢 推奨: シートモード（1枚生成→切り出し）
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "アプリの使い方を説明するUGC動画" \
    --character "20代の日本人女性、カジュアルな服装、明るい表情" \
    --aspect-ratio 9:16 \
    --num-frames 8 \
    --mode sheet \
    --session "app_promo"

# 個別モード（フォールバック）
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "商品レビュー動画" \
    --character "..." \
    --mode individual \
    --session "product_review"

# 既存キャラクター画像を使用
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --scenario "..." \
    --character-image "path/to/character.png" \
    --mode sheet \
    --session "with_ref"

# 動画生成（既存絵コンテから）
python skills/storyboard-generator/scripts/generate_storyboard.py \
    --storyboard-dir "output/storyboard/YYYYMMDD_session" \
    --start-frame 1 \
    --end-frame 8 \
    --video-duration 10
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --scenario | Yes | - | 動画のシナリオ・トピック |
| --character | No* | - | キャラクター詳細プロンプト |
| --character-image | No* | - | 既存キャラクター参照画像パス |
| --mode | No | sheet | 生成モード: sheet / individual |
| --aspect-ratio | No | 9:16 | アスペクト比（9:16, 16:9, 1:1, 4:3, 3:4） |
| --num-frames | No | 16 | フレーム数（4, 8, 16） |
| --output-width | No | 540 | 出力画像の最大幅px（0で無制限） |
| --layout | No | auto | グリッドレイアウト（individualモードのみ） |
| --session | No | - | セッション名（出力フォルダ名） |
| --style | No | modern_clean | ビジュアルスタイル |
| --start-frame | No | - | 動画生成時の開始フレーム番号 |
| --end-frame | No | - | 動画生成時の終了フレーム番号 |
| --video-duration | No | 5 | 動画の長さ（秒）: 5 or 10 |
| --camera-motion | No | - | カメラワーク |

*--character または --character-image のどちらか必須

## Output Structure

```
output/storyboard/
└── YYYYMMDD_HHMMSS_session/
    ├── character_reference.png    # キャラクター参照画像
    ├── storyboard_sheet.png       # 元シート（sheetモード）
    ├── storyboard_grid.jpg        # リサイズ済みグリッド
    ├── frames/
    │   ├── frame_01.jpg           # 切り出しフレーム（JPG圧縮）
    │   ├── frame_02.jpg
    │   └── ...
    ├── scenes.json                # シーン情報（narration, text_overlay, motion_type）
    └── video/                     # 動画生成時
        └── output.mp4
```

## Performance Comparison

| | sheet（推奨） | individual |
|---|---|---|
| API呼び出し | 3回 | N+2回 |
| 生成時間（8フレーム） | ~1分 | ~5分 |
| ファイルサイズ | ~325KB | ~800KB |
| キャラ一貫性 | ◎ | △ |

## Visual Styles

- `modern_clean` - モダン・クリーン（デフォルト）
- `animal_crossing` - どうぶつの森風
- `vibrant_ugc` - ビビッドUGC
- `anime` - アニメ風

## Requirements

- `GEMINI_API_KEY`: Gemini Flash/Image Generation用
- `FAL_KEY`: i2V動画生成用（動画生成時のみ）
- Python packages: google-genai, Pillow, python-dotenv

## Environment Setup

```bash
export GEMINI_API_KEY="your-key"    # Mac/Linux
export PYTHONPATH="/path/to/.pip/local/local/lib/python3.11/dist-packages:$PYTHONPATH"    # Mac/Linux
# Windows (cmd): set GEMINI_API_KEY=your-key
#                set PYTHONPATH=C:\path\to\site-packages;%PYTHONPATH%
# Windows (PowerShell): $env:GEMINI_API_KEY = "your-key"
#                       $env:PYTHONPATH = "C:\path\to\site-packages;$env:PYTHONPATH"
```

## Trigger Phrases

- 「絵コンテを作って」「絵コンテ生成」
- 「ストーリーボードを作成」
- 「UGC動画の絵コンテ」
- 「動画の流れを作って」

## Overview

AI UGC動画制作のための絵コンテを自動生成するスキルです。1枚のシート画像として全フレームを一括生成→切り出しにより、キャラクター一貫性を保証。ナレーション台本・動画化方式の自動判定にも対応。

## Troubleshooting

| エラー | 解決方法 |
|--------|---------|
| API key not found | `GEMINI_API_KEY` を環境変数に設定 |
| Character consistency issues | `--mode sheet`（推奨）を使用。individualモードは一貫性が低い |
| FAL_KEY not set | 動画生成（i2V）時のみ必要。絵コンテ生成だけなら不要 |

## Success Criteria

- [ ] 指定フレーム数の絵コンテ画像が `output/storyboard/` に生成されている
- [ ] `scenes.json` にナレーション・motion_type が含まれている
- [ ] キャラクターの外見がフレーム間で一貫している
