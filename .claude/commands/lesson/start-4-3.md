---
description: "When the user says /start-4-3 — Module 4 Lesson 4-3: Google Calendar操作"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約25分"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "calendar"]
---

# 🎓 Lesson 4-3: Google Calendar操作

## 📍 このセッションでやること

**Lesson 4-3: Google Calendar操作** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでカレンダーイベントの一覧・作成・更新を行う |
| 所要時間 | 約25分 |
| 使うスキル | gogcli calendar |
| 前提条件 | gogcli認証セットアップ済み（start-4-1完了） |

**このセッションの流れ:**
1. 今日・今週のイベントを一覧表示する
2. 新しいイベントを作成する
3. 定例ミーティングの自動セットアップを行う

セッション終了時には、gogcliを使ってカレンダーイベントの閲覧・作成ができるようになっています。

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
(check_prereq → `gog auth list` で認証状態を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: 今日・今週のイベントを一覧表示する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: イベント一覧の表示",
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

カレンダーのイベントを確認してみましょう:

```bash
# 今日のイベント一覧
gog calendar list --account your-email@gmail.com --days 1

# 今週のイベント一覧（7日間）
gog calendar list --account your-email@gmail.com --days 7

# カレンダー一覧の取得（利用可能なカレンダーIDの確認）
gog calendar calendars --account your-email@gmail.com
```

**期待される結果**: イベントのタイトル、開始時刻、終了時刻、場所（設定されている場合）が一覧表示されます。

> **💡 ヒント**: `--days` で指定した日数分の予定が取得されます。デフォルトのカレンダーは `primary` です。

**応用: AIによるスケジュール分析**

取得したイベント一覧をAIに渡して分析してもらいましょう:
```text
上記の今週のスケジュールを分析して:
1. 空き時間のスロットを洗い出してください
2. 会議が集中している日を特定してください
3. 1日あたりの会議時間を計算してください
```

---

## 🚀 Step 2: 新しいイベントを作成する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: イベントの作成",
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

新しいカレンダーイベントを作成します:

```bash
# 基本的なイベント作成
gog calendar create primary --account your-email@gmail.com \
  --summary "AI勉強会" \
  --from "2026-03-15T14:00:00+09:00" \
  --to "2026-03-15T15:00:00+09:00"

# 場所と説明付きのイベント作成
gog calendar create primary --account your-email@gmail.com \
  --summary "チームミーティング" \
  --from "2026-03-16T10:00:00+09:00" \
  --to "2026-03-16T11:00:00+09:00" \
  --location "会議室A" \
  --description "週次進捗共有"
```

**期待される結果**: イベントが作成され、Google Calendarに反映されます。イベントIDが返されます。

> **⚠️ 注意**: 日時はISO 8601形式（`YYYY-MM-DDTHH:MM:SS+09:00`）で指定してください。タイムゾーンオフセット（例: `+09:00`）を含めることを推奨します。

---

## 🚀 Step 3: 定例ミーティングの自動セットアップ

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 定例ミーティングの自動セットアップ",
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

AIを使って複数のイベントを一括で作成してみましょう。以下のプロンプトをCursorに入力してください:

```text
gog calendar create コマンドを使って、以下の定例ミーティングを作成してください:

1. 毎週月曜 10:00-10:30「週次チーム朝会」（来週から4週分）
2. 毎週水曜 14:00-15:00「プロジェクト進捗会議」（来週から4週分）
3. 毎週金曜 17:00-17:30「週次振り返り」（来週から4週分）

アカウント: your-email@gmail.com
各イベントに適切なdescriptionも追加してください。
```

**AIが生成するコマンド例:**
```bash
# 月曜朝会（4週分）
gog calendar create primary --account your-email@gmail.com --summary "週次チーム朝会" --from "2026-03-16T10:00:00+09:00" --to "2026-03-16T10:30:00+09:00" --description "チーム全体の週次キックオフ"
gog calendar create primary --account your-email@gmail.com --summary "週次チーム朝会" --from "2026-03-23T10:00:00+09:00" --to "2026-03-23T10:30:00+09:00" --description "チーム全体の週次キックオフ"
# ... 以下同様
```

**期待される結果**: 12件のイベント（3種類 x 4週）がカレンダーに登録されます。Google Calendarで確認してみましょう。

> **💡 ヒント**: AIに依頼することで、繰り返しの手作業を自動化できます。これがAIアシスタント活用の醍醐味です。

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
      {"id": "trouble_1", "label": "イベントが表示されない"},
      {"id": "trouble_2", "label": "日時フォーマットエラー"},
      {"id": "trouble_3", "label": "カレンダーIDがわからない"},
      {"id": "trouble_4", "label": "作成したイベントが反映されない"}
    ]
  }]
}
```

### トラブル1: イベントが表示されない
**原因**: 対象期間にイベントがない、またはカレンダーIDが異なる
**解決プロンプト**:
```text
--days の値を大きくして試してください（例: --days 30）。
また、gog calendar calendars で利用可能なカレンダー一覧を確認してください。
```

### トラブル2: 日時フォーマットエラー
**原因**: ISO 8601形式になっていない
**解決プロンプト**:
```text
日時は "YYYY-MM-DDTHH:MM:SS+09:00" 形式で指定してください。
例: "2026-03-15T14:00:00+09:00"
日付と時刻の間に "T" を入れ、タイムゾーンオフセットも付けてください。
```

### トラブル3: カレンダーIDがわからない
**原因**: 複数のカレンダーがある場合
**解決プロンプト**:
```text
gog calendar calendars --account your-email@gmail.com で一覧表示し、
対象のカレンダーIDを確認してください。
メインカレンダーは通常 "primary" です。
```

### トラブル4: 作成したイベントが反映されない
**原因**: APIレスポンスの遅延、またはカレンダーのキャッシュ
**解決プロンプト**:
```text
gog calendar list で確認してください。Google Calendar のWebページでブラウザをリロードしてください。
数秒の遅延がある場合があります。
```

---

## ✅ チェックポイント
- [ ] 今日・今週のイベント一覧を取得できた
- [ ] カレンダー一覧（calendar IDs）を確認できた
- [ ] 新しいイベントを作成できた（場所・説明付き）
- [ ] AIを使って定例ミーティングを一括作成できた


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
以下のコマンドを実行して、Calendar操作が正しく動作するか確認してください:
1. gog calendar list --account <メールアドレス> --days 7
2. 上記の結果にこのレッスンで作成したイベントが含まれているか確認
すべて正常に動作するか確認してください。
```

**期待される結果**: 作成したイベントが一覧に表示されます。

---

## 🎉 次のステップ

これでGoogle Calendar操作は完了です！次のレッスンではGoogle Drive操作を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-4）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-4（Google Drive操作）
- next_window → 新しいウィンドウで /start-4-4
- finish → 終了
