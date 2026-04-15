---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
duration: "約25分"
prerequisites: ["start-0-4"]
level: "beginner"
tags: ["slack", "api", "token", "channel"]
---

# 🎓 Lesson 9-1: User Access Token設定・チャネル取得

## 📍 このセッションでやること

**Lesson 9-1: Slack API — トークン確認とチャネル取得** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | User Access Tokenの動作確認、conversations.list / conversations.info でチャネル情報を取得する |
| 所要時間 | 約25分 |
| 使うスキル | curl, Slack Web API, credential_manager |
| 前提条件 | Slack API設定済み（Lesson 0-4: setup-slack） |
| 教材ページ | [Module 9: Slack](https://ai-agent.camp/ja/course/module-9) を並行参照 |

**このセッションの流れ:**
1. User Access Token の確認と接続テスト
2. `conversations.list` で公開チャネル一覧を取得
3. プライベートチャネル・DM・グループDMを含めた全種類取得
4. `conversations.info` で特定チャネルの詳細を取得
5. 複数ワークスペース管理パターンの紹介

セッション終了時には、Slack APIを直接呼び出してチャネル情報を自在に取得できるようになっています。

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

(ready → Step 1へ)
(check_prereq → `uv run python tools/credential_manager.py status` を実行して SLACK_USER_TOKEN の有無を確認。未設定なら `/setup-slack` を案内)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: User Access Token の確認と接続テスト

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: User Access Token の確認と接続テスト",
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

1. credential_manager からトークンを取得して環境変数にセット:
```bash
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN)
```

2. `auth.test` で接続テスト:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/auth.test" \
  | python3 -m json.tool
```

**期待される結果**:
```json
{
    "ok": true,
    "url": "https://your-workspace.slack.com/",
    "team": "Your Workspace",
    "user": "your.name",
    "team_id": "T0XXXXXXX",
    "user_id": "U0XXXXXXX"
}
```

**ポイント**: `ok: true` が返れば接続成功。`user` と `team` で正しいアカウントか確認する。

---

## 🚀 Step 2: conversations.list で公開チャネル一覧を取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 公開チャネル一覧の取得",
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

公開チャネル一覧を取得:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=20" \
  | python3 -m json.tool
```

**期待される結果**: `channels` 配列にチャネル情報が返る。

主要なフィールド:
| フィールド | 説明 |
|-----------|------|
| `id` | チャネルID（C0XXXXXXXの形式） |
| `name` | チャネル名 |
| `is_channel` | 公開チャネルかどうか |
| `num_members` | メンバー数 |
| `purpose.value` | チャネルの説明 |

**必要なOAuthスコープ**: `channels:read`

---

## 🚀 Step 3: 全種類のチャネルを取得（private_channel, mpim, im）

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 全種類のチャネル取得",
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

`types` パラメータにカンマ区切りで全種類を指定:
```bash
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel,private_channel,mpim,im&limit=50" \
  | python3 -m json.tool
```

**チャネル種別の見分け方:**
| types値 | 判定フィールド | 必要なスコープ |
|---------|--------------|---------------|
| `public_channel` | `is_channel: true` | `channels:read` |
| `private_channel` | `is_group: true` | `groups:read` |
| `mpim` | `is_mpim: true` | `mpim:read` |
| `im` | `is_im: true` | `im:read` |

**ポイント**: DMチャネル（`im`）は `user` フィールドに相手のユーザーIDが入る。名前は表示されないので、`users.info` で名前解決が必要になる（Lesson 9-3 で扱う）。

---

## 🚀 Step 4: conversations.info で特定チャネルの詳細を取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 特定チャネルの詳細取得",
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

Step 2/3 で取得したチャネルIDを使って詳細を取得:
```bash
# CHANNEL_ID を実際のIDに置き換える
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.info?channel=CHANNEL_ID" \
  | python3 -m json.tool
```

**期待される結果**: `channel` オブジェクトに詳細情報が返る。

追加で得られるフィールド:
| フィールド | 説明 |
|-----------|------|
| `topic.value` | チャネルのトピック |
| `purpose.value` | チャネルの目的 |
| `created` | 作成日時（Unixタイムスタンプ） |
| `creator` | 作成者のユーザーID |
| `is_member` | 自分がメンバーかどうか |
| `num_members` | メンバー数 |

**ポイント**: `is_member: false` のチャネルは `conversations.history` でメッセージを取得できない。先に `conversations.join` で参加する必要がある。

---

## 🚀 Step 5: 複数ワークスペース管理

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 複数ワークスペース管理",
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

**practice / review の場合 — 複数ワークスペースの管理方法:**

複数のSlackワークスペースを使い分ける場合、トークンを `SLACK_USER_TOKEN_チーム名` の命名規則で管理する:

```bash
# チームごとにトークンを保存
uv run python tools/credential_manager.py store SLACK_USER_TOKEN_MYCOMPANY
uv run python tools/credential_manager.py store SLACK_USER_TOKEN_SIDEJOB

# 使いたいワークスペースのトークンを取得
export SLACK_USER_TOKEN=$(uv run python tools/credential_manager.py get SLACK_USER_TOKEN_MYCOMPANY)

# 接続テスト（どのワークスペースに繋がっているか確認）
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/auth.test" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Team: {d[\"team\"]} / User: {d[\"user\"]}')"
```

**ポイント**: ワークスペースを切り替えるときは `auth.test` で接続先を必ず確認する。誤ったワークスペースにメッセージを送信する事故を防げる。

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
      {"id": "trouble_1", "label": "auth.test で not_authed / invalid_auth が返る"},
      {"id": "trouble_2", "label": "conversations.list で missing_scope エラー"},
      {"id": "trouble_3", "label": "プライベートチャネルが取得できない"},
      {"id": "trouble_4", "label": "ページネーションで全件取得したい"}
    ]
  }]
}
```

### トラブル1: 「not_authed / invalid_auth」
**原因**: トークンが未設定、または無効
**解決方法**:
```bash
# トークンの存在確認
uv run python tools/credential_manager.py status | grep SLACK

# トークンが無い場合は再設定
uv run python tools/credential_manager.py store SLACK_USER_TOKEN
# プロンプトに xoxp- で始まるトークンを貼り付ける
```

### トラブル2: 「missing_scope」
**原因**: Slack Appに必要なOAuth Scopeが設定されていない
**解決方法**:
1. https://api.slack.com/apps でアプリを開く
2. OAuth & Permissions → User Token Scopes に不足スコープを追加
3. ワークスペースに再インストール（トークンが再発行される）
4. 新しいトークンを `credential_manager.py store SLACK_USER_TOKEN` で再保存

### トラブル3: 「プライベートチャネルが取得できない」
**原因**: `groups:read` スコープ未設定、またはチャネルに参加していない
**解決方法**:
```bash
# private_channel で呼んでエラー内容を確認
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=private_channel&limit=5" \
  | python3 -m json.tool
```

### トラブル4: 「ページネーションで全件取得したい」
**原因**: `limit` のデフォルトは100件、ワークスペースにそれ以上のチャネルがある
**解決方法**:
```bash
# レスポンスの response_metadata.next_cursor を使って次ページを取得
curl -s -H "Authorization: Bearer $SLACK_USER_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=100&cursor=NEXT_CURSOR_VALUE" \
  | python3 -m json.tool
```

---

## ✅ チェックポイント
- [ ] `auth.test` でトークンの動作を確認できた
- [ ] `conversations.list` で公開チャネル一覧を取得できた
- [ ] `types` パラメータで全種類のチャネルを取得できた
- [ ] `conversations.info` で特定チャネルの詳細を取得できた
- [ ] 複数ワークスペース管理の方法を理解した

---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```
# auth.test の結果
Team: MyCompany / User: taro.yamada

# conversations.list の結果（チャネル名一覧）
- #general (52 members)
- #random (48 members)
- #project-alpha (12 members)
- #dev-team (8 members, private)
```

---

## ➡️ 次のステップ

これでSlack APIへの接続とチャネル取得ができるようになりました。次のレッスンではメッセージとスレッドの取得を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-9-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-9-2
- finish → 終了
