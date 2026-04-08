---
description: "When the user says /start-10-1 — Module 10 Lesson 10-1: Clasp基本・GASプロジェクト管理"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "約25分"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["gas", "clasp", "google", "automation"]
---

# 🎓 Lesson 10-1: Clasp基本・GASプロジェクト管理

## 📍 このセッションでやること

**Lesson 10-1: GAS開発環境セットアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | ClaspでGASプロジェクトをローカル管理・デプロイできるようにする |
| 所要時間 | 約25分 |
| 使うスキル | gas-clasp-ops, clasp CLI |
| 前提条件 | Node.js インストール済み、Googleアカウント、Apps Script API 有効化済み、Lesson 0-1 完了 |
| 教材ページ | [Module 10: GAS](https://ai-agent.camp/ja/course/module-10) を並行参照 |

**このセッションの流れ:**
1. Claspのインストール
2. GASプロジェクトの作成とpush
3. デプロイと動作確認

セッション終了時には、ローカルからGASを編集・デプロイできるようになっています。

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

## 🚀 Step 1: Claspのインストールと Apps Script API の確認

まず、Google Apps Script API が有効になっているか確認します。
無効の場合、clasp login や clasp create が失敗します。

**Apps Script API 有効化チェック:**
1. https://script.google.com/home/usersettings にアクセス
2. 「Google Apps Script API」のトグルが **ON** になっていることを確認
3. OFF の場合は ON に切り替える

> **重要**: Apps Script API が無効だと `clasp login` 後の操作（`clasp create`, `clasp push` 等）がすべて失敗します。必ず先に有効化してください。

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Claspのインストール",
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
Claspをグローバルインストールして、バージョンを確認してください。
npm install -g @google/clasp を実行し、clasp --version で確認してください。
```

**期待される結果**: Claspのバージョン番号が表示されます（例: 2.4.2）

---

## 🚀 Step 2: Google認証

> **📝 gogcli との関係**: 4-1 で gogcli の Google OAuth 認証（`gog auth login`）を完了していますが、clasp は独自の認証情報を使用します。gogcli の認証と clasp の認証は別々に管理されるため、ここで `clasp login` を実行する必要があります。
>
> - **gogcli 認証**: `~/.config/gogcli/` に保存 → Gmail, Calendar, Drive, Sheets 等の API アクセス用
> - **clasp 認証**: `~/.clasprc.json` に保存 → Apps Script プロジェクトの管理・デプロイ用

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Google認証（clasp login）",
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
clasp login を実行して、Googleアカウントでログインしてください。
ブラウザが開くので認証を完了させてください。
認証完了後、~/.clasprc.json が作成されていることを確認してください。

💡 4-1 で gogcli の Google 認証は完了していますが、
clasp は専用の認証が必要です。同じ Google アカウントでログインしてください。
```

**期待される結果**: ブラウザで認証後、「Authorization successful」と表示されます。

---

## 🚀 Step 3: GASプロジェクトの作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: GASプロジェクトの作成",
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
以下のディレクトリとGASプロジェクトを作成してください：

1. ~/ai-agent-camp/gas-example ディレクトリを作成
2. そのディレクトリで clasp create --type standalone を実行
3. 作成された .clasp.json と appsscript.json の内容を表示
```

**期待される結果**: `.clasp.json` にスクリプトIDが記載され、`appsscript.json` にタイムゾーン設定が含まれます。

---

## 🚀 Step 4: Hello Worldスクリプト作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: Hello Worldスクリプト作成",
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
gas-example ディレクトリに Code.gs ファイルを作成し、以下の内容を記述してください：

function helloWorld() {
  Logger.log("Hello World from GAS!");
  return "Success";
}

function getExecutionInfo() {
  const info = {
    user: Session.getActiveUser().getEmail(),
    timezone: Session.getScriptTimeZone(),
    timestamp: new Date().toISOString()
  };
  Logger.log(JSON.stringify(info));
  return info;
}

その後、clasp push で同期してください。
```

**期待される結果**: 「Pushed X files.」と表示され、Googleドライブに反映されます。

---

## 🚀 Step 5: GASエディタで確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: GASエディタで確認",
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
clasp open を実行して、ブラウザでGoogle Apps Scriptエディタを開いてください。
エディタで helloWorld 関数を実行し、ログを確認してください。
```

**期待される結果**: GASエディタが開き、helloWorld関数を実行すると「Hello World from GAS!」がログに表示されます。

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
      {"id": "trouble_1", "label": "clasp: command not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Push failed: File name contains invalid characters"},
      {"id": "trouble_4", "label": "Script ID is invalid"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"}
    ]
  }]
}
```


### トラブル1: 「clasp: command not found」
**原因**: Claspがインストールされていない、またはPATHに追加されていない
**解決プロンプト**:
```
npm install -g @google/clasp を再実行して、which clasp でパスを確認してください。
パスが通っていない場合の対処法も教えてください。
```

### トラブル2: 「Permission denied」
**原因**: Google認証が完了していない
**解決プロンプト**:
```
clasp logout を実行してから clasp login を再度実行してください。
認証エラーの詳細を教えてください。
```

### トラブル3: 「Push failed: File name contains invalid characters」
**原因**: ファイル名に日本語など非ASCII文字が含まれている
**解決プロンプト**:
```
gas-example ディレクトリ内のファイル名を確認して、英数字とアンダースコアのみに修正してください。
```

### トラブル4: 「Script ID is invalid」
**原因**: .clasp.json が存在しない、または破損している
**解決プロンプト**:
```
.clasp.json ファイルを削除して、clasp create --type standalone を再実行してください。
```

### トラブル5: 「Apps Script API has not been used in project / User has not enabled the Apps Script API」
**原因**: Google Apps Script API が無効になっている
**解決手順**:
1. https://script.google.com/home/usersettings にアクセス
2. 「Google Apps Script API」のトグルを **ON** に切り替える
3. 変更後、`clasp login` からやり直す

> この設定はGoogleアカウント単位です。一度有効にすれば、以降のすべてのGASプロジェクトで使えます。

---

## ✅ チェックポイント
- [ ] Claspがインストールされている（clasp --version で確認）
- [ ] Google認証が完了している（~/.clasp.json が存在）
- [ ] GASプロジェクトが初期化されている
- [ ] Code.gs が作成されている
- [ ] clasp push が成功する
- [ ] GASエディタで実行できる


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
# 1. clasp --version でバージョンが表示されるか
# 2. gas-example/.clasp.json が存在するか
# 3. gas-example/Code.gs が存在するか
# 4. clasp push が成功するか（gas-example ディレクトリで実行）
# 5. clasp open でGASエディタが開けるか
```

**期待される結果**: すべてのチェック項目がパスし、GASプロジェクトがローカルから管理・デプロイできる状態です。

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
      {"id": "next_auto", "label": "次のセクションを開始（/start-10-2）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-10-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /start-10-2
- next_window → 新しいウィンドウで /start-10-2
- finish → 終了
