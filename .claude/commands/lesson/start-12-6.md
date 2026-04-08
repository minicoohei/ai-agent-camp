---
description: "When the user says /start-12-6 — Module 12 Lesson 12-6: Notion への書き込み・更新と安全な確認フロー"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-5"]
duration: "約35分"
level: "intermediate"
tags: ["notion", "mcp", "write", "update"]
---

# 🎓 Lesson 12-6: 書き込みと更新

## 📍 このセッションでやること

**Lesson 12-6** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | **ページ本文の追記・プロパティ更新・新規子ページ作成** を行い、**本番を壊さない確認手順** を身につける |
| 所要時間 | 約35分 |
| 使うスキル | Notion MCP（create / update / append）、必要に応じて ncli |
| 前提条件 | `/start-12-5` まで完了 |
| 教材ページ | [Module 12: Notion](https://ai-agent.camp/ja/course/module-12) を並行参照 |

**このセッションの流れ:**
1. **下書き用** のページまたは DB を複製・作成し、そこでだけ試す
2. 変更内容を **差分としてユーザーに提示** してから実行する
3. 実行後、Notion 側で表示を確認し、ロールバック手順を理解する

> **⚠️ 安全**: 共有Wikiや本番DBでは **必ず複製ページ** で作業する。ユーザーの明示承認なしに本番プロパティを書き換えない。

---

## 🎯 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "🎯 書き込み前の確認",
  "questions": [{
    "id": "target",
    "prompt": "変更の対象はどれですか？",
    "options": [
      {"id": "sandbox", "label": "下書き／複製ページのみ（推奨）"},
      {"id": "existing", "label": "既存の本番ページ（ユーザーが責任を取る）"},
      {"id": "read_only", "label": "今回は手順の読み合わせのみ"}
    ]
  }]
}
```

---

## 🚀 Step 1: サンドボックスの準備

エージェントの指示例:
```text
「演習用 Notion」ページの下に、今日の日付のサブページを1つ作り、
そこにだけ本文を追記してください。親ページの他ブロックには触れないでください。
```

---

## 🚀 Step 2: 追記またはプロパティ更新

1. **追記**: ブロック append で見出し＋箇条書きを追加（既存ブロックの ID はユーザーに確認）
2. **プロパティ**: Select / Status / Date など、**変更前後の値** をチャットに書いてから PATCH
3. **新規 DB 行**: タイトルと必須プロパティだけ埋め、残りはユーザーが手で埋められるようにする

---

## 🚀 Step 3: 検証とロールバック

1. Notion を開き、期待どおり表示されたかユーザーと確認
2. 誤りがあれば **同じツールで元に戻す** か、ページ履歴（あれば）を案内
3. **完了報告** に変更したページ URL・項目名・新しい値を記載する

---

## ✅ 完了条件

- [ ] 本番を直接編集した場合は、事前にユーザーの承認をチャットに残している
- [ ] 少なくとも 1 回、変更前後の差分をユーザーが確認できた
- [ ] 演習用ページ／DB の URL を最終報告に含めた

---

## ➡️ 次のステップ

これでModule 12（Notion連携）は完了です。

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-13-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-13-1
- finish → 終了
