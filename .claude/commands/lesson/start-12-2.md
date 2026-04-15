---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "約25分"
prerequisites: ["start-12-1"]
level: "beginner"
tags: ["notion", "ncli", "database", "query"]
---

# 🎓 Lesson 12-2: データベース取得・クエリ

## 📍 このセッションでやること

**Lesson 12-2: データベース取得・クエリ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | ncli でNotionデータベースを検索・取得し、クエリでデータを抽出・分析する |
| 所要時間 | 約25分 |
| 使うスキル | ncli (Notion CLI) |
| 前提条件 | Lesson 12-1 完了（ncli認証済み） |

**このセッションの流れ:**
1. ワークスペース内のDB検索
2. DB スキーマの確認
3. クエリの実行
4. JSON出力とAI分析
5. フィルタ・ソート条件の変更

セッション終了時には、Notionデータベースの構造を理解し、条件付きクエリを実行できるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

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
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → `ncli whoami` を実行して認証状態を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: ワークスペース内のDB検索

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ワークスペース内のDB検索",
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

**AIが実行すること:**

1. ワークスペース全体を検索してデータベースを探す:
   ```bash
   ncli search "タスク"
   ```

2. 検索結果から、データベースとページを区別して一覧表示する。

3. 複数のキーワードで検索して、ワークスペース内のDBを把握する:
   ```bash
   ncli search "プロジェクト"
   ncli search "管理"
   ```

4. 検索結果をテーブル形式で整理して受講者に共有する:
   - タイトル
   - 種類（データベース / ページ）
   - 最終更新日

**補足**: データベースが見つからない場合は、Lesson 12-4 で新しいDBを作成できます。既存のDBがあれば、それを使って進めましょう。

**期待される結果**: ワークスペース内のデータベースが一覧表示される。

---

## 🚀 Step 2: DBスキーマ確認（ncli fetch）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: DBスキーマ確認",
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

**AIが実行すること:**

1. 受講者にデータベースのURLまたはIDを教えてもらう:
   - Step 1 の検索結果から選んでもらう

2. データベースのスキーマ（プロパティ構造）を取得:
   ```bash
   ncli fetch <db-url>
   ```

3. 取得結果から以下を整理して説明:
   - データベースタイトル
   - 各プロパティの名前と型（title, select, date, number など）
   - Select/Multi-select の選択肢一覧
   - リレーション・ロールアップの参照先

4. スキーマ情報をわかりやすいテーブル形式で出力する:

   | プロパティ名 | 型 | 設定 |
   |---|---|---|
   | タスク名 | title | - |
   | ステータス | select | 未着手, 進行中, 完了 |
   | 期限 | date | - |

**期待される結果**: データベースの全プロパティとその型が一覧表示される。

---

## 🚀 Step 3: クエリ実行（ncli db query）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: クエリ実行",
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

**AIが実行すること:**

1. データベースビューのURLを使ってクエリを実行:
   ```bash
   ncli db query <view-url>
   ```

2. 全レコードの一覧を取得し、テーブル形式で表示する。

3. 結果の各行について主要プロパティの値を整理する。

4. レコード数を確認:
   - 「全XX件のレコードが取得されました」と報告

**補足**: `<view-url>` はNotionのデータベースビューのURLです。ブラウザでデータベースを開いた時のURLをそのまま使えます。

**期待される結果**: データベースの全レコードが取得・表示される。

---

## 🚀 Step 4: JSON出力とAI分析

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: JSON出力とAI分析",
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

**AIが実行すること:**

1. JSON形式でデータを取得:
   ```bash
   ncli db query <view-url> --json
   ```

2. 取得したJSONデータをAIで分析:
   - レコード数の集計
   - プロパティ値の分布（ステータス別の件数など）
   - 日付の範囲（最古〜最新）

3. 分析結果をレポート形式で出力:
   ```
   📊 データベース分析レポート
   ========================
   - 全レコード数: XX件
   - ステータス別: 未着手 X件 / 進行中 X件 / 完了 X件
   - 直近1週間の更新: X件
   ```

4. 結果を `output/notion_db_analysis.md` に保存する。

**期待される結果**: JSON形式のデータが取得でき、AIが構造化された分析レポートを生成する。

---

## 🚀 Step 5: フィルタ・ソート条件の変更

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: フィルタ・ソート条件の変更",
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

**AIが実行すること:**

1. Notionでデータベースのビューを変更する方法を案内:
   - ブラウザでデータベースを開く
   - フィルタ条件を設定（例: ステータスが「進行中」のみ）
   - ソート条件を設定（例: 期限の昇順）
   - そのビューURLをコピー

2. フィルタ済みビューのURLでクエリを実行:
   ```bash
   ncli db query <filtered-view-url>
   ```

3. REST API を使ったフィルタリングも試す:
   ```bash
   ncli rest POST /v1/databases/<db-id>/query '{"filter":{"property":"ステータス","select":{"equals":"進行中"}}}'
   ```

4. 結果を比較して、ビューURLとREST APIの使い分けを解説する:
   - ビューURL: Notion側で設定したフィルタをそのまま使える（簡単）
   - REST API: プログラマティックに条件を指定できる（柔軟）

**期待される結果**: フィルタ・ソート付きのクエリが実行でき、条件に合ったデータのみが表示される。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "Database not found エラー"},
      {"id": "trouble_2", "label": "クエリ結果が空になる"},
      {"id": "trouble_3", "label": "JSON出力が文字化けする"},
      {"id": "trouble_4", "label": "REST APIのフィルタ構文エラー"}
    ]
  }]
}
```

### トラブル1: Database not found エラー
**原因**: データベースIDまたはURLが間違っている、アクセス権限がない
**解決方法**:
```text
以下を確認してください：
1. URLをブラウザから直接コピーしているか
2. ncli search でそのDBが検索結果に出るか
3. DBが共有されているワークスペースに ncli login しているか
```

### トラブル2: クエリ結果が空になる
**原因**: フィルタ条件に一致するレコードがない、またはビューの設定
**解決方法**:
```text
以下を確認してください：
1. フィルタなしのビューURLで試す
2. Notionブラウザで同じビューを開き、データが見えるか確認
3. ncli fetch <db-url> でDB自体にアクセスできるか確認
```

### トラブル3: JSON出力が文字化けする
**原因**: ターミナルの文字コード設定
**解決方法**:
```text
以下を試してください：
1. ターミナルのエンコーディングをUTF-8に設定
2. ncli db query <view-url> --json | python3 -m json.tool で整形
3. ncli db query <view-url> --json > output/result.json でファイル保存
```

### トラブル4: REST APIのフィルタ構文エラー
**原因**: JSONの構文エラー、またはプロパティ名・型の不一致
**解決方法**:
```text
以下を確認してください：
1. JSONのクォーテーションはシングルクォートで囲む（シェル用）
2. プロパティ名は ncli fetch で確認した正確な名前を使う
3. フィルタの型はプロパティの型に合わせる（select → equals、date → on_or_after など）
```

---

## ✅ チェックポイント
- [ ] `ncli search` でワークスペース内のDBが検索できる
- [ ] `ncli fetch` でDBのスキーマ（プロパティ構造）が確認できる
- [ ] `ncli db query` でレコード一覧が取得できる
- [ ] `--json` オプションでJSON形式のデータが取得できる
- [ ] フィルタ・ソート条件を変更してクエリを実行できる

---

## 📋 成果物プレビュー

このレッスンで得られる成果物:

| 成果物 | 説明 |
|--------|------|
| DB スキーマ一覧 | プロパティ名・型・選択肢をテーブル形式で整理 |
| クエリ結果 | 全レコード・フィルタ済みレコードの一覧 |
| `output/notion_db_analysis.md` | AIによるデータベース分析レポート |

---

## ➡️ 次のステップ

これでデータベースの取得とクエリは完了です。次のレッスンでは、ファイルの取得を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-3
- finish → 終了
