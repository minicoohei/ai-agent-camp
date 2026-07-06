---
description: "Lesson command — Discord Bot + Claude Code Channels 公式 plugin セットアップ"
duration: "約30分"
prerequisites: ["Discord アカウント", "Claude Code", "Bun"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "plugin", "module-22"]
---

# /setup-discord -- Discord Bot + Claude Code Channels 公式 plugin セットアップ

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Discord Developer Portal で Bot を作成し、Claude Code 公式 Discord plugin を Channels として起動できる状態にする |
| 所要時間 | 約 30 分（うち手動ブラウザ操作 5 分、Claude Code 設定 5 分、待ち時間 5 分） |
| 前提 | Discord アカウント / Claude Code / Bun / 自分のサーバー（Bot 招待先） |
| つながる先 | aiagent-course Module 22 のスライド内容と一致 |

> **非対話モードでの注意**: ブラウザ操作と Bot トークンの貼り付け、Claude Code 内の plugin コマンド実行が必須です。`claude -p` / `cursor-agent --print` 単独では完走できません。`nonInteractiveMode: deferred` 宣言により、-p 実行時はチェックリストだけ生成して停止します。

---

## Step 0: 進捗と既存設定の確認

**AI が裏で確認する内容:**

1. Claude Code で `discord@claude-plugins-official` plugin がインストール済みか確認する手順を案内
2. `~/.claude/channels/discord/.env` に `DISCORD_BOT_TOKEN` があるか確認（値は表示しない）
3. Discord access 設定は Claude Code 内で `/discord:access` を実行して確認するよう案内

すべて揃っているなら **Step 6（接続テスト）にスキップ**。

---

## Step 1: Discord Developer Portal で Bot を作成

ブラウザで <https://discord.com/developers/applications> を開く（AI が `open` で代行可）。

1. 右上の **New Application** をクリック → アプリ名（例: `AI Agent Camp Demo`）→ **Create**
2. 左サイドバー **Bot** → **Reset Token** → 出てきたトークンをすぐコピーして安全な場所に保存（再表示不可）
3. **Privileged Gateway Intents** で `MESSAGE CONTENT INTENT` だけを ON

> MESSAGE CONTENT INTENT を ON にしないと Bot がメッセージ本文を読めません。

---

## Step 2: Bot をサーバーに招待

1. 左サイドバー **OAuth2** → **URL Generator**
2. **Scopes**: `bot` をチェック
3. **Bot Permissions** で最小権限を選択:
   - `View Channels`
   - `Send Messages`
   - `Send Messages in Threads`
   - `Read Message History`
   - `Attach Files`
4. **Integration type** は **Guild Install** を選ぶ
5. 出てきた URL をブラウザで開いて、自分のサーバーに招待

---

## Step 3: 公式 Discord plugin をインストール

Claude Code を起動して、Claude Code 内で次を実行:

```text
/plugin install discord@claude-plugins-official
/reload-plugins
```

plugin を再読み込みしたら、同じ Claude Code セッションで Bot トークンを設定:

```text
/discord:configure <paste-bot-token>
```

この設定は `~/.claude/channels/discord/.env` に `DISCORD_BOT_TOKEN` を保存します。トークン値をチャットやログに貼らないでください。

---

## Step 4: Channels として Claude Code を起動

いったん Claude Code を終了し、ターミナルから次で起動:

```bash
claude --channels plugin:discord@claude-plugins-official
```

通常の MCP 登録では Discord channel は起動しません。必ず `--channels plugin:discord@claude-plugins-official` で起動してください。

---

## Step 5: アクセス制御を設定

最初の DM は pairing でユーザー ID を捕捉します。Claude Code を Step 4 の起動方法で開いたまま、Discord から Bot に DM してください。Bot が 6 文字の pairing code を返したら、Claude Code 内で次を実行:

```text
/discord:access pair <code>
/discord:access policy allowlist
/discord:access
```

ユーザー ID（snowflake）が分かっている場合は、手動で allowlist に追加できます。

```text
/discord:access allow <snowflake>
/discord:access
```

> 本番運用では、必要なユーザーを追加した後に `allowlist` にしておくと、未知の DM に pairing code を返しません。

---

## Step 6: 接続テスト

Claude Code を次の起動方法で実行中に:

```bash
claude --channels plugin:discord@claude-plugins-official
```

Discord から Bot に DM して、Claude Code 側に通知が届き、Bot が返信できることを確認します。反応がない場合は `/discord:access` で allowlist と pending pairings を確認してください。

---

## つまずきポイント（aiagent-course Module 22 と同じ）

| 症状 | 原因 | 対処 |
|---|---|---|
| Bot トークンが効かない | Token Reset 後に古い値を使っている | 再度 Reset → `/discord:configure <paste-bot-token>` で更新 |
| メッセージが読めない | `MESSAGE CONTENT INTENT` 未 ON | Developer Portal で ON にして `--channels` 付きで再起動 |
| Bot が DM に反応しない | `--channels` なしで Claude Code を起動している | `claude --channels plugin:discord@claude-plugins-official` で起動 |
| 未許可ユーザーの扱いが分からない | access policy / allowlist 未確認 | `/discord:access` で状態を確認し、必要なら `pair` または `allow` を実行 |

---

## 非対話モード（claude -p / cursor-agent --print）での挙動

このコマンドは `nonInteractiveMode: deferred` です。

- Step 0 の read-only チェックは実行する
- Step 1〜3 のブラウザ操作、Token 貼り付け、Claude Code 内 plugin コマンドは実行できないため、`setup-resume.md` を生成して停止する
- 対話モードに戻ってから `/setup-discord` を再実行してください

`setup-resume.md` のフォーマットは `_lib/non-interactive.md` 参照。

---

## 関連

- スライド本体: aiagent-course Module 22
- Claude Code Discord plugin README: <https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord>
- Claude Code Discord access guide: <https://github.com/anthropics/claude-plugins-official/blob/main/external_plugins/discord/ACCESS.md>
- Module 23 (LINE) との比較: `/setup-line-harness`
