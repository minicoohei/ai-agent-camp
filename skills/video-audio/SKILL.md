---
name: video-audio
description: |
  動画用音声生成スキル。ElevenLabs TTS APIでscenes.jsonのナレーションから
  音声ファイルを生成し、動画と同期可能な形式で出力する。
  「ナレーション生成」「TTS」「音声追加」等で発動。
triggers:
  - ナレーション生成
  - 音声を生成
  - TTSで読み上げ
  - 動画に音声を追加
  - ボイスを選んで
  - video-audio
  - ElevenLabs
---

# Video Audio (TTS)

scenes.json の narration フィールドから ElevenLabs TTS で音声を生成する。

## クイックスタート

```bash
# 全ナレーションを結合した1ファイル生成
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --output output/narration.mp3

# フレームごとに個別ファイル生成
python skills/video-audio/scripts/generate_audio.py \
  --storyboard-dir output/storyboard/YYYYMMDD_session \
  --voice akari \
  --per-scene
```

## 日本語ボイス一覧

| ID | 名前 | 特徴 | エイリアス |
|----|------|------|-----------|
| EkK6wL8GaH8IgBZTTDGJ | Akari | 明るく自然な女性 | `akari` |
| EnLxjGl88dNO1Jv6AZk2 | Miyu | 信頼性と深みのある声 | `miyu` |
| G3EZ8O36A0x9lmeOtr0f | Kaori | 親しみやすいフレンドリー | `kaori` |
| PmgfHCGeS5b7sH90BOOJ | Fumi | 落ち着いた女性 | `fumi` |
| StTDrGrPSyfaHGmzwXbj | Masa | 日本語男性 | `masa` |
| gARvXPexe5VF3cKZBian | Mitsuki | ニュートラル | `mitsuki` |
| sRYzP8TwEiiqAWebdYPJ | Hatake Kohei | ボイスアクター | `kohei` |

## オプション

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--voice` | `akari` | ボイス名またはID |
| `--model` | `eleven_multilingual_v2` | TTSモデル |
| `--stability` | `0.5` | 安定性 (0-1) |
| `--similarity` | `0.75` | 類似度ブースト (0-1) |
| `--speed` | `1.0` | 再生速度 |
| `--per-scene` | false | フレームごとに個別ファイル出力 |
| `--silence-gap` | `0.3` | シーン間の無音（秒） |
| `--output` | auto | 出力ファイルパス |

## 出力

### 結合モード（デフォルト）
```
{storyboard_dir}/audio/narration.mp3    # 全ナレーション結合
{storyboard_dir}/audio/narration.json   # タイムスタンプ情報
```

### per-scene モード
```
{storyboard_dir}/audio/frame_01.mp3
{storyboard_dir}/audio/frame_02.mp3
...
{storyboard_dir}/audio/timestamps.json  # 各フレームの開始・終了時刻
```

## timestamps.json フォーマット
```json
{
  "total_duration": 18.5,
  "scenes": [
    {
      "frame_number": 1,
      "start": 0.0,
      "end": 2.8,
      "duration": 2.8,
      "text": "ナレーション台本"
    }
  ]
}
```

## 動画との統合

compose_video.py で `--audio` オプションに渡す:
```bash
python skills/video-editor/scripts/compose_video.py \
  --storyboard-dir output/storyboard/session \
  --audio output/storyboard/session/audio/narration.mp3
```

Remotion の場合は `public/audio/narration.mp3` に配置し、`<Audio>` コンポーネントで参照。

## 環境変数
- `ELEVEN_API_KEY` — ElevenLabs API キー（必須）

## 依存
- Python 3.11+
- curl (ElevenLabs API呼び出し)
- ffmpeg (音声結合用、`.bin/ffmpeg`)
