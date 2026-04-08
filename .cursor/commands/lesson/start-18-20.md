---
description: "When the user says /start-18-20 — Module 18 Lesson 18-20: PM - 総合演習（カプストーン）"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "30分"
category: "lesson"
prerequisites: ["start-18-1", "start-18-2", "start-18-3", "start-18-4", "start-18-5", "start-18-6", "start-18-7", "start-18-8", "start-18-9", "start-18-10", "start-18-11", "start-18-12", "start-18-13", "start-18-14", "start-18-15", "start-18-16", "start-18-17", "start-18-18", "start-18-19"]
level: "intermediate"
tags: ["pm", "capstone", "review", "traceability"]
---

# 🎓 Lesson 18-20: 総合演習（カプストーン）

| 項目 | 内容 |
|------|------|
| ゴール | Module 18の全20レッスンの成果物を統合レビューし、プロダクト開発の全工程を振り返る |
| 所要時間 | 約30分 |
| 使うスキル | pm-toolkit, test-planner, monitoring-dashboard スキル |
| 前提条件 | Lesson 18-1〜Lesson 18-19 完了 |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 Step 1: 全成果物の一覧確認

Module 18 を通じて作成した全20レッスンの成果物を確認し、完成度と進捗状況をレビューします。

```json
{
  "type": "AskQuestion",
  "question": "成果物の確認方法を選んでください",
  "options": [
    "自動スキャン（output/pm/の全ファイル）",
    "フェーズ別に確認",
    "不足分だけ確認",
    "スキップ"
  ],
  "multiple": false
}
```

### 期待される成果物リスト

以下は Module 18 の全20レッスンで生成すべき成果物です：

**企画フェーズ（18-1 〜 18-3）:**
- Lesson 18-1: customer-needs.md（顧客ニーズ分析ドキュメント）
- Lesson 18-2: requirements-brief.md（要求資料）
- Lesson 18-3: prd.md（PRD - Working Backwards方式）

**要件定義フェーズ（18-4 〜 18-7）:**
- Lesson 18-4: review-summary.md（3種レビュー統合結果）
- Lesson 18-5: requirements-spec.md（要件定義書）
- Lesson 18-6: usecases.md（ユースケース記述・シーケンス図）
- Lesson 18-7: wireframes.md（画面遷移図・ワイヤーフレーム）

**設計フェーズ（Lesson 18-8 〜 18-12）:**
- Lesson 18-8: er-diagram.puml（ER図・エンティティ仕様書）
- Lesson 18-9: system-architecture.puml（システム構成図・API設計）
- Lesson 18-10: wbs.md（WBS・ガントチャート）
- Lesson 18-11: notion-export.md（Notion連携エクスポート）
- Lesson 18-12: design-system.md（デザインシステム仕様書）

**実装・テストフェーズ（Lesson 18-13 〜 18-18）:**
- Lesson 18-13: prototype/（HTMLプロトタイプ）
- Lesson 18-14: e2e-tests/（Playwright E2Eテスト）
- Lesson 18-15: test-plan.md（テスト計画書・テストケース）
- Lesson 18-16: unit-test-evidence/（単体テスト実行結果）
- Lesson 18-17: integration-test-evidence/（結合テスト実行結果）
- Lesson 18-18: spec-changes.md（会議体設計・議事録分析）

**統合・総括（Lesson 18-19 〜 18-20）:**
- Lesson 18-19: dashboard.py（marimoダッシュボード）
- Lesson 18-20: capstone-review-summary.html（カプストーン総括レビュー）

### 成果物の自動スキャン

```python
import os
from pathlib import Path

output_dir = Path("output/pm")

# ファイル一覧を取得
deliverables = {
    "planning": [],
    "requirements": [],
    "design": [],
    "implementation": [],
    "integration": []
}

if output_dir.exists():
    for file in sorted(output_dir.glob("*")):
        if file.is_file():
            print(f"✓ {file.name} ({file.stat().st_size} bytes)")
else:
    print(f"output/pm/ ディレクトリが見つかりません")

# 完成度の算出
total_expected = 20
total_found = len(list(output_dir.glob("*"))) if output_dir.exists() else 0
completion_rate = (total_found / total_expected) * 100

print(f"\n完成度: {completion_rate:.1f}% ({total_found}/{total_expected} ファイル)")
```

### フェーズ別完成度

```json
{
  "type": "AskQuestion",
  "question": "どのフェーズの詳細を確認しますか？",
  "options": [
    "企画フェーズ（1-3）",
    "要件定義フェーズ（4-7）",
    "設計フェーズ（8-12）",
    "実装・テストフェーズ（13-18）",
    "全フェーズサマリー"
  ],
  "multiple": false
}
```

## 📍 Step 2: トレーサビリティ確認（要件→設計→テスト）

プロダクト開発における重要な検証：「全ての要件が設計で実装され、全ての設計が テストでカバーされている」ことを確認します。

```json
{
  "type": "AskQuestion",
  "question": "トレーサビリティの確認範囲を選んでください",
  "options": [
    "主要要件5つ",
    "全要件",
    "AIに重要なものを選んでもらう",
    "ダッシュボードのみ確認"
  ],
  "multiple": false
}
```

### トレーサビリティマトリクスの構造

各要件について、以下の追跡を実施：

```text
要件 (Req-001)
├── 設計ドキュメント参照 (Design-Section-2.3)
│   ├── UIワイヤーフレーム (WF-005)
│   ├── APIエンドポイント (POST /api/users)
│   └── DB テーブル (users table)
├── テストケース (TC-USER-001, TC-USER-002, TC-USER-003)
│   ├── Unit Test: UserModel
│   ├── Integration Test: Auth Flow
│   └── UI Test: Registration Form
└── テスト実行結果
    ├── TC-USER-001: PASS
    ├── TC-USER-002: PASS
    └── TC-USER-003: PASS
```

### トレーサビリティ確認スクリプト

```python
import json
import csv
from pathlib import Path

# 要件ファイルの読み込み
req_file = Path("output/pm/requirements-spec.md")
test_file = Path("output/pm/test-plan.md")

traceability_matrix = {
    "total_requirements": 53,
    "requirements_with_tests": 49,
    "requirements_without_tests": 4,
    "tests_without_requirements": 2,
    "coverage_percentage": 92.45
}

# トレーサビリティマトリクス生成
with open("output/pm/traceability-matrix.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Requirement ID",
        "Requirement",
        "Design Reference",
        "Test Cases",
        "Status",
        "Coverage"
    ])
    writer.writeheader()

    # サンプル要件
    requirements = [
        {
            "id": "REQ-001",
            "name": "ユーザー登録機能",
            "design_ref": "Section 3.1, API-001",
            "tests": "TC-AUTH-001, TC-AUTH-002",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-002",
            "name": "ユーザーログイン",
            "design_ref": "Section 3.2, API-002",
            "tests": "TC-AUTH-003, TC-AUTH-004, TC-AUTH-005",
            "status": "Covered",
            "coverage": "✓"
        },
        {
            "id": "REQ-003",
            "name": "パスワードリセット",
            "design_ref": "Section 3.3, API-003",
            "tests": "TC-AUTH-006, TC-AUTH-007",
            "status": "Partially Covered",
            "coverage": "⚠"
        }
    ]

    for req in requirements:
        writer.writerow(req)

print("トレーサビリティマトリクス生成完了")
print(f"全要件数: {traceability_matrix['total_requirements']}")
print(f"テスト対象: {traceability_matrix['requirements_with_tests']}")
print(f"カバレッジ率: {traceability_matrix['coverage_percentage']:.1f}%")
```

### ギャップ分析

```json
{
  "type": "AskQuestion",
  "question": "ギャップ分析の結果をどう対応しますか？",
  "options": [
    "見つかったギャップをすべて修正",
    "高優先度ギャップのみ修正",
    "ギャップを文書化して後回し",
    "影響度評価してから決定"
  ],
  "multiple": false
}
```

**検出されたギャップ例：**
- Req-045（API レート制限）：テストケースが定義されていない
- Req-051（監視ログ）：設計文書で詳細が不明確
- TC-PERF-012（パフォーマンステスト）：対応要件が特定できない

## 📍 Step 3: 品質メトリクスの算出

プロジェクト全体の品質状況を数値化し、客観的に評価します。

```json
{
  "type": "AskQuestion",
  "question": "メトリクスの詳細度を選んでください",
  "options": [
    "サマリーのみ",
    "詳細分析",
    "ベンチマーク比較付き",
    "AI分析推奨"
  ],
  "multiple": false
}
```

### 主要メトリクス

```python
import json
from datetime import datetime

quality_metrics = {
    "timestamp": datetime.now().isoformat(),
    "project_name": "TaskFlow v1",
    "evaluation_date": "2024-07-15",

    # 1. 要件カバレッジ
    "requirements": {
        "total": 53,
        "specified": 53,
        "coverage_rate": 100,
        "status": "✓ Excellent"
    },

    # 2. テストカバレッジ
    "test_coverage": {
        "total_requirements": 53,
        "tested_requirements": 49,
        "coverage_rate": 92.45,
        "status": "✓ Good"
    },

    # 3. テスト実行結果
    "test_results": {
        "total_test_cases": 156,
        "passed": 136,
        "failed": 12,
        "skipped": 8,
        "pass_rate": 87.18,
        "status": "⚠ Need Improvement"
    },

    # 4. ドキュメント完成度
    "documentation": {
        "required_docs": 9,
        "completed_docs": 8,
        "draft_docs": 1,
        "completion_rate": 88.89,
        "status": "✓ Good"
    },

    # 5. コード品質指標
    "code_quality": {
        "lines_of_code": 12450,
        "code_duplication": 8.5,
        "cyclomatic_complexity_avg": 3.2,
        "test_code_ratio": 0.45,
        "status": "✓ Good"
    },

    # 6. スケジュール進捗
    "schedule": {
        "planned_duration_days": 180,
        "actual_elapsed_days": 173,
        "progress_percentage": 96.1,
        "status": "✓ On Track"
    },

    # 7. リスク管理
    "risk_management": {
        "identified_risks": 24,
        "mitigated_risks": 22,
        "active_risks": 2,
        "mitigation_rate": 91.67,
        "status": "✓ Good"
    },

    # 8. 統合スコア
    "overall_health": {
        "score": 88.5,
        "level": "GREEN",
        "status": "✓ Project Health: Excellent"
    }
}

# JSON形式で保存
with open("output/pm/quality-metrics.json", "w") as f:
    json.dump(quality_metrics, f, indent=2, ensure_ascii=False)

# テーブル形式で表示
print("=" * 70)
print("TASKFLOW V1 - 品質メトリクスサマリー")
print("=" * 70)
print(f"評価日時: {quality_metrics['evaluation_date']}")
print()

print("📊 メトリクス一覧")
print("-" * 70)
print(f"要件カバレッジ:     {quality_metrics['requirements']['coverage_rate']}%")
print(f"テストカバレッジ:   {quality_metrics['test_coverage']['coverage_rate']:.2f}%")
print(f"テスト成功率:       {quality_metrics['test_results']['pass_rate']:.2f}%")
print(f"ドキュメント完成度: {quality_metrics['documentation']['completion_rate']:.2f}%")
print(f"スケジュール進捗:   {quality_metrics['schedule']['progress_percentage']:.1f}%")
print(f"リスク対応率:       {quality_metrics['risk_management']['mitigation_rate']:.2f}%")
print()
print(f"🎯 全体プロジェクトスコア: {quality_metrics['overall_health']['score']}/100")
print(f"状態: {quality_metrics['overall_health']['status']}")
print("=" * 70)
```

### ベンチマーク比較

```text
Industry Standard vs TaskFlow v1
┌─────────────────────────┬──────────────┬────────────┬──────┐
│ メトリクス               │ 業界標準     │ TaskFlow   │ 評価 │
├─────────────────────────┼──────────────┼────────────┼──────┤
│ 要件カバレッジ          │ 85-95%       │ 100%       │ 優秀 │
│ テストカバレッジ        │ 80-90%       │ 92.45%     │ 優秀 │
│ テスト成功率            │ 90%以上      │ 87.18%     │ 要改善│
│ ドキュメント完成度      │ 85%以上      │ 88.89%     │ 優秀 │
│ スケジュール達成率      │ 95%以上      │ 96.1%      │ 優秀 │
│ リスク対応率            │ 85%以上      │ 91.67%     │ 優秀 │
└─────────────────────────┴──────────────┴────────────┴──────┘
```

## 📍 Step 4: 改善提案の生成

各フェーズで検出された課題に対して、具体的な改善提案を策定します。

```json
{
  "type": "AskQuestion",
  "question": "改善提案の範囲を選んでください",
  "options": [
    "企画フェーズ",
    "設計フェーズ",
    "実装フェーズ",
    "テスト・運用フェーズ",
    "全体"
  ],
  "multiple": true
}
```

### 改善提案テンプレート

```python
improvement_plan = {
    "planning_phase": {
        "issues": [
            {
                "id": "IMP-P-001",
                "title": "市場分析の追加調査",
                "description": "競合他社との機能比較分析が不十分",
                "priority": "Medium",
                "effort": "3日",
                "recommendation": "Q4で競合製品の詳細ベンチマークを実施"
            }
        ]
    },

    "requirements_phase": {
        "issues": [
            {
                "id": "IMP-R-001",
                "title": "非機能要件の詳細化",
                "description": "パフォーマンス要件が定量的でない",
                "priority": "High",
                "effort": "2日",
                "recommendation": "API応答時間、DB処理時間の具体値を定義"
            },
            {
                "id": "IMP-R-002",
                "title": "ユースケース拡張",
                "description": "エラーハンドリングシナリオが不足",
                "priority": "Medium",
                "effort": "3日",
                "recommendation": "各ユースケースに例外フロー追加"
            }
        ]
    },

    "design_phase": {
        "issues": [
            {
                "id": "IMP-D-001",
                "title": "API設計の統一",
                "description": "エラーレスポンス形式が不統一",
                "priority": "High",
                "effort": "2日",
                "recommendation": "標準エラーレスポンススキーマを定義し、すべてのAPIに適用"
            }
        ]
    },

    "implementation_phase": {
        "issues": [
            {
                "id": "IMP-I-001",
                "title": "テスト実行の失敗",
                "description": "パスワードリセット機能でテスト失敗（TC-AUTH-007）",
                "priority": "High",
                "effort": "1日",
                "recommendation": "エラーハンドリングロジックの修正とテスト再実行"
            }
        ]
    },

    "testing_phase": {
        "issues": [
            {
                "id": "IMP-T-001",
                "title": "テストカバレッジの向上",
                "description": "エッジケースのテストが不足（4要件未カバー）",
                "priority": "Medium",
                "effort": "5日",
                "recommendation": "境界値分析とエラー分岐テストの追加"
            }
        ]
    }
}

# JSONで保存
with open("output/pm/improvement-plan.json", "w") as f:
    json.dump(improvement_plan, f, indent=2, ensure_ascii=False)
```

### レッスンズラーンドドキュメント

```markdown
# Lessons Learned - TaskFlow v1 プロジェクト

## 成功したプラクティス

### 1. 要件のトレーサビリティマトリクス
**効果**: 設計漏れと重複の検出に成功
**継続**: 次プロジェクトでも同じアプローチを採用

### 2. 早期のセキュリティレビュー
**効果**: リスク検出が設計段階で可能に
**継続**: Lesson 18-12 のセキュリティ設計を全プロジェクト標準に

### 3. ユースケース駆動の設計
**効果**: ユーザー視点のUIワイヤーフレーム作成に成功
**継続**: ユースケースから直接テストケースを生成

## 改善すべき点

### 1. テスト実行タイミング
**課題**: テスト成功率87.2%（目標90%）
**原因**: 実装完了直後のテスト実行で、実装不完全
**対策**: スプリント終了後2日以上の緩衝期間を確保

### 2. ドキュメント整備
**課題**: API仕様の更新遅延
**原因**: コード実装とドキュメント更新の非同期
**対策**: CI/CDパイプラインで OpenAPI 仕様の自動生成を導入

### 3. リスク管理の継続性
**課題**: 週次リスクレビューが月次に後退
**原因**: スケジュール圧迫によるミーティング削減
**対策**: リスクレビューは固定スケジュール化、絶対削減対象外

## 次プロジェクト(TaskFlow v2)への推奨事項

1. **スケールアップ**: 基本設計は再利用可能
2. **テスト自動化**: UI テスト自動化ツール導入
3. **DevOps拡充**: 本番環境での継続監視体制の構築
4. **チーム拡大**: 専任テスト担当者の採用
```

### NextSteps ロードマップ

```json
{
  "type": "AskQuestion",
  "question": "TaskFlow v2での優先課題は何ですか？",
  "options": [
    "テスト自動化の強化",
    "API仕様管理の自動化",
    "パフォーマンス最適化",
    "セキュリティ強化",
    "運用自動化"
  ],
  "multiple": true
}
```

## ✅ 成果物

このカプストーン演習で生成される成果物：

```text
output/pm/
├── traceability-matrix.csv        # 要件→設計→テスト追跡マトリクス
├── quality-metrics.json           # 品質メトリクス集計
├── improvement-plan.json          # 改善提案一覧
├── lessons-learned.md             # レッスンズラーンド
└── capstone-review-summary.html   # HTML形式のカプストーン総括
```

## 🚀 チェックリスト

```text
□ output/pm/ の全成果物を確認した（20ファイル以上）
□ トレーサビリティマトリクスを作成した（要件53個）
□ 品質メトリクスを算出した（8つのメトリクス）
□ ギャップ分析を完了した（4個のギャップ検出）
□ 改善提案を生成した（各フェーズで実施）
□ レッスンズラーンドドキュメントを作成した
□ Module 18 全体（18-1 〜 18-20）を振り返った
□ 次プロジェクトへの推奨事項を整理した
```

## 📍 最終確認

```json
{
  "type": "AskQuestion",
  "question": "カプストーン演習の完了状況は？",
  "options": [
    "すべて完了 - Module 18 習得完了",
    "ほぼ完了 - 細部を修正中",
    "部分完了 - 復習が必要な箇所がある",
    "要サポート - 不明な点がある"
  ],
  "multiple": false
}
```

---

## 🎯 Module 18 完了時のポイント

このモジュール完了により、以下のスキルを習得しました：

✅ **企画スキル**: 市場分析、ビジネス要件の定義
✅ **要件定義スキル**: システム要件仕様、ユースケース、ユーザーストーリー
✅ **設計スキル**: システムアーキテクチャ、DB設計、API設計、セキュリティ設計
✅ **実装スキル**: コード構成、CI/CDパイプライン
✅ **テストスキル**: テスト計画、テストケース、テスト自動化
✅ **統合スキル**: トレーサビリティ管理、品質メトリクス、リスク管理


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── project-summary.md  (プロジェクト総括)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/project-summary.md

# 冒頭を確認（最初の30行）
head -30 output/pm/project-summary.md
```

> 💡 全文を確認: `cat output/pm/project-summary.md` で全文表示できます

## ➡️ 次のステップ

```json
{
  "type": "AskQuestion",
  "question": "お疲れ様でした！次のアクションを選んでください",
  "options": [
    "カプストーン演習に挑戦（course/exercises/18-pm-sysdef/capstone/README.md）",
    "別のモジュールに移動",
    "成果物をGitにコミット",
    "ここで終了"
  ],
  "multiple": false
}
```

### カプストーン演習への進み方（オプション）

上級者向けの **実践的なカプストーン演習** では、ダミーデータではなく実際のプロジェクト定義に基づいて、以下を実施します：

1. **実際のプロジェクト仕様** の作成（18-1 〜 18-20 の手法を応用）
2. **チーム演習**：複数人でのロール分担
3. **フィードバックループ**: ステークホルダーレビュー
4. **成果物の品質検証**: Module 18 の全チェックリストで評価

詳細は `course/exercises/18-pm-sysdef/capstone/README.md` を参照してください。

### Gitへのコミット

```bash
# 成果物を Git にコミット
git add output/pm/
git commit -m "Lesson 18-20: TaskFlow PM プロジェクト統合レビュー完了

- トレーサビリティマトリクス: 要件53個、カバレッジ92.45%
- 品質メトリクス集計: 全体スコア 88.5/100
- ギャップ分析: 4項目の改善提案
- レッスンズラーンド: 成功実例と改善点を記録

Module 18 (PM System Definition) 完了
"

git push
```

---

## 🎓 Learning Path サマリー

| 項目 | Lesson | 成果物 |
|------|--------|--------|
| 顧客ニーズ分析 | 18-1 | customer-needs.md |
| 要求資料 | 18-2 | requirements-brief.md |
| PRD | 18-3 | prd.md |
| 3種レビュー | 18-4 | review-summary.md |
| 要件定義書 | 18-5 | requirements-spec.md |
| ユースケース | 18-6 | usecases.md |
| 画面遷移図・WF | 18-7 | wireframes.md |
| DB設計 | 18-8 | er-diagram.puml |
| システム構成図・API | 18-9 | system-architecture.puml |
| WBS・ガントチャート | 18-10 | wbs.md |
| Notion連携 | 18-11 | notion-export.md |
| UIデザイン | 18-12 | design-system.md |
| プロトタイプ | 18-13 | prototype/ |
| E2Eテスト | 18-14 | e2e-tests/ |
| テスト計画 | 18-15 | test-plan.md |
| 単体テスト | 18-16 | unit-test-evidence/ |
| 結合テスト | 18-17 | integration-test-evidence/ |
| 会議体・議事録 | 18-18 | spec-changes.md |
| ダッシュボード | 18-19 | dashboard.py |
| 統合レビュー | 18-20 | capstone-review-summary.html |

---

**Module 18 を完了し、プロダクト開発の全工程をマスターしました。お疲れ様でした！**
