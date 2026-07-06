---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module22-discord"
duration: "約60分"
prerequisites: ["start-21-1", "setup-discord"]
level: "intermediate"
tags: ["discord", "bot", "channels", "plugin"]
nonInteractiveMode: incompatible
---
# Lesson 22-1: Discord 連携 入門

## このセッションでやること

**Discord Bot** と **Claude Code Channels の公式 discord plugin** を組み合わせ、Claude Code から Discord のチャンネル/DM を安全に読み書きする構成を学びます。

## 前提条件

- Discord アカウントと Bot を招待できる自分のサーバーを用意できること
- Claude Code を対話モードで起動できること
- `/setup-discord` を先に実行し、公式 plugin のインストールと `--channels` 起動手順を確認していること

## ゴール

1. Discord Developer Portal で Bot を作成し、MESSAGE CONTENT INTENT を有効化する流れを説明できる
2. `/plugin install discord@claude-plugins-official` から `claude --channels plugin:discord@claude-plugins-official` までの公式フローを確認する
3. `/discord:configure`、ローカル環境変数、allowlist で token とアクセス制御を安全に扱える
4. Bot ができること/できないことを理解し、顧客別チャンネル方式と Bot ハブ方式を選び分ける

## 関連ページ

- 教材ページ: [Module 22](https://ai-agent.camp/ja/course/module-22?slideId=module-overview)

## 次のステップ

次は `/start-23-1` で LINE 公式アカウント運用に進みます。
