"""pptx-creator/scripts/rich_elements.py の単体テスト"""
import pytest


class TestImport:
    def test_import_module(self):
        from rich_elements import rel, hex_to_rgb


class TestRel:
    def test_zero(self):
        from rich_elements import rel
        assert rel(0.0, 10000) == 0

    def test_full(self):
        from rich_elements import rel
        assert rel(1.0, 10000) == 10000

    def test_half(self):
        from rich_elements import rel
        assert rel(0.5, 10000) == 5000

    def test_quarter(self):
        from rich_elements import rel
        assert rel(0.25, 12192000) == 3048000

    def test_returns_int(self):
        from rich_elements import rel
        result = rel(0.333, 10000)
        assert isinstance(result, int)


class TestHexToRgb:
    def test_basic(self):
        from rich_elements import hex_to_rgb
        from pptx.dml.color import RGBColor
        result = hex_to_rgb("4472C4")
        assert isinstance(result, RGBColor)

    def test_with_hash(self):
        from rich_elements import hex_to_rgb
        result = hex_to_rgb("#FF0000")
        # Red
        assert result[0] == 255
        assert result[1] == 0
        assert result[2] == 0

    def test_black(self):
        from rich_elements import hex_to_rgb
        result = hex_to_rgb("000000")
        assert result[0] == 0
        assert result[1] == 0
        assert result[2] == 0

    def test_white(self):
        from rich_elements import hex_to_rgb
        result = hex_to_rgb("FFFFFF")
        assert result[0] == 255
        assert result[1] == 255
        assert result[2] == 255
