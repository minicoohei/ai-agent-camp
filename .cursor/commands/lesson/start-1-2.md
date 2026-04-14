---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "約30分"
level: "beginner"
tags: ["banner", "image", "sns", "multi-platform"]
---

# 🎓 Lesson 1-2: 応用バナー（Instagram, Facebook）

## 📍 このセッションでやること

**Lesson 1-2: 応用バナー（Instagram, Facebook）** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | X・Instagram・Facebook向けに最適化されたバナーを一括生成する |
| 所要時間 | 約30分 |
| 使うスキル | banner-creator（複数プラットフォーム対応） |
| 前提条件 | Lesson 1-1 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 1: バナー・画像生成](https://ai-agent.camp/ja/course/module-1) を並行参照 |

**このセッションの流れ:**
1. 各プラットフォームのサイズを確認する
2. 3プラットフォーム向けバナーを一括生成する
3. デザインの一貫性を確認する
4. 別のキャンペーンで練習する

セッション終了時には、複数SNS向けのバナーが outputs に保存されています。

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

## 🚀 Step 1: 各プラットフォームのサイズを確認する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: 各プラットフォームのサイズを確認する",
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
X、Instagram、Facebookの投稿用バナーの推奨サイズを表形式で教えてください。
アスペクト比と用途も含めてください。
```

**期待される結果**: 以下のような表が表示されます：
| プラットフォーム | サイズ | アスペクト比 |
|---------------|-------|------------|
| X | 1200x675px | 16:9 |
| Instagram | 1080x1080px | 1:1 |
| Facebook | 1200x630px | 1.91:1 |

---

## 🚀 Step 2: 3プラットフォーム向けバナーを一括生成する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 3プラットフォーム向けバナーを一括生成する",
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
「夏のセールイベント」というトピックで、以下の3つのプラットフォーム向けバナーを作成してください：

1. X用（1200x675px）
2. Instagram用（1080x1080px）
3. Facebook用（1200x630px）

それぞれ banner-1-2-x.png、banner-1-2-ig.png、banner-1-2-fb.png として保存してください。
```

**期待される結果**: 3つの異なるサイズのバナーが生成され、それぞれのプラットフォームに最適化されます。

---

## 🚀 Step 3: デザインの一貫性を確認する

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: デザインの一貫性を確認する",
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
先ほど作成した3つのバナーを確認してください。
デザインの一貫性（色、フォント、メッセージ）が保たれているか、
改善点があれば指摘してください。
```

**期待される結果**: 3つのバナー間でブランドの一貫性が評価され、必要に応じて修正提案が得られます。

---

## 🚀 Step 4: 別のキャンペーンで練習する

以下のプロンプトで、別のキャンペーン用バナーセットを作成してみましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 別のキャンペーンで練習する",
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
「新製品発売記念 - 先着100名様限定特典」というトピックで、
X、Instagram、Facebook向けのバナーセットを作成してください。
スタイル: 高級感、プレミアム感
カラー: ゴールドとブラックを基調に
```

**期待される結果**: 統一されたデザインテーマで、3プラットフォーム分のバナーが生成されます。

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
      {"id": "trouble_1", "label": "プラットフォーム名が認識されない"},
      {"id": "trouble_2", "label": "一括生成でエラーが出る"},
      {"id": "trouble_3", "label": "デザインの統一感がない"},
      {"id": "trouble_4", "label": "Instagramの正方形レイアウトが崩れる"}
    ]
  }]
}
```


### トラブル1: 「プラットフォーム名が認識されない」
**原因**: 正しいプラットフォーム名を指定していない
**解決プロンプト**:
```
banner-creatorで利用可能なプラットフォーム名の一覧を教えてください。
--help オプションで確認してください。
```

### トラブル2: 「一括生成でエラーが出る」
**原因**: 途中でAPIエラーやファイル書き込みエラーが発生
**解決プロンプト**:
```
バナー生成を1つずつ実行して、どのプラットフォームでエラーが出るか特定してください。
エラーメッセージを表示してください。
```

### トラブル3: 「デザインの統一感がない」
**原因**: 各プラットフォームで別々にプロンプトを解釈している
**解決プロンプト**:
```
3つのバナーすべてで以下を統一してください：
- メインカラー: #FF6B00（オレンジ）
- フォント: モダンなサンセリフ
- キャッチコピー: 同一のテキスト
```

### トラブル4: 「Instagramの正方形レイアウトが崩れる」
**原因**: 横長デザインを無理に正方形に収めている
**解決プロンプト**:
```
Instagram用バナーは正方形（1:1）に最適化されたレイアウトで再生成してください。
テキストは中央配置、余白を十分に取ってください。
```

---

## ✅ チェックポイント
- [ ] 各プラットフォームの推奨サイズを理解した
- [ ] X、Instagram、Facebookの3種類のバナーを生成できた
- [ ] デザインの一貫性を確認できた
- [ ] 練習課題（別キャンペーンのバナーセット）を完了した


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-1-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-1-3
- finish → 終了
