# module06-agent-development 完成例

## 概要

Claude Code のカスタム Agent、Skill、Command の開発完成例です。日報生成コマンドとコードレビュースキルという2つの実用的なツールを含みます。

## 成果物一覧

| ファイル | 種別 | 説明 |
|----------|------|------|
| `output/agents/daily-reporter.md` | Agent | 日報生成エージェント定義 |
| `skills/code-reviewer/SKILL.md` | Skill | コードレビュースキル定義 |
| `skills/code-reviewer/scripts/pr_analyzer.py` | Script | PR 差分を分析するスクリプト |
| `output/commands/daily-report.md` | Command | `/daily-report` コマンド |

## 使い方

### 日報生成
```bash
# /daily-report コマンドとして使用
# .cursor/commands/utility/ に配置し、必要なら Claude 側 command 導線にも反映
```

### コードレビュー
```bash
# スキルとして使用
python skills/code-reviewer/scripts/pr_analyzer.py . --base main --head feature-branch

# ファイル出力
python skills/code-reviewer/scripts/review_report_generator.py . --format markdown --output report.md
```

## 使用ツール

- Claude Code（Agent / Skill / Command 定義）
- Git CLI / GitHub CLI

## 学習ポイント

1. **Agent の設計**: 役割・トリガー・処理フローの明確な定義
2. **Skill の構造**: SKILL.md（定義）+ scripts/（実装）の分離
3. **Command の作成**: YAML フロントマター + 手順書形式
4. **Git CLI 活用**: `git log`, `git diff` でのデータ取得
5. **GitHub CLI 活用**: `gh pr diff`, `gh pr view` での PR 操作
