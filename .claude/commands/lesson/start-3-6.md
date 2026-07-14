---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1", "start-3-2", "start-3-3", "start-3-4", "start-3-5"]
duration: "約40分"
level: "intermediate"
tags: ["screenshot", "capstone", "manual"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-6: Module 3 総合演習

## 📍 このセッションでやること

**Lesson 3-6: Module 3 総合演習** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Module 3 の全スキルを統合し、操作マニュアル生成プロジェクトを完成させる |
| 所要時間 | 約40分 |
| 使うスキル | screenshot-analyzer, tutorial-generator, screenshot-annotator の総合 |
| 前提条件 | Lesson 3-1〜Lesson 3-5 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. プロジェクトの選択と要件整理
2. 分析・チュートリアル・注釈の一連の実行
3. 完成品の確認とModule 3の振り返り

セッション終了時には、実践的な操作マニュアルが完成し、Module 3 を修了しています。

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

## 🚀 Step 1: プロジェクトの選択

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: プロジェクトの選択",
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
以下の演習プロジェクトから1つ選んでください：

【初級】Webアプリマニュアル（30-40分）
- 対象: 5機能程度のWebアプリ
- 成果物: HTML形式のユーザーマニュアル

【中級】エラー診断レポート（40-50分）
- 対象: 複数のエラー画面
- 成果物: 優先度付き診断レポート + 解決手順書

【上級】マルチプラットフォーム対応（60-90分）
- 対象: PC版 + モバイル版
- 成果物: 両プラットフォーム対応の完全マニュアル

どのプロジェクトを実施するか選んでください。
選んだら、そのプロジェクトの詳細な手順を案内します。
```

**期待される結果**: 選択したプロジェクトの詳細な実施手順が案内されます。

---

## 🚀 Step 2: 【初級】Webアプリマニュアル作成

初級プロジェクトの実施例です：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 【初級】Webアプリマニュアル作成",
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
Gmailのユーザーマニュアルを作成します。

対象ユーザー: 初心者（60代以上のシニア層）
主要機能:
1. ログイン
2. メール受信・閲覧
3. メール作成・送信
4. ラベル管理
5. メール検索

成果物の要件:
- マニュアルHTML: 全5機能以上をカバー
- スクリーンショット: 15枚以上
- トラブルシューティング: 3項目以上

courses/aiagent/lesson03-core/module03-screenshot/practice/data/tutorial-samples/ に
Gmailのスクリーンショットを正式素材として配置した前提で、
マニュアル作成を開始してください。
```

**期待される結果**: シニア向けの丁寧なGmailマニュアルが作成されます。

---

## 🚀 Step 3: 【中級】エラー診断レポート作成

中級プロジェクトの実施例です：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 【中級】エラー診断レポート作成",
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
複数のシステムエラー画面から診断レポートを作成してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/ 内の全エラー画像
出力: output/error-report/

レポート内容:
1. エラー一覧表（優先度、原因、解決策）
2. 各エラーの詳細分析
3. 対応フローチャート
4. 予防措置の提案

出力形式:
- HTML形式の診断レポート
- 優先度別に色分けされたエラー画像
- 対応チェックリスト（Markdown）
```

**期待される結果**: 体系的なエラー診断レポートが作成されます。

---

## 🚀 Step 4: 成果物の確認とエクスポート

作成した成果物を確認しましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 成果物の確認とエクスポート",
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
作成したマニュアル/レポートの品質をチェックしてください。

チェック項目:
- [ ] 全ての画像が正しく表示される
- [ ] 日本語が文字化けしていない
- [ ] リンクが正しく機能する
- [ ] モバイルでも読みやすい
- [ ] 初心者でも理解できる表現

問題があれば修正し、最終版を output/final/ に保存してください。
```

**期待される結果**: 品質チェックが完了し、最終版が保存されます。

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
      {"id": "trouble_1", "label": "時間内に完成しない"},
      {"id": "trouble_2", "label": "品質が不十分"},
      {"id": "trouble_3", "label": "ファイル構成が混乱"}
    ]
  }]
}
```


- 時間内に完成しない
- 品質が不十分
- ファイル構成が混乱する

### トラブル1: 「時間内に完成しない」
**原因**: スコープが大きすぎる
**解決プロンプト**:
```
現在の進捗状況を確認してください。
残り時間で完成できる範囲に絞り込み、
優先度の高い部分だけを完成させてください。
```

### トラブル2: 「品質が不十分」
**原因**: レビューが不足している
**解決プロンプト**:
```
マニュアルの品質を向上させるために、
以下の観点でレビューしてください：
- わかりやすさ
- 正確性
- 一貫性
- デザイン

改善点があれば具体的に提案してください。
```

### トラブル3: 「ファイル構成が混乱」
**原因**: 出力先が整理されていない
**解決プロンプト**:
```
プロジェクトのファイル構成を整理してください。

推奨構成:
project-output/
├── README.md
├── screenshots/
├── tutorials/
├── manual/
├── annotations/
└── scripts/

この構成に合わせてファイルを移動してください。
```

---

## ✅ チェックポイント

### Module 3 修了チェックリスト

### 技術スキル
- [ ] screenshot-analyzer を3回以上使用した
- [ ] tutorial-generator を3回以上使用した
- [ ] screenshot-annotator を5回以上使用した
- [ ] 自作スクリプトで自動化を実装した
- [ ] HTML統合ドキュメントを作成した

### 成果物
- [ ] 実用的なユーザーマニュアルが完成した
- [ ] 統合されたHTMLドキュメントがある
- [ ] 注釈付きスクリーンショットが作成された
- [ ] 実際のユースケースに基づいている

---

## 🎉 Module 3 完了！

おめでとうございます！以下のスキルを習得しました：
- スクリーンショットから自動的にエラー原因を診断
- ステップバイステップのチュートリアルを生成
- 注釈を使ってUIを図解
- 実用的なユーザーマニュアルを作成
- 複雑なプロセスを自動化


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-4-1
- finish → 終了
