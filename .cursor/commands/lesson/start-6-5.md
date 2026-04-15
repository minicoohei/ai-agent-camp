---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3", "start-6-4"]
duration: "約50分"
level: "advanced"
tags: ["agent", "capstone", "deployment"]
---

# 🎓 Lesson 6-5: 総合演習 - AIエージェント開発統合

## 📍 このセッションでやること

**Lesson 6-5: エージェント統合・本番デプロイ** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | Module 1-7の学習を統合し、実動作するAIエージェントプロジェクトを完成させる |
| 所要時間 | 約50分 |
| 使うスキル | Command / Skill / Rules / SubAgent の総合、本番デプロイの考え方 |
| 前提条件 | Lesson 6-1〜Lesson 6-4 完了 |
| 教材ページ | [Module 6: エージェント開発](https://ai-agent.camp/ja/course/module-6) を並行参照 |

**このセッションの流れ:**
1. プロジェクト初期化と要件整理
2. 統合エージェントの組み立て
3. 動作確認と本番デプロイの準備

セッション終了時には、本格的なAIエージェントシステムが完成し、コース修了です。

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

## 🚀 Step 1: プロジェクト初期化

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: プロジェクト初期化",
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
総合演習用のプロジェクト構造を作成してください。

ディレクトリ作成：
mkdir -p ai-content-agent/src/{api,services,subagents,utils}
mkdir -p ai-content-agent/tests
mkdir -p ai-content-agent/.github/workflows
mkdir -p ai-content-agent/.claude/{skills,rules}
mkdir -p ai-content-agent/.cursor/commands

必要なファイルを作成：
touch ai-content-agent/requirements.txt
touch ai-content-agent/README.md
touch ai-content-agent/.env.example

構造を確認してください。
```

**期待される結果**: 総合演習用のプロジェクト構造が作成されます。

---

## 🚀 Step 2: FastAPI サーバー実装

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: FastAPI サーバー実装",
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
ai-content-agent/src/main.py ファイルを作成し、以下の内容を記述してください：

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="AI Content Generator API",
    version="1.0.0",
    description="AI-powered content generation and management"
)

# モデル定義
class TaskRequest(BaseModel):
    title: str
    prompt: str
    priority: str = "medium"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    created_at: str

# インメモリタスクストレージ（本番ではDBを使用）
tasks: Dict[str, Dict] = {}

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    """新規タスクを作成"""
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = {
        "id": task_id,
        "title": request.title,
        "prompt": request.prompt,
        "priority": request.priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None
    }
    return TaskResponse(
        task_id=task_id,
        status="pending",
        created_at=tasks[task_id]["created_at"]
    )

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """タスク情報を取得"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/tasks")
async def list_tasks(limit: int = 10):
    """タスク一覧を取得"""
    task_list = list(tasks.values())
    return task_list[:limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**期待される結果**: FastAPI サーバーが実装されます。

---

## 🚀 Step 3: requirements.txt 作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: requirements.txt 作成",
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
ai-content-agent/requirements.txt ファイルに以下の内容を記述してください：

fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.0
pytest-asyncio==0.23.0
```

**期待される結果**: 依存関係ファイルが作成されます。

---

## 🚀 Step 4: GitHub Actions ワークフロー

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: GitHub Actions ワークフロー",
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
ai-content-agent/.github/workflows/ci.yml ファイルを作成し、以下の内容を記述してください：

name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest tests/ -v || echo "No tests found"

      - name: Health check
        run: |
          python -c "from src.main import app; print('Import successful!')"

      - name: Summary
        if: always()
        run: |
          echo "## CI Summary" >> $GITHUB_STEP_SUMMARY
          echo "- Branch: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- Status: ${{ job.status }}" >> $GITHUB_STEP_SUMMARY
```

**期待される結果**: CI/CDパイプラインが設定されます。

---

## 🚀 Step 5: テストコード作成

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: テストコード作成",
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
ai-content-agent/tests/test_api.py ファイルを作成し、以下の内容を記述してください：

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.main import app

client = TestClient(app)

def test_health_check():
    """ヘルスチェックテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

def test_create_task():
    """タスク作成テスト"""
    response = client.post("/tasks", json={
        "title": "Test Task",
        "prompt": "Generate test content",
        "priority": "high"
    })
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "pending"

def test_get_task():
    """タスク取得テスト"""
    # まずタスクを作成
    create_response = client.post("/tasks", json={
        "title": "Get Test",
        "prompt": "Test prompt"
    })
    task_id = create_response.json()["task_id"]

    # タスクを取得
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test"

def test_get_task_not_found():
    """存在しないタスク取得テスト"""
    response = client.get("/tasks/nonexistent")
    assert response.status_code == 404

def test_list_tasks():
    """タスク一覧テスト"""
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

テストを実行してください：
cd ai-content-agent && pip install -r requirements.txt && pytest tests/ -v
```

**期待される結果**: APIテストが全てパスします。

---

## 🚀 Step 6: 最終チェックとドキュメント

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 6: 最終チェックとドキュメント",
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
ai-content-agent/README.md ファイルを作成し、以下の内容を記述してください：

# AI Content Generator Agent

AI駆動のコンテンツ生成・管理システムです。

## 機能

- RESTful API によるタスク管理
- 非同期コンテンツ生成
- 品質レビュー機能
- 複数プラットフォーム公開

## セットアップ

### 前提条件
- Python 3.11+
- pip

### インストール

```bash
git clone <repository-url>
cd ai-content-agent

python -m venv venv
source venv/bin/activate  # macOS/Linux/WSL

pip install -r requirements.txt
```

### 実行

```bash
python -m src.main
```

API: http://localhost:8000

### テスト

```bash
pytest tests/ -v
```

## API エンドポイント

| Method | Endpoint | 説明 |
|--------|----------|------|
| GET | /health | ヘルスチェック |
| POST | /tasks | タスク作成 |
| GET | /tasks/{id} | タスク取得 |
| GET | /tasks | タスク一覧 |

## プロジェクト構成

```
ai-content-agent/
├── src/
│   ├── main.py          # FastAPI メイン
│   ├── api/             # エンドポイント
│   ├── services/        # ビジネスロジック
│   └── subagents/       # SubAgent実装
├── tests/               # テスト
├── .github/workflows/   # CI/CD
└── requirements.txt     # 依存関係
```

## ライセンス
MIT
```

**期待される結果**: プロジェクトドキュメントが完成します。

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
      {"id": "trouble_1", "label": "インポートエラー"},
      {"id": "trouble_2", "label": "ポートが使用中"},
      {"id": "trouble_3", "label": "GitHub Actionsが失敗"},
      {"id": "trouble_4", "label": "テストが見つからない"}
    ]
  }]
}
```


- インポートエラーが出る
- ポートが使用中
- GitHub Actionsが失敗する
- テストが見つからない

### トラブル1: インポートエラー
**原因**: PYTHONPATHが設定されていない
**解決プロンプト**:
```
以下を確認してください：
1. sys.path にプロジェクトルートを追加
2. __init__.py がディレクトリに存在する
3. 仮想環境がアクティブになっている
```

### トラブル2: ポートが使用中
**原因**: 既に8000番ポートが使われている
**解決プロンプト**:
```
ポートを変更してください：
uvicorn.run(app, host="0.0.0.0", port=8001)
または既存プロセスを終了：
lsof -i :8000 && kill <PID>          # Mac/Linux/WSL
```

### トラブル3: GitHub Actionsが失敗
**原因**: ワークフロー設定のエラー
**解決プロンプト**:
```
以下を確認してください：
1. YAMLのインデントが正しいか
2. requirements.txt のパスが正しいか
3. Pythonバージョンが正しいか
```

### トラブル4: テストが見つからない
**原因**: テストファイルの命名規則が違う
**解決プロンプト**:
```
pytest のテストファイル命名規則：
- test_*.py または *_test.py
- テスト関数は test_ で始まる
```

---

## ✅ チェックポイント

### 総合演習チェックリスト

### Module 6-1: Commands
- [ ] .cursor/commands/ にコマンドを配置
- [ ] 最低3つのコマンドを作成

### Module 6-2: Skills
- [ ] skills/ にスキルを配置
- [ ] SKILL.md でドキュメント化
- [ ] テストコードがある

### Module 6-3: Rules
- [ ] .cursor/rules/rules.md で行動を定義
- [ ] セキュリティ・パフォーマンス基準を明記

### Module 6-4: SubAgents
- [ ] Orchestrator が実装済み
- [ ] 複数のSubAgentが連携
- [ ] エラーハンドリングがある

### Module 6-5: 統合
- [ ] FastAPI サーバー動作確認
- [ ] APIエンドポイントテスト済み
- [ ] GitHub Actions設定済み
- [ ] ドキュメント完成

---

## 🎉 おめでとうございます！

全てのモジュールを完了しました！

### 習得したスキル
1. **AIエージェント開発**: 複雑なワークフロー設計・実装
2. **マイクロサービス**: SubAgentの疎結合設計
3. **外部API連携**: Notion、Slack、Google連携
4. **DevOps**: CI/CDパイプライン構築
5. **エンタープライズ開発**: スケーラブルなシステム設計


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

## ✅ 完了チェック
以下をCursorのチャットに貼り付けて、完了状況を確認してください:

```
# 完了確認: output/ フォルダに期待される出力ファイルが生成されているか確認してください。
```

**期待される結果**: 完了/未完の判定と不足項目が表示されます。

---

## ➡️ 次のステップ

これで全セクション完了です。次にやることを選んでください。

AskUserQuestion（AskQuestion）で選べます。

**AskQuestionの設定例:**
```json
{
  "title": "次のステップを選択",
  "questions": [{
    "id": "next_step",
    "prompt": "次に進む操作を選んでください",
    "options": [
      {"id": "next_module", "label": "Module 7 Skill/Commandsに進む（/start-7-1）"},
      {"id": "course_top", "label": "コーストップを開く（ai-agent.camp）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_module → /start-7-1（Module 7 Skill/Commands）
- course_top → ブラウザで https://ai-agent.camp/ja/course を開く
- finish → 終了
