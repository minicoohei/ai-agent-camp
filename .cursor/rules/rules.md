# Cursor Rules - ai-agent-camp

## このリポジトリの前提
- この repo は非エンジニア向けの教材です。
- Cursor、Claude Code、Codex で同じ curriculum を共有します。
- ツールごとに違うのは入口、セットアップ、実行フローです。

## 学習時の基本ルール
- まず repo 内の文書と既存ファイルを読んで状況を確認する
- 大きい作業は短い計画を書いてから進める
- 既存の教材構造や lesson id を壊さない
- 説明は学習者向けに短く、実ファイルに結びつけて書く

## 重要な入口
- 全体案内: `README.md`
- Codex: `AGENTS.md`
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/commands/*`

## 安全ルール
- `rm -rf`、`git reset --hard`、`git clean -fd`、`git push --force` は使わない
- API キーやトークンをチャットに貼らせない
- `.env.local` に保存した後、`tools/credential_manager.py` で Credential Store に移す
- MCP や外部設定を無条件で承認しない

## 編集時の方針
- 既存 docs と重複する説明を増やさない
- 教材として分かりやすい表現を優先する
- 実態とずれた汎用フレームワーク前提は持ち込まない
