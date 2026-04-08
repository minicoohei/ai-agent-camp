---
description: "When the user says /start-18-17 — Module 18 Lesson 18-17: PM - 結合テスト実施"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-16", "output/pm/unit-test-code/"]
level: "intermediate"
tags: ["pm", "test", "integration", "api-test"]
---

# 🎓 Lesson 18-17: 結合テスト実施

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowのAPI間連携に対し結合テストを実施し、エビデンスを取得する |
| 所要時間 | 約25分 |
| 使うスキル | test-planner スキル |
| 前提条件 | Lesson 18-16 完了 |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 ステップ1: 結合テストシナリオの設計

結合テストは、複数のAPI間の連携を検証する重要なプロセスです。TaskFlowシステムでは以下の連携パターンをテストします。

- **API→DB連携**: タスク作成時のAPI→データベース保存→検索の一連の流れ
- **認証→タスク操作**: ユーザー認証後のタスク作成・編集・削除権限検証
- **通知パイプライン**: タスク更新時の内部通知→Webhook送信の完全性検証
- **全体統合**: 複数システム間の完全な動作検証

```json
{
  "type": "AskQuestion",
  "question": "どのテスト範囲を優先して実施しますか?",
  "options": [
    {
      "id": "api_db",
      "label": "API→DB連携（タスク作成から検索まで）",
      "nextStep": "start-test-api-db"
    },
    {
      "id": "auth_task",
      "label": "認証→タスク操作（権限検証を含む）",
      "nextStep": "start-test-auth-task"
    },
    {
      "id": "notification",
      "label": "通知パイプライン（内部通知→Webhook）",
      "nextStep": "start-test-notification"
    },
    {
      "id": "all",
      "label": "すべてのテストを実施する",
      "nextStep": "start-test-all"
    }
  ],
  "context": "結合テストの範囲選択は、プロジェクトのリスク評価と時間制約に基づいて決定します。関係者の意見を参考にしてください。"
}
```

## 🚀 ステップ2: テストコード生成（pytest + requests）

pytestフレームワークとrequestsライブラリを使用して、API結合テストコードを生成します。テストコードは以下の構造を持つべきです。

- インポートセクション: pytest、requests、unittest.mockの導入
- フィクスチャ設定: テストベースURL、認証トークン、テストデータの初期化
- テストケース: 各API連携シナリオに対応した関数群
- アサーション: HTTP ステータスコード、レスポンスボディ、データベース状態の検証
- クリーンアップ: テスト後の環境復元処理

```json
{
  "type": "AskQuestion",
  "question": "モック戦略をどのように設定しますか?",
  "options": [
    {
      "id": "real_db",
      "label": "テスト用DB使用（実環境に近い検証）",
      "config": {
        "strategy": "integration_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    },
    {
      "id": "mock_db",
      "label": "モックDB使用（高速・隔離テスト）（推奨）",
      "config": {
        "strategy": "unit_testing",
        "database": "in_memory_mock",
        "external_apis": "mocked"
      }
    },
    {
      "id": "hybrid",
      "label": "混合戦略（コア機能はテストDB、外部APIはモック）",
      "config": {
        "strategy": "hybrid_testing",
        "database": "test_database",
        "external_apis": "mocked"
      }
    }
  ],
  "context": "モック戦略は、テストの信頼性と実行速度のバランスを考慮して選択します。実DBテストは検証精度が高い一方、テスト環境の構築と管理が複雑になります。"
}
```

テストコード例:

```python
import pytest
import requests
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

class TestTaskFlowIntegration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.base_url = "http://localhost:8000/api"
        self.auth_token = "test-token-xyz123"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        yield
        # クリーンアップ処理
        self._cleanup_test_data()

    def test_create_task_and_retrieve(self):
        """タスク作成→検索の連携テスト"""
        payload = {
            "title": "Integration Test Task",
            "description": "Testing API→DB coordination",
            "priority": "high"
        }
        response = requests.post(
            f"{self.base_url}/tasks",
            json=payload,
            headers=self.headers
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # DB検索の検証
        get_response = requests.get(
            f"{self.base_url}/tasks/{task_id}",
            headers=self.headers
        )
        assert get_response.status_code == 200
        assert get_response.json()["title"] == payload["title"]

    def test_auth_required_for_task_operations(self):
        """認証なしでのタスク操作を拒否"""
        response = requests.get(f"{self.base_url}/tasks")
        assert response.status_code == 401

    def _cleanup_test_data(self):
        """テストデータのクリーンアップ"""
        pass
```

## ⚠️ ステップ3: テスト実行 & エビデンスキャプチャ

テストの実行と結果の記録は、プロジェクトの品質保証の根拠となります。

以下の手順でテストを実行します。

1. テスト環境の確認
   - テストDBが独立して稼働しているか
   - テストAPIエンドポイントが正しく起動しているか
   - 外部依存が正しくモック化されているか

2. テスト実行コマンド
   ```bash
   pytest tests/integration/ -v --tb=short --html=report.html --cov=src
   ```

3. エビデンス取得
   - テスト実行ログ（JSON形式）
   - スクリーンショット（失敗時の画面状態）
   - パフォーマンスメトリクス（レスポンス時間、メモリ使用率）
   - データベース検証ログ（INSERT/UPDATE/DELETE の記録）

エビデンスファイルの構成:

```text
output/pm/integration-test-evidence/
├── test-execution-log.json
├── test-results.html
├── failed-cases/              # テスト失敗時のみ生成
│   └── case-XXX-description.md
├── performance-metrics.csv
└── summary.md
```

## ✅ ステップ4: 不具合レポート作成

テスト実行で発見された不具合は、適切な形式でレポート化する必要があります。

```json
{
  "type": "AskQuestion",
  "question": "不具合レポートの形式はどちらを選択しますか?",
  "options": [
    {
      "id": "simple",
      "label": "簡易形式（タイトル・原因・対応案のみ）",
      "template": "simple-defect-report.md"
    },
    {
      "id": "detailed",
      "label": "詳細形式（再現手順、期待値、実績値、スクリーンショット含む）",
      "template": "detailed-defect-report.md"
    },
    {
      "id": "jira",
      "label": "Jira形式（フィールド：優先度、担当者、スプリント）",
      "template": "jira-defect-format.json"
    }
  ],
  "context": "不具合レポートの形式は、組織のプロセスと追跡システムに合わせて選択します。詳細形式は開発チームの修正効率を向上させます。"
}
```

不具合レポートのテンプレート（詳細形式）:

```markdown
# 不具合レポート #001

## 概要
- **タイトル**: ユーザー認証後のタスク作成でDB書き込みエラー
- **重要度**: High
- **発見日**: 2024-02-10
- **担当**: Dev Team A

## 再現手順
1. テストユーザーでログイン
2. タスク作成API呼び出し（POST /api/tasks）
3. 500エラーが返される

## 期待値
- ステータスコード: 201 Created
- レスポンス: 作成されたタスクのJSON

## 実績値
- ステータスコード: 500 Internal Server Error
- エラーメッセージ: "Database constraint violation on tasks.user_id"

## 根本原因
タスク作成時のユーザーID検証ロジックがDB制約条件と不一致

## 対応案
- ユーザーID検証ロジックの修正
- DB マイグレーション実行
- リグレッションテストの追加

## エビデンス
- スクリーンショット: error-500-screenshot.png
- ログ抽出: output/pm/logs/api-error.log
- API レスポンス: response-dump.json
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── operation-manual.md  (運用マニュアル)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/operation-manual.md

# 冒頭を確認（最初の30行）
head -30 output/pm/operation-manual.md
```

> 💡 全文を確認: `cat output/pm/operation-manual.md` で全文表示できます

## ➡️ 完成と次のステップ

以下の成果物が output/pm/integration-test-evidence/ に揃ったことを確認してください。

- test-execution-log.json: テスト実行の全記録
- test-results.html: ブラウザで閲覧可能なテスト結果レポート
- failed-cases/*.md: 発見された不具合の詳細レポート
- performance-metrics.csv: APIレスポンス時間などのパフォーマンスデータ

**Next Lesson**: → Lesson 18-18 会議体設計 & 議事録分析

このレッスンで習得した結合テスト実施のスキルは、システム開発の品質保証プロセスの重要な一部です。取得したエビデンスは、ステークホルダーへの信頼性報告と、本番前の最終検証に活用されます。
