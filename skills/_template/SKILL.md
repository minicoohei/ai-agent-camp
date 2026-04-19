---
# === 共通メタデータ (必須) ===
name: skill-name
description: 1行の説明文
version: 1.0.0

# === 分類 (必須) ===
# role: designer | developer | analyst | marketer | communicator | educator | pm
# difficulty: beginner | intermediate | advanced
# tags: [tag1, tag2]

# === 実行情報 (推奨) ===
# estimatedMinutes: 15
# prerequisites: [setup-gemini]  # 先に完了すべきスキル/レッスン

# === Claude Code 固有 (optional) ===
# claude:
#   user-invocable: true
#   allowed-tools: [Bash, Write, Read]

# === Cursor 固有 (optional) ===
# cursor:
#   globs: ["*.py"]
---

# Overview

<!-- 何をするスキルか 1-2文で -->

# Usage

<!-- コマンド例 -->
```bash
# 基本実行
python skills/skill-name/scripts/main.py --arg value

# オプション付き
python skills/skill-name/scripts/main.py --arg value --flag
```

# Workflow

<!-- ステップバイステップの実行プロセス -->
1. Step 1
2. Step 2
3. Step 3

# Platform Specs

<!-- サイズ表、API仕様など。該当しない場合はセクション削除可 -->

# Troubleshooting

<!-- よくあるエラーと解決方法 -->
| エラー | 解決方法 |
|--------|---------|
| API key not found | `setup-gemini` を先に実行 |

# Success Criteria

<!-- 完了の判定基準 -->
- [ ] 出力ファイルが生成されている
- [ ] エラーなく完了
