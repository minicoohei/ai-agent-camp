function getDefaultCalendar() {
  const calendar = CalendarApp.getDefaultCalendar();
  Logger.log("カレンダー名: " + calendar.getName());
  Logger.log("カレンダーID: " + calendar.getId());
  return calendar;
}

function getAllCalendars() {
  const calendars = CalendarApp.getAllCalendars();
  Logger.log("全カレンダー数: " + calendars.length);
  calendars.forEach(calendar => {
    Logger.log("- " + calendar.getName());
  });
  return calendars;
}

function createSimpleEvent(title, startTime, endTime) {
  const calendar = CalendarApp.getDefaultCalendar();
  const event = calendar.createEvent(title, startTime, endTime);
  Logger.log("イベント作成: " + title);
  Logger.log("イベントID: " + event.getId());
  return event.getId();
}

function createTomorrowEvent() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  const startTime = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 14, 0, 0);
  const endTime = new Date(startTime.getTime() + 60 * 60 * 1000);

  return createSimpleEvent("テストイベント", startTime, endTime);
}

function getTodayEvents() {
  const calendar = CalendarApp.getDefaultCalendar();
  const today = new Date();
  const dayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 0, 0, 0);
  const dayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59);

  const events = calendar.getEvents(dayStart, dayEnd);
  Logger.log("今日のイベント数: " + events.length);

  events.forEach(event => {
    Logger.log("- " + event.getTitle() + " (" + event.getStartTime().toLocaleString() + ")");
  });

  return events;
}

function dailyMorningTask() {
  const events = getTodayEvents();
  Logger.log("本日のイベント確認: " + events.length + "件");
  // ここにメール通知などの処理を追加
}

function createDailyTrigger() {
  // 既存トリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  // 毎日9時に実行するトリガーを作成
  ScriptApp.newTrigger("dailyMorningTask")
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();

  Logger.log("毎日9時のトリガーを設定しました");
}
