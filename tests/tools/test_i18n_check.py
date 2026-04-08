"""i18n_check.py の単体テスト"""
import re
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestCodeContextTracker:
    def test_import(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert not tracker.is_inside("<p>普通のテキスト</p>")

    def test_pre_block(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<pre>")
        assert tracker.is_inside("コード内テキスト")
        assert tracker.is_inside("</pre>")
        assert not tracker.is_inside("<p>普通のテキスト</p>")

    def test_script_block(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<script>")
        assert tracker.is_inside("var x = 'テスト';")
        assert tracker.is_inside("</script>")
        assert not tracker.is_inside("<p>外</p>")

    def test_style_block(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<style>")
        assert tracker.is_inside(".class { color: red; }")
        assert tracker.is_inside("</style>")
        assert not tracker.is_inside("<p>外</p>")

    def test_nested_blocks(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<pre>")
        assert tracker.is_inside("<code>")
        assert tracker.is_inside("ネスト内")
        assert tracker.is_inside("</code>")
        assert tracker.is_inside("まだpre内")
        assert tracker.is_inside("</pre>")
        assert not tracker.is_inside("<p>外</p>")

    def test_same_line_open_close(self):
        """同一行に<pre>...</pre>がある場合の処理 (I7 fix)"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<pre>console.log('test')</pre>")
        assert not tracker.is_inside("<p>通常テキスト</p>")

    def test_close_then_open_same_line(self):
        """同一行に</pre><pre>がある場合 (I7 fix)"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        tracker.is_inside("<pre>")
        tracker.is_inside("コード")
        result = tracker.is_inside("</pre><pre>")
        assert result
        assert tracker.is_inside("新しいコード")

    def test_html_comment_single_line(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<!-- コメント -->")
        assert not tracker.is_inside("<p>通常</p>")

    def test_html_comment_multiline(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<!-- 開始")
        assert tracker.is_inside("コメント内")
        assert tracker.is_inside("終了 -->")
        assert not tracker.is_inside("<p>通常</p>")

    def test_code_fence(self):
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("```python")

    def test_code_inline_not_skipped(self):
        """インライン <code> は行全体をスキップしない（regexで部分除去される）"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert not tracker.is_inside("<code>x = 1</code>")
        assert not tracker.is_inside("<p>外</p>")

    def test_code_block_multiline(self):
        """複数行にまたがる <code> ブロックは内部行をスキップする"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert tracker.is_inside("<code>")       # 開始行: in_code=1 → inside
        assert tracker.is_inside("  x = 1")      # 内部行: was_inside → inside
        assert tracker.is_inside("</code>")      # 終了行: was_inside → inside
        assert not tracker.is_inside("<p>外</p>") # 外部: 通常テキスト


class TestResidueDetectionFlow:
    """tracker.is_inside() + regex strip を組み合わせたE2Eテスト。

    check_original_text_residue() の検出フローを模擬:
    1. tracker.is_inside(line) → True なら行全体スキップ
    2. False なら inline code を regex で除去
    3. HTML タグを除去
    4. 残ったテキストで日本語を検出
    """

    RE_JAPANESE = re.compile(r"[\u3040-\u309F\u30A0-\u30FF]")

    def _detect_japanese(self, line: str, tracker) -> bool:
        """check_original_text_residue のコアロジックを簡略再現"""
        if tracker.is_inside(line):
            return False  # スキップ = 日本語検出なし
        # inline code/pre/kbd/samp を除去
        text = re.sub(
            r"<(code|pre|kbd|samp)[^>]*>.*?</\1>", " ",
            line, flags=re.DOTALL,
        )
        # HTMLタグを除去
        text = re.sub(r"<[^>]+>", " ", text)
        return bool(self.RE_JAPANESE.search(text))

    def test_inline_code_with_japanese_detected(self):
        """インライン <code> がある行でもコード外の日本語は検出される"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        line = '<p>これは<code>pip install</code>の例です</p>'
        assert self._detect_japanese(line, tracker)

    def test_inline_code_only_no_japanese(self):
        """インライン <code> のみでコード外に日本語がなければ検出されない"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        line = '<p>Use <code>pip install</code> to install</p>'
        assert not self._detect_japanese(line, tracker)

    def test_multiple_inline_codes_with_japanese(self):
        """複数 <code> がある行でもコード外の日本語は検出される"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        line = (
            '<p><code>/guide</code>, <code>/help</code>'
            ' でガイドを表示</p>'
        )
        assert self._detect_japanese(line, tracker)

    def test_pre_same_line_skipped(self):
        """<pre>...</pre> 同一行はスキップされる（コード内容は検出しない）"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        line = '<pre>日本語のコード例</pre>'
        assert not self._detect_japanese(line, tracker)

    def test_pre_block_then_normal_line(self):
        """<pre> ブロック後の通常行は正しく検出される"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert not self._detect_japanese("<pre>", tracker)
        assert not self._detect_japanese("コード内", tracker)
        assert not self._detect_japanese("</pre>", tracker)
        assert self._detect_japanese("<p>翻訳漏れ</p>", tracker)

    def test_script_block_skipped(self):
        """<script> ブロック内は全行スキップ"""
        from i18n_check import _CodeContextTracker
        tracker = _CodeContextTracker()
        assert not self._detect_japanese("<script>", tracker)
        assert not self._detect_japanese("var msg = 'テスト';", tracker)
        assert not self._detect_japanese("</script>", tracker)
        assert self._detect_japanese("<p>ここは検出</p>", tracker)


# ===================================================================
# Issue / CheckResult テスト
# ===================================================================

class TestIssue:
    def test_creation(self):
        from i18n_check import Issue
        issue = Issue("test.html", 10, "Japanese text found")
        assert issue.file == "test.html"
        assert issue.line == 10
        assert issue.message == "Japanese text found"
        assert issue.severity == "FAIL"

    def test_warn_severity(self):
        from i18n_check import Issue
        issue = Issue("test.html", None, "warning", severity="WARN")
        assert issue.severity == "WARN"

    def test_to_dict(self):
        from i18n_check import Issue
        issue = Issue("test.html", 5, "msg", severity="FAIL")
        d = issue.to_dict()
        assert d["file"] == "test.html"
        assert d["line"] == 5
        assert d["message"] == "msg"
        assert d["severity"] == "FAIL"

    def test_to_dict_no_line(self):
        from i18n_check import Issue
        issue = Issue("test.html", None, "msg")
        d = issue.to_dict()
        assert "line" not in d

    def test_repr(self):
        from i18n_check import Issue
        issue = Issue("test.html", 10, "msg")
        r = repr(issue)
        assert "test.html:10" in r

    def test_repr_no_line(self):
        from i18n_check import Issue
        issue = Issue("test.html", None, "msg")
        r = repr(issue)
        assert "test.html" in r


class TestCheckResult:
    def test_creation(self):
        from i18n_check import CheckResult
        cr = CheckResult("test_check")
        assert cr.name == "test_check"
        assert cr.status == "PASS"
        assert cr.total == 0
        assert cr.passed == 0
        assert cr.issues == []

    def test_add_fail_issue(self):
        from i18n_check import CheckResult, Issue
        cr = CheckResult("test_check")
        cr.add_issue(Issue("f.html", 1, "err", severity="FAIL"))
        assert cr.status == "FAIL"
        assert len(cr.issues) == 1

    def test_add_warn_issue(self):
        from i18n_check import CheckResult, Issue
        cr = CheckResult("test_check")
        cr.add_issue(Issue("f.html", 1, "warn", severity="WARN"))
        assert cr.status == "WARN"

    def test_fail_overrides_warn(self):
        from i18n_check import CheckResult, Issue
        cr = CheckResult("test_check")
        cr.add_issue(Issue("f.html", 1, "warn", severity="WARN"))
        cr.add_issue(Issue("f.html", 2, "err", severity="FAIL"))
        assert cr.status == "FAIL"

    def test_to_dict(self):
        from i18n_check import CheckResult, Issue
        cr = CheckResult("test_check")
        cr.total = 3
        cr.passed = 2
        cr.add_issue(Issue("f.html", 1, "err"))
        d = cr.to_dict()
        assert d["name"] == "test_check"
        assert d["total"] == 3
        assert d["passed"] == 2
        assert len(d["issues"]) == 1


# ===================================================================
# Helpers テスト
# ===================================================================

class TestCollectHtmlFiles:
    def test_finds_html_recursively(self, tmp_path):
        from i18n_check import _collect_html_files
        (tmp_path / "index.html").write_text("<html></html>", encoding="utf-8")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "page.html").write_text("<html></html>", encoding="utf-8")
        files = _collect_html_files(tmp_path)
        assert len(files) == 2

    def test_empty_dir(self, tmp_path):
        from i18n_check import _collect_html_files
        files = _collect_html_files(tmp_path)
        assert files == []


class TestRelative:
    def test_relative_path(self, tmp_path):
        from i18n_check import _relative
        path = tmp_path / "sub" / "file.html"
        result = _relative(path, tmp_path)
        assert result == "sub/file.html"

    def test_unrelated_path(self):
        from i18n_check import _relative
        result = _relative(Path("/a/b/c"), Path("/x/y"))
        assert "/a/b/c" in result


class TestParseHtml:
    def test_valid_html(self, tmp_path):
        from i18n_check import _parse_html
        f = tmp_path / "test.html"
        f.write_text("<html><body><p>Hello</p></body></html>", encoding="utf-8")
        soup = _parse_html(f)
        assert soup is not None
        assert soup.find("p").string == "Hello"

    def test_invalid_path(self):
        from i18n_check import _parse_html
        result = _parse_html(Path("/nonexistent/file.html"))
        assert result is None


class TestReadLines:
    def test_reads_lines(self, tmp_path):
        from i18n_check import _read_lines
        f = tmp_path / "test.txt"
        f.write_text("line1\nline2\nline3", encoding="utf-8")
        lines = _read_lines(f)
        assert len(lines) == 3

    def test_nonexistent(self):
        from i18n_check import _read_lines
        lines = _read_lines(Path("/nonexistent"))
        assert lines == []


class TestIsInsideCodeContext:
    def test_code_fence(self):
        from i18n_check import _is_inside_code_context
        assert _is_inside_code_context("```python") is True

    def test_pre_tag(self):
        from i18n_check import _is_inside_code_context
        assert _is_inside_code_context("<pre>code here</pre>") is True

    def test_normal_text(self):
        from i18n_check import _is_inside_code_context
        assert _is_inside_code_context("<p>Normal text</p>") is False


class TestExtractJapaneseSnippet:
    def test_finds_snippet(self):
        from i18n_check import _extract_japanese_snippet, RE_JAPANESE_ALL
        text = "This is テスト text"
        snippet = _extract_japanese_snippet(text, RE_JAPANESE_ALL)
        assert snippet is not None
        assert "テスト" in snippet

    def test_no_match(self):
        from i18n_check import _extract_japanese_snippet, RE_JAPANESE_ALL
        text = "No Japanese here"
        snippet = _extract_japanese_snippet(text, RE_JAPANESE_ALL)
        assert snippet is None

    def test_context_chars(self):
        from i18n_check import _extract_japanese_snippet, RE_JAPANESE_ALL
        text = "A" * 100 + "テスト" + "B" * 100
        snippet = _extract_japanese_snippet(text, RE_JAPANESE_ALL, context_chars=5)
        assert snippet is not None
        assert len(snippet) < 50  # Should be limited


class TestIsExcludedJapaneseContext:
    def test_inside_code(self):
        from i18n_check import _is_excluded_japanese_context
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<code><span>テスト</span></code>", "html.parser")
        span = soup.find("span")
        assert _is_excluded_japanese_context(span) is True

    def test_inside_pre(self):
        from i18n_check import _is_excluded_japanese_context
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<pre><span>テスト</span></pre>", "html.parser")
        span = soup.find("span")
        assert _is_excluded_japanese_context(span) is True

    def test_normal_context(self):
        from i18n_check import _is_excluded_japanese_context
        from bs4 import BeautifulSoup
        soup = BeautifulSoup("<p><span>テスト</span></p>", "html.parser")
        span = soup.find("span")
        assert _is_excluded_japanese_context(span) is False


class TestResolveLink:
    def test_external_url(self, tmp_path):
        from i18n_check import _resolve_link
        result = _resolve_link("https://example.com", tmp_path / "index.html", tmp_path)
        assert result is None

    def test_anchor(self, tmp_path):
        from i18n_check import _resolve_link
        result = _resolve_link("#section", tmp_path / "index.html", tmp_path)
        assert result is None

    def test_javascript(self, tmp_path):
        from i18n_check import _resolve_link
        result = _resolve_link("javascript:void(0)", tmp_path / "index.html", tmp_path)
        assert result is None

    def test_relative_link(self, tmp_path):
        from i18n_check import _resolve_link
        html_file = tmp_path / "dir" / "page.html"
        result = _resolve_link("other.html", html_file, tmp_path)
        assert result is not None
        assert str(result).endswith("other.html")

    def test_empty_href(self, tmp_path):
        from i18n_check import _resolve_link
        result = _resolve_link("", tmp_path / "index.html", tmp_path)
        assert result is None

    def test_strip_fragment_and_query(self, tmp_path):
        from i18n_check import _resolve_link
        result = _resolve_link("page.html?v=1#top", tmp_path / "index.html", tmp_path)
        assert result is not None
        assert "?" not in str(result)


# ===================================================================
# Check functions テスト
# ===================================================================

class TestCheckLangAttribute:
    def test_correct_lang(self, tmp_path):
        from i18n_check import check_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<html lang="en"><body></body></html>', encoding="utf-8")
        result = check_lang_attribute("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_wrong_lang(self, tmp_path):
        from i18n_check import check_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<html lang="ja"><body></body></html>', encoding="utf-8")
        result = check_lang_attribute("en", tmp_path, [f])
        assert result.status == "FAIL"
        assert len(result.issues) == 1

    def test_no_html_tag(self, tmp_path):
        from i18n_check import check_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<body>No html tag</body>', encoding="utf-8")
        result = check_lang_attribute("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_parse_error(self, tmp_path):
        from i18n_check import check_lang_attribute
        f = tmp_path / "bad.html"
        # Create file that returns None from _parse_html
        with patch("i18n_check._parse_html", return_value=None):
            result = check_lang_attribute("en", tmp_path, [f])
            assert result.status == "FAIL"


class TestCheckCharset:
    def test_correct_charset(self, tmp_path):
        from i18n_check import check_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        result = check_charset("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_missing_charset(self, tmp_path):
        from i18n_check import check_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head></head></html>', encoding="utf-8")
        result = check_charset("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_wrong_charset(self, tmp_path):
        from i18n_check import check_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head><meta charset="ISO-8859-1"></head></html>', encoding="utf-8")
        result = check_charset("en", tmp_path, [f])
        assert result.status == "FAIL"


class TestCheckAltAttributes:
    def test_no_images(self, tmp_path):
        from i18n_check import check_alt_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><p>No images</p></body></html>', encoding="utf-8")
        result = check_alt_attributes("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.total == 0

    def test_correct_alt(self, tmp_path):
        from i18n_check import check_alt_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><img src="img.png" alt="A picture"></body></html>', encoding="utf-8")
        result = check_alt_attributes("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_missing_alt(self, tmp_path):
        from i18n_check import check_alt_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><img src="img.png"></body></html>', encoding="utf-8")
        result = check_alt_attributes("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_japanese_alt(self, tmp_path):
        from i18n_check import check_alt_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><img src="img.png" alt="テスト画像"></body></html>', encoding="utf-8")
        result = check_alt_attributes("en", tmp_path, [f])
        assert result.status == "FAIL"


class TestCheckTitleAttributes:
    def test_no_titles(self, tmp_path):
        from i18n_check import check_title_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><p>No titles</p></body></html>', encoding="utf-8")
        result = check_title_attributes("en", tmp_path, [f])
        assert result.status == "PASS"

    def test_english_title(self, tmp_path):
        from i18n_check import check_title_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><a href="#" title="Click me">Link</a></body></html>', encoding="utf-8")
        result = check_title_attributes("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_japanese_title(self, tmp_path):
        from i18n_check import check_title_attributes
        f = tmp_path / "test.html"
        f.write_text('<html><body><a href="#" title="クリック">Link</a></body></html>', encoding="utf-8")
        result = check_title_attributes("en", tmp_path, [f])
        assert result.status == "FAIL"


class TestCheckMetaTags:
    def test_no_meta(self, tmp_path):
        from i18n_check import check_meta_tags
        f = tmp_path / "test.html"
        f.write_text('<html><head></head><body></body></html>', encoding="utf-8")
        result = check_meta_tags("en", tmp_path, [f])
        assert result.status == "PASS"

    def test_english_title(self, tmp_path):
        from i18n_check import check_meta_tags
        f = tmp_path / "test.html"
        f.write_text('<html><head><title>English Title</title></head></html>', encoding="utf-8")
        result = check_meta_tags("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_japanese_title(self, tmp_path):
        from i18n_check import check_meta_tags
        f = tmp_path / "test.html"
        f.write_text('<html><head><title>日本語タイトル</title></head></html>', encoding="utf-8")
        result = check_meta_tags("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_japanese_meta_description(self, tmp_path):
        from i18n_check import check_meta_tags
        f = tmp_path / "test.html"
        f.write_text(
            '<html><head><meta name="description" content="日本語の説明"></head></html>',
            encoding="utf-8",
        )
        result = check_meta_tags("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_og_tag_translated(self, tmp_path):
        from i18n_check import check_meta_tags
        f = tmp_path / "test.html"
        f.write_text(
            '<html><head><meta property="og:title" content="English OG Title"></head></html>',
            encoding="utf-8",
        )
        result = check_meta_tags("en", tmp_path, [f])
        assert result.status == "PASS"


class TestCheckOriginalTextResidue:
    def test_clean_english(self, tmp_path):
        from i18n_check import check_original_text_residue
        f = tmp_path / "test.html"
        f.write_text(
            '<html lang="en"><body><p>All English text here</p></body></html>',
            encoding="utf-8",
        )
        result = check_original_text_residue("en", tmp_path, [f])
        assert result.passed == 1

    def test_japanese_residue(self, tmp_path):
        from i18n_check import check_original_text_residue
        f = tmp_path / "test.html"
        f.write_text(
            '<html lang="en"><body><p>This has 日本語 residue</p></body></html>',
            encoding="utf-8",
        )
        result = check_original_text_residue("en", tmp_path, [f])
        assert result.status == "FAIL"
        assert len(result.issues) >= 1

    def test_code_block_ignored(self, tmp_path):
        from i18n_check import check_original_text_residue
        f = tmp_path / "test.html"
        f.write_text(
            '<html lang="en"><body><pre>日本語のコード</pre><p>Clean English</p></body></html>',
            encoding="utf-8",
        )
        result = check_original_text_residue("en", tmp_path, [f])
        assert result.passed == 1

    def test_es_detects_hiragana_katakana(self, tmp_path):
        """ES言語ではひらがな・カタカナを検出"""
        from i18n_check import check_original_text_residue
        f = tmp_path / "test.html"
        f.write_text(
            '<html lang="es"><body><p>こんにちは katakana カタカナ</p></body></html>',
            encoding="utf-8",
        )
        result = check_original_text_residue("es", tmp_path, [f])
        assert result.status == "FAIL"


class TestRegexPatterns:
    """正規表現パターンの基本テスト"""

    def test_hiragana_pattern(self):
        from i18n_check import RE_HIRAGANA
        assert RE_HIRAGANA.search("あいう")
        assert not RE_HIRAGANA.search("ABC")

    def test_katakana_pattern(self):
        from i18n_check import RE_KATAKANA
        assert RE_KATAKANA.search("アイウ")
        assert not RE_KATAKANA.search("ABC")

    def test_kanji_pattern(self):
        from i18n_check import RE_KANJI
        assert RE_KANJI.search("漢字")
        assert not RE_KANJI.search("ABC")

    def test_template_var_pattern(self):
        from i18n_check import RE_TEMPLATE_VAR
        assert RE_TEMPLATE_VAR.search("{{PLACEHOLDER}}")
        assert not RE_TEMPLATE_VAR.search("{{lowercase}}")


# ===================================================================
# check_aria_labels
# ===================================================================

class TestCheckAriaLabels:
    def test_no_aria_labels(self, tmp_path):
        from i18n_check import check_aria_labels
        f = tmp_path / "test.html"
        f.write_text('<html><body><p>No aria</p></body></html>', encoding="utf-8")
        result = check_aria_labels("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.total == 0

    def test_english_aria_label(self, tmp_path):
        from i18n_check import check_aria_labels
        f = tmp_path / "test.html"
        f.write_text('<html><body><button aria-label="Close">X</button></body></html>', encoding="utf-8")
        result = check_aria_labels("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_japanese_aria_label(self, tmp_path):
        from i18n_check import check_aria_labels
        f = tmp_path / "test.html"
        f.write_text('<html><body><button aria-label="閉じる">X</button></body></html>', encoding="utf-8")
        result = check_aria_labels("en", tmp_path, [f])
        assert result.status == "FAIL"


# ===================================================================
# check_placeholders
# ===================================================================

class TestCheckPlaceholders:
    def test_no_placeholders(self, tmp_path):
        from i18n_check import check_placeholders
        f = tmp_path / "test.html"
        f.write_text('<html><body><input type="text"></body></html>', encoding="utf-8")
        result = check_placeholders("en", tmp_path, [f])
        assert result.status == "PASS"

    def test_english_placeholder(self, tmp_path):
        from i18n_check import check_placeholders
        f = tmp_path / "test.html"
        f.write_text('<html><body><input placeholder="Search..."></body></html>', encoding="utf-8")
        result = check_placeholders("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_japanese_placeholder(self, tmp_path):
        from i18n_check import check_placeholders
        f = tmp_path / "test.html"
        f.write_text('<html><body><input placeholder="検索..."></body></html>', encoding="utf-8")
        result = check_placeholders("en", tmp_path, [f])
        assert result.status == "FAIL"


# ===================================================================
# check_internal_links
# ===================================================================

class TestCheckInternalLinks:
    def test_valid_link(self, tmp_path):
        from i18n_check import check_internal_links
        f = tmp_path / "index.html"
        target = tmp_path / "page.html"
        target.write_text("<html></html>", encoding="utf-8")
        f.write_text('<html><body><a href="page.html">Link</a></body></html>', encoding="utf-8")
        result = check_internal_links("en", tmp_path, [f])
        assert result.passed >= 1

    def test_broken_link(self, tmp_path):
        from i18n_check import check_internal_links
        f = tmp_path / "index.html"
        f.write_text('<html><body><a href="missing.html">Link</a></body></html>', encoding="utf-8")
        result = check_internal_links("en", tmp_path, [f])
        assert result.status == "FAIL"

    def test_external_link_ignored(self, tmp_path):
        from i18n_check import check_internal_links
        f = tmp_path / "index.html"
        f.write_text('<html><body><a href="https://example.com">Link</a></body></html>', encoding="utf-8")
        result = check_internal_links("en", tmp_path, [f])
        assert result.total == 0

    def test_lang_btn_skipped(self, tmp_path):
        from i18n_check import check_internal_links
        f = tmp_path / "index.html"
        f.write_text('<html><body><a href="../ja/page.html" class="lang-btn">JA</a></body></html>', encoding="utf-8")
        result = check_internal_links("en", tmp_path, [f])
        assert result.total == 0

    def test_link_escapes_lang_dir(self, tmp_path):
        from i18n_check import check_internal_links
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "index.html"
        # Create a file outside lang_dir
        outside = tmp_path / "outside.html"
        outside.write_text("<html></html>", encoding="utf-8")
        f.write_text('<html><body><a href="../outside.html">Link</a></body></html>', encoding="utf-8")
        result = check_internal_links("en", lang_dir, [f])
        assert any("escapes" in i.message for i in result.issues) or result.status == "FAIL"


# ===================================================================
# check_nav_links
# ===================================================================

class TestCheckNavLinks:
    def test_no_nav_links(self, tmp_path):
        from i18n_check import check_nav_links
        f = tmp_path / "test.html"
        f.write_text('<html><body><a href="page.html">Normal link</a></body></html>', encoding="utf-8")
        result = check_nav_links("en", tmp_path, [f])
        assert result.total == 0

    def test_nav_link_with_rel(self, tmp_path):
        from i18n_check import check_nav_links
        f = tmp_path / "test.html"
        target = tmp_path / "next.html"
        target.write_text("<html></html>", encoding="utf-8")
        f.write_text('<html><body><a href="next.html" rel="next">Next</a></body></html>', encoding="utf-8")
        result = check_nav_links("en", tmp_path, [f])
        assert result.passed >= 1

    def test_nav_link_with_class(self, tmp_path):
        from i18n_check import check_nav_links
        f = tmp_path / "test.html"
        target = tmp_path / "next.html"
        target.write_text("<html></html>", encoding="utf-8")
        f.write_text('<html><body><a href="next.html" class="nav-next">Next</a></body></html>', encoding="utf-8")
        result = check_nav_links("en", tmp_path, [f])
        assert result.passed >= 1

    def test_nav_link_by_text(self, tmp_path):
        from i18n_check import check_nav_links
        f = tmp_path / "test.html"
        target = tmp_path / "next.html"
        target.write_text("<html></html>", encoding="utf-8")
        f.write_text('<html><body><a href="next.html">Next Page</a></body></html>', encoding="utf-8")
        result = check_nav_links("en", tmp_path, [f])
        assert result.total >= 1

    def test_broken_nav_link(self, tmp_path):
        from i18n_check import check_nav_links
        f = tmp_path / "test.html"
        f.write_text('<html><body><a href="missing.html" rel="next">Next</a></body></html>', encoding="utf-8")
        result = check_nav_links("en", tmp_path, [f])
        assert result.status == "FAIL"


# ===================================================================
# check_image_references
# ===================================================================

class TestCheckImageReferences:
    def test_valid_image(self, tmp_path):
        from i18n_check import check_image_references
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        img = lang_dir / "img.png"
        img.write_bytes(b"\x89PNG")
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="img.png"></body></html>', encoding="utf-8")
        result = check_image_references("en", lang_dir, [f])
        assert result.passed >= 1

    def test_missing_image(self, tmp_path):
        from i18n_check import check_image_references
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="missing.png"></body></html>', encoding="utf-8")
        result = check_image_references("en", lang_dir, [f])
        assert result.status == "FAIL"

    def test_data_uri_ignored(self, tmp_path):
        from i18n_check import check_image_references
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="data:image/png;base64,xxx"></body></html>', encoding="utf-8")
        result = check_image_references("en", lang_dir, [f])
        assert result.total == 0

    def test_external_url_ignored(self, tmp_path):
        from i18n_check import check_image_references
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="https://example.com/img.png"></body></html>', encoding="utf-8")
        result = check_image_references("en", lang_dir, [f])
        assert result.total == 0


# ===================================================================
# check_template_vars
# ===================================================================

class TestCheckTemplateVars:
    def test_clean_file(self, tmp_path):
        from i18n_check import check_template_vars
        f = tmp_path / "test.html"
        f.write_text('<html><body>No templates</body></html>', encoding="utf-8")
        result = check_template_vars("en", tmp_path, [f])
        assert result.status == "PASS"
        assert result.passed == 1

    def test_unprocessed_var(self, tmp_path):
        from i18n_check import check_template_vars
        f = tmp_path / "test.html"
        f.write_text('<html><body>Hello {{USER_NAME}}</body></html>', encoding="utf-8")
        result = check_template_vars("en", tmp_path, [f])
        assert result.status == "FAIL"
        assert any("USER_NAME" in i.message for i in result.issues)


# ===================================================================
# check_css_loading
# ===================================================================

class TestCheckCssLoading:
    def test_valid_css(self, tmp_path):
        from i18n_check import check_css_loading
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        css = lang_dir / "style.css"
        css.write_text("body {}", encoding="utf-8")
        f = lang_dir / "test.html"
        f.write_text('<html><head><link rel="stylesheet" href="style.css"></head></html>', encoding="utf-8")
        result = check_css_loading("en", lang_dir, [f])
        assert result.passed >= 1

    def test_missing_css(self, tmp_path):
        from i18n_check import check_css_loading
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><head><link rel="stylesheet" href="missing.css"></head></html>', encoding="utf-8")
        result = check_css_loading("en", lang_dir, [f])
        assert result.status == "FAIL"

    def test_cdn_css_ignored(self, tmp_path):
        from i18n_check import check_css_loading
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><head><link rel="stylesheet" href="https://cdn.example.com/style.css"></head></html>', encoding="utf-8")
        result = check_css_loading("en", lang_dir, [f])
        assert result.total == 0


# ===================================================================
# check_relative_paths
# ===================================================================

class TestCheckRelativePaths:
    def test_internal_path(self, tmp_path):
        from i18n_check import check_relative_paths
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        target = lang_dir / "page.html"
        target.write_text("<html></html>", encoding="utf-8")
        f = lang_dir / "test.html"
        f.write_text('<html><body><a href="page.html">Link</a></body></html>', encoding="utf-8")
        result = check_relative_paths("en", lang_dir, [f])
        assert result.passed >= 1

    def test_escaping_path(self, tmp_path):
        from i18n_check import check_relative_paths
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        outside = tmp_path / "outside.html"
        outside.write_text("<html></html>", encoding="utf-8")
        f = lang_dir / "test.html"
        f.write_text('<html><body><a href="../outside.html">Link</a></body></html>', encoding="utf-8")
        result = check_relative_paths("en", lang_dir, [f])
        assert any("escapes" in i.message for i in result.issues)


# ===================================================================
# check_translation_coverage
# ===================================================================

class TestCheckTranslationCoverage:
    def test_full_coverage(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text('{"key1": "val1", "key2": "val2"}', encoding="utf-8")
        (locales / "en.json").write_text('{"key1": "val1", "key2": "val2"}', encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            result = check_translation_coverage("en", tmp_path, [])
        assert result.passed == 2
        assert result.status == "PASS"

    def test_missing_keys(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text('{"key1": "val1", "key2": "val2", "key3": "val3"}', encoding="utf-8")
        (locales / "en.json").write_text('{"key1": "val1"}', encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            result = check_translation_coverage("en", tmp_path, [])
        assert result.status == "WARN"
        assert result.passed == 1

    def test_no_ja_json(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        with patch("i18n_check.LOCALES_DIR", locales):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                result = check_translation_coverage("en", tmp_path, [])
        assert result.status == "WARN"

    def test_no_lang_json(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text('{"key1": "val1"}', encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                result = check_translation_coverage("en", tmp_path, [])
        assert result.status == "WARN"

    def test_nested_keys(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text('{"section": {"key1": "val1", "key2": "val2"}}', encoding="utf-8")
        (locales / "en.json").write_text('{"section": {"key1": "val1"}}', encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            result = check_translation_coverage("en", tmp_path, [])
        assert result.total == 2
        assert result.passed == 1

    def test_invalid_json(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text("{invalid json}", encoding="utf-8")
        (locales / "en.json").write_text("{}", encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            result = check_translation_coverage("en", tmp_path, [])
        assert len(result.issues) > 0

    def test_verbose_shows_missing_keys(self, tmp_path):
        from i18n_check import check_translation_coverage
        locales = tmp_path / "locales"
        locales.mkdir()
        (locales / "ja.json").write_text('{"key1": "v1", "key2": "v2"}', encoding="utf-8")
        (locales / "en.json").write_text('{"key1": "v1"}', encoding="utf-8")
        with patch("i18n_check.LOCALES_DIR", locales):
            result = check_translation_coverage("en", tmp_path, [], verbose=True)
        assert any("Missing key" in i.message for i in result.issues)


# ===================================================================
# check_image_coverage
# ===================================================================

class TestCheckImageCoverage:
    def test_image_exists(self, tmp_path):
        from i18n_check import check_image_coverage
        lang_dir = tmp_path / "en"
        img_dir = lang_dir / "assets" / "images"
        img_dir.mkdir(parents=True)
        img = img_dir / "test.png"
        img.write_bytes(b"\x89PNG")
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="assets/images/test.png"></body></html>', encoding="utf-8")
        result = check_image_coverage("en", lang_dir, [f])
        assert result.passed >= 1

    def test_image_missing(self, tmp_path):
        from i18n_check import check_image_coverage
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html><body><img src="assets/images/missing.png"></body></html>', encoding="utf-8")
        result = check_image_coverage("en", lang_dir, [f])
        assert result.status == "FAIL"


# ===================================================================
# fix_lang_attribute / fix_charset
# ===================================================================

class TestFixFunctions:
    def test_fix_lang_attribute(self, tmp_path):
        from i18n_check import fix_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<html lang="ja"><body></body></html>', encoding="utf-8")
        count = fix_lang_attribute("en", tmp_path, [f])
        assert count == 1
        text = f.read_text(encoding="utf-8")
        assert 'lang="en"' in text

    def test_fix_lang_attribute_missing(self, tmp_path):
        from i18n_check import fix_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<html><body></body></html>', encoding="utf-8")
        count = fix_lang_attribute("en", tmp_path, [f])
        assert count == 1
        text = f.read_text(encoding="utf-8")
        assert 'lang="en"' in text

    def test_fix_lang_attribute_already_correct(self, tmp_path):
        from i18n_check import fix_lang_attribute
        f = tmp_path / "test.html"
        f.write_text('<html lang="en"><body></body></html>', encoding="utf-8")
        count = fix_lang_attribute("en", tmp_path, [f])
        assert count == 0

    def test_fix_charset_missing(self, tmp_path):
        from i18n_check import fix_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head></head><body></body></html>', encoding="utf-8")
        count = fix_charset("en", tmp_path, [f])
        assert count == 1
        text = f.read_text(encoding="utf-8")
        assert 'charset="UTF-8"' in text

    def test_fix_charset_wrong(self, tmp_path):
        from i18n_check import fix_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head><meta charset="ISO-8859-1"></head></html>', encoding="utf-8")
        count = fix_charset("en", tmp_path, [f])
        assert count == 1
        text = f.read_text(encoding="utf-8")
        assert 'charset="UTF-8"' in text

    def test_fix_charset_already_correct(self, tmp_path):
        from i18n_check import fix_charset
        f = tmp_path / "test.html"
        f.write_text('<html><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        count = fix_charset("en", tmp_path, [f])
        assert count == 0


# ===================================================================
# format_text_report / format_json_report
# ===================================================================

class TestFormatReport:
    def test_text_report_pass(self):
        from i18n_check import format_text_report, CheckResult
        cr = CheckResult("test_check")
        cr.total = 3
        cr.passed = 3
        report = format_text_report("en", [cr])
        assert "[PASS]" in report
        assert "1 PASS" in report

    def test_text_report_fail(self):
        from i18n_check import format_text_report, CheckResult, Issue
        cr = CheckResult("test_check")
        cr.total = 3
        cr.passed = 2
        cr.add_issue(Issue("f.html", 1, "error"))
        report = format_text_report("en", [cr])
        assert "[FAIL]" in report

    def test_text_report_warn_verbose(self):
        from i18n_check import format_text_report, CheckResult, Issue
        cr = CheckResult("test_check")
        cr.total = 3
        cr.passed = 2
        cr.add_issue(Issue("f.html", 1, "warn", severity="WARN"))
        report = format_text_report("en", [cr], verbose=True)
        assert "[WARN]" in report

    def test_text_report_many_issues_truncated(self):
        from i18n_check import format_text_report, CheckResult, Issue
        cr = CheckResult("test_check")
        cr.total = 50
        cr.passed = 0
        for i in range(30):
            cr.add_issue(Issue("f.html", i, f"error {i}"))
        report = format_text_report("en", [cr], verbose=False)
        assert "more" in report

    def test_text_report_zero_items(self):
        from i18n_check import format_text_report, CheckResult
        cr = CheckResult("test_check")
        report = format_text_report("en", [cr])
        assert "0 items checked" in report

    def test_text_report_translation_coverage(self):
        from i18n_check import format_text_report, CheckResult
        cr = CheckResult("translation_coverage")
        cr.total = 100
        cr.passed = 80
        report = format_text_report("en", [cr])
        assert "80.0%" in report

    def test_json_report(self):
        from i18n_check import format_json_report, CheckResult, Issue
        cr1 = CheckResult("check1")
        cr1.total = 2
        cr1.passed = 2
        cr2 = CheckResult("check2")
        cr2.add_issue(Issue("f.html", 1, "err"))
        report = format_json_report("en", [cr1, cr2])
        assert report["lang"] == "en"
        assert report["summary"]["pass"] == 1
        assert report["summary"]["fail"] == 1


# ===================================================================
# run_checks / run_fixes
# ===================================================================

class TestRunChecks:
    def test_nonexistent_lang_dir(self, tmp_path):
        from i18n_check import run_checks
        with patch("i18n_check.DIST_DIR", tmp_path):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                results = run_checks("xx")
        assert len(results) == 1
        assert results[0].status == "FAIL"

    def test_empty_lang_dir(self, tmp_path):
        from i18n_check import run_checks
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        with patch("i18n_check.DIST_DIR", tmp_path):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                results = run_checks("en")
        assert len(results) == 1
        assert "No HTML" in results[0].issues[0].message

    def test_unknown_check_name(self, tmp_path):
        from i18n_check import run_checks
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        (lang_dir / "index.html").write_text('<html lang="en"></html>', encoding="utf-8")
        with patch("i18n_check.DIST_DIR", tmp_path):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                results = run_checks("en", check_names=["nonexistent_check"])
        assert any("Unknown check" in i.message for r in results for i in r.issues)

    def test_specific_checks(self, tmp_path):
        from i18n_check import run_checks
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        (lang_dir / "index.html").write_text('<html lang="en"><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        with patch("i18n_check.DIST_DIR", tmp_path):
            with patch("i18n_check.ROOT_DIR", tmp_path):
                results = run_checks("en", check_names=["lang_attribute", "charset_check"])
        assert len(results) == 2

    def test_run_fixes_nonexistent(self, tmp_path):
        from i18n_check import run_fixes
        with patch("i18n_check.DIST_DIR", tmp_path):
            result = run_fixes("xx")
        assert result == {}

    def test_run_fixes_empty(self, tmp_path):
        from i18n_check import run_fixes
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        with patch("i18n_check.DIST_DIR", tmp_path):
            result = run_fixes("en")
        assert result == {}

    def test_run_fixes_applies(self, tmp_path):
        from i18n_check import run_fixes
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html lang="ja"><head></head><body></body></html>', encoding="utf-8")
        with patch("i18n_check.DIST_DIR", tmp_path):
            result = run_fixes("en")
        assert "lang_attribute" in result


# ===================================================================
# main (CLI)
# ===================================================================

class TestMainCLI:
    def test_main_nonexistent_lang(self, tmp_path):
        from i18n_check import main
        with patch("sys.argv", ["i18n_check.py", "--lang", "xx"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    ret = main()
        assert ret == 1  # has failure

    def test_main_json_output(self, tmp_path, capsys):
        from i18n_check import main
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        (lang_dir / "test.html").write_text('<html lang="en"><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "--json"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    with patch("i18n_check.LOCALES_DIR", tmp_path / "locales"):
                        ret = main()
        out = capsys.readouterr().out
        import json
        data = json.loads(out)
        assert "lang" in data

    def test_main_with_checks_filter(self, tmp_path):
        from i18n_check import main
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        (lang_dir / "test.html").write_text('<html lang="en"><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "--checks", "lang_attribute"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    ret = main()
        assert ret == 0

    def test_main_unknown_check(self, tmp_path):
        from i18n_check import main
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "--checks", "bad_check"]):
            ret = main()
        assert ret == 2

    def test_main_with_fix(self, tmp_path, capsys):
        from i18n_check import main
        lang_dir = tmp_path / "en"
        lang_dir.mkdir()
        f = lang_dir / "test.html"
        f.write_text('<html lang="ja"><head><meta charset="UTF-8"></head></html>', encoding="utf-8")
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "--fix", "--checks", "lang_attribute"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    ret = main()
        out = capsys.readouterr().out
        assert "Fixed" in out or "PASS" in out

    def test_main_multiple_langs(self, tmp_path, capsys):
        from i18n_check import main
        for lang_code in ["en", "es"]:
            lang_dir = tmp_path / lang_code
            lang_dir.mkdir()
            (lang_dir / "test.html").write_text(
                f'<html lang="{lang_code}"><head><meta charset="UTF-8"></head></html>',
                encoding="utf-8",
            )
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "es", "--checks", "lang_attribute"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    ret = main()
        assert ret == 0

    def test_main_json_multiple_langs(self, tmp_path, capsys):
        from i18n_check import main
        for lang_code in ["en", "es"]:
            lang_dir = tmp_path / lang_code
            lang_dir.mkdir()
            (lang_dir / "test.html").write_text(
                f'<html lang="{lang_code}"><head><meta charset="UTF-8"></head></html>',
                encoding="utf-8",
            )
        with patch("sys.argv", ["i18n_check.py", "--lang", "en", "es", "--json", "--checks", "lang_attribute"]):
            with patch("i18n_check.DIST_DIR", tmp_path):
                with patch("i18n_check.ROOT_DIR", tmp_path):
                    ret = main()
        out = capsys.readouterr().out
        import json
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 2
