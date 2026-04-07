---
description: "プロジェクト情報を表示"
---

# プロジェクト情報

## 概要
このプロジェクトはAIエージェント開発のベースプラットフォームです。

## ディレクトリ構成
```text
ai-agent-camp/
├── .claude/         # Claude Code設定
│   └── skills/      # 再利用可能スキル
├── .cursor/         # Cursor IDE設定
│   └── commands/    # カスタムコマンド
├── commands/        # レッスンコマンド
├── course/          # HTMLコース教材
└── tools/           # Pythonスクリプト
```

## 技術スタック
- AI Framework: Claude 3.5 Sonnet
- Protocol: MCP（Model Context Protocol）
- IDE: Cursor / Claude Code
