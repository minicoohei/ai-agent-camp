---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "約25分"
level: "intermediate"
tags: ["screenshot", "annotation", "manual"]
---

# 🎓 Lesson 3-4: スクリーンショットに注釈追加

## 📍 このセッションでやること

**Lesson 3-4: スクリーンショットに注釈追加** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | screenshot-annotatorスキルで矢印・枠・番号・テキストを追加し、マニュアル用画像を作成する |
| 所要時間 | 約25分 |
| 使うスキル | screenshot-annotator (Gemini Vision API) |
| 前提条件 | Lesson 3-1 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. ボタンを赤枠で強調する
2. 矢印・コールアウトを追加する
3. 手順番号付きの注釈画像を作成する

セッション終了時には、マニュアル用の注釈付き画像が outputs に保存されています。

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

## 🚀 Step 1: ボタンを赤枠で強調する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ボタンを赤枠で強調する",
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
screenshot-annotatorスキルを使って、ダッシュボードのヘルプボタンを強調してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/dashboard.png
出力: output/screenshots/help-button-annotated.png

注釈:
- 右上のヘルプボタンを赤枠で囲む
- 矢印で「ここをクリック」と指し示す
- スタイル: red_box
```

**期待される結果**: ヘルプボタンが赤枠で囲まれ、矢印と説明テキストが追加された画像が生成されます。

---

## 🚀 Step 2: 吹き出しで説明を追加

検索フォームに説明を追加します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 吹き出しで説明を追加",
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
検索フォームに吹き出しで説明を追加してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/search-form.png
出力: output/screenshots/search-annotated.png

注釈:
- 検索フォームを特定
- スタイル: callout（吹き出し）
- テキスト: 「キーワードを入力してEnterキーを押す」
```

**期待される結果**: 検索フォームに吹き出しが追加され、使い方が説明されます。

---

## 🚀 Step 3: ステップ番号を追加

操作手順に番号を振ります：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ステップ番号を追加",
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
メニュー操作の手順に番号を追加してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/menu-operation.png
出力: output/screenshots/menu-steps-annotated.png

注釈（順番に追加）:
1. 左上のメニューアイコン → 「1」を追加（circle スタイル）
2. 設定メニュー項目 → 「2」を追加
3. プロフィール設定 → 「3」を追加

各番号は赤い円で囲み、操作順序を明確にしてください。
```

**期待される結果**: 操作手順に1、2、3の番号が赤い円で追加された画像が生成されます。

---

## 🚀 Step 4: 注釈スタイル一覧の確認

利用可能な注釈スタイルを確認しましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 注釈スタイル一覧の確認",
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
screenshot-annotatorで利用可能な全ての注釈スタイルを教えてください。

各スタイルについて以下を説明してください：
- スタイル名
- 見た目の説明
- 適した用途
- 使用例
```

**期待される結果**: red_box、arrow、callout、highlight、circle、number などのスタイル一覧が表示されます。

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
      {"id": "trouble_1", "label": "注釈が表示されない"},
      {"id": "trouble_2", "label": "注釈の位置がおかしい"},
      {"id": "trouble_3", "label": "矢印の向きが逆"},
      {"id": "trouble_4", "label": "テキストが読みにくい"}
    ]
  }]
}
```


### トラブル1: 「注釈が表示されない」
**原因**: 指定した要素がスクリーンショットに含まれていない
**解決プロンプト**:
```
スクリーンショットに含まれているUI要素を分析してください。
どの要素に注釈を追加できるか、一覧で教えてください。
```

### トラブル2: 「注釈の位置がおかしい」
**原因**: 要素の説明が不正確
**解決プロンプト**:
```
注釈を追加したい要素の位置をより詳しく指定します。
「画面の左上から約100px、上から約50pxの位置にあるボタン」
のように座標で指定することはできますか？
```

### トラブル3: 「矢印の向きが逆」
**原因**: 矢印の始点と終点の指定が曖昧
**解決プロンプト**:
```
矢印の向きを調整してください。
始点と終点を明示的に指定する方法を教えてください。
```

### トラブル4: 「テキストが読みにくい」
**原因**: 背景色との コントラストが低い
**解決プロンプト**:
```
注釈テキストの視認性を改善してください。
背景色、フォントサイズ、テキスト色を調整する方法を教えてください。
```

---

## ✅ チェックポイント
- [ ] red_box スタイルでボタンを強調できる
- [ ] callout スタイルで吹き出し説明を追加できる
- [ ] number/circle スタイルでステップ番号を追加できる
- [ ] 複数の要素に同時に注釈を追加できる
- [ ] ユーザーの視線を正しく導く注釈を配置できる


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-3-5）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-3-5
- finish → 終了
