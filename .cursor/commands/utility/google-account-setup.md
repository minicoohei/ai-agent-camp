# Google アカウント セットアップ（Calendar/Drive用）

個人GoogleアカウントのCalendar/Driveを連携するセットアップを支援します。
**Gmail用と同じOAuthクライアントIDを流用できます。**

## なぜ別のセットアップが必要か

Gmail/Calendar/Driveはそれぞれ異なるスコープ（権限）が必要です。
このスクリプトは、3つすべてのスコープをまとめて認証します。

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
2. **Gmail API / Calendar API / Drive API を有効化**
3. OAuth同意画面設定（外部、必須項目のみ）
4. 認証情報 → OAuth クライアントID作成（**デスクトップアプリ**）
5. クライアントIDとシークレットをコピー

---

## セットアップ実行

> **重要**: ブラウザ認証があるため、**ターミナルで直接実行**してください。
> Cursorのチャットからのpipe実行はタイムアウトします。

```bash
python scripts/setup_google_account.py --label <アカウント名>
```

### 例

```bash
python scripts/setup_google_account.py --label my-account
python scripts/setup_google_account.py --label work
python scripts/setup_google_account.py --label work
```

### 実行時の入力

1. クライアントID（Google Cloud Consoleからコピー）
2. クライアントシークレット（同上）
3. ブラウザでGoogleログイン → 許可

---

## アカウント追加後の設定

### 1. Secretの確認

```bash
gh secret list --repo <owner/repo> | grep GOOGLE
```

以下のSecretsが登録されます：
- `GOOGLE_<LABEL>_CLIENT_ID`
- `GOOGLE_<LABEL>_CLIENT_SECRET`
- `GOOGLE_<LABEL>_REFRESH_TOKEN`

### 2. GOOGLE_ACCOUNTS_CONFIG を更新

**アカウントを追加するたびに更新が必要です：**

```bash
# 例: my-account と work の2アカウント
gh secret set GOOGLE_ACCOUNTS_CONFIG \
  --body '{"accounts":[{"label":"my-account","type":"oauth"},{"label":"work","type":"oauth"}]}' \
  --repo <owner/repo>
```

### 3. Drive用フォルダID設定（任意）

Driveからファイルを取得する場合、対象フォルダIDを設定します：

```bash
gh secret set GOOGLE_MYACCOUNT_DRIVE_FOLDER_ID \
  --body '<Google DriveのフォルダID>' \
  --repo <owner/repo>
```

または、GOOGLE_ACCOUNTS_CONFIGにフォルダIDを含めることもできます：

```json
{
  "accounts": [
    {
      "label": "my-account",
      "type": "oauth",
      "drive_folder_id": "1234567890abcdef"
    }
  ]
}
```

### 4. ワークフローに環境変数を追加

`.github/workflows/fetch_data.yml` に新しいアカウントの環境変数を追加：

```yaml
env:
  # Calendar/Drive用
  GOOGLE_<LABEL>_CLIENT_ID: ${{ secrets.GOOGLE_<LABEL>_CLIENT_ID }}
  GOOGLE_<LABEL>_CLIENT_SECRET: ${{ secrets.GOOGLE_<LABEL>_CLIENT_SECRET }}
  GOOGLE_<LABEL>_REFRESH_TOKEN: ${{ secrets.GOOGLE_<LABEL>_REFRESH_TOKEN }}
  GOOGLE_<LABEL>_DRIVE_FOLDER_ID: ${{ secrets.GOOGLE_<LABEL>_DRIVE_FOLDER_ID }}
```

### 5. 変更をコミット・プッシュ

```bash
git add .github/workflows/fetch_data.yml
git commit -m "feat: Add Google account <label> for Calendar/Drive"
git push
```

---

## 動作確認

```bash
gh workflow run "Fetch Google Cloud Data" --repo <owner/repo> -f days=1
```

ログで確認：
```
Starting Multi-Calendar fetch (OAuth mode)...
Processing Calendar for account: my-account
[my-account] OAuth authentication successful for Calendar
[my-account] Fetched 5 calendar events
Starting Multi-Drive fetch (OAuth mode)...
Processing Drive for account: my-account
[my-account] OAuth authentication successful for Drive
[my-account] Fetched 10 Drive files
```

---

## 出力ディレクトリ構造

```
output/
├── calendar/
│   ├── my-account/
│   │   ├── 2026-01-16_events.md
│   │   └── 2026-01-17_events.md
│   └── work/
│       └── 2026-01-16_events.md
└── drive/
    ├── my-account/
    │   ├── docs/
    │   ├── sheets/
    │   └── slides/
    └── work/
        └── docs/
```

---

## トラブルシューティング

### 「このアプリは確認されていません」と表示される

→ 正常です。「詳細」→「○○に移動」をクリックして続行。

### 認証エラーが発生する

確認事項：
1. Gmail API / Calendar API / Drive API が有効化されているか
2. OAuth同意画面が設定されているか
3. クライアントID/シークレットが正しいか

### GitHub Secretsへの登録に失敗する

```bash
gh auth status
```
で認証状態を確認。未認証なら `gh auth login` を実行。

### Driveファイルが取得されない

- `drive_folder_id` または `GOOGLE_<LABEL>_DRIVE_FOLDER_ID` が設定されているか確認
- 対象フォルダに読み取り権限があるか確認

### 「multiple remotes detected」エラー

```bash
python scripts/setup_google_account.py --label my-account --repo owner/repo
```
で明示的にリポジトリを指定。
