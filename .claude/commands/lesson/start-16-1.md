---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "25分"
prerequisites: []
level: "beginner"
tags: ["email", "gmail", "gogcli", "setup"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 16-1: Gmail セットアップ - gogcli 認証とメール同期

## 📍 このセッションでやること

**Lesson 16-1: Gmail セットアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | gogcli で Gmail に認証し、メールの検索・閲覧ができる状態にする |
| 所要時間 | 約25分 |
| 使うツール | gogcli (gog) |
| 前提条件 | Google アカウント（Gmail）|
| 教材ページ | [Module 16: メール自動化](https://ai-agent.camp/ja/course/module-16) を並行参照 |

**このセッションの流れ:**
1. gogcli のインストール確認
2. `gog auth add` で Gmail 認証を設定
3. `gog gmail search` でメール検索テスト
4. google-sync によるメール同期を確認

セッション終了時には、gogcli で Gmail にアクセスし、メールの検索・閲覧ができる状態になっています。

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

## 🚀 Step 1: gogcli のインストール確認

まず gogcli がインストールされているか確認します。

**実行するコマンド:**
```bash
gog --version
```

**期待される結果:**
- バージョン番号が表示されればOK（v0.9.0 以上を推奨）
- コマンドが見つからない場合は `brew install gogcli` でインストール（または `/setup-gogcli` を実行）

> **📌 注意**: 以降のコマンドでは、すべての Gmail API 呼び出しに `--account <your-email@gmail.com>` が必要です。複数アカウントを登録している場合は明示的に指定してください。

**AskQuestion:**
```json
{
  "title": "📋 gogcli のインストール状態",
  "questions": [{
    "id": "gog_installed",
    "prompt": "gogcli のインストール結果は？",
    "options": [
      {"id": "installed", "label": "バージョンが表示された → 次へ進む"},
      {"id": "not_installed", "label": "コマンドが見つからない → インストールを手伝って"},
      {"id": "error", "label": "エラーが出た → トラブルシューティング"}
    ]
  }]
}
```

---

## 🚀 Step 2: Gmail 認証の設定

gogcli で Gmail アカウントを認証します。

**実行するコマンド:**
```bash
gog auth add <your-email@gmail.com>
```

ブラウザが開き、Google の OAuth 認証画面が表示されます。
アクセスを許可すると、トークンがローカルに保存されます。

**認証確認:**
```bash
gog auth list
```

**期待される結果:**
```text
ACCOUNT                    DEFAULT
your-email@gmail.com       *
```

**スコープの確認:**
```bash
gog auth services
```

Gmail の送信スコープ（`gmail.send`）が含まれていることを確認します。

---

## 🚀 Step 3: メール検索テスト

認証が完了したら、メールの検索をテストします。

**未読メールを検索:**
```bash
gog gmail search "is:unread" --account <your-email@gmail.com> --max 5
```

**特定の送信者のメールを検索:**
```bash
gog gmail search "from:noreply@github.com" --account <your-email@gmail.com> --max 5
```

**スレッドの詳細表示:**
```bash
gog gmail thread get <thread-id> --account <your-email@gmail.com>
```

**AskQuestion:**
```json
{
  "title": "✅ メール検索のテスト結果",
  "questions": [{
    "id": "search_result",
    "prompt": "メール検索は成功しましたか？",
    "options": [
      {"id": "success", "label": "メールが表示された → 次へ進む"},
      {"id": "empty", "label": "結果が空だった → クエリを変えて再試行"},
      {"id": "auth_error", "label": "認証エラー → トラブルシューティング"}
    ]
  }]
}
```

---

## 🚀 Step 4: google-sync によるメール同期（オプション）

check-inbox スキルはローカルの Markdown ファイルを読み取ります。
google-sync でメールをローカルに同期しておくと、13-2 がスムーズです。

**同期の確認:**
```bash
ls data/google-sync/data/*/gmail/ 2>/dev/null || echo "同期データなし"
```

同期データがない場合は、13-2 で check-inbox を使う際に設定します。

---

## ⚠️ よくあるトラブルと解決方法

**AskQuestion:**
```json
{
  "title": "⚠️ トラブルはありましたか？",
  "questions": [{
    "id": "trouble",
    "prompt": "何か問題がありましたか？",
    "options": [
      {"id": "none", "label": "問題なし → チェックポイントへ"},
      {"id": "auth_fail", "label": "認証が通らない"},
      {"id": "no_results", "label": "検索結果が出ない"},
      {"id": "other", "label": "その他のエラー"}
    ]
  }]
}
```

| トラブル | 解決策 |
|---------|--------|
| `gog` コマンドが見つからない | `brew install gogcli` を実行（または `/setup-gogcli`） |
| 認証でブラウザが開かない | `gog auth add --no-browser <email>` でURLを手動コピー（非対話環境では必須） |
| OAuth スコープ不足 | `gog auth remove <email>` → 再度 `gog auth add <email>` |
| 検索結果が空 | クエリを `is:inbox` に変更して再試行 |

---

## ✅ チェックポイント

以下を確認してください:

- [ ] `gog --version` でバージョンが表示される
- [ ] `gog auth list` でアカウントが表示される
- [ ] `gog gmail search "is:inbox" --account <your-email@gmail.com> --max 3` でメールが取得できる


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/email/
├── index.html  (HTMLメール)
├── style.css
└── assets/
```

### 確認コマンド
```bash
# ファイル一覧
ls -lh output/email/

# ブラウザで開く（macOS: open / Linux: xdg-open）
open output/email/index.html
```

> 💡 HTMLの構造確認: `head -30 output/email/index.html`

---

## ✅ 完了チェック

```bash
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

---

## ➡️ 次のステップ

**AskQuestion:**
```json
{
  "title": "🎉 Lesson 16-1 完了！",
  "questions": [{
    "id": "next_action",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "next_lesson", "label": "13-2 へ → 受信メール分析 & タスク抽出"},
      {"id": "practice", "label": "もう少し検索を練習したい"},
      {"id": "review", "label": "Module 16 の概要を確認"},
      {"id": "end", "label": "今日はここまで"}
    ]
  }]
}
```
