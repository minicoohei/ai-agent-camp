---
description: "Lesson command — Salesforce CLI (sf) セットアップ"
duration: "約15分"
prerequisites: ["Salesforce CLI (sf) アカウント"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-24"]
---

# /setup-salesforce -- Salesforce CLI (sf) セットアップ

> Salesforce 組織を CLI から触る `sf` コマンド。Connected App は不要、ブラウザ OAuth で完結。

**ハイライト**: Connected App 不要・ブラウザ OAuth のみ

## セットアップ手順

1. Salesforce CLI を pin install (npm 推奨) — `npm install -g @salesforce/cli@2.x`

2. Production 組織にログイン — `sf org login web --alias prod`

3. Sandbox の場合 — `sf org login web --alias dev --instance-url https://test.salesforce.com`

4. 接続確認 — `sf org list`

## つまずきポイント

- `sf` v1 (`sfdx`) と v2 (`sf`) はコマンド体系が異なる。v2 を使うこと
- Sandbox は `--instance-url https://test.salesforce.com` を必ず付ける

## 非対話モード

ブラウザ OAuth が必須なので `claude -p` / `cursor-agent --print` では完走できません。対話モードで実行してください。

## 関連スライド

- aiagent-course Module 24: see slide deck for the full visual walkthrough
