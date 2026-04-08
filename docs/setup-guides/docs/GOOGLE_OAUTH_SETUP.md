# Google OAuth セットアップガイド

Gmail、Google Calendar、Google DriveなどのサービスにアクセスするためのOAuth認証設定手順です。

---

## 概要

| 項目 | 内容 |
|------|------|
| 認証方式 | OAuth 2.0 |
| 対応サービス | Gmail, Calendar, Drive, Sheets, Slides |
| 無料枠 | 各サービスのAPI制限に依存 |
| 必要時間 | 約20分 |

---

## 対応サービスとスコープ

| サービス | スコープ | 用途 |
|---------|---------|------|
| Gmail | `gmail.readonly` | メール読み取り |
| Gmail | `gmail.send` | メール送信 |
| Calendar | `calendar.readonly` | カレンダー読み取り |
| Calendar | `calendar.events` | イベント作成・編集 |
| Drive | `drive.readonly` | ファイル読み取り |
| Drive | `drive.file` | ファイル作成・編集 |
| Sheets | `spreadsheets` | スプレッドシート操作 |
| Slides | `presentations` | スライド操作 |

---

## ステップ1: Google Cloud Console でプロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを選択または新規作成
   - 「プロジェクトを選択」> 「新しいプロジェクト」
   - プロジェクト名: `ai-agent-project`（任意）
3. プロジェクトが作成されたら選択

---

## ステップ2: API を有効化

1. 左メニューの「**APIとサービス**」> 「**ライブラリ**」
2. 必要なAPIを検索して有効化：

| API名 | 検索キーワード |
|-------|---------------|
| Gmail API | `gmail` |
| Google Calendar API | `calendar` |
| Google Drive API | `drive` |
| Google Sheets API | `sheets` |
| Google Slides API | `slides` |

各APIの詳細ページで「**有効にする**」をクリック

---

## ステップ3: OAuth 同意画面の設定

1. 左メニューの「**APIとサービス**」> 「**OAuth同意画面**」
2. ユーザータイプを選択
   - **内部**: 組織内ユーザーのみ（Google Workspace）
   - **外部**: 一般ユーザー向け

3. アプリ情報を入力
   - アプリ名: `AI Agent App`
   - ユーザーサポートメール: あなたのメールアドレス
   - デベロッパーの連絡先: あなたのメールアドレス

4. スコープを追加
   - 「スコープを追加または削除」をクリック
   - 必要なスコープを選択（上記表を参照）

5. テストユーザーを追加（外部の場合）
   - 自分のGmailアドレスを追加

6. 「保存して続行」

---

## ステップ4: OAuth クライアントIDの作成

1. 左メニューの「**APIとサービス**」> 「**認証情報**」
2. 「**認証情報を作成**」> 「**OAuthクライアントID**」
3. アプリケーションの種類: **デスクトップアプリ**
4. 名前: `AI Agent Desktop`（任意）
5. 「**作成**」をクリック
6. 表示されるクライアントIDとシークレットをメモ

7. 「**JSONをダウンロード**」をクリック
   - ファイル名: `credentials.json`
   - プロジェクトルートに配置

---

## ステップ5: 認証の実行

### 方法1: セットアップスクリプト（推奨）

```bash
uv run python tools/google_api_setup.py
```

ブラウザが開き、Googleアカウントでログインして権限を付与します。

### 方法2: 手動認証

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

print("認証完了!")
```

---

## ステップ6: 環境変数の設定

### credentials.json の配置

```bash
# プロジェクトルートに配置
cp ~/Downloads/client_secret_*.json credentials.json
```

### .env ファイル（オプション）

```bash
# .env
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_TOKEN_PATH=./token.pickle
```

### GitHub Secrets（CI/CD用）

1. `credentials.json` をBase64エンコード
   ```bash
   base64 -i credentials.json | tr -d '\n'
   ```
2. GitHubのSecrets に `GOOGLE_CREDENTIALS_BASE64` として保存

---

## ステップ7: 動作確認

### Gmail API テスト

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('token.pickle')
service = build('gmail', 'v1', credentials=creds)

results = service.users().messages().list(userId='me', maxResults=5).execute()
messages = results.get('messages', [])
print(f"最新のメール: {len(messages)}件")
```

### Calendar API テスト

```python
service = build('calendar', 'v3', credentials=creds)

events = service.events().list(
    calendarId='primary',
    maxResults=5
).execute()
print(f"最新のイベント: {len(events.get('items', []))}件")
```

---

## 複数アカウント対応

複数のGoogleアカウントを使用する場合：

```bash
# アカウント別のセットアップ
uv run python tools/gmail_account_setup.py  # Gmailアカウント
uv run python tools/google_account_setup.py  # Calendar/Drive用
```

各アカウントのトークンは別ファイルで管理：
```
tokens/
├── gmail_personal.pickle
├── gmail_work.pickle
├── calendar_personal.pickle
└── drive_work.pickle
```

---

## トラブルシューティング

### Access Denied エラー

```
Access Denied: App is not verified
```

**解決策**:
1. OAuth同意画面でテストユーザーに自分を追加
2. または本番環境に移行（Googleの審査が必要）

### invalid_grant エラー

```
Error: invalid_grant
```

**解決策**:
1. `token.pickle` を削除して再認証
   ```bash
   rm token.pickle
   uv run python tools/google_api_setup.py
   ```

### スコープ不足エラー

```
Request had insufficient authentication scopes
```

**解決策**:
1. 必要なスコープを追加
2. `token.pickle` を削除して再認証

### リフレッシュトークンの期限切れ

**症状**: 7日後にトークンが無効になる（テストモードの場合）

**解決策**:
1. OAuth同意画面を本番環境に移行
2. または定期的に再認証

---

## セキュリティ注意事項

1. **credentials.json を公開しない**
   - `.gitignore` に追加
   ```
   credentials.json
   token.pickle
   *.pickle
   ```

2. **最小限のスコープを使用**
   - 必要なスコープのみを要求

3. **トークンの安全な保管**
   - 本番環境ではSecret Managerを使用

---

## 使用するスキル

以下のスキルでGoogle OAuthを使用します：

- `check-inbox` - Gmail/Calendar分析
- `gmail-pending-replies` - 未返信メール確認
- `fetch-slides` - Google Slides取得
- `gas-clasp-ops` - GAS連携

---

## 次のステップ

- [BIGQUERY_SETUP.md](./BIGQUERY_SETUP.md) - BigQuery設定
- [NOTION_API_SETUP.md](./NOTION_API_SETUP.md) - Notion API設定
- [Module 4: データ分析](https://ai-agent.camp/ja/course/module-4) - データ分析の学習
