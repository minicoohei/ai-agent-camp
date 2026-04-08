---
description: "セキュリティ設定の自動セットアップ"
duration: "約5分"
prerequisites: ["ai-agent-camp フォルダを Cursor で開いている"]
level: "beginner"
tags: ["setup", "security"]
---

# /setup-security -- セキュリティ設定の自動セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-security` を実行して進捗を表示
2. 既に設定済みか確認:
   - `.gitignore` が適切に設定されているか
   - pre-commit フックが設定されているか
   - 両方設定済みなら「セキュリティ設定は完了しています。スキップしますか？」と確認

## このコマンドの役割

APIキーやパスワードなどの**秘密情報が誤ってGitHubに公開されるのを防ぐ**セキュリティ設定を、AIが自動で行います。
ユーザーがターミナルを操作する必要はありません。全てAIが裏側で実行します。

| 項目 | 内容 |
|------|------|
| ゴール | .gitignore と pre-commit フックを自動設定し、秘密情報の漏洩を防止する |
| 所要時間 | 約5分 |
| 前提条件 | ai-agent-camp フォルダを Cursor で開いている |
| ユーザー操作 | ボタンを押すだけ（CLIコマンドの入力は不要） |

---

## なぜセキュリティ設定が必要なの？

> **身近な例で説明します:**
>
> あなたが「自宅の鍵の番号」をメモ帳に書いて、そのメモ帳を公園のベンチに置いてきてしまったら、誰でも自宅に入れてしまいますよね。
>
> AIサービスの「APIキー」はこの「鍵の番号」に相当します。APIキーがGitHub（インターネット上のコード保管庫）に公開されると:
>
> - **他人にAPIキーを不正利用される**（あなたのアカウントで大量のリクエストが送られ、高額請求が来る可能性）
> - **個人情報や社内データが流出する**可能性
> - **アカウントが乗っ取られる**可能性
>
> このセキュリティ設定では、**うっかりAPIキーを公開してしまうことを自動で防ぐ仕組み**を作ります。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "セキュリティ設定を始めます",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "始めましょう"},
      {"id": "more_info", "label": "もう少し詳しく知りたい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready -> Step 1 へ)
(more_info -> 以下を表示)

> **このコマンドで設定する3つの安全装置:**
>
> 1. **.gitignore** -- 「このファイルはGitHubにアップロードしないでね」とGitに教えるリスト。APIキーを書いた .env ファイルなどを除外対象に設定します。
>
> 2. **pre-commit フック** -- GitHubにアップロードする直前に「本当に大丈夫？」と自動チェックする仕組み。うっかりAPIキーを含むファイルをアップロードしようとすると、自動でブロックしてくれます。
>
> 3. **現状チェック** -- 既にAPIキーが公開されてしまっていないか、AIが自動で調べます。

(different_lesson -> モジュール一覧を表示)

---

## Step 1: .gitignore の確認・設定

**AIが自動実行すること:**

1. プロジェクトルートの `.gitignore` ファイルを読み取る
2. 以下のエントリが含まれているか確認する:

```text
# 秘密情報（APIキー・トークン）
.env
.env.local
.env.*.local

# 認証情報
credentials/
*.key
*.pem

# OSが自動生成するファイル
.DS_Store
Thumbs.db
```

3. **不足しているエントリがある場合**: 自動で `.gitignore` に追加する

4. 結果をユーザーに表示:

```text
.gitignore を確認しました。

| 除外設定 | 状態 | 説明 |
|---------|------|------|
| .env | 追加済み | APIキーファイル |
| .env.local | 追加済み | ローカル環境変数 |
| .env.*.local | 追加済み | 環境別ローカル変数 |
| credentials/ | 追加済み | 認証情報フォルダ |
| *.key | 追加済み | 秘密鍵ファイル |
| *.pem | 追加済み | 証明書ファイル |

.gitignore を更新しました。
これにより、APIキーなどの秘密情報がGitHubに公開されることを防ぎます。
```

5. **既に全てのエントリが含まれている場合**:
```text
.gitignore は既に正しく設定されています。追加の変更は不要です。
```

**注意: ファイルの確認・編集は全てAIが自動で行う。ユーザーにはコマンドを打たせない。**

---

## Step 2: pre-commit フックの設定

**AIが自動実行すること:**

1. `.git/hooks/pre-commit` ファイルが存在するか確認する
2. 存在しない場合、または .env のチェックが含まれていない場合、以下の内容で作成する:

```bash
#!/bin/sh
# セキュリティチェック: 秘密情報を含むファイルのコミットをブロック
# このフックは /setup-security コマンドによって自動生成されました

# .env ファイルのコミットをブロック
BLOCKED_FILES=$(git diff --cached --name-only | grep -E '^\\.env$|^\\.env\\.|credentials/|.*\\.key$|.*\\.pem$')

if [ -n "$BLOCKED_FILES" ]; then
    echo ""
    echo "============================================"
    echo "  セキュリティ警告: コミットがブロックされました"
    echo "============================================"
    echo ""
    echo "以下のファイルには秘密情報が含まれている可能性があります:"
    echo "$BLOCKED_FILES"
    echo ""
    echo "これらのファイルをGitHubに公開すると、"
    echo "APIキーの不正利用や情報漏洩のリスクがあります。"
    echo ""
    echo "対処方法:"
    echo "  1. git reset HEAD <ファイル名> でステージングから除外"
    echo "  2. 本当に必要な場合のみ git commit --no-verify で強制コミット"
    echo ""
    exit 1
fi
```

3. ファイルに実行権限を付与する（AIが `chmod +x .git/hooks/pre-commit` を裏側で実行）

4. 結果をユーザーに表示:
```text
セキュリティフックを設定しました。

これにより、以下のファイルをうっかりコミットしようとしても、自動でブロックされます:
- .env（APIキーファイル）
- .env.local / .env.*.local（環境変数ファイル）
- credentials/ フォルダ内のファイル
- *.key / *.pem（秘密鍵・証明書）

もし間違ってこれらのファイルをコミットしようとすると、
警告メッセージが表示されてコミットが中断されるので安心です。
```

5. **既にフックが設定されている場合**:
```text
pre-commit フックは既に設定されています。追加の変更は不要です。
```

**注意: ファイルの作成・権限設定は全てAIが自動で行う。ユーザーにはコマンドを打たせない。**

---

## Step 3: 現状の安全性チェック

**AIが自動実行すること:**

1. `git status` を裏側で実行し、.env ファイルが追跡対象になっていないか確認
2. `git log --all --full-history -- .env .env.local .env.*.local` を裏側で実行し、過去に .env がコミットされていないか確認
3. `git ls-files -- .env .env.local` を裏側で実行し、現在 Git 管理下にないか確認

4. 結果をユーザーに表示:

**問題がない場合:**
```text
## 安全性チェック結果

| チェック項目 | 結果 |
|-------------|------|
| .env がGit追跡対象か | 追跡対象外（安全） |
| 過去に .env がコミットされたか | コミット履歴なし（安全） |
| 現在 .env がステージングされているか | ステージングなし（安全） |

すべてのチェックに合格しました。秘密情報は安全に管理されています。
```

**問題がある場合（.envが追跡対象になっている）:**
```text
## 安全性チェック結果

| チェック項目 | 結果 |
|-------------|------|
| .env がGit追跡対象か | 追跡対象になっています（要修正） |

問題を検出しました。.env ファイルがGitの追跡対象になっています。
```

**AskQuestionの設定:**
```json
{
  "title": "問題を自動で修正しますか？",
  "questions": [{
    "id": "fix",
    "prompt": ".env ファイルをGitの追跡対象から除外します。これにより、今後 .env ファイルがGitHubにアップロードされることを防ぎます。",
    "options": [
      {"id": "yes", "label": "自動で修正する"},
      {"id": "explain", "label": "修正内容を詳しく教えて"},
      {"id": "skip", "label": "今はスキップする"}
    ]
  }]
}
```

(yes -> AIが以下を自動実行)
- `git rm --cached .env` を裏側で実行（ファイル自体は削除せず、Git追跡のみ解除）
- `.gitignore` に .env が含まれていることを再確認
- 「修正が完了しました。.env ファイルは引き続きローカルに存在しますが、GitHubにはアップロードされなくなりました」と表示

(explain -> 修正内容の詳細説明を表示してから再度 AskQuestion)

(skip -> 次へ進む)

**問題がある場合（過去に .env がコミットされている）:**
```text
過去に .env ファイルがコミットされた履歴があります。
GitHubにpushしていた場合、APIキーが公開されている可能性があります。

推奨アクション:
1. 対象のAPIキーを再生成（古いキーを無効化）する
2. Google AI Studio で新しいキーを発行する
3. .env ファイルを新しいキーで更新する

APIキーの再生成方法は /start-0-3（Gemini API設定）を参照してください。
```

**注意: Git操作は全てAIが裏側で実行する。ユーザーにはコマンドを打たせない。**

---

## よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブルがありますか？",
  "questions": [{
    "id": "trouble",
    "prompt": "何か問題がありますか？",
    "options": [
      {"id": "trouble_1", "label": "「permission denied」エラーが出る"},
      {"id": "trouble_2", "label": ".gitignore を変更しても反映されない"},
      {"id": "trouble_3", "label": "pre-commit フックが動作しない"},
      {"id": "no_trouble", "label": "問題なし、次へ進む"}
    ]
  }]
}
```

### トラブル1: 「permission denied」エラーが出る
**原因**: ファイルの書き込み権限がない
**AIが行う対処**:
1. ファイルの権限を確認（AIが裏側で `ls -la .git/hooks/pre-commit` を実行）
2. 権限が不足している場合、AIが自動で修正
3. 「権限を修正しました」と表示

### トラブル2: .gitignore を変更しても反映されない
**原因**: 既にGit追跡対象になっているファイルは .gitignore の追加だけでは除外されない
**AIが行う対処**:
1. AIが裏側で `git rm --cached <ファイル名>` を実行（ファイル自体は削除しない）
2. 「Gitの追跡を解除しました。今後はこのファイルがGitHubにアップロードされることはありません」と表示

### トラブル3: pre-commit フックが動作しない
**原因**: ファイルに実行権限がない、またはファイルパスが間違っている
**AIが行う対処**:
1. `.git/hooks/pre-commit` の存在と権限を確認（AIが裏側で実行）
2. 問題があれば自動で再作成・権限付与
3. テストコミットで動作を確認（AIが裏側で `git stash && echo "test" > .env_test && git add .env_test && git reset HEAD .env_test && rm .env_test` のような安全なテストを実行）
4. 「フックの動作を確認しました」と表示

---

## チェックポイント

- [ ] .gitignore に .env / credentials/ / *.key / *.pem が含まれている
- [ ] pre-commit フックが設定されている（.git/hooks/pre-commit が存在し実行可能）
- [ ] .env ファイルがGitの追跡対象になっていない
- [ ] 過去に .env がコミットされた履歴がない（あれば対処済み）

---

## 次のステップ

**AskQuestionの設定:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に何をしますか？",
    "options": [
      {"id": "check", "label": "環境の総合チェックをする（/check-setup）"},
      {"id": "extensions", "label": "拡張機能をセットアップする（/setup-extensions）"},
      {"id": "api", "label": "APIキーを設定する（/start-0-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(check -> /check-setup を案内)
(extensions -> /setup-extensions を案内)
(api -> /start-0-3 を案内)
(finish -> 「お疲れさまでした。セキュリティ設定が完了しました」と表示)

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-security` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/check-setup` で最終チェックを行いましょう」
