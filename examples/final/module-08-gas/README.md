# Module 8: Google Apps Script - 成果物（Final）

Google Apps Script（GAS）によるGoogle Workspace自動化の例です。

## 学習目標
- GASプロジェクトをClasp（CLI）で管理できる
- Googleサービス（Sheets, Gmail, Drive）を自動化できる
- トリガーによる定期実行を設定できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `Code.gs` | GAS | メインスクリプト |
| `appsscript.json` | JSON | マニフェスト |
| `.clasp.json` | JSON | Clasp設定 |
| `README_GAS.md` | Markdown | 使用方法ガイド |

## GASプロジェクト構成

```
┌─────────────────────────────────────────────────────────┐
│  GAS プロジェクト構成                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  gas-project/                                           │
│  ├── .clasp.json       # Clasp設定（ローカル）          │
│  ├── appsscript.json   # マニフェスト                   │
│  ├── Code.gs           # メインスクリプト               │
│  ├── Utils.gs          # ユーティリティ関数             │
│  └── Config.gs         # 設定値                         │
│                                                         │
│  連携サービス:                                          │
│  ├── Google Sheets     # スプレッドシート               │
│  ├── Gmail             # メール送受信                   │
│  ├── Google Drive      # ファイル管理                   │
│  ├── Google Calendar   # 予定管理                       │
│  └── Slack Webhook     # 外部連携                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Claspセットアップ

### 1. Claspインストール
```bash
npm install -g @google/clasp
clasp login
```

### 2. プロジェクト作成
```bash
# 新規作成
clasp create --title "MyAutomation" --type standalone

# 既存プロジェクトをクローン
clasp clone <script_id>
```

### 3. デプロイ
```bash
# コードをプッシュ
clasp push

# ブラウザで開く
clasp open
```

## Code.gs サンプル

```javascript
/**
 * Google Apps Script - 自動化サンプル
 * 
 * 機能:
 * 1. スプレッドシートからデータを読み取り
 * 2. 条件に基づいてメール送信
 * 3. Slackに通知
 * 4. 毎日自動実行（トリガー）
 */

// 設定
const CONFIG = {
  SPREADSHEET_ID: 'YOUR_SPREADSHEET_ID',
  SHEET_NAME: 'タスク一覧',
  SLACK_WEBHOOK: PropertiesService.getScriptProperties().getProperty('SLACK_WEBHOOK'),
  NOTIFY_EMAIL: 'notify@example.com'
};

/**
 * メイン関数 - 毎日実行
 */
function dailyTaskCheck() {
  const tasks = getUncompletedTasks();
  
  if (tasks.length > 0) {
    // メール通知
    sendEmailNotification(tasks);
    
    // Slack通知
    sendSlackNotification(tasks);
    
    // 実行ログ
    logExecution(tasks.length);
  }
}

/**
 * スプレッドシートから未完了タスクを取得
 */
function getUncompletedTasks() {
  const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
  const sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  const data = sheet.getDataRange().getValues();
  
  const tasks = [];
  const headers = data[0];
  const statusCol = headers.indexOf('ステータス');
  const titleCol = headers.indexOf('タスク名');
  const deadlineCol = headers.indexOf('期限');
  const assigneeCol = headers.indexOf('担当者');
  
  for (let i = 1; i < data.length; i++) {
    if (data[i][statusCol] !== '完了') {
      tasks.push({
        title: data[i][titleCol],
        deadline: data[i][deadlineCol],
        assignee: data[i][assigneeCol],
        status: data[i][statusCol]
      });
    }
  }
  
  return tasks;
}

/**
 * メール通知を送信
 */
function sendEmailNotification(tasks) {
  const subject = `【タスクリマインダー】未完了タスク: ${tasks.length}件`;
  
  let body = '以下のタスクが未完了です:\n\n';
  tasks.forEach((task, i) => {
    body += `${i + 1}. ${task.title}\n`;
    body += `   担当: ${task.assignee}\n`;
    body += `   期限: ${formatDate(task.deadline)}\n\n`;
  });
  
  body += '\nスプレッドシート: https://docs.google.com/spreadsheets/d/' + CONFIG.SPREADSHEET_ID;
  
  GmailApp.sendEmail(CONFIG.NOTIFY_EMAIL, subject, body);
  Logger.log('メール送信完了: ' + CONFIG.NOTIFY_EMAIL);
}

/**
 * Slack通知を送信
 */
function sendSlackNotification(tasks) {
  if (!CONFIG.SLACK_WEBHOOK) {
    Logger.log('Slack Webhook未設定');
    return;
  }
  
  const blocks = [
    {
      type: 'header',
      text: {
        type: 'plain_text',
        text: `📋 未完了タスク: ${tasks.length}件`,
        emoji: true
      }
    },
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: tasks.map((t, i) => 
          `${i + 1}. *${t.title}* (${t.assignee}) - ${formatDate(t.deadline)}`
        ).join('\n')
      }
    }
  ];
  
  const payload = {
    blocks: blocks
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };
  
  UrlFetchApp.fetch(CONFIG.SLACK_WEBHOOK, options);
  Logger.log('Slack通知送信完了');
}

/**
 * 日付フォーマット
 */
function formatDate(date) {
  if (!date) return '未設定';
  if (typeof date === 'string') return date;
  return Utilities.formatDate(date, 'Asia/Tokyo', 'yyyy/MM/dd');
}

/**
 * 実行ログを記録
 */
function logExecution(taskCount) {
  const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
  let logSheet = ss.getSheetByName('実行ログ');
  
  if (!logSheet) {
    logSheet = ss.insertSheet('実行ログ');
    logSheet.appendRow(['実行日時', 'タスク数', 'ステータス']);
  }
  
  logSheet.appendRow([new Date(), taskCount, '成功']);
}

/**
 * トリガーを設定
 */
function createDailyTrigger() {
  // 既存のトリガーを削除
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'dailyTaskCheck') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // 毎日午前9時に実行
  ScriptApp.newTrigger('dailyTaskCheck')
    .timeBased()
    .atHour(9)
    .everyDays(1)
    .inTimezone('Asia/Tokyo')
    .create();
  
  Logger.log('トリガー設定完了: 毎日09:00 JST');
}

/**
 * 手動テスト用
 */
function testRun() {
  dailyTaskCheck();
}
```

## appsscript.json

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

## .clasp.json

```json
{
  "scriptId": "YOUR_SCRIPT_ID",
  "rootDir": "./src",
  "fileExtension": "gs"
}
```

## トリガー種類

| トリガー | 説明 | 使用例 |
|---------|------|--------|
| `timeBased` | 時間ベース | 毎日9時に実行 |
| `onOpen` | スプレッドシート開時 | メニュー追加 |
| `onEdit` | セル編集時 | 自動計算 |
| `onFormSubmit` | フォーム送信時 | 回答処理 |
| `onChange` | 構造変更時 | バックアップ |

## チェックリスト

- [ ] Claspがインストールされている
- [ ] GASプロジェクトが作成されている
- [ ] 必要なOAuthスコープが設定されている
- [ ] スクリプトプロパティが設定されている
- [ ] トリガーが正しく設定されている
- [ ] テスト実行が成功する

## 関連レッスン

- `/start-8-1`: GAS基礎・Clasp設定
- `/start-8-2`: スプレッドシート連携
- `/start-8-3`: トリガー・通知設定

## 参考リンク

- [Apps Script Documentation](https://developers.google.com/apps-script)
- [Clasp GitHub](https://github.com/google/clasp)
- [SpreadsheetApp Reference](https://developers.google.com/apps-script/reference/spreadsheet)
