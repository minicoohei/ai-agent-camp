---
description: "Lesson command — Google Ads API セットアップ"
duration: "約180分（API Center 承認待ちが大半）"
prerequisites: ["Google Ads API アカウント"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-25"]
---

# /setup-google-ads -- Google Ads API セットアップ

> Google Ads API v21 (Python SDK) を叩くまでの 3 日間 journey。MCC + Basic Access + OAuth refresh_token が必要。

**ハイライト**: Basic Access 承認に最大 1 営業日。OAuth は web flow が必須

## セットアップ手順

1. Google Ads Manager Account (MCC) を作成

   ```bash
   https://ads.google.com/aw/signup/manager
   ```

2. API Center で Developer Token をリクエスト — `MCC → Tools → API Center → Apply for Basic Access`

3. GCP プロジェクトと OAuth Client (web) を作成

   ```bash
   https://console.cloud.google.com/apis/credentials
   ```

4. refresh_token を取得 (web flow ローカル受信) — `# Google OAuth Playground または `gcloud auth application-default login` で refresh_token を発行（手元の OAuth ヘルパーがあればそれでも可）`

5. Keychain と GitHub Secrets に 5 つの値を保存 — `GOOGLE_ADS_DEVELOPER_TOKEN / CLIENT_ID / CLIENT_SECRET / REFRESH_TOKEN / LOGIN_CUSTOMER_ID`

6. Python SDK で疎通確認 (validate_only=True dry-run) — `python -c "from google.ads.googleads.client import GoogleAdsClient; print('SDK loaded ok')"  # dry-run は次のレッスンで詳しく`

## つまずきポイント

- Test Account からは課金広告は配信できない。Basic Access 承認後は本番アカウントを使う
- EU political advertising ステータスを campaign_operation に必須でセット (`DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`)
- validate_only=True の dry-run でも `mutate` の atomic batch（budget+campaign with temp resource_name `-1`）にしないと resource_name 存在チェックで弾かれる

## 非対話モード

ブラウザ OAuth が必須なので `claude -p` / `cursor-agent --print` では完走できません。対話モードで実行してください。

## 関連スライド

- aiagent-course Module 25: see slide deck for the full visual walkthrough
