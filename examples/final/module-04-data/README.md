# Module 4: データ分析（BigQuery） - 成果物（Final）

BigQuery接続、EDA（探索的データ分析）、可視化の例です。

## 学習目標
- BigQueryに接続し、データを取得できる
- EDA（探索的データ分析）を実行できる
- 分析結果を可視化・レポート化できる

## 成果物一覧

| ファイル | 種類 | 内容 |
|---------|------|------|
| `bigquery_connection.py` | スクリプト | BigQuery接続・認証 |
| `eda_analysis.py` | スクリプト | EDA実行スクリプト |
| `eda_report.html` | レポート | 分析レポート（HTML） |
| `charts/` | 画像 | 各種可視化チャート |
| `analysis_results.json` | データ | 分析結果JSON |

## 使用データセット

本モジュールでは、Google公開データセット「GA4 E-Commerce Sample」を使用します。

```
bigquery-public-data.ga4_obfuscated_sample_ecommerce
├── events_*         # イベントデータ（日付別テーブル）
├── users            # ユーザーデータ
└── items            # 商品データ
```

## BigQuery接続フロー

```
┌─────────────────────────────────────────────────────────┐
│  BigQuery接続フロー                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 認証設定                                            │
│     │                                                   │
│     ├─ gcloud auth login                               │
│     └─ gcloud auth application-default login           │
│                                                         │
│  2. プロジェクト設定                                    │
│     │                                                   │
│     └─ gcloud config set project YOUR_PROJECT_ID       │
│                                                         │
│  3. クライアント初期化                                  │
│     │                                                   │
│     └─ client = bigquery.Client()                      │
│                                                         │
│  4. クエリ実行                                          │
│     │                                                   │
│     └─ result = client.query(sql).to_dataframe()       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 実行コマンド例

### 1. 認証設定
```bash
# GCP認証
gcloud auth login
gcloud auth application-default login

# プロジェクト設定
gcloud config set project YOUR_PROJECT_ID
```

### 2. 接続テスト
```bash
python examples/final/module-04-data/bigquery_connection.py --test
```

### 3. EDA実行
```bash
python examples/final/module-04-data/eda_analysis.py \
  --dataset "bigquery-public-data.ga4_obfuscated_sample_ecommerce" \
  --date-range "2021-01-01:2021-01-31" \
  --output examples/final/module-04-data/eda_report.html
```

## BigQuery接続スクリプト例

```python
#!/usr/bin/env python3
"""BigQuery接続・認証スクリプト"""
from google.cloud import bigquery
import os
import pandas as pd

def get_client():
    """BigQueryクライアントを取得"""
    # 環境変数の競合を回避
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    
    client = bigquery.Client()
    print(f"✓ 接続成功: {client.project}")
    return client

def run_query(client, sql):
    """クエリを実行してDataFrameで返す"""
    job = client.query(sql)
    return job.to_dataframe()

def test_connection():
    """接続テスト"""
    client = get_client()
    
    sql = """
    SELECT
        CURRENT_TIMESTAMP() as current_time,
        @@project_id as project_id,
        '接続成功' as status
    """
    
    result = run_query(client, sql)
    print(result)
    return True

if __name__ == "__main__":
    test_connection()
```

## EDA分析項目

### 1. 基本統計
```python
# データセット概要
- 総レコード数
- ユニークユーザー数
- 日付範囲
- イベントタイプ別カウント
```

### 2. ユーザー分析
```python
# ユーザー行動
- 日別アクティブユーザー（DAU）
- セッション数の分布
- 滞在時間の分布
- デバイス別ユーザー数
```

### 3. イベント分析
```python
# イベントファネル
- page_view → add_to_cart → purchase
- 各ステップのコンバージョン率
- 離脱ポイントの特定
```

### 4. 売上分析
```python
# 売上データ
- 日別売上推移
- 商品カテゴリ別売上
- 平均注文金額
- リピート率
```

## 出力レポート形式

### HTML レポート構成

```
eda_report.html
├── 1. エグゼクティブサマリー
│   ├── KPI概要
│   └── 主要な発見
│
├── 2. データ概要
│   ├── データセット情報
│   ├── 期間・レコード数
│   └── 欠損値の状況
│
├── 3. ユーザー分析
│   ├── DAU推移グラフ
│   ├── デバイス分布（円グラフ）
│   └── ユーザーセグメント
│
├── 4. イベント分析
│   ├── ファネル図
│   ├── イベント発生頻度（棒グラフ）
│   └── 時間帯別アクセス（ヒートマップ）
│
├── 5. 売上分析
│   ├── 売上推移（折れ線グラフ）
│   ├── カテゴリ別売上（棒グラフ）
│   └── 商品ランキング（テーブル）
│
└── 6. 推奨アクション
    ├── 課題の特定
    └── 改善提案
```

## 可視化チャート例

### 日別アクティブユーザー
```
       DAU推移（2021年1月）
    │
 5k │    ╱╲
    │   ╱  ╲    ╱╲
 4k │  ╱    ╲  ╱  ╲
    │ ╱      ╲╱    ╲
 3k │╱              ╲
    └───────────────────→
      1  5  10  15  20  25  30
              日付
```

### コンバージョンファネル
```
    訪問者      100%  ████████████████████
        ↓
    商品閲覧     65%  █████████████
        ↓
    カート追加   25%  █████
        ↓
    購入完了     8%   ██
```

## チェックリスト

- [ ] BigQuery認証が完了している
- [ ] テストクエリが実行できる
- [ ] 公開データセットにアクセスできる
- [ ] EDAスクリプトが実行できる
- [ ] HTMLレポートが生成される
- [ ] チャートが正しく表示される

## 関連レッスン

- `/start-4-1`: BigQuery接続
- `/start-4-2`: EDA実行
- `/start-4-3`: 可視化
- `/start-4-4`: レポート生成

## 参考リンク

- [BigQuery Python Client](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [GA4 公開データセット](https://developers.google.com/analytics/bigquery/web-ecommerce-demo-dataset)
- [Pandas公式ドキュメント](https://pandas.pydata.org/docs/)
- [Plotly（可視化）](https://plotly.com/python/)

## トラブルシューティング

### 認証エラー
```bash
# ADC（Application Default Credentials）を再設定
gcloud auth application-default revoke
gcloud auth application-default login
```

### 権限エラー
```
必要なIAMロール:
- BigQuery Data Viewer
- BigQuery Job User
```

### クォータ超過
```sql
-- クエリコストを抑える
SELECT * FROM `dataset.table`
WHERE _TABLE_SUFFIX = '20210101'  -- 日付を絞る
LIMIT 1000                        -- 行数を制限
```
