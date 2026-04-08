---
description: "When the user says /start-8-1 — Module 8 Lesson 8-1: BigQuery接続と認証設定"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
duration: "約25分"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["data", "bigquery", "gcp", "authentication"]
---

# 🎓 Lesson 8-1: BigQuery接続と認証設定

## 📍 このセッションでやること

**Lesson 8-1: BigQuery接続と認証設定** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GCP認証を設定し、BigQueryに接続して公開データセットにアクセスする |
| 所要時間 | 約25分 |
| 使うスキル | bigquery-auth, gcloud CLI |
| 前提条件 | Google Cloud プロジェクトへのアクセス権限、Python 3.8以上、gcloud CLI インストール済み |
| 教材ページ | [Module 8: データ分析](https://ai-agent.camp/ja/course/module-8) を並行参照 |

**このセッションの流れ:**
1. GCP認証の確認
2. 認証の実行（未設定の場合）
3. BigQuery接続テスト
4. 公開データセットへのアクセス

セッション終了時には、BigQueryでクエリを実行できる状態になっています。

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

## 🚀 Step 1: GCP認証の確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: GCP認証の確認",
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
GCP（Google Cloud Platform）の認証状態を確認してください。

確認項目:
1. gcloud CLI がインストールされているか
2. 現在の認証アカウント
3. 現在のプロジェクトID
4. Application Default Credentials (ADC) の状態

問題があれば、解決方法も教えてください。
```

**期待される結果**: 認証状態が表示され、必要に応じて設定手順が案内されます。

---

## 🚀 Step 2: 認証の実行（未設定の場合）

認証が未設定の場合は、以下のプロンプトで設定を行います：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 認証の実行（未設定の場合）",
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
BigQueryにアクセスするための認証を設定してください。

実行する認証:
1. gcloud auth login（メイン認証）
2. gcloud auth application-default login（Python SDK用）

それぞれのコマンドの実行と、
成功したかどうかの確認をお願いします。
```

**期待される結果**: ブラウザが開き、Googleアカウントでの認証が完了します。

---

## 🚀 Step 3: BigQuery接続テスト

認証完了後、BigQueryへの接続をテストします：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: BigQuery接続テスト",
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
BigQueryへの接続テストを実行してください。

テスト内容:
1. BigQuery Pythonクライアントの初期化
2. 現在のプロジェクトIDの取得
3. シンプルなテストクエリの実行

テストクエリ:
SELECT CURRENT_TIMESTAMP() as current_time,
       @@project_id as project_id,
       "接続成功" as status
```

**期待される結果**: 接続成功のメッセージとプロジェクトIDが表示されます。

---

## 🚀 Step 4: 公開データセットへのアクセス

Google公開データセット（GA4 Eコマースサンプル）にアクセスします：

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 公開データセットへのアクセス",
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
BigQuery公開データセット（GA4 Eコマースサンプル）に
アクセスできるか確認してください。

テストクエリ:
SELECT
    COUNT(*) as event_count,
    COUNT(DISTINCT user_pseudo_id) as unique_users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101`

結果を表示してください。
```

**期待される結果**: GA4サンプルデータセットからイベント数とユーザー数が表示されます。

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
      {"id": "trouble_1", "label": "gcloud: command not found"},
      {"id": "trouble_2", "label": "File xxx was not found"},
      {"id": "trouble_3", "label": "403 Forbidden / Permission denied"},
      {"id": "trouble_4", "label": "Reauthentication needed"}
    ]
  }]
}
```


### トラブル1: 「gcloud: command not found」
**原因**: gcloud CLIがインストールされていない
**解決プロンプト**:
```
gcloud CLI（Google Cloud SDK）のインストール方法を教えてください。
macOSでの手順をお願いします。
```

### トラブル2: 「File xxx was not found」
**原因**: 環境変数 GOOGLE_APPLICATION_CREDENTIALS が無効なパスを指している
**解決プロンプト**:
```
GOOGLE_APPLICATION_CREDENTIALS 環境変数を確認してください。
無効な値が設定されている場合は、クリアする方法を教えてください。
```

### トラブル3: 「403 Forbidden / Permission denied」
**原因**: BigQueryの権限がない
**解決プロンプト**:
```
BigQueryにアクセスするために必要なIAM権限を教えてください。
また、現在のアカウントに設定されている権限を確認する方法も教えてください。
```

### トラブル4: 「Reauthentication needed」
**原因**: 認証トークンの期限切れ
**解決プロンプト**:
```
BigQueryの認証トークンが期限切れになっています。
再認証を実行してください。
```

### ADC認証のリセット
`GOOGLE_APPLICATION_CREDENTIALS` が古いパスを指している場合:
```bash
unset GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```

---

## ✅ チェックポイント
- [ ] gcloud CLI がインストールされている
- [ ] gcloud auth login で認証が完了した
- [ ] gcloud auth application-default login で ADC が設定された
- [ ] BigQueryクライアントが初期化できた
- [ ] テストクエリが実行できた
- [ ] 公開データセット（GA4 Sample）にアクセスできた

---

## 📚 補足: マルチプロジェクト環境

複数のGCPプロジェクトを使い分ける場合：

```
複数のGCPプロジェクトを管理するための
gcloud設定プロファイルの作成方法を教えてください。

例:
- project-a: 開発環境
- project-b: 本番環境

プロファイルの切り替え方法も教えてください。
```


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-8-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-8-2
- finish → 終了
