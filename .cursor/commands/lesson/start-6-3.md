---
description: "When the user says /start-6-3 — Module 6 Lesson 6-3: Rules設定（Cursor Rules）とAI行動制御"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "約25分"
level: "intermediate"
tags: ["agent", "rules", "cursor"]
---

# 🎓 Lesson 6-3: Cursor Rules設定

## 📍 このセッションでやること

**Lesson 6-3: Cursor Rules** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Cursor Rules（.cursor/rules/）でAIの行動・コンテキスト・制約を制御する |
| 所要時間 | 約25分 |
| 使うスキル | Cursor Rules, .mdc ファイル |
| 前提条件 | Lesson 6-1 完了、Cursor 利用中 |
| 教材ページ | [Module 6: エージェント開発](https://ai-agent.camp/ja/course/module-6) を並行参照 |

**このセッションの流れ:**
1. Rulesディレクトリの作成
2. プロジェクト用ルールの定義（コーディング規約・セキュリティ）
3. 動作確認

セッション終了時には、AIがプロジェクトのルールに沿って応答するようになっています。

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

## 🚀 Step 1: Rulesディレクトリの作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: Rulesディレクトリの作成",
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
.cursor/rules/ ディレクトリを作成し、Cursor Rules用の構造を準備してください。

mkdir -p .cursor/rules

ディレクトリが作成されたことを確認してください。
```

**期待される結果**: `.cursor/rules/` ディレクトリが作成されます。

---

## 🚀 Step 2: 基本Rules作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: 基本Rules作成",
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
.cursor/rules/rules.md ファイルを作成し、以下の内容を記述してください：

# Cursor Rules - AIエージェント開発プロジェクト

## プロジェクト概要
AIエージェント開発のベースプラットフォーム
- Python 3.11+
- FastAPI で REST API
- Claude AI API 連携
- GitHub Actions CI/CD

---

## コーディング規約

### Python スタイル
- **PEP 8 準拠**: 全コード
- **Line length**: 100文字以内
- **Indentation**: 4スペース
- **Naming**:
  - 関数・変数: snake_case
  - クラス: PascalCase
  - 定数: UPPER_CASE

### コードサンプル
```python
# 良い例
def calculate_user_score(user_id: int) -> float:
    """ユーザースコアを計算する"""
    user = get_user(user_id)
    return user.points * user.multiplier

# 避ける例
def calc(u):
    return get_user(u).pts * get_user(u).m
```

---

## セキュリティ規約

### 必須チェック項目
- 入力値検証：全エンドポイント
- SQLインジェクション対策：ORM 使用
- 認証：JWT トークン使用
- ロギング：機密情報を含めない
- 環境変数：.env で管理

### 禁止事項
- ハードコードされたパスワード
- ログ出力する機密情報
- 直接的なSQL文実行

---

## AI (Claude) の行動指針

### すべきこと
- 簡潔性: 最小限のコードで機能実装
- 可読性: 他者が理解しやすい実装
- エラーハンドリング: 予想可能なエラーに対応
- テストコード: 実装と同時に提供

### 避けるべき
- 長い関数：1関数30行以下
- グローバル変数：可能な限り避ける
- マジックナンバー：定数で定義
```

**期待される結果**: 基本的なRulesファイルが作成されます。

---

## 🚀 Step 3: セキュリティRules作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: セキュリティRules作成",
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
.cursor/rules/security.md ファイルを作成し、以下の内容を記述してください：

# セキュリティ重視 Rules

## 認証・認可

### JWT トークン
全 API エンドポイントで JWT 検証必須

```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/data")
async def get_data(token = Depends(security)):
    user = verify_token(token.credentials)
    return fetch_user_data(user.id)
```

### 入力値検証
Pydantic モデル使用で自動検証

```python
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    age: int  # 型チェック自動実施
```

## ロギングセキュリティ

```python
# 避ける
logger.info(f"User {user.password} logged in")

# 推奨
logger.info(f"User {user.id} logged in")
```

## 環境変数管理

```python
# .env ファイルで管理
DATABASE_URL=postgresql://...
API_KEY=secret_xxx

# コードで読み込み
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")
```
```

**期待される結果**: セキュリティ専用のRulesファイルが作成されます。

---

## 🚀 Step 4: テストRules作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: テストRules作成",
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
.cursor/rules/testing.md ファイルを作成し、以下の内容を記述してください：

# テスト規約

## テストカバレッジ目標
- 全体: 80% 以上
- ビジネスロジック: 90% 以上
- API エンドポイント: 85% 以上

## テストの種類

### ユニットテスト
関数の入力・出力を検証

```python
def test_calculate_score():
    result = calculate_score(points=100)
    assert result > 0
    assert result <= 100
```

### 統合テスト
複数モジュールを組み合わせたテスト

```python
def test_user_registration_flow():
    user = create_user(email="test@example.com")
    assert user.id > 0
    assert db.query(User).filter(User.id == user.id).first()
```

## テスト実行コマンド

```bash
# 全テスト
pytest tests/ -v

# カバレッジ付き
pytest tests/ --cov=src/ --cov-report=term-missing

# 特定のマーカー
pytest tests/ -m "unit"
```

## テスト命名規則
- ファイル名: test_<モジュール名>.py
- 関数名: test_<機能>_<条件>_<期待結果>

例: test_login_with_invalid_password_returns_401
```

**期待される結果**: テスト専用のRulesファイルが作成されます。

---

## 🚀 Step 5: Rulesの適用確認

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: Rulesの適用確認",
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
作成したRulesファイルの一覧と内容を確認してください：

1. .cursor/rules/ ディレクトリ内のファイルを一覧表示
2. 各Rulesファイルの主要なポイントを要約
3. Rulesがプロジェクト全体に適用されるか確認

確認後、簡単なPython関数を書いて、Rulesに従っているか検証してください。
例：ユーザー情報を取得するAPIエンドポイント
```

**期待される結果**: RulesファイルがCursorに認識され、コード生成時に参照されます。

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
      {"id": "trouble_1", "label": "Rulesが反映されない"},
      {"id": "trouble_2", "label": "Rulesが長すぎて読み込めない"},
      {"id": "trouble_3", "label": "AIがRulesを無視する"},
      {"id": "trouble_4", "label": "Rulesが競合する"}
    ]
  }]
}
```


### トラブル1: Rulesが反映されない
**原因**: ファイルパスが間違っている、またはCursorが再読み込みしていない
**解決プロンプト**:
```
以下を確認してください：
1. ファイルが .cursor/rules/ にあるか
2. Cursorを再起動してRulesを再読み込み
3. ファイル拡張子が .md か確認
```

### トラブル2: Rulesが長すぎて読み込めない
**原因**: ファイルサイズが大きすぎる
**解決プロンプト**:
```
Rulesファイルを分割してください：
- rules.md（基本ルール）
- security.md（セキュリティ）
- testing.md（テスト）
各ファイルは適度なサイズに保ってください。
```

### トラブル3: AIがRulesを無視する
**原因**: Rulesの記述が曖昧、または優先度が低い
**解決プロンプト**:
```
Rulesをより明確に記述してください：
- 「推奨」より「必須」
- 具体的なコード例を含める
- 禁止事項を明確に記載
```

### トラブル4: Rulesが競合する
**原因**: 複数のRulesファイルで矛盾した指示がある
**解決プロンプト**:
```
Rulesファイル間で矛盾がないか確認してください。
基本ルール（rules.md）を優先し、専門ルールは補完的に使用してください。
```

---

## ✅ チェックポイント
- [ ] .cursor/rules/ ディレクトリが存在する
- [ ] rules.md が作成されている
- [ ] security.md が作成されている
- [ ] testing.md が作成されている
- [ ] Rulesに従ったコードが生成される


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
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-6-4）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-6-4
- finish → 終了
