---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "約35分"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "copywriting", "lp", "ab-test"]
---

# 🎓 Lesson 17-3: コピーライティング

## 📍 このセッションでやること

**Lesson 17-3: コピーライティング** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | copywritingスキルでLP/機能ページのコピーを作成し、A/Bテスト用バリエーションを生成する |
| 所要時間 | 約35分 |
| 使うスキル | copywriting, ab-test-setup |
| 前提条件 | Gemini APIキー設定済み |
| 教材ページ | [Module 17: マーケティング](https://ai-agent.camp/ja/course/module-17) を並行参照 |

**このセッションの流れ:**
1. 効果的なLPコピーの構造を理解する（ヒーロー、課題、解決策、CTA）
2. 「Cursor Bootcamp」LPのコピーを作成する
3. A/Bテスト用のバリエーションを生成する

セッション終了時には、LPコピー1セットとバリエーション2パターンが完成しています。

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

## 🚀 Step 1: 効果的なLPコピーの構造を理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: LPコピーの構造を理解する",
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
効果的なランディングページ（LP）のコピー構造を教えてください。
以下のセクションごとに、役割と書き方のコツを説明してください：
1. ヒーローセクション（キャッチコピー + サブコピー）
2. 課題提起（ユーザーの悩みを言語化）
3. 解決策（プロダクトの価値提案）
4. 社会的証明（実績、お客様の声）
5. 特徴・メリット（3〜5個）
6. CTA（行動喚起）
7. FAQ（よくある質問）
```

**期待される結果**: LPの各セクションの役割と、効果的なコピーの書き方パターンが説明されます。

---

## 🚀 Step 2: 「Cursor Bootcamp」LPのコピーを作成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: LPコピーを作成する",
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
copywritingスキルを使って、「Cursor Bootcamp」のLPコピーを作成してください。

プロダクト情報:
- 名前: Cursor Bootcamp
- 概要: 非エンジニア向けのAIエージェント（Claude Code / Cursor）活用研修
- ターゲット: ビジネスパーソン、企業研修参加者
- 価値: AI活用で業務効率を劇的に改善、プログラミング不要
- 実績: 11モジュール、85以上のコマンド、21のスキル搭載
- 価格: お問い合わせベース

以下のセクションのコピーを作成してください：
1. ヒーローセクション（キャッチコピー + サブコピー）
2. 課題提起
3. 解決策
4. 特徴（3つ）
5. CTA

結果をoutput/lp-copy-v1.mdに保存してください。
```

**期待される結果**: Cursor Bootcamp のLPコピーが各セクションごとに生成され、Markdownファイルとして保存されます。

---

## 🚀 Step 3: A/Bテスト用のバリエーションを生成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: A/Bテスト用バリエーションを生成する",
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
先ほど作成したLPコピー（output/lp-copy-v1.md）をもとに、
A/Bテスト用のバリエーションを2パターン作成してください。

バリエーションA（output/lp-copy-v2a.md）:
- ヒーローコピーを「恐怖訴求」型に変更（このまま手作業を続けますか？）
- CTAを「今すぐ体験」に変更

バリエーションB（output/lp-copy-v2b.md）:
- ヒーローコピーを「実績訴求」型に変更（受講者の95%が業務効率化を実感）
- CTAを「無料で相談する」に変更

各パターンの狙いと、どの指標で効果を測るかも記載してください。
```

**期待される結果**: 2つのバリエーションが生成され、A/Bテストの測定指標も含まれます。

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
      {"id": "trouble_1", "label": "コピーが長すぎる・冗長になる"},
      {"id": "trouble_2", "label": "ターゲットに合わないトーンになる"},
      {"id": "trouble_3", "label": "バリエーションの違いが小さすぎる"},
      {"id": "trouble_4", "label": "ファイルが保存されない"}
    ]
  }]
}
```


### トラブル1: 「コピーが長すぎる・冗長になる」
**原因**: プロンプトで文字数や文量の指定がない
**解決プロンプト**:
```
各セクションの目安文字数を指定して再生成してください：
- ヒーロー: キャッチコピー20字以内、サブコピー60字以内
- 課題提起: 100字以内
- 特徴: 各50字以内
- CTA: 10字以内
```

### トラブル2: 「ターゲットに合わないトーンになる」
**原因**: ターゲット像が曖昧
**解決プロンプト**:
```
ターゲットをより具体的に指定して再生成してください：
「ビジネスパーソン」→「30〜40代の営業部マネージャー、ITリテラシーは中程度、
日常的にExcelとPowerPointを使う」
```

### トラブル3: 「バリエーションの違いが小さすぎる」
**原因**: 変更指示が具体的でない
**解決プロンプト**:
```
バリエーションの変更箇所をより明確に指定してください。
訴求軸自体を変える（機能訴求 vs 感情訴求 vs 実績訴求）と
大きな違いが生まれます。
```

### トラブル4: 「ファイルが保存されない」
**原因**: outputディレクトリが存在しない
**解決プロンプト**:
```
outputディレクトリが存在するか確認し、なければ作成してください。
mkdir -p ~/ai-agent-camp/output
```

---

## ✅ チェックポイント
- [ ] LPコピーの構造（ヒーロー/課題/解決策/特徴/CTA）を理解した
- [ ] copywritingスキルで「Cursor Bootcamp」のLPコピーを1セット作成できた
- [ ] A/Bテスト用のバリエーションを2パターン生成できた
- [ ] outputフォルダにlp-copy-v1.md、lp-copy-v2a.md、lp-copy-v2b.mdが保存された


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-17-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-17-4
- finish → 終了
