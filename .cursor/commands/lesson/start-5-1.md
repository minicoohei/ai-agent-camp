---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module05-pptx"
duration: "約25分"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["pptx", "analysis", "document"]
---

# 🎓 Lesson 5-1: PPTX解析

## 📍 このセッションでやること

**Lesson 5-1: PPTX解析** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | PPTXファイルの構造を解析し、スライド情報・レイアウト・テキストを抽出する |
| 所要時間 | 約25分 |
| 使うスキル | pptx-analyzer, document-processor |
| 前提条件 | Python環境セットアップ済み、サンプルPPTXファイルがあるとよい |
| 教材ページ | [Module 5: PPTX](https://ai-agent.camp/ja/course/module-5) を並行参照 |

**このセッションの流れ:**
1. PPTXファイルの構造確認
2. スライド・テキスト・図形の抽出
3. テンプレート情報の取得

セッション終了時には、PPTXの構造をプログラムから扱えるようになっています。

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

## 🚀 Step 1: 必要なライブラリのインストール確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 必要なライブラリのインストール確認",
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
python-pptxがインストールされているか確認してください。
インストールされていなければ、uv add python-pptx を実行してください。
```

**期待される結果**: python-pptxがインストールされ、バージョンが表示されます。

---

## 🚀 Step 2: サンプルPPTXファイルの準備

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: サンプルPPTXファイルの準備",
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
サンプルのPowerPointファイルがあるか確認してください。
なければ、簡単なテスト用PPTXファイル（3スライド程度）を作成してください。
```

> **注意**: `data/` ディレクトリにサンプルPPTXが存在しない場合があります。手元にある任意の `.pptx` ファイルを使用するか、AIにテスト用PPTXファイルを `output/` に生成してもらってください。

**期待される結果**: サンプルPPTXファイルが準備されます。

---

## 🚀 Step 3: PPTXの基本情報を抽出

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: PPTXの基本情報を抽出",
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
~/ai-agent-camp/data/ にあるPPTXファイルを読み込んで、以下の情報を教えてください：
- スライドの総数
- 各スライドのレイアウト名
- 各スライドに含まれるシェイプの数
- 使用されているフォント一覧
```

**期待される結果**: PPTXファイルの構造情報がJSON形式で表示されます。

---

## 🚀 Step 4: スライドごとの詳細解析

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: スライドごとの詳細解析",
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
先ほどのPPTXファイルの各スライドについて、詳細な解析を行ってください：
- テキストの内容（箇条書き含む）
- 画像があればそのサイズと位置
- 表があれば行数・列数
結果をJSONファイルとして ~/ai-agent-camp/output/pptx-analysis.json に保存してください。
```

**期待される結果**: 詳細な解析結果がJSONファイルとして保存されます。

---

## 🚀 Step 5: テンプレート情報の抽出

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: テンプレート情報の抽出",
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
PPTXファイルのスライドマスターとレイアウト情報を抽出してください：
- 利用可能なレイアウトの一覧
- 各レイアウトのプレースホルダー情報
- テーマカラーの設定
これらを再利用可能なテンプレート情報として整理してください。
```

**期待される結果**: テンプレート情報が抽出され、レイアウトの選択肢が明確になります。

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
      {"id": "trouble_1", "label": "PPTXファイルが開けない"},
      {"id": "trouble_2", "label": "文字化けが発生する"},
      {"id": "trouble_3", "label": "画像情報が取得できない"}
    ]
  }]
}
```


### トラブル1: 「PPTXファイルが開けない」
**原因**: ファイルパスが間違っている、またはファイルが破損している
**解決プロンプト**:
```
PPTXファイルが正しく読み込めるか確認してください。
エラーが出る場合は、原因と解決方法を教えてください。
```

### トラブル2: 「文字化けが発生する」
**原因**: エンコーディングの問題
**解決プロンプト**:
```
PPTXの日本語テキストが文字化けしています。
UTF-8エンコーディングで正しく保存する方法を教えてください。
```

### トラブル3: 「画像情報が取得できない」
**原因**: 画像がシェイプ内に正しく埋め込まれていない
**解決プロンプト**:
```
PPTXから画像情報を取得できません。
hasattr(shape, 'image')のチェック方法を確認してください。
```

---

## ✅ チェックポイント
- [ ] python-pptxがインストールできた
- [ ] PPTXファイルを読み込めた
- [ ] スライドの基本情報を取得できた
- [ ] テキストと図形情報を抽出できた
- [ ] レイアウトとプレースホルダー情報を取得できた
- [ ] 解析結果をJSONで保存できた


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-5-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-5-2
- finish → 終了
