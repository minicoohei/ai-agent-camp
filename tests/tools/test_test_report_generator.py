"""test_report_generator.py の単体テスト。

pytest HTMLレポートからのサマリー抽出・Markdown生成を検証する。
"""

import sys
from pathlib import Path

import pytest

from tests.conftest import import_module_from_repo


@pytest.fixture
def mod():
    return import_module_from_repo("test_report_generator", "tools/test_report_generator.py")


# ===========================================================================
# extract_summary_from_html
# ===========================================================================

class TestExtractSummaryFromHtml:
    def test_full_report(self, mod):
        html = """
        <div>10 passed, 2 failed, 1 skipped, 0 error in 3.45 seconds</div>
        """
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 10
        assert result["failed"] == 2
        assert result["skipped"] == 1
        assert result["errors"] == 0
        assert result["total"] == 13
        assert "3.45" in result["duration"]

    def test_empty_html(self, mod):
        result = mod.extract_summary_from_html("")
        assert result["total"] == 0
        assert result["passed"] == 0
        assert result["failed"] == 0
        assert result["duration"] == "N/A"

    def test_only_passed(self, mod):
        html = "<p>5 passed</p>"
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 5
        assert result["total"] == 5
        assert result["failed"] == 0

    def test_only_failed(self, mod):
        html = "<p>3 failed</p>"
        result = mod.extract_summary_from_html(html)
        assert result["failed"] == 3
        assert result["total"] == 3

    def test_only_skipped(self, mod):
        html = "<p>7 skipped</p>"
        result = mod.extract_summary_from_html(html)
        assert result["skipped"] == 7

    def test_singular_error(self, mod):
        """'error' (singular) も検出する"""
        html = "<p>1 error</p>"
        result = mod.extract_summary_from_html(html)
        assert result["errors"] == 1

    def test_plural_seconds(self, mod):
        html = "<p>100 passed in 12.5 seconds</p>"
        result = mod.extract_summary_from_html(html)
        assert "12.5" in result["duration"]

    def test_singular_second(self, mod):
        html = "<p>1 passed in 0.5 second</p>"
        result = mod.extract_summary_from_html(html)
        assert "0.5" in result["duration"]

    def test_large_numbers(self, mod):
        """大きな数値"""
        html = "<p>1000 passed, 500 failed, 100 skipped in 999.99 seconds</p>"
        result = mod.extract_summary_from_html(html)
        assert result["total"] == 1600
        assert result["passed"] == 1000

    def test_zero_results(self, mod):
        html = "<p>0 passed, 0 failed, 0 skipped</p>"
        result = mod.extract_summary_from_html(html)
        assert result["total"] == 0

    def test_html_with_tags(self, mod):
        """HTMLタグを含む"""
        html = '<span class="passed">42 passed</span><span>1 failed</span>'
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 42
        assert result["failed"] == 1

    def test_malformed_html(self, mod):
        """壊れたHTML"""
        html = "<<<not really html>>>"
        result = mod.extract_summary_from_html(html)
        assert result["total"] == 0

    def test_special_characters(self, mod):
        """特殊文字含み"""
        html = "結果: 5 passed & 2 failed <in> 1.0 seconds"
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 5
        assert result["failed"] == 2


# ===========================================================================
# generate_markdown
# ===========================================================================

class TestGenerateMarkdown:
    def test_all_passed(self, mod):
        summary = {"total": 10, "passed": 10, "failed": 0, "skipped": 0, "errors": 0, "duration": "1.5 秒"}
        md = mod.generate_markdown(summary, "report.html")
        assert "# 単体テスト実行レポート" in md
        assert "10" in md
        assert "100.0%" in md
        assert "PASS" in md
        assert "report.html" in md

    def test_with_failures(self, mod):
        summary = {"total": 10, "passed": 8, "failed": 2, "skipped": 0, "errors": 0, "duration": "2.0 秒"}
        md = mod.generate_markdown(summary, "report.html")
        assert "FAIL" in md
        assert "80.0%" in md

    def test_with_errors(self, mod):
        summary = {"total": 5, "passed": 3, "failed": 0, "skipped": 1, "errors": 1, "duration": "N/A"}
        md = mod.generate_markdown(summary, "input.html")
        assert "FAIL" in md

    def test_zero_total_no_division_error(self, mod):
        """total=0 でもゼロ除算しない"""
        summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0, "duration": "N/A"}
        md = mod.generate_markdown(summary, "empty.html")
        assert "0.0%" in md
        # total=0 → total becomes 1 internally → 0/1 = 0%

    def test_markdown_table_structure(self, mod):
        summary = {"total": 1, "passed": 1, "failed": 0, "skipped": 0, "errors": 0, "duration": "0.1 秒"}
        md = mod.generate_markdown(summary, "test.html")
        assert "| 項目 | 結果 |" in md
        assert "実行テスト数" in md


# ===========================================================================
# main (integration via file)
# ===========================================================================

class TestMain:
    def test_file_not_found(self, mod, tmp_path):
        with pytest.raises(SystemExit) as exc_info:
            with __import__("unittest.mock", fromlist=["patch"]).patch(
                "sys.argv", ["prog", "--input", str(tmp_path / "nonexistent.html")]
            ):
                mod.main()
        assert exc_info.value.code == 1

    def test_output_to_file(self, mod, tmp_path):
        html_file = tmp_path / "report.html"
        html_file.write_text("10 passed, 0 failed in 1.0 seconds")
        out_file = tmp_path / "summary.md"

        with __import__("unittest.mock", fromlist=["patch"]).patch(
            "sys.argv", ["prog", "--input", str(html_file), "--output", str(out_file)]
        ):
            mod.main()

        assert out_file.exists()
        content = out_file.read_text()
        assert "PASS" in content

    def test_output_to_stdout(self, mod, tmp_path, capsys):
        html_file = tmp_path / "report.html"
        html_file.write_text("5 passed, 1 failed")

        with __import__("unittest.mock", fromlist=["patch"]).patch(
            "sys.argv", ["prog", "-i", str(html_file)]
        ):
            mod.main()

        captured = capsys.readouterr()
        assert "FAIL" in captured.out

    def test_output_dir_created(self, mod, tmp_path):
        html_file = tmp_path / "report.html"
        html_file.write_text("3 passed")
        out_file = tmp_path / "sub" / "dir" / "summary.md"

        with __import__("unittest.mock", fromlist=["patch"]).patch(
            "sys.argv", ["prog", "-i", str(html_file), "-o", str(out_file)]
        ):
            mod.main()

        assert out_file.exists()


# ===========================================================================
# Boundary
# ===========================================================================

class TestBoundary:
    def test_very_long_html(self, mod):
        """非常に長いHTML"""
        html = "prefix " * 10000 + " 42 passed " + " suffix" * 10000
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 42

    def test_newlines_in_html(self, mod):
        """改行を含むHTML"""
        html = "results:\n  10 passed\n  2 failed\n  in 5.0 seconds"
        result = mod.extract_summary_from_html(html)
        assert result["passed"] == 10
        assert result["failed"] == 2
