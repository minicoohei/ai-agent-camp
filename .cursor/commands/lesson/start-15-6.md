---
description: "When the user says /start-15-6 — Module 15 Lesson 15-6: 絵コンテからアニメ動画を生成する（Gemini画像 + Kling/Veo I2V + FFmpeg結合）"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約40分"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "storyboard", "anime", "kling"]
---

# 15-6: Storyboard Anime Video

## このセッションでやること

**Lesson 15-6: 絵コンテアニメ動画** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | テキストシナリオから絵コンテ画像を生成し、AI動画エンジンで動画化して1本の作品にする |
| 所要時間 | 約40分 |
| 使うツール | storyboard_anime_pipeline (Gemini + Kling/Veo + FFmpeg) |
| 前提条件 | FAL_KEY、GEMINI_API_KEY 設定済み |
| コストガイド | [動画AIコスト戦略ガイド](https://ai-agent.camp/ja/course/module-15) を先に確認推奨 |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**コスト目安**:
- 全フレームI2V（Kling 8本）: 約 **$5.60**
- コスト最適化モード（A-roll 4本 + B-roll 4本）: 約 **$2.80**
- Ken Burns B-rollのみ（テスト用）: **$0**（ローカル処理）

**このセッションの流れ:**
1. 環境確認 & シナリオ準備
2. シーン分解 & フレーム画像生成
3. A-roll / B-roll 分類と動画化
4. トランジション付き結合
5. BGM追加（オプション）
6. 完成動画の確認 & コスト振り返り

セッション終了時には、絵コンテアニメ動画が `output/ugc/storyboard_anime/` に保存されています。

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」と入力すると再開します。

---

## 準備チェック

まずは準備が整っているか確認しましょう。

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
      {"id": "cost_guide", "label": "先にコストガイドを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → FAL_KEY / GEMINI_API_KEY の存在確認を実行)
(cost_guide → https://ai-agent.camp/ja/course/module-15 のパスを案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: 環境確認 & シナリオ準備

**AskQuestionの設定例:**
```json
{
  "title": "Step 1: 環境確認",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**実行内容:**
```text
以下を確認してください：
1. 必要なAPIキーが環境変数に設定されているか
   - echo $FAL_KEY
   - echo $GEMINI_API_KEY
2. FFmpegがインストールされているか
   - ffmpeg -version
3. シナリオ（ストーリー）を考えておく
   - 例: 「少女が魔法の森で不思議な生き物と出会う冒険物語」
   - 例: 「カフェの一日を描いたスライスオブライフ」
   - 例: 「宇宙飛行士が未知の惑星を探索する物語」
```

**期待される結果**: APIキーが確認でき、シナリオのアイデアがある状態。

---

## Step 2: パイプラインの全自動実行

**AskQuestionの設定例:**
```json
{
  "title": "Step 2: 実行モードの選択",
  "questions": [{
    "id": "mode_choice",
    "prompt": "どのモードで実行しますか？",
    "options": [
      {"id": "cost_optimize", "label": "コスト最適化モード（A-roll 4本 + B-roll Ken Burns, 約$2.80）"},
      {"id": "full_i2v", "label": "フルI2Vモード（全シーン動画化, 約$5.60）"},
      {"id": "broll_only", "label": "Ken Burnsのみ（テスト用, $0）"},
      {"id": "explain", "label": "A-roll / B-rollの違いを説明して"}
    ]
  }]
}
```

**コスト最適化モードの実行:**

```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "（ユーザーが指定したシナリオ）" \
  --style anime \
  --engine kling \
  --num-scenes 8 \
  --cost-optimize \
  --aroll-count 4
```

**フルI2Vモードの実行:**

```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "（ユーザーが指定したシナリオ）" \
  --style anime \
  --engine kling \
  --num-scenes 8
```

**パイプラインが自動で実行する5ステップ:**
1. **シーン分解** (Gemini Flash) → `scenes.json`（シナリオを8シーンに分割）
2. **フレーム画像生成** (Gemini Image) → `frames/frame_000.png` ~ `frame_007.png`
3. **動画クリップ生成** (Kling I2V or Ken Burns) → `clips/clip_000.mp4` ~
4. **クロスフェード結合** (FFmpeg xfade) → `joined.mp4`
5. **最終出力** → `final.mp4`

**期待される結果**: `output/ugc/storyboard_anime/` にフレーム画像と動画が生成される。

---

## Step 3: フレーム画像の確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 3: フレーム画像の確認",
  "questions": [{
    "id": "step_action",
    "prompt": "生成されたフレーム画像を確認しますか？",
    "options": [
      {"id": "check", "label": "フレーム画像を確認する"},
      {"id": "regenerate", "label": "特定のフレームを再生成"},
      {"id": "change_style", "label": "別のスタイルで再生成"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**利用可能なスタイル:**
- `anime` - アニメ調（デフォルト）
- `modern_clean` - モダンクリーン
- `vibrant_ugc` - 鮮やかなUGC風
- `animal_crossing` - どうぶつの森風
- `watercolor` - 水彩画風
- `pixel_art` - ドット絵風
- `cinematic_live` - 実写映画風

---

## Step 4: A-roll / B-roll と動画クリップの確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 4: 動画クリップの確認",
  "questions": [{
    "id": "step_action",
    "prompt": "動画クリップの確認方法を選んでください",
    "options": [
      {"id": "check_all", "label": "全クリップを確認"},
      {"id": "check_aroll", "label": "A-rollクリップだけ確認"},
      {"id": "explain_aroll", "label": "A-roll/B-rollの仕組みを解説"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**A-roll / B-roll の解説:**

```text
【A-roll（メイン映像）】
- I2V（Image-to-Video）エンジンで動画化
- キャラクターの動き、重要なアクションシーン
- コスト: Kling $0.70/本、Veo $8/本

【B-roll（補助映像）】
- Ken Burns効果（FFmpeg zoompan）で擬似動画化
- 風景、背景、トランジション用
- コスト: $0（ローカル処理）

【効果の種類（Ken Burns）】
zoom_in, zoom_out, pan_left, pan_right, slow_zoom, pan_down, pan_up
```

**確認ポイント:**
- A-rollクリップ: 動きが自然か
- B-rollクリップ: Ken Burns効果が適切か
- scenes.json の `is_key_scene` が正しく判定されているか

---

## Step 5: BGM追加（オプション）

**AskQuestionの設定例:**
```json
{
  "title": "Step 5: BGM追加",
  "questions": [{
    "id": "bgm_choice",
    "prompt": "BGMを追加しますか？",
    "options": [
      {"id": "add_bgm", "label": "BGMを追加する（ファイルを指定）"},
      {"id": "no_bgm", "label": "BGMなしで完成"},
      {"id": "generate", "label": "Suno AIでBGMを生成（後のレッスンで学習）"}
    ]
  }]
}
```

**BGM追加の実行:**
```bash
cd ~/ai-agent-camp
python -m ugc.storyboard_anime_pipeline \
  --scenario "（同じシナリオ）" \
  --style anime --engine kling \
  --cost-optimize --aroll-count 4 \
  --bgm ./my_bgm.mp3 --bgm-volume 0.20
```

---

## Step 6: 完成動画の確認 & コスト振り返り

**実行内容:**
```text
output/ugc/storyboard_anime/ 内の summary.json を読んで結果を確認。

確認項目:
- 最終動画のパス
- シーン数（A-roll / B-roll の内訳）
- 生成コスト（$）
- 各ステップの成否

コスト最適化のヒント:
- A-rollを4本に絞れば通常の1/4のコスト
- Ken Burns効果は$0なのでB-rollは気軽に増やせる
- 大量生成する場合はGenSpark等の定額サービスも検討
  → 詳細: https://ai-agent.camp/ja/course/module-15
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
      {"id": "trouble_1", "label": "APIキーエラー"},
      {"id": "trouble_2", "label": "フレーム画像のスタイルが統一されない"},
      {"id": "trouble_3", "label": "I2V動画化がタイムアウト"},
      {"id": "trouble_4", "label": "クロスフェード結合が失敗"}
    ]
  }]
}
```

### トラブル1: 「APIキーエラー」
**原因**: 環境変数が未設定
**解決**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI"
```

### トラブル2: 「フレーム画像のスタイルが統一されない」
**原因**: Gemini画像生成のバリエーション
**解決**: `--character` オプションでキャラクター説明を固定
```bash
python -m ugc.storyboard_anime_pipeline \
  --scenario "..." --style anime --engine kling \
  --character "茶色い髪のショートカットの少女、白いワンピース、大きな瞳"
```

### トラブル3: 「I2V動画化がタイムアウト」
**原因**: fal.aiの処理が遅い
**解決**: `--cost-optimize` でI2V本数を減らすか、Kling → Veoに切替

### トラブル4: 「クロスフェード結合が失敗」
**原因**: 動画のフォーマットが不一致
**解決**: パイプライン内で自動的にsimple concat にフォールバックします

---

## QA: /motion-review + /remotion-trace で品質検証

I2V生成後、品質レビューと参考動画との比較を行います。

入力内容:
```text
/motion-review

絵コンテアニメ動画の品質をチェックしてください。

■ チェック対象: 生成された動画ファイル
■ 重点項目:
- シーン間のクロスフェード遷移が自然か
- Ken Burns B-roll とI2V A-roll のテンポバランス
- テロップの表示タイミングと読み取り時間
```

さらに品質を上げたい場合:
```text
/remotion-trace

参考動画のモーションパターンをトレースして、品質を向上させたい。
現在の出力と比較してください。
```

---

## チェックポイント
- [ ] APIキーが正しく設定されている
- [ ] シナリオからシーン分解ができた
- [ ] フレーム画像が生成された
- [ ] A-roll / B-rollの違いを理解した
- [ ] 最終動画を確認できた
- [ ] コスト戦略ガイドの内容を理解した

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
      {"id": "next_auto", "label": "次のセクション（/start-15-7 ミュージックビデオ）"},
      {"id": "retry", "label": "別のシナリオ・スタイルで再生成"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```
