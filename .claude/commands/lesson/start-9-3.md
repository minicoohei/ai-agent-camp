---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
duration: "約25分"
prerequisites: ["start-9-2"]
level: "intermediate"
tags: ["slack", "api", "message", "reply", "post"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 9-3: 返信の送信

## 📍 このセッションでやること

**Lesson 9-3: Slack API — メッセージ送信とユーザー情報取得** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | chat.postMessage でメッセージ・スレッド返信を送信し、users.list / users.info でユーザー情報を取得する |
| 所要時間 | 約25分 |
| 使うスキル | curl, Slack Web API, AIによるテキスト生成 |
| 前提条件 | Lesson 9-2 完了（メッセージ・スレッド取得ができる状態） |
| 教材ページ | [Module 9: Slack](https://ai-agent.camp/ja/course/module-9) を並行参照 |

**このセッションの流れ:**
1. `chat.postMessage` でチャネルにメッセージを送信（dry-run確認フロー）
2. `thread_ts` を指定してスレッド返信を送信
3. メンション付きメッセージの送信
4. `users.list` / `users.info` でユーザー情報を取得（メンション用ID解決）
5. 実践演習: スレッドの内容を要約して返信を作成・送信

セッション終了時には、Slack APIでメッセージ送信・スレッド返信ができ、ユーザー情報も取得できるようになっています。

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
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → トークンを環境変数にセットして Step 1へ)
(check_prereq → `auth.test` を実行して接続確認。`chat:write` スコープの確認も実施。失敗なら Lesson 9-1 を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

**セッション開始時にAIが自動実行する内容:**
```bash
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN)
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'接続OK: {d[\"team\"]} / {d[\"user\"]} (user_id: {d[\"user_id\"]})')" 2>/dev/null || echo "接続失敗: Lesson 9-1 を先に完了してください"
```

---

## 🚀 Step 1: chat.postMessage でメッセージ送信（dry-run確認フロー）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: メッセージ送信（dry-run 付き）",
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

**practice の場合 — AIが実行する内容:**

**重要**: メッセージ送信は取り消せない操作のため、必ず dry-run（プレビュー）を挟む。

1. 送信先チャネルを確認:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=20" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : #{ch[\"name\"]}')"
```

2. **dry-run**: 送信内容をユーザーに確認:
```text
以下の内容を送信します。問題なければ「送信OK」と入力してください。

送信先: #チャネル名 (CHANNEL_ID)
メッセージ: テスト投稿です（Slack API学習中）
```

3. ユーザー確認後に送信:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"テスト投稿です（Slack API学習中）"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**期待される結果**:
```json
{
    "ok": true,
    "channel": "C0XXXXXXX",
    "ts": "1713075000.123456",
    "message": {
        "text": "テスト投稿です（Slack API学習中）",
        "user": "U0XXXXXXX",
        "ts": "1713075000.123456"
    }
}
```

**必要なOAuthスコープ**: `chat:write`

---

## 🚀 Step 2: thread_ts を指定してスレッド返信

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: スレッド返信の送信",
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

**practice の場合 — AIが実行する内容:**

1. 返信先のスレッドを確認（Step 1で投稿したメッセージのtsを使用）:
```bash
# 既存のスレッド付きメッセージを取得
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=5" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    has_thread = '(スレッドあり)' if msg.get('reply_count', 0) > 0 else ''
    print(f'ts={msg[\"ts\"]} {has_thread}: {msg.get(\"text\", \"\")[:60]}')"
```

2. **dry-run** → ユーザー確認後にスレッド返信:
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"スレッド返信テストです","thread_ts":"PARENT_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**ポイント**:
- `thread_ts` に親メッセージの `ts` を指定するとスレッド返信になる
- `reply_broadcast: true` を追加すると、スレッド返信をチャネルにも表示する（「チャネルにも投稿する」と同じ）

---

## 🚀 Step 3: メンション付きメッセージの送信

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: メンション付きメッセージの送信",
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

**practice の場合 — AIが実行する内容:**

メンションはユーザーIDを `<@USER_ID>` 形式で埋め込む:
```bash
# 自分のユーザーIDを確認
MY_USER_ID=$(curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['user_id'])")
echo "自分のユーザーID: $MY_USER_ID"
```

```bash
# メンション付きメッセージの送信（自分宛て ── テスト用）
# dry-run 確認後に実行
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"CHANNEL_ID\",\"text\":\"<@${MY_USER_ID}> メンションテストです\"}" \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**メンション記法一覧:**
| 記法 | 対象 |
|------|------|
| `<@U0XXXXXXX>` | 特定ユーザー |
| `<!channel>` | チャネル全員 |
| `<!here>` | オンラインメンバー全員 |
| `<!subteam^S0XXXXXXX>` | ユーザーグループ |

**注意**: `<!channel>` や `<!here>` は多くの人に通知が飛ぶため、テスト目的では使わないこと。

---

## 🚀 Step 4: users.list / users.info でユーザー情報を取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: ユーザー情報の取得",
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

**practice の場合 — AIが実行する内容:**

1. `users.list` でワークスペースのユーザー一覧を取得:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=50" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if u.get('deleted') or u.get('is_bot'):
        continue
    print(f'{u[\"id\"]} : {u.get(\"real_name\", \"不明\")} (@{u[\"name\"]})')"
```

2. `users.info` で特定ユーザーの詳細を取得:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.info?user=U0XXXXXXX" \
  | python3 -c "
import sys, json
u = json.load(sys.stdin)['user']
print(f'名前: {u.get(\"real_name\", \"不明\")}')
print(f'表示名: {u.get(\"profile\", {}).get(\"display_name\", \"未設定\")}')
print(f'メール: {u.get(\"profile\", {}).get(\"email\", \"非公開\")}')
print(f'ステータス: {u.get(\"profile\", {}).get(\"status_text\", \"なし\")}')
print(f'タイムゾーン: {u.get(\"tz\", \"不明\")}')"
```

**主要フィールド:**
| フィールド | 説明 |
|-----------|------|
| `id` | ユーザーID（メンションに使用） |
| `name` | ユーザー名（@の後に続く名前） |
| `real_name` | 本名 |
| `profile.display_name` | 表示名 |
| `profile.email` | メールアドレス（`users:read.email` スコープが必要） |
| `tz` | タイムゾーン |
| `is_bot` | ボットかどうか |

**必要なOAuthスコープ**: `users:read`

---

## 🚀 Step 5: 実践演習 — スレッドの要約を返信として送信

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 実践演習 — スレッド要約を返信",
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

**practice の場合 — 以下のワークフローを実行:**

この演習では、Lesson 9-2 で学んだメッセージ取得と本レッスンの送信を組み合わせる。

1. **スレッドの取得**: `conversations.replies` でスレッドを取得
2. **ユーザーID解決**: `users.info` でユーザー名に変換
3. **AI要約**: 取得したスレッドの内容をAIに要約させる
4. **dry-run**: 要約テキストを表示してユーザーに確認
5. **スレッド返信**: `chat.postMessage` で要約を返信として送信

```bash
# 1. スレッドを取得してファイルに保存
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.replies?channel=CHANNEL_ID&ts=THREAD_TS" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    print(f'[{ts.strftime(\"%m/%d %H:%M\")}] {msg.get(\"user\",\"?\")} : {msg.get(\"text\",\"\")}')" \
  > ~/ai-agent-camp/data/slack_thread_for_summary.txt
```

```text
# 2. AIに要約を依頼
~/ai-agent-camp/data/slack_thread_for_summary.txt を読んで、
このスレッドの内容を3-5行で要約してください。
要約は「このスレッドのまとめ:」で始めてください。
```

```bash
# 3. dry-run確認後、要約をスレッド返信として送信
curl -s -X POST -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"CHANNEL_ID","text":"このスレッドのまとめ:\n（AIが生成した要約テキスト）","thread_ts":"THREAD_TS"}' \
  "https://slack.com/api/chat.postMessage" \
  | python3 -m json.tool
```

**期待される結果**: スレッドに要約が返信として投稿される。

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
      {"id": "trouble_1", "label": "chat.postMessage で not_authed / missing_scope"},
      {"id": "trouble_2", "label": "メッセージが送信されたが表示されない"},
      {"id": "trouble_3", "label": "メンションが機能しない（テキストのまま表示）"},
      {"id": "trouble_4", "label": "日本語メッセージが文字化けする"}
    ]
  }]
}
```

### トラブル1: 「not_authed / missing_scope」
**原因**: `chat:write` スコープが未設定
**解決方法**:
1. https://api.slack.com/apps でアプリを開く
2. OAuth & Permissions → User Token Scopes に `chat:write` を追加
3. ワークスペースに再インストール
4. 新しいトークンを `credential_manager.py store SLACK_USER_TOKEN` で再保存

### トラブル2: 「メッセージが送信されたが表示されない」
**原因**: 別のチャネルに送信された、またはスレッド内に投稿された
**解決方法**:
```bash
# レスポンスの channel と ts を確認
# channel が想定と一致しているか
# thread_ts が含まれていないか（意図せずスレッド返信になっていないか）
```

### トラブル3: 「メンションがテキストのまま表示される」
**原因**: `@username` のようにテキストで書いている
**解決方法**: メンションは `<@U0XXXXXXX>` の形式でユーザーIDを使う。`@名前` ではメンションにならない。
```bash
# ユーザーIDを検索
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.list?limit=100" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for u in data.get('members', []):
    if not u.get('deleted') and not u.get('is_bot'):
        print(f'<@{u[\"id\"]}> → {u.get(\"real_name\", u[\"name\"])}')"
```

### トラブル4: 「日本語メッセージが文字化けする」
**原因**: JSONエンコーディングの問題
**解決方法**: `Content-Type: application/json; charset=utf-8` を指定し、JSONボディで送信する。`application/x-www-form-urlencoded` では日本語をURLエンコードする必要がある。

---

## ✅ チェックポイント
- [ ] `chat.postMessage` でチャネルにメッセージを送信できた
- [ ] `thread_ts` を指定してスレッド返信を送信できた
- [ ] メンション付きメッセージを送信できた
- [ ] `users.list` / `users.info` でユーザー情報を取得できた
- [ ] スレッドの要約を作成して返信として送信できた

---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力とSlack上の投稿です。

### 期待される出力例
```text
# chat.postMessage の結果
ok: true
channel: C0XXXXXXX
ts: 1713075000.123456

# users.list の結果
U0ABC1234 : 山田太郎 (@taro.yamada)
U0DEF5678 : 佐藤花子 (@hanako.sato)
U0GHI9012 : 田中一郎 (@ichiro.tanaka)

# Slack上の表示
#general に「テスト投稿です（Slack API学習中）」が投稿される
スレッドに要約が返信として投稿される
```

---

## ➡️ 次のステップ

これでSlack APIの基本操作（チャネル取得・メッセージ取得・メッセージ送信・ユーザー情報取得）がすべて完了しました。次のモジュールに進みましょう。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-10-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-10-1
- finish → 終了
