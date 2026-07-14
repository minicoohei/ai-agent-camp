---
description: スキルをグローバル・他プロジェクトに同期
category: utility
nonInteractiveMode: compliant
---
# スキル同期

## 使い方
```text
/sync-skills
```

## 概要
プロジェクトの `.claude/skills/` にあるスキルを、グローバル（`~/.claude/skills/`）や他のプロジェクトにコピーして同期します。スキルの一覧確認や公式プラグインの導入ガイドも利用できます。

## サブコマンド一覧

### 1. スキル一覧の表示
プロジェクトとグローバルのスキルを一覧表示し、差分を確認できます。
```bash
uv run python tools/skill_manager.py list
```

### 2. グローバルに同期
プロジェクトスキルを `~/.claude/skills/` にコピーします。全プロジェクトでスキルが利用可能になります。
```bash
# 全スキルを同期
uv run python tools/skill_manager.py sync-global

# 特定のスキルのみ同期
uv run python tools/skill_manager.py sync-global --skills banner-creator diagram-generator

# 既存スキルを上書き
uv run python tools/skill_manager.py sync-global --force

# コピー先を指定
uv run python tools/skill_manager.py sync-global --target /path/to/target/skills
```

### 3. 別プロジェクトに同期
プロジェクトスキルを別プロジェクトの `.claude/skills/` にコピーします。
```bash
# 全スキルを同期
uv run python tools/skill_manager.py sync-project /path/to/other-project

# 特定のスキルのみ同期
uv run python tools/skill_manager.py sync-project /path/to/other-project --skills banner-creator

# 既存スキルを上書き
uv run python tools/skill_manager.py sync-project /path/to/other-project --force
```

### 4. 公式プラグイン導入ガイド
anthropics/skills リポジトリからプラグインを導入する手順を表示します。
```bash
uv run python tools/skill_manager.py plugin-guide
```

## オプション

| オプション | 対象コマンド | 説明 |
|-----------|-------------|------|
| `--force` | sync-global, sync-project | 既存スキルを上書き（デフォルトはスキップ） |
| `--skills NAME...` | sync-global, sync-project | コピーするスキル名を指定（デフォルトは全て） |
| `--target DIR` | sync-global | コピー先ディレクトリを変更 |

## 注意事項
- `--force` を指定しない場合、コピー先に既にあるスキルはスキップされます
- コピー方式（symlink ではない）のため、同期後のスキルは独立したコピーになります
- スキルを更新した場合は再度同期が必要です
