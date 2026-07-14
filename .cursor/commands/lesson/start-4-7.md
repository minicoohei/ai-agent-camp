---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約30分"
prerequisites: ["start-4-1", "start-4-2", "start-4-3", "start-4-4", "start-4-5", "start-4-6"]
level: "intermediate"
tags: ["google", "workspace", "gogcli", "workflow", "automation"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 4-7: AI秘書ワークフロー統合

## 📍 このセッションでやること

**Lesson 4-7: AI秘書ワークフロー統合** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Gmail+Calendar+Driveを組み合わせたAI秘書ワークフローを構築する |
| 所要時間 | 約30分 |
| 使うスキル | gogcli, check-inbox, google-sync |
| 前提条件 | Lesson 4-1〜4-6 すべて完了済み |

**このセッションの流れ:**
1. google-syncでデータを一括同期する
2. check-inboxでメールからタスクを抽出する
3. カレンダーとの照合で優先度を判定する
4. 日次レポートを自動生成する

セッション終了時には、Gmail・Calendar・Driveを横断したAI秘書ワークフローが動作するようになっています。

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
      {"id": "check_prereq", "label": "前提条件を確認したい（4-1〜4-6の完了状況）"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 4-1〜4-6の完了状況を確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: google-syncでデータを一括同期する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: データ一括同期",
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

google-syncスクリプトを使って、Gmail・Calendar・Driveのデータを一括同期します:

```bash
# google-syncの依存パッケージをインストール
uv sync

# データ同期を実行
python data/google-sync/scripts/sync_google.py --account your-email@gmail.com
```

**sync_google.pyが行うこと:**
1. **Gmail**: 直近のメールを取得し、`data/google-sync/data/gmail/` にMarkdown形式で保存
2. **Calendar**: 今後のイベントを取得し、`data/google-sync/data/calendar/` に保存
3. **Drive**: 最近更新されたドキュメントのメタデータを `data/google-sync/data/docs/` に保存

```bash
# 同期結果を確認
ls -la data/google-sync/data/

# Gmail同期データの確認
ls data/google-sync/data/gmail/ | head -10

# Calendar同期データの確認
ls data/google-sync/data/calendar/
```

**期待される結果**: `data/` ディレクトリにGmail・Calendar・Driveのデータが保存されます。

> **💡 ヒント**: sync_google.pyが存在しない場合は、gogcliコマンドを組み合わせて手動同期もできます。Step 1の代替手順をAIに聞いてください。

**代替手順（gogcli直接実行）:**
```bash
# Gmail: 未読メールを取得
mkdir -p /tmp/google-sync/gmail
gog gmail search "is:unread newer_than:7d" --account your-email@gmail.com > /tmp/google-sync/gmail/unread.txt

# Calendar: 今週のイベント
mkdir -p /tmp/google-sync/calendar
gog calendar list --account your-email@gmail.com --days 7 > /tmp/google-sync/calendar/this_week.txt

# Drive: 最近更新のファイル
mkdir -p /tmp/google-sync/drive
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-07'" --max 20 > /tmp/google-sync/drive/recent.txt
```

---

## 🚀 Step 2: check-inboxでメールからタスクを抽出する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: メールからタスク抽出",
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

check-inboxスキルを使って、メールからアクションアイテムを自動抽出します:

```bash
# check-inboxスクリプトを実行
python skills/check-inbox/scripts/check_inbox.py --account your-email@gmail.com
```

**check-inboxが行うこと:**
1. 直近のメールを取得
2. AIがメール内容を分析し、以下を抽出:
   - **返信が必要なメール**（優先度: 高/中/低）
   - **依頼・タスクが含まれるメール**（期限付き）
   - **FYI（情報共有のみ）**
   - **フォローアップが必要なメール**

**代替手順（AIに直接依頼）:**

gogcliで取得したメールデータをAIに分析させることもできます:

```bash
# 未読メールを取得
gog gmail search "is:unread newer_than:3d" --account your-email@gmail.com
```

取得結果をCursorのチャットに貼り付けて:
```text
上記のメール一覧から、以下の分類でタスクを抽出してください:

## 🔴 至急対応（24時間以内）
- メール件名 / 送信者 / 必要なアクション

## 🟡 今週中に対応
- メール件名 / 送信者 / 必要なアクション

## 🟢 情報確認のみ（FYI）
- メール件名 / 送信者 / 概要

## 📋 フォローアップ
- メール件名 / 送信者 / フォロー期限
```

**期待される結果**: メールがカテゴリ別に分類され、優先度付きのタスクリストが生成されます。

---

## 🚀 Step 3: カレンダーとの照合で優先度を判定する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: カレンダー照合と優先度判定",
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

Step 2で抽出したタスクと、カレンダーの予定を照合して優先度を判定します:

```bash
# 今週のカレンダーを取得
gog calendar list --account your-email@gmail.com --days 7
```

取得したカレンダーデータとStep 2のタスクリストを合わせてAIに依頼します:

```text
以下の2つのデータを照合して、統合的な優先度判定を行ってください:

【メールから抽出したタスク】
（Step 2の結果をここに貼り付け）

【今週のカレンダー】
（カレンダー一覧をここに貼り付け）

以下の観点で分析してください:
1. 会議の直前に準備が必要なタスクはあるか？
2. 会議が集中している日にタスクを割り当てるのは避ける
3. 空き時間のスロットにタスクを割り当てる提案
4. デッドラインが迫っているタスクの警告
5. 明日の準備として今日やるべきことのリスト

結果を以下の形式で出力してください:

## 📅 今日のTo-Do（優先順位付き）
1. [高] タスク名 - 理由
2. [中] タスク名 - 理由
3. [低] タスク名 - 理由

## 📋 今週のTo-Do（日別）
### 月曜日
- タスク（空き: 10:00-12:00に実施推奨）
### 火曜日
- ...

## ⚠️ 注意事項
- 会議前準備のリマインダー
- デッドライン警告
```

**期待される結果**: メールのタスクとカレンダーの予定が統合され、実行可能なTo-Doリストが優先度付きで生成されます。

---

## 🚀 Step 4: 日次レポートを自動生成する

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 日次レポート生成",
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

すべてのデータを統合して日次レポートを生成します。以下のプロンプトをCursorに入力してください:

```text
以下のgogcliコマンドを実行し、結果を統合して日次レポートを生成してください:

1. gog gmail search "newer_than:1d" --account your-email@gmail.com
2. gog calendar list --account your-email@gmail.com --days 1
3. gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-13'" --max 10

以下のフォーマットでレポートを作成し、output/reports/daily_report_2026-03-14.md に保存してください:

# 📊 日次レポート: 2026-03-14

## 📧 メールサマリー
- 受信: X件（未読: X件）
- 要返信: X件
- 主要なメール:
  1. [件名] from [送信者] - [1行要約]

## 📅 今日のスケジュール
| 時間 | イベント | 場所 |
|------|---------|------|
| 10:00-11:00 | xxx | xxx |

## 📁 最近更新されたファイル
- [ファイル名] - [最終更新日時]

## ✅ 今日のTo-Do（優先順位付き）
1. [高] xxx
2. [中] xxx

## 📝 メモ・備考
- 気になった点
```

**応用: 定期実行の設定**

日次レポートを毎朝自動生成するには、以下の方法があります:

```bash
# シェルスクリプトにまとめる
cat > tools/daily_report.sh << 'SCRIPT'
#!/bin/bash
ACCOUNT="your-email@gmail.com"
DATE=$(date +%Y-%m-%d)

echo "=== Gmail ===" > /tmp/daily_data.txt
gog gmail search "newer_than:1d" --account $ACCOUNT >> /tmp/daily_data.txt

echo "=== Calendar ===" >> /tmp/daily_data.txt
gog calendar list --account $ACCOUNT --days 1 >> /tmp/daily_data.txt

echo "=== Drive ===" >> /tmp/daily_data.txt
gog drive ls --account $ACCOUNT --query "modifiedTime > '$(date -v-1d +%Y-%m-%d)'" --max 10 >> /tmp/daily_data.txt

echo "データ収集完了: /tmp/daily_data.txt"
echo "Cursorで「/tmp/daily_data.txt を読み込んで日次レポートを生成してください」と入力してください"
SCRIPT
chmod +x tools/daily_report.sh
```

**期待される結果**: `output/reports/` に日次レポートがMarkdown形式で保存されます。

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
      {"id": "trouble_1", "label": "google-syncスクリプトが動かない"},
      {"id": "trouble_2", "label": "check-inboxがエラーになる"},
      {"id": "trouble_3", "label": "データが多すぎて処理に時間がかかる"},
      {"id": "trouble_4", "label": "レポートの品質を上げたい"}
    ]
  }]
}
```

### トラブル1: google-syncスクリプトが動かない
**原因**: 依存パッケージの不足、またはスクリプトの設定
**解決プロンプト**:
```text
代替手順として、gogcliコマンドを直接使ってデータを収集してください。
Step 1の「代替手順」セクションのコマンドを実行してください。
```

### トラブル2: check-inboxがエラーになる
**原因**: スキルの設定不足、またはメールデータの取得失敗
**解決プロンプト**:
```text
check-inboxの代わりに、gogcli gmail search でメールを取得し、
AIに直接タスク抽出を依頼してください（Step 2の「代替手順」参照）。
```

### トラブル3: データが多すぎて処理に時間がかかる
**原因**: --max パラメータが大きすぎる
**解決プロンプト**:
```text
--max の値を小さくしてください（推奨: 10-20件）。
期間も --query "newer_than:1d" のように短くすると高速化できます。
```

### トラブル4: レポートの品質を上げたい
**原因**: プロンプトの改善が必要
**解決プロンプト**:
```text
プロンプトに以下を追加してみてください:
- 「ビジネスメールの重要度判定基準: 上司/クライアントからのメールを優先」
- 「会議の準備事項を各イベントに付記」
- 「前日のTo-Do未完了分を引き継ぎ」
```

---

## ✅ チェックポイント
- [ ] google-sync（または手動gogcliコマンド）でデータを一括収集できた
- [ ] メールからタスクを抽出し、優先度分類できた
- [ ] カレンダーとタスクを照合して統合To-Doを作成できた
- [ ] 日次レポートをMarkdown形式で生成・保存できた


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
Module 4の総合チェックを行ってください:
1. gog auth list でGoogleアカウントの認証状態を確認
2. output/reports/ に日次レポートが生成されているか確認
3. 以下のgogcliコマンドがすべて動作するか確認:
   - gog gmail search "newer_than:1d" --account <email>
   - gog calendar list --account <email> --days 1
   - gog drive ls --account <email> --max 3
```

**期待される結果**: すべてのコマンドがエラーなく動作し、日次レポートが生成されています。

---

## 🎉 Module 4 完了！

おめでとうございます！Module 4「Google Workspace活用」をすべて完了しました。

**習得したスキル:**
- gogcliのインストールと認証セットアップ
- Gmailのメール検索・閲覧・AI分析
- Google Calendarのイベント管理
- Google Driveのファイル操作
- Google Sheetsのデータ取得・分析
- Gmail+Calendar+Driveを統合したAI秘書ワークフロー

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "Module 5に進む（/start-5-1）"},
      {"id": "review", "label": "Module 4を復習する（/start-4-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_module → /start-5-1（次のモジュールへ）
- review → /start-4-1（Module 4の最初から復習）
- finish → 終了
