# Fetch Slides - Google Slides取得

Google Slidesのプレゼンテーション内容をMarkdown/JSON形式で取得します。

## 機能

- スライド内のテキスト抽出
- テーブル（表）のMarkdown変換
- スピーカーノートの取得
- メタデータ（作成日時、更新者等）の付与

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **URL/ID**: Google SlidesのURLまたはプレゼンテーションID
- **出力形式**: markdown / json（デフォルト: markdown）
- **出力先**: ファイルパス（省略時は画面表示）

### Step 2: ツールの実行

Google Slides API を使って内容を取得します。`/setup-google-api` で認証設定後、以下の手順で実行してください：

```bash
# Google API認証の確認・設定
uv run python tools/api_setup_wizard.py guide google
```

Claude Code / Cursor の対話機能を使い、URLまたはIDを指定してスライド内容を取得・整形します。

### Step 3: 結果の表示

出力されたMarkdownまたはJSONをユーザーに提示します。

## 使用例

### URLから取得

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit
```

### IDから取得

```
/fetch-slides 1abc123xyz
```

### JSON形式で保存

```
/fetch-slides 1abc123xyz --output slides.json --format json
```

### Markdownファイルに保存

```
/fetch-slides https://docs.google.com/presentation/d/1abc123xyz/edit -o output/slides.md
```

## 出力形式

### Markdown

```markdown
---
id: 1abc123xyz
title: プレゼンテーションタイトル
created: 2026-01-15T10:00:00Z
modified: 2026-01-16T14:30:00Z
authors: user@example.com
total_slides: 10
---

# プレゼンテーションタイトル

## 目次

1. [はじめに](#slide-1)
2. [概要](#slide-2)
...

---

## Slide 1 {#slide-1}

スライドの内容...

> **Speaker Notes:**
> ここにスピーカーノートが表示されます

---

## Slide 2 {#slide-2}

...
```

### JSON

```json
{
  "id": "1abc123xyz",
  "title": "プレゼンテーションタイトル",
  "total_slides": 10,
  "slides": [
    {
      "number": 1,
      "content": ["スライドのテキスト..."],
      "speaker_notes": "スピーカーノート..."
    }
  ]
}
```

## 前提条件

Google API認証が必要です。以下のいずれかを設定してください：

1. **サービスアカウント**: `GCP_SA_KEY` 環境変数
2. **OAuth**: `token.json` ファイル

設定方法:

```bash
uv run python tools/api_setup_wizard.py guide google
```

## 関連コマンド

- `/api-setup-wizard` - Google API設定
- `/generate-slide` - スライド画像の生成
