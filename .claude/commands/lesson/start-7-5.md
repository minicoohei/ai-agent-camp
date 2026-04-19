---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "約30分"
prerequisites: ["start-6-1", "start-6-2"]
level: "intermediate"
tags: ["skill", "command", "agent", "analysis"]
---

# 🎓 Lesson 7-5: 既存Skill/Commandの構造理解と分析

## 📍 このセッションでやること

**Lesson 7-5: 既存Skill/Commandの構造理解と分析** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 既存のSkillとCommandの構造を理解し、自分で作成できるようになるための基礎知識を得る |
| 所要時間 | 約30分 |
| 使うスキル | ファイルシステム探索、Markdown |
| 前提条件 | Lesson 6-1・Lesson 6-2 完了（エージェント開発モジュールのCommand/Skill基礎） |

**このセッションの流れ:**
1. `.cursor/commands/` と `.claude/commands/` の構造を探索
2. `skills/` の構造を探索（SKILL.md、scripts/）
3. 既存コマンドの共通パターンを分析（frontmatter、Step構造、チェックリスト）
4. 既存スキルの共通パターンを分析（SKILL.md構造、スクリプト連携）

セッション終了時には、SkillとCommandの設計パターンを体系的に理解し、自分で作成するための知識が身についています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 前提条件の確認を実行)
(view_html → 教材ページURL https://ai-agent.camp/ja/course/module-7 を案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Commandディレクトリの構造を探索する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Commandディレクトリの構造を探索する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

Commandは2つの場所に配置されます：
- `.cursor/commands/` — 現在のワークスペース 用のカスタムコマンド
- `.claude/commands/` — Claude Code 用のカスタムコマンド

入力内容:
```
以下のディレクトリ構造を調べて、レポートを作成してください：

1. .cursor/commands/ のサブディレクトリ一覧と各ディレクトリのファイル数
2. .claude/commands/ のサブディレクトリ一覧と各ディレクトリのファイル数
3. コマンドファイルの命名規則（start-X-Y.md のパターン）

それぞれのディレクトリの役割の違いも説明してください：
- lesson/ → レッスン用コマンド（学習カリキュラムに紐づく）
- utility/ → ユーティリティコマンド（汎用ツール）
```

**期待される結果**: Commandディレクトリの全体像が把握でき、lesson/とutility/の使い分けが理解できる。

---

## 🚀 Step 2: Skillディレクトリの構造を探索する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Skillディレクトリの構造を探索する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

Skillは `skills/` に配置され、各スキルは独立したディレクトリです。

入力内容:
```
skills/ ディレクトリを探索して、以下をレポートしてください：

1. スキル一覧（ディレクトリ名）とそれぞれの概要
2. 各スキルディレクトリの共通構造を分析：
   - SKILL.md の有無
   - scripts/ ディレクトリの有無
   - その他のファイル（references/, templates/ 等）

3. 代表的なスキルを3つ選び、それぞれのディレクトリ構造をツリー表示：
   - banner-creator（画像生成系）
   - data-analyst（データ分析系）
   - check-inbox（通信系）

4. SKILL.md の共通セクションを抽出してください：
   - どのスキルにも共通するセクション
   - スキルによって異なるセクション
```

**期待される結果**: Skillディレクトリの標準構造（SKILL.md + scripts/ + 任意ファイル）が理解できる。

---

## 🚀 Step 3: 既存コマンドの共通パターンを分析する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 既存コマンドの共通パターンを分析する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

レッスンコマンドには共通の「型」があります。この型を理解すれば、自分でコマンドを量産できます。

入力内容:
```
以下の3つのレッスンコマンドを読み、共通パターンを分析してください：

1. .cursor/commands/lesson/start-6-1.md
2. .cursor/commands/lesson/start-7-1.md
3. .cursor/commands/lesson/start-1-1.md

以下の観点で分析し、「コマンドテンプレート」を作成してください：

### YAML Frontmatter の共通項目
- description, duration, prerequisites, level, tags の書き方

### 本文の共通構造
- 📍 このセッションでやること（テーブル形式）
- 🎯 準備チェック（AskQuestion）
- 🚀 Step N:（各ステップの構造）
- ⚠️ よくあるトラブル
- ✅ チェックポイント / 完了チェック
- ➡️ 次のステップ

### AskQuestion パターン
- 各Stepの3択（practice / review / skip）
- トラブル選択
- 次のステップ選択

分析結果を「コマンド作成チートシート」としてまとめてください。
```

**期待される結果**: レッスンコマンドの共通パターンが抽出され、再利用可能なチートシートが完成する。

---

## 🚀 Step 4: 既存スキルの共通パターンを分析する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 既存スキルの共通パターンを分析する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

SKILL.mdはスキルの「設計書」であり、AIエージェントがスキルを理解するための最も重要なファイルです。

入力内容:
```
以下の3つのスキルのSKILL.mdを読み、共通パターンを分析してください：

1. skills/banner-creator/SKILL.md
2. skills/data-analyst/SKILL.md
3. skills/check-inbox/SKILL.md

以下の観点で分析し、「SKILL.md テンプレート」を作成してください：

### SKILL.md の標準構造
- メタデータ（name, description, version, dependencies）
- 概要/目的セクション
- クイックスタート（コマンド例）
- パラメータ/オプション
- 出力例
- トラブルシューティング

### scripts/ ディレクトリとの連携パターン
- SKILL.md から scripts/ のPythonスクリプトをどう参照するか
- スクリプトの入出力パターン（CLI引数、ファイル入力、標準出力）

### Progressive Disclosure の実践
- 第1段階（メタデータ）: 100語以内の説明
- 第2段階（SKILL.md本文）: 5,000語以内の詳細
- 第3段階（scripts/references/）: 必要時のみ読み込み

分析結果を「SKILL.md作成チートシート」としてまとめてください。
```

**期待される結果**: SKILL.mdの標準パターンが抽出され、再利用可能なテンプレートが完成する。

---

## ⚠️ よくあるトラブルと解決方法

Codex では通常チャットで選択肢を提示しながらでトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "ディレクトリ構造が複雑で理解できない"},
      {"id": "trouble_2", "label": "CommandとSkillの違いが分からない"},
      {"id": "trouble_3", "label": "SKILL.mdの書き方が分からない"},
      {"id": "trouble_4", "label": "パターン分析の観点が分からない"}
    ]
  }]
}
```

### トラブル1: ディレクトリ構造が複雑で理解できない
**原因**: 多数のスキル・コマンドが存在し、全体像が見えにくい
**解決プロンプト**:
```
まずは以下の2つだけに注目してください：
1. .cursor/commands/lesson/ の中の start-1-1.md（最もシンプルなレッスン）
2. skills/banner-creator/（最もシンプルなスキル）
この2つの構造を完全に理解してから、他に広げましょう。
```

### トラブル2: CommandとSkillの違いが分からない
**原因**: 両方ともMarkdownファイルで似ている
**解決プロンプト**:
```
簡単に言うと：
- Command = 「レシピ」（手順書）。ユーザーが /コマンド名 で呼び出す指示書
- Skill = 「道具箱」（ツールキット）。AIエージェントが自動的に使う能力

Commandは人間が読む、Skillはエージェントが読む、と覚えてください。
```

### トラブル3: SKILL.mdの書き方が分からない
**原因**: 具体的な記述例が不足
**解決プロンプト**:
```
最もシンプルなSKILL.mdの例として skills/banner-creator/SKILL.md を読んでください。
最低限必要なのは：名前、説明、使い方（コマンド例）の3つだけです。
```

### トラブル4: パターン分析の観点が分からない
**原因**: 何を比較すればよいか不明確
**解決プロンプト**:
```
以下の3つの質問に答える形で分析してください：
1. 「必ずあるもの」は何か？（共通構造）
2. 「あるものとないもの」は何か？（オプション要素）
3. 「書き方が違うもの」は何か？（バリエーション）
```

---

## ✅ チェックポイント
- [ ] .cursor/commands/ と .claude/commands/ のディレクトリ構造を確認した
- [ ] skills/ のディレクトリ構造を確認した
- [ ] レッスンコマンドの共通パターン（frontmatter、Step構造、AskQuestion）を分析した
- [ ] SKILL.mdの共通パターン（メタデータ、クイックスタート、パラメータ）を分析した
- [ ] 「コマンド作成チートシート」を作成した
- [ ] 「SKILL.md作成チートシート」を作成した


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 skills/{skill_name}/
├── SKILL.md  (スキル定義)
├── scripts/    (実行スクリプト)
└── tests/      (テストファイル)
```

### 確認コマンド
```bash
# スキルのディレクトリ構造を確認
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# SKILL.md の冒頭を確認
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ 完了チェック
以下をチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: 以下のチートシートが作成されているか確認してください：
# 1. コマンド作成チートシート（共通パターン、frontmatter、Step構造）
# 2. SKILL.md作成チートシート（標準構造、Progressive Disclosure）
```

**期待される結果**: 2つのチートシートが完成し、次のレッスンでCommand/Skillを自作する準備が整っている。

---

## 🎉 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

Codex では通常チャットで選択肢を提示しながらで選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-7-6）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-7-6
- finish → 終了
