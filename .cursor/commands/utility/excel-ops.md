# Excel Operations - Excel操作

openpyxlを使用してExcelファイルの読み取り・書き込み・分析を行います。

## 機能

- シートの読み取り・Markdown変換
- ワークブック構造の分析
- 新規Excelファイルの作成
- セルの更新

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **コマンド**: read / to-markdown / analyze / write / list-sheets
- **ファイルパス**: Excelファイルのパス
- **シート名**: 特定シートを指定する場合
- **出力先**: ファイルパス（省略時は画面表示）

### Step 2: ツールの実行

```bash
# 読み取り
uv run python tools/excel_ops.py read <file.xlsx>

# Markdown変換
uv run python tools/excel_ops.py to-markdown <file.xlsx>

# 分析
uv run python tools/excel_ops.py analyze <file.xlsx>

# シート一覧
uv run python tools/excel_ops.py list-sheets <file.xlsx>
```

### Step 3: 結果の表示

出力されたデータをユーザーに提示します。

## オプション

### read コマンド

| オプション | 説明 |
|------------|------|
| `--sheet TEXT` / `-s` | 特定シートを読み取り |
| `--max-rows INT` / `-n` | 最大行数（デフォルト: 100） |
| `--format TEXT` / `-f` | 出力形式: text / json |

### to-markdown コマンド

| オプション | 説明 |
|------------|------|
| `--sheet TEXT` / `-s` | 特定シートを変換 |
| `--max-rows INT` / `-n` | 最大行数 |
| `--output PATH` / `-o` | 出力ファイルパス |

### write コマンド

| オプション | 説明 |
|------------|------|
| `--data JSON` / `-d` | JSON形式のデータ（必須） |
| `--output PATH` / `-o` | 別ファイルに出力 |

## 使用例

### ファイル読み取り

```
/excel-ops read report.xlsx
```

### 特定シートをMarkdownに変換

```
/excel-ops to-markdown data.xlsx --sheet "売上データ" -o sales.md
```

### ワークブック分析

```
/excel-ops analyze financial_report.xlsx --format json
```

### 新規ファイル作成

```
/excel-ops write new.xlsx --data '{"headers":["名前","年齢"],"rows":[["田中",30],["佐藤",25]]}'
```

## 出力形式

### read（テキスト形式）

```
Sheet: Sheet1
Dimensions: A1:D100
Rows: 99

Headers: ['名前', '部署', '売上', '達成率']

Sample rows (first 5):
  1: ['田中太郎', '営業部', '1500000', '120%']
  2: ['佐藤花子', '企画部', '980000', '98%']
```

### to-markdown

```markdown
# report.xlsx

**Sheet**: Sheet1
**Dimensions**: A1:D100
**Rows**: 99 (max 100)

| 名前 | 部署 | 売上 | 達成率 |
|------|------|------|--------|
| 田中太郎 | 営業部 | 1500000 | 120% |
| 佐藤花子 | 企画部 | 980000 | 98% |
```

### analyze

```
📊 Analysis Report: report.xlsx
==================================================
Sheets: 3
Total rows: 150
Estimated cells: 600

📋 Sheet1
   Dimensions: A1:D50
   Rows: 50, Columns: 4
   Headers: ['名前', '部署', '売上', '達成率']
```

## 前提条件

openpyxlライブラリが必要です：

```bash
pip install openpyxl
```

## 関連コマンド

- `/pptx-ops` - PowerPoint操作
- `/fetch-slides` - Google Slides取得
