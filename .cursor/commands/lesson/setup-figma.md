---
description: "Lesson command — Figma + Serendie デザインシステム MCP セットアップ"
duration: "約20分"
prerequisites: ["Figma + Serendie MCP アカウント"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-21"]
---

# /setup-figma -- Figma + Serendie デザインシステム MCP セットアップ

> Figma 公式プラグイン（書き込み担当）と Serendie MCP（知識担当）の 2 つを接続。

**ハイライト**: PAT 不要・OAuth ブラウザログインで完結

## セットアップ手順

1. Claude Code に Figma プラグインを導入 — `/plugin install figma@claude-plugins-official`

2. OAuth で Figma にログイン — `/mcp → figma → Authenticate → ブラウザで Allow Access`

3. Serendie MCP を追加 — `claude mcp add --transport http serendie-mcp https://serendie.design/mcp`

4. 動作確認 — `claude mcp list`

5. Serendie UI Kit を Figma の自分のチームに取り込み

   ```bash
   https://www.figma.com/community/file/1433690846108785966
   ```

## つまずきポイント

- Serendie UI Kit を Community からチームに移動しないと「ライブラリを公開」できない
- Figma OAuth は組織アカウントの場合、管理者が App 利用許可を出す必要あり

## 非対話モード

ブラウザ OAuth が必須なので `claude -p` / `cursor-agent --print` では完走できません。対話モードで実行してください。

## 関連スライド

- aiagent-course Module 21: see slide deck for the full visual walkthrough
