---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約30分"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "sheets"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-6: Google Sheets操作

## 📍 このセッションでやること

**Lesson 4-6: Google Sheets操作** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでスプレッドシートの読み書きを行う |
| 所要時間 | 約30分 |
| 使うスキル | gogcli sheets |
| 前提条件 | gogcli認証セットアップ済み（start-4-1完了） |

**このセッションの流れ:**
1. Driveからスプレッドシートを検索する
2. シートのデータを取得する（CSV出力）
3. 取得したデータをAIで分析する

セッション終了時には、gogcliを使ってGoogle Sheetsのデータ読み取りと分析ができるようになっています。

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

## 🚀 Step 1: Driveからスプレッドシートを検索する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: スプレッドシートの検索",
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

まず、操作対象のスプレッドシートを特定しましょう:

```bash
# Driveからスプレッドシートを検索
gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account your-email@gmail.com

# ※ gogcli v0.9.0 には `gog sheets list` コマンドはありません。
# シート（タブ）名は Google Sheets のUIで確認するか、
# gog sheets get でデータ取得時にシート名を指定してください。
```

**スプレッドシートIDの取得方法:**
- Google SheetsのURL: `https://docs.google.com/spreadsheets/d/<ここがスプレッドシートID>/edit`
- または `gog drive ls` の結果からファイルIDを使用

**期待される結果**: Driveにあるスプレッドシートのファイル一覧（ファイル名とID）が表示されます。

> **💡 ヒント**: 練習用のスプレッドシートがない場合は、Google Sheetsで新しいスプレッドシートを作成し、適当なデータ（名前、売上、日付など）を数行入力してください。

---

## 🚀 Step 2: シートのデータを取得する（CSV出力）

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: データの取得",
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

スプレッドシートのデータを取得します:

```bash
# シート全体のデータを取得
gog sheets get <スプレッドシートID> "Sheet1" --account your-email@gmail.com

# 特定の範囲を取得（A1:D10）
gog sheets get <スプレッドシートID> "Sheet1!A1:D10" --account your-email@gmail.com

# CSVファイルとして保存
gog sheets get <スプレッドシートID> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv

# 別の方法: Drive経由でCSVダウンロード
gog drive download <スプレッドシートID> --format csv --out ./downloads/sheet_data.csv --account your-email@gmail.com
```

**範囲指定の書式:**

| 書式 | 説明 | 例 |
|------|------|-----|
| `Sheet1` | シート全体 | `"Sheet1"` |
| `Sheet1!A1:D10` | 特定範囲 | `"Sheet1!A1:D10"` |
| `Sheet1!A:A` | 列全体 | `"Sheet1!A:A"` |
| `Sheet1!1:5` | 行範囲 | `"Sheet1!1:5"` |
| `'売上データ'!A1:Z` | 日本語シート名 | シート名をシングルクォートで囲む |

**期待される結果**: スプレッドシートのデータがターミナルに表示されます。CSVにリダイレクトした場合はファイルに保存されます。

> **⚠️ 注意**: 日本語のシート名を使う場合はシングルクォートで囲んでください（例: `'売上データ'!A1:D10`）。

---

## 🚀 Step 3: 取得したデータをAIで分析する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: AIによるデータ分析",
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

取得したスプレッドシートのデータをAIに分析させましょう:

```bash
# データを取得してファイルに保存
gog sheets get <スプレッドシートID> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv
```

保存したCSVファイルをCursorに読み込ませて、分析を依頼します:

```text
/tmp/sheet_data.csv のデータを分析してください:
1. データの概要（行数、列数、データ型）
2. 基本統計（数値列の平均、最大、最小）
3. 気づいた傾向やパターン
4. データの品質問題（欠損値、異常値）があれば指摘
```

**応用: レポート生成**
```text
上記のスプレッドシートデータから月次レポートのサマリーを作成してください:
- 主要KPIのハイライト
- 前月比の変化
- 注目すべきトレンド
- 改善提案
Markdown形式で output/reports/ に保存してください。
```

**応用: データ可視化**
```text
上記のデータをPythonのmatplotlibで可視化してください:
- 売上の月次推移グラフ
- カテゴリ別の円グラフ
- 上位10件のバーチャート
グラフは output/images/ に保存してください。
```

**期待される結果**: AIがデータの分析結果、統計情報、トレンドの解説を生成してくれます。

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
      {"id": "trouble_1", "label": "スプレッドシートIDがわからない"},
      {"id": "trouble_2", "label": "範囲指定でエラーになる"},
      {"id": "trouble_3", "label": "データが文字化けする"},
      {"id": "trouble_4", "label": "練習用データがない"}
    ]
  }]
}
```

### トラブル1: スプレッドシートIDがわからない
**原因**: IDの取得方法を知らない
**解決プロンプト**:
```text
Google Sheetsを開いてURLを確認してください:
https://docs.google.com/spreadsheets/d/<この部分がID>/edit
または gog drive ls でスプレッドシートを検索してファイルIDを使ってください。
```

### トラブル2: 範囲指定でエラーになる
**原因**: シート名が間違っている、または範囲が存在しない
**解決プロンプト**:
```text
gogcli には `gog sheets list` コマンドはありません。
Google Sheets のUIでシート名（タブ名）を確認してください。
日本語のシート名はシングルクォートで囲む必要があります: '売上データ'!A1:D10
```

### トラブル3: データが文字化けする
**原因**: エンコーディングの問題
**解決プロンプト**:
```text
出力をファイルにリダイレクトしてエンコーディングを確認してください:
gog sheets get ... > /tmp/data.csv
file /tmp/data.csv
UTF-8でない場合は iconv で変換: iconv -f SHIFT_JIS -t UTF-8 /tmp/data.csv
```

### トラブル4: 練習用データがない
**原因**: テストに使えるスプレッドシートがない
**解決プロンプト**:
```text
Google Sheetsで新しいスプレッドシートを作成し、以下のサンプルデータを入力してください:
A1: 名前, B1: 部門, C1: 売上, D1: 月
A2: 田中, B2: 営業, C2: 500000, D2: 1月
A3: 鈴木, B3: マーケ, C3: 350000, D3: 1月
（5-10行あれば十分です）
```

---

## ✅ チェックポイント
- [ ] Driveからスプレッドシートを検索できた
- [ ] 特定の範囲のデータを取得できた
- [ ] データをCSVファイルとして保存できた
- [ ] AIにデータを分析させて結果を確認できた


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
以下のgogcliコマンドを実行して、Sheets操作が正しく動作するか確認してください:
1. gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account <メールアドレス>
2. 上記から1つ選び、gog sheets get <スプレッドシートID> "Sheet1" --account <メールアドレス> でデータを取得
3. 取得したデータが正しく表示されるか確認
すべて正常に動作するか確認してください。
```

**期待される結果**: シート一覧の表示とデータ取得がエラーなく完了します。

---

## 🎉 次のステップ

これでGoogle Sheets操作は完了です！次のレッスンでは、これまで学んだGmail・Calendar・Drive・Sheetsを統合したAI秘書ワークフローを構築します。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-7）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-7）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-7（AI秘書ワークフロー統合）
- next_window → 新しいウィンドウで /start-4-7
- finish → 終了
