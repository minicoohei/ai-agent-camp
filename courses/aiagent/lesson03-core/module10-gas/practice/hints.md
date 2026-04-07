# ヒント: GAS 自動化

## clasp CLI の基本操作

### インストールとログイン
```bash
# インストール
npm install -g @google/clasp

# Google アカウントでログイン
clasp login

# ログイン確認
clasp login --status
```

### プロジェクト操作
```bash
# 新規プロジェクト作成（Sheets紐付き）
clasp create --type sheets --title "勤怠管理"

# 既存プロジェクトをクローン
clasp clone <scriptId>

# ローカル → GAS にプッシュ
clasp push

# GAS → ローカルにプル
clasp pull

# ブラウザでエディタを開く
clasp open

# ログ確認
clasp logs
```

### .clasp.json の構成
```json
{
  "scriptId": "xxxxx",
  "rootDir": "."
}
```

## GAS デバッグ方法

### Logger.log を使う
```javascript
function debug() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('勤怠データ');
  const data = sheet.getDataRange().getValues();
  Logger.log('行数: ' + data.length);
  Logger.log('最初の行: ' + JSON.stringify(data[0]));
}
```

### console.log を使う（Stackdriver Logging）
```javascript
function debug2() {
  console.log('デバッグ情報');
  console.info('情報メッセージ');
  console.warn('警告メッセージ');
  console.error('エラーメッセージ');
}
```

### 実行ログの確認方法
1. GAS エディタ → 「実行」メニュー → 実行ログ
2. clasp logs で確認
3. Google Cloud Console → Logging

## Google Sheets 操作のコツ

### 基本的なデータ読み書き
```javascript
// シート取得
const ss = SpreadsheetApp.getActiveSpreadsheet();
const sheet = ss.getSheetByName('シート名');

// 全データ取得（2次元配列）
const data = sheet.getDataRange().getValues();

// 特定範囲の取得
const range = sheet.getRange('A2:E31');
const values = range.getValues();

// データ書き込み
sheet.getRange('A1').setValue('値');
sheet.getRange('A1:C3').setValues([['a','b','c'], ['d','e','f'], ['g','h','i']]);
```

### 時間計算のコツ
```javascript
// 時間文字列を時間数に変換
function timeToHours(timeStr) {
  const parts = timeStr.split(':');
  return parseInt(parts[0]) + parseInt(parts[1]) / 60;
}

// 勤務時間の計算
const workHours = timeToHours('18:00') - timeToHours('09:00'); // = 9.0
```

## Google Calendar 操作のコツ

### 予定の取得
```javascript
// デフォルトカレンダーの予定を取得
const calendar = CalendarApp.getDefaultCalendar();
const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(today.getDate() + 1);

// 翌日の開始・終了を設定
const start = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 0, 0, 0);
const end = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 23, 59, 59);

const events = calendar.getEvents(start, end);
```

### イベント情報の取得
```javascript
events.forEach(event => {
  Logger.log('タイトル: ' + event.getTitle());
  Logger.log('開始: ' + event.getStartTime());
  Logger.log('終了: ' + event.getEndTime());
  Logger.log('場所: ' + event.getLocation());
  Logger.log('説明: ' + event.getDescription());
});
```

## Slack Webhook のコツ

### Webhook URL の取得方法
1. https://api.slack.com/apps にアクセス
2. 「Create New App」→「From scratch」
3. 「Incoming Webhooks」を有効化
4. 「Add New Webhook to Workspace」でチャンネルを選択
5. 生成された URL をコピー

### メッセージ送信
```javascript
function sendSlackMessage(webhookUrl, text) {
  const payload = {
    text: text,
    // リッチ形式を使う場合:
    // blocks: [{ type: 'section', text: { type: 'mrkdwn', text: '*太字*' } }]
  };

  UrlFetchApp.fetch(webhookUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}
```

## トラブルシューティング

| エラー | 原因 | 対処 |
|--------|------|------|
| `clasp: command not found` | clasp未インストール | `npm install -g @google/clasp` |
| `Script API disabled` | API未有効化 | https://script.google.com/home/usersettings で有効化 |
| `Authorization required` | 権限未承認 | GASエディタで一度手動実行して権限を承認 |
| `Cannot read property of null` | シート名が一致しない | `SHEET_NAME` 定数を実際のシート名に合わせる |
| `Exception: Limit Exceeded` | API制限超過 | 処理量を減らすか、バッチ処理に分割 |
