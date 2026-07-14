---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1", "start-6-2", "start-6-3"]
duration: "約40分"
level: "advanced"
tags: ["agent", "subagent", "orchestration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 6-4: SubAgent統合

## 📍 このセッションでやること

**Lesson 6-4: SubAgent統合** へようこそ！

| 項目 | 内容 |
|------|------|
| ゴール | 複数のSubAgentを組み合わせたアーキテクチャを設計・実装し、効率的なワークフローを構築する |
| 所要時間 | 約40分 |
| 使うスキル | Claude Code SubAgent, タスク分割・オーケストレーション |
| 前提条件 | Lesson 6-1〜Lesson 6-3 完了 |
| 教材ページ | [Module 6: エージェント開発](https://ai-agent.camp/ja/course/module-6) を並行参照 |

**このセッションの流れ:**
1. SubAgentアーキテクチャの設計
2. 専門Agentの定義と連携
3. 統合フローの動作確認

セッション終了時には、複数Agentを組み合わせたワークフローが動くようになっています。

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

## 🚀 Step 1: SubAgentアーキテクチャの設計

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 1: SubAgentアーキテクチャの設計",
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
SubAgentシステムのディレクトリ構造を作成してください：

mkdir -p .claude/subagents/orchestrator
mkdir -p .claude/subagents/content_agent
mkdir -p .claude/subagents/review_agent
mkdir -p .claude/subagents/publish_agent
mkdir -p .claude/subagents/common

各ディレクトリに __init__.py ファイルを作成してください。

構造を確認してください。
```

**期待される結果**: SubAgentシステムのディレクトリ構造が作成されます。

---

## 🚀 Step 2: Orchestrator Agent実装

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 2: Orchestrator Agent実装",
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
.claude/subagents/orchestrator/agent.py ファイルを作成し、以下の内容を記述してください：

import asyncio
from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class OrchestratorAgent:
    """複数のSubAgentを統率する上位Agent"""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.task_queue = asyncio.Queue()

    def submit_task(self, task_id: str, task_data: Dict[str, Any]) -> str:
        """タスクをキューに投入"""
        self.tasks[task_id] = {
            **task_data,
            'status': TaskStatus.PENDING,
            'progress': 0,
            'result': None
        }
        self.task_queue.put_nowait({'id': task_id, **task_data})
        logger.info(f"Task submitted: {task_id}")
        return task_id

    async def process_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """タスクワークフローを処理"""
        task_id = task['id']
        self.tasks[task_id]['status'] = TaskStatus.IN_PROGRESS

        try:
            # Step 1: コンテンツ生成
            logger.info(f"Step 1: Content generation for {task_id}")
            self.tasks[task_id]['progress'] = 33
            content = f"Generated content for: {task.get('prompt', 'default')}"

            # Step 2: レビュー
            logger.info(f"Step 2: Review for {task_id}")
            self.tasks[task_id]['progress'] = 66
            review_passed = True

            # Step 3: 公開
            logger.info(f"Step 3: Publish for {task_id}")
            self.tasks[task_id]['progress'] = 100

            self.tasks[task_id]['status'] = TaskStatus.COMPLETED
            self.tasks[task_id]['result'] = {
                'content': content,
                'review_passed': review_passed,
                'published': True
            }

            return self.tasks[task_id]

        except Exception as e:
            logger.error(f"Workflow failed for {task_id}: {e}")
            self.tasks[task_id]['status'] = TaskStatus.FAILED
            self.tasks[task_id]['error'] = str(e)
            return self.tasks[task_id]

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """タスクのステータスを取得"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """全タスクを取得"""
        return list(self.tasks.values())

# 使用例
async def main():
    orchestrator = OrchestratorAgent()

    # タスク投入
    task_id = orchestrator.submit_task("task_001", {
        "prompt": "AIエージェントについての記事",
        "priority": "high"
    })

    # ワークフロー実行
    task_data = orchestrator.tasks[task_id]
    result = await orchestrator.process_workflow({'id': task_id, **task_data})

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

**期待される結果**: Orchestrator Agentが実装されます。

---

## 🚀 Step 3: Content Agent実装

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 3: Content Agent実装",
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
.claude/subagents/content_agent/agent.py ファイルを作成し、以下の内容を記述してください：

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContentAgent:
    """コンテンツ生成に特化したSubAgent"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = self.config.get('model', 'claude-3-5-sonnet')

    async def generate(
        self,
        prompt: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """プロンプトに基づいてコンテンツを生成"""

        logger.info(f"Generating content for prompt: {prompt[:50]}...")

        # 実際の実装ではClaude APIを呼び出す
        # ここではシミュレーション
        content = f"""
# {prompt}

## 概要
このコンテンツは自動生成されました。

## 詳細
- ポイント1: 重要な情報
- ポイント2: 追加情報
- ポイント3: まとめ

## 結論
以上が {prompt} についての説明です。
"""

        return {
            'content': content.strip(),
            'tokens_used': len(content.split()),
            'model': self.model
        }

    async def summarize(self, text: str, max_length: int = 100) -> str:
        """テキストを要約"""
        logger.info("Summarizing text...")

        # シミュレーション
        words = text.split()[:max_length]
        return ' '.join(words) + "..."

    async def translate(self, text: str, target_lang: str = "en") -> str:
        """テキストを翻訳"""
        logger.info(f"Translating to {target_lang}...")

        # シミュレーション
        return f"[Translated to {target_lang}]: {text[:100]}..."

# テスト用
async def test_content_agent():
    agent = ContentAgent()
    result = await agent.generate("AIエージェントの設計パターン")
    print(result['content'])

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_content_agent())
```

**期待される結果**: Content Agentが実装されます。

---

## 🚀 Step 4: Review Agent実装

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 4: Review Agent実装",
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
.claude/subagents/review_agent/agent.py ファイルを作成し、以下の内容を記述してください：

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ReviewAgent:
    """レビュー・品質チェックを行うSubAgent"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.rules = {
            'min_length': 100,
            'max_length': 5000,
            'forbidden_words': ['テスト', 'TODO'],
            'quality_threshold': 7
        }

    async def review(
        self,
        content: str,
        custom_rules: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """コンテンツをレビュー"""

        rules = {**self.rules, **(custom_rules or {})}
        feedback = []
        score = 10

        # チェック1: 長さ確認
        length = len(content)
        if length < rules['min_length']:
            feedback.append(f"Content too short: {length} chars (min: {rules['min_length']})")
            score -= 2

        if length > rules['max_length']:
            feedback.append(f"Content too long: {length} chars (max: {rules['max_length']})")
            score -= 2

        # チェック2: 禁止ワード確認
        for word in rules.get('forbidden_words', []):
            if word in content:
                feedback.append(f"Forbidden word found: '{word}'")
                score -= 1

        # 判定
        approved = score >= rules.get('quality_threshold', 7)

        logger.info(f"Review completed: score={score}, approved={approved}")

        return {
            'approved': approved,
            'score': max(0, score),
            'feedback': feedback,
            'details': {
                'length': length,
                'forbidden_words_found': sum(1 for w in rules.get('forbidden_words', []) if w in content)
            }
        }

# テスト用
async def test_review_agent():
    agent = ReviewAgent()

    # 短いコンテンツ
    result1 = await agent.review("Short")
    print(f"Short content: {result1}")

    # 正常なコンテンツ
    normal_content = "これは正常なコンテンツです。" * 20
    result2 = await agent.review(normal_content)
    print(f"Normal content: {result2}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_review_agent())
```

**期待される結果**: Review Agentが実装されます。

---

## 🚀 Step 5: 統合テスト

AskUserQuestion（AskQuestion）で「このまま進める / 例だけ確認 / スキップ」を選べます。

**AskQuestionの設定例:**
```json
{
  "title": "🚀 Step 5: 統合テスト",
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
SubAgentシステムの統合テストを作成・実行してください。

.claude/subagents/tests/test_integration.py ファイルを作成：

import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.agent import OrchestratorAgent, TaskStatus
from content_agent.agent import ContentAgent
from review_agent.agent import ReviewAgent

@pytest.mark.asyncio
async def test_orchestrator_submit_task():
    """Orchestratorタスク投入テスト"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_001", {"prompt": "test"})

    assert task_id == "test_001"
    assert orchestrator.tasks[task_id]['status'] == TaskStatus.PENDING

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    """Orchestratorワークフローテスト"""
    orchestrator = OrchestratorAgent()
    task_id = orchestrator.submit_task("test_002", {"prompt": "AI記事"})

    result = await orchestrator.process_workflow({'id': task_id, 'prompt': 'AI記事'})

    assert result['status'] == TaskStatus.COMPLETED
    assert result['progress'] == 100

@pytest.mark.asyncio
async def test_content_agent_generate():
    """ContentAgent生成テスト"""
    agent = ContentAgent()
    result = await agent.generate("テストプロンプト")

    assert 'content' in result
    assert len(result['content']) > 0

@pytest.mark.asyncio
async def test_review_agent_approve():
    """ReviewAgent承認テスト"""
    agent = ReviewAgent()
    long_content = "正常なコンテンツです。" * 50

    result = await agent.review(long_content)

    assert result['approved'] == True
    assert result['score'] >= 7

@pytest.mark.asyncio
async def test_review_agent_reject():
    """ReviewAgent拒否テスト"""
    agent = ReviewAgent()
    short_content = "短い"

    result = await agent.review(short_content)

    assert result['approved'] == False

テストを実行してください：
cd .claude/subagents && pytest tests/test_integration.py -v
```

**期待される結果**: 統合テストが全てパスします。

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
      {"id": "trouble_1", "label": "asyncioエラー"},
      {"id": "trouble_2", "label": "モジュールインポートエラー"},
      {"id": "trouble_3", "label": "非同期処理がハングする"},
      {"id": "trouble_4", "label": "タスクが完了しない"}
    ]
  }]
}
```


### トラブル1: asyncioエラー
**原因**: イベントループが正しく設定されていない
**解決プロンプト**:
```
pytest-asyncio をインストールしてください：
uv add pytest-asyncio

pytest.iniまたはpyproject.tomlで設定：
[pytest]
asyncio_mode = auto
```

### トラブル2: モジュールインポートエラー
**原因**: __init__.py がない、またはパスが通っていない
**解決プロンプト**:
```
各ディレクトリに __init__.py を作成してください。
sys.path にプロジェクトルートを追加してください。
```

### トラブル3: 非同期処理がハングする
**原因**: await が不足している、またはデッドロック
**解決プロンプト**:
```
全ての非同期関数呼び出しに await をつけてください。
asyncio.wait_for() でタイムアウトを設定してください。
```

### トラブル4: タスクが完了しない
**原因**: ワークフロー内で例外が発生している
**解決プロンプト**:
```
try-except でエラーをキャッチし、ログ出力してください。
TaskStatus.FAILED を適切に設定してください。
```

---

## ✅ チェックポイント
- [ ] SubAgentディレクトリ構造が作成されている
- [ ] Orchestrator Agentが実装されている
- [ ] Content Agentが実装されている
- [ ] Review Agentが実装されている
- [ ] 統合テストがパスする


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
      {"id": "next_window", "label": "新しいウィンドウで開始（/start-6-5）"},
      {"id": "finish", "label": "ここで終了する"}
    ]
  }]
}
```

**選択後の案内（例）**:
- next_auto → /next_lesson
- next_window → 新しいウィンドウで /start-6-5
- finish → 終了
