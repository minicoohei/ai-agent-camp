---
description: "When the user says /start-3-1 — Module 3 Lesson 3-1: スクリーンショット分析基礎"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
duration: "約25分"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["screenshot", "analysis", "gemini-vision"]
---

# 🎓 Lesson 3-1: スクリーンショット分析基礎

## 📍 このセッションでやること

**Lesson 3-1: スクリーンショット分析入門** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | screenshot-analyzerスキルで画面のエラーを自動分析し、解決策を提案する |
| 所要時間 | 約25分 |
| 使うスキル | screenshot-analyzer (Gemini Vision API) |
| 前提条件 | Gemini APIキー設定済み、Python環境セットアップ済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. スクリーンショットの準備
2. エラー画面の分析と解決策の取得
3. 分析結果の活用

セッション終了時には、エラー診断結果や解決策の提案が得られるようになっています。

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

## 🚀 Step 1: スクリーンショットの準備

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: スクリーンショットの準備",
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
courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ に
サンプル画像があるか確認してください。
なければ、研修用の画像は同じディレクトリ配下に追加し、
個人の一時素材は lesson 配下の正式素材に移す方法を教えてください。
```

**期待される結果**: inputsフォルダの状態が確認され、必要に応じてテスト画像の準備方法が案内されます。

---

## 🚀 Step 2: 基本的なエラー分析を実行

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 基本的なエラー分析を実行",
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
screenshot-analyzerスキルを使って、スクリーンショットからエラーを分析してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/error-screenshot.png
出力: output/screenshots/analyzed-error.png

分析内容:
- エラーの原因を特定
- 解決方法を提案
- 重要な箇所をマーキング
```

**期待される結果**: エラー箇所が赤枠でマーキングされ、解決策が注釈として追加された画像が生成されます。

---

## 🚀 Step 3: UI問題点の指摘

UIデザインの問題を分析してみましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: UI問題点の指摘",
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
このスクリーンショットのUI問題点を分析してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ui-issue.png
出力: output/screenshots/ui-issue-annotated.png

分析観点:
- ボタンの配置
- 文字サイズ
- 色のコントラスト
- ユーザビリティ

問題箇所に注釈を追加して、改善案を提示してください。
```

**期待される結果**: UIの問題点が視覚的にマーキングされ、改善提案が注釈として追加されます。

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
      {"id": "trouble_1", "label": "スクリーンショットファイルが見つからない"},
      {"id": "trouble_2", "label": "分析結果が不正確"},
      {"id": "trouble_3", "label": "注釈が表示されない"},
      {"id": "trouble_4", "label": "Gemini APIエラー"}
    ]
  }]
}
```


### トラブル1: 「スクリーンショットファイルが見つからない」
**原因**: ファイルパスが間違っている、またはファイルが存在しない
**解決プロンプト**:
```
courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ の中身を確認してください。
画像ファイル（.png, .jpg）があれば一覧表示してください。
```

### トラブル2: 「分析結果が不正確」
**原因**: スクリーンショットの画質が低い、または情報が不足している
**解決プロンプト**:
```
スクリーンショットの分析をより正確にするため、
どのような情報を追加で提供すればよいか教えてください。
```

### トラブル3: 「注釈が表示されない」
**原因**: 出力先のフォルダが存在しない
**解決プロンプト**:
```
output/screenshots/ フォルダを作成してください。
存在しなければ作成し、存在すれば中身を確認してください。
```

### トラブル4: 「Gemini APIエラー」
**原因**: APIキーが設定されていない
**解決プロンプト**:
```
GEMINI_API_KEY 環境変数が設定されているか確認してください。
設定されていなければ、設定方法を教えてください。
```

---

## ✅ チェックポイント
- [ ] スクリーンショットから問題点を特定できる
- [ ] エラーメッセージを正しく解釈できる
- [ ] 問題箇所を視覚的にマーキングできる
- [ ] 具体的な解決策を提案できる
- [ ] 出力フォルダに分析結果が保存される


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-3-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-3-2
- finish → 終了
