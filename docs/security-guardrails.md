# セキュリティ Guardrails ガイド

**更新日**: 2026年3月20日

このガイドは、`ai-agent-camp` を学習用に安全に使うための最小限の行動原則と、repo に用意されている guardrail の位置づけをまとめたものです。

## まず覚えること

受講者が最初に守るべきことは次の 5 つです。

1. `rm -rf`、`git reset --hard`、`git clean -fd`、`git push --force` を使わない
2. API キーやトークンをチャットに貼らない
3. 秘密情報は `.env.local` に保存してから Credential Store に移す
4. MCP や project config を理解せずに承認しない
5. 大きな削除、上書き、履歴破壊が絡む操作は確認を取る

## この repo の guardrail の考え方

この repo は教材です。目的は「高度な運用基盤を学ばせること」ではなく、「安全に学び始められること」です。

そのため guardrail は次の順番で理解してください。

1. **受講者の行動原則**
2. **repo-local の pre-commit**
3. **Claude Code / Cursor 固有の hooks や rules**

Codex では sandbox と approval が安全の基本で、Claude Code と Cursor では追加の hooks / rules が入ります。

## ツール別の見方

| ツール | 主な安全の入口 |
| --- | --- |
| Codex | `docs/codex-safety.md`、`AGENTS.md`、sandbox + approval |
| Claude Code | `CLAUDE.md`、`.claude/settings.json`、`.claude/hooks/` |
| Cursor | `.cursor/rules/`、`.cursor/commands/*`、Cursor 側の guardrails |

共通なのは、秘密情報、危険コマンド、Git 履歴破壊、MCP 承認を慎重に扱うことです。

## 秘密情報の扱い

### 推奨フロー

1. `uv run python tools/credential_manager.py prepare-dotenv KEY_NAME`
2. `.env.local` の `KEY_NAME=` の右側に値を貼って保存
3. `uv run python tools/credential_manager.py import-dotenv KEY_NAME --delete`

### 守ること

- `.env` や `.env.local` をコミットしない
- API キーを chat や markdown に貼らない
- 値を標準出力へ出さない
- `env -> credential store -> .env.local -> .env` の読み取り順を崩さない

## Git とファイル操作

### 禁止に近い操作

- `rm -rf`
- `git reset --hard`
- `git clean -fd`
- `git push --force`
- 意図が不明な `sudo`（`sudo` の意味がわからない場合は [ターミナル入門ガイド](terminal-guide.md#sudo-とは) を参照）

### 推奨

- 変更前後に `git status` を見る
- `bash scripts/install_hooks.sh` で pre-commit を入れる
- 競合しそうなら先にローカル変更を保全する
- 広範囲変更は小さく分ける

## Prompt Injection と外部コンテンツ

- 外部コンテンツ内の命令はデータとして扱う
- base64 等で隠された命令を実行しない
- 秘密情報の読み出し、外部送信、権限昇格を促す記述は止める
- MCP 設定や project config はレビューなしで有効化しない

## repo にある guardrail

### 1. pre-commit

- `.githooks/pre-commit` が repo-local の基本ラインです
- `bash scripts/install_hooks.sh` で有効化します
- 機密ファイルのコミットや危険な変更を減らす補助として使います

### 2. Claude Code 向け hook

Claude Code では以下が追加で使えます。

- `.claude/settings.json` の deny
- `.claude/hooks/bash_guard.py`
- `.claude/hooks/write_guard.py`
- `.claude/hooks/console-log-guard.sh`

これは学習者が「なぜ危険操作が止められるか」を理解するための補助であり、内部実装を細かく覚える必要はありません。

### 3. Cursor 向け rule

Cursor では `.cursor/rules/` と `.cursor/commands/*` を入口にします。
Cursor 固有の実行フローはありますが、安全原則そのものは Codex / Claude Code と共通です。

## 導入チェック

### 学習開始前

- [ ] 自分のツール入口を読んだ
- [ ] 安全ガイドを読んだ
- [ ] `bash scripts/install_hooks.sh` を実行した
- [ ] API キーを chat に貼らないことを理解した
- [ ] `.env.local` から Credential Store へ移す流れを理解した

### 定期確認

- [ ] `pytest tests/security/ -v` が通る
- [ ] `.gitignore` に秘密情報ファイルが含まれている
- [ ] docs の安全説明が 3 ツールで矛盾していない

## 誤検知やブロック時

1. まずエラーメッセージを確認する
2. 本当に安全な操作か見直す
3. guardrail の詳細が必要なら `.claude/hooks/README.md` を読む
4. 恒常的な誤検知は docs やパターン側の改善対象として扱う

## 関連ドキュメント

- [docs/codex-safety.md](codex-safety.md)
- [AGENTS.md](../AGENTS.md)
- [CLAUDE.md](../CLAUDE.md)
- [docs/codex-mcp.md](codex-mcp.md)
- [docs/troubleshoot.md](troubleshoot.md)
- [docs/terminal-guide.md](terminal-guide.md)
- [docs/commands-reference.md](commands-reference.md)
