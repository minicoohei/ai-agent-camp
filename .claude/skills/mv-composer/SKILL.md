---
name: mv-composer
description: "Remotion + Kling i2v でプロモーションMV動画・バイラルショート動画を生成するスキル。 「MV作成」「動画を作って」「プロモーション動画」「TikTok動画」等のリクエストで発動。"
triggers:
  - MV作成
  - 動画を作って
  - プロモーション動画
  - TikTok動画を作って
  - ショート動画
  - mv-composer
  - Remotion動画
  - バイラル動画
---

## トリガーキーワード

MV作成, 動画を作って, プロモーション動画, Remotion動画, アニメMV, 宣伝動画, 広告動画,
TikTok動画, ショート動画, バイラル動画, リール, Short動画の台本, バズる動画

# MV Composer — Remotion + i2v 動画生成（横型 & 縦型）

Remotion（React ベース動画フレームワーク）と Kling 3.0 i2v を組み合わせ、
プロモーションMV動画・バイラルショート動画を自動生成するスキル。

**主な用途**:
- **横型 (16:9)**: サービス/講座の宣伝MV、SNS広告動画、LP埋め込み動画
- **縦型 (9:16)**: TikTok、YouTube Shorts、Instagram Reels
- **正方形 (1:1)**: Instagram フィード

---

## フォーマットプリセット

| プリセット | 解像度 | アスペクト比 | 用途 |
|-----------|--------|------------|------|
| horizontal | 1920x1080 | 16:9 | YouTube, LP埋め込み, SNS広告 |
| vertical | 1080x1920 | 9:16 | TikTok, YouTube Shorts, Reels |
| square | 1080x1080 | 1:1 | Instagram フィード |

Root.tsx で `PRESETS.horizontal` / `PRESETS.vertical` / `PRESETS.square` を切り替え。
MVComposition.tsx の `useScale()` で自動スケール。

---

## アーキテクチャ概要

```
台本（AIDA 8シーン or バイラル Hook→Body→CTA）
  ↓
┌─────────────────────────────────────────────────┐
│ 素材生成（並列実行）                              │
│  ├─ Gemini 3 Pro: イラスト生成 + ロゴ生成        │
│  ├─ ElevenLabs: ナレーション音声 (TTS)            │
│  └─ Kling 3.0 (fal.ai): i2v アニメーション (1-2本)│
└─────────────────────────────────────────────────┘
  ↓
┌─────────────────────────────────────────────────┐
│ Remotion コンポジション                          │
│  ├─ シーンコンポーネント                          │
│  │   ├─ i2v動画背景 (OffthreadVideo)             │
│  │   ├─ 静止画背景 (Img + Ken Burns)             │
│  │   └─ React MG (SVGチャート/ターミナル等)       │
│  ├─ テロップ（グラデーション背景バー付き）        │
│  ├─ ナレーション音声 + BGM                        │
│  ├─ ロゴ/ウォーターマーク                         │
│  └─ CrossFade トランジション                      │
└─────────────────────────────────────────────────┘
  ↓
npx remotion render → MP4 (H.264)
```

---

## 制作フロー（横型プロモーションMV）

### Step 1: 台本設計

8シーンの AIDA 構成で台本を作成する。

```
F1: Hook（フック）     — 共感を引く問題提起
F2: Problem（課題）    — 具体的な痛みの描写
F3: Insight（気づき）  — パラダイムシフトの一言
F4: Evidence（証拠）   — 市場データ/成長曲線
F5: Split（比較）      — Before/After の対比
F6: Demo（実演）       — 実際の操作画面
F7: Proof（信頼）      — ツール連携/実績
F8: CTA（行動喚起）   — 価格 + ボタン + ブランド
```

各シーンに必要な情報:
- `dur`: ナレーション尺（秒）
- `terop`: テロップテキスト（main / sub）
- `motion_type`: `i2v` | `ken_burns` | `react_mg` | `static`

### Step 2: 素材生成

**イラスト生成（Gemini 3 Pro）:**
```bash
python cursor_tools/nanobanana.py \
  --prompt "Anime style, frustrated person at desk with laptop, warm amber lighting, dark room" \
  --output public/assets/illustrations/f1_scene.jpg
```

**ナレーション生成（ElevenLabs）:**
```bash
# voice_id: Hajime = SOuiRq8aXqyALuq5QIQ8（日本語男性）
# 生成後 ffmpeg atempo=1.15 で高速化
ffmpeg -i narration_raw.mp3 -filter:a "atempo=1.15" -y narration_fast/frame_01.mp3
```

### Step 3: i2v アニメーション生成（Kling 3.0）

**重要**: 1動画あたり i2v は **1-2シーンに限定**。コスト最適化のため。

```bash
cd mv-composer
export $(grep '^FAL_KEY=' ../.env | tr -d '"' | xargs)
python3.11 scripts/i2v_batch.py
```

### Step 4: Remotion コンポジション

MVComposition.tsx の scenes 配列を編集し、各シーンコンポーネントを実装。

### Step 5: レンダリング & レビュー

```bash
# 横型レンダリング
npx remotion render src/index.ts MV01-anime output/mv01_final.mp4 --codec h264

# 縦型レンダリング
npx remotion render src/index.ts MV01-vertical output/mv01_vertical.mp4 --codec h264

# フレーム抽出で目視確認
ffmpeg -ss 2 -i output/mv01_final.mp4 -vframes 1 -q:v 2 /tmp/check_f1.jpg
```

---

## 縦型動画（TikTok/Shorts）の制作フロー

### バイラルスクリプト生成

```bash
cd mv-composer
python3.11 scripts/generate_viral_script.py \
  --topic "AIで業務を自動化する方法" \
  --duration 30 \
  --target "30代のビジネスパーソン" \
  --session "ai_automation"
```

出力の `viral_script.json` を読み、scenes 配列を MVComposition.tsx に反映して Remotion でレンダリング。

### ピークフック抽出（バズ動画分析）

```bash
# プリセット素材をダウンロード（初回のみ）
bash scripts/download_assets.sh

# バズ動画のフックを分析
python3.11 scripts/generate_viral_script.py \
  --analyze-video hook_viral_10 \
  --topic "AI自動化" --duration 30
```

### generate_viral_script.py パラメータ

| Parameter | Default | Description |
|-----------|---------|-------------|
| --topic | (必須) | 動画のトピック |
| --product | - | 商材/サービス名 |
| --duration | 30 | 動画の長さ: 15, 30, 60 |
| --target | - | ターゲット層 |
| --tone | casual | casual / professional / energetic / storytelling |
| --hook-style | auto | auto / curiosity / fomo / social_proof / pattern_interrupt / contrarian |
| --split-screen | false | スプリットスクリーン指示 |
| --analyze-video | - | ピークフック抽出（プリセット名 or ファイルパス） |
| --dry-run | false | 結果表示のみ |

### 縦型レイアウトの注意事項

- テロップ: TikTokセーフゾーン Y位置55-65%（上15%・下20%は避ける）
- 字幕: 1行5-8文字、最大2行、太字白+黒縁3px
- `useScale()` でフォントサイズ自動調整（`s = width / 1920`）

---

## バイラルテクニック チートシート

### 1. 冒頭3秒フック（最重要）

**データ**: 3秒維持率65%超 → 4-7xインプレッション / エンゲージメント+340%

**7つの心理トリガー** (バイラル動画の84.3%で使用):

| # | トリガー | 日本語フック例 | 英語フック例 |
|---|---------|--------------|-------------|
| 1 | パターンインタラプト | 「ちょっと待って、これ見て」 | "Wait, look at this" |
| 2 | キュリオシティギャップ | 「99%の人が知らない○○」 | "Nobody tells you this about..." |
| 3 | FOMO | 「今だけ」「これ見逃したら損」 | "You're missing out on..." |
| 4 | ソーシャルプルーフ | 「100万人が使ってる」 | "1M people already use this" |
| 5 | 感情的覚醒 | 「マジでヤバい」「信じられない」 | "I can't believe this works" |
| 6 | サプライズ | （目を見開く + 沈黙1秒） | (wide eyes + 1s pause) |
| 7 | 個人的関連性 | 「○○な人だけ見て」 | "If you're a [target], watch this" |

### 2. モジュラー構造

```
[Hook: 0-3秒] → [Body: 3-15秒] → [CTA: 15秒+]
```

Hook部分だけ差し替えてA/Bテスト。制作コスト-40%、テスト速度2x。

### 3. ループブリッジ

- リウォッチ = アルゴリズムブースト+84%
- 70%完視聴率 → アルゴリズム推進
- パターン: 動画の最後で「さっき言った○○だけど...」→ 冒頭に戻る

### 4. フラッシュテキスト

- 最後の2-3フレーム（0.1秒未満）に赤/黒文字を一瞬表示
- 意識的に読めない速度 → リウォッチ誘導
- テキスト例: 「もう一回見て」「隠しメッセージ」「気づいた？」

### 5. 字幕（キャプション）

- 85%がミュート視聴 → 字幕で維持率+31%、エンゲージメント+38%
- TikTokセーフゾーン: Y位置55-65%（上15%・下20%は避ける）

### 6. 音声ペース

- 1.1-1.3xの速い音声 → 離脱防止
- ElevenLabs の場合 `atempo=1.15` で後処理

---

## クオリティチェックリスト（v1→v16 で確立）

### 視認性
- [ ] テロップ main: **52px以上**（bold時 64px以上）※横型基準、縦型は自動スケール
- [ ] テロップ sub: **32px以上**
- [ ] テロップ背景: 下部グラデーションバー必須
- [ ] 吹き出し/ラベル: **24px以上**、背景の不透明度 0.14 以上

### ロゴ・ブランド
- [ ] ロゴを入れるなら **存在感のあるサイズ** にする（小さいなら入れない）
- [ ] ウォーターマーク: 140px 幅、opacity 0.5 以上
- [ ] ツールロゴ: コンテナ 88px、アイコン 60px、名前 20px

### 色彩・バリエーション
- [ ] 全シーン同色系にしない。最低2色系統を混ぜる
- [ ] F8 CTA は白背景推奨（暗い背景ではロゴが見えない）

### モーション
- [ ] i2v は **1-2シーン** に限定（コスト＋品質のバランス）
- [ ] 静止画シーンは Ken Burns（scale 1→1.04~1.08）で動きをつける
- [ ] React MG: spring animation + interpolate で生き生きと

### データ可視化
- [ ] 棒グラフより**折れ線グラフ（成長曲線）**のほうがダイナミック
- [ ] SVG dashOffset アニメーションで線を描画する演出

---

## Video QA パイプライン（11ステージ多段チェック）

レンダリング済みMVの品質を自動検証するパイプライン。
ローカル検証（Phase 1）→ AI音声検証（Phase 2）→ AI映像検証（Phase 3）→ AIディレクターレビュー（Phase 4）の順に実行。

### 実行方法

```bash
# 全11ステージ実行
python3.11 scripts/video_qa.py output/clearpay_mv_v4.mp4 clearpay

# 新ステージのみ（安価なローカル + ディレクターレビュー）
python3.11 scripts/video_qa.py output/clearpay_mv_v4.mp4 clearpay --stages lufs pacing director

# ローカルチェックのみ（$0）
python3.11 scripts/video_qa.py output/clearpay_mv_v4.mp4 clearpay --stages metadata black silence sync lufs pacing

# 全MV自動検出
python3.11 scripts/video_qa.py
```

### 11ステージ一覧

| # | Phase | Stage | チェック内容 | 手法 | コスト |
|---|-------|-------|------------|------|--------|
| 1 | ローカル | metadata | 解像度・尺・コーデック | ffprobe | $0 |
| 2 | ローカル | black_frames | 黒フレーム（トランジション除外） | ffmpeg blackdetect | $0 |
| 3 | ローカル | silence | 1.5s超の無音区間 | ffmpeg silencedetect | $0 |
| 4 | ローカル | narration_sync | ナレーション尺 vs シーン尺 | ffprobe | $0 |
| 5 | ローカル | **lufs** | **音量バランス（LUFS）** | ffmpeg loudnorm | $0 |
| 6 | ローカル | **pacing** | **ペーシング分析（詰まり/間延び検出）** | ffprobe | $0 |
| 7 | AI音声 | audio_accuracy | Whisper書き起こし + 発音比較 | fal.ai Whisper + Gemini | ~$0.001 |
| 8 | AI映像 | visual + terop | マルチフレーム映像品質 + テロップOCR照合 | Gemini Vision ×8 | ~$0.0015 |
| 9 | AI映像 | i2v_quality | i2vアーティファクト検出 | Gemini Vision + PIL diff | ~$0.0004 |
| 10 | AIレビュー | **director** | **5軸スコアリング + 改善P1/P2/P3** | Gemini Vision (8画像) | ~$0.002 |
| | | **合計** | | | **~$0.005** |

### シーケンス図・詳細設計

→ [docs/video-qa-sequence.md](docs/video-qa-sequence.md)

### 新ステージ詳細

**Stage 5: LUFS音量バランス**:
- ffmpeg loudnorm で全体 + シーン別の統合ラウドネス（LUFS）を測定
- BGMがナレーションを食っている、シーン間の音量差が大きい場合に警告
- Pass条件: シーン間差 < 8dB、全体 > -24dB

**Stage 6: ペーシング分析**:
- ナレーション尺 ÷ シーン尺 の比率を計算
- > 0.95: cramped（詰まりすぎ）、< 0.4: sparse（間延び）
- 各シーンのゲージ表示で直感的に確認可能

**Stage 10: AIディレクターレビュー**:
- 全シーン代表フレーム（50%地点）×8枚 + 全ナレーションテキストをGemini Visionに一括投入
- SaaS企業のシニアクリエイティブディレクター視点で5軸評価:
  - Storytelling / Visual Quality / Text Design / Pacing / Brand Consistency
- 各軸10点満点、合計100点。P1改善案が2件以上なら FAIL
- 強み + 改善案（P1/P2/P3優先度付き + 具体的なシーン指定）を出力

### 多段チェックによる精度向上

**音声精度向上** (Stage 7):
- narration_qa.py の Whisper+Gemini パイプラインを再利用
- fal.ai Whisper で書き起こし → pykakasi でひらがな変換 → Gemini で発音比較
- 「人材→臨済」「立場→直ち」等の TTS 発音エラーを自動検出

**映像精度向上** (Stage 8):
- シーンあたり2フレーム (30% + 70%) を1回の Gemini Vision 呼出に統合
- テロップ検出: Gemini OCR → ひらがな変換 → スライディングウィンドウ部分一致（UI内テキストとの誤照合を回避）
- デザインスコア + フレーム間変化量で総合評価

**i2v品質判定** (Stage 9):
- i2v元ファイルから3フレーム (0.5s, 2.5s, 4.5s) を抽出
- PILでフレーム差分を計算（モーション量の定量評価）
- Gemini Vision で顔の歪み・テクスチャ崩壊・フリッカーを検出

---

## ファイル構成

```
mv-composer/
├── src/
│   ├── index.ts              # registerRoot
│   ├── Root.tsx              # Composition 定義（PRESETS: horizontal/vertical/square）
│   └── MVComposition.tsx     # 全シーンコンポーネント + useScale() + メイン構成
├── public/
│   ├── bgm.mp3
│   ├── narration/
│   ├── narration_fast/       # frame_01.mp3 ~ frame_08.mp3
│   └── assets/
│       ├── logo.png
│       ├── i2v/              # Kling 生成動画（1-2本）
│       ├── illustrations/    # Gemini 生成イラスト
│       ├── logos/            # ツール/企業ロゴ
│       ├── hooks/            # フック分析用素材（download_assets.sh で取得）
│       └── gameplay/         # ゲームプレイ背景素材（同上）
├── scripts/
│   ├── video_qa.py                 # 8ステージ多段QAパイプライン ★
│   ├── narration_qa.py             # ナレーション TTS→STT→比較→自動修正
│   ├── i2v_batch.py                # Kling 3.0 バッチ i2v 生成
│   ├── generate_viral_script.py    # バイラルスクリプト生成 + フック分析
│   └── download_assets.sh          # フック/ゲームプレイ素材DL
├── output/                   # レンダリング済み MP4
├── package.json
├── tsconfig.json
└── remotion.config.ts
```

---

## 必須環境

| 項目 | 値 |
|------|-----|
| Node.js | 18+ |
| Python | 3.11+（i2v / スクリプト生成用） |
| FAL_KEY | fal.ai APIキー（Kling 3.0 用） |
| ELEVEN_API_KEY | ElevenLabs APIキー（TTS 用） |
| GEMINI_API_KEY | Gemini API（イラスト/ロゴ/スクリプト生成） |

---

## コスト目安（1本あたり）

| 項目 | 単価 | 数量 | 小計 |
|------|------|------|------|
| Kling 3.0 i2v | $0.35/5秒 | 2本 | $0.70 |
| ElevenLabs TTS | ~$0.05/シーン | 8本 | $0.40 |
| Gemini イラスト | 無料枠 | 6枚 | $0.00 |
| Gemini スクリプト | 無料枠 | 1回 | $0.00 |
| Remotion レンダリング | ローカル | 1回 | $0.00 |
| **合計** | | | **~$1.10** |

---

## よくある改善パターン

| 問題 | 解決策 |
|------|--------|
| テロップが小さくて読めない | 52px+、グラデーション背景バー追加 |
| ロゴが小さくて存在感ない | 入れるなら大きく。小さいなら入れない |
| 全シーン同じ色で単調 | 暖色/寒色を混ぜる、React MG シーンを挟む |
| 棒グラフがつまらない | 折れ線の描画アニメーション + グローライン |
| 静止画が動かなくて安っぽい | 1-2シーンだけ i2v、残りは Ken Burns |
| CTA が目立たない | 白背景 + 大きいロゴ + パルスするボタン |
| ナレーションが遅い | atempo=1.15 で高速化（ピッチ変化なし） |
| 縦型でレイアウト崩れ | useScale() でスケールファクター適用 |
| 絵文字アイコン3連が安っぽい | UIモックアップパネルに置換（下記テンプレート参照） |
| テロップとシーン内テキストが被る | テキスト内蔵シーンは terop: null にする（下記ルール参照） |

---

## 日本語TTS発音QAパイプライン

ElevenLabs eleven_multilingual_v2 は漢字の誤読が頻発する。
**必ず Whisper STT で検証し、NG なら読みがなヒントで再生成する。**

### 既知の誤読パターン（ElevenLabsで確認済み）

| 原文 | 誤読 | 修正（ひらがな/カタカナ） |
|------|------|-------------------------|
| 承認 | チョンキン | しょうにん |
| 着金 | ちゃくきん（OK） / 着きん | ちゃくきん |
| 60日 | 翌日 | ろくじゅうにち |
| 払った | はばった | 支払った |
| 成果 | 成功 | せいか |
| ClearPay | クリアペー | クリアペイ |
| USDC | （無音/不明瞭） | ユーエスディーシー |
| CPA | （不明瞭） | シーピーエー |
| 承認率 | 成人率 | しょうにんりつ |
| 品質スコア | — | ひんしつスコア |

### QAフロー

```
1. ElevenLabs TTS で音声生成
2. fal.ai Whisper で書き起こし（language: "ja"）
3. 原文と比較（句読点除去で部分一致チェック）
4. NG → ひらがな読みヒントに置換して再生成
5. 再度 Whisper で検証 → PASS まで繰り返し
```

### 丁寧語バリアント

ナレーションのトーンを変える場合（丁寧語、カジュアル等）:
- 全シーンのテキストを書き換えてからバッチ再生成
- 丁寧語化で尺が伸びることが多い → シーン dur の再調整必須
- 例: 「それだけ。」→「それだけです。」で +0.5s 程度

---

## テロップ被り防止ルール

**原則**: シーンに複合テキスト要素が内蔵されている場合、Terop オーバーレイは付けない。

### 判定基準

| シーンタイプ | テキスト内蔵 | terop |
|-------------|------------|-------|
| i2v 背景のみ | なし | **あり**（main + sub） |
| Ken Burns + シンプル背景 | なし | **あり** |
| ブランドリビール（ロゴ+タグライン） | あり | **null** |
| UIモックアップ（パネル+ラベル） | あり | **null** |
| ダッシュボード（メトリクス+チャート） | あり | **null** |
| CTA（ロゴ+スローガン） | あり | **null** |

被りが発生すると情報が二重になり安っぽく見える。
テキスト内蔵シーンではシーンコンポーネント内でフォントサイズ・配置を完結させる。

---

## React MG シーンテンプレート集

### 1. UIモックアップパネル（ClearPay F4実績）

ガラスモーフィズムの2パネル構成。プロダクトのUXを視覚化する。

```
Phase 1 (0–50f): パネルが左右からスライドイン
  - 左パネル: 操作ステップ1（タイプライターURLなど）
  - 右パネル: 操作ステップ2（カウンターアップなど）
Phase 2 (50–70f): 各パネルにチェックマーク出現
Phase 3 (70f+): パネルが左右に退場 → パンチラインテキスト中央表示
```

**パネルスタイル:**
```tsx
background: "rgba(255,255,255,0.04)",
backdropFilter: "blur(20px)",
borderRadius: 20 * s,
border: "1px solid rgba(255,255,255,0.08)",
boxShadow: "0 12px 48px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06)",
```

**タイプライター演出:**
```tsx
const urlChars = Math.min(Math.floor(Math.max(0, frame - delay) * 1.8), fullText.length);
// カーソル点滅: frame % 12 < 6 ? 1 : 0
```

**カウンターアップ:**
```tsx
const amount = interpolate(frame, [startF, endF], [0, targetValue], {
  extrapolateLeft: "clamp", extrapolateRight: "clamp",
});
```

### 2. ダッシュボード（メトリクスカード + バーチャート）

暗い背景 + グリッドオーバーレイ + 3枚のカード + バーチャート。
KPI を視覚化する汎用テンプレート。

```
- メトリクスカード: spring で順次出現、値はカウントアップ
- バーチャート: 各バーが spring で下から伸びる
- グリッド背景: transform: translateY(frame * 0.3 % 60) でゆっくり流れる
```

### 3. 3フェーズアニメーション パターン

**汎用構造**: 「見せる → 完了 → 退場 → パンチライン」

```tsx
// Phase 1: 要素が登場
const enterSpring = spring({ frame: Math.max(0, frame - delay), fps, ... });
// Phase 2: 完了マーク
const checkSpring = spring({ frame: Math.max(0, frame - 30), fps, ... });
// Phase 3: 要素が退場
const exit = interpolate(frame, [70, 85], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
// Phase 4: パンチラインが登場
const punchSpring = spring({ frame: Math.max(0, frame - 78), fps, ... });
```

用途: 操作フロー説明、Before/After、機能紹介 → 一言キャッチコピー

---

## 専用BGM生成（fal.ai Stable Audio）

汎用BGMではなくプロジェクト固有のBGMを生成する。

```python
import fal_client
result = fal_client.subscribe("fal-ai/stable-audio", arguments={
    "prompt": "cinematic electronic, fintech technology, 118bpm, ...",
    "seconds_total": 35,
    "steps": 200,
})
# 出力は WAV → ffmpeg で MP3 変換
# ffmpeg -i output.wav -b:a 192k bgm_project.mp3
```

**プロンプト例:**
- フィンテック: `"cinematic electronic, fintech, professional, 118bpm, building tension"`
- 教育/研修: `"uplifting corporate, inspirational, 110bpm, warm piano"`
- SaaS: `"modern tech, minimalist electronic, 120bpm, clean"`
- ドラマティック: `"epic orchestral, cinematic tension, 100bpm, rising strings"`

BGM音量: `volume={0.15〜0.20}`（ナレーションの邪魔にならない程度）

---

## CrossFade トランジション戦略

| トランジション | 秒数 | 用途 |
|--------------|------|------|
| 標準 | 0.3s | 通常のシーン切替 |
| ロング | 0.8s | 問題→解決、暗→明など劇的な転換 |
| なし | 0s | Hook 冒頭（即座にインパクト） |

```tsx
const transDur = Math.round(0.3 * fps);
const longTransDur = Math.round(0.8 * fps);
// Problem→Solution 間のみ longTransDur を適用
{i === 2 ? longTransDur : transDur}
```
