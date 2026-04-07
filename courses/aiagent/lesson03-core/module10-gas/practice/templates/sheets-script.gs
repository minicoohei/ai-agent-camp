/**
 * 勤怠管理スクリプト テンプレート
 *
 * このテンプレートを元に、各関数の処理を実装してください。
 * 関数シグネチャとコメントは変更しないでください。
 */

// ===== 設定 =====
const SHEET_NAME = '勤怠データ';
const SUMMARY_SHEET_NAME = '月間集計';
const NOTIFICATION_EMAIL = ''; // 通知先メールアドレスを設定

/**
 * 各従業員の月間勤務時間を集計する
 *
 * 処理内容:
 * 1. 勤怠データシートから全行を取得
 * 2. 従業員ごとに出勤時間と退勤時間の差分を計算
 * 3. 月間の合計勤務時間を算出
 * 4. 集計結果を「月間集計」シートに出力
 *
 * @returns {Object} 従業員名をキー、合計時間（h）を値とするオブジェクト
 */
function calculateWorkHours() {
  // TODO: 実装してください
  // ヒント: SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME)
  // ヒント: 時間文字列のパースには Utilities.formatDate() や split(':') を使用
}

/**
 * 集計結果をメールで送信する
 *
 * 処理内容:
 * 1. calculateWorkHours() で集計結果を取得
 * 2. HTML形式のメール本文を作成（テーブル形式）
 * 3. GmailApp.sendEmail() で送信
 *
 * @param {string} [recipient] - 送信先メールアドレス（省略時は NOTIFICATION_EMAIL）
 */
function sendSummaryEmail(recipient) {
  // TODO: 実装してください
  // ヒント: GmailApp.sendEmail(to, subject, body, { htmlBody: htmlContent })
}

/**
 * シートの書式を自動整形する
 *
 * 処理内容:
 * 1. ヘッダー行の背景色を設定（#4285f4）
 * 2. ヘッダー行の文字色を白に設定
 * 3. 列幅を自動調整
 * 4. データ範囲に罫線を追加
 * 5. 日付列の表示形式を設定
 */
function formatSheet() {
  // TODO: 実装してください
  // ヒント: sheet.getRange().setBackground(), setBorder(), setNumberFormat()
}

/**
 * メニューにカスタムメニューを追加
 * スプレッドシートを開いた時に自動実行
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('勤怠管理')
    .addItem('勤務時間集計', 'calculateWorkHours')
    .addItem('集計メール送信', 'sendSummaryEmail')
    .addItem('書式整形', 'formatSheet')
    .addToUi();
}
