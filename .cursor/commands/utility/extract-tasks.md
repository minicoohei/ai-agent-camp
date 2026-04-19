# Extract Tasks - タスク抽出

複数のデータソースからタスクを抽出し、優先順位付きで一覧化します。

## データソース

1. **Git** - 最新のコミット情報、git pull実行
2. **Activity Logger** - 直近の作業ログサマリー
3. **SpecStory** - 仕掛かりタスク（残TODOあり）
4. **Slack-sync** - 各ワークスペースの依頼事項
5. **Output** - カレンダー、Gmail、ボイスメモ
6. **Notion** - タスクデータベース（NOTION_API_KEY設定時）

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **日数**: SpecStory対象日数（デフォルト: 3）
- **ワークスペース**: Slack対象（デフォルト: all）
- **git pull**: 実行するか（デフォルト: yes）

### Step 2: ツールの実行

```bash
uv run python tools/extract_tasks.py --days {日数} --workspaces {ワークスペース}
```

### Step 3: 結果の表示

出力されたMarkdownをユーザーに提示します。

## オプション

| オプション | 説明 | デフォルト |
|------------|------|-----------|
| `--days INT` | SpecStory対象日数 | 3 |
| `--workspaces TEXT` | Slack対象（カンマ区切り） | all |
| `--output PATH` | 出力ファイルパス | stdout |
| `--format TEXT` | 出力形式: markdown / json / html | markdown |
| `--git-pull` | git pullを実行 | True |
| `--no-git-pull` | git pullをスキップ | - |
| `--notion-db TEXT` | NotionデータベースID | 環境変数 |
| `--no-notion` | Notion取得をスキップ | - |
| `--howtodo` | HowToDo手順を生成 | - |

## 使用例

### 基本実行

```
/extract-tasks
```

→ デフォルト設定（3日分、全ワークスペース）で実行

### 日数指定

```
/extract-tasks 7日分
```

→ `--days 7` で実行

### 特定ワークスペースのみ

```
/extract-tasks workspace-1とworkspace-2だけ
```

→ `--workspaces workspace-1,workspace-2` で実行

### git pullなし

```
/extract-tasks git pullしないで
```

→ `--no-git-pull` で実行

### JSON形式で出力

```
/extract-tasks json形式で
```

→ `--format json` で実行

## 出力形式

### 優先度A: 仕掛かりタスク
- SpecStoryから残TODOがあるセッション

### 優先度B: Slack依頼事項
- 各ワークスペースの直近メッセージ
- メンション付きを優先表示

### 優先度C: 定期タスク
- 本日のカレンダー予定
- 最近のメール
- ボイスメモ

## 注意事項

- git pullは`--no-git-pull`を指定しない限り自動実行されます
- Activity Loggerは直近2日分を表示
- 大量のデータがある場合は上位5件程度に絞って表示
