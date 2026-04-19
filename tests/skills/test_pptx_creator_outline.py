"""pptx-creator/scripts/outline_generator.py の単体テスト"""
import pytest


class TestImport:
    def test_import_module(self):
        from outline_generator import (
            _parse_gemini_response,
            _validate_outline,
            VALID_SLIDE_TYPES,
        )

    def test_valid_slide_types(self):
        from outline_generator import VALID_SLIDE_TYPES
        assert "title" in VALID_SLIDE_TYPES
        assert "closing" in VALID_SLIDE_TYPES
        assert "content" in VALID_SLIDE_TYPES
        assert "kpi_dashboard" in VALID_SLIDE_TYPES


class TestParseGeminiResponse:
    def test_yaml_code_block(self):
        from outline_generator import _parse_gemini_response
        text = """```yaml
title: "テスト"
slides:
  - slide_number: 1
    slide_type: title
    title: "Hello"
```"""
        result = _parse_gemini_response(text)
        assert result["title"] == "テスト"
        assert len(result["slides"]) == 1

    def test_bare_yaml(self):
        from outline_generator import _parse_gemini_response
        text = """title: "Direct YAML"
slides:
  - slide_number: 1
    slide_type: title
    title: "Test"
"""
        result = _parse_gemini_response(text)
        assert result["title"] == "Direct YAML"

    def test_yaml_with_prefix(self):
        from outline_generator import _parse_gemini_response
        text = """Here is the outline:
```yaml
title: "Prefixed"
slides:
  - slide_number: 1
    slide_type: title
    title: "T"
```
Let me know if you need changes."""
        result = _parse_gemini_response(text)
        assert result["title"] == "Prefixed"


class TestValidateOutline:
    def test_valid_outline(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "T", "subtitle": "S"},
                {"slide_number": 2, "slide_type": "content", "title": "C", "bullets": ["a"]},
                {"slide_number": 3, "slide_type": "closing", "title": "End", "subtitle": "Bye"},
            ]
        }
        result = _validate_outline(outline, 3)
        assert len(result["slides"]) == 3
        assert result["slides"][0]["slide_type"] == "title"
        assert result["slides"][-1]["slide_type"] == "closing"

    def test_renumbers_slides(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 10, "slide_type": "title", "title": "T"},
                {"slide_number": 20, "slide_type": "closing", "title": "E"},
            ]
        }
        result = _validate_outline(outline, 2)
        assert result["slides"][0]["slide_number"] == 1
        assert result["slides"][1]["slide_number"] == 2

    def test_unknown_type_falls_back_to_content(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "T"},
                {"slide_number": 2, "slide_type": "unknown_type", "title": "X", "body": "text"},
                {"slide_number": 3, "slide_type": "closing", "title": "E"},
            ]
        }
        result = _validate_outline(outline, 3)
        assert result["slides"][1]["slide_type"] == "content"

    def test_forces_title_first(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 1, "slide_type": "content", "title": "Not Title"},
                {"slide_number": 2, "slide_type": "closing", "title": "End"},
            ]
        }
        result = _validate_outline(outline, 2)
        assert result["slides"][0]["slide_type"] == "title"

    def test_forces_closing_last(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "Start"},
                {"slide_number": 2, "slide_type": "content", "title": "Not Closing"},
            ]
        }
        result = _validate_outline(outline, 2)
        assert result["slides"][-1]["slide_type"] == "closing"

    def test_missing_slides_key_raises(self):
        from outline_generator import _validate_outline
        with pytest.raises(ValueError, match="slides"):
            _validate_outline({"title": "No slides"}, 3)

    def test_empty_slides_raises(self):
        from outline_generator import _validate_outline
        with pytest.raises(ValueError, match="at least one"):
            _validate_outline({"title": "T", "slides": []}, 3)

    def test_non_dict_slides_skipped(self):
        from outline_generator import _validate_outline
        outline = {
            "title": "Test",
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "T"},
                "not a dict",
                {"slide_number": 3, "slide_type": "closing", "title": "E"},
            ]
        }
        result = _validate_outline(outline, 3)
        assert len(result["slides"]) == 2
