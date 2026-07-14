---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約30分"
prerequisites: ["start-4-3"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar", "event-management"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-4: Google Calendar 予定登録・管理

## 📍 このセッションでやること

**Lesson 4-4: Google Calendar 予定登録・管理** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでカレンダーイベントの作成・参加者管理・繰り返し設定・削除を行う |
| 所要時間 | 約30分 |
| 使うスキル | gogcli calendar create / delete |
| 前提条件 | Google Calendar操作の基礎（start-4-3完了） |

**このセッションの流れ:**
1. シンプルなイベントを作成する
2. 参加者付き・Google Meet付きイベントを作成する
3. 定期予定（繰り返しルール）を設定する
4. イベントの削除・管理を行う
5. 実践演習: 1週間のスケジュールを一括登録する

セッション終了時には、gogcliを使ってカレンダーイベントの作成・管理が自在にできるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。ツールによって応答が途中で止まることがありますが、故障ではありません。

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
(check_prereq → `gog auth list` で認証状態を確認、start-4-3の完了を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: シンプルなイベント作成

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: シンプルなイベント作成",
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

基本的なイベントを作成してみましょう:

```bash
# シンプルなイベント作成（タイトル・開始・終了のみ）
gog calendar create primary --account your-email@gmail.com \
  --summary "AI勉強会" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00"

# 説明と場所を追加したイベント作成
gog calendar create primary --account your-email@gmail.com \
  --summary "AI勉強会" \
  --from "2026-03-20T14:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --description "Claude Code活用方法の勉強会。資料は事前共有済み。" \
  --location "会議室B"
```

**期待される結果**: イベントが作成され、Google Calendarに反映されます。イベントIDが返されます。

> **⚠️ 注意**: 日時はRFC3339形式（`YYYY-MM-DDTHH:MM:SS+09:00`）で指定してください。タイムゾーンオフセット（例: `+09:00`）を必ず含めてください。

---

## 🚀 Step 2: 参加者付き・Google Meet付きイベント

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 参加者付き・Google Meet付きイベント",
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

参加者を招待し、Google Meetリンクも自動生成するイベントを作成します:

```bash
# 参加者付き・Google Meet付きイベント
gog calendar create primary --account your-email@gmail.com \
  --summary "チームミーティング" \
  --from "2026-03-20T10:00:00+09:00" \
  --to "2026-03-20T11:00:00+09:00" \
  --attendees "colleague@company.com" \
  --with-meet

# 複数参加者をカンマ区切りで指定
gog calendar create primary --account your-email@gmail.com \
  --summary "プロジェクトキックオフ" \
  --from "2026-03-21T13:00:00+09:00" \
  --to "2026-03-21T14:30:00+09:00" \
  --attendees "member1@company.com,member2@company.com,member3@company.com" \
  --with-meet \
  --description "新プロジェクトのキックオフミーティング" \
  --location "オンライン"

# 公開設定・通知オプション付き
gog calendar create primary --account your-email@gmail.com \
  --summary "全体共有会" \
  --from "2026-03-22T15:00:00+09:00" \
  --to "2026-03-22T16:00:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --visibility public \
  --send-updates all
```

**期待される結果**: イベントが作成され、参加者に招待メールが送信されます。Google Meetリンクも自動生成されます。

> **💡 ヒント**: `--send-updates` オプションで招待通知の送信先を制御できます（`all`=全員、`externalOnly`=外部のみ、`none`=通知なし）。

---

## 🚀 Step 3: 定期予定（繰り返しルール）

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 定期予定（繰り返しルール）",
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

`--rrule` オプションで繰り返しルール（RFC 5545 RRULE）を指定できます:

```bash
# 毎週月曜に繰り返す定例（12回分）
gog calendar create primary --account your-email@gmail.com \
  --summary "週次定例" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T11:00:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"

# 毎月第1月曜に繰り返す月次レビュー（6回分）
gog calendar create primary --account your-email@gmail.com \
  --summary "月次レビュー" \
  --from "2026-04-06T14:00:00+09:00" \
  --to "2026-04-06T15:30:00+09:00" \
  --rrule "RRULE:FREQ=MONTHLY;BYDAY=1MO;COUNT=6" \
  --attendees "manager@company.com" \
  --with-meet

# 終日イベント（--all-day オプション）
gog calendar create primary --account your-email@gmail.com \
  --summary "チーム合宿" \
  --from "2026-04-10" \
  --to "2026-04-11" \
  --all-day \
  --description "Q2チーム合宿（1泊2日）"
```

**よく使うRRULEパターン:**

| パターン | RRULE | 説明 |
|---------|-------|------|
| 毎週月曜 | `FREQ=WEEKLY;BYDAY=MO;COUNT=12` | 12週分 |
| 毎週火木 | `FREQ=WEEKLY;BYDAY=TU,TH;COUNT=24` | 12週分（週2回） |
| 毎月1日 | `FREQ=MONTHLY;BYMONTHDAY=1;COUNT=6` | 6ヶ月分 |
| 毎月第2水曜 | `FREQ=MONTHLY;BYDAY=2WE;COUNT=6` | 6ヶ月分 |
| 毎日（平日のみ） | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=20` | 4週分 |

> **💡 ヒント**: `COUNT` で繰り返し回数を、`UNTIL` で終了日を指定できます。`COUNT` を省略すると無限に繰り返されるので注意してください。

---

## 🚀 Step 4: イベント削除・管理

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: イベント削除・管理",
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

作成したイベントの管理・削除を行います:

```bash
# イベントの削除（eventIdはcreate時に返されたもの）
gog calendar delete primary <eventId> --account your-email@gmail.com --force

# イベント一覧からIDを確認して削除
gog calendar list --account your-email@gmail.com --days 7
# 上記で表示されたイベントIDを使って削除
```

**イベント作成時の便利なオプション:**

```bash
# イベントの色を指定（1-11の数値）
gog calendar create primary --account your-email@gmail.com \
  --summary "重要タスク" \
  --from "2026-03-20T09:00:00+09:00" \
  --to "2026-03-20T10:00:00+09:00" \
  --event-color 11

# フォーカスタイム（集中作業時間）
gog calendar create primary --account your-email@gmail.com \
  --summary "集中作業" \
  --from "2026-03-20T13:00:00+09:00" \
  --to "2026-03-20T15:00:00+09:00" \
  --event-type focus-time

# 不在設定（Out of Office）
gog calendar create primary --account your-email@gmail.com \
  --summary "休暇" \
  --from "2026-03-25T00:00:00+09:00" \
  --to "2026-03-26T00:00:00+09:00" \
  --event-type out-of-office
```

**イベントカラー番号の対応:**

| 番号 | 色 | 用途例 |
|------|-----|-------|
| 1 | ラベンダー | 個人 |
| 2 | セージ | 学習 |
| 4 | フラミンゴ | 重要 |
| 5 | バナナ | 注意 |
| 9 | ブルーベリー | 会議 |
| 11 | トマト | 緊急 |

> **💡 ヒント**: `--force` フラグを付けると確認なしで削除されます。繰り返しイベントを削除すると、シリーズ全体が削除される点に注意してください。

---

## 🚀 Step 5: 実践演習（1週間のスケジュールを一括登録）

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 実践演習",
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

これまで学んだ機能を組み合わせて、1週間分のスケジュールを一括登録してみましょう。以下のプロンプトをCursorに入力してください:

```text
gog calendar create コマンドを使って、以下の1週間分のスケジュールを作成してください:

1. 毎朝 9:00-9:15「朝会スタンドアップ」（月-金、--with-meet付き、--rrule使用）
2. 月曜 10:00-12:00「フォーカスタイム」（--event-type focus-time）
3. 火曜 14:00-15:00「1on1ミーティング」（参加者: manager@company.com、--with-meet付き）
4. 水曜 15:00-16:00「チーム勉強会」（--description "AI活用の事例共有"、--event-color 2）
5. 金曜 17:00-17:30「週次振り返り」（--attendees "team@company.com"、--with-meet付き）

アカウント: your-email@gmail.com
開始日: 来週月曜
各イベントに適切なdescriptionも追加してください。
```

**AIが生成するコマンド例:**
```bash
# 1. 朝会スタンドアップ（繰り返し）
gog calendar create primary --account your-email@gmail.com \
  --summary "朝会スタンドアップ" \
  --from "2026-03-23T09:00:00+09:00" \
  --to "2026-03-23T09:15:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=5" \
  --with-meet \
  --description "毎朝の進捗共有（15分）"

# 2. フォーカスタイム
gog calendar create primary --account your-email@gmail.com \
  --summary "フォーカスタイム" \
  --from "2026-03-23T10:00:00+09:00" \
  --to "2026-03-23T12:00:00+09:00" \
  --event-type focus-time \
  --description "集中作業時間。Slackは非通知に設定。"

# 3. 1on1ミーティング
gog calendar create primary --account your-email@gmail.com \
  --summary "1on1ミーティング" \
  --from "2026-03-24T14:00:00+09:00" \
  --to "2026-03-24T15:00:00+09:00" \
  --attendees "manager@company.com" \
  --with-meet \
  --description "マネージャーとの1on1"

# 4. チーム勉強会
gog calendar create primary --account your-email@gmail.com \
  --summary "チーム勉強会" \
  --from "2026-03-25T15:00:00+09:00" \
  --to "2026-03-25T16:00:00+09:00" \
  --event-color 2 \
  --description "AI活用の事例共有"

# 5. 週次振り返り
gog calendar create primary --account your-email@gmail.com \
  --summary "週次振り返り" \
  --from "2026-03-27T17:00:00+09:00" \
  --to "2026-03-27T17:30:00+09:00" \
  --attendees "team@company.com" \
  --with-meet \
  --description "今週の成果と来週の計画を共有"
```

**期待される結果**: 5種類のイベントがカレンダーに登録されます。Google Calendarで確認してみましょう。

> **💡 ヒント**: AIに依頼することで、複雑なスケジュール設定も簡単に自動化できます。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "イベントが作成されない"},
      {"id": "trouble_2", "label": "参加者に通知が届かない"},
      {"id": "trouble_3", "label": "繰り返しルールが正しく動かない"},
      {"id": "trouble_4", "label": "Google Meetリンクが生成されない"}
    ]
  }]
}
```

### トラブル1: イベントが作成されない
**原因**: calendarIdの指定ミス、または日時フォーマットの誤り
**解決プロンプト**:
```text
calendarIdが正しいか確認してください（通常は "primary"）。
日時はRFC3339形式（"YYYY-MM-DDTHH:MM:SS+09:00"）で指定してください。
gog calendar calendars --account your-email@gmail.com でカレンダーIDを確認できます。
```

### トラブル2: 参加者に通知が届かない
**原因**: --send-updates オプションが未指定
**解決プロンプト**:
```text
--send-updates all を追加してください。
デフォルトでは通知が送信されない場合があります。
例: gog calendar create primary --account ... --attendees "..." --send-updates all
```

### トラブル3: 繰り返しルールが正しく動かない
**原因**: RRULE構文の誤り
**解決プロンプト**:
```text
RRULEの構文を確認してください:
- "RRULE:" プレフィックスが必要です
- FREQ は必須（WEEKLY, MONTHLY, DAILY など）
- BYDAY の曜日は2文字（MO, TU, WE, TH, FR, SA, SU）
- COUNT または UNTIL で終了条件を指定してください
正しい例: "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"
```

### トラブル4: Google Meetリンクが生成されない
**原因**: --with-meet フラグの未指定
**解決プロンプト**:
```text
--with-meet フラグを追加してください。
例: gog calendar create primary --account ... --summary "会議" --with-meet
Google Workspace アカウントでない場合、Meet生成に制限がある場合があります。
```

---

## ✅ チェックポイント
- [ ] シンプルなイベント作成成功
- [ ] 参加者付き・Meet付きイベント作成成功
- [ ] 定期予定の設定成功
- [ ] イベント削除成功
- [ ] 1週間分のスケジュール一括登録完了


---

## 📋 成果物プレビュー

このレッスンの成果物はターミナル出力です。

### 期待される出力例
```text
┌─────────────────────────────────────┐
│  コマンド実行結果                      │
│  ステータス: ✅ 成功                   │
│  処理件数: N件                        │
└─────────────────────────────────────┘
```

> 💡 出力をファイルに保存するには、コマンド末尾に ` > output/result.txt` を追加

---

## ✅ 完了チェック
以下をCodexのチャットに入力して、完了状況を確認してください:

```text
以下のコマンドを実行して、Calendar予定登録・管理が正しく動作するか確認してください:
1. gog calendar list --account <メールアドレス> --days 7
2. 上記の結果にこのレッスンで作成したイベントが含まれているか確認
3. 繰り返しイベントが正しく設定されているか確認
すべて正常に動作するか確認してください。
```

**期待される結果**: 作成したイベント（シンプル・参加者付き・繰り返し・フォーカスタイム等）が一覧に表示されます。

---

## 🎉 次のステップ

これでGoogle Calendar 予定登録・管理は完了です！次のレッスンではGoogle Drive操作を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-5）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-5）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-5（Google Drive操作）
- next_window → 新しいウィンドウで /start-4-5
- finish → 終了
