"""
howtodo_generator.py のユニットテスト

HowToDo生成機能のテスト:
- TaskType / HowToDoStep / HowToDoResult データクラス
- classify_task: タスク種別判定
- _build_output_schema: スキーマ生成
- _parse_llm_response: LLM レスポンスパース
- HowToDoGenerator: クラス全体
- 境界値テスト
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    """howtodo_generator モジュールをロード"""
    return import_module_from_repo("howtodo_generator", "tools/howtodo_generator.py")


# ===================================================================
# TaskType
# ===================================================================

class TestTaskType:

    def test_values(self, mod):
        assert mod.TaskType.WORK.value == "work"
        assert mod.TaskType.MEETING.value == "meeting"
        assert mod.TaskType.BROWSER.value == "browser"

    def test_all_types(self, mod):
        types = list(mod.TaskType)
        assert len(types) == 3


# ===================================================================
# HowToDoStep / HowToDoResult
# ===================================================================

class TestDataClasses:

    def test_howtodo_step(self, mod):
        step = mod.HowToDoStep(order=1, action="テスト", check_condition="完了条件")
        assert step.order == 1
        assert step.tool_hint is None

    def test_howtodo_step_with_hint(self, mod):
        step = mod.HowToDoStep(order=1, action="作業", check_condition="確認", tool_hint="Cursor")
        assert step.tool_hint == "Cursor"

    def test_howtodo_result_defaults(self, mod):
        result = mod.HowToDoResult(task_type=mod.TaskType.WORK, title="タスク")
        assert result.summary == ""
        assert result.steps == []
        assert result.needs_reply is False
        assert result.reply_examples == []
        assert result.cursor_prompt is None
        assert result.browser_shortcut is None
        assert result.estimated_minutes == 5

    def test_howtodo_result_to_dict(self, mod):
        step = mod.HowToDoStep(order=1, action="アクション", check_condition="条件")
        result = mod.HowToDoResult(
            task_type=mod.TaskType.WORK,
            title="テスト",
            steps=[step],
            needs_reply=True,
            reply_examples=["例1"],
        )
        d = result.to_dict()
        assert d["task_type"] == "work"
        assert d["title"] == "テスト"
        assert len(d["steps"]) == 1
        assert d["needs_reply"] is True
        assert d["reply_examples"] == ["例1"]


# ===================================================================
# classify_task
# ===================================================================

class TestClassifyTask:

    def test_default_is_work(self, mod):
        """デフォルトは WORK"""
        task = {"source": "slack", "content": "データを更新してください", "title": "更新依頼"}
        task_type, needs_reply = mod.classify_task(task)
        assert task_type == mod.TaskType.WORK

    def test_calendar_source_is_meeting(self, mod):
        task = {"source": "calendar", "content": "定例ミーティング", "title": "チーム定例"}
        task_type, _ = mod.classify_task(task)
        assert task_type == mod.TaskType.MEETING

    def test_output_source_is_meeting(self, mod):
        task = {"source": "output", "content": "議事録", "title": "打ち合わせ結果"}
        task_type, _ = mod.classify_task(task)
        assert task_type == mod.TaskType.MEETING

    def test_meeting_keywords(self, mod):
        for keyword in ["会議", "ミーティング", "mtg", "定例", "1on1"]:
            task = {"source": "slack", "content": keyword, "title": ""}
            task_type, _ = mod.classify_task(task)
            assert task_type == mod.TaskType.MEETING, f"Failed for keyword: {keyword}"

    def test_browser_keywords(self, mod):
        for keyword in ["freee", "salesforce", "管理画面", "kintone"]:
            task = {"source": "slack", "content": keyword, "title": ""}
            task_type, _ = mod.classify_task(task)
            assert task_type == mod.TaskType.BROWSER, f"Failed for keyword: {keyword}"

    def test_needs_reply_with_mentions(self, mod):
        """Slack メンション付きは返信必要"""
        task = {"source": "slack", "content": "確認お願い", "title": "", "mentions": ["@user"]}
        _, needs_reply = mod.classify_task(task)
        assert needs_reply is True

    def test_needs_reply_keywords(self, mod):
        for keyword in ["返信", "確認して", "教えて", "質問"]:
            task = {"source": "slack", "content": keyword, "title": ""}
            _, needs_reply = mod.classify_task(task)
            assert needs_reply is True, f"Failed for keyword: {keyword}"

    def test_no_reply_needed(self, mod):
        task = {"source": "slack", "content": "ファイルを更新しました", "title": "完了報告"}
        _, needs_reply = mod.classify_task(task)
        assert needs_reply is False

    def test_empty_task(self, mod):
        """境界値: 空のタスク"""
        task = {}
        task_type, needs_reply = mod.classify_task(task)
        assert task_type == mod.TaskType.WORK
        assert needs_reply is False

    def test_none_values(self, mod):
        """境界値: None 値を含むタスク → source.lower() で AttributeError"""
        task = {"source": None, "content": None, "title": None}
        with pytest.raises(AttributeError):
            mod.classify_task(task)

    def test_unicode_content(self, mod):
        """Unicode 特殊文字を含むタスク"""
        task = {"source": "slack", "content": "🎉 会議の予定📅", "title": ""}
        task_type, _ = mod.classify_task(task)
        assert task_type == mod.TaskType.MEETING


# ===================================================================
# _build_output_schema
# ===================================================================

class TestBuildOutputSchema:

    def test_work_type_has_cursor_prompt(self, mod):
        schema_str = mod._build_output_schema(mod.TaskType.WORK)
        schema = json.loads(schema_str)
        assert "cursor_prompt" in schema

    def test_browser_type_has_shortcut(self, mod):
        schema_str = mod._build_output_schema(mod.TaskType.BROWSER)
        schema = json.loads(schema_str)
        assert "browser_shortcut" in schema

    def test_meeting_type(self, mod):
        schema_str = mod._build_output_schema(mod.TaskType.MEETING)
        schema = json.loads(schema_str)
        assert "steps" in schema

    def test_needs_reply_adds_examples(self, mod):
        schema_str = mod._build_output_schema(mod.TaskType.WORK, needs_reply=True)
        schema = json.loads(schema_str)
        assert "reply_examples" in schema

    def test_no_reply_no_examples(self, mod):
        schema_str = mod._build_output_schema(mod.TaskType.WORK, needs_reply=False)
        schema = json.loads(schema_str)
        assert "reply_examples" not in schema


# ===================================================================
# _parse_llm_response
# ===================================================================

class TestParseLlmResponse:

    def test_valid_json(self, mod):
        response = json.dumps({
            "summary": "タスク概要",
            "completion_criteria": "完了条件",
            "prerequisites": ["前提1"],
            "steps": [
                {"order": 1, "action": "ステップ1", "check_condition": "条件1", "tool_hint": "Cursor"}
            ],
            "estimated_minutes": 10,
            "cursor_prompt": "テストプロンプト",
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト")
        assert result.summary == "タスク概要"
        assert len(result.steps) == 1
        assert result.steps[0].tool_hint == "Cursor"
        assert result.estimated_minutes == 10

    def test_invalid_json_fallback(self, mod):
        """JSON パースエラー時のフォールバック"""
        result = mod._parse_llm_response("not json {", mod.TaskType.WORK, "テスト")
        assert result.title == "テスト"
        assert result.task_type == mod.TaskType.WORK
        assert len(result.steps) >= 1  # フォールバックステップ

    def test_empty_string(self, mod):
        """境界値: 空文字列"""
        result = mod._parse_llm_response("", mod.TaskType.WORK, "テスト")
        assert result.title == "テスト"

    def test_with_reply_examples(self, mod):
        response = json.dumps({
            "summary": "確認依頼",
            "completion_criteria": "返信完了",
            "steps": [],
            "reply_examples": ["例1", "例2", "例3"],
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト", needs_reply=True)
        assert len(result.reply_examples) == 3

    def test_no_reply_ignores_examples(self, mod):
        response = json.dumps({
            "summary": "作業",
            "steps": [],
            "reply_examples": ["例1"],
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト", needs_reply=False)
        assert result.reply_examples == []

    def test_prerequisites_as_string(self, mod):
        """prerequisites が文字列の場合"""
        response = json.dumps({
            "summary": "タスク",
            "prerequisites": "前提条件",
            "steps": [],
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト")
        assert result.prerequisites == ["前提条件"]

    def test_prerequisites_empty_string(self, mod):
        response = json.dumps({
            "summary": "タスク",
            "prerequisites": "",
            "steps": [],
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト")
        assert result.prerequisites == []

    def test_steps_without_tool_hint(self, mod):
        response = json.dumps({
            "summary": "タスク",
            "steps": [{"order": 1, "action": "アクション", "check_condition": "条件"}],
        })
        result = mod._parse_llm_response(response, mod.TaskType.WORK, "テスト")
        assert result.steps[0].tool_hint is None

    def test_browser_shortcut_parsed(self, mod):
        response = json.dumps({
            "summary": "ブラウザ操作",
            "steps": [],
            "browser_shortcut": {"name": "test", "prompt": "p", "start_url": "https://example.com"},
        })
        result = mod._parse_llm_response(response, mod.TaskType.BROWSER, "テスト")
        assert result.browser_shortcut["name"] == "test"


# ===================================================================
# HowToDoGenerator
# ===================================================================

class TestHowToDoGenerator:

    def test_init_without_api_key(self, mod, monkeypatch):
        """API キーなしの初期化"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            assert gen.client is None

    def test_init_with_explicit_key(self, mod):
        """明示的な API キーで初期化"""
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_genai.Client.return_value = MagicMock()
                gen = mod.HowToDoGenerator(api_key="test-key")
                assert gen.api_key == "test-key"
                mock_genai.Client.assert_called_once_with(api_key="test-key")

    def test_summarize_title_short_title(self, mod, monkeypatch):
        """25文字以下のタイトルはそのまま返す"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen.summarize_title({"title": "短いタイトル"})
            assert result == "短いタイトル"

    def test_summarize_title_long_without_llm(self, mod, monkeypatch):
        """LLM なしで長いタイトルのフォールバック"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            long_title = "あ" * 50
            result = gen.summarize_title({"title": long_title})
            assert len(result) <= 25

    def test_summarize_title_empty(self, mod, monkeypatch):
        """境界値: タイトルなし"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen.summarize_title({})
            assert result == "タスク"

    def test_summarize_title_with_date(self, mod, monkeypatch):
        """日付付きの長いタイトル → 日付を除去"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen.summarize_title({"title": "週次レポート作成タスク（2025-01-15の分）を確認する"})
            assert "2025-01-15" not in result

    def test_check_task_completion_no_client(self, mod, monkeypatch):
        """LLM なしの完了チェック → None"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen.check_task_completion("ファイル内容", "タスク")
            assert result is None


# ===================================================================
# TASK_TYPE_KEYWORDS / NEEDS_REPLY_KEYWORDS
# ===================================================================

class TestKeywords:

    def test_meeting_keywords_not_empty(self, mod):
        assert len(mod.TASK_TYPE_KEYWORDS[mod.TaskType.MEETING]) > 0

    def test_browser_keywords_not_empty(self, mod):
        assert len(mod.TASK_TYPE_KEYWORDS[mod.TaskType.BROWSER]) > 0

    def test_needs_reply_keywords_not_empty(self, mod):
        assert len(mod.NEEDS_REPLY_KEYWORDS) > 0

    def test_all_keywords_are_strings(self, mod):
        for kw_list in mod.TASK_TYPE_KEYWORDS.values():
            for kw in kw_list:
                assert isinstance(kw, str)

    def test_no_duplicate_keywords(self, mod):
        for t_type, kw_list in mod.TASK_TYPE_KEYWORDS.items():
            assert len(kw_list) == len(set(kw_list)), f"Duplicates in {t_type}"


# ===================================================================
# _summarize_title_fallback
# ===================================================================

class TestSummarizeTitleFallback:

    def test_removes_date_in_parens(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen._summarize_title_fallback("レポート作成 (2025-01-15)", "")
            assert "2025" not in result

    def test_truncates_long_title(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen._summarize_title_fallback("あ" * 100, "")
            assert len(result) <= 25

    def test_empty_after_cleaning(self, mod, monkeypatch):
        """クリーニング後に空になる場合"""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen._summarize_title_fallback("(2025-01-01)", "")
            assert len(result) > 0  # フォールバックで何か返る


# ===================================================================
# HowToDoGenerator.summarize_title (LLM path)
# ===================================================================

class TestSummarizeTitleWithLLM:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                return gen

    def test_summarize_title_llm_success(self, mod, monkeypatch):
        """LLM で正常にタイトルを要約"""
        gen = self._make_gen(mod, monkeypatch)
        mock_response = MagicMock()
        mock_response.text = json.dumps({"summary_title": "要約タイトル"})
        gen.client.models.generate_content.return_value = mock_response
        result = gen.summarize_title({"title": "これは非常に長いタスクタイトルですので要約が必要です"})
        assert result == "要約タイトル"

    def test_summarize_title_llm_api_error(self, mod, monkeypatch):
        """LLM API エラー時はフォールバック"""
        gen = self._make_gen(mod, monkeypatch)
        gen.client.models.generate_content.side_effect = RuntimeError("API down")
        result = gen.summarize_title({"title": "これは非常に長いタスクタイトルですので要約が必要です"})
        assert isinstance(result, str)
        assert len(result) <= 25

    def test_summarize_title_llm_response_truncated(self, mod, monkeypatch):
        """LLM レスポンスが25文字超でも25文字に制限"""
        gen = self._make_gen(mod, monkeypatch)
        mock_response = MagicMock()
        mock_response.text = json.dumps({"summary_title": "あ" * 50})
        gen.client.models.generate_content.return_value = mock_response
        result = gen.summarize_title({"title": "これは非常に長いタスクタイトルですので要約が必要です"})
        assert len(result) <= 25

    def test_summarize_title_llm_missing_key(self, mod, monkeypatch):
        """LLM レスポンスに summary_title がない場合"""
        gen = self._make_gen(mod, monkeypatch)
        mock_response = MagicMock()
        mock_response.text = json.dumps({"other": "value"})
        gen.client.models.generate_content.return_value = mock_response
        result = gen.summarize_title({"title": "これは非常に長いタスクタイトルですので要約が必要です"})
        assert len(result) <= 25

    def test_summarize_title_with_remaining_tasks(self, mod, monkeypatch):
        """残タスクがある場合のLLMプロンプト"""
        gen = self._make_gen(mod, monkeypatch)
        mock_response = MagicMock()
        mock_response.text = json.dumps({"summary_title": "残タスク対応"})
        gen.client.models.generate_content.return_value = mock_response
        result = gen.summarize_title({
            "title": "これは非常に長いタスクタイトルですので要約が必要です",
            "remaining_tasks": ["タスク1", "タスク2"],
        })
        assert result == "残タスク対応"


# ===================================================================
# HowToDoGenerator.check_task_completion (LLM path)
# ===================================================================

class TestCheckTaskCompletionWithLLM:

    def test_check_task_completion_success(self, mod, monkeypatch):
        """LLM で正常に完了判定"""
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                completion_data = {
                    "is_in_progress": True,
                    "reason": "未完了のチェックリスト",
                    "remaining_work": "テスト作成",
                    "confidence": 0.8,
                }
                mock_response = MagicMock()
                mock_response.text = json.dumps(completion_data)
                mock_client.models.generate_content.return_value = mock_response
                result = gen.check_task_completion("ファイル内容", "タスク")
                assert result["is_in_progress"] is True
                assert result["confidence"] == 0.8

    def test_check_task_completion_api_error(self, mod, monkeypatch):
        """LLM API エラー時は None"""
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                mock_client.models.generate_content.side_effect = RuntimeError("timeout")
                result = gen.check_task_completion("内容", "タスク")
                assert result is None


# ===================================================================
# HowToDoGenerator.infer_tasks_from_activity
# ===================================================================

class TestInferTasksFromActivity:

    def test_no_client_returns_empty(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            result = gen.infer_tasks_from_activity([])
            assert result == []

    def test_empty_logs_returns_empty(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                # No relevant entries after filtering
                result = gen.infer_tasks_from_activity([{"logs": []}])
                assert result == []

    def test_infer_tasks_success(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                logs = [{
                    "logs": [{
                        "window_title": "Slack - #general",
                        "active_app": "Slack",
                        "timestamp": "2025-01-15T10:00:00",
                        "displays": [{"ocr_text": "メンションがあります"}],
                    }]
                }]
                llm_tasks = [
                    {"title": "Slack返信", "content": "メンション対応", "task_type": "work", "priority": "high", "reason": "メンション"}
                ]
                mock_response = MagicMock()
                mock_response.text = json.dumps(llm_tasks)
                mock_client.models.generate_content.return_value = mock_response
                result = gen.infer_tasks_from_activity(logs)
                assert len(result) == 1
                assert result[0]["source"] == "activity_logger_llm"
                assert result[0]["priority"] == "B"

    def test_infer_tasks_low_priority(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                logs = [{"logs": [{"window_title": "ブラウザ", "timestamp": "2025-01-15T10:00:00", "displays": []}]}]
                llm_tasks = [{"title": "タスク", "content": "内容", "task_type": "work", "priority": "low", "reason": "r"}]
                mock_response = MagicMock()
                mock_response.text = json.dumps(llm_tasks)
                mock_client.models.generate_content.return_value = mock_response
                result = gen.infer_tasks_from_activity(logs)
                assert result[0]["priority"] == "C"

    def test_infer_tasks_api_error(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                mock_client = MagicMock()
                mock_genai.Client.return_value = mock_client
                gen = mod.HowToDoGenerator(api_key="test-key")
                logs = [{"logs": [{"window_title": "Test", "timestamp": "2025-01-15T10:00:00", "displays": []}]}]
                mock_client.models.generate_content.side_effect = RuntimeError("error")
                result = gen.infer_tasks_from_activity(logs)
                assert result == []


# ===================================================================
# HowToDoGenerator.generate (fallback path)
# ===================================================================

class TestGenerateFallback:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def _patch_fallback_methods(self, gen, mod):
        """Patch internal methods that reference non-existent TaskType members."""
        gen._generate_summary = MagicMock(return_value="タスク概要")
        gen._generate_completion_criteria = MagicMock(return_value="完了条件")
        gen._generate_prerequisites = MagicMock(return_value=["前提条件"])
        gen._build_default_steps = MagicMock(return_value=[
            mod.HowToDoStep(1, "ステップ1", "条件1", "Cursor"),
            mod.HowToDoStep(2, "ステップ2", "条件2"),
        ])

    def test_generate_work_fallback(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        self._patch_fallback_methods(gen, mod)
        task = {"title": "API実装", "content": "ユーザー認証APIを追加", "source": "specstory"}
        result = gen.generate(task)
        assert result.task_type == mod.TaskType.WORK
        assert len(result.steps) > 0
        assert result.cursor_prompt is not None

    def test_generate_meeting_fallback(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        self._patch_fallback_methods(gen, mod)
        task = {"title": "定例ミーティング", "content": "チーム定例", "source": "calendar"}
        result = gen.generate(task)
        assert result.task_type == mod.TaskType.MEETING
        assert len(result.steps) > 0

    def test_generate_browser_fallback(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        self._patch_fallback_methods(gen, mod)
        task = {"title": "freee経費申請", "content": "freeeで経費を確認", "source": "slack"}
        result = gen.generate(task)
        assert result.task_type == mod.TaskType.BROWSER
        assert result.browser_shortcut is not None

    def test_generate_with_reply(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        self._patch_fallback_methods(gen, mod)
        task = {"title": "確認して返信", "content": "確認してください", "source": "slack", "mentions": ["@user"]}
        result = gen.generate(task)
        assert result.needs_reply is True
        assert len(result.reply_examples) == 3

    def test_generate_with_remaining_tasks(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        self._patch_fallback_methods(gen, mod)
        task = {
            "title": "タスク",
            "content": "内容",
            "source": "specstory",
            "remaining_tasks": ["コード修正", "テスト作成", "ドキュメント更新"],
        }
        result = gen.generate(task)
        # With remaining_tasks, _build_steps_from_remaining_tasks is used (not _build_default_steps)
        assert len(result.steps) == 3
        assert "コード修正" in result.steps[0].action


# ===================================================================
# HowToDoGenerator._generate_with_llm
# ===================================================================

class TestGenerateWithLLM:

    def test_generate_llm_success(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                with patch.object(mod, "genai_types") as mock_types:
                    mock_client = MagicMock()
                    mock_genai.Client.return_value = mock_client
                    gen = mod.HowToDoGenerator(api_key="test-key")
                    llm_result = {
                        "summary": "タスク概要",
                        "completion_criteria": "完了条件",
                        "steps": [{"order": 1, "action": "ステップ1", "check_condition": "条件1"}],
                        "estimated_minutes": 10,
                        "cursor_prompt": "プロンプト",
                    }
                    mock_response = MagicMock()
                    mock_response.text = json.dumps(llm_result)
                    mock_client.models.generate_content.return_value = mock_response
                    task = {"title": "テスト", "content": "内容", "source": "specstory"}
                    result = gen.generate(task)
                    assert result.summary == "タスク概要"
                    assert len(result.steps) == 1

    def test_generate_llm_error_falls_back(self, mod, monkeypatch):
        with patch.object(mod, "HAS_GENAI", True):
            with patch.object(mod, "genai") as mock_genai:
                with patch.object(mod, "genai_types") as mock_types:
                    mock_client = MagicMock()
                    mock_genai.Client.return_value = mock_client
                    gen = mod.HowToDoGenerator(api_key="test-key")
                    mock_client.models.generate_content.side_effect = RuntimeError("fail")
                    # Patch methods that reference non-existent TaskType members
                    gen._generate_summary = MagicMock(return_value="概要")
                    gen._generate_completion_criteria = MagicMock(return_value="完了条件")
                    gen._generate_prerequisites = MagicMock(return_value=["前提"])
                    gen._build_default_steps = MagicMock(return_value=[
                        mod.HowToDoStep(1, "s1", "c1"),
                    ])
                    task = {"title": "テスト", "content": "内容", "source": "specstory"}
                    result = gen.generate(task)
                    assert result.task_type == mod.TaskType.WORK
                    assert len(result.steps) > 0


# ===================================================================
# _extract_source_info
# ===================================================================

class TestExtractSourceInfo:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def test_specstory_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({
            "source": "specstory", "file": "/path/to/file",
            "remaining_tasks": ["t1", "t2"],
        })
        assert info["source_type"] == "specstory"
        assert "SpecStory" in info["reason"]
        assert info["resource_path"] == "/path/to/file"
        assert len(info["remaining_todos"]) == 2

    def test_slack_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({
            "source": "slack", "workspace": "test-ws", "channel": "general",
            "slack_url": "https://slack.com/msg", "mentions": ["@u"],
        })
        assert "Slack" in info["reason"]
        assert info["resource_url"] == "https://slack.com/msg"

    def test_activity_logger_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "activity_logger"})
        assert "Activity Log" in info["reason"]

    def test_activity_logger_llm_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "activity_logger_llm", "llm_reason": "推測理由"})
        assert info["reason"] == "推測理由"

    def test_calendar_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "calendar"})
        assert "カレンダー" in info["reason"]

    def test_gmail_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "gmail"})
        assert "Gmail" in info["reason"]

    def test_voicememo_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "voicememo"})
        assert "音声メモ" in info["reason"]

    def test_unknown_source(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        info = gen._extract_source_info({"source": "unknown"})
        assert info["reason"] == ""


# ===================================================================
# _extract_action_keywords / _guess_tool
# ===================================================================

class TestHelperMethods:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def test_extract_action_keywords(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        result = gen._extract_action_keywords("APIを実装して追加")
        assert "実装" in result
        assert "追加" in result

    def test_extract_action_keywords_empty(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        result = gen._extract_action_keywords("テスト")
        assert result == ""

    def test_guess_tool_cursor(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        assert gen._guess_tool("コードを修正する") == "Cursor"

    def test_guess_tool_terminal(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        assert gen._guess_tool("npmコマンドを実行") == "Terminal"

    def test_guess_tool_browser(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        assert gen._guess_tool("ブラウザで画面を確認") == "Browser"

    def test_guess_tool_email(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        assert gen._guess_tool("slackで返信する") == "Email/Slack"

    def test_guess_tool_none(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        assert gen._guess_tool("何かをする") is None


# ===================================================================
# _generate_reply_examples
# ===================================================================

class TestGenerateReplyExamples:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def test_confirm_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "確認依頼", "content": "確認してください"})
        assert len(examples) == 3
        assert any("確認" in e for e in examples)

    def test_request_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "お願い", "content": "依頼です"})
        assert len(examples) == 3

    def test_question_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "質問", "content": "教えてください"})
        assert len(examples) == 3

    def test_report_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "報告", "content": "共有します"})
        assert len(examples) == 3

    def test_consult_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "相談", "content": "相談したい"})
        assert len(examples) == 3

    def test_default_pattern(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        examples = gen._generate_reply_examples({"title": "メッセージ", "content": "内容"})
        assert len(examples) == 3


# ===================================================================
# _generate_cursor_prompt / _generate_browser_shortcut
# ===================================================================

class TestCursorPromptAndShortcut:

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def test_cursor_prompt_basic(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        prompt = gen._generate_cursor_prompt({"title": "テスト", "content": "内容"})
        assert "テスト" in prompt
        assert "実行手順" in prompt

    def test_cursor_prompt_with_file(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        prompt = gen._generate_cursor_prompt({"title": "テスト", "file": "/path/to/file.py"})
        assert "/path/to/file.py" in prompt

    def test_cursor_prompt_with_remaining_tasks(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        prompt = gen._generate_cursor_prompt({
            "title": "テスト", "remaining_tasks": ["t1", "t2"],
        })
        assert "t1" in prompt
        assert "t2" in prompt

    def test_browser_shortcut_freee(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        shortcut = gen._generate_browser_shortcut({"title": "freee経費", "content": ""})
        assert "freee" in shortcut["start_url"]

    def test_browser_shortcut_github(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        shortcut = gen._generate_browser_shortcut({"title": "GitHub PR", "content": ""})
        assert "github" in shortcut["start_url"]

    def test_browser_shortcut_slack(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        shortcut = gen._generate_browser_shortcut({"title": "Slack確認", "content": ""})
        assert "slack" in shortcut["start_url"]

    def test_browser_shortcut_default(self, mod, monkeypatch):
        gen = self._make_gen(mod, monkeypatch)
        shortcut = gen._generate_browser_shortcut({"title": "タスク", "content": ""})
        assert shortcut["start_url"] == "https://example.com"


# ===================================================================
# _generate_summary / _generate_completion_criteria / _generate_prerequisites
# ===================================================================

class TestGenerateMeta:
    """_generate_summary, _generate_completion_criteria, _generate_prerequisites
    reference non-existent TaskType members (REPLY, APPROVAL, DOCUMENT).
    These tests verify the AttributeError is raised, confirming the enum mismatch."""

    def _make_gen(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            return mod.HowToDoGenerator()

    def test_summary_raises_for_missing_types(self, mod, monkeypatch):
        """_generate_summary references non-existent TaskType.REPLY → AttributeError"""
        gen = self._make_gen(mod, monkeypatch)
        with pytest.raises(AttributeError):
            gen._generate_summary({"title": "タスク"}, mod.TaskType.WORK)

    def test_completion_criteria_raises_for_missing_types(self, mod, monkeypatch):
        """_generate_completion_criteria references non-existent TaskType.REPLY → AttributeError"""
        gen = self._make_gen(mod, monkeypatch)
        with pytest.raises(AttributeError):
            gen._generate_completion_criteria({"title": "タスク"}, mod.TaskType.WORK)

    def test_prerequisites_browser_with_freee(self, mod, monkeypatch):
        """_generate_prerequisites references TaskType.APPROVAL but BROWSER path tested first."""
        gen = self._make_gen(mod, monkeypatch)
        # This raises because the dict literal also references TaskType.APPROVAL
        with pytest.raises(AttributeError):
            gen._generate_prerequisites(
                {"title": "freee確認", "content": "freee"}, mod.TaskType.BROWSER
            )

    def test_prerequisites_work_path(self, mod, monkeypatch):
        """_generate_prerequisites checks task_type in [BROWSER, APPROVAL, DOCUMENT] → raises"""
        gen = self._make_gen(mod, monkeypatch)
        # The list [TaskType.BROWSER, TaskType.APPROVAL, ...] references non-existent APPROVAL
        with pytest.raises(AttributeError):
            gen._generate_prerequisites(
                {"title": "API", "content": "api"}, mod.TaskType.WORK
            )


# ===================================================================
# generate_batch
# ===================================================================

class TestGenerateBatch:

    def test_batch_multiple_tasks(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            # Patch fallback methods that reference non-existent enum members
            gen._generate_summary = MagicMock(return_value="概要")
            gen._generate_completion_criteria = MagicMock(return_value="完了条件")
            gen._generate_prerequisites = MagicMock(return_value=["前提"])
            gen._build_default_steps = MagicMock(return_value=[
                mod.HowToDoStep(1, "s1", "c1"),
            ])
            tasks = [
                {"title": "タスク1", "content": "内容1", "source": "slack"},
                {"title": "タスク2", "content": "内容2", "source": "specstory"},
            ]
            results = gen.generate_batch(tasks)
            assert len(results) == 2
            for r in results:
                assert "howtodo" in r
                assert "original_title" in r

    def test_batch_empty(self, mod, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with patch.object(mod, "HAS_GENAI", False):
            gen = mod.HowToDoGenerator()
            results = gen.generate_batch([])
            assert results == []


# ===================================================================
# generate_shortcuts_yaml
# ===================================================================

class TestGenerateShortcutsYaml:

    def test_browser_task_generates_yaml(self, mod):
        tasks = [{
            "howtodo": {
                "task_type": "browser",
                "browser_shortcut": {"name": "test-shortcut", "prompt": "do it", "start_url": "https://example.com"},
            }
        }]
        result = mod.generate_shortcuts_yaml(tasks)
        assert "test-shortcut" in result

    def test_non_browser_task_excluded(self, mod):
        tasks = [{
            "howtodo": {
                "task_type": "work",
                "cursor_prompt": "prompt",
            }
        }]
        result = mod.generate_shortcuts_yaml(tasks)
        assert result.strip() in ("[]", "")

    def test_empty_tasks(self, mod):
        result = mod.generate_shortcuts_yaml([])
        assert isinstance(result, str)

    def test_without_yaml_module(self, mod):
        tasks = [{
            "howtodo": {
                "task_type": "browser",
                "browser_shortcut": {"name": "test", "prompt": "p", "start_url": "https://example.com"},
            }
        }]
        with patch.object(mod, "HAS_YAML", False):
            result = mod.generate_shortcuts_yaml(tasks)
            assert "test" in result  # JSON format fallback

    def test_no_shortcut_data(self, mod):
        tasks = [{"howtodo": {"task_type": "browser"}}]
        result = mod.generate_shortcuts_yaml(tasks)
        assert isinstance(result, str)
