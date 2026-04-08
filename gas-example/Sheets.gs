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
  } else {
    sheet.clearContents();
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
