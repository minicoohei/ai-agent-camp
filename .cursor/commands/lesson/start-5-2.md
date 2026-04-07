---
description: "When the user says /start-5-2 — Module 5 Lesson 5-2: PPTX編集と自動生成"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
prerequisites: ["start-5-1"]
duration: "約30分"
level: "intermediate"
tags: ["pptx", "generation", "automation", "document"]
---

# 🎓 Lesson 5-2: PPTX編集と自動生成

## 📍 このセッションでやること

**Lesson 5-2: PPTX編集・自動生成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | python-pptxで新規スライドの作成・テキスト編集・図形・表・画像の追加を行う |
| 所要時間 | 約30分 |
| 使うスキル | pptx_ops, generate_slide, document-processor |
| 前提条件 | Lesson 5-1 完了、Python環境セットアップ済み |
| 教材ページ | [Module 5: PPTX](https://ai-agent.camp/ja/course/module-5) を並行参照 |

**このセッションの流れ:**
1. 新規スライドの追加とテキスト編集
2. 図形・表・画像の追加
3. テンプレートからのスライド自動生成

セッション終了時には、プログラムからPPTXを編集・生成できるようになっています。

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

## 🚀 Step 1: 新規プレゼンテーションの作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 新規プレゼンテーションの作成",
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
python-pptxを使って、新しい16:9のプレゼンテーションを作成してください。
タイトルスライドを追加して、タイトルに「AIエージェント活用講座」、
サブタイトルに「2026年2月」と入力し、
~/ai-agent-camp/output/new_presentation.pptx として保存してください。
```

**期待される結果**: 新しいPPTXファイルが作成され、タイトルスライドが含まれています。

---

## 🚀 Step 2: コンテンツスライドの追加

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: コンテンツスライドの追加",
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
先ほど作成したPPTXに、以下の内容でコンテンツスライドを追加してください：

スライド2:
- タイトル: 「本日のアジェンダ」
- 箇条書き:
  1. AIエージェントとは
  2. Claude Codeの活用方法
  3. 実践ワークショップ
  4. 質疑応答

スライド3:
- タイトル: 「AIエージェントとは」
- 箇条書き:
  1. 自律的にタスクを実行するAI
  2. ユーザーの指示を理解して行動
  3. 複数のツールを組み合わせ可能
```

**期待される結果**: 箇条書き形式のスライドが追加されます。

---

## 🚀 Step 3: 表の追加

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 表の追加",
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
PPTXに新しいスライドを追加し、以下のデータで表を作成してください：

タイトル: 「機能比較表」

| 機能 | Claude Code | 従来ツール |
|------|------------|----------|
| 自然言語対応 | ◯ | △ |
| コード生成 | ◯ | × |
| ファイル操作 | ◯ | △ |
| 学習コスト | 低 | 高 |

ヘッダー行は太字で、見やすいスタイルを適用してください。
```

**期待される結果**: 表を含むスライドが追加されます。

---

## 🚀 Step 4: 図形とデザイン要素の追加

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 図形とデザイン要素の追加",
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
PPTXに新しいスライドを追加し、以下のデザイン要素を追加してください：

- タイトル: 「ワークフロー」
- 3つの四角形を横並びに配置
- 各四角形に「入力」「処理」「出力」のテキスト
- 四角形の間に矢印を配置
- 背景色: 青系統のグラデーション

プロフェッショナルなフロー図のデザインにしてください。
```

**期待される結果**: 図形を使ったフロー図が作成されます。

---

## 🚀 Step 5: テンプレートからの自動生成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: テンプレートからの自動生成",
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
以下のJSON形式のデータから、自動的にプレゼンテーションを生成してください：

{
  "title": "四半期レポート",
  "subtitle": "2026年Q1",
  "author": "営業部",
  "slides": [
    {
      "type": "content",
      "title": "売上実績",
      "points": ["目標達成率: 115%", "前年比: +20%", "新規顧客: 50社"]
    },
    {
      "type": "content",
      "title": "今後の計画",
      "points": ["新製品投入", "海外展開", "DX推進"]
    }
  ]
}

出力: ~/ai-agent-camp/output/quarterly_report.pptx
```

**期待される結果**: JSONデータから自動的にプレゼンテーションが生成されます。

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
      {"id": "trouble_1", "label": "レイアウトインデックスが範囲外"},
      {"id": "trouble_2", "label": "日本語フォントが表示されない"},
      {"id": "trouble_3", "label": "画像の縦横比が崩れる"},
      {"id": "trouble_4", "label": "表のセル幅が均等にならない"}
    ]
  }]
}
```


### トラブル1: 「レイアウトインデックスが範囲外」
**原因**: 使用しようとしているレイアウトが存在しない
**解決プロンプト**:
```
利用可能なすべてのレイアウトとそのインデックスを表示してください。
prs.slide_layouts のリストを確認したいです。
```

### トラブル2: 「日本語フォントが表示されない」
**原因**: フォント指定の問題
**解決プロンプト**:
```
スライドのテキストに日本語フォント「メイリオ」を適用してください。
paragraph.font.name = "Meiryo" の設定方法を教えてください。
```

### トラブル3: 「画像の縦横比が崩れる」
**原因**: 幅と高さの両方を指定している
**解決プロンプト**:
```
画像を挿入する際、縦横比を維持したまま挿入する方法を教えてください。
widthのみを指定する方法でお願いします。
```

### トラブル4: 「表のセル幅が均等にならない」
**原因**: 列幅が自動計算されている
**解決プロンプト**:
```
表の各列の幅を明示的に設定する方法を教えてください。
table.columns[i].width の設定でお願いします。
```

---

## ✅ チェックポイント
- [ ] 新規プレゼンテーションを作成できた
- [ ] タイトルスライドを追加できた
- [ ] 箇条書きコンテンツを追加できた
- [ ] 表を作成して配置できた
- [ ] 図形（四角形、矢印）を配置できた
- [ ] JSONデータから自動生成できた
- [ ] ファイルを正しく保存できた


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/
└── presentation.pptx  (PowerPointプレゼンテーション)
    スライド数: N枚
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/presentation.pptx

# PowerPointで開く（macOS: open / Linux: xdg-open）
open output/presentation.pptx
```

> 💡 スライド数確認: `python3 -c "from pptx import Presentation; p=Presentation('output/presentation.pptx'); print(f'スライド数: {len(p.slides)}')"`

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-6-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-6-1
- finish → 終了
