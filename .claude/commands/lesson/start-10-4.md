---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "約25分"
prerequisites: ["start-10-1"]
level: "intermediate"
tags: ["gas", "gmail", "sheets", "automation", "clasp"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 10-4: GmailAppメール検索・抽出→シート整理

## 📍 このセッションでやること

**Lesson 10-4: GmailAppメール検索・抽出→シート整理** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | GAS の GmailApp でメールを検索・抽出し、スプレッドシートに自動整理する |
| 所要時間 | 約25分 |
| 使うスキル | GAS (GmailApp, SpreadsheetApp), clasp |
| 前提条件 | Lesson 10-1 完了（clasp 認証済み） |

**このセッションの流れ:**
1. appsscript.json に Gmail スコープ追加
2. GmailApp.search() でメール検索
3. スレッド/メッセージから情報を抽出
4. SpreadsheetApp でシートにデータ書き込み
5. 定期実行トリガーの設定

セッション終了時には、メールを自動で検索・抽出し、スプレッドシートに整理するGASスクリプトが完成しています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。

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
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → Lesson 10-1 完了確認。`clasp login --status` で認証状態確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: appsscript.json に Gmail スコープ追加

```json
{
  "title": "🚀 Step 1: Gmail スコープ追加",
  "questions": [{
    "id": "step_action",
    "prompt": "appsscript.json に Gmail の読み取りスコープを追加します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "現在の appsscript.json を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`gas-example/appsscript.json` の `oauthScopes` に以下を追加:

```json
{
  "timeZone": "Asia/Tokyo",
  "dependencies": {},
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.scriptapp"
  ]
}
```

追加後、`clasp push` でデプロイ:

```bash
cd gas-example && npx -y @google/clasp push
```

**期待される結果**: `appsscript.json` に `gmail.readonly` スコープが追加され、push が成功する。

---

## 🚀 Step 2: GmailApp.search() でメール検索

```json
{
  "title": "🚀 Step 2: メール検索",
  "questions": [{
    "id": "step_action",
    "prompt": "GmailApp.search() を使ってメールを検索する関数を作成します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "Gmail検索クエリ構文を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`gas-example/Gmail.gs` に `searchEmails` 関数を作成:

```javascript
function searchEmails(query, maxResults) {
  query = query || "is:unread newer_than:7d";
  maxResults = maxResults || 50;
  var threads = GmailApp.search(query, 0, maxResults);
  Logger.log("検索結果: " + threads.length + " スレッド");
  return threads;
}
```

**Gmail 検索クエリの例:**

| クエリ | 意味 |
|--------|------|
| `is:unread` | 未読メール |
| `newer_than:7d` | 過去7日以内 |
| `from:example@company.com` | 特定の送信者 |
| `subject:会議` | 件名に「会議」を含む |
| `has:attachment` | 添付ファイル付き |
| `is:unread newer_than:3d` | 複合条件 |

`clasp push` → `clasp open` で GAS エディタを開き、`searchEmails` を実行してログを確認。

**期待される結果**: 検索結果のスレッド数がログに表示される。

---

## 🚀 Step 3: メール情報の抽出

```json
{
  "title": "🚀 Step 3: メール情報抽出",
  "questions": [{
    "id": "step_action",
    "prompt": "スレッドからメール情報（送信者・件名・日時・本文）を抽出します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "GmailMessage の API を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`extractEmailData` 関数を追加:

```javascript
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
```

**主要メソッド:**

| メソッド | 取得内容 |
|---------|---------|
| `getSubject()` | 件名 |
| `getFrom()` | 送信者 |
| `getDate()` | 日時 |
| `getPlainBody()` | 本文（テキスト） |
| `isUnread()` | 未読かどうか |
| `getMessages().length` | スレッド内メッセージ数 |

**期待される結果**: メール情報がオブジェクト配列として抽出される。

---

## 🚀 Step 4: スプレッドシートにデータ書き込み

```json
{
  "title": "🚀 Step 4: シートに書き込み",
  "questions": [{
    "id": "step_action",
    "prompt": "抽出したメールデータをスプレッドシートに書き込みます。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "SpreadsheetApp の API を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

`writeToSheet` 関数と、メイン関数 `extractAndOrganizeEmails` を追加:

```javascript
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
        item.subject, item.from,
        Utilities.formatDate(item.date, "Asia/Tokyo", "yyyy-MM-dd HH:mm"),
        item.body, item.isUnread ? "未読" : "既読", item.messageCount
      ];
    });
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }

  Logger.log("シート作成完了: " + ss.getUrl());
  return ss.getUrl();
}

function extractAndOrganizeEmails() {
  var threads = searchEmails("is:unread newer_than:7d", 50);
  var data = extractEmailData(threads);
  var url = writeToSheet(data);
  Logger.log("処理完了: " + data.length + " 件のメールをシートに整理しました");
}
```

`clasp push` → `clasp open` で `extractAndOrganizeEmails` を実行。

**期待される結果**: Google Drive に「メール一覧_YYYY-MM-DD」という名前のスプレッドシートが作成され、メール情報が整理されている。

---

## 🚀 Step 5: 定期実行トリガーの設定

```json
{
  "title": "🚀 Step 5: トリガー設定",
  "questions": [{
    "id": "step_action",
    "prompt": "毎日9時にメール整理を自動実行するトリガーを設定します。",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "ScriptApp.newTrigger の仕様を確認"},
      {"id": "skip", "label": "スキップ"}
    ]
  }]
}
```

**選択後の案内（例）**:

```javascript
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
```

`clasp push` → `clasp open` で `setEmailExtractTrigger` を実行。

**期待される結果**: GAS エディタの「トリガー」画面に、毎日9時の時間主導型トリガーが表示される。

---

## ⚠️ よくあるトラブルと解決方法

```json
{
  "title": "⚠️ トラブルシューティング",
  "questions": [{
    "id": "trouble",
    "prompt": "問題が発生しましたか？",
    "options": [
      {"id": "trouble_1", "label": "Gmail の権限エラー"},
      {"id": "trouble_2", "label": "スプレッドシートが作成されない"},
      {"id": "trouble_3", "label": "日本語が文字化けする"},
      {"id": "trouble_4", "label": "トリガーが動作しない"}
    ]
  }]
}
```

### トラブル1: 「Gmail の権限エラー」
**原因**: `appsscript.json` に `gmail.readonly` スコープが追加されていない、または初回実行時の承認が完了していない。
**解決プロンプト**:
```text
appsscript.json の oauthScopes に "https://www.googleapis.com/auth/gmail.readonly" が含まれているか確認してください。含まれていなければ追加して clasp push してください。初回実行時はGASエディタで関数を実行し、権限の承認ダイアログを完了してください。
```

### トラブル2: 「スプレッドシートが作成されない」
**原因**: `spreadsheets` スコープが不足、またはメール検索結果が0件。
**解決プロンプト**:
```text
oauthScopes に "https://www.googleapis.com/auth/spreadsheets" があるか確認してください。また searchEmails の検索クエリを "newer_than:30d" など範囲を広げて再実行してみてください。
```

### トラブル3: 「日本語が文字化けする」
**原因**: `getPlainBody()` のエンコーディング問題。
**解決プロンプト**:
```text
getPlainBody() の代わりに getBody() を使い、HTML タグを除去するヘルパー関数を追加してみてください。
```

### トラブル4: 「トリガーが動作しない」
**原因**: トリガーの権限が不足、またはスクリプトにエラーがある。
**解決プロンプト**:
```text
GAS エディタの「実行数」画面でエラーログを確認してください。また ScriptApp のスコープが appsscript.json に含まれているか確認してください。
```

---

## ✅ チェックポイント

- [ ] `appsscript.json` に Gmail スコープが追加されている
- [ ] `searchEmails` 関数でメール検索ができる
- [ ] `extractEmailData` 関数で送信者・件名・日時・本文が抽出できる
- [ ] `extractAndOrganizeEmails` でスプレッドシートが生成される
- [ ] 定期実行トリガーが設定されている

---

## 📋 成果物プレビュー

**作成されるファイル:**
```text
gas-example/
├── appsscript.json   # Gmail スコープ追加済み
├── Calendar.gs       # Lesson 10-2 の成果物
├── Sheets.gs         # Lesson 10-3 の成果物
└── Gmail.gs          # 今回の成果物（5関数）
```

**生成されるスプレッドシート:**

| 件名 | 送信者 | 日時 | 本文（先頭200文字） | 未読 | メッセージ数 |
|------|--------|------|---------------------|------|-------------|
| 週次レポート | alice@co.com | 2026-04-14 10:30 | お疲れ様です。今週の... | 未読 | 3 |
| ミーティング議事録 | bob@co.com | 2026-04-13 15:00 | 本日のミーティング... | 既読 | 1 |

---

## ➡️ 次のステップ

```json
{
  "title": "➡️ 次のステップ",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_auto", "label": "Module 11（GitHub Actions）に進む → /start-11-1"},
      {"id": "review_module", "label": "Module 10 の成果物を確認したい"},
      {"id": "finish", "label": "今日はここまで"}
    ]
  }]
}
```
