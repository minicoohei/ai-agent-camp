---
name: slack-todo-extractor
description: "Slackの同期データからメンションを検索しTODO/タスクを抽出・ステータス判定するスキル。 「Slackからタスク抽出」「TODO確認」「メンション確認」等のリクエストで発動。"
triggers:
  - Slackからタスク抽出
  - TODO確認
  - メンション確認
  - 宛のタスク
  - Slackの未対応タスク
  - slack-todo-extractor
  - Slack TODO
---

# Slack TODO抽出スキル

## 概要

Slackの同期データ（`slack-sync/data/`）から、特定ユーザー宛のメンションを検索し、スレッド返信を含めてTODO/タスクを抽出・ステータス判定するスキルです。

## クイックスタート

```bash
# 基本（キーワードベース）
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "2026-01-06:2026-01-08"

# LLMベース（高精度、要GEMINI_API_KEY）
uv run python skills/slack-todo-extractor/scripts/extract_todos.py \
  --users "YourName,your-username" \
  --period "1/6:8" \
  --use-llm
```

## 入力パラメータ

| パラメータ | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| `--users`, `-u` | Yes | 対象ユーザー名（カンマ区切り） | `YourName, your-username` |
| `--period`, `-p` | Yes | 検索期間 | `2026-01-06:2026-01-08` or `1/6:8` |
| `--workspace`, `-w` | No | ワークスペース（省略時は全て） | `my-workspace`, `my-workspace-2` |
| `--use-llm` | No | LLM（Gemini 2.0 Flash）で判定 | - |
| `--output`, `-o` | No | 出力形式 | `markdown`（デフォルト）or `json` |

## 処理フロー

### Step 1: メンション検索
`slack-sync/data/{workspace}/*.md` から `@ユーザー名` を含むメッセージを検索

### Step 2: スレッド返信の確認
各メンションに対して：
- スレッド返信（`> ####` 形式）を抽出
- 同日のチャンネル内後続メッセージを確認

### Step 3: ステータス判定

#### キーワードベース（`--use-llm` なし）
| 条件 | ステータス |
|------|-----------|
| 対象ユーザーが「完了」「対応しました」等 | completed |
| 依頼者が「ありがとう」「確認します」等 | completed |
| 対象ユーザーが「承知」「やります」等 | in_progress |
| 返信なし | pending |

#### LLMベース（`--use-llm` あり）
Gemini 2.0 Flashが文脈を理解して判定：
- 「承知」は受諾であり完了ではない
- 期限が設定されている場合、その期限前は対応中
- 依頼者の確認返信で完了判定

## 環境設定

### GEMINI_API_KEY（LLMモード使用時）

Credential Store に設定：
```bash
uv run python tools/credential_manager.py store GEMINI_API_KEY
```

## 前提条件

- `slack-sync/` のSlack同期が完了していること（`data/slack-sync/` 参照）

## 関連スキル

- `slack-search`: Slackメッセージの全文検索
- `slack-task-manager`: 統合タスク管理
