---
description: "Lesson command — Discord Bot + claude-channel-discord MCP セットアップ"
duration: "約30分"
prerequisites: ["Discord アカウント", "Bun または Node.js 18+"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "discord", "mcp", "module-22"]
---

# /setup-discord -- Discord Bot + claude-channel-discord MCP セットアップ

## このセッションでやること

| 項目 | 内容 |
|------|------|
| ゴール | Discord Developer Portal で Bot を作成し、Claude Code から `claude-channel-discord` MCP 経由で操作できる状態にする |
| 所要時間 | 約 30 分（うち手動ブラウザ操作 5 分、CLI 5 分、待ち時間 5 分） |
| 前提 | Discord アカウント / Bun または Node.js 18+ / 自分のサーバー（Bot 招待先） |
| つながる先 | aiagent-course Module 22 のスライド内容と一致 |

> **非対話モードでの注意**: ブラウザ操作と Bot トークンの貼り付けが必須なので、`claude -p` / `cursor-agent --print` 単独での完走はできません。`nonInteractiveMode: deferred` 宣言により、-p 実行時はチェックリストだけ生成して停止します。

---

## Step 0: 進捗と既存設定の確認

**AI が裏で実行する内容:**

1. `~/.claude/mcp_settings.json` または `<project>/.mcp.json` に `discord` エントリがあるか確認
2. `bunx claude-channel-discord@0.0.4 --version` または `npx claude-channel-discord@0.0.4 --version` でインストール状況を確認
3. macOS Keychain に `DISCORD_BOT_TOKEN` が登録されているか `security find-generic-password -s DISCORD_BOT_TOKEN 2>&1 | head -3` で確認（値は表示しない）

すべて揃っているなら **Step 5（接続テスト）にスキップ**。

---

## Step 1: Discord Developer Portal で Bot を作成

ブラウザで <https://discord.com/developers/applications> を開く（AI が `open` で代行可）。

1. 右上の **New Application** をクリック → アプリ名（例: `AI Agent Camp Demo`）→ **Create**
2. 左サイドバー **Bot** → **Reset Token** → 出てきたトークンを **すぐコピーして安全な場所に保存**（再表示不可）
3. **Privileged Gateway Intents** で次の 2 つを ON:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`

> ⚠️ INTENT を ON にしないと Bot がメッセージ本文を読めません。

---

## Step 2: Bot をサーバーに招待

1. 左サイドバー **OAuth2** → **URL Generator**
2. **Scopes**: `bot`、`applications.commands` をチェック
3. **Bot Permissions** で必要なものを選択（最小: Read Messages / Send Messages / Add Reactions / Manage Messages）
4. 出てきた URL をブラウザで開いて、自分のサーバーに招待

---

## Step 3: Bot トークンを Keychain に保存

```bash
security add-generic-password -a "$USER" -s DISCORD_BOT_TOKEN -w '<paste-token>'
```

シェル起動時に自動で読み込ませるため、`.zshrc` / `.bashrc` に以下を追記:

```bash
export DISCORD_BOT_TOKEN="$(security find-generic-password -s DISCORD_BOT_TOKEN -w 2>/dev/null)"
```

> ⚠️ Token を `.env` に書く場合は `.gitignore` に必ず登録してから。`chmod 600 ~/.env` も推奨。

---

## Step 4: claude-channel-discord MCP を Claude Code に追加

```bash
# Bun 推奨
bun install -g claude-channel-discord@0.0.4

# Claude Code への登録
claude mcp add --transport stdio discord -- bun x claude-channel-discord@0.0.4

# 接続確認
claude mcp list
```

`discord (stdio): bun x claude-channel-discord ... ✓ connected` が出れば OK。

`.mcp.json` を直接書く場合（プロジェクトローカル）:

```json
{
  "mcpServers": {
    "discord": {
      "type": "stdio",
      "command": "bun",
      "args": ["x", "claude-channel-discord"],
      "env": {
        "DISCORD_BOT_TOKEN": "${DISCORD_BOT_TOKEN}"
      }
    }
  }
}
```

---

## Step 5: アクセスポリシーをロックダウン

```bash
/discord:access set --dm-policy allowlist
/discord:access approve <your-discord-user-id>
/discord:access list
```

> `dmPolicy: allowlist` にしないと未許可ユーザーから DM が届く。本番運用では必ず allowlist に。

---

## Step 6: 接続テスト

Claude Code から:

```
> Discord で自分宛に「Hello from MCP」とDMして
```

Bot からの DM が届けば成功。

---

## つまずきポイント（aiagent-course Module 22 と同じ）

| 症状 | 原因 | 対処 |
|---|---|---|
| Bot トークンが効かない | Token Reset 後に古い値を使っている | 再度 Reset → 新しい値を Keychain に上書き |
| メッセージが読めない | `MESSAGE CONTENT INTENT` 未 ON | Developer Portal で ON にして MCP を再接続 |
| 他人同士の DM を読みたい | Discord API 仕様で不可能 | Pattern A（プライベート Ticket チャンネル）に切り替え |
| 未送信ユーザーへ DM できない | DM チャンネル作成不可 | 共通サーバー経由でメンション → 相手から先制 DM をもらう |

---

## 非対話モード（claude -p / cursor-agent --print）での挙動

このコマンドは `nonInteractiveMode: deferred` です。

- Step 0 の read-only チェックは実行する
- Step 1〜2 のブラウザ操作、Step 3 の Token 貼り付けは実行できないため、`setup-resume.md` を生成して停止する
- 対話モードに戻ってから `/setup-discord` を再実行してください

`setup-resume.md` のフォーマットは `_lib/non-interactive.md` 参照。

---

## 関連

- スライド本体: aiagent-course Module 22
- claude-channel-discord: <https://www.npmjs.com/package/claude-channel-discord>
- Module 23 (LINE) との比較: `/setup-line-harness`
