---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約20分"
prerequisites: ["start-15-1"]
level: "intermediate"
tags: ["video", "ai-engine", "fal"]
nonInteractiveMode: deferred
---
# 15-5: 動画AIエンジン概要

## このセッションでやること

**Lesson 15-5: 動画AIエンジン概要** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 最新の動画AIエンジンを理解し、fal.aiの基本的な使い方を習得する |
| 所要時間 | 約20分 |
| 使うツール | fal.ai (FAL_KEY) |
| 前提条件 | FAL_KEY 設定済み、Python 3.10 以上推奨 |
| コストガイド | ※ コストガイドは準備中です |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**重要**: このレッスンでは全エンジンを実際に叩く比較は行いません（高コストのため）。
各エンジンの特徴・価格を理解し、fal.aiの基本パターンだけハンズオンします。
実際のAPI呼び出しは 15-6 以降のプロジェクトレッスンで必要な分だけ行います。

**前提条件: FAL_KEY の設定**

fal.ai のAPIを使用するため、事前にAPIキーの設定が必要です。
未設定の場合は `/setup-fal` を実行してセットアップしてください。

> **注意**: fal-client は Python 3.10 以上を推奨します。`python3 --version` で確認してください。

**このセッションの流れ:**
1. 動画AIエンジンの全体像
2. API従量課金 vs 定額サービスの使い分け
3. fal.ai の基本的な使い方（ハンズオン）
4. エンジン選択の判断基準

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
      {"id": "check_prereq", "label": "FAL_KEYの設定を確認したい"},
      {"id": "cost_guide", "label": "先にコストガイドを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## Step 1: 動画AIエンジンの全体像

**AskQuestionの設定例:**
```json
{
  "title": "Step 1: エンジン概要",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "一緒に調べながら進める"},
      {"id": "review", "label": "まとめだけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**解説内容:**

2025-2026年現在の主要な動画AIエンジンを紹介します。

### Image-to-Video（画像→動画）エンジン

| エンジン | Provider | 価格 | 特徴 |
|---------|----------|------|------|
| **Kling 2.6 Pro** | fal.ai | $0.07/s | 自然な動き、UGCスタイル、グリーンスクリーン対応 |
| **Veo 3.1** | fal.ai | $0.50-1.00/s | 最高品質、ネイティブ音声、Text-to-Video対応 |
| **Runway Gen-3** | Runway | 定額$15-76/月 | 高品質、Web UIが使いやすい |
| **Pika 2.0** | Pika | 定額$8-58/月 | テキスト/画像から動画、効果が豊富 |
| **Minimax** | fal.ai | 要確認 | 長尺動画に強い |
| **LTX Video** | fal.ai | 低コスト | オープンソースベース |

### Lip-sync（リップシンク）エンジン

| エンジン | Provider | 価格 | 特徴 |
|---------|----------|------|------|
| **Fabric 1.0** | fal.ai | $0.08-0.15/s | 高精度リップシンク |
| **LongCat** | fal.ai | $0.10/s | 全身モーション + リップシンク |
| **HeyGen** | 直接API | $0.05/s | アバター内蔵、多言語 |
| **MuseTalk** | fal.ai | 要確認 | fal.ai経由のリップシンク |

### その他

| ツール | 種類 | 価格 | 用途 |
|--------|------|------|------|
| **Suno** | 音楽生成 | fal.ai経由 | AI作曲 |
| **Remotion** | コード動画 | $0（ローカル） | テンプレート動画、スライド |
| **FFmpeg** | 編集 | $0（ローカル） | トランジション、合成、Ken Burns |

### 定額サービス（大量生成向け）

| サービス | 月額 | 特徴 |
|---------|------|------|
| **GenSpark** | $19/月 | AI動画+画像+検索 |
| **Runway** | $15-76/月 | Gen-3 Alpha、高品質 |
| **Pika** | $8-58/月 | 手軽、エフェクト豊富 |
| **CapCut Pro** | $10/月 | 編集+テンプレート |

**ポイント**: APIは自動化に向いているが高コスト。定額サービスは手動だが量産に向いている。
詳しくはコスト戦略ガイド（準備中）を参照。

---

## Step 2: API vs 定額サービスの使い分け

**AskQuestionの設定例:**
```json
{
  "title": "Step 2: コスト戦略",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "一緒に考えながら進める"},
      {"id": "review", "label": "まとめだけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**解説内容:**

```text
判断フローチャート:

自動化が必要？
  YES → API（fal.ai）
    月10本以上？
      YES → 定額サービスも検討
      NO  → APIで十分（学習フェーズ）
  NO  → 定額サービス（手動操作OK）

B-rollで代替できるシーンがある？
  YES → A-roll(API) + B-roll(Ken Burns/Remotion) = コスト最適
  NO  → 全シーンI2V（コスト覚悟）
```

---

## Step 3: fal.ai の基本（ハンズオン）

**AskQuestionの設定例:**
```json
{
  "title": "Step 3: fal.ai ハンズオン",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "実際に実行する"},
      {"id": "review", "label": "コードだけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**実行内容:**

fal.aiクライアントの基本パターンを確認します。
実際のAPI呼び出しは最低限（テキスト生成程度）に留めます。

```python
# fal.ai の基本パターン
import fal_client

# 1. ファイルアップロード
url = fal_client.upload_file("image.png")

# 2. subscribe パターン（結果を待つ）
result = fal_client.subscribe(
    "fal-ai/kling-video/v2.6/pro/image-to-video",
    arguments={
        "image_url": url,
        "prompt": "A person talking naturally",
        "duration": "5",
        "aspect_ratio": "9:16",
    },
    with_logs=True,
    on_queue_update=lambda update: print(f"Status: {update}"),
)

# 3. 結果取得
video_url = result["video"]["url"]
```

```text
確認事項:
1. FAL_KEY が設定されているか
   echo $FAL_KEY
2. fal-client がインストールされているか
   uv pip show fal-client
3. 上記コードの構造を理解（subscribe + arguments + callback）
```

---

## Step 4: エンジン選択の判断基準

**まとめ:**

| ユースケース | 推奨エンジン | 理由 |
|-------------|-------------|------|
| プロダクト紹介（UGC風） | Fabric / Kling | リップシンク + コスパ |
| アニメ/ストーリー | Kling | I2V品質が良い |
| 最高品質デモ | Veo 3.1 | 品質最高（コスト注意） |
| スライド/テンプレート | Remotion | $0、カスタマイズ自由 |
| MV/音楽 | Suno + Kling | 音楽生成 + 映像生成 |
| 大量生成 | GenSpark/Runway | 定額で予算管理 |
| B-roll補助 | Ken Burns (FFmpeg) | $0、静止画から擬似動画 |

---

## チェックポイント
- [ ] 主要な動画AIエンジンの種類を理解した
- [ ] API従量課金と定額サービスの違いを理解した
- [ ] fal.ai の subscribe パターンを理解した
- [ ] コスト戦略ガイドを確認した
- [ ] 自分のユースケースに合ったエンジンが選べる

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
      {"id": "next_76", "label": "15-6: 絵コンテアニメ動画（/start-15-6）"},
      {"id": "next_77", "label": "15-7: ミュージックビデオ（/start-15-7）"},
      {"id": "next_78", "label": "15-8: スライド解説動画（/start-15-8）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

## 参考リンク（aiagent-course Module 15 スライドと共通）

テンプレートやインスピレーションを探すときに使う 5 つのリソース。

- [Dribbble (motion design portfolios)](https://dribbble.com/)
- [Envato Elements — video templates / logo animation](https://elements.envato.com/video-templates/logo+animation)
- [Placeit — minimalist motion-graphics intro maker](https://placeit.net/c/videos/stages/intro-maker-with-minimalist-motion-graphics-988)
- [YouTube — After Effects templates project channel](https://www.youtube.com/@paftereffectstemplatesproj6705)
- [YouTube — motion-graphics templates playlist](https://www.youtube.com/playlist?list=PLCWRuswMLN-huRtRNjplBjZGuIknrhckj)

