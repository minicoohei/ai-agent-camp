---
description: "When the user says /start-13-4 — Module 13 Lesson 13-4: LP制作 - 実際に動くLP作成"
prerequisites: ["start-13-3"]
duration: "約30分"
level: "intermediate"
tags: ["lp", "html", "tailwind", "implementation"]
---

# 🎓 Lesson 13-4: 実際に動くLP作成（HTML/CSS/JS）

## 📍 このセッションでやること

**Lesson 13-4: LP実装** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Pencilデザインを実際に動くHTML/CSS(Tailwind)/JSに変換する |
| 所要時間 | 約30分 |
| 使うスキル | lp-designer, Pencil MCP（code/tailwindガイドライン）, cursor-ide-browser |
| 前提条件 | Lesson 13-3 完了（.pen デザインファイルが存在） |
| 教材ページ | [Module 13: LP/HP制作](https://ai-agent.camp/ja/course/module-13) を並行参照 |

> **💡 ツール情報**: このレッスンでは Pencil MCP を使用します。Cursor IDE、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

**このセッションの流れ:**
1. コード化ガイドラインの取得
2. プロジェクト構造の作成
3. HTML/CSS(Tailwind)/JS の実装
4. レスポンシブ・アニメーション対応
5. ブラウザでの動作確認

セッション終了時には、実際にブラウザで動くLP/HPが完成しています。

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
(check_prereq → .pen ファイルの存在確認)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: コード化ガイドラインの取得

Pencilデザインをコードに変換するためのガイドラインを取得します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: コード化ガイドライン",
  "questions": [{
    "id": "tech_stack",
    "prompt": "実装に使う技術スタックを選んでください",
    "options": [
      {"id": "tailwind", "label": "HTML + Tailwind CSS（推奨・CDN利用）"},
      {"id": "vanilla", "label": "HTML + バニラCSS"},
      {"id": "react", "label": "React + Tailwind CSS"},
      {"id": "nextjs", "label": "Next.js + Tailwind CSS"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
Pencil MCPからコード化に必要なガイドラインを取得してください。

手順:
1. get_guidelines(topic="code") でコーディングガイドラインを取得
2. get_guidelines(topic="tailwind") でTailwind固有のルールを取得
3. .pen ファイルのデザインを batch_get で読み込み
4. デザイン→コード変換の方針をまとめる

特に以下を確認:
- カラーコード（Tailwindのクラス名に変換）
- フォントサイズ（text-sm, text-lg 等へのマッピング）
- 間隔・余白（p-4, m-8 等へのマッピング）
- レイアウト構造（flex, grid の使い方）
```

**期待される結果**: コード変換に必要な情報が整理されます。

---

## 🚀 Step 2: プロジェクト構造の作成

LPのファイル構造を作成します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: プロジェクト構造",
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
LP用のプロジェクト構造を作成してください。

ディレクトリ作成:
mkdir -p output/lp-project/images
mkdir -p output/lp-project/css
mkdir -p output/lp-project/js

ファイル作成:
- output/lp-project/index.html   # メインHTML
- output/lp-project/css/style.css # カスタムCSS
- output/lp-project/js/main.js   # インタラクション
- output/lp-project/package.json  # Vercelデプロイ用

package.json の内容:
{
  "name": "lp-project",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "npx serve ."
  }
}
```

**期待される結果**: LP用のプロジェクト構造が作成されます。

---

## 🚀 Step 3: HTML/CSS(Tailwind)/JS 実装

Pencilデザインをもとにコードを実装します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: コード実装",
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
Pencil の .pen ファイルと output/lp-brief.md をもとに、
output/lp-project/index.html を実装してください。

要件:
1. Tailwind CSS CDN を使用
   <script src="https://cdn.tailwindcss.com"></script>

2. セクション構成（output/lp-brief.md に基づく）:
   - Header: ロゴ + ナビ + CTAボタン（固定ヘッダー）
   - Hero: ヘッドライン + サブヘッドライン + CTA + Hero画像
   - Pain Points: 3カラムのアイコンカード
   - Solution: 2カラム（テキスト + 画像）
   - Features: 3-4カラムの機能カード
   - Social Proof: お客様の声（カルーセルまたはグリッド）
   - FAQ: アコーディオン形式
   - Final CTA: 背景色付きCTAセクション
   - Footer: リンク群 + コピーライト

3. デザインの忠実な再現:
   - Pencilのスタイルガイドの色・フォントを使用
   - 余白・間隔をデザインに合わせる
   - ボタンスタイル（角丸、ホバーエフェクト）

4. レスポンシブ対応:
   - モバイルファースト（sm: → md: → lg:）
   - スマホでは1カラム、PCでは2-4カラム

5. OGP・メタタグ:
   - title, description, og:image を設定

美しくモダンなデザインで実装してください。
```

**期待される結果**: 完全なHTML/CSS/JSが実装されます。

---

## 🚀 Step 4: アニメーション・インタラクション追加

スクロールアニメーションとインタラクションを追加します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: アニメーション追加",
  "questions": [{
    "id": "animation_level",
    "prompt": "アニメーションのレベルを選んでください",
    "options": [
      {"id": "minimal", "label": "最小限（ホバーエフェクトのみ）"},
      {"id": "standard", "label": "標準（スクロールフェードイン + ホバー）"},
      {"id": "rich", "label": "リッチ（パララックス + カウンター + スライドイン）"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
output/lp-project/js/main.js にアニメーションを追加してください。

追加する機能:
1. スクロールフェードイン（Intersection Observer）
   - 各セクションがビューポートに入ったらフェードイン
   - アニメーション: opacity 0→1, translateY 20px→0

2. スムーズスクロール
   - ナビリンクのクリックでスムーズスクロール

3. FAQアコーディオン
   - 質問クリックで回答を展開/折りたたみ

4. ヘッダー固定
   - スクロール時にヘッダーに影を追加

5. カスタムCSS（output/lp-project/css/style.css）
   - アニメーション用のCSS変数とキーフレーム
   - ダークモード対応（オプション）

外部ライブラリは使わず、バニラJSで実装してください。
```

**期待される結果**: アニメーション・インタラクションが追加されます。

---

## 🚀 Step 5: ブラウザでの動作確認

作成したLPをブラウザで確認します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: ブラウザ動作確認",
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
作成したLPをブラウザで確認してください。

手順:
1. ローカルサーバーを起動
   cd output/lp-project && npx serve .

2. ブラウザで http://localhost:3000 を開く
   （cursor-ide-browser MCPを使用）

3. 以下を確認:
   - デスクトップ表示（1280px幅）
   - モバイル表示（375px幅）
   - アニメーションの動作
   - CTAボタンのクリック
   - FAQアコーディオンの動作
   - スムーズスクロール

4. 問題があれば修正

確認結果をスクリーンショットで残してください。
```

**期待される結果**: LPがブラウザで正しく動作することが確認されます。

---

## 🔄 代替ワークフロー（非GUI環境向け）

Pencil MCP が利用できない環境（Claude Code、Codex CLI、SSH等）では、.pen ファイルなしで直接 HTML を作成します。

1. 13-3 の代替ワークフローで HTML モックアップを作成済みの場合、そのまま本レッスンの Step 2 以降に進む
2. `output/lp-brief.md` と `output/lp-wireframe.txt` を参照し、デザイン仕様を確認
3. Step 1 の「コード化ガイドライン取得」は Pencil MCP 部分をスキップし、Tailwind CSS のドキュメントを参考にする
4. Step 3 以降（HTML/CSS/JS 実装、アニメーション、ブラウザ確認）はそのまま実施可能

> .pen ファイルが存在しない場合でも、ワイヤーフレームとブリーフから直接 HTML + Tailwind CSS で実装できます。

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
      {"id": "trouble_1", "label": "Tailwind CSSが効かない"},
      {"id": "trouble_2", "label": "レスポンシブが崩れる"},
      {"id": "trouble_3", "label": "アニメーションが動かない"},
      {"id": "trouble_4", "label": "画像が表示されない"}
    ]
  }]
}
```

### トラブル1: Tailwind CSSが効かない
**解決策**: `<script src="https://cdn.tailwindcss.com"></script>` が `<head>` 内にあるか確認してください。

### トラブル2: レスポンシブが崩れる
**解決策**: `<meta name="viewport" content="width=device-width, initial-scale=1.0">` があるか確認。Tailwindのブレークポイント（sm: md: lg:）を正しく使っているか確認。

### トラブル3: アニメーションが動かない
**解決策**: `main.js` が正しく読み込まれているか確認。`<script src="js/main.js" defer></script>` を `</body>` の前に配置。

### トラブル4: 画像が表示されない
**解決策**: 画像パスが相対パスで正しいか確認。`images/` ディレクトリにファイルが存在するか確認。

---

## ✅ チェックポイント
- [ ] コード化ガイドラインを取得した
- [ ] プロジェクト構造が作成されている
- [ ] index.html が完成している
- [ ] レスポンシブ対応している
- [ ] アニメーションが動作する
- [ ] ブラウザで動作確認済み


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/lp/
├── index.html  (ランディングページ)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/lp/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/lp/index.html
```

> 💡 HTMLの構造確認: `head -30 output/lp/index.html`

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```text
output/lp-project/ のファイル一覧を表示し、
index.html のセクション数とファイルサイズを確認してください。
```

**期待される結果**: プロジェクトファイルの一覧とサイズが表示されます。

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
      {"id": "next_auto", "label": "次のセクション（Vercelデプロイ）を開始"},
      {"id": "next_window", "label": "新しいウィンドウで /start-13-5 を開始"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-13-5 を実行
- next_window → 新しいウィンドウで /start-13-5
- finish → 終了
