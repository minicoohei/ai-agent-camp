---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "約35分"
prerequisites: ["start-15-5"]
level: "advanced"
tags: ["video", "slides", "narration", "tts"]
nonInteractiveMode: deferred
---
# Lesson 15-8: Slide Narration Video

## このセッションでやること

**Lesson 15-8: スライド解説動画** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | HTML教材やスライド画像から、プレゼンターが解説する動画を自動生成する |
| 所要時間 | 約35分 |
| 使うツール | slide_narration_pipeline (Gemini + ElevenLabs + Fabric/Kling + FFmpeg) |
| 前提条件 | FAL_KEY、GEMINI_API_KEY、ELEVEN_API_KEY 設定済み |
| コストガイド | [動画AIコスト戦略ガイド](https://ai-agent.camp/ja/course/module-15) を先に確認推奨 |
| 教材ページ | [Module 15: 動画生成](https://ai-agent.camp/ja/course/module-15) を並行参照 |

**コスト目安**: 5セグメント × Fabric 720p で約 **$12/本**、台本のみなら **$0.03**

**このセッションの流れ:**
1. 環境確認 & 素材準備
2. 台本の自動生成と確認
3. プレゼンター動画生成
4. スライド + プレゼンター合成
5. BGM追加（オプション）
6. 完成動画の確認

セッション終了時には、スライド解説動画が `output/ugc/slide_narration/` に保存されています。

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
      {"id": "cost_guide", "label": "先にコストガイドを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## Step 1: 環境確認 & 素材準備

**AskQuestionの設定例:**
```json
{
  "title": "Step 1: 素材の選択",
  "questions": [{
    "id": "source_choice",
    "prompt": "どの素材からスライド動画を作りますか？",
    "options": [
      {"id": "html", "label": "HTML教材から（このコースの教材を使う）"},
      {"id": "slides", "label": "スライド画像から（PNG/JPGフォルダ指定）"},
      {"id": "script_only", "label": "まず台本だけ生成して確認したい"}
    ]
  }]
}
```

**HTML教材から生成する場合:**
```bash
cd ~/ai-agent-camp
# 例: Module 1 のバナー生成教材を解説動画にする
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/ja/course/module-1 \
  --engine fabric --resolution 720p
```

**スライド画像から生成する場合:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --slides ./my_slides/ \
  --topic "AIエージェント入門" \
  --engine fabric
```

**台本のみ生成:**
```bash
cd ~/ai-agent-camp
python -m ugc.slide_narration_pipeline \
  --html https://ai-agent.camp/ja/course/module-1 \
  --script-only
```

---

## Step 2: 台本の確認・調整

**AskQuestionの設定例:**
```json
{
  "title": "Step 2: 台本の確認",
  "questions": [{
    "id": "step_action",
    "prompt": "生成された台本を確認しますか？",
    "options": [
      {"id": "check", "label": "台本を確認して必要なら修正"},
      {"id": "change_style", "label": "別のスタイルで再生成"},
      {"id": "skip", "label": "そのまま進める"}
    ]
  }]
}
```

**台本スタイル:**
- `friendly` - 親しみやすい話し言葉（デフォルト）
- `formal` - フォーマルなプレゼン風
- `casual` - カジュアルな雑談風

**確認ポイント:**
- 各セグメントの長さは適切か（30-60秒/セグメント推奨）
- 話し言葉として自然か
- 専門用語に説明が入っているか

---

## Step 3: プレゼンター動画の生成

**AskQuestionの設定例:**
```json
{
  "title": "Step 3: エンジン選択",
  "questions": [{
    "id": "engine_choice",
    "prompt": "プレゼンター動画のエンジンを選んでください",
    "options": [
      {"id": "fabric", "label": "Fabric 1.0（リップシンク付き $2.50/30秒）"},
      {"id": "kling", "label": "Kling 2.6 Pro（自然な動き $2.80/30秒）"},
      {"id": "skip_presenter", "label": "プレゼンターなし（スライドのみ）"}
    ]
  }]
}
```

**パイプラインが実行するステップ:**
1. アバター画像生成（Gemini Image）
2. セグメントごとにTTS音声生成（ElevenLabs）
3. セグメントごとにプレゼンター動画生成（選択したエンジン）
4. スライド画像からKen Burns背景動画を生成
5. プレゼンターを右下にオーバーレイ合成

---

## Step 4: 合成結果の確認

**AskQuestionの設定例:**
```json
{
  "title": "Step 4: 合成結果",
  "questions": [{
    "id": "step_action",
    "prompt": "合成結果を確認しますか？",
    "options": [
      {"id": "check", "label": "動画を確認する"},
      {"id": "change_position", "label": "プレゼンターの位置を変更"},
      {"id": "skip", "label": "次に進む"}
    ]
  }]
}
```

**プレゼンター位置オプション:**
- `right` - 右下（デフォルト）
- `left` - 左下
- `bottom` - 下部中央

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
      {"id": "add_bgm", "label": "BGMを追加（ファイル指定、音量12%推奨）"},
      {"id": "no_bgm", "label": "BGMなしで完成"},
      {"id": "generate", "label": "Lesson 15-7（MV）でBGM生成を学ぶ"}
    ]
  }]
}
```

---

## Step 6: 完成動画の確認

**実行内容:**
```text
output/ugc/slide_narration/<timestamp>/ 内の summary.json を確認（タイムスタンプ付きサブディレクトリに出力されます）。

確認項目:
- 最終動画のパス
- セグメント数
- 使用エンジン
- 生成コスト

コスト最適化のヒント:
- 480pにするとFabricコストは半額
- --script-only で台本だけ先に確認（$0.03）
- プレゼンターなしならスライドKen Burns + TTS音声のみ（$0.05）
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
      {"id": "trouble_1", "label": "HTML解析でセクションが取れない"},
      {"id": "trouble_2", "label": "TTS音声が不自然"},
      {"id": "trouble_3", "label": "プレゼンター動画がタイムアウト"},
      {"id": "trouble_4", "label": "オーバーレイ合成がずれる"}
    ]
  }]
}
```

### トラブル1: 「HTML解析でセクションが取れない」
**原因**: HTMLの構造が想定と異なる
**解決**: --slides オプションでスライド画像を直接指定

### トラブル2: 「TTS音声が不自然」
**原因**: 台本のテキストが読み上げに適していない
**解決**: --script-only で台本を先に生成→手動修正→再実行

### トラブル3: 「プレゼンター動画がタイムアウト」
**原因**: fal.aiの処理遅延
**解決**: エンジンを変更（fabric → kling）、セグメントを短くする

### トラブル4: 「オーバーレイ合成がずれる」
**原因**: プレゼンターとスライドの長さ不一致
**解決**: FFmpegの -shortest オプションで自動調整（デフォルト有効）

---

## QA: /narration-qa でナレーション品質チェック

TTS 生成後、必ず発音品質を検証します。

入力内容:
```text
/narration-qa

生成したナレーション音声の品質をチェックしてください。

■ チェック対象: 生成された音声ファイル（MP3/WAV）
■ 重点項目:
- 漢字の誤読がないか（税理士→ぜいりし 等）
- 数字の読み上げが正確か
- テンポが自然か（atempo 1.35x 以内か）
- BGM とのバランス（ナレーション 1.0-1.2 / BGM 0.18-0.25）
```

/narration-qa は Gemini Flash で全クリップを書き起こし、期待テキストと自動比較します。
不一致があれば再生成を提案します（最大3回まで）。

---

## QA: /motion-review で合成動画チェック

ナレーション合格後、動画全体の品質もチェック:

入力内容:
```text
/motion-review

スライド解説動画の合成品質をチェックしてください。
■ 特に: プレゼンター合成の位置・サイズ、スライド遷移のタイミング
```

---

## チェックポイント
- [ ] APIキーが正しく設定されている
- [ ] HTML解析またはスライド画像の準備ができた
- [ ] 台本が自然な話し言葉で生成された
- [ ] プレゼンター動画が生成できた
- [ ] スライドとプレゼンターが合成された
- [ ] 最終動画を確認できた

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
      {"id": "next_auto", "label": "次のセクション（/start-15-9 プロダクト紹介動画）"},
      {"id": "retry", "label": "別の教材で再生成"},
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

