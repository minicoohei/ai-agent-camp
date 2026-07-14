---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "約30分"
prerequisites: ["start-29-1"]
level: "intermediate"
tags: ["slide", "generation", "ai"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-2: 議事録から本番生成・5問

## 📍 このセッションでやること

**Lesson 29-2: 議事録から本番生成・5問** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 議事録・構成メモから、5問の選択を使って編集可能な提案デッキを生成する |
| 所要時間 | 約30分 |
| 使うスキル | slide-forge, generate, AskUserQuestion |
| 前提条件 | Lesson 29-1 |
| 教材ページ | [Module 29: slide-forge](https://ai-agent.camp/ja/course/module-29?slideId=generate) を並行参照 |

**このセッションの流れ:**
1. 入力資料と秘密情報の扱いを確認
2. 5問を選ぶ
3. generate を実行
4. 4形式の成果物を確認

セッション終了時には、自分の議事録から PPTX / PDF / PNG / HTML の提案デッキを生成できています。

> **💡 ヒント**: 秘密情報や API キーをチャットに貼らないでください。`.env` の値は存在確認だけに留めます。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "議事録から本番生成を始める準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 29-1、`.env`、`config.yaml`、入力資料の確認を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 入力資料と秘密情報の扱いを確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 入力資料と秘密情報の扱いを確認",
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

**選択後の案内（例）**:
入力内容:
```
slide-forge で本番生成するための入力と設定を確認してください。

確認項目:
1. 議事録ファイル（.md / .txt / .json / .pdf）または直接テキスト
2. 構成案が別にある場合は --outline として扱う
3. .env に OPENAI_API_KEY と LLM_BACKEND が設定済みか確認する
4. config.yaml があるか確認する
5. 秘密情報や API キーの値はチャットにもログにも表示しない
6. 入力資料に無い固有名詞・数字・日付・費用・KPI を推測補完しない
```

**期待される結果**: 入力資料、設定、生成方針が明確になります。

---

## 🚀 Step 2: 5問を選ぶ

`config.yaml` の選択肢に沿って、デッキの型・シナリオ・トーン・目的・ターゲットを決めます。

AskUserQuestion（AskQuestion）で5問をまとめて選びます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 5問を選ぶ",
  "questions": [
    {
      "id": "deck_type",
      "prompt": "骨子の型を選んでください",
      "options": [
        {"id": "SCQA", "label": "SCQA"},
        {"id": "PREP", "label": "PREP"},
        {"id": "golden_circle", "label": "ゴールデンサークル"},
        {"id": "TAPS", "label": "TAPS"},
        {"id": "whole_part", "label": "ホールパート"}
      ]
    },
    {
      "id": "scenario",
      "prompt": "シナリオを選んでください",
      "options": [
        {"id": "problem", "label": "課題駆動"},
        {"id": "vision", "label": "ビジョン駆動"},
        {"id": "capital", "label": "資本駆動"},
        {"id": "people", "label": "人駆動"}
      ]
    },
    {
      "id": "tone",
      "prompt": "トーンを選んでください",
      "options": [
        {"id": "light", "label": "ライト"},
        {"id": "navy", "label": "コーポレート・ネイビー"},
        {"id": "dark", "label": "シネマ・ダーク"},
        {"id": "editorial", "label": "エディトリアル白"}
      ]
    },
    {
      "id": "goal",
      "prompt": "目的を選んでください",
      "options": [
        {"id": "approval", "label": "承認を得たい（提案）"},
        {"id": "share", "label": "共有して知ってほしい"},
        {"id": "move", "label": "ビジョンで動かす"}
      ]
    },
    {
      "id": "target",
      "prompt": "ターゲットを選んでください",
      "options": [
        {"id": "external", "label": "社外・初対面"},
        {"id": "internal", "label": "社内・意思決定者"},
        {"id": "partner", "label": "既存パートナー"}
      ]
    }
  ]
}
```

**選択後の案内（例）**:
入力内容:
```
選択した5問を CLI の --type / --scenario / --tone / --goal / --target に対応づけてください。
未指定の教材例を使う場合は、入力 examples/loop_engineering.md、型 ゴールデンサークル、シナリオ ビジョン駆動、トーン コーポレート・ネイビー、目的 共有して知ってほしい、ターゲット 社外・初対面を使えます。
```

**期待される結果**: generate コマンドに渡す5つの値が確定します。

---

## 🚀 Step 3: generate を実行

README の形式に合わせて、本文図解と固定 chrome のデッキを生成します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: generate を実行",
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

**選択後の案内（例）**:
入力内容:
```
確定した入力と5問で slide-forge の generate を実行してください。

例:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1

注意:
- --input / --outline は複数指定できます
- --formats は pptx pdf png html を使います
- OpenAI キーは画像生成だけに使われ、LLM エージェントには渡しません
- 秘密情報の値を表示しないでください
```

**期待される結果**: `./out/job1` 配下に生成ジョブが作成され、JSON の `artifacts` に `./out/job1/deck/navy/` 配下の出力パスが表示されます。

---

## 🚀 Step 4: 4形式の成果物を確認

生成された PPTX / PDF / PNG / HTML を確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 4形式の成果物を確認",
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

**選択後の案内（例）**:
入力内容:
```
生成された成果物を確認し、絶対パスを整理してください。

確認する成果物:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/contact_sheet.png
4. ./out/job1/deck/navy/deck.html

確認観点:
- 固定 chrome が全ページで同じ座標に揃っている
- PPTX の見出し・リード・フッターが編集可能テキストになっている
- 入力資料に無い固有名詞・数字・日付・費用・KPI が追加されていない
- revise で直したい点があれば1文でメモする
```

**期待される結果**: 4形式の出力と、次に修正したい点が確認できます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "OPENAI_API_KEY is not available"},
      {"id": "trouble_2", "label": "claude / codex CLI が見つからない"},
      {"id": "trouble_3", "label": "render に失敗"},
      {"id": "trouble_4", "label": "内容が入力資料から逸れている"}
    ]
  }]
}
```

### トラブル1: `OPENAI_API_KEY is not available`
**原因**: `.env` に画像生成用キーが設定されていない
**解決プロンプト**:
```
.env に OPENAI_API_KEY が存在するかだけ確認してください。キーの値は表示せず、必要なら安全な設定手順を案内してください。
```

### トラブル2: `claude` / `codex` CLI が見つからない
**原因**: `LLM_BACKEND` に対応する CLI が PATH に無い
**解決プロンプト**:
```
LLM_BACKEND の値と PATH 上の claude / codex CLI を確認し、必要なセットアップ手順を案内してください。
```

### トラブル3: render に失敗
**原因**: Playwright Chromium、ImageMagick、Poppler の不足
**解決プロンプト**:
```
render 失敗のログを読み、npx playwright install chromium、ImageMagick、Poppler のどれが不足しているか切り分けてください。
```

### トラブル4: 内容が入力資料から逸れている
**原因**: 入力資料に無い情報を推測している
**解決プロンプト**:
```
生成デッキを入力資料と照合し、入力資料に無い固有名詞・数字・日付・費用・KPI を削除または「協議中」に修正してください。
```

---

## ✅ チェックポイント
- [ ] 入力資料または直接テキストを確定した
- [ ] `.env` と `config.yaml` の存在を確認した
- [ ] 秘密情報や API キーの値をチャットに貼っていない
- [ ] 5問を選んだ
- [ ] `python cli.py generate --input examples/loop_engineering.md --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー --goal 共有して知ってほしい --target 社外・初対面 --tastes navy --formats pptx pdf png html --out ./out/job1` を実行した
- [ ] PPTX / PDF / PNG / HTML の出力を確認した

---

## 📚 成果物プレビュー

このレッスンの成果物は、議事録から生成した提案デッキ一式です。

### 期待される出力例
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/contact_sheet.png
./out/job1/deck/navy/deck.html
```

> 💡 次の Lesson 29-3 では、既存ジョブを `revise` で1回修正します。

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: ./out/job1/deck/navy 配下に PPTX / PDF / PNG / HTML が生成され、固定 chrome と編集可能テキストを確認できたか判定してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-29-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-29-3
- finish → 終了
