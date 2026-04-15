---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "約25分"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["notion", "ncli", "auth", "oauth"]
---

# 🎓 Lesson 12-1: ncliセットアップ・ブラウザ認証

## 📍 このセッションでやること

**Lesson 12-1: ncliセットアップ・ブラウザ認証** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | ncli（Notion CLI）をインストールし、OAuthブラウザ認証でNotionワークスペースに接続する |
| 所要時間 | 約25分 |
| 使うスキル | ncli (Notion CLI) |
| 前提条件 | Node.js 18以上、Notionアカウント |

**このセッションの流れ:**
1. ncli のインストール確認
2. `ncli login` でブラウザ認証
3. `ncli whoami` で認証確認
4. `ncli search` で接続テスト
5. `ncli fetch` で基本取得テスト

セッション終了時には、ターミナルからNotionワークスペースにアクセスできる状態になっています。

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
(check_prereq → Node.jsバージョン確認: `node --version` を実行し v18以上か確認)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: ncli インストール確認

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: ncli インストール確認",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする（インストール済みの場合）"}
    ]
  }]
}
```

**AIが実行すること:**

1. ncli がインストール済みか確認:
   ```bash
   npx @sakasegawa/ncli --version
   ```

2. インストールされていない場合、グローバルインストールを実行:
   ```bash
   npm install -g @sakasegawa/ncli
   ```

3. インストール後、バージョンを確認:
   ```bash
   ncli --version
   ```

**補足:** グローバルインストールせずに `npx @sakasegawa/ncli` で毎回実行することも可能です。以降のレッスンでは `ncli` コマンドを直接使用しますが、`npx @sakasegawa/ncli` に読み替えても構いません。

**期待される結果**: ncli のバージョン番号が表示される。

---

## 🚀 Step 2: ブラウザ認証（ncli login）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: ブラウザ認証",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする（認証済みの場合）"}
    ]
  }]
}
```

**AIが実行すること:**

1. ログインコマンドを実行:
   ```bash
   ncli login
   ```

2. ブラウザが自動で開き、Notion の OAuth 認証画面が表示されます。

3. **受講者への案内**:
   - ブラウザでNotionの認証画面が表示されます
   - 「Allow access」をクリックしてワークスペースへのアクセスを許可してください
   - **スクリーンショット撮影**: 認証画面が表示されたらスクリーンショットを撮影し `output/notion_auth_screenshot.png` に保存してください
   - 認証が完了すると、ターミナルに成功メッセージが表示されます

**期待される結果**: OAuth認証が完了し、ncli がNotionワークスペースにアクセスできるようになる。

---

## 🚀 Step 3: 認証確認（ncli whoami）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: 認証確認",
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

**AIが実行すること:**

1. 認証状態を確認:
   ```bash
   ncli whoami
   ```

2. 結果を確認し、以下の情報が表示されることを受講者に説明:
   - ユーザー名
   - ワークスペース名
   - 認証の有効期限

3. 表示された情報をユーザーに共有し、正しいワークスペースに接続されているか確認する。

**期待される結果**: ユーザー名とワークスペース名が正しく表示される。

---

## 🚀 Step 4: 接続テスト（ncli search）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: 接続テスト",
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

**AIが実行すること:**

1. ワークスペース内を検索:
   ```bash
   ncli search "test"
   ```

2. 検索結果を確認し、ページやデータベースが表示されることを確認する。

3. 別のキーワードでも試す:
   ```bash
   ncli search "タスク"
   ```

4. 結果をユーザーに見やすい形式で共有する。

**補足**: 検索結果が0件の場合でもエラーが出なければ接続は成功しています。ワークスペースにまだコンテンツが少ない場合は正常です。

**期待される結果**: 検索が正常に実行され、結果（0件を含む）が返ってくる。

---

## 🚀 Step 5: 基本取得テスト（ncli fetch）

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 基本取得テスト",
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

**AIが実行すること:**

1. 受講者にNotionページのURLを教えてもらう:
   - 「取得テストに使いたいNotionページのURLを教えてください」と案内

2. ページ内容を取得:
   ```bash
   ncli fetch <ページURL>
   ```

3. JSON形式でも取得してみる:
   ```bash
   ncli fetch <ページURL> --json
   ```

4. 取得結果の構造を解説:
   - ページタイトル
   - ブロックの種類（見出し、段落、リストなど）
   - プロパティ情報

**期待される結果**: Notionページの内容がターミナルに表示され、ページ構造が確認できる。

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
      {"id": "trouble_1", "label": "ncli login でブラウザが開かない"},
      {"id": "trouble_2", "label": "認証後に Permission denied エラー"},
      {"id": "trouble_3", "label": "ncli コマンドが見つからない"},
      {"id": "trouble_4", "label": "ncli fetch でページが取得できない"}
    ]
  }]
}
```

### トラブル1: ncli login でブラウザが開かない
**原因**: ターミナル環境からブラウザを起動できない設定になっている
**解決方法**:
```
以下を確認してください：
1. デフォルトブラウザが設定されているか
2. ターミナルからブラウザを開けるか（open https://notion.so で確認）
3. WSL環境の場合は BROWSER 環境変数を設定してください
```

### トラブル2: 認証後に Permission denied エラー
**原因**: ワークスペースへのアクセス権限が不足している
**解決方法**:
```
以下を確認してください：
1. ncli login 時に正しいワークスペースを選択したか
2. ワークスペースの管理者権限があるか
3. 再度 ncli login を実行して認証し直してください
```

### トラブル3: ncli コマンドが見つからない
**原因**: グローバルインストールされていない、またはPATHが通っていない
**解決方法**:
```
以下を試してください：
1. npm install -g @sakasegawa/ncli を再実行
2. npx @sakasegawa/ncli whoami でnpx経由の実行を試す
3. npm root -g でグローバルパッケージのパスを確認
4. シェルを再起動してPATHを更新
```

### トラブル4: ncli fetch でページが取得できない
**原因**: ページURLの形式が正しくない、またはアクセス権限がない
**解決方法**:
```
以下を確認してください：
1. URLが https://www.notion.so/... の形式か
2. ページIDを直接指定する場合は32文字のIDを使う
3. ncli search でページが検索できるか確認
4. ページがワークスペース内に存在するか確認
```

---

## ✅ チェックポイント
- [ ] ncli がインストールされている（バージョン番号が表示される）
- [ ] `ncli login` でOAuth認証が完了している
- [ ] `ncli whoami` でユーザー名・ワークスペース名が表示される
- [ ] `ncli search` で検索が実行できる
- [ ] `ncli fetch` でページ内容が取得できる

---

## 📋 成果物プレビュー

このレッスンで得られる成果物:

| 成果物 | 説明 |
|--------|------|
| ncli インストール済み環境 | ターミナルから `ncli` コマンドが実行可能 |
| OAuth認証完了 | Notionワークスペースへのアクセスが有効 |
| `output/notion_auth_screenshot.png` | 認証画面のスクリーンショット |
| 接続テスト結果 | search / fetch が正常に動作することを確認 |

---

## ➡️ 次のステップ

これでncliのセットアップは完了です。次のレッスンでは、データベースの取得とクエリを学びます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-12-2）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内:**
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-12-2
- finish → 終了
