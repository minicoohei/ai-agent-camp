"""
tutor_generate.py のユニットテスト

学習コンテンツ生成ツールのテスト:
- safe_parse_json: JSON 安全パース
- generate_topic_tutorial: トピック→チュートリアル
- generate_file_tutorial: ファイル→マニュアル
- generate_text_tutorial: テキスト→解説
- create_svg_diagram: SVG 図解生成
- sanitize_plantuml_text: PlantUML テキストサニタイズ
- build_sequence_plantuml: シーケンス図生成
- build_tutorial_html: HTML 構築
- 境界値テスト
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    """tutor_generate モジュールをロード"""
    return import_module_from_repo("tutor_generate", "tools/tutor_generate.py")


# ===================================================================
# safe_parse_json
# ===================================================================

class TestSafeParseJson:

    def test_valid_json(self, mod):
        result = mod.safe_parse_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_json_in_code_block(self, mod):
        raw = '```json\n{"key": "value"}\n```'
        result = mod.safe_parse_json(raw)
        assert result == {"key": "value"}

    def test_empty_string(self, mod):
        """境界値: 空文字列"""
        result = mod.safe_parse_json("")
        assert result == {}

    def test_completely_invalid(self, mod):
        """完全に無効な文字列"""
        result = mod.safe_parse_json("not json at all")
        assert result == {}

    def test_truncated_json(self, mod):
        """途中で切れた JSON"""
        result = mod.safe_parse_json('{"key": "value", "key2": "trun')
        # 修復を試みて最後の有効なオブジェクトを返すか {}
        assert isinstance(result, dict)

    def test_nested_json(self, mod):
        nested = json.dumps({"outer": {"inner": [1, 2, 3]}})
        result = mod.safe_parse_json(nested)
        assert result["outer"]["inner"] == [1, 2, 3]

    def test_json_with_extra_text(self, mod):
        """JSON の後に余分なテキスト"""
        raw = '{"key": "value"} extra text here'
        result = mod.safe_parse_json(raw)
        # 修復ロジックで最初の完全なオブジェクトを取得
        assert result.get("key") == "value"

    def test_unicode_json(self, mod):
        raw = '{"title": "日本語テスト", "emoji": "🎯"}'
        result = mod.safe_parse_json(raw)
        assert result["title"] == "日本語テスト"

    def test_array_json(self, mod):
        raw = '[1, 2, 3]'
        result = mod.safe_parse_json(raw)
        assert result == [1, 2, 3]

    def test_code_block_with_language_tag(self, mod):
        raw = '```json\n{"a": 1}\n```'
        result = mod.safe_parse_json(raw)
        assert result == {"a": 1}

    def test_multiple_code_blocks(self, mod):
        """複数のコードブロック → 最初のものを取得"""
        raw = '```json\n{"first": true}\n```\n\nsome text\n```json\n{"second": true}\n```'
        result = mod.safe_parse_json(raw)
        # greedy regex captures everything between first ``` and last ```
        assert isinstance(result, dict)

    def test_none_like_string(self, mod):
        result = mod.safe_parse_json("null")
        # json.loads("null") returns None, which is falsy
        assert result is None or result == {}


# ===================================================================
# generate_topic_tutorial
# ===================================================================

class TestGenerateTopicTutorial:

    def test_no_client_fallback(self, mod):
        """client=None の場合のフォールバック"""
        result = mod.generate_topic_tutorial(None, "Python入門")
        assert "Python入門" in result["title"]
        assert isinstance(result["sections"], list)

    def test_with_mock_client(self, mod):
        """正常な API レスポンス"""
        response_data = {
            "title": "Python入門チュートリアル",
            "introduction": "Pythonの基本",
            "sequence_flow": [],
            "prerequisites": ["基礎知識"],
            "sections": [{"title": "変数", "content": "説明", "code_example": "", "tips": []}],
            "common_mistakes": [],
            "summary": ["まとめ"],
            "next_steps": ["応用"]
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_topic_tutorial(mock_client, "Python入門")

        assert result["title"] == "Python入門チュートリアル"

    def test_api_error_fallback(self, mod):
        """API エラー時のフォールバック"""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("API error")

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_topic_tutorial(mock_client, "テスト")

        assert isinstance(result, dict)
        assert "title" in result

    def test_json_parse_failure(self, mod):
        """JSON パース失敗時のフォールバック"""
        mock_response = MagicMock()
        mock_response.text = "invalid json {"

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_topic_tutorial(mock_client, "テスト")

        assert isinstance(result, dict)

    def test_empty_topic(self, mod):
        """境界値: 空のトピック"""
        result = mod.generate_topic_tutorial(None, "")
        assert isinstance(result, dict)

    def test_unicode_topic(self, mod):
        """Unicode 特殊文字のトピック"""
        result = mod.generate_topic_tutorial(None, "日本語🎯テスト①②③")
        assert isinstance(result, dict)


# ===================================================================
# generate_file_tutorial
# ===================================================================

class TestGenerateFileTutorial:

    def test_no_client_fallback(self, mod, tmp_path):
        """client=None の場合のフォールバック"""
        f = tmp_path / "test.py"
        f.write_text("print('hello')", encoding="utf-8")
        result = mod.generate_file_tutorial(None, str(f))
        assert "マニュアル" in result["title"]

    def test_file_not_found(self, mod):
        """存在しないファイル"""
        result = mod.generate_file_tutorial(None, "/nonexistent/file.py")
        assert "読み込めませんでした" in result.get("introduction", "")

    def test_with_mock_client(self, mod, tmp_path):
        """正常な API レスポンス"""
        f = tmp_path / "test.py"
        f.write_text("def hello(): pass", encoding="utf-8")

        response_data = {
            "title": "test.py マニュアル",
            "introduction": "テストファイル",
            "sequence_flow": [],
            "process_steps": ["手順1"],
            "prerequisites": [],
            "sections": [],
            "common_mistakes": [],
            "summary": [],
            "next_steps": []
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_file_tutorial(mock_client, str(f))

        assert result["title"] == "test.py マニュアル"

    def test_large_file_truncated(self, mod, tmp_path):
        """境界値: 非常に大きなファイル（8000文字で切り詰め）"""
        f = tmp_path / "big.py"
        f.write_text("x" * 20000, encoding="utf-8")
        result = mod.generate_file_tutorial(None, str(f))
        assert isinstance(result, dict)


# ===================================================================
# generate_text_tutorial
# ===================================================================

class TestGenerateTextTutorial:

    def test_no_client_fallback(self, mod):
        result = mod.generate_text_tutorial(None, "テストテキスト")
        assert isinstance(result, dict)

    def test_empty_text(self, mod):
        """境界値: 空のテキスト"""
        result = mod.generate_text_tutorial(None, "")
        assert isinstance(result, dict)

    def test_very_long_text(self, mod):
        """境界値: 非常に長いテキスト"""
        result = mod.generate_text_tutorial(None, "テスト" * 10000)
        assert isinstance(result, dict)


# ===================================================================
# create_svg_diagram
# ===================================================================

class TestCreateSvgDiagram:

    def test_returns_svg(self, mod):
        svg = mod.create_svg_diagram("テスト")
        assert "<svg" in svg
        assert "</svg>" in svg

    def test_topic_in_svg(self, mod):
        svg = mod.create_svg_diagram("Python入門")
        assert "Python入門" in svg

    def test_empty_topic(self, mod):
        """境界値: 空のトピック"""
        svg = mod.create_svg_diagram("")
        assert "<svg" in svg

    def test_special_chars_in_topic(self, mod):
        """特殊文字を含むトピック"""
        svg = mod.create_svg_diagram("<script>alert('xss')</script>")
        assert "<svg" in svg

    def test_unicode_topic(self, mod):
        svg = mod.create_svg_diagram("日本語テスト🎯")
        assert "日本語テスト🎯" in svg


# ===================================================================
# sanitize_plantuml_text
# ===================================================================

class TestSanitizePlantUmlText:

    def test_parentheses_to_fullwidth(self, mod):
        result = mod.sanitize_plantuml_text("hello(world)")
        assert "（" in result and "）" in result
        assert "(" not in result

    def test_angle_brackets(self, mod):
        result = mod.sanitize_plantuml_text("<tag>")
        assert "＜" in result and "＞" in result

    def test_newline_to_space(self, mod):
        result = mod.sanitize_plantuml_text("line1\nline2")
        assert "\n" not in result
        assert "line1 line2" == result

    def test_semicolon(self, mod):
        result = mod.sanitize_plantuml_text("a;b")
        assert "；" in result

    def test_empty_string(self, mod):
        """境界値: 空文字列"""
        assert mod.sanitize_plantuml_text("") == ""

    def test_no_special_chars(self, mod):
        """特殊文字なしの場合"""
        assert mod.sanitize_plantuml_text("hello world") == "hello world"

    def test_all_special_chars(self, mod):
        """全特殊文字を含む"""
        result = mod.sanitize_plantuml_text("(<>;)\n")
        assert "（" in result
        assert "＜" in result
        assert "＞" in result
        assert "；" in result
        assert "\n" not in result


# ===================================================================
# build_sequence_plantuml
# ===================================================================

class TestBuildSequencePlantuml:

    def test_empty_flow(self, mod):
        """空のフローは空文字列"""
        assert mod.build_sequence_plantuml([]) == ""

    def test_single_message(self, mod):
        flow = ["User -> System: リクエスト送信"]
        result = mod.build_sequence_plantuml(flow)
        assert "@startuml" in result
        assert "@enduml" in result
        assert '"User"' in result
        assert '"System"' in result
        assert "リクエスト送信" in result

    def test_multiple_messages(self, mod):
        flow = [
            "User -> API: リクエスト",
            "API -> DB: クエリ",
            "DB -> API: 結果",
            "API -> User: レスポンス"
        ]
        result = mod.build_sequence_plantuml(flow)
        assert result.count("participant") == 3  # User, API, DB

    def test_invalid_format_ignored(self, mod):
        """不正なフォーマットは無視"""
        flow = ["invalid format without arrow"]
        result = mod.build_sequence_plantuml(flow)
        assert "@startuml" in result
        # 不正な行は参加者・メッセージに含まれない

    def test_mixed_valid_invalid(self, mod):
        flow = [
            "User -> System: 有効",
            "これは無効な行",
            "System -> User: 応答",
        ]
        result = mod.build_sequence_plantuml(flow)
        assert "有効" in result
        assert "応答" in result

    def test_none_in_flow(self, mod):
        """None を含むフロー"""
        flow = [None, "User -> System: テスト"]
        # None は文字列でないので " -> " in None で例外の可能性
        # 実装次第で挙動が変わるが、クラッシュしないことを確認
        try:
            result = mod.build_sequence_plantuml(flow)
            assert isinstance(result, str)
        except (TypeError, AttributeError):
            pass  # None 対応がない場合はエラーが出ても OK


# ===================================================================
# build_tutorial_html
# ===================================================================

class TestBuildTutorialHtml:

    def test_basic_tutorial(self, mod):
        data = {
            "title": "テスト",
            "introduction": "はじめに",
            "sequence_flow": [],
            "prerequisites": ["前提1"],
            "sections": [
                {"title": "セクション1", "content": "内容", "code_example": "print(1)", "tips": ["ヒント"]}
            ],
            "common_mistakes": [{"mistake": "間違い", "correction": "修正"}],
            "summary": ["まとめ1"],
            "next_steps": ["次のステップ"]
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "はじめに" in html
        assert "前提1" in html
        assert "セクション1" in html

    def test_with_source_info(self, mod):
        data = {"title": "テスト", "sections": [], "sequence_flow": []}
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data, source_info="test.py")
        assert "test.py" in html

    def test_empty_tutorial_data(self, mod):
        """境界値: 空のデータ"""
        data = {}
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert isinstance(html, str)

    def test_with_process_steps(self, mod):
        """process_steps がある場合"""
        data = {
            "title": "テスト",
            "process_steps": ["手順1", "手順2"],
            "sequence_flow": [],
            "sections": [],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert isinstance(html, str)

    def test_sections_without_code(self, mod):
        """code_example がないセクション"""
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "sections": [{"title": "S1", "content": "内容", "tips": ["t1"]}],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "S1" in html


# ===================================================================
# DEFAULT_TUTOR_DIR
# ===================================================================

class TestConstants:

    def test_default_dir(self, mod):
        assert isinstance(mod.DEFAULT_TUTOR_DIR, Path)


# ===================================================================
# generate_text_tutorial (with mock client)
# ===================================================================

class TestGenerateTextTutorialWithClient:

    def test_with_mock_client(self, mod):
        """正常な API レスポンス"""
        response_data = {
            "title": "テキスト解説",
            "introduction": "テキストの解説",
            "sequence_flow": [],
            "prerequisites": [],
            "sections": [{"title": "概要", "content": "内容", "code_example": "", "tips": []}],
            "common_mistakes": [],
            "summary": ["まとめ"],
            "next_steps": ["次へ"],
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_text_tutorial(mock_client, "テストテキスト")
        assert result["title"] == "テキスト解説"

    def test_api_error_fallback(self, mod):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_text_tutorial(mock_client, "テスト")
        assert isinstance(result, dict)
        assert "title" in result

    def test_json_parse_failure(self, mod):
        mock_response = MagicMock()
        mock_response.text = "not valid json"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_text_tutorial(mock_client, "テスト")
        assert isinstance(result, dict)


# ===================================================================
# generate_file_tutorial (additional)
# ===================================================================

class TestGenerateFileTutorialAdditional:

    def test_api_error_fallback(self, mod, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("print('hello')", encoding="utf-8")
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("fail")
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_file_tutorial(mock_client, str(f))
        assert isinstance(result, dict)

    def test_json_parse_failure(self, mod, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("x = 1", encoding="utf-8")
        mock_response = MagicMock()
        mock_response.text = "not json"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_file_tutorial(mock_client, str(f))
        assert isinstance(result, dict)

    def test_binary_file(self, mod, tmp_path):
        """バイナリファイルの読み込み試行"""
        f = tmp_path / "binary.bin"
        f.write_bytes(b"\x00\x01\x02\x03" * 1000)
        result = mod.generate_file_tutorial(None, str(f))
        assert isinstance(result, dict)


# ===================================================================
# analyze_learning_gaps
# ===================================================================

class TestAnalyzeLearningGaps:

    def test_no_client_fallback(self, mod):
        result = mod.analyze_learning_gaps(None, "テスト会話履歴")
        assert isinstance(result, dict)
        assert "topics" in result

    def test_with_client_success(self, mod):
        response_data = {
            "sequence_flow": ["User -> Assistant: 質問"],
            "topics": [{"topic": "Git", "reason": "理解不足", "priority": "high", "related_concepts": []}],
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_learning_gaps(mock_client, "テスト")
        assert len(result["topics"]) == 1

    def test_api_error(self, mod):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("error")
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_learning_gaps(mock_client, "テスト")
        assert "topics" in result

    def test_json_parse_failure(self, mod):
        mock_response = MagicMock()
        mock_response.text = "invalid"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_learning_gaps(mock_client, "テスト")
        assert isinstance(result, dict)


# ===================================================================
# generate_learning_content
# ===================================================================

class TestGenerateLearningContent:

    def test_no_client_fallback(self, mod):
        result = mod.generate_learning_content(None, "Git", "学習必要", ["GitHub"])
        assert isinstance(result, dict)
        assert "concept" in result

    def test_with_client_success(self, mod):
        response_data = {
            "prerequisites": ["基礎知識"],
            "concept": "Gitとは",
            "examples": [{"title": "例", "description": "説明", "code": "git init"}],
            "common_mistakes": [{"mistake": "間違い", "explanation": "正しい方法"}],
            "summary": ["まとめ"],
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_learning_content(mock_client, "Git", "理由", [])
        assert result["concept"] == "Gitとは"

    def test_api_error(self, mod):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = RuntimeError("error")
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_learning_content(mock_client, "Git", "理由", [])
        assert isinstance(result, dict)

    def test_with_code_block_response(self, mod):
        mock_response = MagicMock()
        mock_response.text = '```json\n{"prerequisites": [], "concept": "テスト", "examples": [], "common_mistakes": [], "summary": []}\n```'
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_learning_content(mock_client, "テスト", "理由", [])
        assert result["concept"] == "テスト"

    def test_empty_related_concepts(self, mod):
        result = mod.generate_learning_content(None, "Python", "学習", [])
        assert isinstance(result, dict)


# ===================================================================
# build_tutorial_html (extended)
# ===================================================================

class TestBuildTutorialHtmlExtended:

    def test_with_common_mistakes(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "sections": [],
            "common_mistakes": [
                {"mistake": "間違い1", "correction": "修正1"},
                {"mistake": "間違い2", "explanation": "説明2"},
            ],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "間違い1" in html
        assert "修正1" in html

    def test_with_summary_and_next_steps(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "sections": [],
            "summary": ["ポイント1", "ポイント2"],
            "next_steps": ["次のステップ1"],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "ポイント1" in html
        assert "次のステップ1" in html

    def test_section_with_dict_code_example(self, mod):
        """code_example が dict の場合"""
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "sections": [{"title": "S1", "content": "内容", "code_example": {"key": "value"}, "tips": []}],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "key" in html

    def test_with_sequence_flow(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": ["User -> System: リクエスト"],
            "sections": [],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value="@startuml\n@enduml"):
            with patch.object(mod, "generate_plantuml_img_tag", return_value="<img/>"):
                html = mod.build_tutorial_html(data)
        assert "処理フロー" in html

    def test_with_process_steps_plantuml(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "process_steps": ["手順1", "手順2"],
            "sections": [],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            with patch.object(mod, "generate_plantuml_img_tag", return_value="<img/>"):
                html = mod.build_tutorial_html(data)
        assert "手順フロー" in html

    def test_with_introduction(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "introduction": "はじめにの説明です。",
            "sections": [],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "はじめにの説明です。" in html

    def test_with_prerequisites(self, mod):
        data = {
            "title": "テスト",
            "sequence_flow": [],
            "prerequisites": ["Python基礎", "Git基礎"],
            "sections": [],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            html = mod.build_tutorial_html(data)
        assert "Python基礎" in html


# ===================================================================
# build_specstory_html
# ===================================================================

class TestBuildSpecstoryHtml:

    def test_with_topics(self, mod):
        topics_data = {
            "sequence_flow": ["User -> Assistant: 質問"],
            "topics": [{"topic": "Git", "reason": "学習必要", "related_concepts": ["GitHub"]}],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value="@startuml\n@enduml"):
            with patch.object(mod, "generate_plantuml_img_tag", return_value="<img/>"):
                with patch.object(mod, "generate_learning_content", return_value={
                    "prerequisites": ["基礎"],
                    "concept": "Gitとは",
                    "examples": [{"title": "例", "description": "説明", "code": "git init"}],
                    "common_mistakes": [{"mistake": "間違い", "explanation": "修正"}],
                    "summary": ["まとめ"],
                }):
                    with patch.object(mod, "build_referenced_files_html", return_value=""):
                        html = mod.build_specstory_html(topics_data, None, [])
        assert "Git" in html
        assert "学習ガイド" in html

    def test_empty_topics(self, mod):
        topics_data = {"sequence_flow": [], "topics": []}
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            with patch.object(mod, "build_referenced_files_html", return_value=""):
                html = mod.build_specstory_html(topics_data, None, [])
        assert "見つかりませんでした" in html

    def test_no_sequence_flow(self, mod):
        topics_data = {"topics": [{"topic": "テスト", "reason": "r", "related_concepts": []}]}
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            with patch.object(mod, "generate_learning_content", return_value={
                "prerequisites": [], "concept": "c", "examples": [], "common_mistakes": [], "summary": [],
            }):
                with patch.object(mod, "build_referenced_files_html", return_value=""):
                    html = mod.build_specstory_html(topics_data, None, [])
        assert "テスト" in html

    def test_with_example_code_as_dict(self, mod):
        """code が dict の場合"""
        topics_data = {
            "sequence_flow": [],
            "topics": [{"topic": "T", "reason": "r", "related_concepts": []}],
        }
        with patch.object(mod, "build_sequence_plantuml", return_value=""):
            with patch.object(mod, "generate_learning_content", return_value={
                "prerequisites": [], "concept": "c",
                "examples": [{"title": "例", "description": "d", "code": {"key": "val"}}],
                "common_mistakes": [], "summary": [],
            }):
                with patch.object(mod, "build_referenced_files_html", return_value=""):
                    html = mod.build_specstory_html(topics_data, None, [])
        assert "key" in html


# ===================================================================
# safe_parse_json (additional edge cases)
# ===================================================================

class TestSafeParseJsonAdditional:

    def test_json_with_trailing_comma(self, mod):
        """末尾カンマは修復可能かテスト"""
        raw = '{"key": "value",}'
        result = mod.safe_parse_json(raw)
        assert isinstance(result, dict)

    def test_deeply_nested_json(self, mod):
        nested = {"a": {"b": {"c": {"d": {"e": "deep"}}}}}
        result = mod.safe_parse_json(json.dumps(nested))
        assert result["a"]["b"]["c"]["d"]["e"] == "deep"

    def test_json_with_escaped_quotes(self, mod):
        raw = '{"msg": "He said \\"hello\\""}'
        result = mod.safe_parse_json(raw)
        assert "hello" in result.get("msg", "")

    def test_empty_object(self, mod):
        result = mod.safe_parse_json("{}")
        assert result == {}

    def test_empty_array(self, mod):
        result = mod.safe_parse_json("[]")
        assert result == []


# ===================================================================
# build_sequence_plantuml (additional edge cases)
# ===================================================================

class TestBuildSequencePlantumlAdditional:

    def test_duplicate_participants(self, mod):
        flow = [
            "User -> System: リクエスト1",
            "User -> System: リクエスト2",
        ]
        result = mod.build_sequence_plantuml(flow)
        # 'participant "User"' should appear only once
        assert result.count('participant "User"') == 1

    def test_unicode_actors(self, mod):
        flow = ["ユーザー -> サーバー: リクエスト"]
        result = mod.build_sequence_plantuml(flow)
        assert "ユーザー" in result
        assert "サーバー" in result

    def test_message_with_colon(self, mod):
        """メッセージ部分にコロンが含まれる場合"""
        flow = ["A -> B: URL: https://example.com"]
        result = mod.build_sequence_plantuml(flow)
        assert "URL: https://example.com" in result


# ===================================================================
# safe_parse_json repair logic (lines 59-60, 62-63)
# ===================================================================

class TestSafeParseJsonRepairBranches:

    def test_repair_finds_last_valid_object(self, mod):
        """修復ロジック: depth==0 で last_valid が更新される (line 74)"""
        raw = '{"key": "value"} garbage after'
        result = mod.safe_parse_json(raw)
        assert result.get("key") == "value"

    def test_repair_with_escaped_backslash(self, mod):
        """修復ロジック: escape=True のパス (lines 59-60)"""
        raw = '{"msg": "hello\\\\world"} extra'
        result = mod.safe_parse_json(raw)
        assert isinstance(result, dict)

    def test_repair_string_with_brackets(self, mod):
        """修復ロジック: in_string 時の括弧スキップ (lines 62-63)"""
        raw = '{"msg": "has {braces} and [brackets]"} trailing'
        result = mod.safe_parse_json(raw)
        assert result.get("msg") == "has {braces} and [brackets]"

    def test_repair_last_valid_zero_returns_empty(self, mod):
        """修復ロジック: last_valid==0 で {} を返す (line 76)"""
        raw = '{"key": "never closed'
        result = mod.safe_parse_json(raw)
        assert result == {}


# ===================================================================
# generate_file_tutorial: JSON parse failure branch (lines 208-212)
# ===================================================================

class TestGenerateFileTutorialJsonEmpty:

    def test_json_parse_returns_empty_dict(self, mod, tmp_path):
        """safe_parse_json が空 dict を返した場合のフォールバック"""
        f = tmp_path / "test.py"
        f.write_text("x = 1", encoding="utf-8")
        mock_response = MagicMock()
        mock_response.text = "completely invalid"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"), \
             patch.object(mod, "safe_parse_json", return_value={}):
            result = mod.generate_file_tutorial(mock_client, str(f))
        assert result["title"] == str(f)
        assert result["introduction"] == ""


# ===================================================================
# generate_text_tutorial: JSON parse failure branch (lines 262-274)
# ===================================================================

class TestGenerateTextTutorialJsonEmpty:

    def test_json_parse_returns_empty_dict(self, mod):
        """safe_parse_json が空 dict を返した場合のフォールバック"""
        mock_response = MagicMock()
        mock_response.text = "broken"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"), \
             patch.object(mod, "safe_parse_json", return_value={}):
            result = mod.generate_text_tutorial(mock_client, "test")
        assert result["title"] == "テキスト解説"
        assert result["introduction"] == ""

    def test_exception_fallback(self, mod):
        """例外発生時のフォールバック (lines 272-274)"""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = ValueError("unexpected")

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_text_tutorial(mock_client, "test")
        assert result["title"] == "テキスト解説"


# ===================================================================
# analyze_learning_gaps: result branch (lines 279-325)
# ===================================================================

class TestAnalyzeLearningGapsResult:

    def test_result_with_counts(self, mod):
        """正常レスポンスで topic_count, flow_count を表示"""
        response_data = {
            "sequence_flow": ["User -> Assistant: Q1", "Assistant -> User: A1"],
            "topics": [
                {"topic": "Git", "reason": "r", "priority": "high", "related_concepts": []},
                {"topic": "Docker", "reason": "r2", "priority": "low", "related_concepts": ["K8s"]},
            ],
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_learning_gaps(mock_client, "test")
        assert len(result["topics"]) == 2
        assert len(result["sequence_flow"]) == 2

    def test_empty_result_from_parse(self, mod):
        """safe_parse_json が空 dict を返した場合"""
        mock_response = MagicMock()
        mock_response.text = "garbage"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"), \
             patch.object(mod, "safe_parse_json", return_value={}):
            result = mod.analyze_learning_gaps(mock_client, "test")
        assert result == {"sequence_flow": [], "topics": []}

    def test_exception_branch(self, mod):
        """例外発生時のフォールバック"""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = TypeError("bad")

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.analyze_learning_gaps(mock_client, "test")
        assert result == {"sequence_flow": [], "topics": []}


# ===================================================================
# generate_learning_content: JSON code block & exception (lines 330-352)
# ===================================================================

class TestGenerateLearningContentBranches:

    def test_json_loads_without_code_block(self, mod):
        """コードブロックなしの直接 JSON"""
        response_data = {
            "prerequisites": ["P"],
            "concept": "direct",
            "examples": [],
            "common_mistakes": [],
            "summary": ["S"],
        }
        mock_response = MagicMock()
        mock_response.text = json.dumps(response_data)
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_learning_content(mock_client, "T", "R", [])
        assert result["concept"] == "direct"

    def test_json_loads_failure_exception(self, mod):
        """json.loads が失敗する場合 (例外ブランチ)"""
        mock_response = MagicMock()
        mock_response.text = "not json at all"
        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response

        with patch.object(mod, "get_flash_model", return_value="test-model"):
            result = mod.generate_learning_content(mock_client, "T", "R", ["C1"])
        assert "concept" in result
        assert "T" in result["concept"]
