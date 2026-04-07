---
description: "When the user says /start-18-10 — Module 18 Lesson 18-10: PM - WBS & ガントチャート"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-9", "output/pm/api-spec.yaml"]
level: "intermediate"
tags: ["pm", "wbs", "gantt", "schedule"]
---

# 🎓 Lesson 18-10: WBS & ガントチャート

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowプロジェクトのWBSを作成し、PlantUMLでガントチャートを生成する |
| 所要時間 | 約25分 |
| 使うスキル | pm-toolkit スキル |
| 前提条件 | Lesson 18-9 完了、これまでの設計ドキュメントが揃っている |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

---

## 📍 学習目標

このレッスンでは、以下の内容を学習します：

- **WBS（Work Breakdown Structure）** の作成方法
- プロジェクトのタスク分解と階層構造化
- 工数見積もりの主要手法
- PlantUML Ganttチャートの生成と活用
- クリティカルパスの分析

---

## 🚀 ステップ1：WBSの作成

Work Breakdown Structure（WBS）は、プロジェクトをより小さく管理可能なタスクに分解する手法です。TaskFlowプロジェクトの全体構造を可視化します。

### 📊 TaskFlow WBS構造

```text
TaskFlow プロジェクト
├── 1. 企画フェーズ
│   ├── 1.1 要件定義
│   ├── 1.2 競合分析
│   └── 1.3 プロジェクト計画
├── 2. 設計フェーズ
│   ├── 2.1 システム設計
│   ├── 2.2 UI/UX設計
│   ├── 2.3 データベース設計
│   └── 2.4 API仕様設計
├── 3. 実装フェーズ
│   ├── 3.1 バックエンド開発
│   ├── 3.2 フロントエンド開発
│   ├── 3.3 インテグレーション
│   └── 3.4 テスト環境構築
├── 4. テストフェーズ
│   ├── 4.1 単体テスト
│   ├── 4.2 統合テスト
│   ├── 4.3 UAT
│   └── 4.4 本番環境テスト
└── 5. デプロイ・運用フェーズ
    ├── 5.1 本番環境準備
    ├── 5.2 デプロイメント
    ├── 5.3 運用開始
    └── 5.4 利用者サポート設定
```

### ❓ WBSの粒度を選択

```json
{
  "type": "AskQuestion",
  "id": "wbs-granularity",
  "question": "WBSの粒度を選んでください",
  "description": "WBSの分解レベルは、プロジェクトの規模と複雑さに応じて選択します",
  "options": [
    {
      "value": "level2",
      "label": "大項目のみ（Level 2）",
      "description": "5つの主フェーズのみ。小規模プロジェクト向け",
      "recommended": false
    },
    {
      "value": "level3",
      "label": "中項目まで（Level 3）",
      "description": "各フェーズの主要タスク。推奨レベル",
      "recommended": true
    },
    {
      "value": "level4",
      "label": "詳細（Level 4）",
      "description": "さらに細分化。複雑なプロジェクト向け",
      "recommended": false
    },
    {
      "value": "ai-suggest",
      "label": "AIに最適な粒度を提案してもらう",
      "description": "プロジェクト規模から自動判定"
    }
  ],
  "default": "level3"
}
```

---

## 💼 ステップ2：工数見積もり

WBSの各タスクに対して、実現に必要な工数を見積もります。正確な工数見積もりはプロジェクト成功の鍵です。

### 📌 主要な見積もり手法

| 手法 | 特徴 | 適用場面 |
|------|------|---------|
| **類推見積もり** | 過去の類似プロジェクトから推定 | 経験が豊富にある場合 |
| **3点見積もり** | 楽観値/最頻値/悲観値から算出 | 不確実性が高い場合 |
| **ファンクションポイント法** | 機能の複雑さで算出 | ソフトウェア開発 |
| **ボトムアップ見積もり** | 詳細タスクから積み上げ | 詳細設計後 |

### ❓ 見積もり手法を選択

```json
{
  "type": "AskQuestion",
  "id": "estimation-method",
  "question": "見積もり手法を選んでください",
  "description": "プロジェクト特性に応じて適切な見積もり手法を選択してください",
  "options": [
    {
      "value": "analogy",
      "label": "類推見積もり",
      "description": "過去の類似プロジェクトから推定。迅速な見積もり向け"
    },
    {
      "value": "three-point",
      "label": "3点見積もり（楽観/最頻/悲観）",
      "description": "PERT手法。不確実性を考慮した精密な見積もり"
    },
    {
      "value": "function-point",
      "label": "ファンクションポイント法",
      "description": "機能の複雑度で定量化。ソフトウェア開発に最適"
    },
    {
      "value": "ai-estimate",
      "label": "AIに見積もってもらう",
      "description": "WBSを分析して自動見積もり"
    }
  ],
  "default": "three-point"
}
```

### 📋 TaskFlow 工数見積もり例（3点見積もり）

| WBSコード | タスク | 楽観（日） | 最頻（日） | 悲観（日） | 期待値（日） |
|-----------|--------|----------|----------|----------|-----------|
| 1.1 | 要件定義 | 2 | 3 | 5 | 3.2 |
| 1.2 | 競合分析 | 1 | 2 | 4 | 2.2 |
| 1.3 | プロジェクト計画 | 1 | 2 | 3 | 2.0 |
| 2.1 | システム設計 | 3 | 5 | 8 | 5.2 |
| 2.2 | UI/UX設計 | 2 | 4 | 7 | 4.2 |
| 2.3 | DB設計 | 2 | 3 | 5 | 3.2 |
| 2.4 | API仕様設計 | 2 | 3 | 5 | 3.2 |
| 3.1 | バックエンド開発 | 8 | 12 | 18 | 12.3 |
| 3.2 | フロントエンド開発 | 6 | 10 | 15 | 10.2 |
| 3.3 | インテグレーション | 2 | 4 | 7 | 4.2 |
| 3.4 | テスト環境構築 | 1 | 2 | 3 | 2.0 |
| 4.1 | 単体テスト | 3 | 5 | 8 | 5.2 |
| 4.2 | 統合テスト | 2 | 4 | 6 | 4.0 |
| 4.3 | UAT | 2 | 3 | 5 | 3.2 |
| 4.4 | 本番環境テスト | 1 | 2 | 3 | 2.0 |
| 5.1 | 本番環境準備 | 1 | 2 | 4 | 2.2 |
| 5.2 | デプロイメント | 1 | 2 | 3 | 2.0 |
| 5.3 | 運用開始 | 1 | 2 | 3 | 2.0 |
| 5.4 | サポート設定 | 1 | 1 | 2 | 1.2 |

**計画総工数：73.7人日**

---

## 📅 ステップ3：PlantUML Ganttチャートの生成

ガントチャートはプロジェクトのスケジュール、タスク依存関係、進捗を可視化します。

### ❓ ガントチャート表示期間を選択

```json
{
  "type": "AskQuestion",
  "id": "gantt-period",
  "question": "ガントチャートの表示期間を選んでください",
  "description": "プロジェクトの期間に応じて表示期間を選択します",
  "options": [
    {
      "value": "1month",
      "label": "1ヶ月",
      "description": "詳細な日単位の表示"
    },
    {
      "value": "3months",
      "label": "3ヶ月",
      "description": "推奨。一般的なプロジェクト期間"
    },
    {
      "value": "6months",
      "label": "6ヶ月",
      "description": "大規模プロジェクト向け"
    },
    {
      "value": "custom",
      "label": "カスタム",
      "description": "任意の期間を指定"
    }
  ],
  "default": "3months"
}
```

### 📊 PlantUML Ganttチャート例

```plantuml
@startgantt
title TaskFlow プロジェクト ガントチャート
dateFormat YYYY-MM-DD
projectScale monthly
axisFormat %Y-%m

section 企画
要件定義           :crit, wbs-1-1, 2024-04-01, 3d
競合分析           :crit, wbs-1-2, after wbs-1-1, 2d
プロジェクト計画     :crit, wbs-1-3, after wbs-1-2, 2d

section 設計
システム設計       :des1, wbs-2-1, after wbs-1-3, 5d
UI/UX設計         :des1, wbs-2-2, after wbs-1-3, 4d
DB設計            :des2, wbs-2-3, after wbs-2-1, 3d
API仕様設計       :des2, wbs-2-4, after wbs-2-1, 3d
デザインレビュー   :milestone, des-review, after wbs-2-4, 1d

section 実装
バックエンド開発   :impl1, wbs-3-1, after des-review, 12d
フロントエンド開発  :impl1, wbs-3-2, after des-review, 10d
インテグレーション  :impl2, wbs-3-3, after wbs-3-1, 4d
テスト環境構築     :impl2, wbs-3-4, after wbs-3-1, 2d

section テスト
単体テスト        :test1, wbs-4-1, after wbs-3-3, 5d
統合テスト        :test1, wbs-4-2, after wbs-4-1, 4d
UAT              :test2, wbs-4-3, after wbs-4-2, 3d
本番環境テスト     :test2, wbs-4-4, after wbs-4-3, 2d
テスト完了       :milestone, test-complete, after wbs-4-4, 1d

section デプロイ・運用
本番環境準備      :deploy1, wbs-5-1, after test-complete, 2d
デプロイメント    :deploy1, wbs-5-2, after wbs-5-1, 2d
運用開始         :deploy2, wbs-5-3, after wbs-5-2, 2d
サポート設定      :deploy2, wbs-5-4, after wbs-5-3, 1d
リリース         :crit, milestone, after wbs-5-4, 1d

@endgantt
```

### 🎯 PlantUML Gantt文法の主要要素

```markdown
- **dateFormat**: 日付形式（YYYY-MM-DDなど）
- **projectScale**: 表示単位（daily/weekly/monthly）
- **section**: セクション（フェーズ）名
- **タスク定義**: `タスク名 :type, id, start, duration`
  - type: `crit`(重要), `milestone`(マイルストーン), `active`(進行中)
  - start: `2024-04-01` または `after id`
  - duration: `5d`(5日), `1w`(1週間)
- **マイルストーン**: `milestone` type で表示
```

---

## 🔍 ステップ4：クリティカルパス分析

クリティカルパスはプロジェクト完了までの最長経路であり、遅延の影響が最も大きいタスク群です。

### ❓ クリティカルパス分析の実施

```json
{
  "type": "AskQuestion",
  "id": "critical-path",
  "question": "クリティカルパス分析をしますか？",
  "description": "クリティカルパスを特定することで、プロジェクトの遅延リスクを管理します",
  "options": [
    {
      "value": "ai-analyze",
      "label": "はい、AIに分析してもらう",
      "description": "WBSと工数から自動分析。推奨"
    },
    {
      "value": "manual",
      "label": "自分で確認する",
      "description": "WBSと依存関係を確認して手動で特定"
    },
    {
      "value": "skip",
      "label": "スキップ",
      "description": "クリティカルパス分析をスキップ"
    }
  ],
  "default": "ai-analyze"
}
```

### 📍 TaskFlow クリティカルパス例

**最長経路（総工数約55日）：**
```text
要件定義（3.2日）
→ 競合分析（2.2日）
→ プロジェクト計画（2.0日）
→ システム設計（5.2日）
→ API仕様設計（3.2日）
→ バックエンド開発（12.3日）
→ インテグレーション（4.2日）
→ 単体テスト（5.2日）
→ 統合テスト（4.0日）
→ UAT（3.2日）
→ 本番環境テスト（2.0日）
→ 本番環境準備（2.2日）
→ デプロイメント（2.0日）
→ 運用開始（2.0日）
→ サポート設定（1.2日）
```

### ⚠️ リスク領域の特定

| リスク領域 | 要因 | 対策 |
|-----------|------|------|
| バックエンド開発 | 最長（12.3日）の実装タスク | 早期着手、リソース確保 |
| インテグレーション | 予期しない相互作用 | 早期統合テスト実施 |
| データベース設計 | 要件変更の可能性 | 要件確定を最優先 |

---

## 📝 成果物の確認リスト

### ✅ 出力ファイル

1. **output/pm/wbs.md** - WBS構造と詳細説明
2. **output/pm/gantt-chart.puml** - PlantUML Ganttチャート

### ✅ チェックポイント

```markdown
□ WBS を Level 3 以上に分解
□ 工数見積もりが全タスクに設定済み
□ ガントチャートが生成済み
□ マイルストーンが3つ以上設定済み
□ wbs.md ファイルが生成済み
□ gantt-chart.puml ファイルが生成済み
□ クリティカルパスが識別済み（オプション）
□ リスク領域が特定済み（オプション）
```

---

## 🔧 トラブルシューティング

### ❓ WBSの分解粒度がわからない

**解決策：**
- まずは Level 3（中項目）で開始することを推奨
- タスク数が 20～30 個が管理しやすい範囲
- フェーズごとに 3～5 個の WBS 項目が目安

### ❓ 工数見積もりの根拠がない

**解決策：**
- 過去の類似タスク実績を参照
- チームメンバーのスキルレベルを考慮
- 3点見積もりで不確実性を吸収
- バッファ（10～20%）を確保

### ❓ PlantUML Gantt 構文がわからない

**解決策：**
- [PlantUML Gantt 公式ドキュメント](https://plantuml.com/gantt-diagram)を参照
- `after` キーワードで依存関係を表現
- `milestone` で主要な節目を表示
- `crit` で重要なタスクをハイライト

### ❓ クリティカルパスの概念が理解できない

**解決策：**
- CPM（Critical Path Method）の基本を学習
- 各タスクの「最早開始日」「最遅開始日」を計算
- スラック（余裕）がゼロのタスク群がクリティカルパス
- 遅延影響が最も大きいため、優先的に管理

---

## 🎬 次のステップ

### ➡️ 次のレッスン

**[Lesson 18-11: Notion連携](./start-18-11.md)**

Notion 統合により、WBS と ガントチャートを チーム全体で共有し、リアルタイムで進捗を管理します。

### 📚 関連リソース

- [Module 18: PM & システム定義](https://ai-agent.camp/ja/course/module-18)
- [PlantUML Gantt 公式ドキュメント](https://plantuml.com/gantt-diagram)

---

## 📌 重要なポイント

🎯 **WBS は「何をするか」を明確にする**
- 曖昧なタスクは後々のトラブルの原因になる
- 各タスクは独立し、かつ包括的であるべき（MECE原則）

⏱️ **工数見積もりは控えめに**
- 初期見積もりは 20～30% のバッファを追加
- 実装中に不確実性が減少すれば、バッファを削減可能

📊 **ガントチャートは生きたドキュメント**
- プロジェクト開始後も定期的に更新
- 実績と計画のズレを定期的に確認（進捗率、残工数）

🚨 **クリティカルパス外のタスクは柔軟性がある**
- バッファ（スラック）を有効活用してリソース調整
- ただし、スラックが消費されるとクリティカルパスが変わることに注意

---

**このレッスンが完了したら、Lesson 18-11 へ進みます。**
