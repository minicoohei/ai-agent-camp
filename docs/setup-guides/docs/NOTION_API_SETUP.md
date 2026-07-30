# Notion セットアップガイド（OAuth 統一）

Notion のページ・データベースを Claude Code / Cursor から操作するためのセットアップ手順です。
**認証はすべて OAuth に統一**されており、API キー（Internal Integration Token）は使用しません。

---

## 概要

| 項目 | 内容 |
|------|------|
| 名称 | Notion CLI (ncli) + Notion 公式 Hosted MCP |
| 用途 | ターミナルおよび MCP 経由でのページ／データベース操作 |
| 認証方式 | **OAuth のみ**（ブラウザでの承認） |
| 無料枠 | Notion 無料プランで利用可能（API 利用に追加費用なし） |
| 必要時間 | 約10分 |

---

## ステップ1: ncli（Notion CLI）のインストール

```bash
npm install -g @sakasegawa/ncli
```

> 前提: Node.js 18 以上

確認:

```bash
ncli --version
```

---

## ステップ2: ncli で OAuth ログイン

```bash
ncli login
```

実行するとブラウザで Notion の OAuth 認証画面が自動で開きます。

1. Notion にログインしていない場合はログイン
2. アクセスを許可するワークスペースを選択
3. 「Allow access」をクリック

承認が完了するとターミナルに `Logged in as ...` のような表示が出ます。

> **重要**: API キー（`secret_xxx`）の入力は不要です。OAuth がブラウザで完結します。
> ワークスペース単位で権限を付与するため、ページごとの「Add connections」共有は **不要** です。

---

## ステップ3: 動作確認

```bash
# ログインユーザーの確認
ncli whoami

# ワークスペース内検索のスモークテスト
ncli search ""
ncli search "test"
```

ユーザー名が表示され、検索結果が返ってくれば OAuth 権限が正しく付与されています。

---

## ステップ4: Notion Hosted MCP の設定

Notion 公式の Hosted MCP は `https://mcp.notion.com/mcp` で提供されており、Streamable HTTP + OAuth で動作します。

### Claude Code の場合

`~/.claude/mcp_settings.json` に以下を追加:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### Cursor の場合

`~/.cursor/mcp.json` に同じ内容を追加します。

> **重要**:
> - `command` / `args` / `env` は **書きません**（ローカル起動ではなく Hosted MCP のため）
> - `NOTION_TOKEN` などのシークレットは **設定しません**（OAuth で認証）
> - `type` は必ず `http`

---

## ステップ5: 再起動と OAuth 承認

設定後、ツールを再起動してください。

- **Claude Code**: `exit` で終了 → `claude` で再起動
- **Cursor**: コマンドパレット (`Cmd+Shift+P` / `Ctrl+Shift+P`) → 「Reload Window」

再起動後、初めて Notion MCP のツールを呼び出したタイミングで、ブラウザに Notion の OAuth 承認ダイアログが開きます。「Allow access」をクリックして承認してください。

---

## ステップ6: 動作確認（MCP 経由）

ツール内で Notion MCP のツール（例: ワークスペース検索、ページ取得）を呼び出し、ワークスペースの情報が返ってくれば成功です。

---

## トラブルシューティング

### OAuth 認証が失敗する

- ブラウザでポップアップ／リダイレクトが許可されているか確認する
- もう一度 `ncli login` または MCP ツールの呼び出しを実行して OAuth をやり直す
- それでも失敗する場合は、ブラウザの Notion セッションを一度ログアウトしてから再試行する

### MCP サーバーから応答がない

- `~/.claude/mcp_settings.json` または `~/.cursor/mcp.json` の `notion` エントリを確認:
  - `type: "http"` になっているか
  - `url: "https://mcp.notion.com/mcp"` になっているか
  - `command` や `NOTION_TOKEN` が混入していないか
- JSON の構文を `python -m json.tool ~/.claude/mcp_settings.json` で検証
- ツール（Claude Code / Cursor）を完全に再起動
- ネットワーク到達性を `curl -I https://mcp.notion.com/mcp` で確認

### ページが取得できない / 別のワークスペースが見える

OAuth 承認時に意図しないワークスペースを選択した可能性があります。

```bash
ncli logout
ncli login
```

を実行して正しいワークスペースを選び直してください。MCP 側でも、ツールの認証ストアから Notion をログアウトしてから再認証します。

### object_not_found エラー

OAuth でワークスペース全体への権限を付与しているため、対象ページがそのワークスペースに存在することを確認してください。別ワークスペースのページにアクセスしたい場合は、`ncli logout` → `ncli login` で適切なワークスペースを選び直す必要があります。

### rate_limited エラー

Notion API のレート制限（おおむね 3 req/s）に達しています。リクエスト間に待機時間を入れる、もしくはバッチ処理を検討してください。

---

## セキュリティ

- OAuth トークンは ncli および各ツール（Claude Code / Cursor）の認証ストアで管理されます
- リポジトリやコミットに認証情報を含める必要は **ありません**
- 不要になったらツールから `notion` の認証情報を削除し、`ncli logout` でログアウトしてください

---

## 使用するスキル

以下のスキルで Notion を使用します:

- `notion-fetch` - Notion データ取得（ncli または MCP 経由）

---

## 次のステップ

- [Module 12: Notion 連携](https://ai-agent.camp/ja/course/module-12)
- [GEMINI_API_SETUP.md](./GEMINI_API_SETUP.md)
- [SLACK_TOKEN_SETUP.md](./SLACK_TOKEN_SETUP.md)

---

## 参考リンク

- [Notion API 公式ドキュメント](https://developers.notion.com/)
- [Notion 公式 MCP（Hosted）](https://developers.notion.com/docs/mcp)
- [@sakasegawa/ncli](https://www.npmjs.com/package/@sakasegawa/ncli)
