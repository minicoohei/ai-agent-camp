#!/usr/bin/env python3
"""
BigQueryデータ分析スクリプト（Final Example）

このスクリプトを実行すると、BigQueryに接続して
データ分析を実行し、レポートを生成します。

必要条件:
- gcloud CLI認証済み
- Python 3.9以上
- google-cloud-bigquery, pandas

使用方法:
    python bigquery_analysis.py --test          # 接続テスト
    python bigquery_analysis.py --eda           # EDA実行
    python bigquery_analysis.py --query "SQL"   # カスタムクエリ
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

try:
    from google.cloud import bigquery
    HAS_BIGQUERY = True
except ImportError:
    HAS_BIGQUERY = False
    print("Warning: google-cloud-bigquery がインストールされていません")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas がインストールされていません")


# 公開データセット設定
PUBLIC_DATASET = "bigquery-public-data.ga4_obfuscated_sample_ecommerce"
DEFAULT_TABLE = f"{PUBLIC_DATASET}.events_20210101"


class BigQueryAnalyzer:
    """BigQuery分析クラス"""
    
    def __init__(self, project_id: str = None):
        self.project_id = project_id
        self.client = None
        
        if HAS_BIGQUERY:
            try:
                # GOOGLE_APPLICATION_CREDENTIALSの競合を回避
                if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                    cred_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                    if not os.path.exists(cred_path):
                        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                
                self.client = bigquery.Client(project=project_id)
                print(f"✅ BigQuery接続成功: {self.client.project}")
            except Exception as e:
                print(f"⚠️ BigQuery接続エラー: {e}")
                print("モックモードで実行します")
    
    def test_connection(self) -> Dict[str, Any]:
        """接続テスト"""
        if self.client:
            query = """
            SELECT
                CURRENT_TIMESTAMP() as current_time,
                @@project_id as project_id,
                '接続成功' as status
            """
            result = self.client.query(query).to_dataframe()
            return {
                "status": "success",
                "project_id": result.iloc[0]["project_id"],
                "current_time": str(result.iloc[0]["current_time"])
            }
        else:
            return {
                "status": "mock",
                "project_id": "mock-project",
                "current_time": datetime.now().isoformat(),
                "message": "BigQueryクライアントが利用できないため、モック結果を返しています"
            }
    
    def run_query(self, sql: str) -> Any:
        """SQLクエリを実行"""
        if self.client and HAS_PANDAS:
            return self.client.query(sql).to_dataframe()
        else:
            print("モッククエリ実行:")
            print(sql)
            return None
    
    def get_dataset_info(self, table_id: str = DEFAULT_TABLE) -> Dict[str, Any]:
        """データセット情報を取得"""
        if self.client:
            try:
                table = self.client.get_table(table_id)
                return {
                    "table_id": table_id,
                    "created": str(table.created),
                    "num_rows": table.num_rows,
                    "num_bytes": table.num_bytes,
                    "schema": [
                        {"name": f.name, "type": f.field_type}
                        for f in table.schema[:20]  # 最初の20カラム
                    ]
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            # モック結果
            return {
                "table_id": table_id,
                "created": "2021-01-01 00:00:00",
                "num_rows": 1234567,
                "num_bytes": 987654321,
                "schema": [
                    {"name": "event_date", "type": "STRING"},
                    {"name": "event_timestamp", "type": "INTEGER"},
                    {"name": "event_name", "type": "STRING"},
                    {"name": "user_pseudo_id", "type": "STRING"},
                    {"name": "platform", "type": "STRING"}
                ]
            }
    
    def run_eda(self, date_range: str = "20210101:20210103") -> Dict[str, Any]:
        """探索的データ分析（EDA）を実行"""
        start_date, end_date = date_range.split(":")
        
        queries = {
            "basic_stats": f"""
                SELECT
                    COUNT(*) as total_events,
                    COUNT(DISTINCT user_pseudo_id) as unique_users,
                    COUNT(DISTINCT event_name) as event_types,
                    MIN(event_timestamp) as first_event,
                    MAX(event_timestamp) as last_event
                FROM `{PUBLIC_DATASET}.events_*`
                WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
            """,
            
            "events_by_type": f"""
                SELECT
                    event_name,
                    COUNT(*) as event_count,
                    COUNT(DISTINCT user_pseudo_id) as unique_users
                FROM `{PUBLIC_DATASET}.events_*`
                WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY event_name
                ORDER BY event_count DESC
                LIMIT 10
            """,
            
            "platform_distribution": f"""
                SELECT
                    platform,
                    COUNT(*) as event_count,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
                FROM `{PUBLIC_DATASET}.events_*`
                WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY platform
                ORDER BY event_count DESC
            """,
            
            "daily_active_users": f"""
                SELECT
                    _TABLE_SUFFIX as date,
                    COUNT(DISTINCT user_pseudo_id) as dau
                FROM `{PUBLIC_DATASET}.events_*`
                WHERE _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY date
                ORDER BY date
            """
        }
        
        results = {
            "date_range": {"start": start_date, "end": end_date},
            "analyses": {}
        }
        
        for name, sql in queries.items():
            if self.client and HAS_PANDAS:
                try:
                    df = self.run_query(sql)
                    results["analyses"][name] = df.to_dict(orient="records")
                except Exception as e:
                    results["analyses"][name] = {"error": str(e)}
            else:
                # モック結果
                results["analyses"][name] = self._get_mock_eda_result(name)
        
        return results
    
    def _get_mock_eda_result(self, analysis_name: str) -> List[Dict]:
        """モックEDA結果"""
        mock_data = {
            "basic_stats": [
                {
                    "total_events": 125000,
                    "unique_users": 8500,
                    "event_types": 25,
                    "first_event": 1609459200000000,
                    "last_event": 1609545600000000
                }
            ],
            "events_by_type": [
                {"event_name": "page_view", "event_count": 45000, "unique_users": 8000},
                {"event_name": "scroll", "event_count": 32000, "unique_users": 6500},
                {"event_name": "click", "event_count": 18000, "unique_users": 5200},
                {"event_name": "view_item", "event_count": 12000, "unique_users": 4100},
                {"event_name": "add_to_cart", "event_count": 5500, "unique_users": 2800},
                {"event_name": "purchase", "event_count": 1800, "unique_users": 1200}
            ],
            "platform_distribution": [
                {"platform": "WEB", "event_count": 85000, "percentage": 68.0},
                {"platform": "ANDROID", "event_count": 25000, "percentage": 20.0},
                {"platform": "IOS", "event_count": 15000, "percentage": 12.0}
            ],
            "daily_active_users": [
                {"date": "20210101", "dau": 3200},
                {"date": "20210102", "dau": 2800},
                {"date": "20210103", "dau": 3100}
            ]
        }
        return mock_data.get(analysis_name, [])


def generate_html_report(eda_results: Dict, output_path: str):
    """HTMLレポートを生成"""
    html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>BigQuery EDA レポート</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a365d; border-bottom: 3px solid #4299e1; padding-bottom: 10px; }}
        h2 {{ color: #2d3748; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #4299e1; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; }}
        tr:hover {{ background: #f7fafc; }}
        .metric {{ display: inline-block; background: #ebf8ff; padding: 15px 25px; margin: 10px; border-radius: 8px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #2b6cb0; }}
        .metric-label {{ color: #4a5568; font-size: 0.9em; }}
        .info {{ background: #e6fffa; padding: 15px; border-radius: 8px; border-left: 4px solid #38b2ac; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>BigQuery データ分析レポート</h1>
        <p><strong>生成日時:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>分析期間:</strong> {eda_results['date_range']['start']} - {eda_results['date_range']['end']}</p>
        
        <h2>基本統計</h2>
        <div class="metrics">
"""
    
    # 基本統計
    basic = eda_results['analyses'].get('basic_stats', [{}])[0]
    html += f"""
            <div class="metric">
                <div class="metric-value">{basic.get('total_events', 0):,}</div>
                <div class="metric-label">総イベント数</div>
            </div>
            <div class="metric">
                <div class="metric-value">{basic.get('unique_users', 0):,}</div>
                <div class="metric-label">ユニークユーザー</div>
            </div>
            <div class="metric">
                <div class="metric-value">{basic.get('event_types', 0)}</div>
                <div class="metric-label">イベント種類</div>
            </div>
        </div>
"""
    
    # イベント種類別
    html += """
        <h2>イベント種類別集計（Top 10）</h2>
        <table>
            <tr><th>イベント名</th><th>イベント数</th><th>ユニークユーザー</th></tr>
"""
    for event in eda_results['analyses'].get('events_by_type', []):
        html += f"""
            <tr>
                <td>{event.get('event_name', '')}</td>
                <td>{event.get('event_count', 0):,}</td>
                <td>{event.get('unique_users', 0):,}</td>
            </tr>
"""
    html += "        </table>\n"
    
    # プラットフォーム分布
    html += """
        <h2>プラットフォーム分布</h2>
        <table>
            <tr><th>プラットフォーム</th><th>イベント数</th><th>割合</th></tr>
"""
    for platform in eda_results['analyses'].get('platform_distribution', []):
        html += f"""
            <tr>
                <td>{platform.get('platform', '')}</td>
                <td>{platform.get('event_count', 0):,}</td>
                <td>{platform.get('percentage', 0)}%</td>
            </tr>
"""
    html += "        </table>\n"
    
    # DAU
    html += """
        <h2>日別アクティブユーザー（DAU）</h2>
        <table>
            <tr><th>日付</th><th>DAU</th></tr>
"""
    for day in eda_results['analyses'].get('daily_active_users', []):
        html += f"""
            <tr>
                <td>{day.get('date', '')}</td>
                <td>{day.get('dau', 0):,}</td>
            </tr>
"""
    html += """
        </table>
        
        <div class="info">
            <strong>データソース:</strong> Google Analytics 4 公開サンプルデータセット<br>
            <code>bigquery-public-data.ga4_obfuscated_sample_ecommerce</code>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTMLレポート生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="BigQueryデータ分析スクリプト")
    parser.add_argument("--test", action="store_true", help="接続テスト")
    parser.add_argument("--eda", action="store_true", help="EDA実行")
    parser.add_argument("--query", type=str, help="カスタムSQLクエリ")
    parser.add_argument("--date-range", type=str, default="20210101:20210103",
                        help="分析期間 (YYYYMMDD:YYYYMMDD)")
    parser.add_argument("--output", "-o", type=str, help="出力ファイルパス")
    parser.add_argument("--format", choices=["json", "html", "csv"], default="json",
                        help="出力形式")
    parser.add_argument("--project", type=str, help="GCPプロジェクトID")
    
    args = parser.parse_args()
    
    # アナライザー初期化
    analyzer = BigQueryAnalyzer(project_id=args.project)
    
    # 接続テスト
    if args.test:
        result = analyzer.test_connection()
        print("\n接続テスト結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    
    # カスタムクエリ
    if args.query:
        result = analyzer.run_query(args.query)
        if HAS_PANDAS and result is not None:
            print("\nクエリ結果:")
            print(result)
            if args.output:
                if args.format == "csv":
                    result.to_csv(args.output, index=False)
                else:
                    result.to_json(args.output, orient="records", force_ascii=False, indent=2)
                print(f"\n保存完了: {args.output}")
        return
    
    # EDA実行
    if args.eda:
        print("EDA実行中...")
        results = analyzer.run_eda(args.date_range)
        
        # 出力
        output_path = args.output or f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if args.format == "html":
            output_path = output_path if output_path.endswith(".html") else f"{output_path}.html"
            generate_html_report(results, output_path)
        else:
            output_path = output_path if output_path.endswith(".json") else f"{output_path}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON出力: {output_path}")
        
        # サマリー表示
        basic = results['analyses'].get('basic_stats', [{}])[0]
        print("\n=== EDAサマリー ===")
        print(f"期間: {results['date_range']['start']} - {results['date_range']['end']}")
        print(f"総イベント数: {basic.get('total_events', 0):,}")
        print(f"ユニークユーザー: {basic.get('unique_users', 0):,}")
        return
    
    # デフォルト: データセット情報を表示
    info = analyzer.get_dataset_info()
    print("\nデータセット情報:")
    print(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
