---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "約30分"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "x-post", "banner", "sns"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 17-1: X投稿 & バナー作成

## 📍 このセッションでやること

**Lesson 17-1: X投稿 & バナー作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | social-content + banner-creator スキルでX投稿テキストとバナーを作成する |
| 所要時間 | 約30分 |
| 使うスキル | social-content, banner-creator (Gemini Image Generation API) |
| 前提条件 | Gemini APIキー設定済み |
| 教材ページ | [Module 17: マーケティング](https://ai-agent.camp/ja/course/module-17) を並行参照 |

**このセッションの流れ:**
1. X投稿のベストプラクティスを理解する（投稿時間、ハッシュタグ、文字数制限）
2. social-contentスキルでX投稿テキスト3パターンを作成する
3. banner-creatorでX投稿用バナーを作成する（1200x675px）

セッション終了時には、X投稿テキスト3パターンとバナー画像1枚が完成しています。

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

## 🚀 Step 1: X投稿のベストプラクティスを理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: X投稿のベストプラクティスを理解する",
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
X（Twitter）投稿のベストプラクティスを教えてください。
以下の点をカバーしてください：
- 最適な投稿時間帯
- ハッシュタグの効果的な使い方（個数、選び方）
- 文字数制限（140字 vs 280字）と理想的な長さ
- エンゲージメントを高めるテクニック
```

**期待される結果**: X投稿の最適な投稿時間、ハッシュタグ戦略、文字数のベストプラクティスが説明されます。

---

## 🚀 Step 2: social-contentスキルでX投稿テキスト3パターンを作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: X投稿テキスト3パターンを作成する",
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
social-contentスキルを使って、以下のテーマでX投稿テキストを3パターン作成してください：
テーマ: 「Cursor Bootcamp - AIエージェント活用研修」
ターゲット: ビジネスパーソン、非エンジニア
トーン: 親しみやすく、興味を引く

パターン1: 問いかけ型（〜していませんか？）
パターン2: 実績・数字型（〜%の効率化）
パターン3: ストーリー型（体験談風）

各パターンにハッシュタグも含めてください。
```

**期待される結果**: 3パターンのX投稿テキストが生成され、それぞれ異なるアプローチで訴求されます。

---

## 🚀 Step 3: banner-creatorでX投稿用バナーを作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: X投稿用バナーを作成する",
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
banner-creatorを使って、X投稿用のバナーを作成してください。
トピック: 「Cursor Bootcamp - AIで業務効率を10倍に」
プラットフォーム: x_post（1200x675px）
スタイル: モダン、テック感、ビジネス向け
出力先: ~/ai-agent-camp/outputs/marketing-12-1-banner.png
```

**期待される結果**: outputs フォルダに 1200x675px のX投稿用バナー画像が生成されます。

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
      {"id": "trouble_1", "label": "APIエラーが発生する"},
      {"id": "trouble_2", "label": "投稿テキストが長すぎる"},
      {"id": "trouble_3", "label": "バナーサイズが合わない"},
      {"id": "trouble_4", "label": "画像が生成されない"}
    ]
  }]
}
```


### トラブル1: 「APIエラーが発生する」
**原因**: Gemini APIキーが未設定、またはレート制限
**解決プロンプト**:
```
Gemini APIキーが正しく設定されているか確認してください。
環境変数 GEMINI_API_KEY の値を確認してください。
レート制限の場合は30秒ほど待ってから再実行してください。
```

### トラブル2: 「投稿テキストが長すぎる」
**原因**: X投稿の280文字制限を超えている
**解決プロンプト**:
```
生成されたテキストを280文字以内に収まるよう短縮してください。
ハッシュタグも文字数に含まれるので注意してください。
日本語は1文字=半角2文字換算ではなく、1文字=1文字としてカウントされます。
```

### トラブル3: 「バナーサイズが合わない」
**原因**: プラットフォーム指定が正しくない
**解決プロンプト**:
```
banner-creatorの--platformオプションを「x_post」に指定してください。
これにより自動的に1200x675px（16:9）で生成されます。
```

### トラブル4: 「画像が生成されない」
**原因**: outputsディレクトリが存在しない、または権限の問題
**解決プロンプト**:
```
outputsディレクトリが存在するか確認し、なければ作成してください。
mkdir -p ~/ai-agent-camp/outputs
```

---

## ✅ チェックポイント
- [ ] X投稿のベストプラクティス（投稿時間、ハッシュタグ、文字数）を理解した
- [ ] social-contentスキルでX投稿テキスト3パターンを作成できた
- [ ] banner-creatorでX投稿用バナー（1200x675px）を1枚生成できた
- [ ] outputsフォルダにバナー画像ファイルが保存された


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
# 完了確認: outputs/ フォルダに期待される出力ファイルが生成されているか確認してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-17-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-17-2
- finish → 終了
