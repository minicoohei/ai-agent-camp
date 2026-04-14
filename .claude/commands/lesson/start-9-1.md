---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module09-slack"
prerequisites: ["start-0-4"]
duration: "約25分"
level: "intermediate"
tags: ["slack", "search", "bookrag"]
---

# 🎓 Lesson 9-1: Slack検索

## 📍 このセッションでやること

**Lesson 9-1: Slackキーワード拡張検索** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | slack-searchでチャンネル・メッセージをキーワード拡張検索する |
| 所要時間 | 約25分 |
| 使うスキル | slack-search (BookRAG) |
| 前提条件 | Slack API設定済み（Lesson 0-4）、data/slack-sync にデータがあるとよい |
| 教材ページ | [Module 9: Slack検索](https://ai-agent.camp/ja/course/module-9) を並行参照 |

**このセッションの流れ:**
1. Slack検索の基本とインデックス確認
2. キーワード・意味検索の実行
3. 検索結果の活用

セッション終了時には、Slackの会話をキーワード拡張検索（SequenceMatcherベースの類似度検索）で検索できるようになっています。

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

## 🚀 Step 1: Slack同期データの確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Slack同期データの確認",
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
~/ai-agent-camp/data/slack-sync/data/ フォルダを確認してください。
以下の情報を教えてください：
- 同期済みのチャンネル一覧
- 総メッセージファイル数
- 最終同期日時
```

**期待される結果**: Slackデータの同期状況が表示されます。もし同期されていなければ、セットアップが必要です。

---

## 🚀 Step 2: キーワード検索の実行

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: キーワード検索の実行",
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
Slackで「プロジェクト進捗」というキーワードを含むメッセージを検索してください。
直近1週間以内のものを、以下の形式で表示してください：
- チャンネル名
- 日時
- 発言者
- メッセージ内容（100文字まで）
```

**期待される結果**: 該当するメッセージの一覧が表示されます。

---

## 🚀 Step 3: チャンネル指定検索

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: チャンネル指定検索",
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
Slackの特定チャンネルを検索してください：
- チャンネル: #general（または存在するチャンネル名）
- キーワード: ミーティング OR 会議
- 期間: 直近2週間

見つかったメッセージを時系列で整理してください。
```

**期待される結果**: 指定チャンネルからの検索結果が表示されます。

---

## 🚀 Step 4: ユーザー別検索

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: ユーザー別検索",
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
Slackで特定ユーザーの発言を検索してください：
- 対象ユーザー: @YourName（自分のユーザー名に置き換え）
- 検索キーワード: レビュー OR 確認
- 期間: 直近1ヶ月

結果を重要度順にソートしてください。
```

**期待される結果**: 特定ユーザーの発言が抽出されます。

---

## 🚀 Step 5: キーワード拡張検索の活用

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: キーワード拡張検索の活用",
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
Slackで「顧客からのフィードバック」に関連するメッセージをキーワード拡張検索してください。

以下の類義語も含めて検索してください：
- フィードバック、意見、要望、苦情、感想
- お客様、クライアント、顧客

検索結果をカテゴリ別（ポジティブ/ネガティブ/ニュートラル）に分類してください。
```

**期待される結果**: 意味的に関連するメッセージが分類されて表示されます。

---

## 🚀 Step 6: 検索結果のレポート化

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 6: 検索結果のレポート化",
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
先ほどの検索結果をMarkdownレポートにまとめてください。

以下の形式でお願いします：
# Slack検索レポート
生成日時: (現在日時)

## 検索条件
- キーワード: ...
- 期間: ...

## 検索結果サマリー
- 総件数: ...
- チャンネル別内訳: ...

## 詳細
(メッセージ一覧)

出力: ~/ai-agent-camp/output/slack_search_report.md
```

**期待される結果**: 検索結果がMarkdown形式でレポート化されます。

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
      {"id": "trouble_1", "label": "同期データが見つからない"},
      {"id": "trouble_2", "label": "検索結果が少ない"},
      {"id": "trouble_3", "label": "日本語検索がうまくいかない"},
      {"id": "trouble_4", "label": "特定ユーザーのIDがわからない"}
    ]
  }]
}
```


### トラブル1: 「同期データが見つからない」
**原因**: slack-syncのセットアップが未完了
**解決プロンプト**:
```
slack-syncのセットアップ状況を確認してください。
~/ai-agent-camp/data/slack-sync/ フォルダの構造と必要なファイルを教えてください。
```

### トラブル2: 「検索結果が少ない」
**原因**: 検索条件が厳しすぎる
**解決プロンプト**:
```
検索結果を増やすために、以下を試してください：
- 検索期間を1ヶ月に拡大
- キーワードをより一般的なものに変更
- チャンネル指定を外す
```

### トラブル3: 「日本語検索がうまくいかない」
**原因**: エンコーディングまたはトークン化の問題
**解決プロンプト**:
```
日本語キーワードで検索がうまくいきません。
以下を試してください：
- ひらがな/カタカナ両方で検索
- キーワードを短く分割
- 部分一致検索を使用
```

### トラブル4: 「特定ユーザーのIDがわからない」
**原因**: Slack User IDの特定が必要
**解決プロンプト**:
```
Slack User IDを確認する方法を教えてください。
users.jsonファイルから自分のUser IDを検索してください。
```

---

## ✅ チェックポイント
- [ ] Slack同期データの場所を確認できた
- [ ] キーワード検索が実行できた
- [ ] チャンネル指定検索ができた
- [ ] ユーザー別検索ができた
- [ ] キーワード拡張検索を活用できた
- [ ] 検索結果をレポート化できた


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-9-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-9-2
- finish → 終了
