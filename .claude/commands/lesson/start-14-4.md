---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "40分"
prerequisites: ["start-14-3"]
level: "intermediate"
tags: ["article", "illustration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 14-4: 挿絵計画と生成 - nanobanana + PlantUML

## 📍 このセッションでやること

**Lesson 14-4: 挿絵計画と生成 - nanobanana + PlantUML** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 記事内の挿絵マーカーを検出し、nanobananaとPlantUMLで挿絵を自動生成して埋め込む |
| 所要時間 | 約40分 |
| 使うスキル | nanobanana, diagram-generator |
| 前提条件 | Gemini APIキー設定済み、Lesson 14-3（ドラフト）完了済み |
| 教材ページ | [Module 14: 記事作成](https://ai-agent.camp/ja/course/module-14) を並行参照 |

**このセッションの流れ:**
1. ドラフト内の挿絵マーカー（`<!-- illustration: ... -->`）を確認する
2. type=diagram のマーカー → PlantUMLで図表を生成する
3. type=image のマーカー → nanobananaで画像を生成する
4. 生成した画像をMarkdownに埋め込む

セッション終了時には、挿絵付きの記事ドラフトが完成しています。

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

## 🚀 Step 1: ドラフト内の挿絵マーカーを確認

Codex では通常チャットで選択肢を提示しながらでマーカーの検出方法を選びます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 挿絵マーカーを確認する",
  "questions": [{
    "id": "marker_method",
    "prompt": "挿絵マーカーをどう検出しますか？",
    "options": [
      {"id": "auto_detect", "label": "マーカーを自動検出する"},
      {"id": "manual_specify", "label": "手動で挿絵箇所を指定する"}
    ]
  }]
}
```

**「マーカーを自動検出する」の場合:**
入力内容:
```text
output/article-16-3-draft-final.mdを読み込んで、
挿絵マーカー（<!-- illustration: ... -->）を全て抽出してください。

各マーカーについて以下を一覧表示してください：
1. 行番号
2. タイプ（image / diagram）
3. 説明文（description）
4. 前後のコンテキスト（どのセクションに属するか）

マーカーが不足している場合は、追加すべき箇所を提案してください。
```

**「手動で挿絵箇所を指定する」の場合:**
```text
output/article-16-3-draft-final.mdの内容を表示してください。
挿絵を入れたい箇所を指定するので、マーカーを追加します。
```

**期待される結果**: ドラフト内の全挿絵マーカーがリスト化され、生成計画が立てられます。

---

## 🚀 Step 2: PlantUMLで図表を生成（type=diagram）

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: PlantUMLで図表を生成する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする（diagram マーカーがない場合）"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
diagram-generatorスキルを使って、以下の挿絵マーカーに対応する図表を生成してください。

対象マーカー:
<!-- illustration: type=diagram, description="業務効率化のフロー図" -->

生成条件:
- 形式: PlantUML → PNG画像
- スタイル: シンプルで見やすい配色
- 出力先: output/images/article-16-4-diagram-1.png

実行コマンド:
uv run python tools/generate_diagram.py --type flowchart --topic "業務効率化フロー" --output output/images/article-16-4-diagram-1.png

全てのdiagramマーカーに対して画像を生成してください。
```

**期待される結果**: output/images/ にPlantUMLベースの図表画像が生成されます。

---

## 🚀 Step 3: nanobananaで画像を生成（type=image）

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: nanobananaで画像を生成する",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする（image マーカーがない場合）"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
nanobananaスキルを使って、以下の挿絵マーカーに対応する画像を生成してください。

対象マーカー:
<!-- illustration: type=image, description="AIツールを使って作業するビジネスパーソン" -->

生成条件:
- スタイル: モダンでクリーンなイラスト風
- サイズ: 記事挿絵に適したアスペクト比（16:9 or 4:3）
- 出力先: output/images/article-16-4-image-1.png

実行コマンド:
uv run python tools/nanobanana.py --prompt "AIツールを使って作業するビジネスパーソン、モダンなイラスト風" --output output/images/article-16-4-image-1.png

全てのimageマーカーに対して画像を生成してください。
```

**期待される結果**: output/images/ にnanobananaで生成された挿絵画像が保存されます。

---

## 🚀 Step 4: 生成した画像をMarkdownに埋め込み

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 画像をMarkdownに埋め込む",
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
output/article-16-3-draft-final.mdの挿絵マーカーを、
生成した画像のMarkdown記法に置換してください。

置換ルール:
- <!-- illustration: type=diagram, description="..." -->
  → ![説明文](images/article-16-4-diagram-N.png)
- <!-- illustration: type=image, description="..." -->
  → ![説明文](images/article-16-4-image-N.png)

各画像にはalt属性（説明文）とキャプション（*図N: 説明*）を追加してください。

結果をoutput/article-16-4-with-images.mdに保存してください。
```

**期待される結果**: 挿絵マーカーが実際の画像参照に置換され、完全な記事ドラフトが保存されます。

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
      {"id": "trouble_1", "label": "PlantUMLの図表が正しく生成されない"},
      {"id": "trouble_2", "label": "nanobananaの画像がイメージと違う"},
      {"id": "trouble_3", "label": "挿絵マーカーが見つからない"},
      {"id": "trouble_4", "label": "画像の埋め込みパスが壊れる"}
    ]
  }]
}
```


### トラブル1: 「PlantUMLの図表が正しく生成されない」
**原因**: PlantUMLの記法エラー、またはJava環境の問題
**解決プロンプト**:
```text
PlantUMLの記法を確認してください。
まずシンプルな図表で動作確認を行い、徐々に要素を追加してください。
Java環境が必要な場合: java -version で確認してください。
代替案: Gemini Image Generation APIで図表を直接生成することも可能です。
```

### トラブル2: 「nanobananaの画像がイメージと違う」
**原因**: プロンプトが具体的でない
**解決プロンプト**:
```text
画像生成プロンプトをより具体的にしてください：
- スタイル指定: 「フラットデザインのイラスト」「写真風」「水彩画風」
- 色味指定: 「ブルー系の落ち着いた配色」
- 構図指定: 「中央にメインオブジェクト、背景はシンプル」
再生成して比較してみましょう。
```

### トラブル3: 「挿絵マーカーが見つからない」
**原因**: 15-1/16-3でマーカーが挿入されなかった
**解決プロンプト**:
```text
ドラフトに挿絵マーカーを追加してください。
各H2セクションの冒頭または末尾に以下の形式で挿入します：
<!-- illustration: type=image|diagram, description="セクション内容を表す説明" -->
```

### トラブル4: 「画像の埋め込みパスが壊れる」
**原因**: 相対パスと絶対パスの不一致
**解決プロンプト**:
```bash
Markdown内の画像パスは記事ファイルからの相対パスで記述してください。
記事がoutput/にある場合: ![alt](images/filename.png)
画像がoutput/images/にあることを確認: ls output/images/
```

---

## ✅ チェックポイント
- [ ] ドラフト内の挿絵マーカーを全て検出・確認した
- [ ] type=diagramのマーカーに対してPlantUML図表を生成できた
- [ ] type=imageのマーカーに対してnanobanana画像を生成できた
- [ ] 全ての挿絵をMarkdownに埋め込んだ記事をoutput/に保存した


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/
└── article-14-4-*.md  (記事ドキュメント)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/article-14-4-*.md

# 冒頭を確認（最初の30行）
head -30 output/article-14-4-*.md
```

> 💡 全文を確認: `cat output/article-14-4-*.md` で全文表示できます

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-14-5）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-14-5
- finish → 終了
