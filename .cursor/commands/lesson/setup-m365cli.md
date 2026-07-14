---
description: "Lesson command — M365 CLI セットアップ"
duration: "約20分"
prerequisites: ["Microsoft 365 CLI (PnP CLI) アカウント"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "module-19"]
---

# /setup-m365cli -- M365 CLI セットアップ

> Microsoft 365 (Outlook / SharePoint / Teams) を CLI からまとめて触る `@pnp/cli-microsoft365`。デバイスコード認証だけで完結します。

**ハイライト**: PAT 不要・OAuth デバイスコードのみ

## セットアップ手順

1. Node.js 18+ を確認 — `node -v`

2. @pnp/cli-microsoft365 を pin install — `npm install -g @pnp/cli-microsoft365@7.x`

3. デバイスコードでログイン

   ```bash
   m365 login
# 出力された URL をブラウザで開いてコードを入力
   ```

4. 接続確認 — `m365 status`

## つまずきポイント

- ログインしたままにするには `m365 logout` を実行しないこと（Token 失効まで保持）
- WSL 環境では `m365 login` 出力 URL を Windows ブラウザで開く必要あり（自動 open は呼ばない）

## 非対話モード

ブラウザ操作と入力が必要なので、`claude -p` 実行時は読み取り系チェックのみ実施し、`setup-resume.md` を生成して終了します。

## 関連スライド

- aiagent-course Module 19: see slide deck for the full visual walkthrough
