---
name: tmux-session-manager
description: "Lightsail上のClaude Code tmuxセッションをSSH経由で管理。 「セッション確認」「PR同期」「tmuxの状態」等のリクエストで発動。"
triggers:
  - セッション確認
  - セッション一覧
  - tmuxの状態
  - PRの進捗確認
  - セッションに指示
  - tmux-session-manager
  - sync-prs
---
# Tmux Session Manager Skill

Lightsail 上で稼働する Claude Code tmux セッションを SSH 経由で管理するスキル。
Issue/PR 単位のセッション状況確認、指示送信、PR 同期を行う。

## トリガー

以下のキーワードで発動:
- 「セッション確認」「セッション一覧」「tmux の状態」
- 「PR の進捗」「Issue の作業状況」
- 「セッション作成」「PR 同期」「sync-prs」
- 「ダッシュボード」「tmux dashboard」
- 「セッションに指示」「send-keys」

## スクリプトパス

リモート (Lightsail) 上:
```
REPO=/home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata
CC=$REPO/ops/tmux-manager/cc-session.sh
SYNC=$REPO/ops/tmux-manager/sync-prs.sh
```

## コマンド実行方法

全てのコマンドは SSH 経由で実行する。`ssh lightsail` のエイリアスが `~/.ssh/config` に設定済み。

### ダッシュボード表示

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh dashboard"
```

### セッション一覧

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh list"
```

### セッション状態確認

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh status PR-45"
```

### セッション出力キャプチャ

```bash
# デフォルト100行
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45"

# 行数指定
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45 200"
```

### セッション作成

```bash
# PR 用
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create PR-45"

# Issue 用
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create ISSUE-123"
```

### 指示送信 (send-keys)

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh send PR-45 'このPRのレビューコメントに対応して push してください'"
```

### 全 Open PR 同期

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/sync-prs.sh --cleanup"
```

### セッション終了

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh kill PR-45"
```

## ワークフロー

### 1. 全体状況確認

ユーザーが「セッション確認」「今の状態は？」と聞いた場合:

1. `dashboard` コマンドで全体概要を表示
2. 必要に応じて個別の `status` で詳細確認
3. 結果をユーザーに分かりやすく要約して報告

### 2. PR 同期 + セッション作成

ユーザーが「PR 同期して」「全 PR のセッション作って」と言った場合:

1. `sync-prs.sh --cleanup` で全 Open PR を同期
2. 結果（作成数、スキップ数、クリーンアップ数）を報告

### 3. 特定セッションへの指示

ユーザーが「PR-45 にレビュー対応させて」と言った場合:

1. `status PR-45` で現在の状態を確認
2. アイドル状態なら `send PR-45 "指示内容"` で指示を送信
3. 作業中なら「現在作業中です。完了を待ちますか？」と確認

### 4. セッション出力の確認・要約

ユーザーが「PR-45 で何してる？」と聞いた場合:

1. `capture PR-45 100` で最新出力を取得
2. 内容を要約してユーザーに報告

## 注意事項

- SSH 接続がタイムアウトする場合は `-o ConnectTimeout=10` を追加
- 作業中のセッションに send-keys しない（状態を必ず確認）
- セッション数は同時 5 以下を推奨（Lightsail リソース制約）
- ログは `ops/tmux-manager/logs/` に保存されている
