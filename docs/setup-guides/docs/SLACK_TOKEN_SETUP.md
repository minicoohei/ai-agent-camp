# Slack Token セットアップガイド

Slack APIを使用して、チャンネル検索、メッセージ取得、TODO抽出などを行うための設定手順です。

---

## 概要

| 項目 | 内容 |
|------|------|
| API名 | Slack Web API |
| 用途 | チャンネル検索、メッセージ取得、タスク抽出 |
| 無料枠 | 無制限（レート制限あり） |
| 必要時間 | 約15分 |

---

## トークンの種類

| トークン | 用途 | 有効期限 | 推奨 |
|---------|------|---------|:----:|
| Bot Token | ボット用アクセス | 無期限 | O |
| User Token | ユーザー代理アクセス | 90日 | - |

> **推奨**: Bot Token を使用してください。User Token は90日で期限切れになります。

---

## ステップ1: Slack App の作成

1. [Slack API Apps](https://api.slack.com/apps) にアクセス
2. 「**Create New App**」をクリック
3. 「**From scratch**」を選択
4. アプリ名とワークスペースを入力
   - App Name: `AI Agent Bot`（任意）
   - Workspace: 対象のワークスペースを選択
5. 「**Create App**」をクリック

---

## ステップ2: スコープの設定

### Bot Token Scopes（推奨）

1. 左メニューの「**OAuth & Permissions**」をクリック
2. 「**Scopes**」セクションまでスクロール
3. 「**Bot Token Scopes**」で「**Add an OAuth Scope**」をクリック
4. 以下のスコープを追加：

| スコープ | 用途 |
|---------|------|
| `channels:history` | パブリックチャンネルのメッセージ取得 |
| `channels:read` | パブリックチャンネル一覧取得 |
| `groups:history` | プライベートチャンネルのメッセージ取得 |
| `groups:read` | プライベートチャンネル一覧取得 |
| `users:read` | ユーザー情報取得 |
| `users:read.email` | ユーザーメールアドレス取得 |
| `search:read` | メッセージ検索 |
| `files:read` | ファイル情報取得 |
| `im:history` | DMのメッセージ取得 |
| `mpim:history` | グループDMのメッセージ取得 |

### User Token Scopes（オプション）

特定の機能（ユーザーとして検索など）が必要な場合：

| スコープ | 用途 |
|---------|------|
| `search:read` | ユーザーとしてメッセージ検索 |

---

## ステップ3: アプリのインストール

1. 「**OAuth & Permissions**」ページの上部
2. 「**Install to Workspace**」をクリック
3. 権限を確認して「**許可する**」をクリック
4. 表示されるトークンをコピー

```
Bot Token: xoxb-...（約50文字）
User Token: xoxp-...（約100文字）
```

---

## ステップ4: 環境変数の設定

### 方法1: Credential Store（推奨）

OSの暗号化ストレージに安全に保存します。

```bash
# keyring パッケージのインストール（初回のみ）
pip install keyring

# Bot Token を保存（入力は画面に表示されません）
uv run python tools/credential_manager.py store SLACK_BOT_TOKEN

# User Token を保存（オプション）
uv run python tools/credential_manager.py store SLACK_USER_TOKEN
```

> **なぜ推奨？** Slack Token はワークスペースのデータにアクセスできる認証情報です。Credential Store はOSレベルで暗号化され、平文ファイルに保存されるリスクがありません。

### 方法2: .env ファイル（フォールバック）

Credential Store が使えない環境では `.env` を使用できます。

```bash
# .env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_USER_TOKEN=xoxp-your-user-token-here  # オプション
```

> **注意**: `.env` ファイルは `.gitignore` に含まれていることを必ず確認してください。

### 方法3: シェル環境変数

```bash
export SLACK_BOT_TOKEN=xoxb-your-bot-token-here
```

---

## ステップ5: ボットをチャンネルに招待

Bot Token でチャンネルにアクセスするには、ボットを招待する必要があります。

1. Slackでチャンネルを開く
2. メッセージ入力欄に `/invite @AI Agent Bot` を入力
3. Enterで送信

または、チャンネル設定から「インテグレーション」> 「アプリを追加する」

---

## ステップ6: 動作確認

### Pythonで確認

```python
import os
from slack_sdk import WebClient

# クライアント作成
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# 認証テスト
response = client.auth_test()
print(f"Bot User: {response['user']}")
print(f"Team: {response['team']}")

# チャンネル一覧取得
channels = client.conversations_list(types="public_channel")
for channel in channels['channels'][:5]:
    print(f"- {channel['name']}")
```

### curlで確認

```bash
curl -X POST https://slack.com/api/auth.test \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## レート制限

| Tier | 制限 |
|------|------|
| Tier 1 | 1+ リクエスト/分 |
| Tier 2 | 20+ リクエスト/分 |
| Tier 3 | 50+ リクエスト/分 |
| Tier 4 | 100+ リクエスト/分 |

主要なAPIのTier:
- `conversations.history`: Tier 3
- `conversations.list`: Tier 2
- `search.messages`: Tier 2
- `users.info`: Tier 4

---

## トラブルシューティング

### invalid_auth エラー

```
slack_sdk.errors.SlackApiError: invalid_auth
```

**解決策**:
1. トークンが正しくコピーされているか確認
2. トークンの種類（Bot/User）が正しいか確認
3. アプリが再インストールされていないか確認

### channel_not_found エラー

```
channel_not_found
```

**解決策**:
1. チャンネルIDが正しいか確認
2. ボットがチャンネルに招待されているか確認
3. プライベートチャンネルの場合、`groups:read` スコープがあるか確認

### missing_scope エラー

```
missing_scope: need xxx
```

**解決策**:
1. 必要なスコープを追加
2. アプリを再インストール（OAuth & Permissions > Reinstall）

### User Token の期限切れ

**症状**: 90日後にトークンが無効になる

**解決策**:
- Bot Token を使用する（推奨）
- 定期的にトークンを更新する仕組みを構築

---

## Slack同期データの活用

このプロジェクトでは、Slack履歴を定期的に同期してローカルで検索できるようにしています。

### 同期データの場所

```
slack-sync/
├── data/
│   ├── {workspace}/           # 現在のチャンネルデータ
│   ├── summary/{workspace}/   # サマリー
│   └── archive/{workspace}/   # アーカイブ
└── index/
    └── book_index.json        # 検索インデックス
```

### セマンティック検索の利用

```python
from slack_search import SlackSearch

search = SlackSearch()

# チャンネル検索
results = search.find_channels("DX展示会")

# 人物検索
persons = search.find_person("清水")

# タイムライン検索
timeline = search.get_timeline("2025-12-01", "2025-12-31")
```

---

## 使用するスキル

以下のスキルでSlack APIを使用します：

- `slack-search.skill` - チャンネル・メッセージ検索
- `slack-task-manager` - TODO抽出・タスク管理
- `slack-unanswered` - 未返信メッセージ検索
- `check-inbox` - Slack統合分析

---

## 次のステップ

- [GOOGLE_OAUTH_SETUP.md](./GOOGLE_OAUTH_SETUP.md) - Google OAuth設定
- [BIGQUERY_SETUP.md](./BIGQUERY_SETUP.md) - BigQuery設定
- [Module 6: Slack検索](https://ai-agent.camp/ja/course/module-6) - Slack連携の学習
