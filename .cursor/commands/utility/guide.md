# Guide - 次のアクション提示

このコマンドは、`tools/guide_action.py` を使用して、SpecStory履歴から現在の状況を分析し、背景説明と次のアクションを提示します。

## 機能

- SpecStory履歴から現在の状況を分析
- **背景・文脈の説明**を提供
- **次のアクション**を明確に提示
- **次のAgentで使うプロンプト例**を生成
- **参照したファイルを明示**

## 実行手順

### ステップ1: SpecStoryファイル一覧を取得

まず、以下のコマンドでファイル一覧をJSON形式で取得してください：

```bash
uv run python tools/guide_action.py --list --json
```

### ステップ2: ファイル選択UIを表示

取得したJSONをもとに、AskQuestionツールを使ってユーザーにファイル選択UIを表示してください。

**AskQuestionの設定:**
- `title`: "分析するSpecStoryファイルを選択"
- `questions`: 取得したJSONの各ファイルを選択肢として提示
- `allow_multiple`: true（複数選択を許可）

例：
```json
{
  "title": "分析するSpecStoryファイルを選択",
  "questions": [{
    "id": "specstory_files",
    "prompt": "分析するファイルを選択してください（複数選択可）",
    "options": [
      {"id": "2025-12-18_10-00Z-example.md", "label": "2025-12-18 10:00Z - Example Title"},
      ...
    ],
    "allow_multiple": true
  }]
}
```

### ステップ3: 選択されたファイルで分析実行

ユーザーが選択したファイル名を使って、以下のコマンドを実行してください：

```bash
uv run python tools/guide_action.py --names "{選択されたファイル名をカンマ区切りで}" --output "{出力パス}"
```

例：
```bash
uv run python tools/guide_action.py --names "2025-12-18_10-00Z-example.md,2025-12-17_09-30Z-another.md"
```

### ステップ4: 結果の確認

- 生成されたHTMLファイルのパスを確認し、ユーザーに報告してください。
- Live Serverで開く方法を案内してください。

## オプション

| オプション | 説明 |
|-----------|------|
| `--list`, `-l` | SpecStoryファイル一覧を表示 |
| `--json`, `-j` | JSON形式で出力（--listと併用） |
| `--names`, `-n` | ファイル名で指定（カンマ区切り） |
| `--select`, `-s` | 番号で指定（例: 1,2,3） |
| `--files`, `-f` | 最新N件を分析（デフォルト: 3） |
| `--output`, `-o` | 出力ファイルパス |

## 出力内容

- **参照したSpecStoryファイル一覧**: どのファイルを分析したか
- **現在の状況サマリー**: 今何をしているか
- **背景説明**: なぜこの作業が必要か
- **次のアクション**: 具体的にやるべきこと
- **プロンプト例**: 新しいAgentに入力するプロンプト
- **期待される結果**: 何が達成されるか
