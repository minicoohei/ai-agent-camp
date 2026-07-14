---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "35分"
prerequisites: ["start-16-1"]
level: "intermediate"
tags: ["email", "gmail", "gogcli", "send"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 16-3: gogcli でメール送信

## 📍 このセッションでやること

**Lesson 16-3: gogcli でメール送信** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | `gog gmail send` でメール新規作成・送信・スレッド返信・添付を実践する |
| 所要時間 | 約35分 |
| 使うツール | gogcli (gog) |
| 前提条件 | Lesson 16-1 完了（gogcli認証済み）|
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. バージョン確認と `--account` の指定方法を学ぶ
2. 自分宛にテストメールを送信
3. スレッド返信（`--thread-id`）を実践
4. 添付ファイル送信（`--attach`）を実践

セッション終了時には、gogcli でメールの送信・返信・添付が安全にできるようになっています。

> **⚠️ 重要**: メール送信はやり直しがきかない操作です。送信前に内容をよく確認してください。
> **📌 注意**: v0.9.0 では `--dry-run` フラグは廃止されました。送信前の確認は目視で行ってください。

---

## 🎯 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "previous_lesson", "label": "13-1 をまずやりたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

---

## 🚀 Step 1: バージョン確認と事前準備

まず gogcli のバージョンを確認し、`--account` の指定方法を理解します。

```bash
gog --version
```

v0.9.0 以上であることを確認してください。

> **📌 重要**: v0.9.0 では `--dry-run` フラグは廃止されました。送信前にコマンドの引数（宛先・件名・本文）を目視で確認してください。
> すべての `gog gmail` コマンドには `--account <your-email@gmail.com>` が必要です。

**AskQuestion:**
```json
{
  "title": "📋 バージョン確認",
  "questions": [{
    "id": "version_result",
    "prompt": "gogcli のバージョンは v0.9.0 以上ですか？",
    "options": [
      {"id": "correct", "label": "v0.9.0 以上 → 次へ進む"},
      {"id": "old_version", "label": "古いバージョン → アップデートを手伝って"},
      {"id": "error", "label": "エラーが出た → トラブルシューティング"}
    ]
  }]
}
```

---

## 🚀 Step 2: テストメールを送信

**⚠️ 送信先は必ず自分自身のメールアドレスを使用してください。**

```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "gogcli テスト送信" \
  --body "このメールは gogcli (gog gmail send) から送信されたテストメールです。"
```

**期待される結果:**
- 送信成功のメッセージが表示
- 自分の受信箱にメールが届く

**ファイルから本文を読み込む場合:**
```bash
echo "これはファイルから読み込んだ本文です。" > /tmp/test-email.txt
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "ファイルから送信テスト" \
  --body-file /tmp/test-email.txt
```

---

## 🚀 Step 3: スレッド返信

先ほど送信したメールのスレッドに返信します。

**Step 3-1: スレッドIDを取得**
```bash
gog gmail search "subject:gogcli テスト送信" --account <your-email@gmail.com> --max 1
```

出力からスレッドIDを確認します。

**Step 3-2: スレッドに返信**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --thread-id <thread-id> \
  --subject "Re: gogcli テスト送信" \
  --body "このメールは gogcli からのスレッド返信テストです。"
```

> **📌 注意**: v0.9.0 では `--subject` は必須です。返信時も省略できません。

**全員返信（reply-all）の場合:**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --reply-to-message-id <message-id> \
  --reply-all \
  --subject "Re: 元の件名" \
  --body "全員返信のテストです。"
```

---

## 🚀 Step 4: 添付ファイル送信

ファイルを添付してメールを送信します。

**テスト用ファイルを作成:**
```bash
echo "添付ファイルのテスト内容です。" > /tmp/test-attachment.txt
```

**添付ファイル付きメールを送信:**
```bash
gog gmail send \
  --account <your-email@gmail.com> \
  --to <your-email@gmail.com> \
  --subject "添付ファイルテスト" \
  --body "添付ファイル付きメールのテストです。" \
  --attach /tmp/test-attachment.txt
```

> **📌 注意**: 送信前に `--to`, `--subject`, `--body`, `--attach` の内容を目視で確認してください。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestion:**
```json
{
  "title": "⚠️ トラブルはありましたか？",
  "questions": [{
    "id": "trouble",
    "prompt": "何か問題がありましたか？",
    "options": [
      {"id": "none", "label": "問題なし → チェックポイントへ"},
      {"id": "send_fail", "label": "送信に失敗した"},
      {"id": "scope_error", "label": "権限エラーが出た"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

| トラブル | 解決策 |
|---------|--------|
| `insufficient permission` | `gog auth remove <email>` → `gog auth add <email>` で再認証 |
| 送信したが届かない | 迷惑メールフォルダを確認 |
| `thread not found` | スレッドIDが正しいか `gog gmail search` で再確認 |
| 添付ファイルエラー | ファイルパスが正しいか確認（絶対パス推奨） |

---

## ✅ チェックポイント

- [ ] `gog --version` で v0.9.0 以上を確認できた
- [ ] 自分宛にテストメールを送信し、受信を確認できた
- [ ] `--thread-id` でスレッド返信ができた
- [ ] `--attach` で添付ファイルを送信できた


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/email/
├── index.html  (HTMLメール)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/email/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/email/index.html
```

> 💡 HTMLの構造確認: `head -30 output/email/index.html`

---

## ✅ 完了チェック

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-3 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_lesson", "label": "13-4 へ → メールシーケンス設計"},
      {"id": "practice", "label": "もう少し送信を練習したい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```
