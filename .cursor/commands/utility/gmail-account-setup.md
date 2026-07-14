---
nonInteractiveMode: incompatible
---

# Gmail アカウント セットアップ

個人Gmailアカウントを連携するセットアップを支援します。

## なぜOAuth Client IDが必要か

個人Gmail（@gmail.com）はセキュリティ上、**本人がブラウザでログインして許可**しないとアクセスできません。OAuth Client IDは「どのアプリからのアクセスか」を識別するための身分証です。

---

## 前提条件の確認

### 1. GitHub CLIの確認

```bash
gh auth status
```

認証されていない場合：
```bash
gh auth login
```

### 2. OAuth クライアントIDの確認

ユーザーに質問：
「Google Cloud ConsoleでOAuth クライアントIDは作成済みですか？」

**まだの場合は以下を案内：**

📄 `docs/GMAIL_OAUTH_SETUP.md` を参照、または https://console.cloud.google.com/ で：

1. プロジェクト作成（初回のみ）
2. Gmail API有効化
3. OAuth同意画面設定（外部、必須項目のみ）
4. 認証情報 → OAuth クライアントID作成（**デスクトップアプリ**）
5. クライアントIDとシークレットをコピー

---

## セットアップ実行

> **重要**: ブラウザ認証があるため、**ターミナルで直接実行**してください。
> Cursorのチャットからのpipe実行はタイムアウトします。

```bash
python scripts/setup_gmail_account.py --label <アカウント名>
```

### 例

```bash
python scripts/setup_gmail_account.py --label my-account
python scripts/setup_gmail_account.py --label work
python scripts/setup_gmail_account.py --label work
```

### 実行時の入力

1. クライアントID（Google Cloud Consoleからコピー）
2. クライアントシークレット（同上）
3. ブラウザでGoogleログイン → 許可

---

## アカウント追加後の設定

### 1. Secretの確認

```bash
gh secret list --repo <owner/repo> | grep GMAIL
```

### 2. GMAIL_ACCOUNTS_CONFIG を更新

**アカウントを追加するたびに更新が必要です：**

```bash
# 例: my-account と work の2アカウント
gh secret set GMAIL_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. ワークフローに環境変数を追加

`.github/workflows/fetch_data.yml` に新しいアカウントの環境変数を追加：

```yaml
env:
  GMAIL_<LABEL>_CLIENT_ID: ${{ secrets.GMAIL_<LABEL>_CLIENT_ID }}
  GMAIL_<LABEL>_CLIENT_SECRET: ${{ secrets.GMAIL_<LABEL>_CLIENT_SECRET }}
  GMAIL_<LABEL>_REFRESH_TOKEN: ${{ secrets.GMAIL_<LABEL>_REFRESH_TOKEN }}
```

### 4. 変更をコミット・プッシュ

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Gmail account <label>"
git push
```

---

## 動作確認

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

ログで確認：
```
Starting Multi-Gmail fetch...
Processing account: my-account
[my-account] OAuth authentication successful
Processing account: work
[work] OAuth authentication successful
```

---

## トラブルシューティング

### 「このアプリは確認されていません」と表示される

→ 正常です。「詳細」→「○○に移動」をクリックして続行。

### 認証エラーが発生する

確認事項：
1. Gmail APIが有効化されているか
2. OAuth同意画面が設定されているか
3. クライアントID/シークレットが正しいか

### GitHub Secretsへの登録に失敗する

```bash
gh auth status
```
で認証状態を確認。未認証なら `gh auth login` を実行。

### 「multiple remotes detected」エラー

```bash
python scripts/setup_gmail_account.py --label my-account --repo owner/repo
```
で明示的にリポジトリを指定。

### Git push競合エラー

同時に複数のワークフローが実行された場合に発生。再度実行すれば解消。

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```
