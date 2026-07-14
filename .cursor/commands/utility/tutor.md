---
nonInteractiveMode: deferred
---

# Tutor - 学習コンテンツ生成

このコマンドは、`tools/tutor_generate.py` を使用して、様々な入力ソースから初学者向けの学習用HTMLを自動生成します。

## 機能

- **複数の入力ソース対応**: トピック / ファイル / テキスト / SpecStory
- 初学者向けの**チュートリアル形式HTML**を自動生成
- **参照したファイルを明示**
- **PlantUML処理フロー図**を表示

## 実行手順

### ステップ1: 入力ソースを選択

AskQuestionツールを使って、ユーザーに入力ソースを選択してもらってください：

```json
{
  "title": "学習コンテンツの入力ソースを選択",
  "questions": [{
    "id": "input_source",
    "prompt": "どの方法でチュートリアルを作成しますか？",
    "options": [
      {"id": "topic", "label": "トピック指定 - 任意のトピックについてチュートリアルを生成"},
      {"id": "file", "label": "ファイル指定 - コードファイルの使い方マニュアルを生成"},
      {"id": "text", "label": "テキスト指定 - 貼り付けたコード/テキストの解説を生成"},
      {"id": "specstory", "label": "SpecStory分析 - 会話履歴から学習ギャップを分析"}
    ]
  }]
}
```

### ステップ2: 入力ソースに応じた処理

#### トピック指定の場合

ユーザーにトピックを入力してもらい、以下を実行：

```bash
uv run python tools/tutor_generate.py --topic "トピック名"
```

例：
```bash
uv run python tools/tutor_generate.py --topic "Gitの基本"
uv run python tools/tutor_generate.py --topic "GitHub Actions入門"
uv run python tools/tutor_generate.py --topic "Pythonのデコレータ"
```

#### ファイル指定の場合

ユーザーにファイルを選択/入力してもらい、以下を実行：

```bash
uv run python tools/tutor_generate.py --file "ファイルパス"
```

例：
```bash
uv run python tools/tutor_generate.py --file "src/auth.py"
uv run python tools/tutor_generate.py --file "tools/guide_action.py"
```

#### テキスト指定の場合

ユーザーにテキスト/コードを入力してもらい、以下を実行：

```bash
uv run python tools/tutor_generate.py --text "入力テキスト"
```

#### SpecStory分析の場合

1. まずファイル一覧を取得：
```bash
uv run python tools/tutor_generate.py --list --json
```

2. AskQuestionでファイル選択UI表示：
```json
{
  "title": "分析するSpecStoryファイルを選択",
  "questions": [{
    "id": "specstory_files",
    "prompt": "分析するファイルを選択してください（複数選択可）",
    "options": [...],
    "allow_multiple": true
  }]
}
```

3. 選択されたファイルで実行：
```bash
uv run python tools/tutor_generate.py --names "file1.md,file2.md"
```

### ステップ3: 結果の確認

- 生成されたHTMLファイルのパスを確認し、ユーザーに報告してください。
- Live Serverで開く方法を案内してください。

## オプション一覧

| オプション | 説明 |
|-----------|------|
| `--topic`, `-t` | トピックを指定してチュートリアル生成 |
| `--file` | ファイルパスを指定してマニュアル生成 |
| `--text` | テキストを指定して解説生成 |
| `--specstory` | SpecStory履歴から学習ギャップ分析 |
| `--list`, `-l` | SpecStoryファイル一覧を表示 |
| `--json`, `-j` | JSON形式で出力（--listと併用） |
| `--names`, `-n` | ファイル名で指定（カンマ区切り） |
| `--select`, `-s` | 番号で指定（例: 1,2,3） |
| `--files`, `-f` | 分析するファイル数（デフォルト: 1） |
| `--output`, `-o` | 出力ファイルパス |

## 出力内容（チュートリアル形式）

- **入力ソース情報**: どのソースから生成したか
- **処理フロー図**: PlantUMLによる処理の可視化
- **概要**: トピックの紹介と学ぶ意義
- **前提知識**: 必要な基礎知識
- **セクション**: ステップバイステップの説明
  - 詳細な説明
  - コード例
  - ポイント・Tips
- **よくある間違いと注意点**: 初心者が陥りやすいポイント
- **まとめ**: 学習内容の確認
- **次のステップ**: 次に学ぶべきこと

## 使用例

### トピックからチュートリアル生成
```
/tutor
→ 「トピック指定」を選択
→ 「Dockerの基本」と入力
```

### ファイルからマニュアル生成
```
/tutor
→ 「ファイル指定」を選択
→ ファイルを選択または入力
```

### SpecStoryから学習ギャップ分析
```
/tutor
→ 「SpecStory分析」を選択
→ 分析するファイルを複数選択
```
