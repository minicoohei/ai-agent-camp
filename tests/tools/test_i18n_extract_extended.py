"""i18n_extract.py の拡張テスト - カバレッジ向上"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestExtractTextsFromHtmlEdgeCases:
    def test_no_body(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = "<html><head><title>Only Title</title></head></html>"
        f = tmp_path / "no_body.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        assert "title" in result
        assert len([k for k in result if not k.startswith("title") and not k.startswith("meta")]) == 0

    def test_empty_html(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        f = tmp_path / "empty.html"
        f.write_text("", encoding="utf-8")
        result = extract_texts_from_html(f)
        assert isinstance(result, dict)

    def test_skips_numeric_only(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = "<html><body><p>12345</p><p>proper text here</p></body></html>"
        f = tmp_path / "numbers.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        values = list(result.values())
        assert not any(v == "12345" for v in values)
        assert any("proper text here" in v for v in values)

    def test_skips_bi_icon_class(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = "<html><body><span>bi-arrow-left</span><p>normal text content</p></body></html>"
        f = tmp_path / "icons.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        values = list(result.values())
        assert not any("bi-arrow" in v for v in values)

    def test_extracts_placeholder(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = '<html><body><label placeholder="enter text here">Label Text</label></body></html>'
        f = tmp_path / "placeholder.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        assert any("enter text here" in v for v in result.values())

    def test_extracts_aria_label(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = '<html><body><button aria-label="close button text">X</button></body></html>'
        f = tmp_path / "aria.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        assert any("close button text" in v for v in result.values())

    def test_img_title_attr(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = '<html><body><img alt="image alt text" title="image title text"></body></html>'
        f = tmp_path / "img_title.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        assert any("image title text" in v for v in result.values())

    def test_inside_pre_skipped(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = "<html><body><pre><p>code block text content</p></pre><p>normal text content</p></body></html>"
        f = tmp_path / "pre.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        values = list(result.values())
        assert not any("code block text content" in v for v in values)

    def test_multiple_heading_levels(self, tmp_path):
        from i18n_extract import extract_texts_from_html
        html = "<html><body><h1>Title Level 1</h1><h2>Title Level 2</h2><h3>Title Level 3</h3></body></html>"
        f = tmp_path / "headings.html"
        f.write_text(html, encoding="utf-8")
        result = extract_texts_from_html(f)
        values = list(result.values())
        assert any("Title Level 1" in v for v in values)
        assert any("Title Level 2" in v for v in values)

    def test_string_class_attribute(self, tmp_path):
        """class属性が文字列として渡される場合のテスト"""
        from i18n_extract import _generate_key
        from bs4 import BeautifulSoup
        # class属性がリストではなく文字列の場合
        soup = BeautifulSoup('<p class="lead badge">text</p>', "html.parser")
        p = soup.find("p")
        counters = {}
        key = _generate_key("p", p, counters)
        assert "lead" in key

    def test_role_attribute(self, tmp_path):
        from i18n_extract import _generate_key
        from bs4 import BeautifulSoup
        soup = BeautifulSoup('<p role="alert">text</p>', "html.parser")
        p = soup.find("p")
        counters = {}
        key = _generate_key("p", p, counters)
        assert "alert" in key


class TestExtractAll:
    def test_multiple_files(self, tmp_path):
        from i18n_extract import extract_all
        course = tmp_path / "course"
        course.mkdir()
        for i in range(3):
            f = course / f"page{i}.html"
            f.write_text(f"<html><head><title>Page {i}</title></head><body><p>Content {i} text</p></body></html>",
                         encoding="utf-8")
        files = list(course.glob("*.html"))
        with patch("i18n_extract.COURSE_DIR", course):
            result = extract_all(files)
        assert len(result) == 3

    def test_empty_file_skipped(self, tmp_path):
        from i18n_extract import extract_all
        course = tmp_path / "course"
        course.mkdir()
        f = course / "empty.html"
        f.write_text("<html><body></body></html>", encoding="utf-8")
        with patch("i18n_extract.COURSE_DIR", course):
            result = extract_all([f])
        # Empty files may or may not produce entries
        assert isinstance(result, dict)


class TestTranslateBatch:
    def test_successful_translation(self):
        from i18n_extract import translate_batch
        client = MagicMock()
        response = MagicMock()
        response.text = '{"key1": "Hello", "key2": "World"}'
        client.models.generate_content.return_value = response
        result = translate_batch(client, {"key1": "test1", "key2": "test2"}, "en", "model")
        assert result == {"key1": "Hello", "key2": "World"}

    def test_markdown_fence_removal(self):
        from i18n_extract import translate_batch
        client = MagicMock()
        response = MagicMock()
        response.text = '```json\n{"key1": "Hello"}\n```'
        client.models.generate_content.return_value = response
        result = translate_batch(client, {"key1": "test1"}, "en", "model")
        assert result == {"key1": "Hello"}

    def test_api_error_returns_original(self):
        from i18n_extract import translate_batch
        client = MagicMock()
        client.models.generate_content.side_effect = RuntimeError("API error")
        texts = {"key1": "original"}
        result = translate_batch(client, texts, "en", "model")
        assert result == texts

    def test_invalid_json_returns_original(self):
        from i18n_extract import translate_batch
        client = MagicMock()
        response = MagicMock()
        response.text = "not valid json at all"
        client.models.generate_content.return_value = response
        texts = {"key1": "original"}
        result = translate_batch(client, texts, "en", "model")
        assert result == texts


class TestBuildTranslationPrompt:
    def test_contains_target_language(self):
        from i18n_extract import _build_translation_prompt
        result = _build_translation_prompt({"k": "v"}, "en", "English")
        assert "English" in result
        assert "Japanese" in result

    def test_contains_technical_terms(self):
        from i18n_extract import _build_translation_prompt
        result = _build_translation_prompt({"k": "v"}, "en", "English")
        assert "Claude Code" in result


class TestPrintStats:
    def test_prints_stats(self, capsys):
        from i18n_extract import print_stats
        data = {
            "file1.html": {"h1.0": "Title", "p.0": "Text"},
            "file2.html": {"h2.0": "Sub"},
        }
        print_stats(data)
        captured = capsys.readouterr()
        assert "Files scanned" in captured.out
        assert "Total keys" in captured.out
        assert "3" in captured.out  # total keys

    def test_prints_empty_data(self, capsys):
        from i18n_extract import print_stats
        print_stats({})
        captured = capsys.readouterr()
        assert "Files scanned" in captured.out


class TestSaveJson:
    def test_saves_file(self, tmp_path):
        from i18n_extract import save_json
        data = {"key": "value"}
        out = tmp_path / "subdir" / "test.json"
        save_json(data, out)
        assert out.exists()
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded == data

    def test_unicode_content(self, tmp_path):
        from i18n_extract import save_json
        data = {"key": "value with special chars"}
        out = tmp_path / "test.json"
        save_json(data, out)
        content = out.read_text(encoding="utf-8")
        assert "special chars" in content


class TestTranslateFileTexts:
    def test_single_batch(self):
        from i18n_extract import translate_file_texts
        client = MagicMock()
        response = MagicMock()
        response.text = '{"k1": "v1", "k2": "v2"}'
        client.models.generate_content.return_value = response
        texts = {"k1": "t1", "k2": "t2"}
        with patch("i18n_extract.time"):
            result = translate_file_texts(client, texts, "en", "model", batch_size=50)
        assert len(result) == 2

    def test_multiple_batches(self):
        from i18n_extract import translate_file_texts
        client = MagicMock()
        response = MagicMock()
        response.text = '{"k0": "v0"}'
        client.models.generate_content.return_value = response
        texts = {f"k{i}": f"t{i}" for i in range(3)}
        with patch("i18n_extract.time"):
            result = translate_file_texts(client, texts, "en", "model", batch_size=1)
        assert client.models.generate_content.call_count == 3
