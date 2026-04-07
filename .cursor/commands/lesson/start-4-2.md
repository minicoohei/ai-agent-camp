---
description: "When the user says /start-4-2 — Module 4 Lesson 4-2: Gmail検索・閲覧"
duration: "約25分"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "gmail"]
---

# 🎓 Lesson 4-2: Gmail検索・閲覧

## 📍 このセッションでやること

**Lesson 4-2: Gmail検索・閲覧** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでGmailのメールを検索・閲覧・分析できるようにする |
| 所要時間 | 約25分 |
| 使うスキル | gogcli gmail |
| 前提条件 | gogcli認証セットアップ済み（start-4-1完了） |

**このセッションの流れ:**
1. Gmailの検索クエリ構文を学ぶ
2. メールスレッドの詳細を閲覧する
3. 検索結果をAIで分析・要約する

セッション終了時には、gogcliを使ってGmailのメールを自在に検索・分析できるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

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
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → `gog auth list` で認証状態を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Gmailの検索クエリ構文を学ぶ

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Gmailの検索クエリ構文を学ぶ",
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

gogcliのGmail検索で使える主要なクエリ構文を試してみましょう:

```bash
# 未読メールを検索
gog gmail search "is:unread" --account your-email@gmail.com

# 特定の送信者からのメールを検索
gog gmail search "from:example@company.com" --account your-email@gmail.com

# 直近7日間のメールを検索
gog gmail search "newer_than:7d" --account your-email@gmail.com

# 件名にキーワードを含むメールを検索
gog gmail search "subject:会議" --account your-email@gmail.com

# 添付ファイル付きメールを検索
gog gmail search "has:attachment newer_than:30d" --account your-email@gmail.com

# 複合条件: 未読かつ直近3日以内
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

**主要な検索演算子:**

| 演算子 | 説明 | 例 |
|--------|------|-----|
| `is:unread` | 未読メール | `is:unread` |
| `from:` | 送信者指定 | `from:boss@company.com` |
| `to:` | 受信者指定 | `to:team@company.com` |
| `subject:` | 件名検索 | `subject:議事録` |
| `newer_than:` | 期間指定 | `newer_than:7d` / `newer_than:1m` |
| `has:attachment` | 添付あり | `has:attachment` |
| `label:` | ラベル指定 | `label:important` |
| `in:` | フォルダ指定 | `in:inbox` / `in:sent` |

**期待される結果**: 各クエリに合致するメールの一覧（メールID、件名、送信者、日時）が表示されます。

---

## 🚀 Step 2: メールスレッドの詳細を閲覧する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: メールスレッドの詳細を閲覧する",
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

Step 1で取得したメールのスレッドIDを使って、詳細を確認します:

```bash
# メール検索でスレッドIDを取得
gog gmail search "newer_than:1d" --account your-email@gmail.com

# スレッドの詳細を取得（上記で表示されたスレッドIDを使用）
gog gmail thread get <スレッドID> --account your-email@gmail.com

# メッセージの本文を取得
gog gmail message get <メッセージID> --account your-email@gmail.com
```

**手順:**
1. `gog gmail search` でメールを検索し、興味のあるメールのスレッドIDをメモ
2. `gog gmail thread get` でスレッド全体（返信含む）を閲覧
3. `gog gmail message get` で個別メッセージの本文を取得

**期待される結果**: メールの件名、送信者、日時、本文が表示されます。スレッド表示では返信の連鎖も確認できます。

---

## 🚀 Step 3: 検索結果をAIで分析・要約する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 検索結果をAIで分析・要約する",
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

gogcliで取得したメールをAIに分析させます:

```bash
# 直近1週間の未読メールを取得
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com
```

取得したメール一覧をCursorのチャットに貼り付けて、以下のようなプロンプトで分析を依頼します:

```text
上記のメール一覧を分析して、以下の観点でまとめてください:
1. 返信が必要なメール（優先度: 高/中/低）
2. 情報共有のみのメール（FYI）
3. タスクが含まれているメール
4. 各メールの1行要約
```

**応用例:**
```bash
# 特定の人とのやり取りを時系列でまとめる
gog gmail search "from:boss@company.com newer_than:30d" --account your-email@gmail.com

# → AIに依頼: 「上記のメールを時系列順にまとめ、未対応の依頼事項を抽出してください」
```

**期待される結果**: AIがメールを分類し、優先度付きのタスクリストや要約を生成してくれます。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "検索結果が0件になる"},
      {"id": "trouble_2", "label": "メール本文が文字化けする"},
      {"id": "trouble_3", "label": "認証エラーが出る"},
      {"id": "trouble_4", "label": "--accountを忘れてエラーになる"}
    ]
  }]
}
```

### トラブル1: 検索結果が0件になる
**原因**: クエリ構文の誤り、または該当メールがない
**解決プロンプト**:
```text
クエリを緩くして試してください。まず "newer_than:30d" で直近30日のメールがあるか確認してください。
日本語の件名検索がうまくいかない場合は、送信者や日付で絞り込んでみてください。
```

### トラブル2: メール本文が文字化けする
**原因**: エンコーディングの問題
**解決プロンプト**:
```text
gogcliの出力をファイルにリダイレクトしてみてください:
gog gmail message get <id> --account <email> > /tmp/mail.txt
ファイルのエンコーディングを確認: file /tmp/mail.txt
```

### トラブル3: 認証エラーが出る
**原因**: トークンの有効期限切れ
**解決プロンプト**:
```text
gog auth remove your-email@gmail.com で認証を削除し、
gog auth add your-email@gmail.com で再認証してください。
```

### トラブル4: --accountを忘れてエラーになる
**原因**: gogcliは全コマンドで--accountが必須
**解決プロンプト**:
```text
gogcliでは --account <メールアドレス> がすべてのコマンドで必須です。
エイリアスを設定すると便利です:
alias gogg="gog --account your-email@gmail.com"
```

---

## ✅ チェックポイント
- [ ] Gmailの検索クエリ構文を理解した（is:unread, from:, newer_than:等）
- [ ] メールスレッドの詳細を閲覧できた
- [ ] 検索結果をAIに分析させて要約を生成できた
- [ ] 複合条件での検索ができた


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```text
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```text
以下のgogcliコマンドを実行して、Gmail検索・閲覧が正しく動作するか確認してください:
1. gog gmail search "is:unread newer_than:7d" --account <メールアドレス>
2. 上記の結果から1件選び、gog gmail thread get でスレッド詳細を表示
すべて正常に動作するか確認してください。
```

**期待される結果**: 検索結果とスレッド詳細がエラーなく表示されます。

---

## 🎉 次のステップ

これでGmail検索・閲覧は完了です！次のレッスンではGoogle Calendar操作を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-3）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-3（Google Calendar操作）
- next_window → 新しいウィンドウで /start-4-3
- finish → 終了
