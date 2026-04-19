---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
duration: "約25分"
prerequisites: ["start-9-1"]
level: "beginner"
tags: ["slack", "api", "message", "thread", "history"]
---

# 🎓 Lesson 9-2: メッセージ・スレッド取得

## 📍 このセッションでやること

**Lesson 9-2: Slack API — メッセージとスレッドの取得** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | conversations.history / conversations.replies でメッセージとスレッドを取得し、AIで要約・タスク抽出する |
| 所要時間 | 約25分 |
| 使うスキル | curl, Slack Web API, AIによるテキスト分析 |
| 前提条件 | Lesson 9-1 完了（トークン設定・チャネル取得ができる状態） |
| 教材ページ | [Module 9: Slack](https://ai-agent.camp/ja/course/module-9) を並行参照 |

**このセッションの流れ:**
1. `conversations.history` でチャネルメッセージを取得
2. メッセージ構造の理解（ts, user, text, thread_ts）
3. `conversations.replies` でスレッド返信を展開
4. DM・グループDMのメッセージ取得
5. 取得結果をAIに渡して要約・タスク抽出

セッション終了時には、任意のチャネルからメッセージを取得し、スレッドを展開して内容を分析できるようになっています。

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
(check_prereq → `auth.test` を実行して接続確認。失敗なら Lesson 9-1 を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

**セッション開始時にAIが自動実行する内容:**
```bash
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN)
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'接続OK: {d[\"team\"]} / {d[\"user\"]}')" 2>/dev/null || echo "接続失敗: Lesson 9-1 を先に完了してください"
```

---

## 🚀 Step 1: conversations.history でチャネルメッセージを取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: チャネルメッセージの取得",
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

まずチャネル一覧からIDを取得し、そのチャネルのメッセージを取得:
```bash
# チャネル一覧を取得（IDとnameの対応を確認）
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=10" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : #{ch[\"name\"]}')"
```

```bash
# 特定チャネルのメッセージを取得（CHANNEL_ID を置き換え）
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=10" \
  | python3 -m json.tool
```

**主要パラメータ:**
| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `channel` | チャネルID（必須） | `C0XXXXXXX` |
| `limit` | 取得件数（デフォルト100、最大1000） | `20` |
| `oldest` | この時刻以降のメッセージを取得（Unixタイムスタンプ） | `1700000000` |
| `latest` | この時刻以前のメッセージを取得（Unixタイムスタンプ） | `1700100000` |

**必要なOAuthスコープ**: `channels:history`（公開チャネル）、`groups:history`（プライベート）

---

## 🚀 Step 2: メッセージ構造の理解

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: メッセージ構造の理解",
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

取得したメッセージを見やすく整形:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=5" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    thread = ' [スレッドあり]' if 'thread_ts' in msg and msg.get('reply_count', 0) > 0 else ''
    print(f'--- {ts.strftime(\"%Y-%m-%d %H:%M\")} ---')
    print(f'User: {msg.get(\"user\", \"不明\")}')
    print(f'Text: {msg.get(\"text\", \"\")}')
    print(f'ts: {msg[\"ts\"]}{thread}')
    if msg.get('reply_count'):
        print(f'返信数: {msg[\"reply_count\"]}')
    print()"
```

**メッセージの主要フィールド:**
| フィールド | 説明 |
|-----------|------|
| `ts` | メッセージのタイムスタンプ（一意識別子としても使用） |
| `user` | 送信者のユーザーID |
| `text` | メッセージ本文 |
| `thread_ts` | スレッドの親メッセージのts（スレッド返信の場合に存在） |
| `reply_count` | スレッド返信の数（親メッセージにのみ存在） |
| `reactions` | リアクション一覧 |

**ポイント**: `ts` はメッセージの一意識別子であり、タイムスタンプでもある。`thread_ts` と同じ値なら親メッセージ、異なる値なら返信メッセージ。

---

## 🚀 Step 3: conversations.replies でスレッド返信を展開

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: スレッド返信の展開",
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

Step 2 でスレッドがあるメッセージの `ts` を使ってスレッド全体を取得:
```bash
# THREAD_TS を親メッセージの ts に置き換える
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.replies?channel=CHANNEL_ID&ts=THREAD_TS" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
msgs = data.get('messages', [])
print(f'スレッド内メッセージ数: {len(msgs)}')
print('=' * 50)
for i, msg in enumerate(msgs):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    role = '親メッセージ' if i == 0 else f'返信 {i}'
    print(f'[{role}] {ts.strftime(\"%Y-%m-%d %H:%M\")}')
    print(f'User: {msg.get(\"user\", \"不明\")}')
    print(f'{msg.get(\"text\", \"\")}')
    print('-' * 50)"
```

**ポイント**:
- `conversations.replies` のレスポンスには親メッセージも含まれる（配列の先頭）
- `ts` パラメータには親メッセージの `ts`（= `thread_ts`）を指定する
- ページネーションが必要な場合は `cursor` パラメータを使用する

---

## 🚀 Step 4: DM・グループDMのメッセージ取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: DM・グループDMのメッセージ取得",
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

DM（im）とグループDM（mpim）もチャネルIDさえ分かれば同じAPIで取得できる:
```bash
# DM一覧を取得
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=im&limit=10" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : DM with user {ch.get(\"user\", \"不明\")}')"
```

```bash
# DMのメッセージを取得（DM_CHANNEL_ID を置き換え）
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=DM_CHANNEL_ID&limit=10" \
  | python3 -m json.tool
```

**必要なOAuthスコープ:**
| チャネル種別 | 読み取りスコープ | 履歴スコープ |
|-------------|-----------------|-------------|
| DM（im） | `im:read` | `im:history` |
| グループDM（mpim） | `mpim:read` | `mpim:history` |

**ポイント**: DMのチャネルIDは `D0XXXXXXX` の形式。`conversations.list` で `types=im` を指定すると取得できる。相手のユーザー名は `users.info` で解決する（Lesson 9-3 で扱う）。

---

## 🚀 Step 5: 取得結果をAIに渡して要約・タスク抽出

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: AIによる要約・タスク抽出",
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

チャネルのメッセージを取得し、AIに分析を依頼:
```bash
# メッセージを取得してファイルに保存
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=30" \
  | python3 -c "
import sys, json, datetime
data = json.load(sys.stdin)
for msg in data.get('messages', []):
    ts = datetime.datetime.fromtimestamp(float(msg['ts']))
    print(f'[{ts.strftime(\"%Y-%m-%d %H:%M\")}] {msg.get(\"user\",\"?\")} : {msg.get(\"text\",\"\")}')" \
  > ~/ai-agent-camp/data/slack_messages_latest.txt
```

保存後、AIに以下の分析を依頼:
```text
~/ai-agent-camp/data/slack_messages_latest.txt を読んで、以下を教えてください:

1. 話題のサマリー（箇条書き3-5個）
2. アクションアイテム（誰が何をすべきか）
3. 未解決の質問
4. 重要な決定事項
```

**期待される結果**: メッセージの内容がカテゴリ別に整理されて表示される。

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
      {"id": "trouble_1", "label": "channel_not_found エラーが出る"},
      {"id": "trouble_2", "label": "not_in_channel エラーが出る"},
      {"id": "trouble_3", "label": "メッセージが空で返ってくる"},
      {"id": "trouble_4", "label": "ユーザーIDを名前に変換したい"}
    ]
  }]
}
```

### トラブル1: 「channel_not_found」
**原因**: チャネルIDが間違っている、またはチャネルが削除されている
**解決方法**:
```bash
# チャネル一覧を再取得してIDを確認
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=50" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    print(f'{ch[\"id\"]} : #{ch[\"name\"]}')"
```

### トラブル2: 「not_in_channel」
**原因**: そのチャネルに参加していない
**解決方法**: Slackアプリ上でチャネルに参加するか、APIで `conversations.join` を呼ぶ。User Tokenの場合はユーザー自身がチャネルメンバーである必要がある。

### トラブル3: 「メッセージが空で返ってくる」
**原因**: `oldest` / `latest` の期間指定が狭すぎる、またはチャネルにメッセージがない
**解決方法**:
```bash
# パラメータなしで最新メッセージを取得してみる
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.history?channel=CHANNEL_ID&limit=5" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'ok: {data.get(\"ok\")}')
print(f'メッセージ数: {len(data.get(\"messages\", []))}')"
```

### トラブル4: 「ユーザーIDを名前に変換したい」
**原因**: `conversations.history` のレスポンスにはユーザーIDのみ含まれる
**解決方法**: Lesson 9-3 の `users.info` で名前解決する。急ぎの場合は以下で確認:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/users.info?user=U0XXXXXXX" \
  | python3 -c "import sys,json; u=json.load(sys.stdin)['user']; print(f'{u[\"real_name\"]} (@{u[\"name\"]})')"
```

---

## ✅ チェックポイント
- [ ] `conversations.history` でチャネルメッセージを取得できた
- [ ] メッセージの構造（ts, user, text, thread_ts）を理解した
- [ ] `conversations.replies` でスレッド返信を展開できた
- [ ] DM / グループDMのメッセージを取得できた
- [ ] 取得したメッセージをAIで要約できた

---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力とテキストファイルです。

### 期待される出力例
```text
# conversations.history の整形結果
--- 2025-04-14 10:30 ---
User: U0ABC1234
Text: 来週のリリース日程について確認です
ts: 1713075000.123456 [スレッドあり]
返信数: 3

# スレッド展開
[親メッセージ] 2025-04-14 10:30
User: U0ABC1234
来週のリリース日程について確認です
--------------------------------------------------
[返信 1] 2025-04-14 10:35
User: U0DEF5678
木曜日で調整中です
--------------------------------------------------
```

---

## ➡️ 次のステップ

これでメッセージとスレッドの取得ができるようになりました。次のレッスンではメッセージの送信とユーザー情報の取得を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-9-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-9-3
- finish → 終了
