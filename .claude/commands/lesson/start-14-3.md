---
description: "When the user says /start-14-3 — Module 14 Lesson 14-3: 記事執筆 - スタイル適用ドラフト作成"
category: "lesson"
duration: "35分"
prerequisites: ["start-14-1", "start-14-2"]
level: "intermediate"
tags: ["article", "writing"]
---

# 🎓 Lesson 14-3: 記事執筆 - スタイル適用ドラフト作成

## 📍 このセッションでやること

**Lesson 14-3: 記事執筆 - スタイル適用ドラフト作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | スタイルプロファイルを適用して記事のドラフトを生成する |
| 所要時間 | 約35分 |
| 使うスキル | article-writer, style-analyzer |
| 前提条件 | Lesson 14-1（アウトライン）・Lesson 14-2（スタイルプロファイル）完了済み |
| 教材ページ | [Module 14: 記事作成](https://ai-agent.camp/ja/course/module-14) を並行参照 |

**このセッションの流れ:**
1. 16-1で作成したアウトラインと16-2のスタイルプロファイルを確認する
2. article-writerでスタイル適用ドラフトを生成する
3. ドラフトをレビューし、手動で調整する

セッション終了時には、あなたの文体が反映された記事ドラフト（Markdown形式）が完成しています。

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

## 🚀 Step 1: アウトラインとスタイルプロファイルの確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 前回の成果物を確認する",
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
以下の2つのファイルを読み込んで、記事執筆の準備状況を確認してください。

1. アウトライン: output/article-14-1-outline-final.md
2. スタイルプロファイル: output/style_profile.yaml

確認ポイント:
- アウトラインの見出し構成は適切か
- スタイルプロファイルの主要パラメータ（語尾、文長、口調）
- 両者の組み合わせで想定される記事のイメージ

問題があれば修正を提案してください。
```

**期待される結果**: アウトラインとスタイルプロファイルの内容が確認され、記事執筆の準備が整います。

---

## 🚀 Step 2: article-writerでスタイル適用ドラフト生成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: スタイル適用ドラフトを生成する",
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
article-writerスキルを使って、アウトラインとスタイルプロファイルを組み合わせた記事ドラフトを生成してください。

実行コマンド:
python skills/article-writer/scripts/article_writer.py --theme output/article-14-1-outline-final.md --style output/style_profile.yaml --output output/article-16-3-draft.md

生成条件:
- アウトライン: output/article-14-1-outline-final.md の構成に従う
- スタイル: output/style_profile.yaml の文体パラメータを適用
- 挿絵マーカー: <!-- illustration: ... --> をアウトラインの指定位置に維持
- 文字数: アウトラインで設定した想定文字数に合わせる

結果をoutput/article-16-3-draft.mdに保存してください。
```

**期待される結果**: あなたの文体が反映された記事ドラフトがMarkdown形式で生成されます。挿絵マーカーも適切な位置に配置されています。

---

## 🚀 Step 3: ドラフトのレビューと手動調整

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ドラフトをレビュー・調整する",
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
output/article-16-3-draft.mdのドラフトをレビューしてください。

以下の観点で確認し、フィードバックをお願いします：
1. 文体の一貫性: スタイルプロファイルの特徴が記事全体に反映されているか
2. 導入の引き込み: 最初の3行で読者の興味を引けているか
3. セクション間のつながり: 接続詞・導入文が自然か
4. 具体性: 抽象的すぎる箇所はないか
5. まとめ・CTA: 読者に行動を促せているか

修正したい箇所があれば指示してください。
修正を反映した最終ドラフトをoutput/article-16-3-draft-final.mdに保存します。
```

**期待される結果**: ドラフトのレビュー結果が示され、修正を反映した最終ドラフトが保存されます。

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
      {"id": "trouble_1", "label": "文体がスタイルプロファイルと合わない"},
      {"id": "trouble_2", "label": "記事が長すぎる・短すぎる"},
      {"id": "trouble_3", "label": "挿絵マーカーが消えてしまった"},
      {"id": "trouble_4", "label": "前回のファイルが見つからない"}
    ]
  }]
}
```


### トラブル1: 「文体がスタイルプロファイルと合わない」
**原因**: スタイルプロファイルのパラメータが正しく読み込まれていない
**解決プロンプト**:
```text
スタイルプロファイル（output/style_profile.yaml）の内容を再確認し、
以下のパラメータを明示的に指定して再生成してください：
- 語尾: 「です/ます」調
- 平均文長: 40〜60字
- 口調: 親しみやすいが丁寧
--styleオプションでプロファイルを明示的に指定してください。
```

### トラブル2: 「記事が長すぎる・短すぎる」
**原因**: 文字数の指定が曖昧
**解決プロンプト**:
```text
各セクションの目標文字数を明示してドラフトを再生成してください：
- 導入: 300〜400字
- 本文各セクション: 500〜700字
- まとめ: 200〜300字
合計で目標文字数に収まるよう調整してください。
```

### トラブル3: 「挿絵マーカーが消えてしまった」
**原因**: ドラフト生成時にマーカーが除去された
**解決プロンプト**:
```text
アウトライン（output/article-14-1-outline-final.md）から挿絵マーカーを抽出し、
ドラフトの対応する位置に再挿入してください。
形式: <!-- illustration: type=image|diagram, description="説明文" -->
```

### トラブル4: 「前回のファイルが見つからない」
**原因**: 15-1/16-2が未完了、またはファイルパスが異なる
**解決プロンプト**:
```bash
outputディレクトリの中身を確認してください：
ls -la ~/ai-agent-camp/output/
アウトラインやスタイルプロファイルが見つからない場合は、
先にLesson 14-1（/start-14-1）とLesson 14-2（/start-14-2）を完了してください。
```

---

## ✅ チェックポイント
- [ ] アウトラインとスタイルプロファイルの内容を確認した
- [ ] article-writerでスタイル適用ドラフトを生成できた
- [ ] ドラフトの文体がスタイルプロファイルと一致している
- [ ] レビュー・調整済みの最終ドラフトをoutput/に保存した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── article-14-3-*.md  (記事ドキュメント)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/article-14-3-*.md

# 冒頭を確認（最初の30行）
head -30 output/article-14-3-*.md
```

> 💡 全文を確認: `cat output/article-14-3-*.md` で全文表示できます

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```bash
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-14-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-14-4
- finish → 終了
