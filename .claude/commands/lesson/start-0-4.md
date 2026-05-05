---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch03-api-settings"
duration: "約15分"
prerequisites: ["start-0-1", "start-0-2", "start-0-3"]
level: "beginner"
tags: ["setup", "slack", "api"]
nonInteractiveMode: deferred
---
# Lesson 0-4: Slack API設定

## セットアップ進捗の確認

**AIが自動実行:** `uv run python tools/setup_progress.py show` を実行して現在のセットアップ進捗を表示する。

---

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Slack App を作成し、Bot Token を取得して .env に設定し、Slack 連携機能を使えるようにする |
| 所要時間 | 約15分 |
| 前提条件 | Lesson 0-1〜Lesson 0-3 完了、Slack ワークスペースの管理者権限（または App 作成権限） |
| 教材ページ | [コース教材トップ](https://ai-agent.camp/ja/course/module-0) を並行参照 |

> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

---

## Slack APIの自動セットアップ

このレッスンでは `/setup-slack` を実行するだけで完了します。
**ターミナルの操作は一切不要です。全てAIが自動で実行します。**
もしAIが「ターミナルで実行してください」と案内した場合は [ターミナル入門ガイド](../../../docs/terminal-guide.md) を参照してください。

### AIが自動で行うこと

1. ブラウザで Slack App 管理画面を自動起動
2. Slack App の作成手順をステップバイステップで案内
3. Bot Token Scopes（channels:history, channels:read, chat:write, users:read）の設定を案内
4. ワークスペースへのインストールとトークン取得を案内
5. `.env` ファイルにトークン行を自動追加
6. ユーザーが `.env` ファイルにトークンを直接入力
7. Slack API へのテストリクエストを自動実行して動作確認

**重要**: トークンはチャットに貼り付けないでください。以下のコマンドで安全に保存できます。

```bash
uv run python tools/credential_manager.py store SLACK_BOT_TOKEN
```

実行するとパスワード入力プロンプトが表示されます。入力した値は画面に表示されず、OS の Credential Store（macOS Keychain 等）に安全に保存されます。

> **補足**: `.env` ファイルへの直接書き込みも可能ですが、Claude Code ではセキュリティガード（write_guard）によりブロックされる場合があります。`credential_manager.py` を使う方法が最も安全で確実です。

**AskQuestionの設定:**
```json
{
  "title": "Slack API セットアップ",
  "questions": [{
    "id": "action",
    "prompt": "Slack APIの設定を始めますか？",
    "options": [
      {"id": "run", "label": "セットアップを開始する（/setup-slack を実行）"},
      {"id": "already_done", "label": "既にSlack APIを設定済み"},
      {"id": "no_slack", "label": "Slackワークスペースを持っていない"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(run → `/setup-slack` の内容を実行する)
(already_done → チェックポイントへ)
(no_slack → 「Slackは無料で作成できます。https://slack.com/create からテスト用ワークスペースを作成してから、このセットアップを再開してください」と案内)
(different_lesson → モジュール一覧を表示)

---

## 実行コマンド

```text
/setup-slack
```

## 期待される出力例

```text
Slack API テスト結果:
接続: 正常
ワークスペース: your-workspace
Bot名: AIAgent Bootcamp
```

## よくあるトラブル
- ブラウザが開かない → `https://api.slack.com/apps` を手動で開く
- `not_authed` エラー → トークンが正しくコピーされているか .env を確認
- `missing_scope` エラー → Slack管理画面でスコープ追加後「Reinstall to Workspace」を実行

---

## チェックポイント
- [ ] Slack App「AIAgent Bootcamp」を作成した
- [ ] 必要な Bot Token Scopes を設定した
- [ ] ワークスペースに App をインストールした
- [ ] .env ファイルに SLACK_BOT_TOKEN が設定されている
- [ ] API テストが成功した

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next", "label": "セキュリティ設定をする（/start-0-5）"},
      {"id": "try_slack", "label": "Slack検索を試してみる（/start-6-1）"},
      {"id": "check", "label": "環境チェックをする（/check-setup）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(next → /start-0-5 を案内)
(try_slack → /start-6-1 を案内)
(check → /check-setup の内容を実行する)
(finish → 終了)
