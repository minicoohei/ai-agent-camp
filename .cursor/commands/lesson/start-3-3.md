---
description: "When the user says /start-3-3 — Module 3 Lesson 3-3: チュートリアル自動生成"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "約25分"
level: "intermediate"
tags: ["screenshot", "tutorial", "documentation"]
---

# 🎓 Lesson 3-3: チュートリアル自動生成

## 📍 このセッションでやること

**Lesson 3-3: チュートリアル自動生成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | tutorial-generatorスキルでスクショから操作チュートリアルを自動生成する |
| 所要時間 | 約25分 |
| 使うスキル | tutorial-generator (Gemini Vision API) |
| 前提条件 | Lesson 3-1 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. ログイン画面のチュートリアル生成
2. 複数ステップのチュートリアル作成
3. マニュアル形式での出力

セッション終了時には、操作手順書やオンボーディングドキュメントが生成できるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 📁 サンプル画像の準備

このレッスンではスクリーンショット画像を入力として使用します。`courses/aiagent/lesson03-core/module03-screenshot/practice/data/` 配下に以下の素材を用意してください:

- **login-screen.png** — 任意のWebサイトのログイン画面のスクリーンショット
- **signup-form.png** — 任意の登録フォームのスクリーンショット
- **purchase-step1~4.png** — ECサイトの購入フロー各ステップのスクリーンショット（4枚）

> **ヒント**: 手元にスクリーンショットがない場合は、以下のいずれかの方法で用意してください:
> - 任意のWebサイトのスクリーンショットを撮影して `practice/data/tutorial-samples/` に保存（macOS: `Cmd+Shift+4`、Windows: `Win+Shift+S`）
> - nanobananaスキルでサンプル画像を自動生成:
>   ```bash
>   uv run python tools/nanobanana.py --prompt "ログインフォームのスクリーンショット、メールとパスワード入力欄、ログインボタン" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
>   uv run python tools/nanobanana.py --prompt "会員登録フォーム、名前・メール・パスワード入力欄" --output courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
>   ```
> - 既存の `practice/data/screenshots/` にある画像（`dashboard.png`, `ui-issue.png` 等）で代替実行も可能です
> - `practice/` に存在しないが研修で必要な素材は、削除せずに該当 lesson の `practice/` または `final/` 配下へ正式素材として移してください

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

## 🚀 Step 1: ログイン画面のチュートリアル生成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ログイン画面のチュートリアル生成",
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
tutorial-generatorスキルを使って、ログイン画面のチュートリアルを生成してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/login-screen.png
出力: output/tutorials/login-tutorial.html

対象ユーザー: 初心者
目的: ログイン方法の説明
出力形式: HTML（日本語）
```

> **注意**: スクリプト実行時は `PYTHONPATH=. python skills/tutorial-generator/scripts/generate_tutorial.py ...` のようにPYTHONPATHを設定してください。

**期待される結果**: ステップバイステップのログインチュートリアルがHTML形式で生成されます。

---

## 🚀 Step 2: コンテキスト情報を追加したチュートリアル

より詳しい説明のために、コンテキスト情報を追加します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: コンテキスト情報を追加したチュートリアル",
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
ユーザー登録画面のチュートリアルを生成してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/signup-form.png
出力: output/tutorials/signup-tutorial.html

コンテキスト情報:
- 新規ユーザー登録画面です
- メール、パスワード、名前を入力して登録します
- パスワードは8文字以上必要です
- メール認証が必要です

これらの情報を反映した詳細なチュートリアルを作成してください。
```

**期待される結果**: コンテキスト情報が反映された、詳しい説明付きのチュートリアルが生成されます。

---

## 🚀 Step 3: 複数ステップの操作フローを生成

ECサイトの購入フローなど、複数画面にまたがるチュートリアルを生成します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 複数ステップの操作フローを生成",
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
購入フローのチュートリアルを作成してください。

以下の画面順で処理:
1. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step1.png - 商品選択
2. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step2.png - カート確認
3. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step3.png - 配送先入力
4. courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/purchase-step4.png - 決済完了

出力: output/tutorials/purchase-tutorial.html

各ステップの操作を詳細に説明し、
全体を1つのHTMLドキュメントにまとめてください。
```

**期待される結果**: 4つのステップが連続したチュートリアルドキュメントが生成されます。

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
      {"id": "trouble_1", "label": "チュートリアルが生成されない"},
      {"id": "trouble_2", "label": "AIの説明が不正確"},
      {"id": "trouble_3", "label": "日本語が文字化けする"},
      {"id": "trouble_4", "label": "複数ファイルの処理が途中で止まる"}
    ]
  }]
}
```


### トラブル1: 「チュートリアルが生成されない」
**原因**: スクリーンショットのファイル形式が対応していない
**解決プロンプト**:
```
サポートされている画像ファイル形式を教えてください。
また、現在のスクリーンショットの形式を確認してください。
```

### トラブル2: 「AIの説明が不正確」
**原因**: コンテキスト情報が不足している
**解決プロンプト**:
```
チュートリアルの精度を上げるために、
どのようなコンテキスト情報を追加すればよいですか？
具体例とともに教えてください。
```

### トラブル3: 「日本語が文字化けする」
**原因**: エンコーディングの問題
**解決プロンプト**:
```
生成されたHTMLファイルの文字エンコーディングを確認してください。
UTF-8で正しく保存されているか確認し、問題があれば修正してください。
```

### トラブル4: 「複数ファイルの処理が途中で止まる」
**原因**: ファイルが見つからない、またはタイムアウト
**解決プロンプト**:
```
指定した全てのファイルが存在するか確認してください。
存在するファイルのみでチュートリアルを生成してください。
```

---

## ✅ チェックポイント
- [ ] スクリーンショットから自動的にチュートリアルを生成できる
- [ ] コンテキスト情報を活用して詳しい説明を生成できる
- [ ] 複数ステップの操作フロー全体をカバーできる
- [ ] HTML形式のチュートリアルが正しく表示される
- [ ] 日本語で適切なチュートリアルが生成される


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-3-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-3-4
- finish → 終了
