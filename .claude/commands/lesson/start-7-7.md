---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "約40分"
prerequisites: ["start-7-5", "start-7-1"]
level: "intermediate"
tags: ["skill", "skill-design", "python", "SKILL.md"]
---

# 🎓 Lesson 7-7: SKILL.md駆動のスキル開発

## 📍 このセッションでやること

**Lesson 7-7: SKILL.md駆動のスキル開発** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | SKILL.mdを核としたスキルを1つゼロから作成する |
| 所要時間 | 約40分 |
| 使うスキル | SKILL.md、Python |
| 前提条件 | Lesson 7-5 完了（構造理解）、Lesson 7-1 完了推奨（スキル設計基礎） |

**このセッションの流れ:**
1. スキルのアイデアを決める（AskUserQuestion使用）
2. SKILL.mdのドラフト作成（目的、入出力、使い方）
3. scripts/ ディレクトリにPythonスクリプト実装
4. SKILL.mdを最終版に仕上げ（Anthropicベストプラクティス準拠）
5. 動作テスト

セッション終了時には、自分だけのオリジナルスキルが完成し、`skills/` の正本として管理できる状態になっています。

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

## 🚀 Step 1: スキルのアイデアを決める

まずはどんなスキルを作るか決めましょう。以下のカテゴリから選ぶか、自分のアイデアを入力してください。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: スキルのアイデアを決める",
  "questions": [{
    "id": "skill_idea",
    "prompt": "どんなスキルを作りたいですか？",
    "options": [
      {"id": "doc_creation", "label": "Document Creation（文書生成系）"},
      {"id": "workflow_auto", "label": "Workflow Automation（作業自動化系）"},
      {"id": "data_processing", "label": "Data Processing（データ処理系）"},
      {"id": "custom", "label": "自分のアイデアで作りたい（入力する）"}
    ]
  }]
}
```

**各カテゴリのアイデア例:**

### Document Creation（文書生成系）
| スキル名 | 概要 | 入力 | 出力 |
|----------|------|------|------|
| changelog-generator | Git履歴からCHANGELOG生成 | Gitリポジトリ | CHANGELOG.md |
| email-drafter | 用件からメール文面生成 | 要点メモ | メール本文 |
| invoice-generator | 請求書自動生成 | 顧客情報+明細 | PDF/Markdown |

### Workflow Automation（作業自動化系）
| スキル名 | 概要 | 入力 | 出力 |
|----------|------|------|------|
| file-organizer | ファイル整理・リネーム | ディレクトリ | 整理後のツリー |
| csv-transformer | CSV形式変換・クリーニング | CSV | 変換済みCSV |
| git-branch-cleanup | 不要ブランチの一括整理 | Gitリポジトリ | レポート |

### Data Processing（データ処理系）
| スキル名 | 概要 | 入力 | 出力 |
|----------|------|------|------|
| log-analyzer | ログファイル分析・要約 | ログファイル | 分析レポート |
| json-schema-validator | JSONスキーマ検証 | JSON+スキーマ | 検証結果 |
| text-summarizer | 長文テキストの要約 | テキスト | 要約 |

入力内容（自分のアイデアの場合）:
```
以下の情報でスキルのアイデアを具体化してください：

1. スキル名（英語、ハイフン区切り）: 例: changelog-generator
2. 一言説明: 例: Git履歴からCHANGELOGを自動生成する
3. カテゴリ: Document Creation / Workflow Automation / Data Processing
4. 入力: 何を受け取るか
5. 出力: 何を生成するか
6. 誰が使うか: エンジニア / PM / デザイナー / 全員
7. 既存スキルとの違い: このプロジェクトの既存スキルと重複しないか

スキル名とカテゴリが決まったら、Step 2に進みます。
```

**期待される結果**: 作成するスキルの名前、カテゴリ、入出力が明確になる。

---

## 🚀 Step 2: SKILL.mdのドラフト作成

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: SKILL.mdのドラフト作成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める（自分のスキルで作成）"},
      {"id": "review", "label": "例だけ確認する（サンプルSKILL.mdを見る）"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

SKILL.mdは以下の構造で作成します。Progressive Disclosureに基づき、メタデータは100語以内、本文は5,000語以内に収めます。

入力内容（例: changelog-generator の場合）:
```
以下のディレクトリとファイルを作成してください：

mkdir -p skills/[スキル名]/scripts

次に、skills/[スキル名]/SKILL.md を以下の構造で作成：

---
name: [スキル名]
description: "[一言説明]"
version: 1.0.0
author: [あなたの名前]
dependencies:
  python: "3.9+"
  packages: ["必要なパッケージ"]
---

# /[スキル名] - [スキルの表示名]

## 概要
[2-3文でスキルの目的と価値を説明]

## クイックスタート

### 基本的な使い方
```bash
python skills/[スキル名]/scripts/main.py --input [入力] --output [出力]
```

### オプション付き
```bash
python skills/[スキル名]/scripts/main.py --input [入力] --format markdown --verbose
```

## パラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|-----------|------|-----------|------|
| --input | はい | - | 入力ファイル/ディレクトリ |
| --output | いいえ | stdout | 出力先（ファイルパスまたは stdout） |
| --format | いいえ | markdown | 出力形式（markdown / json / text） |
| --verbose | いいえ | false | 詳細ログ出力 |

## 出力例

[実際の出力サンプルを記載]

## トリガーフレーズ

このスキルは以下のようなリクエストで発動します：
- 「[フレーズ1]」
- 「[フレーズ2]」
- 「[フレーズ3]」

## 注意事項
- [制約事項1]
- [制約事項2]
```

**期待される結果**: SKILL.mdのドラフトが完成し、スキルの全体設計が明確になる。

---

## 🚀 Step 3: Pythonスクリプトの実装

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: Pythonスクリプトの実装",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める（自分のスキル用スクリプトを作成）"},
      {"id": "review", "label": "例だけ確認する（サンプルスクリプトを見る）"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:

scripts/main.py は以下の標準パターンで実装します。

入力内容:
```
skills/[スキル名]/scripts/main.py を作成してください。

以下のパターンに従って実装してください：

#!/usr/bin/env python3
"""
[スキル名] - [一言説明]

Usage:
    python main.py --input <入力> [--output <出力>] [--format <形式>]
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_args():
    """コマンドライン引数のパース"""
    parser = argparse.ArgumentParser(
        description="[スキルの説明]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --input data.csv
    python main.py --input data.csv --output report.md --format markdown
        """
    )
    parser.add_argument("--input", "-i", required=True, help="入力ファイルパス")
    parser.add_argument("--output", "-o", default=None, help="出力ファイルパス（省略時は標準出力）")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "text"], default="markdown", help="出力形式")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細ログ出力")
    parser.add_argument("--test", action="store_true", help="テストモードで実行")
    return parser.parse_args()


def validate_input(input_path: str) -> Path:
    """入力ファイルの存在確認"""
    path = Path(input_path)
    if not path.exists():
        print(f"エラー: 入力ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)
    return path


def process(input_path: Path, output_format: str, verbose: bool) -> str:
    """メイン処理（ここにスキル固有のロジックを実装）"""
    if verbose:
        print(f"処理中: {input_path}", file=sys.stderr)

    # TODO: ここにスキル固有の処理を実装
    result = f"# 処理結果\n\n- 入力: {input_path}\n- 形式: {output_format}\n- 処理日時: {datetime.now().isoformat()}\n"

    return result


def output_result(result: str, output_path: str = None):
    """結果の出力"""
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(result, encoding="utf-8")
        print(f"出力完了: {output_path}", file=sys.stderr)
    else:
        print(result)


def run_test():
    """テストモード"""
    print("=== テストモード ===")
    # テスト用のダミー入力で動作確認
    test_input = Path("/tmp/test_input.txt")
    test_input.write_text("テストデータ", encoding="utf-8")

    result = process(test_input, "markdown", verbose=True)
    print(result)
    print("=== テスト完了 ===")

    # クリーンアップ
    test_input.unlink(missing_ok=True)


def main():
    args = parse_args()

    if args.test:
        run_test()
        return

    input_path = validate_input(args.input)
    result = process(input_path, args.format, args.verbose)
    output_result(result, args.output)


if __name__ == "__main__":
    main()

---

上記のテンプレートの「TODO」部分に、あなたのスキル固有の処理を実装してください。
process() 関数の中身を、スキルの目的に合わせて書き換えます。
```

**期待される結果**: main.py が完成し、`python main.py --test` で動作確認できる。

---

## 🚀 Step 4: SKILL.mdを最終版に仕上げる

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: SKILL.mdを最終版に仕上げる",
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

Step 3で実装した内容を反映し、SKILL.mdを完成させます。Anthropicベストプラクティスに準拠しているかチェックします。

入力内容:
```
Step 2で作成したSKILL.mdを以下の観点で改善してください：

### Anthropicベストプラクティス チェックリスト

1. **Progressive Disclosure**
   - [ ] メタデータ（name + description）は100語以内か
   - [ ] SKILL.md本文は5,000語以内か
   - [ ] scripts/ は必要時のみ読み込む構成か

2. **トリガーの精度**
   - [ ] 正しく発動すべきフレーズが5つ以上あるか
   - [ ] 発動すべきでないフレーズが3つ以上あるか
   - [ ] 既存スキルとのトリガー衝突がないか

3. **入出力の明確さ**
   - [ ] 入力仕様（形式、必須/任意）が明記されているか
   - [ ] 出力サンプルが含まれているか
   - [ ] エラー時の挙動が説明されているか

4. **実用性**
   - [ ] クイックスタートのコマンド例がコピペで動くか
   - [ ] パラメータ表が完備されているか
   - [ ] 注意事項・制約事項が明記されているか

上記チェックリストに基づいてSKILL.mdを更新してください。
```

**期待される結果**: SKILL.mdがベストプラクティスに準拠した最終版になる。

---

## 🚀 Step 5: 動作テスト

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 動作テスト",
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

入力内容:
```
作成したスキルの動作テストを行ってください：

1. ディレクトリ構造の確認
   tree skills/[スキル名]/

   期待される構造:
   [スキル名]/
   ├── SKILL.md
   └── scripts/
       └── main.py

2. テストモードで実行
   python skills/[スキル名]/scripts/main.py --test

3. 実データで実行
   python skills/[スキル名]/scripts/main.py --input [実際のファイル] --verbose

4. エラーケースの確認
   python skills/[スキル名]/scripts/main.py --input nonexistent_file.txt
   → 適切なエラーメッセージが表示されるか

5. 出力形式の確認
   python skills/[スキル名]/scripts/main.py --input [ファイル] --format json
   python skills/[スキル名]/scripts/main.py --input [ファイル] --format text

すべてのテストが通ったら、スキルは完成です。
```

**期待される結果**: 正常系・異常系ともに期待通りの動作をする。

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
      {"id": "trouble_1", "label": "Pythonスクリプトが動かない"},
      {"id": "trouble_2", "label": "SKILL.mdの書き方が分からない"},
      {"id": "trouble_3", "label": "スキルがClaude Codeから認識されない"},
      {"id": "trouble_4", "label": "アイデアが思いつかない"}
    ]
  }]
}
```

### トラブル1: Pythonスクリプトが動かない
**原因**: パスや依存パッケージの問題
**解決プロンプト**:
```
以下を確認してください：
1. python3 --version が 3.9 以上か
2. 必要なパッケージがインストールされているか（uv add [パッケージ名]）
3. スクリプトの実行権限があるか（chmod +x scripts/main.py）
4. ファイルのエンコーディングがUTF-8か
```

### トラブル2: SKILL.mdの書き方が分からない
**原因**: テンプレートが抽象的
**解決プロンプト**:
```
最もシンプルなSKILL.mdは以下の3セクションだけで十分です：
1. メタデータ（name, description）
2. クイックスタート（コマンド例1つ）
3. パラメータ表
まずこの3つだけ書いて、後から肉付けしましょう。
```

### トラブル3: スキルがClaude Codeから認識されない
**原因**: ディレクトリ配置の問題
**解決プロンプト**:
```
スキルは skills/[スキル名]/ に配置する必要があります。
以下を確認してください：
1. SKILL.md が skills/[スキル名]/SKILL.md にあるか
2. ファイル名が正確に SKILL.md か（大文字小文字に注意）
3. Claude Code を再起動して /skill-name で呼び出してみてください
```

### トラブル4: アイデアが思いつかない
**原因**: スキルの概念が抽象的
**解決プロンプト**:
```
以下の質問に答えてみてください：
1. 昨日の業務で「面倒だな」と思ったことは？
2. 毎週同じ作業を繰り返していることは？
3. 「これ自動化できたらいいのに」と思ったことは？
その答えがスキルのアイデアです。
```

---

## ✅ チェックポイント
- [ ] スキルのアイデア（名前、カテゴリ、入出力）が決定した
- [ ] SKILL.mdのドラフトが作成された
- [ ] scripts/main.py が実装された
- [ ] SKILL.mdがAnthropicベストプラクティスに準拠している
- [ ] テストモード（--test）で動作確認済み
- [ ] 実データでの動作確認済み
- [ ] エラーケースの動作確認済み


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
# 完了確認: 以下を確認してください：
# 1. skills/[スキル名]/SKILL.md が存在するか
# 2. skills/[スキル名]/scripts/main.py が存在するか
# 3. python skills/[スキル名]/scripts/main.py --test が成功するか
```

**期待される結果**: スキルのディレクトリ構造が正しく、テストが通る。

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-7-8）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-7-8
- finish → 終了
