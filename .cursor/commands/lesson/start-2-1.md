---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
duration: "約25分"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["diagram", "flowchart", "gemini"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 2-1: フロー図生成

## 📍 このセッションでやること

**Lesson 2-1: フロー図生成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | diagram-generatorスキルで経費精算などの業務フロー図を作成する |
| 所要時間 | 約25分 |
| 使うスキル | diagram-generator (Gemini Image Generation API) |
| 前提条件 | Gemini APIキー設定済み、Python環境セットアップ済み |
| 教材ページ | [Module 2: 図表・フロー](https://ai-agent.camp/ja/course/module-2) を並行参照 |

**このセッションの流れ:**
1. フロー図の基本要素を理解する
2. シンプルなフロー図を作成する
3. 応用フロー図に挑戦する

セッション終了時には、業務フローを図解した画像が outputs に保存されています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

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

## 🚀 Step 1: フロー図の基本要素を理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: フロー図の基本要素を理解する",
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
フローチャートで使用する基本的な図形と、その意味を教えてください。
開始/終了、処理、判断、データ、矢印などを説明してください。
```

**期待される結果**: フロー図の基本要素が説明されます：
- 開始/終了: 楕円形
- 処理: 長方形
- 判断: ひし形
- データ: 平行四辺形
- 矢印: プロセスの流れ

---

## 🚀 Step 2: シンプルなフロー図を作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: シンプルなフロー図を作成する",
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
diagram-generatorを使って、経費精算の申請承認フローを図解してください：

1. 申請者が経費申請を提出
2. 上司が確認
3. 承認または却下
4. 承認の場合、経理部が処理
5. 却下の場合、申請者に差戻し

出力先: ~/ai-agent-camp/output/flow-expense.png
```

**期待される結果**: 判断分岐を含む経費精算フローの図が生成されます。

---

## 🚀 Step 3: 条件分岐を含む複雑なフローを作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 条件分岐を含む複雑なフローを作成する",
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
採用選考プロセスのフロー図を作成してください：

応募受付 → 書類審査 → 合格？
  → Yes: 一次面接 → 合格？
    → Yes: 二次面接 → 合格？
      → Yes: 内定通知
      → No: 見送り通知
    → No: 見送り通知
  → No: 見送り通知

判断分岐が明確にわかるようにしてください。
出力先: ~/ai-agent-camp/output/flow-recruitment.png
```

**期待される結果**: 複数の判断分岐がある採用フローが可視化されます。

---

## 🚀 Step 4: 練習課題 - 商品発注プロセス

以下のプロンプトで、実践的なフロー図を作成してみましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 練習課題 - 商品発注プロセス",
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
商品発注プロセスのフロー図を作成してください：

在庫確認 → 在庫不足？
  → Yes: 発注書作成 → 承認依頼 → 承認？
    → Yes: 発注実行 → 納品待ち → 納品確認 → 検収 → 支払い処理
    → No: 発注書修正（発注書作成に戻る）
  → No: 在庫補充なし（終了）

出力先: ~/ai-agent-camp/output/flow-order.png
```

**期待される結果**: ループ処理を含む発注プロセスが図解されます。

---

## 🚀 Step 5: 練習課題 - バグ修正ワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 練習課題 - バグ修正ワークフロー",
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
ソフトウェアのバグ修正ワークフローを図解してください：

バグ報告 → トリアージ → 優先度判定
  → 高優先度: 即時対応チームへ割り当て
  → 中優先度: 次スプリントに追加
  → 低優先度: バックログに登録

その後、共通フロー：
修正作業 → コードレビュー → 承認？
  → Yes: テスト → 合格？
    → Yes: リリース
    → No: 修正作業に戻る
  → No: 修正作業に戻る

出力先: ~/ai-agent-camp/output/flow-bugfix.png
```

**期待される結果**: 複数の分岐と戻りループを含むワークフローが図解されます。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "フローが複雑すぎて読みにくい"},
      {"id": "trouble_2", "label": "条件分岐が不明確"},
      {"id": "trouble_3", "label": "矢印の方向が分かりにくい"},
      {"id": "trouble_4", "label": "図が生成されない"}
    ]
  }]
}
```


### トラブル1: 「フローが複雑すぎて読みにくい」
**原因**: 一つの図に情報を詰め込みすぎている
**解決プロンプト**:
```
このフローをサブプロセスに分割してください。
メインフローと詳細フローに分けて、それぞれ別の図として作成してください。
```

### トラブル2: 「条件分岐が不明確」
**原因**: 判断条件の表現が曖昧
**解決プロンプト**:
```
判断分岐の条件を明確にしてください：
- 「承認？」→「金額が10万円以下？」
- 「合格？」→「面接評価がA以上？」
具体的な判断基準を図に記載してください。
```

### トラブル3: 「矢印の方向が分かりにくい」
**原因**: フローの流れが複雑で追いづらい
**解決プロンプト**:
```
フローの流れを左から右、上から下に統一してください。
戻りループは点線で表現してください。
```

### トラブル4: 「図が生成されない」
**原因**: diagram-generatorの実行環境に問題がある
**解決プロンプト**:
```
diagram-generatorの動作確認をしてください。
必要なパッケージがインストールされているか確認し、
エラーメッセージがあれば表示してください。
```

---

## ✅ チェックポイント
- [ ] フロー図の基本要素（開始/終了、処理、判断、矢印）を理解した
- [ ] シンプルな直線的フローを作成できた
- [ ] 条件分岐を含むフローを作成できた
- [ ] 練習課題（商品発注）を完了した
- [ ] 練習課題（バグ修正ワークフロー）を完了した


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/diagrams/
├── flow-{テーマ名}.png
└── (バリエーション)
```
> 形式: PNG | サイズ: 自動設定

### 確認コマンド
```bash
# ファイル一覧
ls -la output/diagrams/

# 画像を開く（macOS: open / Linux: xdg-open）
open output/diagrams/
```

> 💡 **Claude Code**: Read ツールでファイルパスを指定するとチャット内で画像プレビューできます
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-2-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-2-2
- finish → 終了
