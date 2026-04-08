---
description: "When the user says /start-10-3 — Module 10 Lesson 10-3: Google Sheets自動化・データ処理レポート"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1", "start-10-2"]
duration: "約30分"
level: "intermediate"
tags: ["gas", "sheets", "google", "automation"]
---

# 🎓 Lesson 10-3: Google Sheets自動化・データ処理レポート

## 📍 このセッションでやること

**Lesson 10-3: GASとGoogle Sheets連携** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GASからスプレッドシートの読み書き・データ処理・レポート生成を自動化する |
| 所要時間 | 約30分 |
| 使うスキル | gas-clasp-ops, Google Sheets API, gogcli |
| 前提条件 | Lesson 10-1・Lesson 10-2 完了、GASプロジェクト作成済み |
| 教材ページ | [Module 10: GAS](https://ai-agent.camp/ja/course/module-10) を並行参照 |

**このセッションの流れ:**
1. スプレッドシートアクセス
2. データ読み取り機能
3. データ書き込み機能
4. レポート生成機能
5. 自動化ワークフロー

セッション終了時には、Sheets連携の自動化ができるようになっています。

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

## 🚀 Step 1: スプレッドシートアクセス

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: スプレッドシートアクセス",
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
gas-example ディレクトリに Sheets.gs ファイルを作成し、以下の内容を記述してください：

function getActiveSpreadsheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    Logger.log("アクティブなスプレッドシートがありません。新規作成してください。");
    return null;
  }
  Logger.log("スプレッドシート: " + ss.getName());
  Logger.log("スプレッドシートID: " + ss.getId());
  return ss;
}

function getAllSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) return [];

  const sheets = ss.getSheets();
  Logger.log("全シート数: " + sheets.length);

  sheets.forEach(sheet => {
    Logger.log("- " + sheet.getName() + " (" + sheet.getLastRow() + "行)");
  });

  return sheets;
}

clasp push で同期してください。
```

**期待される結果**: Sheets.gs がGoogleドライブに同期されます。

---

## 🚀 Step 2: データ読み取り機能

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: データ読み取り機能",
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
Sheets.gs に以下のデータ読み取り関数を追加してください：

function getDataRange(sheetName, range) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("シートが見つかりません: " + sheetName);
    return [];
  }

  const data = sheet.getRange(range).getValues();
  Logger.log("データ取得: " + range + " (" + data.length + "行)");
  return data;
}

function getAllData(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];

  const lastRow = sheet.getLastRow();
  const lastColumn = sheet.getLastColumn();

  if (lastRow < 1) {
    Logger.log("データがありません");
    return [];
  }

  return sheet.getRange(1, 1, lastRow, lastColumn).getValues();
}

clasp push で同期してください。
```

**期待される結果**: スプレッドシートからデータを読み取る関数が追加されます。

---

## 🚀 Step 3: データ書き込み機能

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: データ書き込み機能",
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
Sheets.gs に以下のデータ書き込み関数を追加してください：

function writeSingleCell(sheetName, cell, value) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("シートが見つかりません: " + sheetName);
    return false;
  }

  sheet.getRange(cell).setValue(value);
  Logger.log("セル書き込み: " + cell + " = " + value);
  return true;
}

function appendRow(sheetName, rowData) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    Logger.log("シートが見つかりません: " + sheetName);
    return false;
  }

  sheet.appendRow(rowData);
  Logger.log("行追加: " + rowData.join(", "));
  return true;
}

function writeDataRange(sheetName, startCell, data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return false;

  const rows = data.length;
  const cols = data[0].length;
  const range = sheet.getRange(startCell).offset(0, 0, rows, cols);
  range.setValues(data);

  Logger.log("範囲書き込み完了: " + rows + "行 x " + cols + "列");
  return true;
}

clasp push で同期してください。
```

**期待される結果**: スプレッドシートへのデータ書き込み関数が追加されます。

---

## 🚀 Step 4: レポート生成機能

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: レポート生成機能",
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
Sheets.gs に以下のレポート生成関数を追加してください：

function generateSummaryReport(sourceSheetName, reportSheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceSheet = ss.getSheetByName(sourceSheetName);
  let reportSheet = ss.getSheetByName(reportSheetName);

  // レポートシートがなければ作成
  if (!reportSheet) {
    reportSheet = ss.insertSheet(reportSheetName);
  }

  // レポートシートをクリア
  reportSheet.clearContents();

  // レポートヘッダー
  reportSheet.getRange("A1").setValue("=== サマリーレポート ===");
  reportSheet.getRange("A1").setFontSize(14).setFontWeight("bold");
  reportSheet.getRange("A2").setValue("生成日時: " + new Date().toLocaleString("ja-JP"));

  // データ統計
  const lastRow = sourceSheet.getLastRow();
  const lastCol = sourceSheet.getLastColumn();

  reportSheet.getRange("A4").setValue("総レコード数:");
  reportSheet.getRange("B4").setValue(lastRow - 1); // ヘッダー除く

  reportSheet.getRange("A5").setValue("総列数:");
  reportSheet.getRange("B5").setValue(lastCol);

  Logger.log("サマリーレポート生成完了");
}

function createTestData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("TestData");

  if (!sheet) {
    sheet = ss.insertSheet("TestData");
  }

  // ヘッダー
  sheet.getRange("A1:D1").setValues([["日付", "商品", "数量", "金額"]]);

  // サンプルデータ
  const testData = [
    ["2024-01-01", "商品A", 10, 1000],
    ["2024-01-02", "商品B", 5, 500],
    ["2024-01-03", "商品A", 15, 1500],
    ["2024-01-04", "商品C", 8, 800],
    ["2024-01-05", "商品B", 12, 1200]
  ];

  sheet.getRange(2, 1, testData.length, 4).setValues(testData);
  Logger.log("テストデータ作成完了");
}

clasp push して、まず createTestData を実行し、次に generateSummaryReport("TestData", "Report") を実行してください。
```

**期待される結果**: テストデータとサマリーレポートが自動生成されます。

---

## 🚀 Step 5: 自動化ワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 自動化ワークフロー",
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
Sheets.gs に以下の自動化ワークフロー関数を追加してください：

function dailyReportTask() {
  Logger.log("===== 日次レポート生成開始 =====");

  try {
    // レポート生成
    generateSummaryReport("TestData", "DailyReport");

    // 完了通知（メール送信）
    const userEmail = Session.getActiveUser().getEmail();
    if (userEmail) {
      GmailApp.sendEmail(
        userEmail,
        "日次レポート完了 " + new Date().toLocaleDateString("ja-JP"),
        "日次レポートが生成されました。スプレッドシートのDailyReportシートをご確認ください。"
      );
    }

    Logger.log("日次レポート完了");
  } catch (error) {
    Logger.log("エラー: " + error);
  }
}

function setDailyReportTrigger() {
  // 既存の同名トリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === "dailyReportTask") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // 毎日10時に実行するトリガーを作成
  ScriptApp.newTrigger("dailyReportTask")
    .timeBased()
    .everyDays(1)
    .atHour(10)
    .create();

  Logger.log("毎日10時のレポート生成トリガーを設定しました");
}

clasp push で同期してください。
```

**期待される結果**: 日次レポート自動生成とトリガー設定ができます。

---

## 🚀 Step 6: gogcli × GAS × clasp deploy — メール集計パイプライン

> **📝 ポイント**: gogcli でメールを取得 → GAS で集計処理 → Sheets に出力 → clasp deploy で本番反映、という E2E パイプラインを構築します。ローカル CLI（gogcli）とクラウド実行環境（GAS）を組み合わせた実践的なワークフローです。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 6: gogcli × GAS × clasp deploy",
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
gogcli でメールを取得し、GAS で集計してスプレッドシートに出力するパイプラインを構築します。

### Step 6-1: gogcli で未読メールを取得

gog gmail search "is:unread" --json > ~/ai-agent-camp/gas-example/unread_emails.json

取得した JSON の内容を確認してください（送信者、件名、日時など）。

### Step 6-2: GAS でメール集計スクリプトを作成

Sheets.gs に以下の関数を追加してください：

function aggregateEmailStats() {
  // GmailApp でメール統計を集計してシートに出力
  const threads = GmailApp.search("is:unread", 0, 50);
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("メール集計");

  if (!sheet) {
    sheet = ss.insertSheet("メール集計");
  }

  sheet.clearContents();

  // ヘッダー
  sheet.getRange("A1:E1").setValues([["送信者", "件名", "受信日時", "ラベル", "スレッド数"]]);
  sheet.getRange("A1:E1").setFontWeight("bold");

  // メールデータ
  const data = threads.map(thread => {
    const msg = thread.getMessages()[0];
    return [
      msg.getFrom(),
      msg.getSubject(),
      msg.getDate().toLocaleString("ja-JP"),
      thread.getLabels().map(l => l.getName()).join(", "),
      thread.getMessageCount()
    ];
  });

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  // 集計サマリー
  const summaryRow = data.length + 3;
  sheet.getRange("A" + summaryRow).setValue("集計日時:");
  sheet.getRange("B" + summaryRow).setValue(new Date().toLocaleString("ja-JP"));
  sheet.getRange("A" + (summaryRow + 1)).setValue("未読メール数:");
  sheet.getRange("B" + (summaryRow + 1)).setValue(data.length);

  Logger.log("メール集計完了: " + data.length + "件");
}

clasp push で同期してください。

### Step 6-3: clasp deploy で本番デプロイ

cd ~/ai-agent-camp/gas-example
clasp push
clasp deploy --description "メール集計v1"

デプロイIDが表示されることを確認してください。
GASエディタで aggregateEmailStats を実行してスプレッドシートに出力されることを確認してください。
```

**期待される結果**: gogcli でローカルにメールデータを確認でき、GAS 側で同じメールデータをスプレッドシートに集計し、clasp deploy で本番デプロイが完了します。

**💡 実践演習: gogcliでメール取得→GASで集計→Sheetsに出力→clasp deploy**

以下のワークフローを実践してみましょう:
1. `gog gmail search "is:unread" --json` でローカルに未読メール一覧を取得
2. GAS の `aggregateEmailStats()` を実行してスプレッドシートに集計
3. gogcli の出力と GAS の出力を比較し、データの一致を確認
4. `clasp push && clasp deploy --description "メール集計v1"` で本番デプロイ
5. デプロイしたスクリプトにトリガーを設定し、毎朝自動実行されるようにする

> **ヒント**: このパイプラインは実務で非常によく使われるパターンです。
> - **gogcli**: ローカルでデータを素早く確認・デバッグ
> - **GAS**: クラウド上で定期実行・自動化
> - **clasp**: ローカル開発 → クラウドデプロイのCI/CDフロー

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
      {"id": "trouble_1", "label": "Sheet not found"},
      {"id": "trouble_2", "label": "Invalid range"},
      {"id": "trouble_3", "label": "Permission denied for Gmail"},
      {"id": "trouble_4", "label": "データが書き込めない"},
      {"id": "trouble_5", "label": "clasp deploy が失敗する"},
      {"id": "trouble_6", "label": "gogcli の認証エラー（gog gmail search が失敗）"}
    ]
  }]
}
```


### トラブル1: 「Sheet not found」
**原因**: シート名が存在しない
**解決プロンプト**:
```
getAllSheets() を実行して、存在するシート名を確認してください。
シート名のスペルが正しいか確認してください。
```

### トラブル2: 「Invalid range」
**原因**: 範囲指定の形式が不正
**解決プロンプト**:
```
範囲指定を A1:C10 形式で確認してください。
getLastRow() と getLastColumn() で有効範囲を確認してください。
```

### トラブル3: 「Permission denied for Gmail」
**原因**: Gmail APIの権限がない
**解決プロンプト**:
```
GASエディタでGmail APIを有効化してください。
appsscript.json にGmailスコープを追加する方法を教えてください。
```

### トラブル4: データが書き込めない
**原因**: シートが保護されている、または配列のサイズが不一致
**解決プロンプト**:
```
シートの保護設定を確認してください。
書き込むデータ配列の行数と列数が正しいか確認してください。
```

### トラブル5: clasp deploy が失敗する
**原因**: デプロイ権限がない、または appsscript.json の設定不備
**解決プロンプト**:
```
clasp deployments で既存のデプロイ一覧を確認してください。
appsscript.json に必要な oauthScopes が設定されているか確認してください。
clasp login --status で認証状態を確認してください。
```

### トラブル6: gogcli の認証エラー
**原因**: gogcli の認証が未完了、またはトークンが期限切れ
**解決プロンプト**:
```
gog auth status で認証状態を確認してください。
認証切れの場合は gog auth login で再認証してください。
4-1 を参照して gogcli のセットアップを完了させてください。
```

---

## ✅ チェックポイント
- [ ] スプレッドシートにアクセスできる
- [ ] データの読み取りができる
- [ ] データの書き込みができる
- [ ] レポート生成ができる
- [ ] 自動化トリガーが設定できる
- [ ] メール通知が送信される
- [ ] gogcli でメールデータが取得できる（`gog gmail search "is:unread" --json`）
- [ ] GAS でメール集計がスプレッドシートに出力される
- [ ] `clasp deploy` で本番デプロイが成功する


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/gas/
└── Code.gs  (GASスクリプト)
```

### 確認コマンド
```bash
# ローカルのスクリプトファイルを確認
ls -la output/gas/

# スクリプト内容の冒頭を確認
head -30 output/gas/Code.gs

# GASエディタで確認
clasp open
```

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: Google Sheets にテストデータ・レポートシートが作成されているか、GAS関数（clasp push済み）が正常に動作するか、clasp deploy が成功しているかを確認してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-11-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-11-1
- finish → 終了
