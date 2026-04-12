---
name: viral-short-video
description: "TikTok/YouTube Shorts向けのバイラル動画スクリプト&ストーリーボード生成スキル。 調査済みのバイラルテクニック（3秒フック、モジュラー構造、ループブリッジ、フラッシュテキスト、 スプリットスクリーン等）をスクリプティングとストーリーボード作成に自動組み込み。 「TikTok動画のスクリプト」「バイラル動画を作りたい」「Short動画の台本」等で発動。"
triggers:
  - バイラル動画を作りたい
  - TikTok動画のスクリプト
  - Short動画の台本
  - バズる動画を作りたい
  - リール動画の企画
  - viral-short-video
  - TikTok Shorts
---

# Viral Short Video - バイラルショート動画スクリプト&ストーリーボード

TikTok / YouTube Shorts 向けのバイラル動画制作パイプライン。
調査に基づくバイラルテクニックをスクリプトに自動埋め込みし、
既存の `storyboard-generator` / `video-editor` と連携して動画を生成する。

## パイプライン全体像

```
[トピック/商材/ターゲット]
  ↓
[generate_viral_script.py]  ← このスキルの中核
  ├─ viral_script.json       (バイラル構造化スクリプト)
  ├─ scenes.json             (storyboard-generator互換)
  ├─ hook_variants.json      (フックバリエーション x3)
  └─ hook_analysis.json      (--analyze-video時: ピークフック分析)
  ↓
[storyboard-generator]       ← 既存スキル
  ├─ frames/                 (絵コンテ画像)
  └─ scenes.json             (拡張済み)
  ↓
[video-editor]               ← 既存スキル（拡張済み）
  ├─ キャプション焼き込み
  ├─ フラッシュテキスト挿入
  ├─ スプリットスクリーン合成 (背景オーバーレイ方式)
  └─ 最終動画.mp4
```

## 同梱アセット

### ゲームプレイ背景素材 (`assets/gameplay/`)

| プリセット名 | ゲーム | 長さ | 備考 |
|-------------|--------|------|------|
| subway_surfers | Subway Surfers | 26分 | 縦型HD, No Copyright |
| minecraft | Minecraft Parkour | 5分 | 縦型2K 60fps, No Copyright |

### フックコンピレーション素材 (`assets/hooks/`)

| プリセット名 | 内容 | 用途 |
|-------------|------|------|
| hook_viral_10 | 10 TikTok Hooks You Can Use To Go Viral | フック実例集: 10パターン |
| hook_trifecta | This HOOK Combo Will Get You Viral on TikTok | フック三位一体戦略+実例 |
| hook_600k_gmv | This Hook Made $600K GMV on TikTok Shop | $600K売上フック分解 |

初回セットアップ: `bash skills/viral-short-video/scripts/download_assets.sh`

## Usage

```bash
# 基本: トピックからバイラルスクリプト生成
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "仮想通貨ウォレットの安全な使い方" \
  --duration 30 \
  --target "20-30代の仮想通貨初心者" \
  --session "crypto_wallet_tips"

# 商材名を指定してスクリプト生成
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "このアプリで送金手数料を90%カットする方法" \
  --product "My Product" \
  --duration 15 \
  --tone casual \
  --session "tp_fees"

# ストーリーボード生成まで一気通貫
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "AIで動画を作る方法" \
  --duration 60 \
  --generate-storyboard \
  --character "20代の日本人女性、カジュアルな服装" \
  --session "ai_video_tutorial"

# dry-run（スクリプトのみ生成、画像生成なし）
python skills/viral-short-video/scripts/generate_viral_script.py \
  --topic "3つの投資の間違い" \
  --duration 30 \
  --dry-run

# ピークフック抽出: 同梱のフックコンピレーション動画を分析
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_viral_10 \
  --topic "仮想通貨ウォレット" --duration 30

# ピークフック抽出: カスタム動画を分析
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video path/to/any_viral_video.mp4 \
  --topic "アプリ紹介" --duration 15

# ピークフック抽出: dry-run（分析結果の表示のみ）
python skills/viral-short-video/scripts/generate_viral_script.py \
  --analyze-video hook_trifecta \
  --topic "副業" --dry-run
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --topic | Yes | - | 動画のトピック/テーマ |
| --product | No | - | 商材/サービス名 |
| --duration | No | 30 | 動画の長さ（秒）: 15, 30, 60 |
| --target | No | - | ターゲット層の説明 |
| --tone | No | casual | トーン: casual, professional, energetic, storytelling |
| --hook-style | No | auto | フックスタイル: curiosity, fomo, social_proof, pattern_interrupt, contrarian |
| --split-screen | No | false | スプリットスクリーン用の指示を含める |
| --flash-text | No | true | フラッシュテキスト（リウォッチ誘導）を含める |
| --loop | No | true | ループブリッジ（冒頭回帰）を含める |
| --variants | No | 3 | フックバリエーション数 |
| --generate-storyboard | No | false | scenes.json生成後にstoryboard-generatorを呼び出す |
| --character | No | - | ストーリーボード用キャラクター説明 |
| --session | No | - | セッション名（出力フォルダ名） |
| --dry-run | No | false | スクリプトのみ生成（APIコール最小） |
| --lang | No | ja | スクリプト言語: ja, en |
| --analyze-video | No | - | ピークフック抽出。プリセット名(hook_viral_10, hook_trifecta, hook_600k_gmv)またはファイルパス |

## Output Structure

```
output/viral-scripts/
└── YYYYMMDD_HHMMSS_session/
    ├── viral_script.json      # メインスクリプト（バイラル構造化）
    ├── scenes.json            # storyboard-generator互換形式
    ├── hook_variants.json     # フックバリエーション
    ├── hook_analysis.json     # ピークフック分析結果（--analyze-video時のみ）
    └── storyboard/            # --generate-storyboard時のみ
        ├── frames/
        ├── storyboard_sheet.png
        └── scenes.json
```

## viral_script.json フォーマット

```json
{
  "meta": {
    "topic": "トピック",
    "product": "商材名",
    "duration": 30,
    "target": "ターゲット層",
    "tone": "casual"
  },
  "hook": {
    "text": "正直これ教えたくなかったんだけど...",
    "duration": 3,
    "trigger_type": "curiosity_gap",
    "visual_note": "目を見開いてカメラに向かって話す",
    "emotion": "surprise"
  },
  "body": [
    {
      "text": "実はこのアプリ使うだけで送金手数料が...",
      "duration": 5,
      "visual_note": "スマホ画面を見せながら説明",
      "motion_type": "i2v"
    }
  ],
  "cta": {
    "text": "リンクはプロフィールから。今すぐチェックして",
    "duration": 3,
    "visual_note": "画面下を指差す",
    "emotion": "friendly"
  },
  "loop_bridge": {
    "enabled": true,
    "end_text": "さっき言った一番ヤバいやつだけど...",
    "connects_to": "hook",
    "visual_note": "冒頭と同じカメラアングルに戻る"
  },
  "flash_text": {
    "enabled": true,
    "text": "最後まで見た？もう一回見て",
    "color": "red",
    "duration_frames": 3,
    "position": "center"
  },
  "viral_techniques": {
    "split_screen": false,
    "captions": true,
    "lofi_aesthetic": true,
    "fast_pace": true,
    "speech_speed": 1.2
  },
  "hook_variants": [
    {
      "text": "99%の人がこれ知らないんだけど...",
      "trigger_type": "curiosity_gap"
    },
    {
      "text": "これ見逃したらマジで損する",
      "trigger_type": "fomo"
    },
    {
      "text": "100万人が使ってるのに誰も教えてくれない",
      "trigger_type": "social_proof"
    }
  ]
}
```

---

## バイラルテクニック チートシート

### 1. 冒頭3秒フック（最重要）

**データ**: 3秒維持率65%超 → 4-7xインプレッション / エンゲージメント+340%

**7つの心理トリガー** (バイラル動画の84.3%で使用):

| # | トリガー | 日本語フック例 | 英語フック例 |
|---|---------|--------------|-------------|
| 1 | パターンインタラプト | 「ちょっと待って、これ見て」 | "Wait, look at this" |
| 2 | キュリオシティギャップ | 「99%の人が知らない〇〇」 | "Nobody tells you this about..." |
| 3 | FOMO | 「今だけ」「これ見逃したら損」 | "You're missing out on..." |
| 4 | ソーシャルプルーフ | 「100万人が使ってる」 | "1M people already use this" |
| 5 | 感情的覚醒 | 「マジでヤバい」「信じられない」 | "I can't believe this works" |
| 6 | サプライズ | （目を見開く + 沈黙1秒） | (wide eyes + 1s pause) |
| 7 | 個人的関連性 | 「〇〇な人だけ見て」 | "If you're a [target], watch this" |

### 2. モジュラー構造

```text
[Hook: 0-3秒] → [Body: 3-15秒] → [CTA: 15秒+]
```

- 効果: 制作コスト-40%、テスト速度2x
- Hook部分だけ差し替えてA/Bテスト

### 3. ループブリッジ

- 効果: リウォッチ = アルゴリズムブースト+84%
- 70%完視聴率 → アルゴリズム推進
- 92%完視聴率 → 3xリーチ（Sticky Content認定）
- パターン: 動画の最後で「さっき言った〇〇だけど...」→ 冒頭に戻る

### 4. フラッシュテキスト（リウォッチトリガー）

- 最後の2-3フレーム（0.1秒未満）に赤/黒文字を一瞬表示
- 意識的に読めない速度 → 「今なんか見えた？」→ リウォッチ
- テキスト例: 「もう一回見て」「隠しメッセージ」「気づいた？」
- 色: 赤（緊急性・目立つ） or 黒背景に白文字（ミステリアス）

### 5. 背景ゲームプレイ（オーバーレイ方式）

- 全画面背景: Minecraft/Subway Surfers → 上部にメインコンテンツをオーバーレイ
- TikTokスタイル: ゲームプレイが全画面(1080x1920)、メインが上部(1080x960)
- 効果: 平均視聴時間+40%、コメント・シェア2x
- Gen Z(18-24歳)の67%に特に有効
- プリセット素材同梱: `subway_surfers`, `minecraft`
- 注意: ブランドイメージを損なう可能性 → オーガニック投稿向け推奨

### 6. ピークフック抽出

- バズ動画の最もフックの強い瞬間を自動特定
- video-frame-reader + Gemini Flash Vision でスコアリング
- 抽出したフックパターンでスクリプト再構成案を自動生成
- 同梱のフックコンピレーション素材(3本)で即座に分析可能

### 7. 字幕（キャプション）

- 85%がミュート視聴 → 字幕で維持率+31%、エンゲージメント+38%
- TikTokセーフゾーン: Y位置55-65%（上15%・下20%は避ける）
- 日本語: 1行5-8文字、最大2行、太字白+黒縁3px

### 8. ロファイ感（UGC風）

- UGC風 vs プロ品質: CTR 4x、コンバージョン率+29%
- iPhone撮影風のカジュアルな雰囲気
- 背景: 自宅風、カフェ風など自然な環境

### 9. 音声ペース

- 1.1-1.3xの速い音声 → 離脱防止
- 間を詰めて情報密度を上げる

---

## 連携スキル

| スキル | 役割 | 連携方法 |
|-------|------|---------|
| `storyboard-generator` | scenes.json → 絵コンテ画像 | `--generate-storyboard` で自動連携 |
| `video-editor` | 最終動画合成（キャプション/フラッシュ/背景オーバーレイ） | `compose_video.py --flash-text --split-screen subway_surfers` |
| `video-frame-reader` | 動画のキーフレーム抽出 | `--analyze-video` で自動連携 |
| `banner-creator` | サムネイル生成 | 別途実行 |
| `social-content` | 投稿文・ハッシュタグ生成 | 別途実行 |

## Requirements

- `GEMINI_API_KEY`: Gemini Flash（スクリプト生成）用
- Python packages: google-genai, python-dotenv
- `storyboard-generator` の依存（絵コンテ生成時のみ）
- `ffmpeg`（動画合成時のみ）

## Trigger Phrases

- 「TikTok動画のスクリプトを作って」
- 「バイラル動画を作りたい」
- 「Short動画の台本」
- 「TikTok用のスクリプト生成」
- 「バズる動画を作りたい」
- 「リール動画の企画」
