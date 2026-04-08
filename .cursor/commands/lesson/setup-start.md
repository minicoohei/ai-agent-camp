---
description: "研修環境セットアップ（最初に実行）"
duration: "約10分"
prerequisites: ["Cursor をインストール済み"]
level: "beginner"
tags: ["setup", "environment"]
---

# 研修環境セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-start` を実行して現在の進捗を表示する
2. 以下を自動チェックして、全て成功なら「基本ツールは既にインストール済みです。スキップしますか？」と確認:
   - `python3 --version`
   - `node --version`
   - `git --version`
   - `gh --version`
3. Mac の場合、Homebrew が使えるか `which brew` で確認。使える場合、未インストールのツールを `brew install` で自動インストールする選択肢を提供

## このセッションでやること

**研修環境セットアップ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Python / Node.js / Git / GitHub CLI がインストールされていることを確認し、未導入なら案内する |
| 所要時間 | 約10分（全てインストール済みなら3分） |
| 使うスキル | なし（AIが全て自動で確認します） |
| 前提条件 | Cursor をインストール済み、ai-agent-camp フォルダを開いている |
| 次のコマンド | `/setup-github`（GitHub アカウント設定） |

**このセッションの流れ:**
1. OS自動判定（Mac / Windows）
2. Python の確認
3. Node.js の確認
4. Git の確認
5. GitHub CLI の確認

> **重要**: あなたがターミナルにコマンドを入力する必要は一切ありません。全てAIが裏側で自動実行します。画面に表示される結果を確認するだけでOKです。
>
> **ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## セッション開始前の確認

**AskQuestionの設定:**
```json
{
  "title": "セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "what_is_this", "label": "このコマンドは何をするの？"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(what_is_this → 以下を案内:「このコマンドは、研修に必要なソフトウェアがパソコンに入っているかをAIが自動で調べます。入っていないものがあれば、インストール方法を画面の案内に沿って進めるだけです。コマンド入力は不要です。」→ Step 1へ)
(different_lesson → モジュール一覧を表示)

---

## Step 1: OSの自動判定

**AIが自動実行する内容:**
AIが以下を裏側で実行してOSを判定する:

```bash
uname -s
```

Mac なら `Darwin`、Linux なら `Linux` が返る。失敗した場合は以下を試す:

```powershell
echo $env:OS
```

Windows なら `Windows_NT` が返る。

**判定結果の表示:**
- Mac の場合: 「お使いのパソコンは **Mac** です。Mac 向けの手順で進めます。」
- Windows の場合: 「お使いのパソコンは **Windows** です。Windows 向けの手順で進めます。」

**判定した OS 情報は以降の全ステップで使用する。**

> ユーザーへの操作依頼: なし（AIが全自動で判定）

---

## Step 2: Pythonの確認

**AIが自動実行する内容:**

1. 以下を実行してバージョンを確認する:

```bash
# Mac / Linux
python3 --version

# Windows
python --version
```

2. 結果を確認して以下を判定:
   - バージョンが表示された場合 → インストール済み
   - コマンドが見つからない場合 → 未インストール

### Python がインストール済みの場合

表示例:
```text
Python 3.12.x が見つかりました。問題ありません。
```
→ Step 3 へ自動で進む

### Python が未インストールの場合

**AskQuestionの設定:**
```json
{
  "title": "Python のインストールが必要です",
  "questions": [{
    "id": "python_install",
    "prompt": "Python 3 がインストールされていません。インストール方法を案内します。",
    "options": [
      {"id": "guide_me", "label": "インストール手順を教えて"},
      {"id": "already_done", "label": "別の方法でインストール済み（再確認して）"}
    ]
  }]
}
```

(guide_me → OS に応じた案内を表示)
(already_done → `python3 --version` / `python --version` を再実行して確認)

**Mac の場合の案内:**
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
2. 開いたページで黄色い「Download Python 3.12.x」ボタンをクリック
3. ダウンロードされた .pkg ファイルをダブルクリック
4. インストーラーの指示に従って「続ける」→「インストール」をクリック
5. 完了したら、ここに「終わった」と入力してください
```

```bash
AIが実行: open https://www.python.org/downloads/
```

**Windows の場合の案内:**
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
   ※ ブラウザが開かない場合は、Microsoft Store アプリを開いて「Python 3.12」で検索してください
2. Microsoft Store で「Python 3.12」の「入手」ボタンをクリック
3. インストールが完了したら、ここに「終わった」と入力してください
```

```bash
AIが実行: start https://apps.microsoft.com/search?query=Python+3.12
# 失敗した場合は start https://www.python.org/downloads/ にフォールバック
```

**インストール完了後:**
AIが `python3 --version` / `python --version` を再実行してインストールを確認。
- 成功 → 「Python のインストールが完了しました！」と表示して Step 3 へ
- 失敗 → トラブルシューティングセクションへ案内

---

## Step 3: Node.js の確認

**AIが自動実行する内容:**

1. 以下を実行してバージョンを確認する:

```bash
node --version
```

2. 結果を確認して以下を判定:
   - バージョン 18.x 以上が表示された場合 → インストール済み
   - バージョンが古い場合 → アップデートを案内
   - コマンドが見つからない場合 → 未インストール

### Node.js がインストール済み（18.x 以上）の場合

表示例:
```text
Node.js v20.x.x が見つかりました。問題ありません。
```
→ Step 4 へ自動で進む

### Node.js が未インストール / バージョンが古い場合

**AskQuestionの設定:**
```json
{
  "title": "Node.js のインストールが必要です",
  "questions": [{
    "id": "node_install",
    "prompt": "Node.js 18以上が必要です。インストール方法を案内します。",
    "options": [
      {"id": "guide_me", "label": "インストール手順を教えて"},
      {"id": "already_done", "label": "別の方法でインストール済み（再確認して）"}
    ]
  }]
}
```

(guide_me → OS に応じた案内を表示)
(already_done → `node --version` を再実行して確認)

**Mac / Windows 共通の案内:**
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
2. 開いたページで緑色の「LTS」と書かれたボタンをクリック（推奨版です）
3. ダウンロードされたファイルを開いてインストーラーを起動
4. インストーラーの指示に従って「Next」→「Install」をクリック
5. 完了したら、ここに「終わった」と入力してください
```

```bash
# AIが実行:
# Mac:
open https://nodejs.org/
# Windows:
start https://nodejs.org/
```

**インストール完了後:**
AIが `node --version` を再実行してインストールを確認。
- 成功 → 「Node.js のインストールが完了しました！」と表示して Step 4 へ
- 失敗 → 「Cursor を一度閉じて再度開いてから、もう一度このコマンド（/setup-start）を実行してください」と案内

---

## Step 4: Git の確認

**AIが自動実行する内容:**

1. 以下を実行してバージョンを確認する:

```bash
git --version
```

2. 結果を確認して以下を判定:
   - バージョンが表示された場合 → インストール済み
   - コマンドが見つからない場合 → 未インストール

### Git がインストール済みの場合

表示例:
```text
Git 2.x.x が見つかりました。問題ありません。
```
→ Step 5 へ自動で進む

### Git が未インストールの場合

**Mac の場合の案内:**
```text
Git をインストールします。
AIが自動でインストールコマンドを実行します。
ポップアップが表示されたら「インストール」をクリックしてください。
```

```bash
AIが実行: xcode-select --install
# Xcode コマンドラインツールのインストーラーが起動する。ユーザーはポップアップで「インストール」をクリックするだけ
```

インストール完了後、AIが `git --version` を再実行して確認。

**Windows の場合の案内:**
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
2. ダウンロードが自動で始まります（始まらない場合は「Click here to download」をクリック）
3. ダウンロードされた .exe ファイルを開いてインストーラーを起動
4. 全てデフォルト設定のまま「Next」→「Install」をクリック
5. 完了したら、ここに「終わった」と入力してください
```

```bash
AIが実行: start https://git-scm.com/download/win
```

**インストール完了後:**
AIが `git --version` を再実行してインストールを確認。
- 成功 → 「Git のインストールが完了しました！」と表示して Step 5 へ
- 失敗 → 「Cursor を一度閉じて再度開いてから、もう一度このコマンド（/setup-start）を実行してください」と案内

---

## Step 5: GitHub CLI の確認

**AIが自動実行する内容:**

1. 以下を実行してバージョンを確認する:

```bash
gh --version
```

2. 結果を確認して以下を判定:
   - バージョンが表示された場合 → インストール済み
   - コマンドが見つからない場合 → 未インストール

### GitHub CLI がインストール済みの場合

表示例:
```text
GitHub CLI 2.x.x が見つかりました。問題ありません。
```
→ 完了セクションへ

### GitHub CLI が未インストールの場合

**AskQuestionの設定:**
```json
{
  "title": "GitHub CLI のインストールが必要です",
  "questions": [{
    "id": "gh_install",
    "prompt": "GitHub CLI がインストールされていません。インストール方法を案内します。",
    "options": [
      {"id": "guide_me", "label": "インストール手順を教えて"},
      {"id": "already_done", "label": "別の方法でインストール済み（再確認して）"}
    ]
  }]
}
```

(guide_me → OS に応じた案内を表示)
(already_done → `gh --version` を再実行して確認)

**Mac の場合の案内:**

まず以下を実行して Homebrew がインストール済みか確認する:

```bash
brew --version
```

Homebrew がある場合:
```text
AIが自動でインストールを実行します。少しお待ちください...
```

```bash
AIが実行: brew install gh
```

Homebrew がない場合:
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
2. 開いたページで「Download for macOS」をクリック
3. ダウンロードされた .pkg ファイルをダブルクリック
4. インストーラーの指示に従って「続ける」→「インストール」をクリック
5. 完了したら、ここに「終わった」と入力してください
```

```bash
AIが実行: open https://cli.github.com/
```

**Windows の場合の案内:**
```text
以下の手順でインストールしてください:

1. AIがブラウザを自動で開きます（少しお待ちください）
2. 開いたページで「Download for Windows」をクリック
3. ダウンロードされた .msi ファイルを開いてインストーラーを起動
4. 全てデフォルト設定のまま「Next」→「Install」をクリック
5. 完了したら、ここに「終わった」と入力してください
```

```bash
AIが実行: start https://cli.github.com/
```

**インストール完了後:**
AIが `gh --version` を再実行してインストールを確認。
- 成功 → 「GitHub CLI のインストールが完了しました！」と表示して完了セクションへ
- 失敗 → 「Cursor を一度閉じて再度開いてから、もう一度このコマンド（/setup-start）を実行してください」と案内

---

## よくあるトラブルと解決方法

**AskQuestionの設定:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "ブラウザが自動で開かない"},
      {"id": "trouble_2", "label": "インストールしたのに「見つからない」と言われる"},
      {"id": "trouble_3", "label": "インストーラーがエラーになる"},
      {"id": "trouble_4", "label": "Mac でポップアップが出ない（Git）"},
      {"id": "trouble_5", "label": "その他のトラブル"}
    ]
  }]
}
```

### トラブル1: 「ブラウザが自動で開かない」
**原因**: デフォルトブラウザの設定、またはセキュリティソフトのブロック
**解決方法**:
```text
ブラウザが開かない場合は、以下のURLを直接ブラウザのアドレスバーにコピー＆ペーストしてください:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git (Windows): https://git-scm.com/download/win
- GitHub CLI: https://cli.github.com/
```

### トラブル2: 「インストールしたのに見つからないと言われる」
**原因**: Cursor（ターミナル）がインストール情報を認識していない
**解決方法**:
```text
Cursor を一度完全に閉じて（右上の × ボタン）、再度開いてください。
その後、もう一度 /setup-start を実行してください。
これでほとんどの場合解決します。
```

### トラブル3: 「インストーラーがエラーになる」
**原因**: 権限不足、ディスク容量不足、またはネットワーク問題
**解決方法**:
AIが以下を自動診断:

```bash
# 1. ディスク空き容量を確認
df -h /                          # Mac / Linux
wmic logicaldisk get freespace   # Windows

# 2. ネットワーク接続を確認
ping -c 1 google.com             # Mac / Linux
ping -n 1 google.com             # Windows
```

3. 結果に応じた具体的な解決策を提示

### トラブル4: 「Mac で Git のポップアップが出ない」
**原因**: Xcode コマンドラインツールが既にインストール済み、または別の問題
**解決方法**:
AIが `xcode-select -p` を実行してパスを確認。
パスが表示されれば既にインストール済み。`git --version` を再確認する。

### トラブル5: 「その他のトラブル」
**解決方法**:
```text
どのような問題が起きていますか？画面に表示されているエラーメッセージや状況を教えてください。
AIが原因を診断して解決策を提示します。
```

---

## チェックポイント

AIが全項目を自動で確認し、結果を一覧表示する:

| 項目 | 状態 | バージョン |
|------|------|-----------|
| OS | (AIが自動表示) | Mac / Windows |
| Python | (AIが自動表示) | 3.x.x |
| Node.js | (AIが自動表示) | 20.x.x |
| Git | (AIが自動表示) | 2.x.x |
| GitHub CLI | (AIが自動表示) | 2.x.x |

全て OK の場合のみ次のステップへ進める。

---

## 次のステップ

**全てインストール済みの場合:**

```text
おめでとうございます！必要なソフトウェアが全て揃いました！

次は GitHub の設定を行います。
Cursor のチャットに以下を入力してください:

/setup-github
```

**未インストールの項目がある場合:**

```text
以下の項目がまだインストールされていません:
- (未インストールの項目を列挙)

上記のインストールを完了してから、もう一度 /setup-start を実行してください。
```

---

## 完了処理

**AIが自動実行する内容:**
1. 以下のコマンドで進捗を更新:
   ```bash
   uv run python tools/setup_progress.py complete setup-start --details "{\"python\":\"$(python3 --version 2>&1 | awk '{print $2}')\",\"node\":\"$(node --version 2>&1)\",\"git\":\"$(git --version 2>&1 | awk '{print $3}')\"}"
   ```
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/setup-github` でGitHub設定を行いましょう」
