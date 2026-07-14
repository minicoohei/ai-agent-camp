---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "30分"
prerequisites: ["start-14-1"]
level: "beginner"
tags: ["article", "style"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 14-2: 文体学習 - スタイルプロファイル作成

## 📍 このセッションでやること

**Lesson 14-2: 文体学習 - スタイルプロファイル作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 自分の文章を複数読み込ませ、文体の特徴を分析してスタイルプロファイルを作成する |
| 所要時間 | 約30分 |
| 使うスキル | style-analyzer |
| 前提条件 | Lesson 14-1 完了済み、Gemini APIキー設定済み、分析対象の文章サンプル（3〜5本推奨） |
| 教材ページ | [Module 14: 記事作成](https://ai-agent.camp/ja/course/module-14) を並行参照 |

**このセッションの流れ:**
1. 自分の文章サンプルを準備する（3〜5本推奨）
2. style-analyzerで文体分析を実行する
3. 生成されたスタイルプロファイルを確認・理解する

セッション終了時には、あなたの文体特徴を数値化したスタイルプロファイル（YAML形式）が完成しています。

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

## 🚀 Step 1: 文章サンプルの準備

Codex では通常チャットで選択肢を提示しながらでサンプルの準備状況を選びます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 文章サンプルを準備する",
  "questions": [{
    "id": "sample_status",
    "prompt": "分析に使う文章サンプルはありますか？",
    "options": [
      {"id": "ready", "label": "サンプルを用意済み（ファイルパスを指定する）"},
      {"id": "write_now", "label": "サンプル文章を今書く"},
      {"id": "use_demo", "label": "デモ用サンプルを使う"}
    ]
  }]
}
```

**選択後の案内（例）**:

**「サンプルを用意済み」の場合:**
```text
分析に使う文章ファイルのパスを教えてください。
3〜5本のMarkdownまたはテキストファイルが理想的です。
例: output/samples/sample1.md, output/samples/sample2.md
```

**「サンプル文章を今書く」の場合:**
```text
output/samples/ ディレクトリに文章サンプルを作成しましょう。
以下のテンプレートを使って、3本の短い文章（各300〜500字）を書いてください：

テーマ例:
1. 最近学んだこと
2. おすすめのツール紹介
3. 仕事の工夫・コツ

各ファイルをoutput/samples/sample1.md、sample2.md、sample3.mdに保存します。
```

**「デモ用サンプルを使う」の場合:**
```text
デモ用のサンプル文章3本を生成して、output/samples/に保存します。
異なる文体パターン（カジュアル/フォーマル/技術的）のサンプルが含まれます。
```

**期待される結果**: output/samples/ に分析対象の文章サンプルが3〜5本準備されます。

---

## 🚀 Step 2: style-analyzerで文体分析を実行

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 文体分析を実行する",
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
style-analyzerスキルを使って、以下の文章サンプルの文体分析を実行してください。

入力ファイル:
- output/samples/sample1.md
- output/samples/sample2.md
- output/samples/sample3.md

分析項目:
1. 語尾パターン（です/ます調、だ/である調、混合）
2. 平均文長（1文あたりの文字数）
3. 漢字/ひらがな/カタカナ比率
4. 口調の特徴（丁寧さ、親しみやすさ、専門性）
5. 接続詞の傾向（使用頻度、よく使う接続詞）
6. 段落構成パターン（1段落の文数、改行頻度）

結果をoutput/style_profile.yamlに保存してください。

実行コマンド:
python skills/style-analyzer/scripts/style_analyzer.py --input output/samples/sample1.md --input output/samples/sample2.md --input output/samples/sample3.md --output output/style_profile.yaml
```

**期待される結果**: 文体の特徴が数値化・構造化され、YAML形式のスタイルプロファイルとして保存されます。

---

## 🚀 Step 3: プロファイル結果の確認と解説

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: プロファイル結果を確認する",
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
output/style_profile.yamlの内容を読み込んで、以下を説明してください：

1. 私の文体の特徴サマリー（3〜5行）
2. 各分析項目の意味と数値の解釈
3. この文体が向いている記事タイプ（ブログ/解説/技術記事など）
4. 文体の強み（読者に好印象を与えるポイント）
5. 改善のヒント（より読みやすくするための提案）

15-3でこのプロファイルを使って記事を生成するので、
プロファイルの内容をしっかり理解しておきましょう。
```

**期待される結果**: スタイルプロファイルの各項目の解説と、文体の特徴・強み・改善ポイントが説明されます。

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
      {"id": "trouble_1", "label": "文章サンプルが少なくて分析精度が低い"},
      {"id": "trouble_2", "label": "スタイルプロファイルの値が極端になる"},
      {"id": "trouble_3", "label": "style-analyzerでエラーが出る"},
      {"id": "trouble_4", "label": "ファイルが保存されない"}
    ]
  }]
}
```


### トラブル1: 「文章サンプルが少なくて分析精度が低い」
**原因**: サンプル数が1〜2本では文体の傾向を正確に捉えられない
**解決プロンプト**:
```text
サンプル数を増やすために、以下を試してください：
- 過去のメール、チャット、レポートなどからテキストを抽出する
- 短い文章でも3本以上あれば基本的な傾向は分析可能です
- どうしても用意できない場合は「デモ用サンプル」で練習してから、
  後日自分のサンプルで再分析してください
```

### トラブル2: 「スタイルプロファイルの値が極端になる」
**原因**: サンプル間で文体が大きく異なる（仕事用とプライベート用の混在など）
**解決プロンプト**:
```text
サンプルの文体が統一されているか確認してください。
用途別（ビジネス/カジュアル）に分けて、
それぞれ別のプロファイルを作成することをお勧めします：
- output/style_profile_business.yaml
- output/style_profile_casual.yaml
```

### トラブル3: 「style-analyzerでエラーが出る」
**原因**: ファイルパスの誤り、またはファイル形式が非対応
**解決プロンプト**:
```text
以下を確認してください：
1. ファイルパスが正しいか（絶対パスで指定）
2. ファイル形式が .md または .txt であるか
3. ファイルが空でないか
4. 文字コードがUTF-8であるか
```

### トラブル4: 「ファイルが保存されない」
**原因**: outputディレクトリが存在しない
**解決プロンプト**:
```bash
outputディレクトリが存在するか確認し、なければ作成してください。
mkdir -p ~/ai-agent-camp/output/samples
```

---

## ✅ チェックポイント
- [ ] 文章サンプルを3本以上準備した
- [ ] style-analyzerで文体分析を実行できた
- [ ] スタイルプロファイル（YAML形式）がoutput/に保存された
- [ ] プロファイルの各項目の意味を理解した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── article-14-2-*.md  (記事ドキュメント)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/article-14-2-*.md

# 冒頭を確認（最初の30行）
head -30 output/article-14-2-*.md
```

> 💡 全文を確認: `cat output/article-14-2-*.md` で全文表示できます

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-14-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-14-3
- finish → 終了
