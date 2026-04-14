---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "約30分"
level: "beginner"
tags: ["image", "nanobanana", "gemini", "editing"]
---

# 🎓 Lesson 1-3: nanobanana画像編集

## 📍 このセッションでやること

**Lesson 1-3: nanobanana画像編集** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | nanobananaスキルでテキストから画像を生成し、既存画像の編集も行う |
| 所要時間 | 約30分 |
| 使うスキル | nanobanana (Gemini Image Generation API) |
| 前提条件 | Lesson 1-1 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 1: バナー・画像生成](https://ai-agent.camp/ja/course/module-1) を並行参照 |

**このセッションの流れ:**
1. テキストから画像を生成する
2. 具体的なシーンの画像を生成する
3. 既存画像の編集（オプション）

セッション終了時には、outputs に生成・編集した画像が保存されています。

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

## 🚀 Step 1: テキストから画像を生成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: テキストから画像を生成する",
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
nanobananaを使って、以下の画像を生成してください：
- スタイル: フラットデザイン
- テーマ: チームワーク
- 用途: ビジネスプレゼンテーション
出力先: ~/ai-agent-camp/output/nanobanana-teamwork.png
```

**期待される結果**: チームワークをテーマにしたフラットデザインの画像が生成されます。

---

## 🚀 Step 2: 具体的なシーンの画像を生成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 具体的なシーンの画像を生成する",
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
nanobananaで「モダンなオフィス風景」の画像を生成してください。
条件：
- フラットデザイン、ミニマル
- 明るい色調
- デスク、観葉植物、窓を含む
出力先: ~/ai-agent-camp/output/nanobanana-office.png
```

**期待される結果**: 指定した条件を満たすオフィス画像が生成されます。

---

## 🚀 Step 3: 既存画像を編集する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 既存画像を編集する",
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
先ほど生成したオフィス画像（nanobanana-office.png）を編集してください：
- 背景を夕焼け空に変更
- 温かみのある照明効果を追加
出力先: ~/ai-agent-camp/output/nanobanana-office-sunset.png
```

**期待される結果**: 元の画像をベースに、夕焼け空の背景に変更された画像が生成されます。

---

## 🚀 Step 4: ロゴ風画像とアイコンを生成する

以下のプロンプトで、ビジネスで使える画像を作成してみましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: ロゴ風画像とアイコンを生成する",
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
nanobananaで以下の2つの画像を生成してください：

1. コーヒーショップのロゴ風画像
   - シンプル、フラットデザイン
   - コーヒーカップのシルエット
   - 出力先: ~/ai-agent-camp/output/logo-coffee.png

2. AIエージェントを象徴するアイコン
   - テクノロジー感、未来的
   - 青と白を基調
   - 出力先: ~/ai-agent-camp/output/icon-ai.png
```

**期待される結果**: ロゴ風画像とアイコンの2つが生成されます。

---

## 🚀 Step 5: スタイルを変えて比較する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: スタイルを変えて比較する",
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
「成長するビジネス」をテーマに、3つの異なるスタイルで画像を生成してください：

1. フラットデザイン（シンプル、ミニマル）
2. 3Dイラスト風（立体的、ポップ）
3. 水彩画風（手描き感、温かみ）

それぞれ別のファイルで保存してください。
```

**期待される結果**: 同じテーマで異なるスタイルの3つの画像が生成され、比較できます。

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
      {"id": "trouble_1", "label": "生成画像が期待と異なる"},
      {"id": "trouble_2", "label": "画像編集が反映されない"},
      {"id": "trouble_3", "label": "APIレート制限エラー"},
      {"id": "trouble_4", "label": "ロゴが複雑すぎる"}
    ]
  }]
}
```


### トラブル1: 「生成画像が期待と異なる」
**原因**: プロンプトが抽象的すぎる
**解決プロンプト**:
```
プロンプトをより具体的に書き直してください：
悪い例: 「きれいな画像」
良い例: 「青空の下、緑の芝生の上でピクニックをしている家族、
        フラットデザイン、明るい色調、16:9のアスペクト比」
```

### トラブル2: 「画像編集が反映されない」
**原因**: 編集指示が不明確、または入力画像のパスが間違っている
**解決プロンプト**:
```
入力画像のパスを確認してください：
ls ~/ai-agent-camp/output/nanobanana-office.png

ファイルが存在する場合、編集指示をより具体的にしてください：
「背景のみを変更」「被写体は維持」など
```

### トラブル3: 「APIレート制限エラー」
**原因**: 短時間に多くのリクエストを送信した
**解決プロンプト**:
```
APIレート制限に達しました。
1分ほど待ってから再度実行してください。
連続生成する場合は、各リクエスト間に5秒の待機を入れてください。
```

### トラブル4: 「ロゴが複雑すぎる」
**原因**: シンプルさの指定が不十分
**解決プロンプト**:
```
ロゴをより簡潔に再生成してください：
- 最大3色まで
- 単一のシンボルのみ
- テキストなし
- 背景は透明または単色
```

---

## ✅ チェックポイント
- [ ] テキストから画像を生成できた
- [ ] 具体的な条件を指定して画像を生成できた
- [ ] 既存画像を編集できた
- [ ] ロゴ風画像とアイコンを生成できた
- [ ] 異なるスタイルで同じテーマの画像を生成し比較できた


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-2-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-2-1
- finish → 終了
