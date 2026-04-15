---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "約25分"
prerequisites: ["start-12-2"]
level: "intermediate"
tags: ["notion", "ncli", "file", "fetch"]
---

# 🎓 Lesson 12-3: ファイル取得

## 📍 このセッションでやること

**Lesson 12-3: ファイル取得** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Notionページ内のブロック構造を理解し、ファイル・画像ブロックを特定してローカルにダウンロードする |
| 所要時間 | 約25分 |
| 使うスキル | ncli (Notion CLI) |
| 前提条件 | Lesson 12-2 完了（DBクエリが実行できる状態） |

**このセッションの流れ:**
1. ページ内のブロック構造を確認
2. ファイルブロック・画像ブロックの特定
3. ファイル情報の取得
4. ローカルへのダウンロード
5. 取得結果の整理

セッション終了時には、Notionページ内の添付ファイルや画像を特定し、ローカルにダウンロードできるようになっています。

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

## 🚀 Step 1: ページ内のブロック構造を確認

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ブロック構造の確認",
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

1. 受講者にファイルが含まれるNotionページのURLを教えてもらう:
   - 「画像やファイルが添付されているNotionページのURLを教えてください」と案内
   - ファイルがない場合は、テスト用にNotionで画像を1枚貼り付けてもらう

2. ページの全ブロックを取得:
   ```bash
   ncli fetch <ページURL>
   ```

3. ブロック構造を解説:
   - Notionのページは「ブロック」の集まりで構成されている
   - 各ブロックには型がある（paragraph, heading_1, image, file, code など）
   - ブロックは入れ子にできる（子ブロックを持てる）

4. 取得結果のブロック一覧を整理して表示:

   | # | ブロック型 | 内容プレビュー |
   |---|-----------|---------------|
   | 1 | heading_1 | セクションタイトル |
   | 2 | paragraph | テキスト内容... |
   | 3 | image | 画像ファイル |
   | 4 | file | 添付ファイル |

**期待される結果**: ページ内のブロック一覧が型ごとに整理されて表示される。

---

## 🚀 Step 2: ファイルブロック・画像ブロックの特定

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ファイルブロックの特定",
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

1. JSON形式で詳細なブロックデータを取得:
   ```bash
   ncli fetch <ページURL> --json
   ```

2. 取得結果からファイル関連ブロックをフィルタリング:
   - `image` 型ブロック: 埋め込み画像
   - `file` 型ブロック: 添付ファイル
   - `pdf` 型ブロック: PDFファイル
   - `video` 型ブロック: 動画ファイル

3. 各ファイルブロックの詳細を抽出:
   - ブロックID
   - ファイルの種類（external / file）
   - URL
   - キャプション（あれば）

4. ファイル一覧を整理して表示:
   ```
   📎 ファイルブロック一覧
   ========================
   1. [image] スクリーンショット.png — Notion hosted
   2. [file] レポート.pdf — External URL
   3. [image] ロゴ.svg — External URL
   ```

**期待される結果**: ページ内のファイル・画像ブロックが特定され、一覧表示される。

---

## 🚀 Step 3: ファイル情報取得（URL・タイプ・サイズ）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ファイル情報取得",
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

1. 特定したファイルブロックのURLを取得:
   - Notion hosted ファイル: 一時URL（有効期限あり）
   - External ファイル: 外部URL（永続）

2. ファイルの詳細情報を確認:
   ```bash
   curl -sI "<ファイルURL>" | head -20
   ```

3. 取得できる情報を整理:
   - Content-Type（ファイル形式）
   - Content-Length（ファイルサイズ）
   - 有効期限（Notion hosted の場合）

4. 情報をテーブル形式で出力:

   | ファイル名 | 形式 | サイズ | ホスト | 備考 |
   |-----------|------|--------|--------|------|
   | screenshot.png | image/png | 245KB | Notion | 一時URL（1時間有効） |
   | report.pdf | application/pdf | 1.2MB | External | 永続URL |

**補足**: Notion hosted ファイルのURLには有効期限があります。ダウンロードする場合は取得後すぐに実行してください。

**期待される結果**: 各ファイルの詳細情報（形式・サイズ・ホスト種別）が表示される。

---

## 🚀 Step 4: ローカルへのダウンロード

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: ファイルダウンロード",
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

1. 出力ディレクトリを作成:
   ```bash
   mkdir -p output/notion_files
   ```

2. ファイルURLを使ってダウンロード:
   ```bash
   curl -sL "<ファイルURL>" -o output/notion_files/<ファイル名>
   ```

3. 複数ファイルがある場合はまとめてダウンロード:
   ```bash
   # 各ファイルを順にダウンロード
   curl -sL "<URL1>" -o output/notion_files/file1.png
   curl -sL "<URL2>" -o output/notion_files/file2.pdf
   ```

4. ダウンロード結果を確認:
   ```bash
   ls -la output/notion_files/
   ```

**補足**: Notion hosted ファイルの一時URLは通常1時間程度で失効します。失効した場合は `ncli fetch` を再実行してURLを再取得してください。

**期待される結果**: ファイルが `output/notion_files/` ディレクトリにダウンロードされる。

---

## 🚀 Step 5: 取得結果の整理（Markdownで出力）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 取得結果の整理",
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

1. ダウンロードしたファイルの一覧をMarkdown形式で整理:
   ```markdown
   # Notionファイル取得結果

   ## ページ情報
   - ページ名: ○○○
   - 取得日時: YYYY-MM-DD HH:MM
   - ファイル数: X件

   ## ファイル一覧
   | # | ファイル名 | 形式 | サイズ | ローカルパス |
   |---|-----------|------|--------|-------------|
   | 1 | screenshot.png | PNG | 245KB | output/notion_files/screenshot.png |
   | 2 | report.pdf | PDF | 1.2MB | output/notion_files/report.pdf |
   ```

2. この一覧を `output/notion_files_inventory.md` に保存する。

3. 受講者に結果を共有し、ファイルが正しくダウンロードされたか確認する。

**期待される結果**: ファイル一覧がMarkdown形式で `output/notion_files_inventory.md` に保存される。

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
      {"id": "trouble_1", "label": "ファイルURLが取得できない"},
      {"id": "trouble_2", "label": "ダウンロードしたファイルが壊れている"},
      {"id": "trouble_3", "label": "一時URLが失効した"},
      {"id": "trouble_4", "label": "ページにファイルが見つからない"}
    ]
  }]
}
```

### トラブル1: ファイルURLが取得できない
**原因**: ブロックのJSON構造が想定と異なる
**解決方法**:
```
以下を確認してください：
1. ncli fetch <ページURL> --json でJSON全体を確認
2. ファイルブロックの型を確認（image / file / pdf / video）
3. file.url または external.url のパスを正確に辿る
```

### トラブル2: ダウンロードしたファイルが壊れている
**原因**: URLリダイレクトが正しく処理されていない
**解決方法**:
```
以下を試してください：
1. curl に -L オプション（リダイレクト追従）を付ける
2. curl -sL "<URL>" -o file.png のように実行
3. ファイルサイズが0でないか確認（ls -la で確認）
```

### トラブル3: 一時URLが失効した
**原因**: Notion hosted ファイルのURLは約1時間で失効する
**解決方法**:
```
以下を実行してください：
1. ncli fetch <ページURL> --json を再実行
2. 新しいURLを取得する
3. すぐにダウンロードを実行する
```

### トラブル4: ページにファイルが見つからない
**原因**: ページにファイルブロックが含まれていない
**解決方法**:
```
以下を確認してください：
1. Notionブラウザでページを開き、ファイルが添付されているか確認
2. ファイルが子ページ内にある場合は、そのページのURLを使う
3. テスト用に画像を1枚Notionにドラッグ&ドロップしてから再試行
```

---

## ✅ チェックポイント
- [ ] `ncli fetch` でページのブロック構造が確認できる
- [ ] ファイル・画像ブロックを特定できる
- [ ] ファイルのURL・タイプ・サイズ情報が取得できる
- [ ] `curl` でファイルをローカルにダウンロードできる
- [ ] 取得結果がMarkdown形式で整理されている

---

## 📋 成果物プレビュー

このレッスンで得られる成果物:

| 成果物 | 説明 |
|--------|------|
| `output/notion_files/` | ダウンロードしたファイル群 |
| `output/notion_files_inventory.md` | ファイル一覧（Markdown形式） |
| ブロック構造の理解 | ページ内のブロック型と階層構造の知識 |

---

## ➡️ 次のステップ

これでファイル取得は完了です。次のレッスンでは、ページやDBの作成を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-4
- finish → 終了
