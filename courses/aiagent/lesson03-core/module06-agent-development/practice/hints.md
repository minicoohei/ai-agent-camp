# ヒント: エージェント開発

## SKILL.md の書き方

### YAML フロントマター
```yaml
---
name: skill-name        # スキルの識別子（ハイフン区切り）
description: |          # Claude Code がスキルを選択する際に参照する説明
  何をするスキルか、
  いつ使うべきかを記載
---
```

### 重要なポイント
- `description` は Claude Code がスキルの適用を判断する材料
- トリガーフレーズを含めると、ユーザーの指示に反応しやすくなる
- パラメータ表は使い方の理解に必須

## コマンドの書き方

### ファイル配置
```
.cursor/commands/
├── lesson/              # レッスン用コマンド
│   └── start-X-Y.md
└── utility/             # ユーティリティコマンド
    └── command-name.md
```

### 構成要素
1. **YAML フロントマター**: `description` フィールド
2. **タイトル**: `# /command-name`
3. **説明**: コマンドの目的
4. **処理手順**: Claude Code が実行する手順
5. **実行コマンド**: 実際の bash/python コマンド

### コマンドの処理フロー
```
ユーザーが /command-name を実行
  → ツールがコマンドファイルを読み込む
  → ファイル内の手順に従って処理を実行
  → 結果をユーザーに表示
```

## エージェント定義ファイル

### 配置場所
```
.claude/agents/agent-name.md
```

### 構成
- **役割**: エージェントの目的と責任範囲
- **トリガー**: いつ起動するか
- **使用ツール**: どのスキルやコマンドを使うか
- **処理フロー**: 具体的な処理の流れ

## Git ログの取得方法

### 当日のコミット取得
```bash
# 今日のコミット一覧
git log --since="today 00:00" --format="%h %s" --no-merges

# 詳細なフォーマット
git log --since="today 00:00" --format="%h|%s|%an|%ai" --no-merges

# 統計情報付き
git log --since="today 00:00" --stat --no-merges
```

### 差分統計
```bash
# 追加/削除行数
git diff --stat HEAD~5

# 数値のみ
git diff --shortstat HEAD~5
```

## gh コマンド（GitHub CLI）

### PR 操作
```bash
# PR 一覧
gh pr list

# PR の差分
gh pr diff <PR番号>

# PR の詳細
gh pr view <PR番号>

# PR のファイル一覧
gh pr diff <PR番号> --name-only
```

## スキルのテスト方法

### 手動テスト
```bash
# スクリプト直接実行
python skills/my-skill/scripts/main.py --param value

# 出力確認
cat output/result.json
```

### 構造チェック
```bash
# 必須ファイルの確認
ls skills/my-skill/SKILL.md
ls skills/my-skill/scripts/main.py

# SKILL.md のフロントマター確認
head -10 skills/my-skill/SKILL.md
```

## よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| SKILL.md に `name` フィールドがない | YAML フロントマターに `name` を必ず記載 |
| scripts/ の Python にシバンがない | `#!/usr/bin/env python3` を先頭に |
| コマンドに `description` がない | フロントマターに必ず記載 |
| パスが相対パス | `skills/...` のように明示 |
| エージェントの役割が曖昧 | 具体的なタスクと出力形式を定義 |
