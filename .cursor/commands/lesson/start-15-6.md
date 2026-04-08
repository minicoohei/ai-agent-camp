---
description: "When the user says /start-15-6 — Module 15 Lesson 15-6: AIでミュージックビデオを作成する（Suno + ビート同期 + シーン動画化）"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約45分"
prerequisites: ["start-15-2"]
level: "advanced"
tags: ["video", "music-video", "suno", "beat-sync"]
---

# Lesson 15-6: Music Video

## このセッションでやること

**Lesson 15-6: ミュージックビデオ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | AI楽曲を生成し、ビートに同期したシーン動画を組み合わせてMVを作る |
| 所要時間 | 約45分 |
| 使うツール | mv_pipeline (Suno/fal.ai + librosa + Gemini + Kling + FFmpeg) |
| 前提条件 | FAL_KEY、GEMINI_API_KEY 設定済み。pip install librosa 推奨 |
| コストガイド | [動画AIコスト戦略ガイド](https://ai-agent.camp/ja/course/module-15) を先に確認推奨 |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**コスト目安**:
- フルI2V（Kling 8本）+ AI楽曲: 約 **$6-12**
- コスト最適化（A-roll 3本 + B-roll 5本）: 約 **$3-5**
- 既存楽曲 + Ken Burnsのみ: 約 **$0.10**（画像生成のみ）

**このセッションの流れ:**
1. 環境確認 & 楽曲の準備
2. AI楽曲生成 or 既存楽曲の読み込み
3. ビート解析 & シーンタイムライン
4. シーン画像 + 動画クリップ生成
5. ビート同期結合 & 音楽ミックス
6. 完成MVの確認

セッション終了時には、ミュージックビデオが `output/ugc/mv/` に保存されています。

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」と入力すると再開します。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "install_librosa", "label": "librosaをインストールしたい"},
      {"id": "cost_guide", "label": "先にコストガイドを見たい"}
    ]
  }]
}
```

(install_librosa → `pip install librosa` を実行)

---

## Step 1: 環境確認 & 楽曲の準備

**AskQuestionの設定例:**
```json
{
  "title": "Step 1: 楽曲の準備",
  "questions": [{
    "id": "music_source",
    "prompt": "楽曲をどう準備しますか？",
    "options": [
      {"id": "generate", "label": "AIで楽曲を生成する（fal.ai Suno）"},
      {"id": "existing", "label": "手持ちの音楽ファイルを使う"},
      {"id": "explain", "label": "AI楽曲生成の仕組みを説明して"}
    ]
  }]
}
```

**環境確認:**
```text
以下を確認してください：
1. APIキー
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
2. FFmpeg
   - ffmpeg -version
3. librosa（ビート解析用、オプション）
   - python -c "import librosa; print(librosa.__version__)"
   - インストール: pip install librosa
```

---

## Step 2: パイプラインの実行

**AI楽曲生成 + MV作成:**
```bash
cd ~/ai-agent-camp
python -m ugc.mv_pipeline \
  --prompt "明るいポップソング、前向きな歌詞、テンポ120BPM" \
  --style anime \
  --engine kling \
  --num-scenes 8 \
  --cost-optimize --aroll-count 3
```

**既存楽曲 + MV作成:**
```bash
cd ~/ai-agent-camp
python -m ugc.mv_pipeline \
  --music ./my_song.mp3 \
  --style cinematic_live \
  --engine kling \
  --num-scenes 8
```

**パイプラインが自動で実行する7ステップ:**
1. **楽曲準備** → AI生成 or 既存ファイルコピー
2. **ビート解析** (librosa) → `beat_analysis.json`（テンポ、ビート位置、セクション）
3. **シーンプロンプト生成** (Gemini) → `scenes.json`（歌詞・雰囲気→映像プロンプト変換）
4. **フレーム画像生成** (Gemini Image) → 8枚のシーン画像
5. **動画クリップ生成** (Kling I2V + Ken Burns) → 8本のクリップ
6. **ビート同期結合** (FFmpeg xfade) → `joined.mp4`
7. **音楽ミックス** (FFmpeg) → `final.mp4`

---

## Step 3: ビート解析の確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 3: ビート解析結果",
  "questions": [{
    "id": "step_action",
    "prompt": "ビート解析結果を確認しますか？",
    "options": [
      {"id": "check", "label": "解析結果を確認する"},
      {"id": "explain_beat", "label": "ビート同期の仕組みを解説"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**確認ポイント:**
- テンポ（BPM）が楽曲に合っているか
- セクション（verse/chorus）が正しく検出されているか
- 各シーンの長さがビートに合っているか

**ビート同期の仕組み:**
```text
楽曲のビート位置を検出
    ↓
ダウンビート（強拍）でシーン分割
    ↓
chorus部分 → A-roll（I2Vでダイナミックに）
verse部分 → B-roll（Ken Burnsで落ち着いた映像）
    ↓
ビート位置でカット切替
```

---

## Step 4: シーン画像と動画クリップの確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 4: クリップの確認",
  "questions": [{
    "id": "step_action",
    "prompt": "確認方法を選んでください",
    "options": [
      {"id": "check_frames", "label": "フレーム画像を確認"},
      {"id": "check_clips", "label": "動画クリップを確認"},
      {"id": "regenerate", "label": "特定シーンを再生成"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**利用可能なビジュアルスタイル:**
- `anime` - アニメ調
- `cinematic_live` - 実写映画風
- `abstract` - 抽象的・アート風
- `watercolor` - 水彩画風
- `pixel_art` - ドット絵風
- `vibrant_ugc` - 鮮やかなSNS風

**シーンプロンプトの工夫:**
```text
verse（Aメロ/Bメロ）→ narrative（物語的）or landscape（風景）
chorus（サビ）→ performance（パフォーマンス）or abstract（抽象的）
bridge（ブリッジ）→ abstract（抽象的）or landscape（風景）
```

---

## Step 5: 完成MVの確認 & コスト振り返り

**実行内容:**
```text
output/ugc/mv/ 内の summary.json を確認。

確認項目:
- 楽曲パス & 長さ
- ビジュアルスタイル
- シーン数（A-roll / B-roll 内訳）
- 生成コスト

コスト最適化テクニック:
- chorus部分だけA-roll（I2V）にしてインパクトを集中
- verse部分はKen Burns B-rollで落ち着いた映像に
- これにより A-roll 3本 + B-roll 5本 = $2.10 + $0 = $2.10（映像のみ）
- 詳細: https://ai-agent.camp/ja/course/module-15
```

---

## よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "AI楽曲生成が失敗する"},
      {"id": "trouble_2", "label": "librosaのインストールでエラー"},
      {"id": "trouble_3", "label": "ビートとシーン切替がずれる"},
      {"id": "trouble_4", "label": "映像と音楽の雰囲気が合わない"}
    ]
  }]
}
```

### トラブル1: 「AI楽曲生成が失敗する」
**原因**: fal.aiの音楽生成エンドポイントの変更
**解決**: --music オプションで手持ちの音楽ファイルを使う

### トラブル2: 「librosaのインストールでエラー」
**原因**: 依存ライブラリの問題
**解決**:
```bash
pip install librosa soundfile
# それでもダメなら:
pip install librosa --no-deps
pip install soundfile numba
```
librosaなしでも均等分割で動作します。

### トラブル3: 「ビートとシーン切替がずれる」
**原因**: ビート検出の精度
**解決**: `--num-scenes` を減らす（8→6）とビートに合いやすくなる

### トラブル4: 「映像と音楽の雰囲気が合わない」
**原因**: スタイル選択のミスマッチ
**解決**: 楽曲のジャンルに合わせてスタイルを変更
- ポップ → `anime` or `vibrant_ugc`
- ロック → `cinematic_live`
- エレクトロニック → `abstract`
- クラシック → `watercolor`

---

## チェックポイント
- [ ] APIキーが正しく設定されている
- [ ] 楽曲を準備できた（AI生成 or 手持ち）
- [ ] ビート解析が実行できた
- [ ] シーン画像が生成された
- [ ] A-roll / B-roll の動画クリップが生成された
- [ ] ビート同期でMVが完成した
- [ ] 音楽とのミックスが成功した

---

## 次のステップ

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "次のモジュール（/start-16-1 メール/LINE自動化）"},
      {"id": "retry", "label": "別の楽曲・スタイルで再生成"},
      {"id": "review_all", "label": "Module 15 の振り返り"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```
