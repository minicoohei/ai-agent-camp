# Module 9: GitHub Actions 成果物（Final）

GitHub Actionsを使用したCI/CD、Gmail通知、Slack通知の実装例です。

## 成果物一覧

| ファイル | 説明 |
|---------|------|
| `gmail-notification.yml` | Gmail通知ワークフロー |
| `slack-notification.yml` | Slack通知ワークフロー |
| `ci-with-notifications.yml` | Gmail/Slack統合CI/CDワークフロー |

## セットアップ手順

### 1. Gmail通知の設定

#### 1-1. Gmailアプリパスワードの取得

1. [Googleアカウント](https://myaccount.google.com/) にアクセス
2. 「セキュリティ」→「2段階認証」を有効化（必須）
3. 「セキュリティ」→「アプリパスワード」
4. アプリを選択 →「その他」→「GitHub Actions」と入力
5. 生成された16文字のパスワードをコピー

#### 1-2. GitHub Secretsの設定

リポジトリの Settings → Secrets and variables → Actions で以下を追加:

| Secret名 | 値 |
|----------|-----|
| `GMAIL_ADDRESS` | 送信元Gmailアドレス（例: `your-email@gmail.com`） |
| `GMAIL_APP_PASSWORD` | 上記で取得した16文字のアプリパスワード |
| `NOTIFY_EMAIL` | 通知先メールアドレス |

### 2. Slack通知の設定

#### 2-1. Slack Incoming Webhookの作成

1. [Slack API](https://api.slack.com/apps) にアクセス
2. 「Create New App」→「From scratch」
3. App名とワークスペースを選択
4. 「Incoming Webhooks」を有効化
5. 「Add New Webhook to Workspace」
6. 投稿先チャンネルを選択
7. Webhook URLをコピー

#### 2-2. GitHub Secretsの設定

| Secret名 | 値 |
|----------|-----|
| `SLACK_WEBHOOK_URL` | コピーしたWebhook URL |

### 3. ワークフローファイルの配置

```bash
# リポジトリのルートで実行
mkdir -p .github/workflows

# ワークフローファイルをコピー
cp output/final/module-09-actions/*.yml .github/workflows/
```

## 使用方法

### Gmail通知の手動テスト

```bash
# GitHub CLIを使用
gh workflow run gmail-notification.yml \
  -f subject="テスト通知" \
  -f body="これはテストメールです"
```

### Slack通知の手動テスト

```bash
gh workflow run slack-notification.yml \
  -f message="テスト通知です" \
  -f status="info"
```

### CI/CDワークフローの有効化

`ci-with-notifications.yml` はプッシュ時に自動実行されます。

```yaml
# 手動実行も可能
gh workflow run ci-with-notifications.yml
```

## ワークフロー詳細

### gmail-notification.yml

```
┌─────────────────────────────────────────────────────────┐
│                   Gmail Notification                     │
├─────────────────────────────────────────────────────────┤
│ トリガー:                                                │
│   - workflow_call（他のワークフローから呼び出し）         │
│   - workflow_dispatch（手動実行）                        │
│   - schedule（毎日9時JST）                               │
├─────────────────────────────────────────────────────────┤
│ 機能:                                                    │
│   - CI/CD結果のメール通知                                │
│   - 日次レポートの自動送信                               │
│   - HTML形式のリッチなメール                             │
└─────────────────────────────────────────────────────────┘
```

### slack-notification.yml

```
┌─────────────────────────────────────────────────────────┐
│                   Slack Notification                     │
├─────────────────────────────────────────────────────────┤
│ トリガー:                                                │
│   - workflow_call（他のワークフローから呼び出し）         │
│   - workflow_dispatch（手動実行）                        │
│   - push（main/developブランチ）                        │
│   - pull_request（マージ時）                            │
├─────────────────────────────────────────────────────────┤
│ 機能:                                                    │
│   - Block Kit形式のリッチな通知                          │
│   - ステータス別の色分け（success/failure/warning）      │
│   - アクションボタン付き                                 │
│   - メンション対応（@channel, @here）                    │
└─────────────────────────────────────────────────────────┘
```

### ci-with-notifications.yml

```
┌─────────────────────────────────────────────────────────┐
│               CI/CD with Notifications                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│   │  Build   │───▶│   Test   │───▶│  Deploy  │        │
│   └──────────┘    └──────────┘    └──────────┘        │
│        │               │               │               │
│        ▼               ▼               ▼               │
│   ┌─────────────────────────────────────────┐         │
│   │          成功/失敗を判定               │         │
│   └─────────────────────────────────────────┘         │
│        │                                    │          │
│        ▼                                    ▼          │
│   ┌──────────┐                      ┌──────────┐      │
│   │  Slack   │                      │  Gmail   │      │
│   │  通知    │                      │  通知    │      │
│   └──────────┘                      └──────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## カスタマイズ例

### 通知先チャンネルを環境ごとに変更

```yaml
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Set channel based on branch
        id: channel
        run: |
          if [ "${{ github.ref_name }}" = "main" ]; then
            echo "webhook=${{ secrets.SLACK_WEBHOOK_PROD }}" >> $GITHUB_OUTPUT
          else
            echo "webhook=${{ secrets.SLACK_WEBHOOK_DEV }}" >> $GITHUB_OUTPUT
          fi
      
      - name: Send notification
        env:
          SLACK_WEBHOOK_URL: ${{ steps.channel.outputs.webhook }}
        run: |
          curl -X POST "$SLACK_WEBHOOK_URL" ...
```

### 特定のエラーでのみ通知

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        id: test
        continue-on-error: true
        run: npm test
      
      - name: Notify on critical failure
        if: steps.test.outcome == 'failure' && contains(github.event.head_commit.message, 'critical')
        run: |
          # 緊急通知を送信
```

### Slack通知にカスタムフィールドを追加

```yaml
- name: Send custom Slack notification
  run: |
    curl -X POST "$SLACK_WEBHOOK_URL" \
      -H 'Content-type: application/json' \
      --data '{
        "blocks": [
          {
            "type": "section",
            "fields": [
              {
                "type": "mrkdwn",
                "text": "*テスト結果:*\n✅ 100/100 passed"
              },
              {
                "type": "mrkdwn",
                "text": "*カバレッジ:*\n📊 85.3%"
              },
              {
                "type": "mrkdwn",
                "text": "*ビルド時間:*\n⏱️ 2m 34s"
              }
            ]
          }
        ]
      }'
```

## トラブルシューティング

### Gmail送信エラー

```
smtplib.SMTPAuthenticationError: (535, '5.7.8 Username and Password not accepted')
```

**解決策:**
1. 2段階認証が有効か確認
2. アプリパスワードを再生成
3. Secretsの値にスペースや改行が含まれていないか確認

### Slack Webhook エラー

```
{"ok":false,"error":"invalid_token"}
```

**解決策:**
1. Webhook URLが正しいか確認
2. Slackアプリが削除されていないか確認
3. Webhookを再作成

### 権限エラー（PR Comment）

```
Resource not accessible by integration
```

**解決策:**
ワークフローに適切なpermissionsを追加:

```yaml
permissions:
  pull-requests: write
  contents: read
```

## 関連ドキュメント

- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [Slack API - Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Gmail SMTP設定](https://support.google.com/mail/answer/7126229)
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)

## チェックリスト

- [ ] Gmailの2段階認証を有効化
- [ ] Gmailアプリパスワードを取得
- [ ] Slack Incoming Webhookを作成
- [ ] GitHub Secretsを設定
- [ ] ワークフローファイルを配置
- [ ] 手動実行でテスト
- [ ] プッシュして自動実行を確認
