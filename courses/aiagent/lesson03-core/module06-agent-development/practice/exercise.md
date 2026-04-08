# 演習: エージェント開発

![エージェント開発ワークフロー](images/exercise-hero.png)

## 概要

Claude Code のカスタム Agent、Skill、Command を自分で開発する方法を学びます。日報生成コマンドとコードレビュースキルという2つの実用的なツールを作成し、Claude Code の拡張方法を体験します。

## 前提条件

- Claude Code が使えること
- Git の基本操作ができること
- `.claude/` ディレクトリの構造を理解していること
- Python 3.8+ が利用可能

## タスク

### タスク 1: 日報生成コマンド開発

Git のコミットログから自動で日報を生成するコマンドを作成します。

1. `data/agent-requirements.md` の仕様書を確認する
2. `templates/command-template.md` を参考に、`/daily-report` コマンドを作成する
3. コマンドの処理フローを設計する:
   - `git log` で当日のコミットを取得
   - コミットメッセージを分類（機能追加、バグ修正、リファクタリング等）
   - Markdown 形式の日報を生成
4. 実際にコマンドファイルを `.cursor/commands/utility/daily-report.md` として作成する

### タスク 2: コードレビュースキル開発

PR の差分を分析してレビューレポートを生成するスキルを作成します。

1. `templates/skill-template/SKILL.md` のテンプレートを確認する
2. `templates/skill-template/scripts/main.py` のスクリプト骨格を確認する
3. 以下の機能を実装する:
   - `gh pr diff` で PR の差分を取得
   - 変更ファイル数、追加行数、削除行数を集計
   - ファイルタイプ別の変更サマリーを生成
   - レビューポイント（大規模変更、テスト不足等）を検出
4. スキルディレクトリを `skills/code-review/` に作成する
5. `SKILL.md` 先頭に YAML frontmatter（name, description, version, author, dependencies）を入れ、Description / Quick Start / Parameters / Output Example セクションを記載する

### タスク 3: エージェント定義ファイル作成

日報生成エージェントの定義ファイルを作成します。

1. `templates/agent-template.md` を参考にする
2. `.claude/agents/daily-reporter.md` を作成し、先頭に name / description の YAML frontmatter を入れる
3. システムプロンプトでエージェントの役割、使用ツール、出力形式を定義する

## 完了条件

- [ ] タスク 1: `/daily-report` コマンドが作成され、実行できる
- [ ] タスク 2: コードレビュースキルが作成され、SKILL.md と main.py がある
- [ ] タスク 3: エージェント定義ファイルが作成されている
- [ ] 各ファイルが適切なディレクトリに配置されている

## ヒント

- 詳しくは `hints.md` を参照してください
- コマンドは Markdown ファイルで、主に Cursor / Claude Code の command 導線で使います
- スキルは SKILL.md（説明）+ scripts/（実装）の構成
- エージェントは `.claude/agents/` に配置する Markdown ファイル
