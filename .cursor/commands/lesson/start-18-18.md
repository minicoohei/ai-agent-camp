---
description: "When the user says /start-18-18 — Module 18 Lesson 18-18: PM - 会議体設計 & 議事録分析"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-17"]
level: "intermediate"
tags: ["pm", "meeting", "minutes", "spec-change"]
---

# 🎓 Lesson 18-18: 会議体設計 & 議事録分析

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowプロジェクトの会議体を設計し、サンプル議事録からAIで仕様変更を自動抽出する |
| 所要時間 | 約25分 |
| 使うスキル | pm-toolkit スキル |
| 前提条件 | Lesson 18-17 完了 |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 ステップ1: 会議体の種類と目的の設計

プロジェクトマネジメントにおいて、適切な会議体構造は情報流通と意思決定の効率性を大きく左右します。TaskFlowプロジェクトでは、プロジェクト規模に応じた会議体を設計する必要があります。

### 会議体の基本分類

**定例会議（Weekly/Bi-weekly）**
- スタンドアップミーティング: 進捗報告と課題共有（15分）
- スプリント計画会議: 次スプリントのタスク選定（60分）
- スプリント振り返り: 実績の反省と改善計画（45分）

**レビュー会議（As-needed）**
- 設計レビュー: 仕様の検討と承認（90分）
- コードレビュー: 品質保証と知見共有（60分）
- ビジネスレビュー: ステークホルダー報告（120分）

**振り返り会議（Sprint end）**
- 振り返りワークショップ: チーム間の学習と改善発見（60分）
- リスク振り返り: プロジェクトリスク評価（45分）

**臨時会議（Ad-hoc）**
- 緊急対応会議: 本番障害などの対応協議（30分）
- 顧客要望協議: 新要件の検討（60分）

```json
{
  "type": "AskQuestion",
  "question": "TaskFlowプロジェクトの会議体規模をどのように設計しますか?",
  "options": [
    {
      "id": "small_team",
      "label": "小規模チーム（3-5名）- 3種類の会議体",
      "meetings": [
        "Daily Standup",
        "Sprint Planning & Review",
        "Design Review"
      ],
      "frequency": "lightweight"
    },
    {
      "id": "medium_team",
      "label": "中規模チーム（6-15名）- 6種類の会議体",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Business Review"
      ],
      "frequency": "standard"
    },
    {
      "id": "large_org",
      "label": "大規模組織（16名以上）- 7種以上の会議体",
      "meetings": [
        "Daily Standup",
        "Sprint Planning",
        "Sprint Review",
        "Sprint Retrospective",
        "Design Review",
        "Code Review",
        "Business Review",
        "Risk Review",
        "Executive Steering"
      ],
      "frequency": "comprehensive"
    }
  ],
  "context": "会議体の規模はチーム構成、プロジェクト複雑度、ステークホルダー数によって決定されます。過度な会議は生産性低下を招くため、必要最小限で効果的な構成を目指します。"
}
```

## 🚀 ステップ2: PlantUMLで会議体構造図を作成

会議体の構造、関係性、流れを視覚的に表現するため、PlantUMLで構造図を作成します。

```json
{
  "type": "AskQuestion",
  "question": "会議体構造図のスタイルはどちらを選択しますか?",
  "options": [
    {
      "id": "org_chart",
      "label": "組織図型（会議体の階層と従属関係）",
      "focus": "hierarchy",
      "best_for": "意思決定フロー、責任分担の明確化"
    },
    {
      "id": "flow_chart",
      "label": "フロー型（時系列に沿った会議の流れ）",
      "focus": "timeline",
      "best_for": "スプリント周期、意思決定プロセス"
    },
    {
      "id": "matrix",
      "label": "マトリクス型（会議体と参加者・出力物の対応表）",
      "focus": "relationship",
      "best_for": "参加者の役割分担、責任範囲"
    }
  ],
  "context": "図のスタイル選択は、プレゼンテーション対象（経営層か現場か）と情報の見やすさによって決定します。"
}
```

### PlantUML図の例（フロー型）

```plantuml
@startuml TaskFlow_MeetingStructure
!define ACCENT_COLOR #FF6B6B
!define PRIMARY_COLOR #4ECDC4
!define SUCCESS_COLOR #95E1D3

skinparam defaultFontName "Courier New"
skinparam defaultFontSize 12
skinparam backgroundColor #FFFACD
skinparam classBorderColor #333
skinparam classBackgroundColor #FFF
skinparam arrowColor #333

rectangle "Sprint Cycle (2 weeks)" #E8F8F5 {
  node "Monday\nSprint Planning\n(10:00-11:00)" as planning #PRIMARY_COLOR
  node "Daily\nStandup\n(09:30-10:00)" as standup #4ECDC4
  node "Wednesday\nDesign Review\n(14:00-15:30)" as design #FF9999
  node "Friday\nSprint Review\n(15:00-16:30)" as review #ACCENT_COLOR
  node "Friday\nRetro\n(16:30-17:30)" as retro #95E1D3

  planning --> standup: attend
  standup --> design: issues found
  design --> review: design approved
  review --> retro: feedback
  retro --> planning: improvements
}

rectangle "Ad-hoc Meetings" #FFE8E8 {
  node "Customer Request\nMeeting" as customer #FF6B6B
  node "Emergency\nResponse" as emergency #DD3C51
}

note right of planning
  Attendees: Team Lead, Dev, PM
  Output: Sprint Goal, Task Board
end note

note right of design
  Attendees: Architect, Senior Dev
  Output: Design Approval, Issues
end note

@enduml
```

この図は以下の要素を含みます：

- **メインサイクル**: 2週間のスプリント周期内の定例会議
- **参加者**: 各会議への出席者リスト
- **出力物**: 会議から生成される成果物
- **依存関係**: 前の会議の決定が次の会議に影響する流れ

ファイルを生成してください: **output/pm/meeting-structure.puml**

## ⚠️ ステップ3: サンプル議事録の読み込み

以下のサンプル議事録を分析対象として使用します。

議事録には以下の情報が通常含まれます：

- **会議情報**: 日時、場所、参加者
- **アジェンダ**: 検討事項リスト
- **決定事項**: 合意された方針や仕様
- **アクションアイテム**: 後続タスク、担当者、期限
- **課題・リスク**: 顕在化した問題
- **次回会議予定**: フォローアップ

サンプル議事録の一部例：

```markdown
# 会議議事録

## 会議情報
- 日時: 2024-02-09 10:00-11:30
- 場所: Zoom / Meeting Room A
- 参加者: PM (田中), Dev Lead (佐藤), Architect (鈴木), QA (安藤)

## アジェンダ
1. Sprint #5 進捗報告
2. タスク作成画面のUI仕様について
3. API レスポンスタイムの最適化方針
4. 本番リリース前のテスト計画

## 決定事項
- タスク作成画面：「優先度」フィールドを追加（ドロップダウン：低/中/高/緊急）
- API レスポンスタイム目標：P95で500ms以下に設定
- 本番リリース：3月中旬を予定

## 仕様変更
- タスク作成API に priority フィールド追加 (enum: low, medium, high, urgent)
- タスク一覧API に フィルタ機能を実装 (filter by status, assignee, priority)
- UI: タスク詳細画面に「優先度」表示を追加

## アクションアイテム
| 項目 | 担当 | 期限 |
|------|------|------|
| 優先度フィールドの仕様書作成 | 鈴木 | 2024-02-12 |
| API スキーマ更新 | 佐藤 | 2024-02-13 |
| UI 画面設計書更新 | 田中 | 2024-02-14 |
| テストケース設計 | 安藤 | 2024-02-16 |

## リスク・課題
- API レスポンスタイム最適化は技術的複雑度が高い → 対応期間を1週間延長
- DB インデックス追加による影響評価が必要
```

```json
{
  "type": "AskQuestion",
  "question": "議事録分析の深さをどのレベルで実施しますか?",
  "options": [
    {
      "id": "spec_changes_only",
      "label": "仕様変更のみ抽出",
      "extraction_target": [
        "API スキーマ変更",
        "UI 要件変更",
        "DB スキーマ変更",
        "新機能追加"
      ]
    },
    {
      "id": "all_decisions",
      "label": "全決定事項抽出（仕様＋方針＋承認事項）",
      "extraction_target": [
        "仕様変更",
        "技術的判断",
        "リソース配置決定",
        "リリーススケジュール確定"
      ]
    },
    {
      "id": "comprehensive",
      "label": "アクションアイテム含む完全分析",
      "extraction_target": [
        "仕様変更",
        "全決定事項",
        "アクションアイテム（担当＋期限）",
        "リスク・課題の登録",
        "ステークホルダーの合意度"
      ]
    }
  ],
  "context": "分析の深さはプロジェクト規模と追跡体制によって決定します。中規模以上のプロジェクトでは、完全分析によるアクションアイテム管理が重要です。"
}
```

## ✅ ステップ4: AIによる仕様変更の自動抽出

議事録から仕様変更に該当する箇所を自動抽出し、構造化されたレポートとして生成します。

抽出する情報：

- **変更内容**: どのコンポーネント（API/UI/DB）が変わるのか
- **影響範囲**: どの機能やモジュールが影響を受けるのか
- **変更理由**: なぜこの変更が必要なのか（ビジネス要件か技術的理由か）
- **対応優先度**: この変更を実装する優先順位（Critical/High/Medium/Low）
- **推定工数**: 実装に必要な作業量（時間あるいはStory Points）
- **対応期限**: いつまでに対応する必要があるのか

自動抽出結果の出力形式（Markdown）:

```markdown
# 仕様変更抽出レポート

生成日時: 2024-02-10 15:45 JST
ソース: meeting-minutes-sample.md (2024-02-09)
分析対象: 4つの決定事項から3つの仕様変更を抽出

## 仕様変更一覧

### Change #1: タスク優先度フィールドの追加

| 項目 | 内容 |
|------|------|
| **変更内容** | タスク作成API に priority フィールドを追加（enum: low/medium/high/urgent） |
| **影響範囲** | - API: POST /tasks, GET /tasks, PUT /tasks/{id}<br>- DB: tasks テーブルに priority カラム追加<br>- UI: タスク作成・編集画面にドロップダウン追加<br>- テスト: 優先度フィルタのテストケース追加 |
| **変更理由** | ビジネス要件。タスクの優先度付けにより、チームが重要度に基づいて作業を優先できるようになる。顧客からの要望。 |
| **対応優先度** | **High** |
| **推定工数** | 8 Story Points (API 3日 + UI 2日 + テスト 2日) |
| **対応期限** | 2024-02-16 |
| **設計担当** | 鈴木 |
| **実装担当** | 佐藤チーム |

関連アクションアイテム:
- [ ] 仕様書の詳細化 (期限: 2024-02-12)
- [ ] API スキーマの更新 (期限: 2024-02-13)
- [ ] 画面設計書の更新 (期限: 2024-02-14)
- [ ] テストケース設計 (期限: 2024-02-16)

### Change #2: タスク一覧フィルタ機能の実装

| 項目 | 内容 |
|------|------|
| **変更内容** | GET /tasks API にクエリパラメータベースのフィルタ機能を追加<br>対応フィルタ: status, assignee, priority |
| **影響範囲** | - API: GET /tasks エンドポイントの拡張<br>- DB: インデックス最適化（performance向上）<br>- フロントエンド: フィルタUI の実装 |
| **変更理由** | ユーザビリティ向上。ユーザーが大量のタスクから必要なものを効率的に検索できるようになる。 |
| **対応優先度** | **High** |
| **推定工数** | 13 Story Points (API 3日 + フロント 2日 + DB最適化 1日 + テスト 2日) |
| **対応期限** | 2024-02-23 |
| **設計担当** | 鈴木 |
| **実装担当** | 佐藤、田中 |

リスク: DB インデックス追加による既存データへの影響評価が必要

### Change #3: API レスポンスタイムの目標設定

| 項目 | 内容 |
|------|------|
| **変更内容** | API レスポンスタイムの非機能要件を設定<br>P95: 500ms以下, P99: 1000ms以下 |
| **影響範囲** | - API: 全エンドポイントの最適化<br>- インフラ: キャッシング戦略の導入<br>- テスト: パフォーマンステスト自動化 |
| **変更理由** | 技術的必要性。ユーザー体験向上。SLA 達成の必須条件。 |
| **対応優先度** | **Critical** |
| **推定工数** | 21 Story Points (調査・分析 2日 + 実装 4日 + テスト 2日 + 本番検証 1日) |
| **対応期限** | 2024-03-01 (本番リリース前) |
| **設計担当** | 鈴木 |
| **実装担当** | 佐藤 (バックエンド), インフラチーム |

## サマリー

- **抽出仕様変更数**: 3件
- **Critical**: 1件
- **High**: 2件
- **総推定工数**: 42 Story Points
- **リスク件数**: 1件（DB インデックス検証）
- **次回フォローアップ**: 2024-02-13 進捗確認ミーティング

## 自動抽出の信頼度

- 全抽出項目の AI 確信度: 95%
- 手動確認推奨項目: Change #2 の DB インデックス影響評価
- 確認責任者: インフラリード (山田)
```

ファイルを生成してください: **output/pm/spec-changes.md**


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── retrospective.md  (振り返りレポート)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/retrospective.md

# 冒頭を確認（最初の30行）
head -30 output/pm/retrospective.md
```

> 💡 全文を確認: `cat output/pm/retrospective.md` で全文表示できます

## ➡️ 完成と次のステップ

以下の成果物が完成しており、output/pm/ に配置されていることを確認してください。

**生成すべきファイル:**

1. **meeting-structure.puml** - PlantUML形式の会議体構造図
   - スプリント周期内の定例会議を表示
   - 各会議の参加者と出力物を記載
   - Ad-hoc会議を別セクションで表示

2. **spec-changes.md** - 仕様変更抽出レポート
   - 変更内容、影響範囲、理由を含む表形式
   - 優先度とリスク評価
   - アクションアイテムとの対応付け

**達成条件:**
- PlantUML図が正しく描画可能（エラーなし）
- 仕様変更が 3件以上抽出されている
- 各変更に対して優先度と推定工数が明記されている
- AI 抽出の確信度が 90%以上

**Next Lesson**: `/start-18-19` でmarimoダッシュボード作成に進みましょう

このレッスンで習得した会議体設計とAI議事録分析のスキルは、プロジェクトの意思決定を可視化し、変更要件の漏れを防ぐための重要なプラクティスです。構造化された会議管理と自動化された情報抽出により、PM の効率と精度が大きく向上します。
