---
description: "When the user says /start-18-16 — Module 18 Lesson 18-16: PM - 単体テスト実施（pytest）"
duration: "25分"
category: "lesson"
prerequisites: ["start-18-15", "output/pm/test-cases.md"]
level: "intermediate"
tags: ["pm", "test", "unit-test", "pytest"]
---

# 🎓 Lesson 18-16: 単体テスト実施

| 項目 | 内容 |
|------|------|
| ゴール | TaskFlowのバックエンドロジックに対しpytestで単体テストを実施し、エビデンスを取得する |
| 所要時間 | 約25分 |
| 使うスキル | test-planner スキル |
| 前提条件 | Lesson 18-15 完了、output/pm/test-cases.md が存在する |
| 教材ページ | [Module 18](https://ai-agent.camp/ja/course/module-18) |

## 📍 Step 1: テスト対象関数の特定

### TaskFlow バックエンドの主要モジュール

TaskFlow のバックエンドは、以下の機能モジュールで構成されています：

1. **認証・認可モジュール** (`auth.py`)
   - ユーザー認証、トークン生成、権限チェック

2. **タスク CRUD モジュール** (`tasks.py`)
   - タスクの作成・読取・更新・削除

3. **バリデーションモジュール** (`validators.py`)
   - 入力値のバリデーション、ビジネスロジックの検証

4. **通知モジュール** (`notifications.py`)
   - メール送信、Slack 通知

5. **DB アクセスモジュール** (`database.py`)
   - データベース操作、トランザクション管理

### どのモジュールのテストを実施しますか？

```json
{
  "type": "AskQuestion",
  "question": "テスト対象となる機能モジュールをお選びください。複数選択も可能です。",
  "options": [
    {
      "id": "auth_logic",
      "label": "認証ロジック (auth.py)",
      "value": "auth_logic",
      "description": "ユーザー認証、トークン生成、権限チェック機能のテスト"
    },
    {
      "id": "task_crud",
      "label": "タスク CRUD (tasks.py)",
      "value": "task_crud",
      "description": "タスク作成・更新・削除・検索機能のテスト"
    },
    {
      "id": "validation",
      "label": "バリデーション (validators.py)",
      "value": "validation",
      "description": "入力値検証とビジネスロジック検証のテスト"
    },
    {
      "id": "notifications",
      "label": "通知モジュール (notifications.py)",
      "value": "notifications",
      "description": "メール、Slack 通知機能のテスト（モック使用）"
    },
    {
      "id": "all_modules",
      "label": "すべてのモジュール",
      "value": "all_modules",
      "description": "上記すべてのモジュールの包括的なテスト"
    }
  ],
  "required": true,
  "helpText": "最初は『タスク CRUD』または『バリデーション』がテストしやすくお勧めです。"
}
```

### テスト対象関数の抽出

選択したモジュールに基づいて、以下の情報を分析します：

- 各関数のシグネチャ（入出力）
- 依存関係（他の関数やライブラリへの依存）
- サイドエフェクト（DB操作、外部 API 呼び出しなど）
- 既存のテストコード（あれば）
- カバレッジ未達成の行

抽出された関数例：

```python
# auth.py
def authenticate_user(email: str, password: str) -> Dict[str, Any]
def verify_token(token: str) -> Dict[str, Any]
def check_permission(user_id: int, resource_id: int) -> bool

# tasks.py
def create_task(user_id: int, title: str, description: str) -> Task
def update_task(task_id: int, updates: Dict) -> Task
def delete_task(task_id: int) -> bool
def get_tasks_by_user(user_id: int, filters: Dict) -> List[Task]

# validators.py
def validate_email(email: str) -> bool
def validate_password(password: str) -> bool
def validate_task_input(title: str, description: str) -> bool
```

---

## 🚀 Step 2: pytestテストコードの生成

### pytest のテストスタイル

pytest では、複数のテストコード作成スタイルがあります：

1. **関数型テスト** - シンプルで読みやすい（初心者向け）
   ```python
   def test_authenticate_user_success():
       result = authenticate_user("user@example.com", "Pass1234!")
       assert result["success"] is True
   ```

2. **クラス型テスト** - 関連テストを整理（中規模プロジェクト向け）
   ```python
   class TestAuthentication:
       def test_authenticate_user_success(self):
           ...
   ```

3. **Fixture 活用** - 前後処理とモック管理（大規模プロジェクト向け）
   ```python
   @pytest.fixture
   def test_user():
       return create_test_user()

   def test_authenticate_user(test_user):
       result = authenticate_user(test_user.email, "Pass1234!")
       assert result["success"] is True
   ```

4. **AI 推奨スタイル** - プロジェクト規模と複雑さに基づいた最適なスタイル

### どのテストスタイルで生成しますか？

```json
{
  "type": "AskQuestion",
  "question": "pytest テストコードの作成スタイルをお選びください。プロジェクト規模と複雑さに基づいて選択します。",
  "options": [
    {
      "id": "function_style",
      "label": "関数型テスト",
      "value": "function_style",
      "description": "シンプルで読みやすい。初心者や小規模なテストに最適"
    },
    {
      "id": "class_style",
      "label": "クラス型テスト",
      "value": "class_style",
      "description": "関連するテストをグループ化。中規模プロジェクト向け"
    },
    {
      "id": "fixture_style",
      "label": "Fixture 活用",
      "value": "fixture_style",
      "description": "テスト前後の準備処理を効率化。大規模プロジェクト向け"
    },
    {
      "id": "ai_recommended",
      "label": "AI推奨スタイル",
      "value": "ai_recommended",
      "description": "AI がプロジェクト規模と複雑さに基づいて最適なスタイルを選択"
    }
  ],
  "required": true,
  "helpText": "最初は『関数型テスト』でシンプルに始めることがお勧めです。複雑なセットアップが必要な場合は『Fixture 活用』を選択します。"
}
```

### テストコード生成のプロセス

選択したスタイルに基づいて、以下が実行されます：

1. **Lesson 18-15 で生成したテストケースを読み込み**
   - output/pm/test-cases.md からテストケースを抽出

2. **テスト関数テンプレートの生成**
   ```python
   # test_tasks.py
   import pytest
   from app.tasks import create_task, update_task, delete_task
   from app.models import Task

   # 正常系テスト
   def test_create_task_success():
       """TC-004: 正常系 - タスク作成成功"""
       task = create_task(
           user_id=1,
           title="New Task",
           description="Task description"
       )
       assert task.title == "New Task"
       assert task.user_id == 1

   # 異常系テスト
   def test_create_task_empty_title():
       """TC-005: 異常系 - タイトルが空文字列"""
       with pytest.raises(ValueError, match="Title cannot be empty"):
           create_task(user_id=1, title="", description="desc")

   # 境界値テスト
   def test_create_task_max_title_length():
       """TC-006: 境界値 - タイトル最大文字数"""
       long_title = "x" * 255
       task = create_task(user_id=1, title=long_title, description="desc")
       assert len(task.title) == 255
   ```

3. **モック・フィクスチャの作成**
   ```python
   @pytest.fixture
   def test_user():
       return User(id=1, email="test@example.com")

   @pytest.fixture
   def test_db(monkeypatch):
       # テスト用 DB をセットアップ
       monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
   ```

4. **テストコードファイルの生成**
   - output/pm/unit-test-code/test_auth.py
   - output/pm/unit-test-code/test_tasks.py
   - output/pm/unit-test-code/test_validators.py
   - output/pm/unit-test-code/conftest.py (共通 Fixture)

---

## ⚠️ Step 3: テスト実行 & エビデンスキャプチャ

### pytest 実行方法の選択

テスト実行にはいくつかのパターンがあります：

1. **全テスト実行** - すべてのテストを一度に実行
2. **カテゴリ別実行** - モジュール別（auth テスト、tasks テスト）に分けて実行
3. **1つずつ実行** - デバッグが必要な場合、個別テストを確認しながら実行

### テスト実行方法をお選びください

```json
{
  "type": "AskQuestion",
  "question": "pytest テストの実行方法をお選びください。詳細なエビデンスキャプチャが必要です。",
  "options": [
    {
      "id": "run_all",
      "label": "全テスト実行",
      "value": "run_all",
      "description": "すべてのテストを一度に実行。実行時間が短い（推奨）"
    },
    {
      "id": "run_by_category",
      "label": "カテゴリ別実行",
      "value": "run_by_category",
      "description": "モジュール別（auth, tasks, validators）に分けて実行。詳細な結果が得られる"
    },
    {
      "id": "run_individually",
      "label": "1つずつ実行",
      "value": "run_individually",
      "description": "個別テストを確認しながら実行。デバッグに便利（時間がかかる）"
    }
  ],
  "required": true,
  "helpText": "最初は『全テスト実行』で全体像をつかみ、失敗したテストは『カテゴリ別実行』で詳細確認するのがお勧めです。"
}
```

### テスト実行とエビデンスキャプチャ

選択した方法に基づいて、以下が実行されます：

1. **テスト実行環境の準備**
   ```bash
   # 仮想環境の確認
   python3 -m venv venv          # Windowsでは python -m venv venv
   source venv/bin/activate      # Windowsでは venv\Scripts\activate

   # 依存パッケージのインストール
   pip install pytest pytest-cov pytest-html pydantic
   ```

2. **テスト実行と結果キャプチャ**
   ```bash
   # 全テスト実行（HTML レポート、カバレッジ報告付き）
   pytest output/pm/unit-test-code/ \
     --html=output/pm/unit-test-evidence/report.html \
     --self-contained-html \
     --cov=app \
     --cov-report=html:output/pm/unit-test-evidence/coverage \
     --cov-report=term \
     -v --tb=short > output/pm/unit-test-evidence/test-output.log 2>&1
   ```

3. **エビデンスファイルの生成**
   ```
   output/pm/unit-test-evidence/
   ├── report.html              # pytest HTML レポート
   ├── coverage/                # カバレッジレポート（HTML）
   │   └── index.html
   ├── test-output.log          # テスト実行ログ
   ├── summary.md               # テスト結果サマリー
   └── failed-tests.txt         # 失敗したテストの詳細
   ```

4. **テスト結果サマリーの自動生成**
   ```
   # サマリー例
   テスト実行結果サマリー
   =======================

   実行テスト数: 42
   成功: 40
   失敗: 2
   スキップ: 0
   実行時間: 12.34 秒

   カバレッジ: 87.5%

   失敗テスト:
   - test_create_task_with_null_user() - ValueError
   - test_update_nonexistent_task() - KeyError
   ```

---

## ✅ Step 4: テスト結果レポート生成

### 生成されるレポート

**output/pm/unit-test-evidence/report.html**
- 全テストケースの実行結果（成功/失敗）
- 各テストの実行時間
- スタックトレース（失敗時）
- カバレッジマップ

**output/pm/unit-test-evidence/summary.md**
```markdown
# 単体テスト実行レポート

## 概要
- 実行日時: 2026-02-10 15:30:45
- テスト対象モジュール: auth.py, tasks.py, validators.py
- テストスタイル: 関数型テスト
- テスト実行方法: 全テスト実行

## テスト結果
| 項目 | 結果 |
|------|------|
| 実行テスト数 | 42 |
| 成功 | 40 (95.2%) |
| 失敗 | 2 (4.8%) |
| スキップ | 0 |
| 実行時間 | 12.34 秒 |

## カバレッジ
| モジュール | カバレッジ |
|-----------|-----------|
| auth.py | 92% |
| tasks.py | 85% |
| validators.py | 88% |
| **全体** | **87.5%** |

## 失敗テストの詳細
### test_create_task_with_null_user()
- **エラー**: ValueError: user_id cannot be null
- **期待値**: タスク作成時にユーザー ID が null の場合、エラーが発生
- **実際**: エラーメッセージがマッチしていない

### test_update_nonexistent_task()
- **エラー**: KeyError: task not found
- **期待値**: 存在しないタスク更新時、適切なエラーメッセージが返される
- **実際**: KeyError が発生している（エラーハンドリング未実装）

## 改善提案
1. エラーメッセージの標準化
2. null チェックの強化
3. 例外ハンドリングの統一
```

### レポート実行コマンド

```bash
# test-planner スキルを実行（対話形式で Step 1-3 の選択肢に回答）
/test-planner --mode execute
```

または手動実行：

```bash
# テスト実行と結果キャプチャ
pytest output/pm/unit-test-code/ \
  --html=output/pm/unit-test-evidence/report.html \
  --self-contained-html \
  --cov=app \
  --cov-report=term \
  -v

# サマリー生成
uv run python tools/test_report_generator.py \
  --input output/pm/unit-test-evidence/report.html \
  --output output/pm/unit-test-evidence/summary.md
```

### ファイル確認

```bash
# 生成されたファイルの確認
ls -la output/pm/unit-test-evidence/
cat output/pm/unit-test-evidence/summary.md
```


---

## 📋 成果物プレビュー

### 期待される出力
```text
📁 output/pm/unit-test-code/
└──   (単体テストコード)
```

### 確認コマンド
```bash
# ファイルの存在とサイズを確認
ls -lh output/pm/unit-test-code/

# 冒頭を確認（最初の30行）
head -30 output/pm/unit-test-code/
```

> 💡 全文を確認: `cat output/pm/unit-test-code/` で全文表示できます

---

## ➡️ Next Step

単体テストの実施が完了しました。次のステップに進む準備ができました：

**[Lesson 18-17: 統合テスト & E2E テスト](./start-18-17.md)**

次のレッスンでは、複数のモジュール間の連携をテストする統合テストと、エンドツーエンドのテストを実施します。
