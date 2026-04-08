---
description: "When the user says /start-13-2 — Module 13 Lesson 13-2: LP制作 - ワイヤーフレーム作成"
prerequisites: ["start-13-1"]
duration: "約25分"
level: "intermediate"
tags: ["lp", "wireframe", "design", "information-architecture"]
---

# 🎓 Lesson 13-2: ワイヤーフレーム作成（ASCII + ビジュアルWF）

## 📍 このセッションでやること

**Lesson 13-2: ワイヤーフレーム作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | LP/HPのセクション構造をASCII WFとビジュアルWFで設計する |
| 所要時間 | 約25分 |
| 使うスキル | lp-designer, diagram-generator |
| 前提条件 | Lesson 13-1 完了（output/lp-brief.md が存在） |
| 教材ページ | [Module 13: LP/HP制作](https://ai-agent.camp/ja/course/module-13) を並行参照 |

**このセッションの流れ:**
1. ブリーフの読み込みとセクション確認
2. ASCII ワイヤーフレームの作成
3. diagram-generator でビジュアルWF生成
4. セクション間の情報設計レビュー

セッション終了時には、LPの構造設計が完成しています。

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
(check_prereq → output/lp-brief.md の存在確認)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: ブリーフの読み込み

13-1 で作成したブリーフを確認します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ブリーフの読み込み",
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
output/lp-brief.md を読み込んで、以下を確認してください:

1. セクション構成が明確か
2. 各セクションに必要なコンテンツが定義されているか
3. セクション間の論理的な流れが適切か

確認結果をサマリーで表示してください。
```

**期待される結果**: ブリーフの内容がサマリーとして表示されます。

---

## 🚀 Step 2: ASCII ワイヤーフレーム作成

テキストベースでLPの構造を設計します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ASCII ワイヤーフレーム",
  "questions": [{
    "id": "wf_style",
    "prompt": "ワイヤーフレームのスタイルを選んでください",
    "options": [
      {"id": "single_column", "label": "シングルカラム（シンプルLP向け）"},
      {"id": "two_column", "label": "2カラム構成（説明+画像の並列）"},
      {"id": "card_grid", "label": "カードグリッド（機能紹介向け）"},
      {"id": "full_width", "label": "フルワイド（インパクト重視）"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```text
output/lp-brief.md のセクション構成をもとに、ASCII ワイヤーフレームを作成してください。

フォーマット:
- 罫線文字（┌─┐│└─┘）を使用
- 各セクションの幅・高さの比率を視覚的に表現
- テキスト配置、画像配置、ボタン位置を [ ] で表示
- レスポンシブ時のレイアウト変更も併記

出力先: output/lp-wireframe.txt

以下のセクションを含めてください:
1. Header / Navigation
2. Hero セクション
3. Pain Points セクション
4. Solution セクション
5. Features セクション
6. Social Proof セクション
7. FAQ セクション
8. Final CTA セクション
9. Footer
```

**期待される結果**: ASCII ワイヤーフレームが `output/lp-wireframe.txt` に保存されます。

---

## 🚀 Step 3: ビジュアルWF生成（diagram-generator）

diagram-generator を使って、ビジュアルなワイヤーフレームを生成します。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ビジュアルWF生成",
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
output/lp-wireframe.txt のASCII WFをもとに、ビジュアルなワイヤーフレームを
diagram-generator で生成してください。

実行コマンド:
uv run python tools/generate_diagram.py --topic "LPワイヤーフレーム: Hero→PainPoints→Solution→Features→SocialProof→FAQ→CTA の構成図。各セクションの配置とコンテンツ要素を図示" --style minimalist

出力先: output/images/lp-wireframe.png

生成後、画像を確認してセクション構成が正しいか確認してください。
```

**期待される結果**: `output/images/lp-wireframe.png` にビジュアルWFが生成されます。

---

## 🚀 Step 4: 情報設計レビュー

生成したWFの情報設計を確認し、改善点をチェックします。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 情報設計レビュー",
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
作成したWF（output/lp-wireframe.txt と output/images/lp-wireframe.png）をレビューし、
以下の観点で改善提案をしてください:

## レビュー観点
1. **ストーリーフロー**: 課題→解決策→根拠→行動 の流れが自然か
2. **CTA配置**: ファーストビューとラストに十分なCTAがあるか
3. **情報量バランス**: 各セクションの情報量が適切か（多すぎ/少なすぎ）
4. **スキャナビリティ**: 流し読みでも要点が伝わるか
5. **モバイル対応**: スマホで見たときの構成に問題はないか

改善があれば output/lp-wireframe.txt を更新してください。
```

**期待される結果**: レビュー結果と改善済みWFが完成します。

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
      {"id": "trouble_1", "label": "ブリーフファイルが見つからない"},
      {"id": "trouble_2", "label": "diagram-generator がエラーになる"},
      {"id": "trouble_3", "label": "WFのレイアウトが崩れる"},
      {"id": "trouble_4", "label": "セクション構成に迷う"}
    ]
  }]
}
```

### トラブル1: ブリーフファイルが見つからない
**解決策**: `/start-13-1` でブリーフを作成するか、架空の内容でブリーフを生成してください。

### トラブル2: diagram-generator がエラーになる
**解決策**: `GEMINI_API_KEY` が設定されているか確認してください（`echo $GEMINI_API_KEY`）。

### トラブル3: WFのレイアウトが崩れる
**解決策**: 等幅フォントで表示されているか確認してください。Cursorのターミナルで表示することを推奨します。

### トラブル4: セクション構成に迷う
**解決策**: 基本テンプレート（Hero → Pain → Solution → Features → Proof → CTA）を使い、不要なセクションは後で削除しましょう。

---

## ✅ チェックポイント
- [ ] ブリーフが読み込まれている
- [ ] ASCII WF が `output/lp-wireframe.txt` に保存されている
- [ ] ビジュアルWF が `output/images/lp-wireframe.png` に生成されている
- [ ] 情報設計レビューが完了している
- [ ] セクション間の流れが論理的


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
output/lp-wireframe.txt と output/images/lp-wireframe.png が存在するか確認し、
セクション構成の概要を表示してください。
```

**期待される結果**: WFファイルの存在確認と構成サマリーが表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次は Pencil MCP のセットアップを行い、デザインファイル作成に進みます。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "setup_pencil", "label": "Pencilセットアップを開始（/setup-pencil）"},
      {"id": "skip_pencil", "label": "Pencil設定済み → デザイン作成へ（/start-13-3）"},
      {"id": "next_window", "label": "新しいウィンドウで /setup-pencil を開始"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- setup_pencil → /setup-pencil を実行（Pencil未導入の場合）
- skip_pencil → /start-13-3 を実行（Pencil導入済みの場合）
- next_window → 新しいウィンドウで /setup-pencil
- finish → 終了
