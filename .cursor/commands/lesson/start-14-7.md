---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "40分"
prerequisites: ["start-14-1", "start-14-2", "start-14-3", "start-14-4", "start-14-5", "start-14-6"]
level: "advanced"
tags: ["article", "parallel"]
---

# 🎓 Lesson 14-7: 並列実行と仕上げ - 複数記事の同時処理

## 📍 このセッションでやること

**Lesson 14-7: 並列実行と仕上げ - 複数記事の同時処理** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 複数のテーマで記事を並列生成し、全工程を一括実行する方法を学ぶ |
| 所要時間 | 約40分 |
| 使うスキル | article-writer, style-analyzer, proofreading-agent, fact-checker, nanobanana, diagram-generator |
| 前提条件 | Lesson 14-1〜Lesson 14-6 完了済み（全工程の理解） |
| 教材ページ | [Module 14: 記事作成](https://ai-agent.camp/ja/course/module-14) を並行参照 |

**このセッションの流れ:**
1. 複数テーマを設定する
2. Task toolを使った並列記事生成を実演する
3. 各記事の校閲・ファクトチェックを並列実行する
4. 全記事の最終確認と出力

セッション終了時には、複数テーマの記事が並列で完成し、全工程の一括実行パターンを習得しています。

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
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 複数テーマの設定

Codex では通常チャットで選択肢を提示しながらでテーマ数を選びます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: テーマ数を選ぶ",
  "questions": [{
    "id": "theme_count",
    "prompt": "並列生成するテーマ数を選んでください",
    "options": [
      {"id": "two", "label": "2テーマ（初心者向け・処理時間短め）"},
      {"id": "three", "label": "3テーマ（標準・並列処理の効果を体感）"},
      {"id": "custom", "label": "テーマを自分で指定する"}
    ]
  }]
}
```

**「2テーマ」の場合:**
入力内容:
```text
以下の2テーマで記事の並列生成を行います。

テーマA: 「リモートワークの生産性を上げる5つのコツ」
- ターゲット: 在宅勤務中のビジネスパーソン
- 記事タイプ: ブログ記事
- 想定文字数: 2500〜3000字

テーマB: 「AI時代に求められるスキルとは」
- ターゲット: キャリアアップを考える20〜30代
- 記事タイプ: 解説記事
- 想定文字数: 3000〜3500字

各テーマのアウトラインをoutput/batch/theme-a-outline.md、theme-b-outline.mdに保存してください。
```

**「3テーマ」の場合:**
```text
以下の3テーマで並列生成を行います。

テーマA: 「リモートワークの生産性を上げる5つのコツ」
テーマB: 「AI時代に求められるスキルとは」
テーマC: 「チーム効率を高めるコミュニケーション術」

各テーマのアウトラインをoutput/batch/に保存してください。
```

**期待される結果**: 複数テーマのアウトラインがoutput/batch/に生成されます。

---

## 🚀 Step 2: Task toolを使った並列記事生成

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 並列記事生成を実行する",
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
```text
Task toolを使って、複数テーマの記事を並列生成してください。

各テーマに対して以下の工程を並列実行します：
1. アウトライン → ドラフト生成（article-writer + style-analyzer）
2. 挿絵マーカーの検出と画像生成（nanobanana / diagram-generator）
3. 画像の埋め込み

並列実行パターン:
- Task 1: テーマAの記事生成（output/batch/theme-a-draft.md）
- Task 2: テーマBの記事生成（output/batch/theme-b-draft.md）
（3テーマの場合は Task 3 も追加）

スタイルプロファイルは共通で output/style_profile.yaml を使用してください。
全タスク完了後、結果をoutput/batch/に保存してください。
```

**期待される結果**: 複数テーマの記事ドラフトが並列で生成され、処理時間が逐次実行より短縮されます。

---

## 🚀 Step 3: 校閲・ファクトチェックの並列実行

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 校閲・ファクトチェックを並列実行する",
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
```text
各記事に対して校閲とファクトチェックを並列実行してください。

並列実行パターン:
- Task 1: テーマAの校閲（proofreading-agent）
- Task 2: テーマBの校閲（proofreading-agent）
- Task 3: テーマAのファクトチェック（fact-checker）※校閲完了後
- Task 4: テーマBのファクトチェック（fact-checker）※校閲完了後

各タスクの結果:
- output/batch/theme-a-proofread.md
- output/batch/theme-b-proofread.md
- output/batch/theme-a-final.md
- output/batch/theme-b-final.md

処理の流れ: 校閲 → ファクトチェック → 出典追加 → 最終版保存
```

**期待される結果**: 全記事の校閲・ファクトチェックが並列で完了し、最終版が保存されます。

---

## 🚀 Step 4: 全記事の最終確認と出力

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 最終確認と出力",
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
```text
output/batch/ の全記事について、最終レポートを作成してください。

レポート内容:
1. 各記事のサマリー
   - テーマ、文字数、挿絵数、出典数
2. 品質スコア
   - 校閲指摘の修正率
   - ファクトチェック通過率
3. 並列処理の効率
   - 逐次実行との時間比較（推定）
   - 並列処理で節約された時間
4. 全記事の一覧（ファイルパス付き）

レポートをoutput/batch/batch-report.mdに保存してください。

また、Module 14全体の学習内容を振り返るサマリーも表示してください：
- Lesson 14-1: テーマ設定・アウトライン
- Lesson 14-2: スタイルプロファイル
- Lesson 14-3: スタイル適用ドラフト
- Lesson 14-4: 挿絵生成
- Lesson 14-5: 校閲
- Lesson 14-6: ファクトチェック
- Lesson 14-7: 並列実行（今回）
```

**期待される結果**: 全記事の最終レポートと、Module 14の学習サマリーが出力されます。

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
      {"id": "trouble_1", "label": "並列タスクの一部が失敗する"},
      {"id": "trouble_2", "label": "処理時間が長すぎる"},
      {"id": "trouble_3", "label": "記事間でスタイルがバラバラになる"},
      {"id": "trouble_4", "label": "output/batch/ にファイルが見つからない"}
    ]
  }]
}
```


### トラブル1: 「並列タスクの一部が失敗する」
**原因**: APIレート制限、または1つのタスクのエラーが他に影響
**解決プロンプト**:
```text
失敗したタスクだけを再実行してください。
APIレート制限の場合は30秒待ってから再実行してください。
成功したタスクの結果は保持されています。
失敗したテーマのファイルパスを確認: ls output/batch/
```

### トラブル2: 「処理時間が長すぎる」
**原因**: テーマ数が多い、または記事の文字数が長い
**解決プロンプト**:
```text
以下で処理時間を短縮できます：
1. テーマ数を2つに減らす
2. 各記事の想定文字数を2000字以内に設定する
3. 挿絵生成をスキップする（後から追加可能）
4. 校閲とファクトチェックを「重要度高のみ」に限定する
```

### トラブル3: 「記事間でスタイルがバラバラになる」
**原因**: 各タスクが独立してスタイルを解釈している
**解決プロンプト**:
```text
全記事で同じスタイルプロファイル（output/style_profile.yaml）を
明示的に指定してください。
各タスクの--styleオプションにプロファイルパスを必ず含めてください。
生成後にスタイルの一貫性チェックを追加で実行することも可能です。
```

### トラブル4: 「output/batch/ にファイルが見つからない」
**原因**: ディレクトリが存在しない
**解決プロンプト**:
```bash
ディレクトリを作成してから再実行してください：
mkdir -p ~/ai-agent-camp/output/batch
```

---

## ✅ チェックポイント
- [ ] 複数テーマ（2〜3本）のアウトラインを設定した
- [ ] Task toolで記事ドラフトを並列生成できた
- [ ] 校閲・ファクトチェックを並列実行できた
- [ ] 全記事の最終版がoutput/batch/に保存された
- [ ] バッチレポートで品質と効率を確認した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── article-14-7-*.md  (記事ドキュメント)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/article-14-7-*.md

# 冒頭を確認（最初の30行）
head -30 output/article-14-7-*.md
```

> 💡 全文を確認: `cat output/article-14-7-*.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでModule 14: 記事作成の全レッスンが完了です！

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-15-1）"},
      {"id": "review_module", "label": "Module 14を復習する"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-15-1
- review_module → Module 14の各レッスンを振り返る
- finish → 終了
