---
name: video-scriptwriter
description: "TikTok/YouTube向け動画スクリプト自動生成スキル。 テーマ+フォーマット+尺を指定すると、scenes.json（storyboard/audio/editor互換）を生成。 Playbookの知見を自動参照して最適な構成を適用。 「スクリプト作成」「台本生成」「企画作って」等で発動。"
triggers:
  - 動画のスクリプトを作成
  - 台本を生成
  - 動画の企画を作って
  - TikTok用の台本
  - scenes.jsonを生成
  - video-scriptwriter
  - 動画の構成案
---

# Video Scriptwriter

テーマ → 企画 → scenes.json を自動生成する。

## 6つのフォーマット

| フォーマット | 説明 | 量産適性 |
|-------------|------|----------|
| `split_screen_teaching` | 上半分テキスト+TTS / 下半分ゲーム映像 | ★★★★★ |
| `ranking_list` | ランキングTOP5型 | ★★★★☆ |
| `reddit_story` | Reddit/2ch読み上げ + 背景動画 | ★★★★★ |
| `dark_facts` | 「知ると怖い○○」雑学型 | ★★★★☆ |
| `standard_teaching` | 標準教育/解説型 | ★★★★☆ |
| `product_intro` | 商品紹介/レビュー型 | ★★★☆☆ |

## クイックスタート

```bash
# 基本
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "睡眠の質を上げる5つの方法" \
  --format ranking_list \
  --duration 30s

# Split-screen教育型
python3 skills/video-scriptwriter/scripts/generate_script.py \
  --topic "量子コンピュータとは何か" \
  --format split_screen_teaching \
  --duration 30s \
  --hook shocking

# フォーマット一覧
python3 skills/video-scriptwriter/scripts/generate_script.py --list-formats
```

## オプション

| オプション | デフォルト | 説明 |
|-----------|----------|------|
| `--topic` | (必須) | 動画のトピック/テーマ |
| `--format` | standard_teaching | フォーマット |
| `--duration` | 30s | 動画尺 (15s/30s/60s) |
| `--language` | ja | 言語 |
| `--hook` | question | Hookスタイル (question/shocking/pov/wait/ranking/dark/nobody/comparison) |
| `--output` | auto | 出力ディレクトリ |
| `--instructions` | - | 追加指示テキスト |

## 出力: scenes.json

storyboard-generator / video-audio / video-editor と互換性のあるフォーマット:

```json
{
  "title": "動画タイトル",
  "format": "split_screen_teaching",
  "scenes": [
    {
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "scene_type": "hook",
      "narration": "ナレーション",
      "text_overlay": { "main_text": "テロップ" },
      "visual_prompt": "English prompt for image gen...",
      "motion_type": "i2v"
    }
  ],
  "metadata": {
    "target_audience": "...",
    "estimated_retention_hooks": ["hook手法", "段階的情報開示"]
  }
}
```

## パイプライン連携

```
scriptwriter (テーマ → scenes.json)
  ↓
storyboard-generator (scenes.json → AI画像)
  ↓
video-audio (scenes.json → TTS音声)
  ↓
video-editor (画像 + 音声 → 最終動画)
```

## Playbook連携

`video-playbook` に蓄積された知見を自動参照:
- 平均シーン長、ペーシング
- 構成パターン
- テロップスタイル
- 効果的なテクニック

## 依存
- Gemini API (`GEMINI_API_KEY`)
- video-playbook (オプション、知見参照)
