---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "約20分"
prerequisites: ["start-29-2"]
level: "intermediate"
tags: ["slide", "assets", "vision"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-4: 実画像の自動取得 fetch-assets

## 📍 このセッションでやること

**Lesson 29-4: 実画像の自動取得 fetch-assets** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 既存ジョブに実在の企業ロゴ・人物宣材・製品画像を安全に追加する |
| 所要時間 | 約20分 |
| 使うスキル | slide-forge, fetch-assets, vision照合 |
| 前提条件 | Lesson 29-2 |
| 教材ページ | [Module 29: slide-forge](https://ai-agent.camp/ja/course/module-29?slideId=fetch-assets) を並行参照 |

**このセッションの流れ:**
1. 対象ジョブとキー設定を確認
2. 権利と利用可否を確認
3. fetch-assets を実行
4. 取得結果とデッキを確認

セッション終了時には、vision 照合に合格した実画像だけを使う流れを確認できています。

> **💡 ヒント**: 取得画像の権利・利用可否の確認は利用者の責任です。秘密情報や API キーをチャットに貼らないでください。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "fetch-assets で実画像取得を始める準備はできていますか？",
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
(check_prereq → Lesson 29-2 の出力、GEMINI_API_KEY、SERPAPI_KEY、権利確認を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 対象ジョブとキー設定を確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 対象ジョブとキー設定を確認",
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
fetch-assets の対象ジョブとキー設定を確認してください。

確認項目:
1. 既存ジョブの --out パス（例: ./out/job1）
2. .env に GEMINI_API_KEY があるか確認する
3. SERPAPI_KEY は Google 画像検索用に推奨
4. キーの値は表示しない
5. 議事録に実在の企業名・製品名・人物名が含まれているか確認する
```

**期待される結果**: fetch-assets を実行できる対象と設定が明確になります。

---

## 🚀 Step 2: 権利と利用可否を確認

Web から取得する画像の扱いを確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 権利と利用可否を確認",
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
fetch-assets 実行前に、画像の権利と利用可否を確認してください。

重要:
1. 取得画像の権利・利用可否の確認は利用者の責任です
2. 結果 JSON の catalog[].note に出典 URL が残ります
3. vision 照合で score が低い素材は使いません
4. 合格素材が無いスライドは図解のままにします
5. Web を使いたくない場合は --photo-catalog で手元画像カタログを使えます
```

**期待される結果**: fetch-assets を使う範囲と責任分界が明確になります。

---

## 🚀 Step 3: fetch-assets を実行

既存ジョブに後付けで実画像を注入します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: fetch-assets を実行",
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
既存ジョブに fetch-assets を実行してください。

python cli.py fetch-assets --out ./out/job1

新規生成時にまとめて取得する場合:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1 --fetch-assets

注意:
- GEMINI_API_KEY は抽出と vision 照合に必須です
- SERPAPI_KEY は Google 画像検索に推奨です
- 秘密情報の値は表示しません
- 合格した素材が無い場合は図解のままにします
```

**期待される結果**: 実画像候補が取得され、vision 照合に合格した素材だけがデッキへ反映されます。

---

## 🚀 Step 4: 取得結果とデッキを確認

結果 JSON と更新後のデッキを確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 取得結果とデッキを確認",
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
fetch-assets の結果と更新後のデッキを確認してください。

確認観点:
1. 結果 JSON の catalog[].note に出典 URL が残っている
2. 名前と画像が一致している
3. score が低い素材が無理に使われていない
4. 権利・利用可否を利用者側で確認する必要がある
5. 固定 chrome と PPTX の編集可能テキストが維持されている
```

**期待される結果**: 実画像の出典、照合結果、デッキ反映状態を確認できます。

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
      {"id": "trouble_1", "label": "GEMINI_API_KEY が無い"},
      {"id": "trouble_2", "label": "素材が採用されない"},
      {"id": "trouble_3", "label": "別会社のロゴが出る"},
      {"id": "trouble_4", "label": "権利確認が不安"}
    ]
  }]
}
```

### トラブル1: `GEMINI_API_KEY` が無い
**原因**: 抽出と vision 照合に必要なキーが未設定
**解決プロンプト**:
```
.env に GEMINI_API_KEY が存在するかだけ確認してください。値は表示せず、未設定なら安全な設定手順を案内してください。
```

### トラブル2: 素材が採用されない
**原因**: vision 照合の score が不足している、または候補が見つからない
**解決プロンプト**:
```
fetch-assets の結果 JSON を確認し、score が低い素材や候補なしの理由を整理してください。無理に採用せず図解のままでよいことも説明してください。
```

### トラブル3: 別会社のロゴが出る
**原因**: 似た名前の別会社候補が検索に混ざっている
**解決プロンプト**:
```
catalog の候補名、出典 URL、vision 照合結果を確認し、名前と画像が一致しない素材を除外してください。
```

### トラブル4: 権利確認が不安
**原因**: Web 取得画像の利用条件を確認していない
**解決プロンプト**:
```
取得画像の出典 URL を一覧化し、利用者が権利・利用可否を確認するためのチェックリストを作ってください。
```

---

## ✅ チェックポイント
- [ ] 既存ジョブの `--out` パスを確認した
- [ ] `GEMINI_API_KEY` の存在を値を出さずに確認した
- [ ] `SERPAPI_KEY` の必要性を理解した
- [ ] 取得画像の権利・利用可否は利用者責任で確認することを理解した
- [ ] `python cli.py fetch-assets --out ./out/job1` を実行した
- [ ] 結果 JSON の `catalog[].note` と更新後デッキを確認した
- [ ] 秘密情報や API キーをチャットに貼っていない

---

## 📚 成果物プレビュー

このレッスンの成果物は、実画像候補の照合結果と更新後のデッキです。

### 期待される出力例
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 出典 URL は結果 JSON の `catalog[].note` を確認します。権利・利用可否は必ず利用者側で判断します。

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: fetch-assets の結果 JSON と更新後 deck.pptx を確認し、出典 URL、vision 照合、権利確認の未完了項目を判定してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。必要に応じて、新しいウィンドウで別のレッスンを開始してください。

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-29-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-29-1
- finish → 終了
