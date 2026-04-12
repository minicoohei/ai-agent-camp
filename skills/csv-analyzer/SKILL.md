---
name: csv-analyzer
description: |
  CSVファイルの行数・列数の取得、データ型推定、欠損値検出、数値列の統計情報を出力するスキル。
  「CSVを分析して」「CSVの中身を確認」「データの概要を見せて」等のリクエストで発動。
triggers:
  - csv-analyzer
  - CSV分析
  - CSVファイル解析
  - データ概要
  - 欠損値チェック
  - CSV統計
  - CSVプロファイリング
---

## トリガーワード
「CSV分析」「CSVファイル解析」「データ概要」「欠損値チェック」「CSV統計」

# CSV Analyzer Skill

## 概要
CSVファイルを分析し、統計情報とデータ型推定を行うSkillです。

## 機能
- 行数・列数の取得
- データ型推定（各列のデータ型を自動判定）
- 統計情報（数値列の基本統計量）
- 欠損値検出（NULLやNA値の検出）
- エンコーディング判定

## 使用方法

### コマンドライン実行
```bash
python skills/csv-analyzer/scripts/analyzer.py --input data.csv
```

### Python での利用
```python
from scripts.analyzer import CSVAnalyzer

analyzer = CSVAnalyzer("data.csv")
result = analyzer.analyze()
print(result)
```

## 出力形式
```json
{
  "filename": "data.csv",
  "rows": 1000,
  "columns": 5,
  "encoding": "utf-8",
  "file_size_mb": 2.5,
  "columns_info": []
}
```

## 依存関係
- pandas >= 2.0
- chardet >= 5.0

## インストール
```bash
pip install -r skills/csv-analyzer/requirements.txt
```
