/**
 * Google Apps Script サンプル集（Final Example）
 * 
 * このファイルには、研修で作成するGASスクリプトの
 * 完成版サンプルが含まれています。
 * 
 * 使用方法:
 * 1. https://script.google.com/ を開く
 * 2. 新しいプロジェクトを作成
 * 3. このコードをコピー&ペースト
 * 4. 必要に応じてスプレッドシートIDなどを書き換え
 */

// ========================================
// 1. スプレッドシート操作
// ========================================

/**
 * スプレッドシートのデータを取得
 */
function getSpreadsheetData() {
  // スプレッドシートIDを指定（URLから取得）
  const SHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
  const SHEET_NAME = 'シート1';
  
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const sheet = ss.getSheetByName(SHEET_NAME);
    
    // 全データを取得
    const data = sheet.getDataRange().getValues();
    
    // ヘッダー行
    const headers = data[0];
    
    // データ行をオブジェクトの配列に変換
    const records = data.slice(1).map(row => {
      const record = {};
      headers.forEach((header, i) => {
        record[header] = row[i];
      });
      return record;
    });
    
    Logger.log(`取得したレコード数: ${records.length}`);
    Logger.log(JSON.stringify(records, null, 2));
    
    return records;
    
  } catch (e) {
    Logger.log(`エラー: ${e.message}`);
    return [];
  }
}

/**
 * スプレッドシートにデータを追加
 */
function appendToSpreadsheet(newData) {
  const SHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
  const SHEET_NAME = 'シート1';
  
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const sheet = ss.getSheetByName(SHEET_NAME);
  
  // 配列の場合は一括追加
  if (Array.isArray(newData[0])) {
    sheet.getRange(
      sheet.getLastRow() + 1, 
      1, 
      newData.length, 
      newData[0].length
    ).setValues(newData);
  } else {
    // 1行追加
    sheet.appendRow(newData);
  }
  
  Logger.log('データを追加しました');
}

// ========================================
// 2. メール送信
// ========================================

/**
 * テンプレートメールを送信
 */
function sendTemplateEmail() {
  const recipient = 'example@example.com';
  const subject = '【リマインダー】週次レポート提出のお願い';
  
  // HTMLテンプレート
  const htmlBody = `
    <div style="font-family: sans-serif; max-width: 600px;">
      <h2 style="color: #333;">週次レポート提出のお願い</h2>
      <p>お疲れ様です。</p>
      <p>今週の週次レポートの提出期限が近づいております。</p>
      <ul>
        <li><strong>提出期限</strong>: ${getNextFriday()}</li>
        <li><strong>提出先</strong>: 共有フォルダ</li>
      </ul>
      <p>ご対応よろしくお願いいたします。</p>
      <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
      <p style="color: #666; font-size: 12px;">このメールはGoogle Apps Scriptから自動送信されました。</p>
    </div>
  `;
  
  GmailApp.sendEmail(recipient, subject, '', {
    htmlBody: htmlBody,
    name: '自動リマインダー'
  });
  
  Logger.log(`メール送信完了: ${recipient}`);
}

/**
 * 次の金曜日の日付を取得
 */
function getNextFriday() {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const daysUntilFriday = (5 - dayOfWeek + 7) % 7 || 7;
  const nextFriday = new Date(today.getTime() + daysUntilFriday * 24 * 60 * 60 * 1000);
  
  return Utilities.formatDate(nextFriday, 'Asia/Tokyo', 'yyyy/MM/dd (E)');
}

/**
 * スプレッドシートの一覧に対して一括メール送信
 */
function sendBulkEmails() {
  const SHEET_ID = 'YOUR_SPREADSHEET_ID_HERE';
  const ss = SpreadsheetApp.openById(SHEET_ID);
  const sheet = ss.getSheetByName('メール送信先');
  
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  
  // ヘッダーのインデックスを取得
  const emailCol = headers.indexOf('メールアドレス');
  const nameCol = headers.indexOf('氏名');
  const sentCol = headers.indexOf('送信済');
  
  let sentCount = 0;
  
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    
    // 既に送信済みならスキップ
    if (row[sentCol] === '済') continue;
    
    const email = row[emailCol];
    const name = row[nameCol];
    
    if (!email) continue;
    
    // メール送信
    const subject = `【${name}様】お知らせ`;
    const body = `${name}様\n\nお世話になっております。\n...`;
    
    try {
      GmailApp.sendEmail(email, subject, body);
      
      // 送信済みフラグを更新
      sheet.getRange(i + 1, sentCol + 1).setValue('済');
      sentCount++;
      
      // 送信間隔を空ける（レート制限対策）
      Utilities.sleep(1000);
      
    } catch (e) {
      Logger.log(`送信エラー (${email}): ${e.message}`);
    }
  }
  
  Logger.log(`送信完了: ${sentCount}件`);
}

// ========================================
// 3. カレンダー連携
// ========================================

/**
 * 今日の予定を取得
 */
function getTodayEvents() {
  const calendar = CalendarApp.getDefaultCalendar();
  const today = new Date();
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);
  
  const events = calendar.getEvents(today, tomorrow);
  
  const eventList = events.map(event => ({
    title: event.getTitle(),
    start: Utilities.formatDate(event.getStartTime(), 'Asia/Tokyo', 'HH:mm'),
    end: Utilities.formatDate(event.getEndTime(), 'Asia/Tokyo', 'HH:mm'),
    location: event.getLocation() || '-',
    description: event.getDescription() || '-'
  }));
  
  Logger.log(`今日の予定: ${eventList.length}件`);
  Logger.log(JSON.stringify(eventList, null, 2));
  
  return eventList;
}

/**
 * カレンダーにイベントを追加
 */
function createCalendarEvent(title, startTime, endTime, options = {}) {
  const calendar = CalendarApp.getDefaultCalendar();
  
  const event = calendar.createEvent(title, startTime, endTime, {
    description: options.description || '',
    location: options.location || '',
    guests: options.guests || '',
    sendInvites: options.sendInvites || false
  });
  
  Logger.log(`イベント作成: ${event.getTitle()}`);
  return event;
}

// ========================================
// 4. Slack通知（Webhook）
// ========================================

/**
 * Slackにメッセージを送信
 */
function sendSlackNotification(message, channel = '#general') {
  const WEBHOOK_URL = 'YOUR_SLACK_WEBHOOK_URL_HERE';
  
  const payload = {
    channel: channel,
    username: 'GAS Bot',
    icon_emoji: ':robot_face:',
    text: message,
    blocks: [
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: message
        }
      },
      {
        type: 'context',
        elements: [
          {
            type: 'mrkdwn',
            text: `Sent from Google Apps Script at ${new Date().toLocaleString('ja-JP')}`
          }
        ]
      }
    ]
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };
  
  try {
    const response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    Logger.log(`Slack送信成功: ${response.getResponseCode()}`);
    return true;
  } catch (e) {
    Logger.log(`Slack送信エラー: ${e.message}`);
    return false;
  }
}

// ========================================
// 5. 定期実行（トリガー設定）
// ========================================

/**
 * トリガーを設定
 */
function createTriggers() {
  // 既存のトリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    ScriptApp.deleteTrigger(trigger);
  });
  
  // 毎日9時に実行
  ScriptApp.newTrigger('dailyReport')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
  
  // 毎週月曜日に実行
  ScriptApp.newTrigger('weeklyDigest')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();
  
  Logger.log('トリガーを設定しました');
}

/**
 * 日次レポート
 */
function dailyReport() {
  const events = getTodayEvents();
  
  if (events.length === 0) {
    sendSlackNotification(':calendar: 今日の予定はありません');
    return;
  }
  
  let message = ':calendar: *今日の予定*\n\n';
  events.forEach(event => {
    message += `• *${event.start}-${event.end}* ${event.title}\n`;
  });
  
  sendSlackNotification(message);
}

/**
 * 週次ダイジェスト
 */
function weeklyDigest() {
  const message = `:newspaper: *週次ダイジェスト*\n\n` +
    `今週もよろしくお願いします！\n` +
    `重要なタスクの確認をお忘れなく。`;
  
  sendSlackNotification(message);
}

// ========================================
// 6. Web API（doGet/doPost）
// ========================================

/**
 * GETリクエストハンドラー
 * デプロイ後、URLにアクセスすると実行される
 */
function doGet(e) {
  const action = e.parameter.action || 'status';
  
  let response;
  
  switch (action) {
    case 'status':
      response = {
        status: 'ok',
        timestamp: new Date().toISOString(),
        message: 'GAS API is running'
      };
      break;
      
    case 'events':
      response = {
        status: 'ok',
        events: getTodayEvents()
      };
      break;
      
    case 'data':
      response = {
        status: 'ok',
        data: getSpreadsheetData()
      };
      break;
      
    default:
      response = {
        status: 'error',
        message: 'Unknown action'
      };
  }
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * POSTリクエストハンドラー
 */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const action = data.action;
    
    let response;
    
    switch (action) {
      case 'notify':
        sendSlackNotification(data.message, data.channel);
        response = { status: 'ok', message: 'Notification sent' };
        break;
        
      case 'add':
        appendToSpreadsheet(data.values);
        response = { status: 'ok', message: 'Data added' };
        break;
        
      default:
        response = { status: 'error', message: 'Unknown action' };
    }
    
    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (e) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'error',
        message: e.message
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ========================================
// 7. ユーティリティ関数
// ========================================

/**
 * 日付フォーマット
 */
function formatDate(date, format = 'yyyy-MM-dd') {
  return Utilities.formatDate(date, 'Asia/Tokyo', format);
}

/**
 * HTTPリクエスト
 */
function fetchJson(url, options = {}) {
  const response = UrlFetchApp.fetch(url, {
    muteHttpExceptions: true,
    ...options
  });
  
  return JSON.parse(response.getContentText());
}

/**
 * プロパティサービス（設定値の保存）
 */
function setProperty(key, value) {
  PropertiesService.getScriptProperties().setProperty(key, value);
}

function getProperty(key) {
  return PropertiesService.getScriptProperties().getProperty(key);
}

// ========================================
// テスト用関数
// ========================================

function testAll() {
  Logger.log('=== GAS サンプル テスト ===\n');
  
  Logger.log('1. スプレッドシートデータ取得');
  // getSpreadsheetData(); // コメント解除して実行
  
  Logger.log('\n2. 今日の予定取得');
  getTodayEvents();
  
  Logger.log('\n3. 次の金曜日');
  Logger.log(getNextFriday());
  
  Logger.log('\n=== テスト完了 ===');
}
