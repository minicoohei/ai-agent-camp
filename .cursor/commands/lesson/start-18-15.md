---
description: "When the user says /start-18-15 — Module 18 Lesson 18-15: PM - テスト計画書 & テストケース生成"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-14", "output/pm/usecases.md"]
level: "intermediate"
tags: ["pm", "test", "test-plan", "test-cases"]
---

# 🎓 Lesson 18-15: テスト計画書 & テストケース生成

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowのユースケースからテスト計画書とテストケースを自動生成する |
| 所要時間 | 約25分 |
| 使うスキル | test-planner スキル |
| 前提条件 | output/pm/usecases.md が存在する |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 Step 1: テスト計画書の構成説明

### テスト計画書の基本要素

テスト計画書は、以下の要素で構成されます：

- **テスト対象範囲**: システムのどの部分をテストするか
- **テスト戦略**: 何をどのように検証するか
- **テスト環境**: テスト用の環境構成
- **スケジュール**: テスト実施期間と各フェーズのタイミング
- **リソース**: テスト実行に必要なツールと人員
- **成功基準**: テスト合格の基準

テストケースは、個別の機能やシナリオをテストするための具体的な手順と期待値です。

### あなたのテスト経験レベルはどのレベルですか？

```json
{
  "type": "AskQuestion",
  "question": "あなたのテスト経験レベルをお選びください。これによってテスト計画書の詳細度と複雑さを調整します。",
  "options": [
    {
      "id": "beginner",
      "label": "初級者 - テストの経験が少ない or テスト観点が不明確",
      "value": "beginner",
      "description": "AI がテスト観点を多めに提案し、詳細な説明を含めます"
    },
    {
      "id": "intermediate",
      "label": "中級者 - 基本的なテスト観点は理解している",
      "value": "intermediate",
      "description": "標準的なテスト計画書とテストケースを生成します"
    },
    {
      "id": "advanced",
      "label": "上級者 - テスト戦略や最適化まで考慮する",
      "value": "advanced",
      "description": "リスク分析、カバレッジ最適化、効率化まで含めた計画を提案"
    }
  ],
  "required": true,
  "helpText": "選択したレベルに基づいて、適切な詳細度のテスト計画書とテストケースを生成します。"
}
```

---

## 🚀 Step 2: ユースケースからテストケース生成

### テスト観点の分類

テストケースを効果的に生成するには、複数の観点からのテストが必要です：

1. **正常系テスト**: ユースケースの正常な流れをテスト
2. **異常系テスト**: エラーや予期しない入力をテスト
3. **境界値テスト**: 入力値の最小値・最大値・その周辺をテスト
4. **セキュリティテスト**: 認可・認証・入力検証などをテスト

### どの観点までテストケースを生成しますか？

```json
{
  "type": "AskQuestion",
  "question": "テストケース生成で、どの観点までカバーしたいですか？段階的に詳細度が増します。",
  "options": [
    {
      "id": "normal_only",
      "label": "正常系のみ",
      "value": "normal_only",
      "description": "ユースケースの正常な流れのテストケースのみを生成（最小限）"
    },
    {
      "id": "normal_abnormal",
      "label": "正常系 + 異常系",
      "value": "normal_abnormal",
      "description": "正常な流れと一般的なエラーパターンをカバー（標準的）"
    },
    {
      "id": "normal_abnormal_boundary",
      "label": "正常系 + 異常系 + 境界値",
      "value": "normal_abnormal_boundary",
      "description": "上記に加えて境界値テストを含む（より詳細）"
    },
    {
      "id": "comprehensive",
      "label": "正常系 + 異常系 + 境界値 + セキュリティ",
      "value": "comprehensive",
      "description": "セキュリティテストを含む完全なテストカバレッジ（最詳細）"
    }
  ],
  "required": true,
  "helpText": "選択した観点に基づいて、テストケース数と詳細度が決定されます。最初は『正常系 + 異常系』がバランス型です。"
}
```

### テストケースの生成プロセス

選択に基づいて、以下の処理が実行されます：

1. output/pm/usecases.md を読み込み
2. 各ユースケースから、選択した観点のテストケースを自動生成
3. テストケースに ID、説明、前提条件、手順、期待値を付与
4. テストケースをグループ化（ユースケース別、機能別など）
5. output/pm/test-cases.md に保存

テストケースは以下の形式で生成されます：

```text
### テストケース ID: TC-001
**ユースケース**: UC-001 - ユーザー登録
**観点**: 正常系
**説明**: メールアドレスとパスワードでユーザー登録が成功する

**前提条件**:
- システムがアクセス可能
- ユーザーは未登録状態

**テスト手順**:
1. 登録画面を開く
2. メールアドレスを入力（例：user@example.com）
3. パスワードを入力（例：Pass1234!）
4. 登録ボタンをクリック

**期待値**:
- 登録が成功する
- 確認メールが送信される
- ユーザーがログイン可能になる
```

---

## ⚠️ Step 3: テストケースの優先順位付け

### 優先度付けの考え方

テストケースの数が多い場合、すべてのテストケースを実施することは難しい場合があります。
リソースに限りがある場合は、優先度を付けて重要なテストから順に実施します。

優先度付けの主な方法：

1. **リスクベース**: ビジネスリスクが高い機能のテストを優先
2. **カバレッジベース**: より多くの機能・分岐をカバーするテストを優先
3. **AI提案**: 過去のデータやベストプラクティスに基づいて AI が優先度を提案

### テストケースの優先度付け方法をお選びください

```json
{
  "type": "AskQuestion",
  "question": "生成したテストケースの優先順位付け方法をお選びください。限定的なテスト期間の場合に有効です。",
  "options": [
    {
      "id": "risk_based",
      "label": "リスクベース優先度付け",
      "value": "risk_based",
      "description": "ビジネスリスクが高い機能（認証、決済など）のテストケースを上位に配置"
    },
    {
      "id": "coverage_based",
      "label": "カバレッジベース優先度付け",
      "value": "coverage_based",
      "description": "機能・分岐カバレッジが高いテストケースを上位に配置（限定予算で最大カバレッジを達成）"
    },
    {
      "id": "ai_suggested",
      "label": "AI推奨優先度付け",
      "value": "ai_suggested",
      "description": "ベストプラクティスと機能の複雑さを組み合わせた優先度を AI が提案"
    },
    {
      "id": "priority_all",
      "label": "すべてを優先度付け（推奨）",
      "value": "priority_all",
      "description": "上記 3 つの観点をすべて採用し、複数の優先度ランクを表示（最も柔軟）"
    }
  ],
  "required": true,
  "helpText": "リスクベースが最も一般的です。複数の観点が必要な場合は『AI推奨』または『すべてを優先度付け』を選択してください。"
}
```

### 優先度付けの実行

選択した方法に基づいて：

1. 各テストケースに優先度スコアを計算
2. リスク行列、カバレッジマップなどを生成
3. 優先度による実施順序を決定
4. output/pm/test-cases.md に優先度情報を追記

---

## ✅ Step 4: テスト計画書と テストケース生成の実行

### 生成されるファイル

**output/pm/test-plan.md**
```text
# テスト計画書

## 1. テスト対象範囲
- TaskFlow バックエンド API
- フロントエンド UI
- 認証・認可機能
- タスク管理機能
- 通知機能

## 2. テスト戦略
- 単体テスト (Unit Test)
- 統合テスト (Integration Test)
- E2E テスト (End-to-End Test)

## 3. テスト環境
- 開発環境: localhost:3000
- テスト DB: SQLite (テスト専用)

## 4. スケジュール
- フェーズ 1: 単体テスト (5 営業日)
- フェーズ 2: 統合テスト (3 営業日)
- フェーズ 3: E2E テスト (2 営業日)

## 5. 成功基準
- テストケース実行率: 100%
- テストケース成功率: 95% 以上
- 重大バグ: 0 件
```

**output/pm/test-cases.md**
```text
# テストケース一覧

## ユースケース UC-001: ユーザー登録

### TC-001 正常系 - 通常のユーザー登録
**優先度**: High (リスクベース)
**優先度**: High (カバレッジベース)
**期待値**: 登録成功

### TC-002 異常系 - メールアドレス重複
**優先度**: High
**期待値**: エラーメッセージ表示

### TC-003 異常系 - パスワード不足
**優先度**: Medium
**期待値**: バリデーション エラー表示

## ユースケース UC-002: タスク作成
...
```

### 実行コマンド

```bash
# test-planner スキルを実行（対話形式で Step 1-3 の選択肢に回答）
/test-planner
```

または、スキルが自動的に以下を実行します：

1. **テスト計画書の生成**
   ```bash
   uv run python tools/test_planner.py \
     --input output/pm/usecases.md \
     --output output/pm/test-plan.md \
     --experience-level <選択値> \
     --test-scope <選択値>
   # Windowsでは python3 を python に読み替えてください
   ```

2. **テストケースの生成**
   ```bash
   uv run python tools/test_case_generator.py \
     --input output/pm/usecases.md \
     --output output/pm/test-cases.md \
     --coverage <選択値> \
     --prioritize <選択値>
   # Windowsでは python3 を python に読み替えてください
   ```

3. **ファイルの生成確認**
   ```bash
   ls -la output/pm/test-plan.md output/pm/test-cases.md
   ```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/
└── test-cases.md  (テストケース)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/test-cases.md

# 冒頭を確認（最初の30行）
head -30 output/pm/test-cases.md
```

> 💡 全文を確認: `cat output/pm/test-cases.md` で全文表示できます

---

## ➡️ Next Step

次のレッスンに進む準備ができました：

**[start-18-16: 単体テスト実施（pytest）](./start-18-16.md)**

Lesson 18-16 では、生成したテストケースに基づいて、バックエンドロジックに対する pytest による単体テストを実施します。
