---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module25-google-ads"
duration: "約60分"
prerequisites: ["start-24-1"]
level: "intermediate"
tags: ["google-ads", "ads", "gaql", "oauth"]
nonInteractiveMode: incompatible
---
# Lesson 25-1: Google Ads 連携 入門

## このセッションでやること

**Google Ads API** を AI エージェントから安全に扱うために、アカウント階層、Developer Token / OAuth、読み取り系 API、dry-run を前提にした変更設計を学びます。

## 前提条件

- Google Ads アカウント、GCP プロジェクト、Python 環境を用意できること
- `/setup-google-ads` で MCC、Developer Token、OAuth、5つの秘密情報、dry-run 接続確認まで進めること
- ブラウザでの OAuth 承認が必要なため、非対話モードでは完走できないこと

## ゴール

1. Google Ads の MCC、アカウント、キャンペーン、広告グループ、キーワード/広告の階層を理解する
2. Developer Token、OAuth Client、refresh_token、LOGIN_CUSTOMER_ID の役割を確認する
3. キャンペーン一覧や GAQL レポートなど、読み取り系 API から始める流れを理解する
4. dry-run、PAUSED 作成、JSON ログ、確認ゲートで安全に変更系 API を扱う考え方を整理する

## 関連ページ

- 教材ページ: [Module 25](https://ai-agent.camp/ja/course/module-25?slideId=module-overview)
