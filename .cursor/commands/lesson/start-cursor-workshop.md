---
description: "Cursorの使い方研修（メール・議事録・画像要約）を開始する"
aliases: ["/start-cursor-usage", "/cursor-workshop"]
duration: "約15分"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["cursor", "workshop", "basics"]
---

# Cursorの使い方 研修（ハンズオン）

## このコマンドでやること

**Cursorの使い方** の実践演習です。メール作成・議事録作成・画像要約のいずれかを選び、**@ で Resource を指定する**ことと**ドラッグ＆ドロップ**でコンテキストを渡す操作を習得します。

| 項目 | 内容 |
|------|------|
| ゴール | @ とドラッグ＆ドロップでファイルをAIに渡し、メール・議事録・画像要約のいずれかを完成させる |
| 所要時間 | 各演習 約10〜15分 |
| 教材ページ | [Cursorの使い方](../../../course/index.html) |
| 研修用ファイル | `course/foundation/cursor-workshop/` 内の `draft_email.txt` / `meeting_memo.txt` を使用 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」と入力すると再開します。

> **Claude Code / Codex ユーザーへ**: このレッスンはCursor GUI操作（@メンション、ドラッグ＆ドロップ）を前提としています。CLI環境では、ファイルパスを直接指定して同等の操作が可能です。例: `このファイルを読んで要約して: course/foundation/cursor-workshop/draft_email.txt`

---

## Step 1: 教材とファイルの場所の確認

- **教材**: [course/index.html](../../../course/index.html) の「コンテキストの渡し方」「研修内容（ハンズオン）」を参照してください。
- **研修用ファイル**: ワークスペース内の `course/foundation/cursor-workshop/` に以下があります。
  - `draft_email.txt` … メール作成演習用たたき台
  - `meeting_memo.txt` … 議事録演習用メモ
  - 画像要約は任意の画像（スクショ・図表など）を用意してください。

---

## Step 2: @ で Resource を指定する

1. Cursorのチャット入力欄で **@** を入力する
2. 表示された一覧から「File」を選び、`course/foundation/cursor-workshop/draft_email.txt` や `meeting_memo.txt` を選択する
3. 選択したファイルがコンテキストに含まれた状態で、指示文を書いて送信する

例: `@draft_email.txt` を付けたうえで「このメールを敬語で整えて、完成した形で出力してください」

---

## Step 3: ドラッグ＆ドロップ

1. エクスプローラーや Finder から、使いたいファイルをチャット入力欄に**ドラッグ＆ドロップ**する
2. ファイルがチャットに追加されたら、指示文を書いて送信する

@ と同じく、AIがその内容を読んだうえで返答します。

---

## Step 4: 演習を選ぶ

**演習ごとに Step 1〜3 のコマンドがあります。** 直接そのコマンドで始めてもよいです。

| 演習 | コマンド（Step 1〜3） |
|------|------------------------|
| メールを作成する | `/start-cursor-workshop-email` |
| 議事録を作成・レビューする | `/start-cursor-workshop-minutes` |
| 画像を読み込んで要約する | `/start-cursor-workshop-image` |

**AskQuestionの設定例:**
```json
{
  "title": "演習を選んでください",
  "questions": [{
    "id": "exercise",
    "prompt": "どれから試しますか？",
    "options": [
      {"id": "email", "label": "メールを作成する（/start-cursor-workshop-email）"},
      {"id": "minutes", "label": "議事録を作成・レビューする（/start-cursor-workshop-minutes）"},
      {"id": "image", "label": "画像を読み込んで要約する（/start-cursor-workshop-image）"},
      {"id": "view_only", "label": "手順だけ確認する"}
    ]
  }]
}
```

( email を選んだ場合 → 以下「メールを作成する」の手順を案内。または `/start-cursor-workshop-email` で Step 1〜3 を開始 )
( minutes を選んだ場合 → 以下「議事録を作成・レビューする」の手順を案内。または `/start-cursor-workshop-minutes` で Step 1〜3 を開始 )
( image を選んだ場合 → 以下「画像を読み込んで要約する」の手順を案内。または `/start-cursor-workshop-image` で Step 1〜3 を開始 )

### メールを作成する（email）

- **ファイル**: `course/foundation/cursor-workshop/draft_email.txt` を @ で指定するか、ドラッグ＆ドロップする
- **指示例**: 「このたたき台をビジネスメールとして完成させてください。件名・宛先・本文を整えた形で出力してください」
- **期待**: 敬語で整ったメール文面が返る

### 議事録を作成・レビューする（minutes）

- **ファイル**: `course/foundation/cursor-workshop/meeting_memo.txt` を @ で指定するか、ドラッグ＆ドロップする
- **指示例**: 「このメモを議事録形式にまとめてください。日付・出席者・議題・決定事項・次回の順で書いてください」
- **期待**: 体裁の整った議事録が返る。続けて「表現をレビューして改善案を出してください」と依頼してもよい

### 画像を読み込んで要約を作成する（image）

- **やり方**: 任意の画像（スクリーンショット・図表・スライド1枚など）をチャットに**ドラッグ＆ドロップ**する（または @ で画像ファイルを指定する）
- **指示例**: 「この画像の内容を要約してください」「この図が説明していることを箇条書きで教えてください」
- **期待**: 画像の内容に基づいた要約や説明が返る

---

## チェックポイント

- [ ] @ を入力してファイルを選び、指示を送れた
- [ ] ファイルをドラッグ＆ドロップして、指示を送れた
- [ ] メール・議事録・画像要約のうち、少なくとも1つを完了した

---

## 次に進む

演習が終わったら、[Cursorの使い方](../../../course/index.html) の他のセクション（モードの使い分け・Commands など）に進むか、環境セットアップの `/start-0-1` に進んでください。
