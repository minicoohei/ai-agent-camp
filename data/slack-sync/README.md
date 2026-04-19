# Slack Message Sync

Slackのメッセージを自動的にGitHubリポジトリにMarkdown形式で保存するツールです。

## 特徴

- **Bot招待不要**: User Tokenを使用するため、各チャンネルにBotを招待する必要がありません
- **差分更新**: 前回取得以降の新しいメッセージのみを取得
- **Markdown形式**: 読みやすいMarkdown形式で保存
- **GitHub Actions**: 毎時自動実行

## セットアップ手順

### Step 1: Slack App の作成

1. [Slack API](https://api.slack.com/apps) にアクセス
2. 「Create New App」→「From scratch」を選択
3. App名（例: `Message Archiver`）とワークスペースを設定
4. 「Create App」をクリック

### Step 2: OAuth Scopes の設定

1. 左メニューから「OAuth & Permissions」を選択
2. 「User Token Scopes」セクションまでスクロール
3. 以下のスコープを追加:
   - `channels:history` - パブリックチャンネルの履歴
   - `channels:read` - パブリックチャンネル一覧
   - `groups:history` - プライベートチャンネルの履歴
   - `groups:read` - プライベートチャンネル一覧
   - `users:read` - ユーザー情報（名前解決用）
   - `im:history` - DM履歴（オプション）
   - `mpim:history` - グループDM履歴（オプション）

4. 「Redirect URLs」セクションで「Add New Redirect URL」をクリック
5. `https://example.com/callback` を追加（ダミーURL）
6. 「Save URLs」をクリック

### Step 3: Client ID と Client Secret の取得

1. 左メニューから「Basic Information」を選択
2. 「App Credentials」セクションから以下をメモ:
   - **Client ID**
   - **Client Secret**

### Step 4: User Token の取得

ローカルPCで以下のコマンドを実行:

```bash
# 依存関係のインストール
uv add requests python-dotenv

# 環境変数を設定（または .env ファイルに記載）
export SLACK_CLIENT_ID="あなたのClient ID"
export SLACK_CLIENT_SECRET="あなたのClient Secret"

# 認証URLを生成
python scripts/get_token.py --generate-url
```

表示されたURLをブラウザで開き、「許可する」をクリックします。

リダイレクト先のページはエラーになりますが、**アドレスバーのURL**を確認してください:

```
https://example.com/callback?code=xxxxxxxxxx...
```

この `code=` 以降の文字列をコピーして:

```bash
python scripts/get_token.py --code=コピーしたコード
```

成功すると `xoxp-...` で始まるTokenが表示されます。

### Step 5: GitHub Secrets の設定

1. GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. 以下を追加:
   - **Name**: `SLACK_USER_TOKEN`
   - **Secret**: 取得した `xoxp-...` トークン
4. 「Add secret」をクリック

### Step 6: GitHub Actions の有効化

1. リポジトリの「Actions」タブを開く
2. ワークフローが表示されたら「Enable」をクリック
3. 手動実行する場合は「Run workflow」をクリック

## ファイル構成

```
slack-sync/
├── .github/
│   └── workflows/
│       └── slack-sync.yml    # GitHub Actionsワークフロー
├── scripts/
│   ├── get_token.py          # Token取得スクリプト
│   └── fetch_slack.py        # メッセージ取得スクリプト
├── data/
│   └── *.md                  # チャンネルごとのMarkdownファイル
├── .last_sync.json           # 同期状態
├── requirements.txt          # Python依存関係
└── README.md                 # このファイル
```

## 出力形式

各チャンネルのメッセージは `data/{チャンネル名}.md` に保存されます:

```markdown
# general

## 2026-01-06

### 10:30 - 山田太郎
今日のミーティングは14時からです。

### 10:45 - 鈴木花子
了解しました！

---

## 2026-01-05

### 18:00 - 田中一郎
お疲れ様でした。
```

## 設定オプション

### 特定のチャンネルのみ取得

環境変数 `SLACK_TARGET_CHANNELS` にチャンネルIDまたはチャンネル名をカンマ区切りで設定:

```yaml
env:
  SLACK_TARGET_CHANNELS: "general,random,C01234567"
```

GitHub Actionsの手動実行時にも指定可能です。

## トラブルシューティング

### Token取得時のエラー

- **invalid_code**: codeは一度しか使えません。再度認証URLから取得してください
- **code_already_used**: このcodeは既に使用済みです

### メッセージ取得時のエラー

- **not_in_channel**: プライベートチャンネルに参加していない
- **channel_not_found**: チャンネルが存在しない、またはアクセス権がない

## 注意事項

- User Tokenは**あなた個人の権限**で動作します
- あなたがアクセスできるチャンネルのみ取得可能です
- Tokenを他人と共有しないでください
- 退職などでワークスペースから削除されるとTokenは無効になります

## ライセンス

MIT License
