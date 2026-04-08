---
name: session-retrospective
description: "セッション終了時に自己改善Issueを自動生成するスキル。セッション中に遭遇した問題・非効率・改善点を振り返り、GitHub Issueとして登録する。「振り返り」「自己改善Issue」「レトロスペクティブ」「session-retro」などのリクエストで使用。"
version: 1.0.0
author: ai-agent-camp
dependencies: []
---

# Session Retrospective - セッション自己改善Issue生成

## 概要

セッション（会話）の終了時に、遭遇した問題・非効率・改善すべき点を振り返り、
GitHub Issue として自動登録するスキルです。

## トリガー

以下のようなリクエストで発動:
- 「振り返りIssue出して」「自己改善Issue」
- 「レトロスペクティブ」「session-retro」
- 「改善点をIssueにして」
- セッション終了時の自動ルーティンとして

## ワークフロー

### Phase 1: セッション振り返り（自動分析）

会話履歴から以下のカテゴリで改善点を抽出:

| カテゴリ | ラベル | 検出パターン |
|---------|--------|-------------|
| **認証・設定の不備** | `auth` | トークン取得失敗、API認証エラー、環境変数の不整合 |
| **パス・規約の欠如** | `convention` | 形式のバラつき、命名規約の不統一、テンプレート非準拠 |
| **ツール・スクリプト不足** | `tooling` | ワンオフスクリプトで対処した箇所、自動化すべき手作業 |
| **ドキュメント不整合** | `docs` | CLAUDE.mdとMEMORYの矛盾、古い記載、情報の重複管理 |
| **ワークフローの非効率** | `workflow` | 試行錯誤が多かった箇所、フォールバックが必要だった処理 |
| **エラーハンドリング** | `error` | 想定外のエラー、不親切なエラーメッセージ、リトライが必要だった処理 |

### Phase 2: Issue ドラフト生成

各改善点について以下の構造でIssueを生成:

```markdown
## 背景
（何をしている時に問題が発生したか）

## 問題
（具体的な問題点。エラーメッセージやコマンドがあれば含める）

## 提案
（改善案を1〜3つ、具体的に）

## 発生状況
（どのセッション・タスクで発生したか）
```

### Phase 3: ユーザー確認

AskUserQuestion で各Issue候補を表示し、登録するか選択してもらう:
- 「全て登録」
- 「選んで登録」（1件ずつ確認）
- 「修正して登録」（内容を編集してから）

### Phase 4: GitHub Issue 登録

```bash
# GH_TOKEN取得（git remote URLから抽出）
export GH_TOKEN=$(git remote get-url origin | grep -oP '(?<=https://)[^@]+(?=@)' | sed 's/x-access-token://')    # Mac/Linux
# Windows (cmd): for /f "tokens=*" %i in ('git remote get-url origin') do set GH_TOKEN=%i
# Windows (PowerShell): $env:GH_TOKEN = (git remote get-url origin) -replace '.*https://([^@]+)@.*','$1' -replace 'x-access-token:',''

# Issue登録（--body-file を使用。heredoc だと Markdown のコードブロックでエスケープ問題が発生する）
cat > /tmp/issue_body.md << 'EOF'
Issue本文（Markdown）
EOF
gh issue create --repo TokenPocket/ai-agent-camp \
  --title "改善: <タイトル>" \
  --body-file /tmp/issue_body.md
```

## 実行方法

### 方法1: スキル呼び出し

```text
振り返りIssueを出して
```

### 方法2: スクリプト直接実行（テンプレートからIssue生成）

```bash
# JSONファイルから一括登録
python skills/session-retrospective/scripts/create_issues.py --input issues.json

# テストモード（dry-run、実際には登録しない）
python skills/session-retrospective/scripts/create_issues.py --input issues.json --dry-run
```

## Issue品質ガイドライン

### 良いIssue
- 再現可能な具体的な問題記述
- 実行したコマンドやエラーメッセージを含む
- 1 Issue = 1 改善点（スコープが明確）
- 提案が実装可能で具体的

### 悪いIssue（出すべきでないもの）
- 「もっと良くしたい」のような漠然とした内容
- セッション固有の一時的な問題（再発しないもの）
- ユーザーの操作ミスに起因するもの
- 既存のIssueと重複する内容

## 分析テンプレート

セッションを振り返る際の思考フレームワーク:

1. **ブロッカー**: 作業が止まった瞬間はあったか？ → 根本原因は？
2. **ワークアラウンド**: 正規の方法ではなく迂回策を使った箇所はあるか？
3. **繰り返し**: 同じ作業を2回以上行った箇所はあるか？
4. **ドキュメント参照**: CLAUDE.mdやMEMORYを見ても答えがなかった質問は？
5. **手作業**: スクリプトやツールで自動化できた手作業は？

## 出力

- GitHub Issues（TokenPocket/ai-agent-camp リポジトリ）
- コンソールにIssue URLを一覧表示
