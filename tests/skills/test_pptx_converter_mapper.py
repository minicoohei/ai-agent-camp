"""pptx-converter/scripts/mapper.py の単体テスト"""
import pytest
import json


class TestImport:
    def test_import_module(self):
        from mapper import (
            _extract_json_from_response,
            _guess_extension,
            _extract_current_value,
            _deep_copy_element,
        )


class TestExtractJsonFromResponse:
    def test_json_code_block(self):
        from mapper import _extract_json_from_response
        text = '```json\n[{"role": "title"}]\n```'
        result = _extract_json_from_response(text)
        assert result == [{"role": "title"}]

    def test_bare_json(self):
        from mapper import _extract_json_from_response
        text = '[{"role": "body"}, {"role": "caption"}]'
        result = _extract_json_from_response(text)
        assert len(result) == 2

    def test_json_with_surrounding_text(self):
        from mapper import _extract_json_from_response
        text = 'Here is the analysis:\n```json\n[{"role": "title"}]\n```\nDone.'
        result = _extract_json_from_response(text)
        assert result == [{"role": "title"}]

    def test_empty_text(self):
        from mapper import _extract_json_from_response
        assert _extract_json_from_response("") is None

    def test_none_text(self):
        from mapper import _extract_json_from_response
        assert _extract_json_from_response(None) is None

    def test_invalid_json(self):
        from mapper import _extract_json_from_response
        assert _extract_json_from_response("not json at all") is None

    def test_json_object_not_array(self):
        from mapper import _extract_json_from_response
        assert _extract_json_from_response('{"key": "value"}') is None


class TestGuessExtension:
    def test_png(self):
        from mapper import _guess_extension
        assert _guess_extension("image/png") == ".png"

    def test_jpeg(self):
        from mapper import _guess_extension
        assert _guess_extension("image/jpeg") == ".jpg"

    def test_gif(self):
        from mapper import _guess_extension
        assert _guess_extension("image/gif") == ".gif"

    def test_svg(self):
        from mapper import _guess_extension
        assert _guess_extension("image/svg+xml") == ".svg"

    def test_webp(self):
        from mapper import _guess_extension
        assert _guess_extension("image/webp") == ".webp"

    def test_unknown_defaults_png(self):
        from mapper import _guess_extension
        assert _guess_extension("application/octet-stream") == ".png"


class TestExtractCurrentValue:
    def test_text_type(self):
        from mapper import _extract_current_value
        result = _extract_current_value({"type": "text", "value": "Hello World"})
        assert result == "Hello World"

    def test_text_truncated(self):
        from mapper import _extract_current_value
        result = _extract_current_value({"type": "text", "value": "a" * 200})
        assert len(result) <= 100

    def test_chart_with_categories(self):
        from mapper import _extract_current_value
        result = _extract_current_value({
            "type": "chart",
            "value": {"categories": ["Q1", "Q2", "Q3"]}
        })
        assert "3 categories" in result

    def test_chart_without_value(self):
        from mapper import _extract_current_value
        result = _extract_current_value({"type": "chart", "value": ""})
        assert result == "chart"

    def test_table_with_rows(self):
        from mapper import _extract_current_value
        result = _extract_current_value({
            "type": "table",
            "value": [["a", "b"], ["c", "d"]]
        })
        assert "2 rows" in result

    def test_image_with_path(self):
        from mapper import _extract_current_value
        result = _extract_current_value({
            "type": "image",
            "value": "",
            "image_info": {"extracted_path": "assets/logo.png"}
        })
        assert result == "assets/logo.png"

    def test_empty_value(self):
        from mapper import _extract_current_value
        result = _extract_current_value({"type": "text", "value": ""})
        assert result == ""


class TestDeepCopyElement:
    def test_basic_copy(self):
        from mapper import _deep_copy_element
        original = {"type": "text", "value": "hello"}
        copied = _deep_copy_element(original)
        assert copied == original
        copied["value"] = "modified"
        assert original["value"] == "hello"

    def test_children_are_copied(self):
        from mapper import _deep_copy_element
        original = {
            "type": "group",
            "children": [{"type": "text", "value": "child"}]
        }
        copied = _deep_copy_element(original)
        copied["children"][0]["value"] = "modified"
        assert original["children"][0]["value"] == "child"

    def test_text_nodes_are_copied(self):
        from mapper import _deep_copy_element
        original = {
            "type": "smartart",
            "text_nodes": [{"text": "node1"}]
        }
        copied = _deep_copy_element(original)
        copied["text_nodes"][0]["text"] = "modified"
        assert original["text_nodes"][0]["text"] == "node1"
