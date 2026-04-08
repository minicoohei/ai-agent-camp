---
description: "When the user says /start-13-3 — Module 13 Lesson 13-3: LP制作 - Pencilデザインファイル作成"
prerequisites: ["start-13-2", "setup-pencil"]
duration: "約30分"
level: "intermediate"
tags: ["lp", "pencil", "design", "mockup"]
---

# 🎓 Lesson 13-3: デザインファイル作成（Pencil MCP）

## 📍 このセッションでやること

**Lesson 13-3: デザインファイル作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Pencil MCP を使ってLP/HPのデザインファイル（.pen）を作成する |
| 所要時間 | 約30分 |
| 使うスキル | lp-designer, Pencil MCP（user-pencil） |
| 前提条件 | Lesson 13-2 完了（output/lp-wireframe.txt が存在）、Pencil MCP セットアップ済み（/setup-pencil） |
| 教材ページ | [Module 13: LP/HP制作](https://ai-agent.camp/ja/course/module-13) を並行参照 |

> **💡 ツール情報**: このレッスンでは Pencil MCP を使用します。Cursor IDE、Claude Code（CLI/デスクトップ）のいずれでも利用可能です。Codex CLI 等の一部環境では `request_user_input is not supported` エラーが出る場合があります。その場合は「代替ワークフロー」セクションを参照してください。

**このセッションの流れ:**
1. Pencil で `output/lp/lp-design.pen` にデザインファイルを作成
2. LPデザインガイドラインの取得
3. スタイルガイドの適用
4. セクションごとのデザイン作成
5. デザイン確認とスクリーンショット書き出し

セッション終了時には、プロ品質のデザインファイルが完成しています。

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
(check_prereq → Pencil MCP の接続確認)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 新規Pencilドキュメント作成

Pencil MCP で新しい .pen ファイルを作成します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Pencilドキュメント作成",
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
Pencil MCPでLPデザイン用の新規ドキュメントを作成してください。

手順:
1. mkdir -p output/lp で保存先ディレクトリを作成
2. get_editor_state() で現在の状態を確認
3. open_document("output/lp/lp-design.pen") で .pen ファイルを作成
4. ファイルが開いたことを確認

保存先: output/lp/lp-design.pen
```

**期待される結果**: `output/lp/lp-design.pen` にデザインファイルが作成・オープンされます。

---

## 🚀 Step 2: LPデザインガイドライン取得

Pencil のランディングページ用ガイドラインを取得します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: デザインガイドライン",
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
Pencil MCPでLPデザインのガイドラインを取得してください。

手順:
1. get_guidelines(topic="landing-page") でLPデザインルールを取得
2. ガイドラインの要点をまとめて表示
3. 特に重要なルール（レイアウト、タイポグラフィ、カラー）をハイライト

このガイドラインに従ってデザインを進めます。
```

**期待される結果**: LPデザインのルールとベストプラクティスが表示されます。

---

## 🚀 Step 3: スタイルガイド適用

デザイントーンに合ったスタイルガイドを選択・適用します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: スタイルガイド選択",
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
output/lp-brief.md からデザイントーンを読み取り、
Pencil MCPでスタイルガイドを適用してください。

手順:
1. get_style_guide_tags でタグ一覧を取得
2. ブリーフのデザイントーンに合うタグを選択
3. get_style_guide(tags=["landing-page", "{トーン}", "{カテゴリ}"]) でスタイル取得
4. スタイルの配色・フォント・レイアウトパターンを確認

選択したスタイルの概要をまとめてください。
```

**期待される結果**: デザイントーンに合ったスタイルガイドが適用されます。

---

## 🚀 Step 4: セクションデザイン作成

batch_design を使って各セクションを作成します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: セクションデザイン",
  "questions": [{
    "id": "design_approach",
    "prompt": "デザインのアプローチを選んでください",
    "options": [
      {"id": "all_at_once", "label": "全セクションを一括で作成"},
      {"id": "step_by_step", "label": "1セクションずつ確認しながら作成"},
      {"id": "hero_first", "label": "まずHeroセクションだけ作成"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
output/lp-brief.md と output/lp-wireframe.txt を参照し、
Pencil MCP の batch_design を使って LP のデザインを作成してください。

以下のセクションを順番に作成:

1. **Hero セクション**
   - 背景: グラデーションまたは画像
   - ヘッドライン（H1）: ブリーフのコピーを使用
   - サブヘッドライン
   - CTAボタン（目立つ色、角丸）
   - Hero画像またはモックアップ

2. **Pain Points セクション**
   - セクションタイトル
   - 3つの課題カード（アイコン + テキスト）

3. **Solution セクション**
   - 左: 説明テキスト（ベネフィット3点）
   - 右: サービスのスクリーンショットまたはイラスト

4. **Features セクション**
   - セクションタイトル
   - 3-4つの機能カード（アイコン + タイトル + 説明）

5. **Social Proof セクション**
   - お客様の声カード（写真 + 名前 + 会社 + コメント）
   - 星レーティング

6. **FAQ セクション**
   - アコーディオン形式の Q&A 3-5個

7. **Final CTA セクション**
   - 背景色付き
   - ヘッドライン + CTAボタン

8. **Footer**
   - リンク群 + コピーライト

各セクション作成後に get_screenshot で確認してください。
```

**期待される結果**: 全セクションがデザインされた .pen ファイルが完成します。

---

## 🚀 Step 5: デザイン確認と調整

完成したデザインを視覚的に確認します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: デザイン確認",
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
Pencil MCP の get_screenshot でデザイン全体のスクリーンショットを取得し、
以下の観点でレビューしてください:

1. **一貫性**: 色・フォント・間隔がスタイルガイドと合っているか
2. **視覚的階層**: ヘッドラインが目立ち、CTAが見つけやすいか
3. **余白**: セクション間の余白が適切か
4. **コントラスト**: テキストの可読性は十分か
5. **CTA**: ボタンが目立ち、クリックしたくなるか

問題があれば batch_design で修正し、再度 get_screenshot で確認してください。

最後に、完成したデザインのスクリーンショットを保存してください:
1. mkdir -p output/lp/design
2. get_screenshot() でフルページのスクリーンショットを取得
3. output/lp/design/lp-full.png に保存
```

**期待される結果**: デザインがレビュー・調整され、`output/lp/design/lp-full.png` にスクリーンショットが保存されます。

---

## 🔄 代替ワークフロー（非GUI環境向け）

Pencil MCP が利用できない環境（Claude Code、Codex CLI、SSH等）では、HTML + Tailwind CSS で直接デザインモックアップを作成します。

1. `output/lp-wireframe.txt` と `output/lp-brief.md` を参照してデザイン要件を確認
2. `output/lp-project/` に HTML + Tailwind CSS CDN でモックアップを直接実装:
   ```bash
   mkdir -p output/lp-project
   ```
3. 各セクション（Hero、Pain Points、Solution、Features、Social Proof、FAQ、CTA、Footer）を HTML で作成
4. Tailwind のユーティリティクラスでスタイルガイド相当の配色・フォント・余白を適用
5. `.pen` ファイルの代わりに完成した HTML ファイルを成果物とし、13-4 へそのまま進む

> この方法では 13-4 の「.pen ファイルが前提」の手順をスキップし、直接 HTML 実装に取り組めます。

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
      {"id": "trouble_1", "label": "Pencil MCP に接続できない"},
      {"id": "trouble_2", "label": "batch_design でエラーが出る"},
      {"id": "trouble_3", "label": "スタイルガイドが見つからない"},
      {"id": "trouble_4", "label": "デザインが崩れて見える"}
    ]
  }]
}
```

### トラブル1: Pencil MCP に接続できない
**解決策**: Cursor の MCP 設定で user-pencil が有効になっているか確認してください。設定 → MCP Servers で確認できます。

### トラブル2: batch_design でエラーが出る
**解決策**: 操作の構文が正しいか確認してください。`get_guidelines` で最新の構文ルールを取得できます。

### トラブル3: スタイルガイドが見つからない
**解決策**: `get_style_guide_tags` で利用可能なタグを確認し、近いものを選んでください。

### トラブル4: デザインが崩れて見える
**解決策**: `snapshot_layout` でレイアウト構造を確認し、ノードの配置を調整してください。

---

## ✅ チェックポイント
- [ ] `output/lp/lp-design.pen` が作成されている
- [ ] LPデザインガイドラインを確認した
- [ ] スタイルガイドが適用されている
- [ ] 全セクション（Hero〜Footer）がデザインされている
- [ ] `output/lp/design/lp-full.png` にスクリーンショットが保存された


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/lp/
├── lp-design.pen          ← Pencil デザインファイル（本体）
└── design/
    └── lp-full.png        ← デザインのスクリーンショット
```

### 確認コマンド
```bash
# .pen ファイルの存在確認
ls -lh output/lp/lp-design.pen

# スクリーンショットの確認
ls -la output/lp/design/

# 画像を開く（macOS: open / Linux: xdg-open）
open output/lp/design/lp-full.png
```

> 💡 **Claude Code**: `Read output/lp/design/lp-full.png` でチャット内プレビュー
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー
> 💡 **.pen ファイル**: Pencil MCP の `batch_get` や `get_screenshot` で中身を確認できます

---

## ✅ 完了チェック
以下をチャットに貼り付けて、完了状況を確認してください:

```text
以下のファイルが存在するか確認してください:
1. output/lp/lp-design.pen（Pencil デザインファイル）
2. output/lp/design/lp-full.png（スクリーンショット）

また、get_editor_state() で現在のドキュメント状態を確認し、
作成されたセクション（ノード）の一覧を表示してください。
```

**期待される結果**: .pen ファイルとスクリーンショットの存在確認、デザイン要素の一覧が表示されます。

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
      {"id": "next_auto", "label": "次のセクション（LP実装）を開始"},
      {"id": "next_window", "label": "新しいウィンドウで /start-13-4 を開始"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-13-4 を実行
- next_window → 新しいウィンドウで /start-13-4
- finish → 終了
