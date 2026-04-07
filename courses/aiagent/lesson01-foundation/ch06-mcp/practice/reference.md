# 参照テキスト: MCP（Model Context Protocol）

## MCP とは

Anthropic が策定したオープンプロトコル。AI モデルと外部ツール・データソースを標準化された方法で接続します。USB-C のように、どのツールでも同じインターフェースで接続できることを目指しています。

## 4つの主要概念

### 1. Tools（ツール）
AI が呼び出せる関数。入力パラメータと出力を定義。

```json
{
  "name": "search_database",
  "description": "データベースを検索する",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    }
  }
}
```

### 2. Resources（リソース）
AI が読み取れるデータソース。ファイル、データベース、API のデータ。

```
resource://database/users → ユーザー一覧
resource://file/config.json → 設定ファイル
```

### 3. Prompts（プロンプト）
事前定義されたプロンプトテンプレート。パラメータを受け取って展開。

```json
{
  "name": "code_review",
  "arguments": [
    { "name": "language", "required": true },
    { "name": "code", "required": true }
  ]
}
```

### 4. Sampling（サンプリング）
MCP サーバーから AI モデルにリクエストを送る逆方向の通信。サーバー側で AI の判断を利用する場合に使用。

## プロトコル仕様

### 通信方式
- **JSON-RPC 2.0** ベース
- **トランスポート**: stdio（標準入出力）または HTTP SSE
- **セッション管理**: 初期化 → 通常通信 → 終了

### メッセージフロー
```
クライアント（Claude Code / Cursor / Codex）  ←→  MCP サーバー（ツール提供）
     │                              │
     │  initialize →                │
     │  ← initialized               │
     │                              │
     │  tools/list →                │
     │  ← tools 一覧                │
     │                              │
     │  tools/call →                │
     │  ← result                    │
```

## 主要な MCP サーバー

| サーバー | 提供元 | 機能 |
|----------|--------|------|
| filesystem | Anthropic | ファイル操作（読み書き、検索） |
| github | Anthropic | GitHub API 操作 |
| slack | Anthropic | Slack メッセージ操作 |
| postgres | Anthropic | PostgreSQL クエリ実行 |
| puppeteer | Anthropic | ブラウザ自動操作 |
| google-drive | Community | Google Drive ファイル操作 |
| notion | Community | Notion ページ/DB 操作 |
| brave-search | Community | Web 検索 |
| memory | Anthropic | 永続的な記憶ストア |
| sequential-thinking | Anthropic | 段階的思考プロセス |

## ツール別の MCP 導線

```json
// .claude/settings.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem", "/path/to/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

- **Cursor**: エディタ側の MCP / tool 連携設定を使う
- **Claude Code**: `.claude/settings.json` などの project guide 側設定を使う
- **Codex**: Codex の MCP 設定層と repo 側の `AGENTS.md`, `docs/codex-mcp.md` を使う
