---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
duration: "約30分"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["banner", "image", "gemini"]
---

# 🎓 Lesson 1-1: バナー生成入門

## 📍 このセッションでやること

**Lesson 1-1: バナー生成入門** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | banner-creatorスキルで X投稿用バナーを1枚作成する |
| 所要時間 | 約30分 |
| 使うスキル | banner-creator (Gemini Image Generation API) |
| 前提条件 | Gemini APIキー設定済み、Python環境セットアップ済み |
| 教材ページ | [Module 1: バナー・画像生成](https://ai-agent.camp/ja/course/module-1) を並行参照 |

**このセッションの流れ:**
1. X投稿用バナーのサイズを理解する
2. 最初のバナーを1枚生成する
3. トピックを変えて3枚練習する

セッション終了時には、outputsフォルダにあなたが作ったバナー画像が保存されています。

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

## 🚀 Step 1: X投稿用バナーのサイズを理解する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: X投稿用バナーのサイズを理解する",
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
X（Twitter）投稿用バナーの推奨サイズと、各SNSの画像サイズの違いを教えてください。
```

**期待される結果**: X投稿用の推奨サイズ（1200x675px、16:9）と他のSNSとの違いが説明されます。

---

## 🚀 Step 2: 最初のバナーを生成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 最初のバナーを生成する",
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
トピック: 「AIで業務効率化」
スタイル: モダン、ビジネス向け
出力先: docs/generated/banners/banner-1-1.png
```

**期待される結果**: `docs/generated/banners/` フォルダにバナー画像が生成されます。

---

## 🚀 Step 3: トピックを変えて練習する

以下のプロンプトで、異なるトピックのバナーを作成してみましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: トピックを変えて練習する",
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
以下の3つのトピックでX投稿用バナーを作成してください：
1. 「週末限定セール開催中」
2. 「新サービスリリース記念キャンペーン」
3. 「採用情報：エンジニア募集」

それぞれ別のファイル名で保存してください。
```

**期待される結果**: 3つの異なるバナーが生成され、トピックごとにデザインが変わります。

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
      {"id": "trouble_1", "label": "「モジュールが見つからない」エラー"},
      {"id": "trouble_2", "label": "画像が生成されない"},
      {"id": "trouble_3", "label": "デザインが気に入らない"},
      {"id": "trouble_4", "label": "APIエラーが発生する"}
    ]
  }]
}
```


### トラブル1: 「モジュールが見つからない」エラー
**原因**: 必要なPythonパッケージがインストールされていない
**解決プロンプト**:
```
banner-creatorの実行に必要なパッケージをインストールしてください。
uv add pillow requests を実行してください。
```

### トラブル2: 「画像が生成されない」
**原因**: 出力先ディレクトリが存在しない、または権限の問題
**解決プロンプト**:
```
docs/generated/banners/ ディレクトリが存在するか確認し、なければ作成してください。
```

### トラブル3: 「デザインが気に入らない」
**原因**: トピックの指定が抽象的すぎる
**解決プロンプト**:
```
トピックをより具体的にして再生成してください：
「AIで業務効率化」→「AIチャットボットで問い合わせ対応を80%自動化」
```

### トラブル4: 「APIエラーが発生する」
**原因**: Gemini APIキーが未設定、またはレート制限
**解決プロンプト**:
```
Gemini APIキーが正しく設定されているか確認してください。
環境変数 GEMINI_API_KEY が設定されているか（空でないか）を確認してください。
※ セキュリティのため、キーの実際の値は表示しないでください。
```

---

## ✅ チェックポイント
- [ ] X投稿用バナーの推奨サイズを理解した
- [ ] banner-creatorを使ってバナーを生成できた
- [ ] `docs/generated/banners/` フォルダに画像ファイルが保存された
- [ ] 練習課題（3つのバナー）を完了した


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 docs/generated/banners/
├── banner-{テーマ名}.png
└── (バリエーション)
```
> 形式: PNG | サイズ: 自動設定

### 確認コマンド
```bash
# ファイル一覧
ls -la docs/generated/banners/

# 画像を開く（macOS: open / Linux: xdg-open）
open docs/generated/banners/
```

> 💡 **Claude Code**: Read ツールでファイルパスを指定するとチャット内で画像プレビューできます
> 💡 **Cursor**: ファイルエクスプローラーで画像をクリックしてプレビュー

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: docs/generated/banners/ フォルダにバナー画像が生成されているか確認してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-1-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-1-2
- finish → 終了
