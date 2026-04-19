# module10-gas 完成例

## 概要

Google Apps Script を使った業務自動化の完成例です。勤怠データの集計と、カレンダー予定の Slack 通知という2つの実用的なスクリプトを含みます。

## 成果物一覧

| ファイル | 説明 |
|----------|------|
| `output/sheets-automation.gs` | 勤怠集計スクリプト（集計・メール送信・書式整形） |
| `output/calendar-sync.gs` | カレンダー→Slack 通知スクリプト |
| `output/appsscript.json` | GAS プロジェクトマニフェスト |

## 主な機能

### sheets-automation.gs
- `calculateWorkHours()`: 従業員ごとの月間勤務時間を集計し、集計シートに出力
- `sendSummaryEmail()`: 集計結果を HTML テーブル形式でメール送信
- `formatSheet()`: ヘッダー色設定、列幅自動調整、罫線追加

### calendar-sync.gs
- `getTomorrowEvents()`: 翌日のカレンダー予定を取得
- `formatEventMessage()`: 時刻順にソートし、Slack向けに整形
- `sendToSlack()`: Incoming Webhook で Slack に通知
- `createDailyTrigger()`: 毎日17:00の自動実行トリガー設定

## デプロイ手順

```bash
# 1. clasp でプロジェクト作成
clasp create --type sheets --title "勤怠管理自動化"

# 2. ファイルをコピー
cp output/*.gs .
cp output/appsscript.json .

# 3. プッシュ
clasp push

# 4. ブラウザで確認
clasp open
```

## 使用ツール

- Google Apps Script（clasp によるローカル開発）
- `gas-clasp-ops` スキル

## 学習ポイント

1. **SpreadsheetApp**: シートの読み書き、範囲操作、書式設定
2. **CalendarApp**: カレンダーイベントの取得とパース
3. **UrlFetchApp**: 外部 API（Slack Webhook）への HTTP リクエスト
4. **ScriptApp.newTrigger**: 時間ベースの自動実行設定
5. **GmailApp**: メール送信（HTML形式対応）
