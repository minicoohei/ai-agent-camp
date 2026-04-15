---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "約25分"
prerequisites: ["start-12-3"]
level: "intermediate"
tags: ["notion", "ncli", "create", "page", "file", "database"]
---

# 🎓 Lesson 12-4: ファイル作成・ページ作成

## 📍 このセッションでやること

**Lesson 12-4: ファイル作成・ページ作成** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | ncli でNotionにページ・データベースを作成し、ファイルをアップロードする |
| 所要時間 | 約25分 |
| 使うスキル | ncli (Notion CLI) |
| 前提条件 | Lesson 12-3 完了（ファイル取得ができる状態） |

**このセッションの流れ:**
1. シンプルなページ作成
2. 本文付きページ作成（パイプ入力）
3. ファイルアップロード
4. データベース作成
5. DBにエントリ追加

セッション終了時には、ncli を使ってNotionにページ・DB・ファイルを自由に作成できるようになっています。

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

## 🚀 Step 1: シンプルなページ作成

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: シンプルなページ作成",
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

1. まず受講者に親ページを確認:
   - 「ページを作成する場所（親ページ）のURLを教えてください。特になければワークスペースのトップレベルに作成します」と案内

2. テストページを作成:
   ```bash
   ncli page create --title "ncli テストページ"
   ```

3. 親ページを指定して作成する場合:
   ```bash
   ncli page create --title "ncli テストページ" --parent <親ページURL>
   ```

4. 作成されたページの情報を確認:
   - ページID
   - ページURL
   - 作成日時

5. ブラウザでNotionを開き、ページが正しく作成されたか確認するよう案内する。

**期待される結果**: Notionに新しいページが作成され、ブラウザで確認できる。

---

## 🚀 Step 2: 本文付きページ作成（パイプ入力）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 本文付きページ作成",
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

1. `--body` オプションで本文付きページを作成:
   ```bash
   ncli page create --title "議事録テンプレート" --body "# 会議概要

## 日時
- 日付: $(date +%Y-%m-%d)

## 参加者
- （ここに記入）

## 議題
1. 議題1
2. 議題2

## 決定事項
- （ここに記入）

## 次のアクション
- [ ] タスク1
- [ ] タスク2"
   ```

2. パイプを使った入力も試す:
   ```bash
   echo "# レポート本文

これはパイプ経由で入力された本文です。

## セクション1
テスト内容を記載しています。" | ncli page create --title "パイプ入力テスト" --body -
   ```

3. ファイルの内容をそのままページに流し込む:
   ```bash
   cat README.md | ncli page create --title "READMEコピー" --body -
   ```

4. 作成したページを `ncli fetch` で確認:
   ```bash
   ncli fetch <作成されたページURL>
   ```

**補足**: `--body -` はパイプからの入力（標準入力）を本文として使うことを意味します。長文のコンテンツを作成する際に便利です。

**期待される結果**: Markdown形式の本文を持つページが作成される。

---

## 🚀 Step 3: ファイルアップロード

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ファイルアップロード",
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

1. テスト用ファイルを準備（なければ作成）:
   ```bash
   echo "これはncliアップロードテスト用のファイルです。" > output/test_upload.txt
   ```

2. ファイルをNotionにアップロード:
   ```bash
   ncli file upload output/test_upload.txt
   ```

3. 画像ファイルのアップロードも試す（あれば）:
   ```bash
   ncli file upload output/notion_auth_screenshot.png
   ```

4. アップロード結果を確認:
   - アップロード先のページ/ブロック情報
   - ファイルURL

5. Notionブラウザでアップロードされたファイルが表示されるか確認するよう案内。

**期待される結果**: ファイルがNotionにアップロードされ、ブラウザで確認できる。

---

## 🚀 Step 4: データベース作成

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: データベース作成",
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

1. タスク管理用データベースを作成:
   ```bash
   ncli db create --title "タスク管理" \
     --prop "Name:title" \
     --prop "Status:select=Open,InProgress,Done" \
     --prop "Priority:select=High,Medium,Low" \
     --prop "DueDate:date" \
     --prop "Category:multi_select=開発,デザイン,企画,ドキュメント"
   ```

2. 作成されたDBの情報を確認:
   - データベースID
   - データベースURL
   - プロパティ一覧

3. `ncli fetch` でスキーマを確認:
   ```bash
   ncli fetch <作成されたDB-URL>
   ```

4. 各プロパティが正しく作成されたか、テーブル形式で表示する:

   | プロパティ名 | 型 | 選択肢 |
   |---|---|---|
   | Name | title | - |
   | Status | select | Open, InProgress, Done |
   | Priority | select | High, Medium, Low |
   | DueDate | date | - |
   | Category | multi_select | 開発, デザイン, 企画, ドキュメント |

**期待される結果**: プロパティ付きのデータベースが作成される。

---

## 🚀 Step 5: DBにエントリ追加

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: DBにエントリ追加",
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

1. Step 4 で作成したDBにタスクを追加:
   ```bash
   ncli page create --parent <DB-URL> \
     --prop "Name=APIドキュメント作成" \
     --prop "Status=Open" \
     --prop "Priority=High" \
     --prop "Category=ドキュメント"
   ```

2. さらにタスクを追加:
   ```bash
   ncli page create --parent <DB-URL> \
     --prop "Name=ユーザー認証機能実装" \
     --prop "Status=InProgress" \
     --prop "Priority=High" \
     --prop "Category=開発"
   ```

3. 3つ目のタスクも追加:
   ```bash
   ncli page create --parent <DB-URL> \
     --prop "Name=UIモックアップ作成" \
     --prop "Status=Open" \
     --prop "Priority=Medium" \
     --prop "Category=デザイン"
   ```

4. 追加されたエントリを確認:
   ```bash
   ncli db query <DB-view-URL>
   ```

5. 結果をテーブル形式で表示し、全タスクが正しく追加されたか確認する。

**期待される結果**: 3件のタスクがDBに追加され、クエリで一覧表示できる。

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
      {"id": "trouble_1", "label": "ページ作成時に Parent not found エラー"},
      {"id": "trouble_2", "label": "--body で本文が正しく反映されない"},
      {"id": "trouble_3", "label": "ファイルアップロードが失敗する"},
      {"id": "trouble_4", "label": "DB作成時にプロパティがエラーになる"}
    ]
  }]
}
```

### トラブル1: ページ作成時に Parent not found エラー
**原因**: 親ページのURLまたはIDが間違っている
**解決方法**:
```
以下を確認してください：
1. 親ページのURLをブラウザから直接コピーする
2. ncli fetch <親ページURL> で親ページにアクセスできるか確認
3. --parent を省略してワークスペースのトップレベルに作成を試す
```

### トラブル2: --body で本文が正しく反映されない
**原因**: Markdown構文がNotionのブロックに変換されない場合がある
**解決方法**:
```
以下を試してください：
1. シンプルなテキストで試す（# 見出し、- リスト のみ）
2. パイプ入力（echo "..." | ncli page create --body -）を試す
3. 長文の場合はファイルに保存してから cat file.md | ncli page create --body -
```

### トラブル3: ファイルアップロードが失敗する
**原因**: ファイルサイズが大きすぎる、またはファイルパスが間違っている
**解決方法**:
```
以下を確認してください：
1. ファイルパスが正しいか（ls でファイルの存在を確認）
2. ファイルサイズが5MB以下か確認
3. 小さなテキストファイルで試してみる
```

### トラブル4: DB作成時にプロパティがエラーになる
**原因**: --prop の構文が間違っている
**解決方法**:
```
--prop の正しい構文：
- タイトル: --prop "Name:title"
- セレクト: --prop "Status:select=Option1,Option2"
- マルチセレクト: --prop "Tags:multi_select=Tag1,Tag2"
- 日付: --prop "Date:date"
- 数値: --prop "Count:number"
プロパティ名にスペースを含む場合はクォーテーションで囲んでください。
```

---

## ✅ チェックポイント
- [ ] `ncli page create` でページが作成できる
- [ ] `--body` オプションで本文付きページが作成できる
- [ ] `ncli file upload` でファイルがアップロードできる
- [ ] `ncli db create` でプロパティ付きDBが作成できる
- [ ] DBにエントリ（ページ）を追加できる

---

## 📋 成果物プレビュー

このレッスンで得られる成果物:

| 成果物 | 説明 |
|--------|------|
| ncli テストページ | シンプルなページ（タイトルのみ） |
| 議事録テンプレート | 本文付きページ（Markdown形式） |
| アップロードファイル | Notionにアップロードされたファイル |
| タスク管理DB | 5つのプロパティを持つデータベース |
| タスクエントリ 3件 | DBに追加されたサンプルタスク |

---

## ➡️ 次のステップ

これでページ・DB・ファイルの作成は完了です。次のレッスンでは、既存コンテンツの書き込みと更新を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-5）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-5
- finish → 終了
