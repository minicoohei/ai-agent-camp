# Module 11: エージェント開発 - 成果物（Final）

カスタムCommand、Skill、MCPサーバー設定の例です。

## 学習目標
- Cursorでカスタムコマンドを作成できる
- Claude Code用のカスタムスキルを開発できる
- MCPサーバーを設定・活用できる
- エージェントのワークフローを設計できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `commands/` | コマンド | カスタムコマンド例 |
| `skills/` | スキル | カスタムスキル例 |
| `mcp-config.json` | JSON | MCP設定例 |
| `agent-workflow.md` | Markdown | ワークフロー設計 |

## エージェント開発の全体像

```
┌─────────────────────────────────────────────────────────┐
│  AIエージェント開発コンポーネント                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Commands（コマンド）                                │
│     ├─ .cursor/commands/      # Cursor用               │
│     ├─ commands/lesson/       # レッスン用             │
│     └─ commands/utility/      # ユーティリティ         │
│                                                         │
│  2. Skills（スキル）                                    │
│     ├─ .claude/skills/        # Claude Code用          │
│     ├─ SKILL.md               # スキル定義             │
│     └─ scripts/               # 実行スクリプト         │
│                                                         │
│  3. MCP（Model Context Protocol）                       │
│     ├─ .claude/mcp.json       # MCP設定                │
│     ├─ Tools                  # 実行アクション         │
│     ├─ Resources              # 読み取りデータ         │
│     └─ Prompts                # テンプレート           │
│                                                         │
│  4. Rules（ルール）                                     │
│     ├─ .cursor/rules/         # プロジェクトルール     │
│     └─ CLAUDE.md              # プロジェクト説明       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## カスタムCommand例

### .cursor/commands/project-setup.md

```markdown
---
description: 新規プロジェクトのセットアップを実行
---

# プロジェクトセットアップ

## 概要
新規プロジェクトの初期セットアップを自動化するコマンドです。

## 実行内容

1. **ディレクトリ構造の作成**
   ```
   project/
   ├── src/
   ├── tests/
   ├── docs/
   └── .github/workflows/
   ```

2. **設定ファイルの生成**
   - .gitignore
   - README.md
   - requirements.txt / package.json

3. **Git初期化**
   - git init
   - 初期コミット

## パラメータ

- **project_name**: プロジェクト名（必須）
- **language**: Python / Node.js / Go（デフォルト: Python）
- **with_ci**: CI/CD設定を含めるか（デフォルト: true）

## 使用例

```
/project-setup my-new-project --language Python --with_ci true
```

## 実行後の確認

- [ ] ディレクトリ構造が作成された
- [ ] 設定ファイルが生成された
- [ ] Gitリポジトリが初期化された
- [ ] 初期コミットが作成された
```

### .cursor/commands/code-review.md

```markdown
---
description: コードレビューを実行
---

# コードレビュー

## 概要
指定されたファイルまたはディレクトリのコードレビューを実行します。

## チェック項目

### 1. コード品質
- 可読性
- 命名規則
- コメントの適切さ
- 重複コードの検出

### 2. セキュリティ
- 入力バリデーション
- 機密情報のハードコーディング
- SQLインジェクション対策

### 3. パフォーマンス
- N+1問題
- 不要なループ
- メモリリーク

### 4. ベストプラクティス
- エラーハンドリング
- テストカバレッジ
- ドキュメント

## 使用例

```
/code-review src/main.py
/code-review src/
```

## 出力形式

- 問題の重要度（Critical/Major/Minor）
- 該当箇所（ファイル名:行番号）
- 問題の説明
- 修正提案
```

## カスタムSkill例

### .claude/skills/data-analyzer/SKILL.md

```markdown
# Data Analyzer Skill

## 概要
CSVファイルやJSONデータを分析し、サマリーレポートを生成するスキルです。

## 機能
- データ読み込み（CSV, JSON, Excel）
- 基本統計量の算出
- 欠損値・外れ値の検出
- 可視化チャートの生成
- レポート出力（HTML/PDF）

## 使用方法

```bash
# 基本的な分析
python .claude/skills/data-analyzer/scripts/analyze.py \
  --input data.csv \
  --output report.html

# 詳細オプション
python .claude/skills/data-analyzer/scripts/analyze.py \
  --input data.csv \
  --columns "売上,数量,日付" \
  --date-column "日付" \
  --output report.html \
  --format html
```

## 入力形式
- CSV（UTF-8, Shift-JIS対応）
- JSON
- Excel（.xlsx）

## 出力形式
- HTML（インタラクティブ）
- PDF
- Markdown
- JSON（分析結果のみ）

## 依存関係
- pandas
- plotly
- numpy
```

### .claude/skills/data-analyzer/scripts/analyze.py

```python
#!/usr/bin/env python3
"""データ分析スキル"""
import pandas as pd
import numpy as np
import json
import argparse
from pathlib import Path

def load_data(file_path: str) -> pd.DataFrame:
    """データを読み込み"""
    suffix = Path(file_path).suffix.lower()
    
    if suffix == '.csv':
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except:
            return pd.read_csv(file_path, encoding='shift-jis')
    elif suffix == '.json':
        return pd.read_json(file_path)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")

def basic_stats(df: pd.DataFrame) -> dict:
    """基本統計量を算出"""
    stats = {
        'shape': {'rows': df.shape[0], 'columns': df.shape[1]},
        'columns': list(df.columns),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing': df.isnull().sum().to_dict(),
        'numeric_summary': {}
    }
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        stats['numeric_summary'][col] = {
            'mean': df[col].mean(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'median': df[col].median()
        }
    
    return stats

def generate_report(df: pd.DataFrame, stats: dict, output_path: str):
    """HTMLレポートを生成"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>データ分析レポート</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background: #4a5568; color: white; }}
        </style>
    </head>
    <body>
        <h1>データ分析レポート</h1>
        
        <h2>基本情報</h2>
        <ul>
            <li>行数: {stats['shape']['rows']:,}</li>
            <li>列数: {stats['shape']['columns']}</li>
        </ul>
        
        <h2>カラム情報</h2>
        <table>
            <tr><th>カラム名</th><th>データ型</th><th>欠損数</th></tr>
            {''.join(f"<tr><td>{col}</td><td>{stats['dtypes'][col]}</td><td>{stats['missing'][col]}</td></tr>" for col in stats['columns'])}
        </table>
        
        <h2>数値カラムの統計</h2>
        <table>
            <tr><th>カラム</th><th>平均</th><th>標準偏差</th><th>最小</th><th>最大</th></tr>
            {''.join(f"<tr><td>{col}</td><td>{s['mean']:.2f}</td><td>{s['std']:.2f}</td><td>{s['min']:.2f}</td><td>{s['max']:.2f}</td></tr>" for col, s in stats['numeric_summary'].items())}
        </table>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"レポート生成完了: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    df = load_data(args.input)
    stats = basic_stats(df)
    generate_report(df, stats, args.output)
```

## MCP設定例

### .claude/mcp.json

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"],
      "description": "ファイルシステムアクセス（指定ディレクトリのみ）"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub操作（Issue, PR, リポジトリ）"
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      },
      "description": "Slackメッセージ検索・送信"
    },
    "postgresql": {
      "command": "npx",
      "args": ["-y", "@anthropics/mcp-server-postgres", "${DATABASE_URL}"],
      "description": "PostgreSQLクエリ実行"
    }
  }
}
```

## エージェントワークフロー設計

```markdown
# 週次レポート自動生成ワークフロー

## トリガー
- 毎週金曜 17:00（スケジュール）
- 手動実行（/weekly-report）

## ステップ

1. **データ収集**（並列実行）
   - GitHub: 今週のコミット、PR、Issue
   - Slack: 重要チャンネルのサマリー
   - Notion: タスク完了状況

2. **分析**
   - 進捗率の計算
   - ブロッカーの特定
   - トレンド分析

3. **レポート生成**
   - Markdownレポート作成
   - チャート生成（PlantUML）
   - PDF出力

4. **配信**
   - Slackチャンネルに投稿
   - メール送信（オプション）
   - Notionページに保存

## エラーハンドリング
- API失敗時: リトライ（3回）
- データ不足時: 部分レポート生成
- 致命的エラー: Slackアラート
```

## チェックリスト

- [ ] カスタムコマンドが作成されている
- [ ] スキルが正しく動作する
- [ ] MCP設定が完了している
- [ ] ワークフローが設計されている
- [ ] エラーハンドリングが実装されている

## 関連レッスン

- `/start-11-1`: Custom Command作成基本
- `/start-11-2`: Skill作成基本
- `/start-11-3`: MCP設定
- `/start-11-4`: ワークフロー設計
- `/start-11-5`: エージェント統合

## 参考リンク

- [Cursor Commands Documentation](https://docs.cursor.sh/)
- [Claude Skills Guide](https://docs.anthropic.com/)
- [MCP Official](https://modelcontextprotocol.io/)
