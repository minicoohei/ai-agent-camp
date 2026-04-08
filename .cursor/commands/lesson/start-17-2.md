---
description: "When the user says /start-17-2 — Module 17 Lesson 17-2: SEO調査 & キーワード戦略"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "約40分"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "seo", "keyword", "audit"]
---

# 🎓 Lesson 17-2: SEO調査 & キーワード戦略

## 📍 このセッションでやること

**Lesson 17-2: SEO調査 & キーワード戦略** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | seo-audit + programmatic-seo スキルでSEO監査とキーワード戦略を策定する |
| 所要時間 | 約40分 |
| 使うスキル | seo-audit, programmatic-seo |
| 前提条件 | Gemini APIキー設定済み |
| 教材ページ | [Module 17: マーケティング](https://ai-agent.camp/ja/course/module-17) を並行参照 |

**このセッションの流れ:**
1. SEO監査の基本項目を理解する
2. seo-auditスキルでターゲットサイトのSEO課題を診断する
3. programmatic-seoでキーワード戦略とページテンプレートを設計する

セッション終了時には、SEO監査レポートとキーワードリストが完成しています。

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

## 🚀 Step 1: SEO監査の基本項目を理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: SEO監査の基本項目を理解する",
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
SEO監査で確認すべき基本項目を教えてください。
以下のカテゴリに分けて説明してください：
- テクニカルSEO（サイト速度、クロール、インデックス）
- オンページSEO（タイトル、メタディスクリプション、見出し構造）
- コンテンツSEO（キーワード密度、内部リンク、コンテンツ品質）
- オフページSEO（被リンク、ドメインオーソリティ）
```

**期待される結果**: SEO監査の4カテゴリの基本項目と、各項目のチェックポイントが説明されます。

---

## 🚀 Step 2: seo-auditスキルでSEO課題を診断する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: seo-auditでSEO課題を診断する",
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
seo-auditスキルを使って、以下のサイトのSEO課題を診断してください：
URL: https://example.com（自社サイトまたは練習用サイト）

以下の項目を重点的にチェックしてください：
- メタタグ（title、description）の最適化状況
- 見出し構造（H1〜H3）の適切さ
- 画像のalt属性の有無
- 内部リンク構造
- モバイルフレンドリー対応

結果をレポート形式でoutput/seo-audit-report.mdに保存してください。
```

**期待される結果**: SEO監査レポートが生成され、改善すべき課題が優先度付きでリストアップされます。

---

## 🚀 Step 3: programmatic-seoでキーワード戦略を設計する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: キーワード戦略とページテンプレートを設計する",
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
programmatic-seoスキルを使って、「AIエージェント活用」をテーマにキーワード戦略を設計してください。

以下を含めてください：
1. メインキーワード（5個）とロングテールキーワード（15個）のリスト
2. キーワードの検索意図分類（情報収集/比較検討/購入意思）
3. 各キーワードに対応するページテンプレート案
4. トピッククラスター構造（ピラーページ + サテライト記事）

結果をoutput/keyword-strategy.mdに保存してください。
```

**期待される結果**: キーワードリストとページテンプレート案、トピッククラスター構造が設計されます。

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
      {"id": "trouble_1", "label": "SEO監査の結果が表示されない"},
      {"id": "trouble_2", "label": "URLにアクセスできないエラー"},
      {"id": "trouble_3", "label": "キーワードリストが少なすぎる"},
      {"id": "trouble_4", "label": "レポートファイルが保存されない"}
    ]
  }]
}
```


### トラブル1: 「SEO監査の結果が表示されない」
**原因**: 対象サイトのHTMLが取得できない、またはスキルの読み込みエラー
**解決プロンプト**:
```
seo-auditスキルの内容を確認してください。
まずスキルファイルを読み込んでから再実行してください：
skills/seo-audit/SKILL.md
```

### トラブル2: 「URLにアクセスできないエラー」
**原因**: 対象URLが存在しない、またはアクセス制限
**解決プロンプト**:
```
対象URLが正しくアクセス可能か確認してください。
練習用にはhttps://ai-agent.camp/ja/course などのWebページを対象にすることもできます。
```

### トラブル3: 「キーワードリストが少なすぎる」
**原因**: テーマの指定が狭すぎる
**解決プロンプト**:
```
テーマをより広く設定してキーワードを再生成してください：
「AIエージェント活用」→「AI 業務効率化 ツール 研修 自動化」のように
関連する複数の概念を含めてください。
```

### トラブル4: 「レポートファイルが保存されない」
**原因**: outputディレクトリが存在しない
**解決プロンプト**:
```
outputディレクトリが存在するか確認し、なければ作成してください。
mkdir -p ~/ai-agent-camp/output
```

---

## ✅ チェックポイント
- [ ] SEO監査の基本項目（テクニカル/オンページ/コンテンツ/オフページ）を理解した
- [ ] seo-auditスキルでSEO課題を診断できた
- [ ] SEO監査レポートがoutputフォルダに保存された
- [ ] キーワードリスト（メイン5個+ロングテール15個）が完成した
- [ ] トピッククラスター構造を設計できた


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/marketing/
├── banner-*.png
└── (バリエーション)
```
> 形式: PNG | サイズ: 自動設定

### 確認コマンド
```bash
# ファイル一覧
ls -la output/marketing/

# 画像を開く（macOS: open / Linux: xdg-open）
open output/marketing/
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-17-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-17-3
- finish → 終了
