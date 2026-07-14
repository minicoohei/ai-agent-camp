# Claude Code Security Hooks

## 概要

このディレクトリには Claude Code の `PreToolUse` / `PostToolUse` フックスクリプトが格納されています。
`.claude/settings.json` の `hooks` 設定で有効化され、ツール実行の前後に自動的に検査を行います。

## 3層防御アーキテクチャ

| 層 | 機構 | タイミング | 役割 |
|----|------|----------|------|
| 第1層 | `.claude/settings.json` deny リスト | 即時ブロック | 明白な危険コマンドの拒否 |
| 第2層 | `.claude/hooks/` PreToolUse / PostToolUse スクリプト | ツール実行前後の検査 | rm→gomi 置換・複雑なパターン検知・PI 対策・実行後の品質警告 |
| 第3層 | Git の `pre-commit` hook | git commit 前 | 機密ファイルのコミット防止（要インストール） |

第3層はクローン直後には有効ではありません。`bash scripts/install_hooks.sh` を実行して
インストールしてください。`python3 tools/scripts/verify_integrity.py` は未設定または
実行権限のない `pre-commit` hook を警告します。

## フック一覧

### bash_guard.py — Bash コマンド事前検査

**対象ツール:** `Bash`

**処理フロー:**

1. stdin から JSON を読み取り `tool_input.command` を取得
2. ブロックパターンに一致 → exit 2（ブロック）
3. `rm` コマンド検出時:
   - gomi がインストール済み → `rm` を `gomi` に自動置換（`updatedInput`）
   - gomi 未インストール → exit 2 + インストール案内
4. いずれにも該当しない → exit 0（許可）

安全側に倒す設計のため、heredoc や複数行文字列の本文に含まれる行頭の `rm` も
コマンドと区別せず置換対象になります。

**ブロックパターン一覧:**

| パターン | 説明 |
|---------|------|
| `> .env` | .env への上書き禁止（`>>` 追記は許可） |
| `rm/gomi .env` | .env の削除禁止 |
| `rm/gomi *.pem/*.key/*.p12/*.pfx` | 鍵ファイルの削除禁止 |
| `rm/gomi credentials*.json` | 認証情報ファイルの削除禁止 |
| `sudo` | sudo の使用禁止 |
| `git push --force/-f` | 強制プッシュ禁止 |
| `git clean -x` | .env も削除される git clean 禁止 |
| `curl/wget + $API_KEY/$TOKEN/$SECRET` | API キーの外部送信禁止 |
| `:(){ :|:& };:` | フォークボム禁止 |

### write_guard.py — Write/Edit ツール事前検査

**対象ツール:** `Write`, `Edit`

**処理フロー:**

1. stdin から JSON を読み取り `file_path` と `content`/`new_string` を取得
2. 保護対象ファイル → exit 2（ブロック）
3. PI パターン + 危険操作パターン → exit 2（ブロック）
4. PI パターンのみ → stderr 警告 + exit 0（許可）
5. 問題なし → exit 0（許可）

**保護対象ファイル:**

| パターン | 例 |
|---------|-----|
| `.env`, `.env.local`, `.env.*` | 環境変数ファイル |
| `credentials*.json` | 認証情報 |
| `client_secret*.json` | OAuth クライアントシークレット |
| `token.json`, `refresh_token.json` | トークンファイル |
| `*.pem`, `*.key`, `*.p12`, `*.pfx` | 鍵・証明書ファイル |

**Prompt Injection 検知:**

PI パターン（英語・日本語・LLM 系メタタグ）と危険操作（curl, eval, exec, rm -rf 等）の
**組み合わせ**でブロック。PI パターン単独でも書き込みをブロックし、人間の確認を要求する。
正当な書き込みであれば `CLAUDE_GUARDRAILS_SKIP=1` を付けて再実行してください
（**テスト・検証時のみ** の最終手段）。

### git-push-review.sh — Git push 事前レビュー

**対象ツール:** `Bash`（`PreToolUse`）

`git push` を含むコマンドの実行前に現在のブランチを確認します。`main` または
`master` からの直接 push は `decision: block` を返してブロックします。feature
ブランチからの push は、push 対象コミット数と変更概要を stderr に表示して許可します。

### console-log-guard.sh — console.log 残存検査

**対象ツール:** `Edit`, `Write`（`PostToolUse`）

編集後の `.ts` / `.tsx` / `.js` / `.jsx` ファイルを検査し、`console.log` が残っていれば
行番号付きで stderr に警告します。警告専用フックのため、検出時もブロックしません。

### pptx_quality_check.py — PPTX 品質検査

**対象ツール:** `Bash`（`PostToolUse`）

Bash コマンドまたは実行結果に含まれる既存の `.pptx` 出力ファイルを読み取り、テキストの
はみ出し、要素の重なり、画面外配置を検査します。問題は stderr に警告し、処理は
ブロックしません。PPTX が見つからない場合や検査依存関係がない場合は何も行いません。

## 設定

### フックの有効化

`.claude/settings.json` に以下を追加:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/bash_guard.py" }]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/write_guard.py" }]
      }
    ]
  }
}
```

### ⚠️ 一時的なスキップ（テスト・検証専用 / 本番禁止）

`CLAUDE_GUARDRAILS_SKIP=1` を立てるとフックが skip されます。**通常運用では使用禁止**:

```bash
# テスト・PI ペイロード検証など、ガードを意図的に外したいときのみ
CLAUDE_GUARDRAILS_SKIP=1 claude
```

- **本変数が立っている間、すべての PI 検知 / .env 保護 / exfil ヘッダー検知が無効化されます**
- スキップ実行時は `[GUARDRAILS_SKIP]` 警告が stderr に出力される（サイレント無効化を防ぐため）
- セッション開始時に意図せずこの変数が立っていないか必ず確認してください
- **fork 先のリポジトリが `.claude/settings.json` の `env` キーや `scripts/` 内でこの変数を立てていないかも確認**

## 誤検知が発生した場合

1. stderr のエラーメッセージを確認
2. パターンが過剰なら本ファイル末尾「パターンの追加・変更」を見て修正
3. ワンショットの正当操作なら `CLAUDE_GUARDRAILS_SKIP=1` で再実行（**最終手段**）

## パターンの追加・変更

- `bash_guard.py` の `BLOCK_PATTERNS` リストに `(regex, message)` タプルを追加
- `write_guard.py` の `PROTECTED_FILE_PATTERNS` / `PI_PATTERNS` / `PI_DANGEROUS_PATTERNS` を編集

## トラブルシューティング

| 問題 | 原因 | 解決策 |
|------|------|--------|
| 全ツールがブロックされる | フックスクリプトが存在しない | `.claude/hooks/` にスクリプトを配置 |
| rm コマンドが使えない | gomi 未インストール | `brew install gomi` を実行 |
| .env に書き込めない | 保護対象ファイル | 手動でエディタから編集 |
| hooks 変更が反映されない | セッションキャッシュ | Claude Code を再起動 |
