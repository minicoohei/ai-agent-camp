---
description: "Shared spec — how slash commands behave under claude -p / cursor-agent --print."
nonInteractiveMode: compliant
tags: ["lib", "convention"]
---

# Non-interactive mode convention

このファイルは **コマンドそのもの** ではなく、すべての slash command が参照する **共通仕様** です。`claude -p` / `cursor-agent --print` のように TTY が無いモードで slash command が呼ばれた場合の振る舞いを統一します。

## 何が問題か

Slash command の多くは AI が `AskQuestion` ブロックでユーザーに選択肢を提示する設計になっています。`claude -p` などの非対話モードではこの選択肢が画面に表示できず、AI が「答えが来るのを待つ」「勝手にデフォルトを選ぶ」「stuck する」のいずれかになります。OAuth 認証フローや AI ツール再起動の指示も同じ理由で詰みます。

## 解決方針: 3 つの宣言モード

各 slash command の frontmatter で `nonInteractiveMode` を宣言します:

| 値 | 意味 | -p 実行時の振る舞い |
|---|---|---|
| `compliant` | 対話的入力なしで完走可能 | そのまま実行 |
| `deferred` | 対話入力が必要だが、-p ではここまで進めて停止できる | 読み取り系の操作は実行 → 残ステップを `setup-resume.md` に書き出して終了 |
| `incompatible` | -p では原理的に動かない（ブラウザ OAuth 等） | 即座に「対話モードで実行してください」のメッセージだけ出して exit |

## 非対話モード判定（AI への指示）

コマンド開始時、AI は以下のいずれかを満たす場合に「非対話モード」と判定する:

- `process.env.CLAUDE_CODE_NON_INTERACTIVE === "1"` または `CLAUDE_CODE_PRINT === "1"`
- `process.env.CURSOR_AGENT_PRINT === "1"` または `CURSOR_NONINTERACTIVE === "1"`
- 標準入力が TTY ではない（`tty.isatty(stdin.fd) === false`）
- session metadata に `print: true` / `headless: true` などのヒントがある

判定が曖昧な場合は、コマンド frontmatter の `nonInteractiveMode` を尊重する（`compliant` ならそのまま進める、それ以外なら deferred として扱う）。

## AskQuestion の deferred 化

AskQuestion を見つけたとき、非対話モードであれば:

1. 選択肢の中から `recommended: true` または「⭐推奨」「(Recommended)」マークがあるものを **暫定選択** として記録する。
2. それを **実行はせず**、`setup-resume.md` に「次に対話モードで `/<command-name>` を再実行し、ここで `<暫定選択>` を選ぶ」と書く。
3. その後の `AskQuestion`-依存ステップは省略し、レポートだけ表示して終了する。

## OAuth フローの incompatible 化

OAuth ブラウザフロー（`gcloud auth login` / `gh auth login` / Notion OAuth 等）は非対話モードで詰むため、`nonInteractiveMode: incompatible` を宣言する。AI は冒頭でこう案内する:

> このコマンドはブラウザ認証を必要とするため、`claude -p` / `cursor-agent --print` では完走できません。対話モードで `claude` または `cursor-agent` を起動し直してから `/コマンド名` を実行してください。

## AI ツール再起動指示の deferred 化

「Claude Code を再起動してください」という指示は -p では実行不能。これも `setup-resume.md` に記載して exit。

## setup-resume.md フォーマット

```markdown
# 中断した setup の再開ガイド

中断時刻: 2026-05-04 15:23 JST  
中断したコマンド: /setup-notion  
理由: 非対話モード（claude -p）では完走できないため

## 次にやること

1. 対話モードで Claude Code または Cursor を起動
2. 再度 `/setup-notion` を実行
3. 「セットアップ方式を選択」で **A. Hosted MCP（OAuth）⭐推奨** を選択
4. 自動でブラウザが開くので、Notion にログインしてアクセスを許可
5. AI ツールを再起動して接続を確認

## 補足

- 暫定選択した内容: hosted_oauth
- すでに完了した read-only ステップ:
  - `.mcp.json` の存在確認: あり
  - 既存の Notion MCP エントリ: なし
```

## frontmatter テンプレ

新規 slash command を書くときは以下から選んで `nonInteractiveMode` を入れる:

```yaml
---
description: "..."
nonInteractiveMode: compliant   # or: deferred, incompatible
---
```

宣言が無いコマンドは静的解析（`tools/cli_mode_check/check.py`）で D 評価扱いとなり、CI で警告される。

## 関連

- 静的解析ツール: `tools/cli_mode_check/check.py`
- レポート出力先: `reports/cli-mode-*.csv` / `.md`
