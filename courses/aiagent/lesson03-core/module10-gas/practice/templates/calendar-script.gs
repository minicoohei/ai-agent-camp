/**
 * カレンダー連携スクリプト テンプレート
 *
 * Google Calendar から翌日の予定を取得し、Slack に通知します。
 * 各関数の処理を実装してください。
 */

// ===== 設定 =====
const SLACK_WEBHOOK_URL = ''; // Slack Incoming Webhook URL を設定
const CALENDAR_ID = 'primary'; // 対象カレンダーID

/**
 * 翌日のカレンダー予定を取得する
 *
 * 処理内容:
 * 1. 翌日の開始時刻（00:00）と終了時刻（23:59）を計算
 * 2. CalendarApp でイベントを取得
 * 3. イベント情報を構造化して返す
 *
 * @returns {Array<Object>} イベント配列 [{title, start, end, location, description}]
 */
function getTomorrowEvents() {
  // TODO: 実装してください
  // ヒント: CalendarApp.getDefaultCalendar().getEvents(startTime, endTime)
  // ヒント: new Date() で今日の日付を取得し、setDate(getDate() + 1) で翌日に
}

/**
 * イベントリストを見やすいテキストに整形する
 *
 * 処理内容:
 * 1. イベントを開始時刻順にソート
 * 2. 各イベントを「時刻 | タイトル | 場所」形式に整形
 * 3. 予定がない場合は「予定はありません」を返す
 *
 * @param {Array<Object>} events - イベント配列
 * @returns {string} 整形されたメッセージ文字列
 */
function formatEventMessage(events) {
  // TODO: 実装してください
  // ヒント: Utilities.formatDate(date, 'Asia/Tokyo', 'HH:mm')
}

/**
 * Slack Webhook でメッセージを送信する
 *
 * 処理内容:
 * 1. Slack メッセージペイロードを作成
 * 2. UrlFetchApp.fetch() で POST リクエスト送信
 * 3. レスポンスを確認
 *
 * @param {string} message - 送信するメッセージ
 */
function sendToSlack(message) {
  // TODO: 実装してください
  // ヒント: UrlFetchApp.fetch(SLACK_WEBHOOK_URL, { method: 'post', payload: JSON.stringify({text: message}) })
}

/**
 * メイン実行関数
 * 翌日の予定を取得 → 整形 → Slack 通知
 */
function notifyTomorrowSchedule() {
  const events = getTomorrowEvents();
  const message = formatEventMessage(events);

  if (SLACK_WEBHOOK_URL) {
    sendToSlack(message);
  } else {
    Logger.log('Slack Webhook URL が未設定です。メッセージ:');
    Logger.log(message);
  }
}

/**
 * 時間トリガーを設定する
 * 毎日17:00に notifyTomorrowSchedule を実行
 */
function createDailyTrigger() {
  // 既存のトリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'notifyTomorrowSchedule') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // 新規トリガー作成
  ScriptApp.newTrigger('notifyTomorrowSchedule')
    .timeBased()
    .atHour(17)
    .everyDays(1)
    .create();

  Logger.log('トリガーを設定しました: 毎日17:00');
}
