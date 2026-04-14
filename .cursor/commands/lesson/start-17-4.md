---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "約35分"
prerequisites: ["start-17-3"]
level: "intermediate"
tags: ["marketing", "pencil", "design", "mockup"]
---

# 🎓 Lesson 17-4: Pencil MCPでデザインモックアップ

## 📍 このセッションでやること

**Lesson 17-4: Pencil MCPでデザインモックアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Pencil MCPでマーケティングバナーのデザインモックアップを作成する |
| 所要時間 | 約35分 |
| 使うスキル | Pencil MCP (get_editor_state, batch_design, get_screenshot) |
| 前提条件 | Pencil MCP が有効化済み |
| 教材ページ | [Module 17: マーケティング](https://ai-agent.camp/ja/course/module-17) を並行参照 |

> **💡 ツール情報**: このレッスンでは Pencil MCP を使用します。Cursor IDE、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

**このセッションの流れ:**
1. Pencil MCPの基本操作を理解する（get_editor_state, batch_design）
2. 広告バナーのモックアップを作成する
3. get_screenshotでキャプチャしてoutput/pencil/に保存する

セッション終了時には、バナーデザインモックアップ1点と画像キャプチャが完成しています。

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

## 🚀 Step 1: Pencil MCPの基本操作を理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Pencil MCPの基本操作を理解する",
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
Pencil MCPの基本操作を教えてください。以下のツールの使い方を説明してください：

1. get_editor_state() - 現在のエディター状態を取得
2. open_document() - 新しいドキュメントを作成/既存を開く
3. batch_design() - デザイン要素を挿入・更新・削除
   - I() (Insert): 新しい要素を挿入
   - U() (Update): 既存要素を更新
   - D() (Delete): 要素を削除
4. get_screenshot() - デザインのスクリーンショットを取得
5. batch_get() - ノード情報を取得

それぞれの基本的な使い方と引数を説明してください。
```

**期待される結果**: Pencil MCPの主要ツール5つの使い方と引数の説明が得られます。

---

## 🚀 Step 2: 広告バナーのモックアップを作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 広告バナーのモックアップを作成する",
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
Pencil MCPを使って、以下の仕様で広告バナーのモックアップを作成してください。

手順:
1. mkdir -p output/pencil
2. open_document("output/pencil/marketing-banner.pen") で .pen ファイルを作成
3. 以下の仕様でバナーをデザイン

バナー仕様:
- サイズ: 1200x628px（Facebook/Instagram広告サイズ）
- テーマ: 「Cursor Bootcamp」プロモーション
- コピー:
  - メインコピー: 「AIの力で、あなたの仕事が変わる」
  - サブコピー: 「非エンジニアのためのAIエージェント活用研修」
  - CTA: 「今すぐ申し込む」
- デザイン:
  - 背景: グラデーション（ダークブルー → パープル）
  - テキスト: 白色、メインコピーは太字・大きめ
  - CTAボタン: オレンジ色の角丸ボタン
  - ロゴ配置: 右下にCursor Bootcampロゴテキスト
```

**期待される結果**: Pencil MCPのエディター上に広告バナーのモックアップが作成されます。

---

## 🚀 Step 3: get_screenshotでキャプチャして保存する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: スクリーンショットをキャプチャして保存する",
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
作成したバナーモックアップのスクリーンショットを取得し、
以下のパスに保存してください：

出力先: output/pencil/marketing-banner-mockup.png
デザインファイル: output/pencil/marketing-banner.pen（Step 2 で作成済み）

手順:
1. get_screenshot()でモックアップのスクリーンショットを取得
2. 画像を output/pencil/marketing-banner-mockup.png に保存
3. 保存されたファイルのパスとサイズを確認

また、デザインのフィードバックポイントも3つ挙げてください。
（配色、レイアウト、タイポグラフィなどの観点で）
```

**期待される結果**: output/pencil/ にバナーモックアップの画像が保存され、改善ポイントが提示されます。

---

## 🔄 代替ワークフロー（非GUI環境向け）

Pencil MCP が利用できない環境（Claude Code、Codex CLI、SSH等）では、HTML + Tailwind CSS で直接モックアップを作成します。

1. `output/pencil/` ディレクトリを作成
2. HTML + Tailwind CSS CDN でバナーモックアップを作成:
   ```bash
   mkdir -p output/pencil
   ```
3. `output/pencil/marketing-banner-mockup.html` にバナーデザインを実装
   - `<script src="https://cdn.tailwindcss.com"></script>` を使用
   - Step 2 のバナー仕様（サイズ、コピー、配色）をそのまま適用
4. ブラウザで開いてスクリーンショットを取得、または Playwright でキャプチャ:
   ```bash
   npx playwright screenshot output/pencil/marketing-banner-mockup.html output/pencil/marketing-banner-mockup.png
   ```

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
      {"id": "trouble_1", "label": "Pencil MCPに接続できない"},
      {"id": "trouble_2", "label": "batch_designでエラーが出る"},
      {"id": "trouble_3", "label": "スクリーンショットが取得できない"},
      {"id": "trouble_4", "label": "デザインが意図と異なる"}
    ]
  }]
}
```


### トラブル1: 「Pencil MCPに接続できない」
**原因**: Pencil MCP サーバーが無効化されている
**解決プロンプト**:
```
Pencil MCPが有効化されているか確認してください。
Cursorの設定でMCPサーバーの状態を確認し、
user-pencilサーバーが有効になっていることを確認してください。
```

### トラブル2: 「batch_designでエラーが出る」
**原因**: オペレーション構文の誤り、または親ノードIDの指定ミス
**解決プロンプト**:
```
batch_designの操作構文を確認してください。
まずget_editor_state()で現在の状態を取得し、
有効なノードIDを確認してから操作を実行してください。
操作は1行に1つの形式で記述してください：
例: foo=I("parent", { ... })
```

### トラブル3: 「スクリーンショットが取得できない」
**原因**: エディターにドキュメントが開かれていない
**解決プロンプト**:
```
get_editor_state()で現在のエディター状態を確認してください。
ドキュメントが開かれていない場合は、
open_document("new")で新しいドキュメントを作成してください。
```

### トラブル4: 「デザインが意図と異なる」
**原因**: デザイン指示が具体的でない、またはノードの配置がずれている
**解決プロンプト**:
```
snapshot_layoutで現在のレイアウトを確認し、
各ノードの位置とサイズを把握してください。
その後、U()（Update）操作で位置やスタイルを調整してください。
get_screenshotで結果を確認しながら繰り返し調整すると効果的です。
```

---

## ✅ チェックポイント
- [ ] Pencil MCPの基本操作（get_editor_state, batch_design, get_screenshot）を理解した
- [ ] 広告バナーのモックアップをPencil MCPで作成できた
- [ ] get_screenshotでスクリーンショットを取得できた
- [ ] output/pencil/にバナーモックアップ画像が保存された


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/pencil/
├── marketing-banner.pen             ← Pencil デザインファイル（本体）
├── marketing-banner-mockup.png      ← スクリーンショット (1200x628px)
└── marketing-banner-mockup.html     (代替: HTML版)
```
> 形式: PNG | サイズ: 1200x628px（Facebook/Instagram広告サイズ）

### 確認コマンド
```bash
# .pen ファイルとスクリーンショットの確認
ls -lh output/pencil/marketing-banner.pen
ls -lh output/pencil/marketing-banner-mockup.png

# 画像を開く（macOS: open / Linux: xdg-open）
open output/pencil/marketing-banner-mockup.png
```

> 💡 **Claude Code**: `Read output/pencil/marketing-banner-mockup.png` でチャット内プレビュー
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー
> 💡 **.pen ファイル**: Pencil MCP の `batch_get` や `get_screenshot` で中身を確認できます

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでModule 17: マーケティングの全レッスンが完了です！

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "次のモジュールを開始（/start-18-1）"},
      {"id": "review_module", "label": "Module 17を復習する"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_module → /start-18-1 で 要件定義/システム開発モジュールへ
- review_module → Module 17の各レッスンを振り返る
- finish → 終了
