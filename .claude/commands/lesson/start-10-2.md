---
description: "When the user says /start-10-2 — Module 10 Lesson 10-2: Google Calendar API連携・イベント自動化"
chapter: "courses/aiagent/lesson03-core/module10-gas"
prerequisites: ["start-10-1"]
duration: "約30分"
level: "intermediate"
tags: ["gas", "calendar", "google", "automation"]
---

# 🎓 Lesson 10-2: Google Calendar API連携・イベント自動化

## 📍 このセッションでやること

**Lesson 10-2: GASとGoogle Calendar連携** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GASからGoogle Calendar APIでイベント操作を自動化する |
| 所要時間 | 約30分 |
| 使うスキル | gas-clasp-ops, Google Calendar API, gogcli |
| 前提条件 | Lesson 10-1 完了、GASプロジェクト作成済み、Apps Script API 有効化済み |
| 教材ページ | [Module 10: GAS](https://ai-agent.camp/ja/course/module-10) を並行参照 |

**このセッションの流れ:**
1. カレンダー取得スクリプトの作成
2. イベントの作成・更新・削除
3. トリガーと通知の設定

セッション終了時には、カレンダー連携の自動化ができるようになっています。

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

## 🚀 Step 1: カレンダー取得スクリプト

**前提条件チェック（自動実行）:**
以下を確認してから進めてください：

1. **`.clasp.json` の存在確認**: `gas-example/.clasp.json` が存在するか確認。存在しない場合は 4-1 を先に完了してください。
2. **Apps Script API の有効化確認**: https://script.google.com/home/usersettings で「Google Apps Script API」が ON になっているか確認。
3. **`appsscript.json` の oauthScopes 設定**: Calendar API を使うため、`gas-example/appsscript.json` に以下のスコープを追加してください：

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

> **重要**: oauthScopes を設定しないと、Calendar API の呼び出し時に「Permission denied」エラーが発生します。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: カレンダー取得スクリプト",
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
gas-example ディレクトリに Calendar.gs ファイルを作成し、以下の内容を記述してください：

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

clasp push で同期してください。
```

**期待される結果**: Calendar.gs がGoogleドライブに同期され、カレンダー一覧を取得できます。

---

## 🚀 Step 2: イベント作成機能

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: イベント作成機能",
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
Calendar.gs に以下のイベント作成関数を追加してください：

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

clasp push して、GASエディタで createTomorrowEvent を実行してください。
```

**期待される結果**: 明日14:00から1時間の「テストイベント」がカレンダーに追加されます。

---

## 🚀 Step 3: イベント一覧取得

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: イベント一覧取得",
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
Calendar.gs に以下のイベント取得関数を追加してください：

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

clasp push して実行してください。
```

**期待される結果**: 今日のカレンダーイベント一覧がログに表示されます。

---

## 🚀 Step 4: 定期実行トリガー設定

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 定期実行トリガー設定",
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
Calendar.gs に以下のトリガー設定関数を追加してください：

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

clasp push して、createDailyTrigger を実行してください。
```

**期待される結果**: 毎日9時に自動実行されるトリガーが設定されます。

---

## 🚀 Step 5: gogcli × GAS 連携 — カレンダーデータの取得と転記

> **📝 ポイント**: 4-1 で設定した gogcli を使って、ローカルでカレンダーデータを取得し、GAS でスプレッドシートに自動転記するワークフローを体験します。gogcli（ローカル CLI）と GAS（クラウド実行）を組み合わせることで、柔軟なデータパイプラインを構築できます。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: gogcli × GAS 連携",
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
gogcli と GAS を連携させて、カレンダー情報をスプレッドシートに自動転記します。

### Step 5-1: gogcli でカレンダーデータを取得

gog calendar list --days 7 --json > ~/ai-agent-camp/gas-example/calendar_data.json

取得した JSON ファイルの内容を確認してください。

### Step 5-2: GAS でカレンダーデータを読み込んでシートに転記

Calendar.gs に以下の関数を追加してください：

function importCalendarDataToSheet() {
  // gogcli で取得した JSON データをスプレッドシートに転記するイメージ
  // 実際にはスプレッドシートに紐づけた GAS から CalendarApp で直接取得する方法と、
  // gogcli の出力を手動/自動でシートに貼り付ける方法の2パターンがある

  const calendar = CalendarApp.getDefaultCalendar();
  const now = new Date();
  const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  const events = calendar.getEvents(now, weekLater);

  // スプレッドシートに書き込み
  const ss = SpreadsheetApp.create("カレンダー週次レポート");
  const sheet = ss.getActiveSheet();

  // ヘッダー
  sheet.getRange("A1:E1").setValues([["タイトル", "開始日時", "終了日時", "場所", "説明"]]);

  // イベントデータ
  const data = events.map(event => [
    event.getTitle(),
    event.getStartTime().toLocaleString("ja-JP"),
    event.getEndTime().toLocaleString("ja-JP"),
    event.getLocation() || "",
    event.getDescription() || ""
  ]);

  if (data.length > 0) {
    sheet.getRange(2, 1, data.length, 5).setValues(data);
  }

  Logger.log("カレンダーデータ転記完了: " + data.length + "件");
  Logger.log("スプレッドシートURL: " + ss.getUrl());
  return ss.getUrl();
}

clasp push して、GASエディタで importCalendarDataToSheet を実行してください。
```

**期待される結果**: gogcli でローカルにカレンダー JSON を取得でき、GAS 側でも同じカレンダーデータをスプレッドシートに転記できます。

**💡 実践演習: gogcliで取得したカレンダー情報をGASでスプレッドシートに自動転記**

以下のワークフローを実践してみましょう:
1. `gog calendar list --days 7 --json` で今週の予定を取得
2. 出力された JSON の構造を確認（タイトル、日時、場所など）
3. GAS の `importCalendarDataToSheet()` を実行して同じデータをスプレッドシートに転記
4. gogcli の出力と GAS の出力を比較し、データの一致を確認

> **ヒント**: gogcli はローカル CLI なので CI/CD やスクリプトとの連携が容易です。一方 GAS はクラウド上で定期実行（トリガー）できます。両者を組み合わせることで、ローカル確認 → クラウド自動化の開発フローが実現できます。

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
      {"id": "trouble_1", "label": "Calendar not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Event not found"},
      {"id": "trouble_4", "label": "トリガーが動作しない"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"},
      {"id": "trouble_6", "label": "gogcli の認証エラー（gog calendar list が失敗）"}
    ]
  }]
}
```


### トラブル1: 「Calendar not found」
**原因**: カレンダーIDが無効、またはアクセス権限がない
**解決プロンプト**:
```
getAllCalendars() を実行して、アクセス可能なカレンダーの一覧を確認してください。
カレンダーIDが正しいか確認してください。
```

### トラブル2: 「Permission denied」
**原因**: Calendar APIの権限が付与されていない
**解決プロンプト**:
```
GASエディタで「サービス」からGoogle Calendar APIを追加してください。
appsscript.json に oauthScopes を追加する方法も教えてください。
```

### トラブル3: 「Event not found」
**原因**: イベントIDが存在しない、または削除されている
**解決プロンプト**:
```
getEventById の前に null チェックを追加して、イベントが存在しない場合のエラーハンドリングを実装してください。
```

### トラブル4: トリガーが動作しない
**原因**: トリガーの実行権限がない
**解決プロンプト**:
```
GASエディタで「トリガー」メニューからトリガーの状態を確認してください。
エラーログがあれば内容を教えてください。
```

### トラブル5: 「Apps Script API has not been used in project / User has not enabled the Apps Script API」
**原因**: Google Apps Script API が無効になっている
**解決手順**:
1. https://script.google.com/home/usersettings にアクセス
2. 「Google Apps Script API」のトグルを **ON** に切り替える
3. 変更後、`clasp login` からやり直す

> この設定はGoogleアカウント単位です。一度有効にすれば、以降のすべてのGASプロジェクトで使えます。

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
- [ ] カレンダー取得ができている
- [ ] イベント作成ができている
- [ ] イベント一覧取得ができている
- [ ] トリガーが設定されている
- [ ] 定期実行が動作する
- [ ] gogcli でカレンダーデータが取得できる（`gog calendar list --days 7 --json`）
- [ ] GAS でカレンダーデータをスプレッドシートに転記できる


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
# 完了確認: 以下を確認してください。
# 1. gas-example/Calendar.gs が存在するか
# 2. appsscript.json に oauthScopes（calendar, script.external_request）が設定されているか
# 3. clasp push が成功するか（gas-example ディレクトリで実行）
# 4. GASエディタで getDefaultCalendar() を実行してカレンダー名が表示されるか
# 5. createTomorrowEvent() でカレンダーにイベントが作成されるか
```

**期待される結果**: すべてのチェック項目がパスし、GASからGoogle Calendar APIを使ったイベント操作ができる状態です。

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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-10-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-10-3
- finish → 終了
