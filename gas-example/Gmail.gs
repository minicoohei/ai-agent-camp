/**
 * Gmail.gs — GmailApp メール検索・抽出・シート整理
 * Lesson 10-4 の成果物テンプレート
 */

/**
 * メール検索
 * @param {string} query - Gmail検索クエリ
 * @param {number} maxResults - 最大取得件数
 * @return {GmailThread[]} スレッド配列
 */
function searchEmails(query, maxResults) {
  query = query || "is:unread newer_than:7d";
  maxResults = maxResults || 50;
  var threads = GmailApp.search(query, 0, maxResults);
  Logger.log("検索結果: " + threads.length + " スレッド");
  return threads;
}

/**
 * スレッドからメール情報を抽出
 * @param {GmailThread[]} threads - スレッド配列
 * @return {Object[]} メール情報配列
 */
function extractEmailData(threads) {
  var data = [];
  threads.forEach(function(thread) {
    var messages = thread.getMessages();
    var lastMessage = messages[messages.length - 1];
    data.push({
      subject: lastMessage.getSubject(),
      from: lastMessage.getFrom(),
      date: lastMessage.getDate(),
      body: lastMessage.getPlainBody().substring(0, 200),
      isUnread: lastMessage.isUnread(),
      messageCount: messages.length
    });
  });
  return data;
}

/**
 * データをスプレッドシートに書き込み
 * @param {Object[]} data - メール情報配列
 * @param {string} sheetName - シート名
 */
function writeToSheet(data, sheetName) {
  sheetName = sheetName || "メール一覧_" + Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy-MM-dd");
  var ss = SpreadsheetApp.create(sheetName);
  var sheet = ss.getActiveSheet();

  // ヘッダー行
  var headers = ["件名", "送信者", "日時", "本文（先頭200文字）", "未読", "メッセージ数"];
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(1, 1, 1, headers.length).setFontWeight("bold");

  // データ行
  if (data.length > 0) {
    var rows = data.map(function(item) {
      return [
        item.subject,
        item.from,
        Utilities.formatDate(item.date, "Asia/Tokyo", "yyyy-MM-dd HH:mm"),
        item.body,
        item.isUnread ? "未読" : "既読",
        item.messageCount
      ];
    });
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }

  Logger.log("シート作成完了: " + ss.getUrl());
  return ss.getUrl();
}

/**
 * メイン関数: メール検索→抽出→シート整理
 */
function extractAndOrganizeEmails() {
  var threads = searchEmails("is:unread newer_than:7d", 50);
  var data = extractEmailData(threads);
  var url = writeToSheet(data);
  Logger.log("処理完了: " + data.length + " 件のメールをシートに整理しました");
  Logger.log("シートURL: " + url);
}

/**
 * 定期実行トリガー設定（毎日9時）
 */
function setEmailExtractTrigger() {
  // 既存トリガー削除
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === "extractAndOrganizeEmails") {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // 新規トリガー作成
  ScriptApp.newTrigger("extractAndOrganizeEmails")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("毎日9時のトリガーを設定しました");
}
