---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "約35分"
level: "intermediate"
tags: ["agent", "skill", "skills"]
---

# 🎓 Lesson 6-2: Skill作成基本

## 📍 このセッションでやること

**Lesson 6-2: Skill開発** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | `skills/` に再利用可能なSkillを作成し、Codex / Claude Code / Cursor から参照できる形にする |
| 所要時間 | 約35分 |
| 使うスキル | SKILL.md, Python |
| 前提条件 | Lesson 6-1 完了、Python環境セットアップ済み |
| 教材ページ | [Module 6: エージェント開発](https://ai-agent.camp/ja/course/module-6) を並行参照 |

**このセッションの流れ:**
1. Skillディレクトリ構造の作成
2. SKILL.md とスクリプトの実装
3. 動作確認と利用ガイドへの反映

セッション終了時には、自作Skillが共通の `skills/` ディレクトリで管理できるようになっています。

> **💡 ヒント**: AIの応答が途中で止まった場合は「続きを表示して」「止まってるよ」と入力すると再開します。これはCursorの仕様で、故障ではありません。

---

## 🎯 準備チェック

まずは準備が整っているか確認しましょう。

**AskQuestionの設定:**
```json
{
  "title": "🎯 セッション開始前の確認",
  "questions": [{
    "id": "readiness",
    "prompt": "準備はできていますか？",
    "options": [
      {"id": "ready", "label": "準備OK！始めましょう"},
      {"id": "check_prereq", "label": "前提条件を確認したい"},
      {"id": "view_html", "label": "先に教材ページを見たい"},
      {"id": "different_lesson", "label": "別のレッスンに移動したい"}
    ]
  }]
}
```

(ready → Step 1へ)
(check_prereq → 前提条件の確認を実行)
(view_html → 教材ページのパスを案内)
(different_lesson → モジュール一覧を表示)

---

## 🚀 Step 1: Skillディレクトリ構造の作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Skillディレクトリ構造の作成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
skills/csv-analyzer ディレクトリを作成し、以下の構造を準備してください：

mkdir -p skills/csv-analyzer/scripts
mkdir -p skills/csv-analyzer/tests
mkdir -p skills/csv-analyzer/examples

touch skills/csv-analyzer/SKILL.md
touch skills/csv-analyzer/requirements.txt

ディレクトリ構造を確認してください。
```

**期待される結果**: Skillのディレクトリ構造が作成されます。

---

## 🚀 Step 2: SKILL.mdドキュメント作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: SKILL.mdドキュメント作成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
skills/csv-analyzer/SKILL.md ファイルを作成し、以下の内容を記述してください：

---
name: csv-analyzer
description: CSVファイルを分析し、統計情報とデータ型推定を行うSkill
version: 1.0.0
author: ユーザー名
dependencies:
  - python: "3.8+"
  - packages: ["pandas", "chardet"]
---

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

analyzer = CSVAnalyzer('data.csv')
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
uv sync
```
```

**期待される結果**: SKILL.md ドキュメントが作成されます。

---

## 🚀 Step 3: Python実装の作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: Python実装の作成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
skills/csv-analyzer/scripts/analyzer.py ファイルを作成し、以下の内容を記述してください：

import pandas as pd
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

class CSVAnalyzer:
    """CSVファイルを分析するクラス"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def analyze(self) -> Dict[str, Any]:
        """CSVファイルを分析"""
        df = pd.read_csv(self.file_path)
        file_size_mb = self.file_path.stat().st_size / (1024 * 1024)

        return {
            "filename": self.file_path.name,
            "rows": len(df),
            "columns": len(df.columns),
            "file_size_mb": round(file_size_mb, 2),
            "columns_info": self._analyze_columns(df)
        }

    def _analyze_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """各列を分析"""
        columns_info = []
        for col in df.columns:
            col_data = df[col]
            col_info = {
                "name": col,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isna().sum()),
                "unique_values": int(col_data.nunique())
            }

            # 数値列の場合は統計情報を追加
            if pd.api.types.is_numeric_dtype(col_data):
                col_info["stats"] = {
                    "min": float(col_data.min()) if not col_data.isna().all() else None,
                    "max": float(col_data.max()) if not col_data.isna().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isna().all() else None
                }

            columns_info.append(col_info)
        return columns_info

    def to_json(self, output_path: str = None) -> str:
        """分析結果をJSON形式で出力"""
        result = self.analyze()
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

        if output_path:
            Path(output_path).write_text(json_str, encoding='utf-8')

        return json_str

def main():
    parser = argparse.ArgumentParser(description="CSVファイルを分析")
    parser.add_argument("--input", required=True, help="入力CSVファイルパス")
    parser.add_argument("--output", help="出力JSONファイルパス（省略時は標準出力）")
    args = parser.parse_args()

    analyzer = CSVAnalyzer(args.input)
    result = analyzer.to_json(args.output)

    if not args.output:
        print(result)

if __name__ == "__main__":
    main()
```

**期待される結果**: CSVAnalyzer クラスが実装されます。

---

## 🚀 Step 4: requirements.txt作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: requirements.txt作成",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
skills/csv-analyzer/requirements.txt ファイルを作成し、以下の内容を記述してください：

pandas>=2.0.0
chardet>=5.0.0
pytest>=7.4.0
```

**期待される結果**: 依存関係ファイルが作成されます。

---

## 🚀 Step 5: テストの作成と実行

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: テストの作成と実行",
  "questions": [{
    "id": "step_action",
    "prompt": "このステップをどうしますか？",
    "options": [
      {"id": "practice", "label": "このまま進める"},
      {"id": "review", "label": "例だけ確認する"},
      {"id": "skip", "label": "スキップする"}
    ]
  }]
}
```

**選択後の案内（例）**:
入力内容:
```
skills/csv-analyzer/tests/test_analyzer.py ファイルを作成し、以下の内容を記述してください：

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.analyzer import CSVAnalyzer

@pytest.fixture
def sample_csv():
    """テスト用CSVファイルを作成"""
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, None, 28],
        'score': [85.5, 90.0, 78.5, 82.0, 88.5]
    })
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.csv', delete=False, encoding='utf-8'
    ) as f:
        df.to_csv(f, index=False)
        return f.name

def test_analyze_basic(sample_csv):
    """基本的な分析テスト"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    assert result['rows'] == 5
    assert result['columns'] == 4
    assert 'columns_info' in result

def test_column_types(sample_csv):
    """列タイプの分析テスト"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    col_names = [col['name'] for col in result['columns_info']]
    assert 'id' in col_names
    assert 'name' in col_names

def test_null_detection(sample_csv):
    """欠損値検出テスト"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    age_col = next(col for col in result['columns_info'] if col['name'] == 'age')
    assert age_col['null_count'] == 1

def test_file_not_found():
    """ファイル未存在エラーテスト"""
    with pytest.raises(FileNotFoundError):
        CSVAnalyzer('nonexistent.csv')

その後、以下のコマンドでテストを実行してください：
cd skills/csv-analyzer && uv sync && pytest tests/ -v
```

**期待される結果**: テストが作成され、全テストがパスします。

---

## ⚠️ よくあるトラブルと解決方法

AskUserQuestion（AskQuestion）でトラブル内容を選んでもらい、押すだけで案内します。

**AskQuestionの設定例:**
```json
{
  "title": "トラブル内容を選択",
  "questions": [{
    "id": "trouble",
    "prompt": "当てはまる内容を1つ選んでください",
    "options": [
      {"id": "trouble_1", "label": "モジュールがインポートできない"},
      {"id": "trouble_2", "label": "pandasがインストールされていない"},
      {"id": "trouble_3", "label": "テストが失敗する"},
      {"id": "trouble_4", "label": "JSON出力が文字化けする"}
    ]
  }]
}
```


### トラブル1: モジュールがインポートできない
**原因**: Pythonパスが通っていない
**解決プロンプト**:
```
sys.path にスクリプトディレクトリを追加してください：
sys.path.insert(0, str(Path(__file__).parent.parent))
または PYTHONPATH 環境変数を設定してください。
```

### トラブル2: pandasがインストールされていない
**原因**: 依存パッケージ未インストール
**解決プロンプト**:
```
uv sync を実行してください。
仮想環境を使用している場合は、正しい環境がアクティブか確認してください。
```

### トラブル3: テストが失敗する
**原因**: テストファイルのパスが間違っている
**解決プロンプト**:
```
pytest を実行するディレクトリを確認してください。
テストファイルが tests/ ディレクトリにあるか確認してください。
```

### トラブル4: JSON出力が文字化けする
**原因**: エンコーディングがUTF-8でない
**解決プロンプト**:
```
json.dumps() で ensure_ascii=False を指定してください。
ファイル出力時は encoding='utf-8' を指定してください。
```

---

## ✅ チェックポイント
- [ ] ディレクトリ構造が作成されている
- [ ] SKILL.md でドキュメント化されている
- [ ] analyzer.py が実装されている
- [ ] requirements.txt が作成されている
- [ ] テストが全てパスする


---

## 📋 成果物プレビュー

### 期待される出力
```
📁 output/
└── {プロジェクト名}/  (エージェント/コード成果物)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/{プロジェクト名}/

# 冒頭を確認（最初の30行）
head -30 output/{プロジェクト名}/
```

> 💡 全文を確認: `cat output/{プロジェクト名}/` で全文表示できます

---

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: skills/csv-analyzer/ ディレクトリが正しく作成され、pytest テストが全てパスするか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これでこのセクションは完了です。次のセクションを始めるか、新しいウィンドウを開いて、新しいセクションを開始してください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_auto", "label": "次のセクションを開始（/next_lesson）"},
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-6-3）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-6-3
- finish → 終了
