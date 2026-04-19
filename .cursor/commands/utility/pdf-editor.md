# PDF Page Editor

PDFのテキストを編集（修正・削除）するコマンドです。
AskQuestion形式でインタラクティブにページ・テキスト選択を行います。

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **PDFファイルパス**: 編集対象のPDF（必須）
- **編集内容**: どのテキストをどう変更するか（任意、後で確認可）

---

### Step 2: PDF解析

```bash
uv run python tools/pdf_page_editor.py analyze "{PDFファイルパス}"
```

- ワークスペースが作成されます（`{PDF名}_workspace/`）
- 各ページのテキスト要素が解析されます
- `analysis.yaml` からページ一覧を取得してください

---

### Step 3: ページ選択（AskQuestion）

**ask_question ツールを使用してページを選択:**

```yaml
title: "編集するページを選択"
questions:
  - id: "page_select"
    prompt: "どのページを編集しますか？"
    options:
      # analysis.yaml から動的に生成
      # 例:
      - id: "page_1"
        label: "ページ1 - {最初のテキスト要素の冒頭20文字}..."
      - id: "page_2"
        label: "ページ2 - {最初のテキスト要素の冒頭20文字}..."
      # ... 全ページ分
    allow_multiple: false
```

> **実装ヒント**: `analysis.yaml` の各ページから最初のテキスト要素を取得し、
> そのテキストの冒頭20文字程度をラベルに含めると、ユーザーがページを識別しやすくなります。

---

### Step 4: テキスト一覧表示

```bash
uv run python tools/pdf_page_editor.py show {ワークスペース} {ページ番号}
```

- そのページの全テキスト要素を**番号付きリスト**で表示
- 例：
  ```
  ページ3のテキスト要素:
  [1] AIデータ分析の新しい標準
  [2] 株式会社○○
  [3] 2024年12月
  [4] 目次
  ...
  ```

---

### Step 5: テキスト選択（AskQuestion）

**ask_question ツールを使用して選択方法を確認:**

```yaml
title: "編集するテキストを選択"
questions:
  - id: "text_select_method"
    prompt: "テキストの選択方法を選んでください"
    options:
      - id: "by_number"
        label: "番号で選択（上の一覧から番号を指定）"
      - id: "by_input"
        label: "テキストを直接入力"
    allow_multiple: false
```

#### 番号で選択の場合

**続けて ask_question ツールでテキスト番号を選択:**

```yaml
title: "テキスト番号を選択"
questions:
  - id: "text_number"
    prompt: "編集するテキストの番号を選んでください"
    options:
      # Step 4 で表示した一覧から動的に生成
      - id: "text_1"
        label: "[1] AIデータ分析の新しい標準"
      - id: "text_2"
        label: "[2] 株式会社○○"
      # ... 全テキスト要素分
    allow_multiple: false
```

#### テキストを直接入力の場合

ユーザーに編集対象のテキストを入力してもらいます。

---

### Step 6: 編集タイプ選択（AskQuestion）

**ask_question ツールを使用して編集タイプを選択:**

```yaml
title: "編集の種類を選択"
questions:
  - id: "edit_type"
    prompt: "どのような編集を行いますか？"
    options:
      - id: "replace"
        label: "テキスト置換（別のテキストに変更）"
      - id: "delete"
        label: "テキスト削除（テキストを消す）"
      - id: "prompt"
        label: "自由記述（AIに編集を指示）"
    allow_multiple: false
```

#### 編集タイプ別の追加入力

- **置換の場合**: 新しいテキストを入力してもらう
- **削除の場合**: 確認のみ（追加入力なし）
- **自由記述の場合**: 編集指示を入力してもらう

---

### Step 7: 編集実行

```bash
# テキスト置換
uv run python tools/pdf_page_editor.py edit {ワークスペース} {ページ番号} --replace "{旧テキスト}" "{新テキスト}"

# テキスト削除
uv run python tools/pdf_page_editor.py edit {ワークスペース} {ページ番号} --delete "{削除するテキスト}"

# 自由記述
uv run python tools/pdf_page_editor.py edit {ワークスペース} {ページ番号} --prompt "{編集指示}"
```

---

### Step 8: 結果表示

編集完了後、以下をユーザーに表示：

```
✅ 編集完了

元画像: {ワークスペース}/pages/page_{番号:03d}.png
編集後: {ワークスペース}/edited/page_{番号:03d}_edited.png
```

- 必要に応じて `open` コマンドで画像を開く

---

### Step 9: 次のアクション選択（AskQuestion）

**ask_question ツールを使用して次のアクションを確認:**

```yaml
title: "次のアクション"
questions:
  - id: "next_action"
    prompt: "次に何をしますか？"
    options:
      - id: "same_page"
        label: "同じページの別のテキストを編集"
      - id: "other_page"
        label: "別のページを編集"
      - id: "rebuild"
        label: "編集を完了してPDFを再構成"
      - id: "exit"
        label: "編集を終了（再構成なし）"
    allow_multiple: false
```

#### アクション別の遷移

- **同じページの別のテキストを編集**: → Step 4 に戻る
- **別のページを編集**: → Step 3 に戻る
- **編集を完了してPDFを再構成**: → Step 10 へ
- **編集を終了（再構成なし）**: → 完了

---

### Step 10: PDF再構成（オプション）

```bash
uv run python tools/pdf_page_editor.py rebuild {ワークスペース}
```

- 編集済みページを含む新しいPDFが生成されます
- 出力: `{ワークスペース}/{PDF名}_edited.pdf`

---

## フロー図

```
PDF解析 → [AskQuestion] ページ選択
              ↓
         テキスト一覧表示
              ↓
    [AskQuestion] テキスト選択方法
         ↓              ↓
     番号選択      直接入力
         ↓              ↓
  [AskQuestion]    テキスト入力
   番号選択
         ↓              ↓
    [AskQuestion] 編集タイプ選択
              ↓
         編集実行
              ↓
         結果表示
              ↓
    [AskQuestion] 次のアクション
     ↓      ↓       ↓        ↓
  同ページ 別ページ  再構成   終了
     ↓      ↓       ↓
   Step4  Step3  Step10
```

---

## 使用例

```
/pdf-editor docs/presentation.pdf
```

→ PDF解析 → [AskQuestion] ページ選択 → テキスト一覧表示 → [AskQuestion] テキスト選択 → [AskQuestion] 編集タイプ → 編集実行 → [AskQuestion] 次のアクション

---

## ワークスペース構造

```
{PDF名}_workspace/
├── pages/           # 抽出したページ画像
│   ├── page_001.png
│   └── ...
├── edited/          # 編集済み画像
│   ├── page_001_edited.png
│   └── ...
├── analysis.yaml    # 解析結果（テキスト要素）
└── {PDF名}_edited.pdf  # 最終出力
```

---

## 注意事項

- `GEMINI_API_KEY` または `GOOGLE_API_KEY` が必要
- 画像編集はAI生成のため、フォント・レイアウトが微妙に変わる可能性あり
- 依存: `pdf2image`, `img2pdf`, `tqdm`, `PyYAML`, `Pillow`, `google-genai`
