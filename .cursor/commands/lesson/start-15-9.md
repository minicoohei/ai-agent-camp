---
description: "When the user says /start-15-9 — Module 15 Lesson 15-9: プロダクト紹介動画を作成する（グリーンスクリーンアバター + スクショ合成）"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約30分"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "product-demo", "avatar", "kling"]
---

# 15-9: Product Demo Video

## このセッションでやること

**Lesson 15-9: プロダクト紹介動画** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | グリーンスクリーンのアバターがスマホ画面でアプリを紹介する動画を生成する |
| 所要時間 | 約30分 |
| 使うツール | product_demo_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| 前提条件 | FAL_KEY、GEMINI_API_KEY、ELEVEN_API_KEY 設定済み |
| コストガイド | [動画AIコスト戦略ガイド](https://ai-agent.camp/ja/course/module-15) を先に確認推奨 |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**コスト目安**: Fabricエンジン 480p で約 **$2.50/本**、Kling で約 **$2.80/本**

**このセッションの流れ:**
1. 環境確認 & スクリーンショット準備
2. エンジン選択 & パイプライン実行
3. 台本の確認・調整
4. グリーンスクリーン合成の確認
5. BGM追加（オプション）
6. 完成動画の確認 & コスト振り返り

セッション終了時には、プロダクト紹介動画が `output/ugc/product_demo/` に保存されています。

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
(check_prereq → FAL_KEY / GEMINI_API_KEY / ELEVEN_API_KEY の存在確認を実行)
(cost_guide → https://ai-agent.camp/ja/course/module-15 のパスを案内)
(different_lesson → モジュール一覧を表示)

---

## Step 1: 環境確認 & スクリーンショット準備

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
   - echo $ELEVEN_API_KEY (または $ELEVENLABS_API_KEY)
2. FFmpegがインストールされているか
   - ffmpeg -version
3. 紹介したいアプリ/サービスのスクリーンショットを用意
   - スマホ画面サイズ（縦長）推奨
   - なければサンプルを作成します
```

**期待される結果**: APIキーが確認でき、スクリーンショットの準備ができた状態。

---

## Step 2: パイプラインの全自動実行

**AskQuestionの設定例:**
```json
{
  "title": "Step 2: 動画生成エンジンの選択",
  "questions": [{
    "id": "engine_choice",
    "prompt": "どのエンジンを使いますか？",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0（コスパ良好 $2.50、リップシンク付き）"},
      {"id": "kling", "label": "Kling 2.6 Pro（自然な動き $2.80、UGCスタイル）"},
      {"id": "veo", "label": "Veo 3.1（最高品質 $15+、コスト注意）"},
      {"id": "longcat", "label": "LongCat（全身アニメーション $3.00）"}
    ]
  }]
}
```

**選択後の実行:**

```bash
cd ~/ai-agent-camp
python -m ugc.product_demo_pipeline \
  --product "（ユーザーが指定した製品名）" \
  --screenshot ./（ユーザーのスクリーンショット）\
  --engine fabric \
  --platform tiktok \
  --resolution 480p
```

**パイプラインが自動で実行する6ステップ:**
1. **台本生成** (Gemini Flash) → `script.txt`
2. **アバター画像生成** (Gemini Image) → `avatar.png`（グリーンスクリーン付きスマホ持ち人物）
3. **TTS音声生成** (ElevenLabs) → `speech.mp3`
4. **動画生成** (Fabric/Kling/Veo) → `raw_video.mp4`
5. **グリーンスクリーン合成** (FFmpeg) → `composited.mp4`（スクショがスマホ画面に合成）
6. **最終出力** → `final.mp4`

**期待される結果**: `output/ugc/product_demo/` に動画が生成される。

---

## Step 3: 生成された台本の確認・調整

**AskQuestionの設定例:**
```json
{
  "title": "Step 3: 台本の確認",
  "questions": [{
    "id": "step_action",
    "prompt": "生成された台本を確認しますか？",
    "options": [
      {"id": "check", "label": "台本を確認して必要なら修正"},
      {"id": "regenerate", "label": "別の台本を再生成"},
      {"id": "skip", "label": "そのまま進める"}
    ]
  }]
}
```

**実行内容:**
```text
output/ugc/product_demo/ 内の script.txt を読んで内容を確認してください。

確認ポイント:
- フック（最初の2秒）は注目を引くか？
- 製品の魅力が伝わるか？
- 話し言葉として自然か？
- 長すぎないか（30秒 = 約90文字目安）？
```

---

## Step 4: グリーンスクリーン合成の確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 4: 合成結果の確認",
  "questions": [{
    "id": "step_action",
    "prompt": "合成結果を確認しますか？",
    "options": [
      {"id": "check", "label": "動画を確認する"},
      {"id": "retry_opencv", "label": "OpenCVバックエンドで再合成"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**確認ポイント:**
- スクリーンショットがスマホ画面に正しく合成されているか
- 緑色の残りがないか
- アバターとスクショのバランスは良いか

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
      {"id": "generate", "label": "Suno AIでBGMを生成（fal.ai, 後のレッスンで学習）"}
    ]
  }]
}
```

**BGM追加の実行:**
```python
from tools.ugc.audio_post import mix_bgm
mix_bgm(
    video_path="output/ugc/product_demo/.../composited.mp4",
    bgm_path="./my_bgm.mp3",
    output_path="output/ugc/product_demo/.../final_with_bgm.mp4",
    bgm_volume=0.15,
)
```

---

## Step 6: 完成動画の確認 & コスト振り返り

**実行内容:**
```text
output/ugc/product_demo/ 内の summary.json を読んで結果を確認。

確認項目:
- 最終動画のパス
- 使用エンジン
- 生成コスト（$）
- 各ステップの成否

コスト最適化のヒント:
- 480pにすればFabricのコストは半額
- アバター画像を使い回せば毎回 $0.02 節約
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
      {"id": "trouble_2", "label": "グリーンスクリーン合成が失敗"},
      {"id": "trouble_3", "label": "動画生成がタイムアウト"},
      {"id": "trouble_4", "label": "音声と口が合わない"}
    ]
  }]
}
```

### トラブル1: 「APIキーエラー」
**原因**: 環境変数が未設定
**解決**:
```bash
cat .env | grep -E "FAL_KEY|GEMINI|ELEVEN"    # Mac/Linux
# Windows (cmd): findstr "FAL_KEY GEMINI ELEVEN" .env
# Windows (PowerShell): Select-String -Path .env -Pattern "FAL_KEY|GEMINI|ELEVEN"
```

### トラブル2: 「グリーンスクリーン合成が失敗」
**原因**: 緑色の検出が難しい画像
**解決**: OpenCVバックエンドを試す
```python
from ugc import composite_video
composite_video(video, screenshot, output, backend="opencv")
```

### トラブル3: 「動画生成がタイムアウト」
**原因**: fal.aiの処理が遅い
**解決**: Fabricに切り替えるか、リトライ

### トラブル4: 「音声と口が合わない」
**解決**: MuseTalkでリップシンク補正
```python
from ugc.audio_post import apply_musetalk
apply_musetalk(video, audio, output)
```

---

## QA: /narration-qa + /motion-review で品質検証

グリーンスクリーン合成後、音声と映像の両方を検証します。

入力内容:
```
/narration-qa

プロダクト紹介動画のナレーション品質をチェックしてください。
■ 対象: 生成された音声ファイル
```

```
/motion-review

プロダクト紹介動画の合成品質をチェックしてください。
■ 重点項目:
- グリーンスクリーンのキーイング品質（緑のフリンジ残り）
- スクリーンショット合成の位置とサイズ
- アバターの口パクと音声の同期
```

---

## チェックポイント
- [ ] APIキーが正しく設定されている
- [ ] スクリーンショットを用意できた
- [ ] パイプラインが正常に完了した
- [ ] グリーンスクリーン合成が成功した
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
      {"id": "next_auto", "label": "次のモジュール（/start-16-1）"},
      {"id": "retry", "label": "別のエンジンで同じ動画を再生成"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```
