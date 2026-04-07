---
description: 外部プラグインからスキルをインストール
category: utility
---

# 外部プラグインインストール

## 使い方
```text
/install-plugins
```

## 概要
外部プラグインレジストリ（`external-plugins.yaml`）に定義された6つのリポジトリから、厳選されたスキルをインストールします。SkillsBench論文に基づき、全スキルを一括導入せず、タスクに応じた2-3モジュールの組み合わせを推奨しています。

## サブコマンド一覧

### 1. 利用可能なスキル一覧
レジストリに登録された全プラグインと推奨スキルを表示します。
```bash
# 概要表示
uv run python tools/skill_manager.py plugin-list

# 各スキルのインストール状態も表示
uv run python tools/skill_manager.py plugin-list --verbose
```

### 2. 推奨スキルを一括インストール
全プラグインの推奨スキル（約17個）をまとめてインストールします。
```bash
uv run python tools/skill_manager.py plugin-install --all-recommended
```

### 3. 特定のプラグインからインストール
```bash
# プラグイン指定（推奨スキルのみ）
uv run python tools/skill_manager.py plugin-install --plugin knowledge-work-plugins

# プラグイン + スキル名指定
uv run python tools/skill_manager.py plugin-install --plugin claude-scientific-skills --skill matplotlib plotly

# 既存スキルを上書き
uv run python tools/skill_manager.py plugin-install --plugin marimo-skills --force
```

## 対象プラグイン

| プラグイン | リポジトリ | 推奨スキル数 |
|-----------|-----------|-------------|
| knowledge-work-plugins | anthropics/knowledge-work-plugins | 5 |
| ui-ux-pro-max-skill | nextlevelbuilder/ui-ux-pro-max-skill | 1 |
| planning-with-files | OthmanAdi/planning-with-files | 1 |
| claude-scientific-skills | K-Dense-AI/claude-scientific-skills | 5 |
| claude-skills | alirezarezvani/claude-skills | 3 |
| marimo-skills | marimo-team/skills | 2 |

## オプション

| オプション | 説明 |
|-----------|------|
| `--plugin NAME` | 対象プラグイン名を指定 |
| `--skill NAME...` | インストールするスキル名を指定 |
| `--all-recommended` | 全推奨スキルをインストール |
| `--force` | 既存スキルを上書き |

## 注意事項
- インストールされたスキルの SKILL.md に `source:` フィールドが自動追加されます（出典追跡）
- 既存のプロジェクトスキルと名前が衝突する場合はスキップされます（`--force` で上書き可能）
- 初回実行時にリポジトリのクローンが行われるため、ネットワーク接続が必要です
