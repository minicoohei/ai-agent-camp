# Setup Google API for MCP - Google API設定ガイド

このコマンドは、Cursor Browserを使用して、MCP（Model Context Protocol）用のGoogle API設定とOAuth 2.0認証をステップバイステップでガイドします。

## 対象API

- Gmail API
- Google Calendar API
- Google Drive API
- Google Sheets API

## 機能

- **Cursor Browser活用**: ブラウザ操作で設定を半自動化
- **ステップバイステップガイド**: 各ステップで状態を確認しながら進行
- **ユーザー操作の明確化**: セキュリティ上必要な手動操作を明示
- **OAuth認証フロー**: クレデンシャル取得から認証完了まで

## 実行手順

### Phase 1: パラメータの確認

ユーザーの入力から以下の情報を確認してください：

1. **対象API**（複数選択可）:
   - `gmail` - Gmail API
   - `calendar` - Google Calendar API
   - `drive` - Google Drive API
   - `sheets` - Google Sheets API

2. **プロジェクト名**（任意、デフォルト: `mcp-google-api`）

3. **出力先ディレクトリ**（任意、デフォルト: プロジェクトルート）

### Phase 2: Google Cloud Console設定（Cursor Browser）

以下の手順をCursor Browserで実行してください。

#### ステップ1: Google Cloud Consoleにアクセス

```
browser_navigate: https://console.cloud.google.com/
```

実行後、`browser_snapshot`でページ状態を確認し、ログイン状態をチェック。

**ユーザーに案内:**
- ログインしていない場合: 「Googleアカウントにログインしてください」
- ログイン済みの場合: 次のステップへ

#### ステップ2: プロジェクト作成（必要な場合）

既存プロジェクトを使用する場合はスキップ可能。

```
browser_navigate: https://console.cloud.google.com/projectcreate
```

**ユーザーに案内:**
```
【プロジェクト作成】
1. プロジェクト名を入力してください（推奨: mcp-google-api）
2. 組織を選択してください（個人アカウントの場合は「組織なし」）
3. 「作成」をクリックしてください

準備ができたら「完了」と入力してください。
```

#### ステップ3: API有効化

選択されたAPIを順番に有効化します。URLパターン:

```
Gmail API:     https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={PROJECT_ID}
Calendar API:  https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}
Drive API:     https://console.cloud.google.com/apis/library/drive.googleapis.com?project={PROJECT_ID}
Sheets API:    https://console.cloud.google.com/apis/library/sheets.googleapis.com?project={PROJECT_ID}
```

各APIページで:
1. `browser_navigate`でAPIページにアクセス
2. `browser_snapshot`でページ状態を確認
3. 「有効にする」ボタンが見つかれば、ユーザーにクリックを案内

**ユーザーに案内:**
```
【API有効化: {API名}】
青い「有効にする」ボタンをクリックしてください。
有効化が完了したら「完了」と入力してください。
```

#### ステップ4: OAuth同意画面設定

```
browser_navigate: https://console.cloud.google.com/auth/overview?project={PROJECT_ID}
```

**ユーザーに案内:**
```
【OAuth同意画面の設定】
1. ユーザータイプで「外部」を選択し、「作成」をクリック
2. 以下の情報を入力:
   - アプリ名: 任意（例: MCP Google API）
   - ユーザーサポートメール: あなたのメールアドレス
   - デベロッパーの連絡先情報: あなたのメールアドレス
3. 「保存して次へ」をクリック
4. スコープの画面では、そのまま「保存して次へ」
5. テストユーザーの画面で、あなたのメールアドレスを追加
6. 「保存して次へ」→「ダッシュボードに戻る」

完了したら「完了」と入力してください。
```

#### ステップ5: OAuthクライアントID作成

```
browser_navigate: https://console.cloud.google.com/auth/clients?project={PROJECT_ID}
```

**ユーザーに案内:**
```
【OAuthクライアントID作成】
1. 「+ クライアントを作成」または「認証情報を作成」をクリック
2. アプリケーションの種類: 「デスクトップアプリ」を選択
3. 名前: 任意（例: MCP Desktop Client）
4. 「作成」をクリック
5. 表示されたダイアログで「JSONをダウンロード」をクリック
6. ダウンロードしたファイルを安全な場所に保存

JSONファイルのパスを教えてください
（macOS 例: ~/Downloads/client_secret_xxx.json）
（Windows WSL2 例: /mnt/c/Users/<Windowsユーザー名>/Downloads/client_secret_xxx.json）
```

### Phase 3: OAuth認証フロー実行

ダウンロードしたクレデンシャルJSONを使用して、認証フローを実行します。

```bash
uv run python tools/google_api_setup.py auth \
  --credentials "{クレデンシャルJSONのパス}" \
  --scopes "{選択されたスコープ}" \
  --output "{出力先ディレクトリ}"
```

**スコープの対応表:**
- gmail: `https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify`
- calendar: `https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.events`
- drive: `https://www.googleapis.com/auth/drive`
- sheets: `https://www.googleapis.com/auth/spreadsheets`

### Phase 4: 完了確認

認証が成功すると、以下のファイルが生成されます:
- `token.json` - 認証トークン
- `mcp_config.json` - MCP設定ファイル（参考）

**ユーザーに報告:**
```
【設定完了】
Google API設定が完了しました！

生成されたファイル:
- token.json: 認証トークン（重要: 安全に保管してください）
- mcp_config.json: MCP設定例

次のステップ:
1. MCPサーバーの設定ファイルを編集
2. 生成されたtokenのパスを設定
3. MCPサーバーを起動してテスト

詳細なMCP設定方法は、各MCPサーバーのドキュメントを参照してください。
```

## 使用例

### 基本的な使用（すべてのAPI）
```
/setup-google-api gmail calendar drive sheets
```

### 特定のAPIのみ
```
/setup-google-api gmail sheets
```

### プロジェクト名を指定
```
/setup-google-api gmail --project my-mcp-project
```

## 注意事項

### セキュリティ上の注意
- **クレデンシャルJSONとtoken.jsonは絶対に公開しないでください**
- これらのファイルがあれば、あなたのGoogleアカウントにアクセスできます
- `.gitignore`に追加して、リポジトリにコミットしないようにしてください

### ユーザー操作が必要な箇所
以下の操作はセキュリティ上、ユーザー自身が行う必要があります：
1. Googleアカウントへのログイン
2. OAuth同意画面での権限承認
3. クレデンシャルJSONのダウンロード
4. 認証フロー実行時のブラウザでの承認

### トラブルシューティング

#### エラー: "Access blocked: This app's request is invalid"
- OAuth同意画面の設定が完了していない可能性があります
- テストユーザーとして自分のメールアドレスが追加されているか確認してください

#### エラー: "invalid_grant"
- token.jsonが無効になっている可能性があります
- token.jsonを削除して、再度認証フローを実行してください

#### エラー: "API not enabled"
- 必要なAPIが有効化されていない可能性があります
- Google Cloud ConsoleでAPIが有効になっているか確認してください
