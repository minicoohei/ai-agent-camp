---
description: "Lesson command — Freee MCP セットアップ"
duration: "約30分"
prerequisites: ["Freee MCP アカウント"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-20"]
---

# /setup-freee -- Freee MCP セットアップ

> freee 会計に MCP 経由で接続。ブラウザ OAuth + Client ID/Secret が必要。

**ハイライト**: Freee Developer App + OAuth ブラウザログイン必須

## セットアップ手順

1. freee Developer Portal でアプリ作成

   ```bash
   https://app.secure.freee.co.jp/developers/applications
   ```

2. Client ID / Client Secret を控える — `（Web ブラウザのみ）`

3. freee-mcp を pin install — `npm install -g freee-mcp@0.26.0`

4. Claude Code に MCP 登録 — `claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0`

5. OAuth ブラウザフローで認可 — `claude mcp の指示に従う`

## つまずきポイント

- 事業所 ID は `freee_get_companies` で取得 → `~/.config/freee-mcp/config.json` に保存
- Sandbox / 本番アプリは別物。Sandbox で試してから本番アプリに切り替え

## 非対話モード

ブラウザ OAuth が必須なので `claude -p` / `cursor-agent --print` では完走できません。対話モードで実行してください。

## 関連スライド

- aiagent-course Module 20: see slide deck for the full visual walkthrough
