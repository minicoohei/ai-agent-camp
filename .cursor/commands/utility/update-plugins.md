---
description: インストール済み外部スキルを更新
category: utility
nonInteractiveMode: compliant
---
# 外部プラグイン更新

## 使い方
```text
/update-plugins
```

## 概要
`plugin-install` でインストールした外部スキルを、レジストリ（`external-plugins.yaml`）のバージョンに更新します。

## サブコマンド

### 1. 全外部スキルを更新
```bash
uv run python tools/skill_manager.py plugin-update
```

### 2. 特定プラグインのみ更新
```bash
uv run python tools/skill_manager.py plugin-update --plugin knowledge-work-plugins
```

### 3. 更新内容のプレビュー
```bash
uv run python tools/skill_manager.py plugin-update --dry-run
```

### 4. キャッシュの削除
リポジトリクローンのキャッシュを削除してディスク容量を解放します。
```bash
uv run python tools/skill_manager.py plugin-clean
```

## オプション

| オプション | 説明 |
|-----------|------|
| `--plugin NAME` | 対象プラグイン名を指定 |
| `--dry-run` | 更新内容を表示するのみ（実際には更新しない） |

## 注意事項
- 更新対象は SKILL.md に `source:` フィールドを持つスキルのみです
- 更新時はリポジトリの最新版を取得するため、ネットワーク接続が必要です
- `plugin-clean` でキャッシュを削除すると、次回の install/update 時に再クローンが必要です
