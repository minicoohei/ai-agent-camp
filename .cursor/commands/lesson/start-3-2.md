---
description: "When the user says /start-3-2 — Module 3 Lesson 3-2: エラー診断の応用"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "約25分"
level: "intermediate"
tags: ["screenshot", "error-diagnosis", "analysis"]
---

# 🎓 Lesson 3-2: エラー診断の応用

## 📍 このセッションでやること

**Lesson 3-2: エラー診断の応用** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 複雑なエラー画面を分析し、優先度を判定して解決策を提案する |
| 所要時間 | 約25分 |
| 使うスキル | screenshot-analyzer（応用） |
| 前提条件 | Lesson 3-1 完了、Gemini APIキー設定済み |
| 教材ページ | [Module 3: スクショ分析](https://ai-agent.camp/ja/course/module-3) を並行参照 |

**このセッションの流れ:**
1. APIレスポンスエラーの分析
2. 複合エラーの優先度判定と解決策
3. 実務に近いケースへの応用

セッション終了時には、本番に近いエラー診断ができるようになっています。

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

## 🚀 Step 1: APIレスポンスエラーの分析

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: APIレスポンスエラーの分析",
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
screenshot-analyzerスキルを使って、APIレスポンスエラーを分析してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/api-error-response.png
出力: output/screenshots/api-error-analysis.html

分析内容:
- エラーコードの意味
- 根本原因の推測
- 優先度の判定（高/中/低）
- 具体的な解決手順
```

**期待される結果**: エラーの詳細分析がHTML形式で出力され、優先度と解決手順が明記されます。

---

## 🚀 Step 2: 複数エラーの優先順位付け

複数のエラーが同時に発生している画面を分析します：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 複数エラーの優先順位付け",
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
複数のエラーが表示されたスクリーンショットを分析してください。

入力: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/multiple-errors.png
出力: output/screenshots/error-priority.png

エラーを重要度で分類:
- 【高】赤枠: 即座に対応が必要
- 【中】黄枠: 早めに対応が望ましい
- 【低】青枠: 時間があれば対応

各エラーに番号を振り、対応順序を明確にしてください。
```

**期待される結果**: 各エラーが色分けされ、対応優先度が一目でわかる画像が生成されます。

---

## 🚀 Step 3: よくあるエラーパターンの診断

よくあるHTTPエラーの診断を練習しましょう：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: よくあるエラーパターンの診断",
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
以下のエラーパターンについて、スクリーンショットがなくても
診断と解決策を提案してください：

1. 502 Bad Gateway
2. 503 Service Unavailable
3. 401 Unauthorized
4. CORS エラー

それぞれの原因と解決策をテーブル形式でまとめてください。
```

**期待される結果**: 各エラーの原因と解決策が整理されたテーブルが表示されます。

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
      {"id": "trouble_1", "label": "分析結果が抽象的すぎる"},
      {"id": "trouble_2", "label": "複数エラーの関連性がわからない"},
      {"id": "trouble_3", "label": "優先度の判定基準がわからない"},
      {"id": "trouble_4", "label": "HTML出力が文字化けする"}
    ]
  }]
}
```


### トラブル1: 「分析結果が抽象的すぎる」
**原因**: スクリーンショットの情報が不足している
**解決プロンプト**:
```
より正確なエラー分析のために、追加で必要な情報を教えてください。
スクリーンショットに含めるべき要素（コンソールログ、ネットワークタブなど）も提案してください。
```

### トラブル2: 「複数エラーの関連性がわからない」
**原因**: エラーの連鎖関係が複雑
**解決プロンプト**:
```
このエラー画面で、どのエラーが根本原因で、
どのエラーが派生的なものか分析してください。
エラーの因果関係を図解してください。
```

### トラブル3: 「優先度の判定基準がわからない」
**原因**: 判定基準が明確でない
**解決プロンプト**:
```
エラーの優先度を判定する基準を教えてください。
以下の観点で説明してください：
- ユーザー影響
- ビジネス影響
- 技術的深刻度
- 対応の緊急性
```

### トラブル4: 「HTML出力が文字化けする」
**原因**: 文字エンコーディングの問題
**解決プロンプト**:
```
生成されたHTMLファイルが文字化けしています。
UTF-8エンコーディングで再生成してください。
```

---

## ✅ チェックポイント
- [ ] エラースクリーンショットを自動で分析できる
- [ ] 根本原因と派生的な問題を区別できる
- [ ] 優先度に基づいて対応順序を決められる
- [ ] HTML形式で分析レポートを出力できる
- [ ] 複数エラーを色分けして可視化できる


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-3-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-3-3
- finish → 終了
