---
description: "When the user says /start-4-1 — Module 4 Lesson 4-1: gogcli認証セットアップ"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "約25分"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "auth"]
---

# 🎓 Lesson 4-1: gogcli認証セットアップ

## 📍 このセッションでやること

**Lesson 4-1: gogcli認証セットアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcliでGoogleアカウントに認証し、Gmail/Calendar/Driveが使える状態にする |
| 所要時間 | 約25分 |
| 使うスキル | gogcli (gog) |
| 前提条件 | 環境セットアップ済み（start-0-1完了） |

**このセッションの流れ:**
1. gogcliのインストール確認
2. OAuth認証でGoogleアカウントを追加
3. 認証状態の確認と基本動作テスト

セッション終了時には、gogcliからGmail・Calendar・Driveにアクセスできる状態になっています。

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
(check_prereq → 前提条件の確認を実行)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: gogcliのインストール確認

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: gogcliのインストール確認",
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

gogcliがインストールされているか確認します。以下のコマンドを実行してください:

```bash
# バージョン確認
gog --version

# インストールされていない場合
go install github.com/nicholasgasior/gog@latest
# または Homebrew（macOS）
brew install gogcli
```

**期待される結果**: gogcliのバージョン番号が表示されます（例: `gog version 0.x.x`）。

> **📝 補足**: gogcliはGCPコンソールでのOAuthクライアント作成が不要です。内蔵OAuthクレデンシャルを使って認証するため、セットアップが非常に簡単です。

---

## 🚀 Step 2: OAuth認証でGoogleアカウントを追加

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: OAuth認証でGoogleアカウントを追加",
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

Googleアカウントの認証を行います。以下のコマンドを実行してください:

```bash
# Googleアカウントを追加（ブラウザが開きます）
gog auth add your-email@gmail.com
```

**手順:**
1. コマンドを実行するとブラウザが自動で開きます
2. Googleアカウントでログインします
3. gogcliへのアクセス許可を承認します（Gmail, Calendar, Drive, Sheets等）
4. 「認証が完了しました」と表示されたらブラウザを閉じてOK

```bash
# 認証されたアカウント一覧を確認
gog auth list

# 利用可能なサブコマンド一覧を確認
gog --help
```

**期待される結果**: `gog auth list` にあなたのメールアドレスが表示されます。

> **⚠️ 注意**: 認証情報はローカルマシンに安全に保存されます。トークンは `.gog/` ディレクトリ内に格納されます。

---

## 🚀 Step 3: 基本動作テスト

Codex では通常チャットで選択肢を提示しながらで「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 基本動作テスト",
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

各サービスが正しく動作するか確認します:

```bash
# Gmail: 最新のメール5件を検索
gog gmail search "newer_than:1d" --account your-email@gmail.com

# Calendar: 今日のイベントを一覧
gog calendar list --account your-email@gmail.com --days 1

# Drive: ルートフォルダのファイル一覧
gog drive ls --account your-email@gmail.com --max 5
```

**期待される結果**: 各コマンドでGmail/Calendar/Driveのデータが表示されます。エラーが出なければ認証は正常に完了しています。

> **💡 ヒント**: `--account` フラグはすべてのgogcliコマンドで必須です。毎回メールアドレスを指定する必要があります。

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
      {"id": "trouble_1", "label": "gogcliがインストールできない"},
      {"id": "trouble_2", "label": "ブラウザが開かない"},
      {"id": "trouble_3", "label": "認証後もアクセスできない"},
      {"id": "trouble_4", "label": "Permission deniedエラー"}
    ]
  }]
}
```

### トラブル1: gogcliがインストールできない
**原因**: Go言語がインストールされていない、またはPATHが通っていない
**解決プロンプト**:
```text
gogcliのインストール方法を確認してください。
Homebrewが使える場合は brew install gogcli を試してください。
Goがインストール済みなら go install github.com/nicholasgasior/gog@latest を試してください。
```

### トラブル2: ブラウザが開かない
**原因**: リモート環境やヘッドレス環境で実行している
**解決プロンプト**:
```text
gog auth add 実行時に表示されるURLをコピーして、手動でブラウザに貼り付けてください。
認証コードが発行されたらターミナルに入力してください。
```

### トラブル3: 認証後もアクセスできない
**原因**: トークンの保存に失敗している、またはスコープ不足
**解決プロンプト**:
```text
gog auth remove your-email@gmail.com で一度認証を削除し、
gog auth add your-email@gmail.com で再認証してください。
```

### トラブル4: Permission deniedエラー
**原因**: Googleアカウント側でアクセス許可が不足している
**解決プロンプト**:
```text
Google アカウントのセキュリティ設定で「安全性の低いアプリ」がブロックされていないか確認してください。
Google Workspace管理者がAPI制限をかけている場合は管理者に相談してください。
```

---

## ✅ チェックポイント
- [ ] gogcliがインストールされている（`gog --version` が動作する）
- [ ] Googleアカウントの認証が完了している（`gog auth list` に表示される）
- [ ] Gmailの検索が動作する（`gog gmail search` でメールが表示される）
- [ ] Calendarの一覧が動作する（`gog calendar list` でイベントが表示される）
- [ ] Driveのファイル一覧が動作する（`gog drive ls` でファイルが表示される）


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
以下のコマンドを実行して、gogcliの認証状態を確認してください:
1. gog auth list
2. gog gmail search "newer_than:1d" --account <メールアドレス>
3. gog calendar list --account <メールアドレス> --days 1
すべて正常に動作するか確認してください。
```

**期待される結果**: 3つのコマンドすべてがエラーなく実行できます。

---

## 🎉 次のステップ

これでgogcli認証セットアップは完了です！次のレッスンではGmail検索・閲覧を学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/start-4-2）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-4-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-4-2（Gmail検索・閲覧）
- next_window → 新しいウィンドウで /start-4-2
- finish → 終了
