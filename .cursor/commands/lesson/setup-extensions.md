---
description: "Lesson command"
duration: "約5分"
prerequisites: ["Cursor が起動している"]
level: "beginner"
tags: ["setup", "extensions"]
---

# /setup-extensions -- 拡張機能の自動セットアップ

## Step 0: セットアップ進捗の確認

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py show --current setup-extensions` を実行して進捗を表示
2. 既にインストール済みの拡張機能を確認し、全て揃っていれば「拡張機能は既にインストール済みです。スキップしますか？」と確認

## このコマンドの役割

Cursor / VS Code の拡張機能を**AIが自動でチェック・インストール**します。
ユーザーがターミナルを操作する必要はありません。全てAIが裏側で実行します。

| 項目 | 内容 |
|------|------|
| ゴール | 研修に必要な拡張機能を全て自動インストールする |
| 所要時間 | 約5分 |
| 前提条件 | Cursor（または VS Code）が起動している |
| ユーザー操作 | ボタンを押すだけ（CLIコマンドの入力は不要） |

> **ポイント**: このコマンドで行う操作は全てAIが自動実行します。ターミナルにコマンドを打つ必要はありません。

---

## 準備チェック

**AskQuestionの設定:**
```json
{
  "title": "拡張機能セットアップを始めます",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "始めましょう"},
      {"id": "what_is_this", "label": "拡張機能って何？先に説明を見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready -> Step 1 へ)
(what_is_this -> 以下を表示)

> **拡張機能とは？**
> Cursor（エディタ）に追加できる「便利機能パック」のようなものです。
> 例えば「Python拡張機能」を入れると、Pythonコードの色分け表示や自動補完が使えるようになります。
> このセットアップでは、研修で使う拡張機能をAIが自動でインストールします。

(different_lesson -> モジュール一覧を表示)

---

## Step 1: 現在の拡張機能を確認

**AIが自動実行すること:**

1. 以下のコマンドを**AIが裏側で**実行して、インストール済みの拡張機能一覧を取得する:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

2. 取得した一覧を「見やすい表形式」でユーザーに表示する:
```text
現在インストール済みの拡張機能:
| # | 拡張機能ID | 説明 |
|---|-----------|------|
| 1 | ms-python.python | Python |
| 2 | ... | ... |

合計: XX 個の拡張機能がインストールされています。
```

3. コマンドが失敗した場合（`cursor` も `code` も見つからない場合）:
   - 「Cursorのコマンドラインツールが見つかりません」と案内
   - **Cursorの場合**: 「Cursorメニュー > コマンドパレット（Cmd+Shift+P / Ctrl+Shift+P） > "Shell Command: Install 'cursor' command" を選択してください」とGUI手順を案内
   - **VS Codeの場合**: 「コマンドパレット > "Shell Command: Install 'code' command in PATH" を選択してください」とGUI手順を案内
   - 解決後、再度 Step 1 を実行

**注意: ユーザーにはコマンドを打たせない。AIが自動で実行して結果を表示する。**

---

## Step 2: 必須拡張機能の自動インストール

**AIが自動実行すること:**

1. 以下の「必須拡張機能リスト」と Step 1 の結果を照合し、不足している拡張機能を特定する:

| 拡張機能ID | 用途 |
|-----------|------|
| `marp-team.marp-vscode` | Markdownでプレゼン資料を作成する（Marp） |
| `hediet.vscode-drawio` | エディタ内で図表を作成・編集する（Draw.io） |
| `jebbs.plantuml` | テキストからUML図を自動生成する（PlantUML） |
| `nicepkg.aide-pro` | AI開発アシスタント（AIDE Pro） |
| `ms-python.python` | Pythonコードの実行・デバッグ |
| `ms-python.vscode-pylance` | Pythonの高精度な補完・型チェック |
| `esbenp.prettier-vscode` | コードの自動整形（Prettier） |

2. 不足している拡張機能がある場合、ユーザーに報告してからインストールする:
```text
以下の拡張機能が未インストールです。自動でインストールします:
- marp-team.marp-vscode（Markdownプレゼン）
- hediet.vscode-drawio（図表エディタ）

インストール中...
```

3. 各拡張機能を以下のコマンドで**AIが裏側で**インストール:
```bash
cursor --install-extension {拡張機能ID} 2>/dev/null || code --install-extension {拡張機能ID}
```

4. 全てインストール済みの場合:
```text
必須拡張機能は全てインストール済みです（7/7）。
```

5. インストール結果を1つずつ報告:
```text
| 拡張機能 | 状態 |
|---------|------|
| Marp | インストール完了 |
| Draw.io | インストール完了 |
| PlantUML | 既にインストール済み |
| ... | ... |
```

**注意: インストールコマンドはAIが自動実行する。ユーザーには結果のみ表示する。**

---

## Step 3: 推奨拡張機能の案内

**AskQuestionの設定:**
```json
{
  "title": "推奨拡張機能もインストールしますか？",
  "questions": [{
    "id": "optional_install",
    "prompt": "以下の拡張機能は必須ではありませんが、あると便利です。インストールしますか？\n- Git Graph: Gitの履歴をビジュアルに表示\n- GitLens: 各行の変更履歴を表示\n- Markdown All in One: Markdownの便利機能まとめ",
    "options": [
      {"id": "yes_all", "label": "全部インストールする"},
      {"id": "choose", "label": "選んでインストールしたい"},
      {"id": "skip", "label": "今はスキップする"}
    ]
  }]
}
```

(yes_all -> 以下を全て自動インストール)
(choose -> 個別に AskQuestion で選択させる)
(skip -> Step 4 へ)

**推奨拡張機能リスト:**

| 拡張機能ID | 用途 |
|-----------|------|
| `mhutchie.git-graph` | Gitの履歴をグラフ表示（ブランチの流れが一目でわかる） |
| `eamodio.gitlens` | 各行の最終変更者・日時を表示 |
| `yzhang.markdown-all-in-one` | Markdown編集の便利機能（目次自動生成、ショートカットなど） |

**AIが自動実行すること:**
- 選択された拡張機能を `cursor --install-extension {ID} 2>/dev/null || code --install-extension {ID}` で自動インストール
- 結果を表形式で報告

**(choose の場合) AskQuestionの設定:**
```json
{
  "title": "インストールする拡張機能を選択",
  "questions": [
    {
      "id": "git_graph",
      "prompt": "Git Graph（Gitの履歴をビジュアル表示）をインストールしますか？",
      "options": [
        {"id": "yes", "label": "インストールする"},
        {"id": "no", "label": "スキップ"}
      ]
    },
    {
      "id": "gitlens",
      "prompt": "GitLens（行ごとの変更履歴を表示）をインストールしますか？",
      "options": [
        {"id": "yes", "label": "インストールする"},
        {"id": "no", "label": "スキップ"}
      ]
    },
    {
      "id": "markdown",
      "prompt": "Markdown All in One（Markdown編集の便利機能）をインストールしますか？",
      "options": [
        {"id": "yes", "label": "インストールする"},
        {"id": "no", "label": "スキップ"}
      ]
    }
  ]
}
```

---

## Step 4: インストール結果確認

**AIが自動実行すること:**

1. 再度 `cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null` を**AIが裏側で**実行
2. 必須拡張機能が全てインストールされているか照合
3. 最終結果を表形式で表示:

```text
## 拡張機能セットアップ結果

### 必須拡張機能（7個）
| 拡張機能 | 用途 | 状態 |
|---------|------|------|
| Marp | プレゼン作成 | インストール済み |
| Draw.io | 図表作成 | インストール済み |
| PlantUML | UML図生成 | インストール済み |
| AIDE Pro | AI開発アシスタント | インストール済み |
| Python | Python開発 | インストール済み |
| Pylance | Python補完 | インストール済み |
| Prettier | コード整形 | インストール済み |

### 推奨拡張機能
| 拡張機能 | 状態 |
|---------|------|
| Git Graph | インストール済み / 未インストール |
| GitLens | インストール済み / 未インストール |
| Markdown All in One | インストール済み / 未インストール |
```

4. 全てインストール済みの場合: 「拡張機能のセットアップが完了しました」と表示
5. 失敗した拡張機能がある場合:
   - 「以下の拡張機能のインストールに失敗しました」と案内
   - GUI手順を案内: 「Cursorの拡張機能パネル（Cmd+Shift+X / Ctrl+Shift+X）を開いて、"{拡張機能名}" で検索し、手動でインストールしてください」

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
      {"id": "trouble_1", "label": "拡張機能のインストールが失敗する"},
      {"id": "trouble_2", "label": "cursorコマンドが見つからない"},
      {"id": "trouble_3", "label": "インストールしたのに使えない"},
      {"id": "no_trouble", "label": "問題なし、次へ進む"}
    ]
  }]
}
```

### トラブル1: 拡張機能のインストールが失敗する
**原因**: ネットワーク接続の問題、またはマーケットプレイスのサーバー障害
**AIが行う対処**:
1. ネットワーク接続を確認（AIが裏側で実行）:
```bash
# Mac / Linux
ping -c 1 marketplace.visualstudio.com

# Windows
ping -n 1 marketplace.visualstudio.com
```
2. 接続OKなら再試行
3. それでも失敗する場合 → GUI手順を案内:
   「拡張機能パネル（Cmd+Shift+X / Ctrl+Shift+X）を開いて、手動で検索・インストールしてください」

### トラブル2: cursorコマンドが見つからない
**原因**: Cursorのコマンドラインツールが PATH に追加されていない
**AIが行う対処**:
- 「コマンドパレット（Cmd+Shift+P / Ctrl+Shift+P）を開き、"Shell Command: Install" と入力して表示される項目を選択してください」とGUI手順を案内
- 「その後、Cursorを再起動してからこのコマンドを再実行してください」

### トラブル3: インストールしたのに使えない
**原因**: Cursorの再読み込みが必要
**AIが行う対処**:
- 「コマンドパレット（Cmd+Shift+P / Ctrl+Shift+P）を開き、"Developer: Reload Window" を選択してください」とGUI手順を案内

---

## チェックポイント

- [ ] 必須拡張機能7個が全てインストールされている
- [ ] 拡張機能パネル（Cmd+Shift+X / Ctrl+Shift+X）で確認できる
- [ ] Pythonファイルを開いたとき、構文ハイライトが有効になっている

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
      {"id": "security", "label": "セキュリティ設定をする（/setup-security）"},
      {"id": "check", "label": "環境の総合チェックをする（/check-setup）"},
      {"id": "lesson", "label": "レッスンを始める（/start-0-1）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

(security -> /setup-security を案内)
(check -> /check-setup を案内)
(lesson -> /start-0-1 を案内)
(finish -> 「お疲れさまでした」と表示)

---

## 完了処理

**AIが自動実行する内容:**
1. `uv run python tools/setup_progress.py complete setup-extensions` を実行して進捗を更新
2. 更新後の進捗サマリーが自動表示される
3. ユーザーに次のステップを案内: 「次は `/setup-security` でセキュリティ設定を行いましょう」
