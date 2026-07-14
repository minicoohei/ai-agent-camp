---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約25分"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "drive"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-5: Google Drive操作

## 📍 このセッションでやること

**Lesson 4-5: Google Drive操作** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでDriveのファイル一覧・ダウンロード・アップロードを行う |
| 所要時間 | 約25分 |
| 使うスキル | gogcli drive |
| 前提条件 | gogcli認証セットアップ済み（start-4-1完了） |

**このセッションの流れ:**
1. Drive内のファイルを一覧表示・検索する
2. ファイルをダウンロードする
3. ファイルをアップロードする

セッション終了時には、gogcliを使ってGoogle Driveのファイル操作ができるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

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
(check_prereq → `gog auth list` で認証状態を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Drive内のファイルを一覧表示・検索する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ファイル一覧・検索",
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

Google Drive内のファイルを一覧表示してみましょう:

```bash
# ルートフォルダのファイル一覧（最新10件）
gog drive ls --account your-email@gmail.com --max 10

# ファイル名で検索
gog drive ls --account your-email@gmail.com --query "name contains '議事録'"

# MIMEタイプで絞り込み（スプレッドシートのみ）
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.spreadsheet'"

# Google Docs のみ
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.document'"

# PDF ファイルのみ
gog drive ls --account your-email@gmail.com --query "mimeType='application/pdf'"

# 特定フォルダ内のファイル一覧
gog drive ls --account your-email@gmail.com --query "'<フォルダID>' in parents"

# 最近変更されたファイル
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-01'" --max 10
```

**主要なMIMEタイプ:**

| Google形式 | MIMEタイプ |
|-----------|-----------|
| Google Docs | `application/vnd.google-apps.document` |
| Google Sheets | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| フォルダ | `application/vnd.google-apps.folder` |

**期待される結果**: ファイルID、ファイル名、MIMEタイプ、最終更新日が一覧表示されます。

---

## 🚀 Step 2: ファイルをダウンロードする

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ファイルのダウンロード",
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

Step 1で取得したファイルIDを使ってダウンロードします:

```bash
# 通常のファイル（PDF, 画像等）をダウンロード
gog drive download <ファイルID> --account your-email@gmail.com --out ./downloads/filename.pdf

# Google Docs → PDF に変換してダウンロード
gog drive download <ファイルID> --account your-email@gmail.com --format pdf --out ./downloads/document.pdf

# Google Sheets → CSV に変換してダウンロード
gog drive download <ファイルID> --account your-email@gmail.com --format csv --out ./downloads/sheet.csv

# Google Sheets → Excel に変換してダウンロード
gog drive download <ファイルID> --account your-email@gmail.com --format xlsx --out ./downloads/sheet.xlsx

# Google Slides → PPTX に変換してダウンロード
gog drive download <ファイルID> --account your-email@gmail.com --format pptx --out ./downloads/slides.pptx
```

**エクスポート形式の一覧:**

| Google形式 | エクスポート可能な形式 |
|-----------|---------------------|
| Google Docs | PDF, DOCX, TXT, HTML, EPUB |
| Google Sheets | CSV, XLSX, PDF, TSV |
| Google Slides | PPTX, PDF, TXT |

**期待される結果**: 指定した出力先にファイルがダウンロードされます。

> **💡 ヒント**: Google形式のファイル（Docs/Sheets/Slides）は直接ダウンロードできないため、`--format` で変換形式を指定する必要があります。

---

## 🚀 Step 3: ファイルをアップロードする

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: ファイルのアップロード",
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

ローカルのファイルをGoogle Driveにアップロードします:

```bash
# テスト用ファイルを作成
echo "これはgogcliアップロードテストです。" > /tmp/test-upload.txt

# ファイルをアップロード（ルートフォルダへ）
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com

# 特定のフォルダにアップロード
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com --parent <フォルダID>

# 複数ファイルのアップロード（AIに依頼）
# 以下のプロンプトをCursorに入力:
```

**応用: AIを使った一括アップロード**
```text
output/ フォルダ内のPNGファイルをすべてGoogle Driveの特定フォルダにアップロードしてください。
アカウント: your-email@gmail.com
フォルダID: <フォルダID>
gogcli drive upload コマンドを使ってください。
```

**期待される結果**: ファイルがGoogle Driveにアップロードされ、ファイルIDが返されます。Google DriveのWebページで確認できます。

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
      {"id": "trouble_1", "label": "ファイル一覧が空になる"},
      {"id": "trouble_2", "label": "ダウンロードがエラーになる"},
      {"id": "trouble_3", "label": "アップロードが失敗する"},
      {"id": "trouble_4", "label": "フォルダIDの調べ方がわからない"}
    ]
  }]
}
```

### トラブル1: ファイル一覧が空になる
**原因**: クエリの条件が厳しすぎる、またはアクセス権限のないドライブを見ている
**解決プロンプト**:
```text
まず条件なしで gog drive ls --account <email> --max 5 を試してください。
共有ドライブのファイルはデフォルトでは表示されない場合があります。
```

### トラブル2: ダウンロードがエラーになる
**原因**: Google形式ファイルに --format を指定していない
**解決プロンプト**:
```text
Google Docs/Sheets/Slides は --format で変換形式を指定する必要があります。
例: --format pdf（PDF変換）
例: --format csv（CSV変換）
```

### トラブル3: アップロードが失敗する
**原因**: ファイルパスが間違っている、またはファイルサイズが大きすぎる
**解決プロンプト**:
```text
ファイルパスが正しいか確認してください: ls -la <ファイルパス>
大きなファイル（数百MB以上）の場合はタイムアウトする可能性があります。
```

### トラブル4: フォルダIDの調べ方がわからない
**原因**: フォルダIDの取得方法を知らない
**解決プロンプト**:
```text
方法1: gog drive ls でフォルダ一覧を取得（MIMEタイプが folder のもの）
gog drive ls --account <email> --query "mimeType='application/vnd.google-apps.folder'"

方法2: Google DriveのWebページでフォルダを開き、URLの末尾がフォルダIDです
https://drive.google.com/drive/folders/<ここがフォルダID>
```

---

## ✅ チェックポイント
- [ ] Drive内のファイルを一覧表示できた
- [ ] ファイル名やMIMEタイプで検索できた
- [ ] ファイルをダウンロードできた（Google形式の変換ダウンロード含む）
- [ ] ファイルをアップロードできた


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```text
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```text
以下のgogcliコマンドを実行して、Drive操作が正しく動作するか確認してください:
1. gog drive ls --account <メールアドレス> --max 5
2. 上記の結果から1件選び、gog drive download でダウンロード
3. ダウンロードしたファイルが存在するか確認（ls -la）
すべて正常に動作するか確認してください。
```

**期待される結果**: ファイル一覧の表示とダウンロードがエラーなく完了します。

---

## 🎉 次のステップ

これでGoogle Drive操作は完了です！次のレッスンではGoogle Sheets操作を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-6）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-6）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-6（Google Sheets操作）
- next_window → 新しいウィンドウで /start-4-6
- finish → 終了
