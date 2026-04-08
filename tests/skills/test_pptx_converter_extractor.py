"""pptx-converter/scripts/extractor.py の単体テスト（ユーティリティ関数）"""
import pytest


class TestImport:
    def test_import_module(self):
        from extractor import _safe_str, _safe_enum_name, _alignment_name


class TestSafeStr:
    def test_none(self):
        from extractor import _safe_str
        assert _safe_str(None) == ""

    def test_string(self):
        from extractor import _safe_str
        assert _safe_str("hello") == "hello"

    def test_integer(self):
        from extractor import _safe_str
        assert _safe_str(42) == "42"


class TestSafeEnumName:
    def test_none(self):
        from extractor import _safe_enum_name
        assert _safe_enum_name(None) == "unknown"

    def test_with_name_attr(self):
        from extractor import _safe_enum_name

        class FakeEnum:
            name = "TEST_VALUE"

        assert _safe_enum_name(FakeEnum()) == "TEST_VALUE"

    def test_without_name_attr(self):
        from extractor import _safe_enum_name
        assert _safe_enum_name(42) == "42"


class TestAlignmentName:
    def test_none(self):
        from extractor import _alignment_name
        assert _alignment_name(None) == ""

    def test_left(self):
        from extractor import _alignment_name
        from pptx.enum.text import PP_ALIGN
        assert _alignment_name(PP_ALIGN.LEFT) == "left"

    def test_center(self):
        from extractor import _alignment_name
        from pptx.enum.text import PP_ALIGN
        assert _alignment_name(PP_ALIGN.CENTER) == "center"

    def test_right(self):
        from extractor import _alignment_name
        from pptx.enum.text import PP_ALIGN
        assert _alignment_name(PP_ALIGN.RIGHT) == "right"

    def test_justify(self):
        from extractor import _alignment_name
        from pptx.enum.text import PP_ALIGN
        assert _alignment_name(PP_ALIGN.JUSTIFY) == "justify"
