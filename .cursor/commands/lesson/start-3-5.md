---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4"]
duration: "約30分"
level: "intermediate"
tags: ["screenshot", "batch-processing", "manual"]
---

# 🎓 Lesson 3-5: 複数スクリーンショットの一括分析

## 📍 このセッションでやること

**Lesson 3-5: 複数スクリーンショットの一括分析** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 複数スクショを一括処理し、統合されたユーザーマニュアルを作成する |
| 所要時間 | 約30分 |
| 使うスキル | screenshot-analyzer, tutorial-generator, screenshot-annotator の統合 |
| 前提条件 | Lesson 3-1〜Lesson 3-4 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. マニュアル作成の要件定義
2. 複数スクショの一括分析と構成設計
3. 統合マニュアルの出力

セッション終了時には、実務レベルの操作マニュアルが作成できるようになっています。

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

## 🚀 Step 1: マニュアル作成の要件定義

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: マニュアル作成の要件定義",
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
Webアプリのユーザーマニュアルを作成します。

対象機能:
1. ログイン
2. ダッシュボード
3. データ入力
4. レポート生成
5. ユーザー設定

各機能のスクリーンショットは `courses/aiagent/lesson03-core/module03-screenshot/practice/data/` 配下に正式素材として配置します。
practice に存在しないが研修で必要な素材は、`practice/` または `final/` 配下へ移設してから使ってください。

マニュアル作成の計画を立ててください：
- 各機能に必要なスクリーンショット数
- チュートリアル生成の順序
- 統合方法
```

**期待される結果**: マニュアル作成の詳細な計画が提示されます。

---

## 🚀 Step 2: チュートリアルの一括生成

複数のスクリーンショットからチュートリアルを一括生成します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: チュートリアルの一括生成",
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
以下のスクリーンショットからチュートリアルを一括生成してください。

入力ファイル:
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/data-input.png
- courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/report.png

出力先: output/manual/

各ファイルに対して:
1. tutorial-generatorでチュートリアル生成
2. screenshot-annotatorで重要箇所に注釈追加
3. HTML形式で保存

処理状況を報告しながら実行してください。
```

**期待される結果**: 各スクリーンショットに対してチュートリアルが生成され、進捗が報告されます。

---

## 🚀 Step 3: 注釈の一括追加

全ての画像に一貫した注釈スタイルを適用します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 注釈の一括追加",
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
courses/aiagent/lesson03-core/module03-screenshot/practice/data/ 配下のPNG画像に対して、
重要な操作ボタンを赤枠で強調してください。

出力先: output/annotated/

各画像について:
- メインの操作ボタンを自動検出
- red_box スタイルで強調
- 操作説明を吹き出しで追加

処理した画像の一覧を表示してください。
```

**期待される結果**: 全ての画像に一貫したスタイルで注釈が追加されます。

---

## 🚀 Step 4: HTMLマニュアルへの統合

生成したコンテンツを1つのHTMLドキュメントに統合します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: HTMLマニュアルへの統合",
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
生成したチュートリアルと注釈付き画像を
1つのHTMLマニュアルに統合してください。

統合するファイル:
- output/manual/*.html（チュートリアル）
- output/annotated/*.png（注釈付き画像）

出力: output/complete-manual.html

構成:
1. 目次（各機能へのリンク）
2. 各機能のチュートリアル
3. トラブルシューティングセクション
4. FAQ

日本語で、初心者にもわかりやすい表現で作成してください。
```

**期待される結果**: 目次付きの完全なHTMLマニュアルが生成されます。

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
      {"id": "trouble_1", "label": "バッチ処理でエラーが発生"},
      {"id": "trouble_2", "label": "マニュアルが長すぎる"},
      {"id": "trouble_3", "label": "HTMLが正しく表示されない"},
      {"id": "trouble_4", "label": "画像が表示されない"}
    ]
  }]
}
```


### トラブル1: 「バッチ処理でエラーが発生」
**原因**: 一部のファイルパスが間違っている
**解決プロンプト**:
```
処理対象のファイル一覧を確認してください。
存在しないファイルがあれば報告し、
存在するファイルのみで処理を続行してください。
```

### トラブル2: 「マニュアルが長すぎる」
**原因**: 情報量が多すぎて読みづらい
**解決プロンプト**:
```
マニュアルを以下のように分割してください：
- 基本編（必須操作のみ）
- 応用編（詳細設定）
- 管理者編（管理機能）

各編を別のHTMLファイルとして出力してください。
```

### トラブル3: 「HTMLが正しく表示されない」
**原因**: HTMLタグの構造エラー
**解決プロンプト**:
```
生成されたHTMLファイルの構造を検証してください。
エラーがあれば修正し、正しいHTML5形式で再生成してください。
```

### トラブル4: 「画像が表示されない」
**原因**: 画像パスが相対パスで正しく解決されない
**解決プロンプト**:
```
HTMLマニュアル内の画像パスを確認してください。
全ての画像が正しく参照されているか検証し、
必要に応じてパスを修正してください。
```

---

## ✅ チェックポイント
- [ ] マニュアル作成の要件定義ができる
- [ ] 複数ファイルを一括処理できる
- [ ] 自動生成と手動編集を効率的に組み合わせられる
- [ ] HTMLドキュメントに統合できる
- [ ] 目次と構造化されたマニュアルが作成できる


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/screenshots/
├── analyzed-{対象名}.png
└── (バリエーション)
```
> 形式: PNG | サイズ: 自動設定

### 確認コマンド
```bash
# ファイル一覧
ls -la output/screenshots/

# 画像を開く（macOS: open / Linux: xdg-open）
open output/screenshots/
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-3-6）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-3-6
- finish → 終了
