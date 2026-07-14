---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "約15分"
prerequisites: ["start-29-2"]
level: "beginner"
tags: ["slide", "revise"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-3: revise で既存ジョブを修正

## 📍 このセッションでやること

**Lesson 29-3: revise で既存ジョブを修正** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 既存ジョブに修正指示を1つ入れ、必要なページだけを再生成する |
| 所要時間 | 約15分 |
| 使うスキル | slide-forge, revise, 差分確認 |
| 前提条件 | Lesson 29-2 |
| 教材ページ | [Module 29: slide-forge](https://ai-agent.camp/ja/course/module-29?slideId=revise) を並行参照 |

**このセッションの流れ:**
1. 対象ジョブと修正指示を決める
2. revise を実行
3. 更新後の成果物を確認
4. 不要な変化がないか確認

セッション終了時には、生成済みデッキを1回修正し、更新後の PPTX / PDF / HTML / PNG を確認できています。

> **💡 ヒント**: 入力資料に無い数字や固有名詞は追加しません。秘密情報や API キーもチャットに貼らないでください。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "revise で既存ジョブを修正する準備はできていますか？",
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
(check_prereq → Lesson 29-2 の出力フォルダと修正指示の確認を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 対象ジョブと修正指示を決める

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 対象ジョブと修正指示を決める",
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
revise 対象のジョブと修正指示を確定してください。

確認項目:
1. 対象ジョブの --out パス（例: ./out/job1）
2. 修正指示を1文で書く（例: p3をもっと強く、表紙のタイトルを短く）
3. 入力資料に無い数字・固有名詞を追加しない
4. 秘密情報や API キーの値は表示しない
```

**期待される結果**: `--out` パスと `--instruction` に入れる文が確定します。

---

## 🚀 Step 2: revise を実行

README / quickstart の形式に合わせて `revise` を実行します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: revise を実行",
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
確定したジョブと修正指示で revise を実行してください。

例:
python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"

注意:
- 変更ページの本文画像だけを再生成します
- 入力資料に無い情報は追加しません
- 秘密情報の値を表示しないでください
```

**期待される結果**: 既存ジョブの成果物が更新されます。

---

## 🚀 Step 3: 更新後の成果物を確認

更新後の出力を開き、修正指示が反映されたか確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 更新後の成果物を確認",
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
更新された成果物を確認してください。

確認する成果物:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/deck.html
4. ./out/job1/deck/navy/contact_sheet.png

確認観点:
- 修正指示が反映されている
- PPTX のテキストは編集可能なまま
- 固定 chrome の座標が崩れていない
```

**期待される結果**: 修正対象ページの改善が確認できます。

---

## 🚀 Step 4: 不要な変化がないか確認

修正対象以外のページに不要な変化がないか確認します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 不要な変化がないか確認",
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
revise 前後の成果物を比較し、修正対象以外のページに不要な変化がないか確認してください。

確認観点:
1. 修正指示と関係ないページのストーリーが変わっていない
2. 固定 chrome の座標が全ページで揃っている
3. 入力資料に無い数字・固有名詞が増えていない
4. 次に直すなら、別の revise 指示を1文で書ける
```

**期待される結果**: revise が意図した範囲に収まっていることを確認できます。

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
      {"id": "trouble_1", "label": "--out パスが見つからない"},
      {"id": "trouble_2", "label": "修正指示が反映されない"},
      {"id": "trouble_3", "label": "関係ないページが変わった"},
      {"id": "trouble_4", "label": "API キーの扱いが不安"}
    ]
  }]
}
```

### トラブル1: `--out` パスが見つからない
**原因**: Lesson 29-2 の出力フォルダと違うパスを指定している
**解決プロンプト**:
```
Lesson 29-2 で生成した out フォルダを探し、revise に渡す --out パスを特定してください。
```

### トラブル2: 修正指示が反映されない
**原因**: 指示が曖昧、または対象ページが特定できていない
**解決プロンプト**:
```
修正指示を「p3 の見出しを短く」「p5 の効果数字を大きく」のように、対象ページと変更内容が分かる1文に直してください。
```

### トラブル3: 関係ないページが変わった
**原因**: 修正指示の範囲が広すぎる
**解決プロンプト**:
```
revise の修正指示を対象ページと対象要素に絞り、不要な変更が起きない形に言い換えてください。
```

### トラブル4: API キーの扱いが不安
**原因**: 値を表示する確認をしている
**解決プロンプト**:
```
.env のキーは値を表示せず、存在有無だけを確認してください。秘密情報をチャットに貼らない運用を徹底してください。
```

---

## ✅ チェックポイント
- [ ] 対象ジョブの `--out` パスを確認した
- [ ] 修正指示を1文で決めた
- [ ] 秘密情報や API キーの値をチャットに貼っていない
- [ ] `python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"` を実行した
- [ ] 更新後の PPTX / PDF / HTML / PNG を確認した
- [ ] 修正対象以外のページに不要な変化がないことを確認した

---

## 📚 成果物プレビュー

このレッスンの成果物は、revise 後に更新された既存ジョブです。

### 期待される出力例
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 修正を重ねる場合も、1回の revise では対象ページと変更内容を絞ると確認しやすくなります。

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: revise 後の deck.pptx / deck.pdf / deck.html / contact_sheet.png を確認し、修正指示の反映と不要な変化の有無を判定してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-29-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-29-4
- finish → 終了
