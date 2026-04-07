"""i18n_extract.py の単体テスト"""
import pytest
import inspect
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestImport:
    def test_import_module(self):
        import i18n_extract
        assert hasattr(i18n_extract, "main")
        assert hasattr(i18n_extract, "extract_texts_from_html")

    def test_uses_common_module(self):
        import i18n_extract
        from i18n_common import COURSE_DIR
        assert i18n_extract.COURSE_DIR == COURSE_DIR


class TestGetDirectText:
    def test_simple_text(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _get_direct_text
        soup = BeautifulSoup("<p>Hello World</p>", "html.parser")
        p = soup.find("p")
        assert _get_direct_text(p) == "Hello World"

    def test_excludes_child_text(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _get_direct_text
        soup = BeautifulSoup("<p>Parent <span>Child</span> text</p>", "html.parser")
        p = soup.find("p")
        result = _get_direct_text(p)
        assert "Child" not in result
        assert "Parent" in result
        assert "text" in result

    def test_empty_element(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _get_direct_text
        soup = BeautifulSoup("<p></p>", "html.parser")
        p = soup.find("p")
        assert _get_direct_text(p) == ""


class TestGenerateKey:
    def test_simple_tag(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _generate_key
        soup = BeautifulSoup("<h1>Title</h1>", "html.parser")
        h1 = soup.find("h1")
        counters = {}
        key = _generate_key("h1", h1, counters)
        assert key == "h1.0"

    def test_semantic_class(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _generate_key
        soup = BeautifulSoup('<p class="lead">Text</p>', "html.parser")
        p = soup.find("p")
        counters = {}
        key = _generate_key("p", p, counters)
        assert key == "p.lead.0"

    def test_counter_increments(self):
        from bs4 import BeautifulSoup
        from i18n_extract import _generate_key
        soup = BeautifulSoup("<p>A</p><p>B</p>", "html.parser")
        counters = {}
        ps = soup.find_all("p")
        key1 = _generate_key("p", ps[0], counters)
        key2 = _generate_key("p", ps[1], counters)
        assert key1 == "p.0"
        assert key2 == "p.1"


class TestExtractTextsFromHtml:
    def test_extracts_title(self, tmp_path):
        html = "<html><head><title>テストページ</title></head><body><p>内容です</p></body></html>"
        f = tmp_path / "test.html"
        f.write_text(html, encoding="utf-8")
        from i18n_extract import extract_texts_from_html
        result = extract_texts_from_html(f)
        assert "title" in result
        assert result["title"] == "テストページ"

    def test_extracts_meta(self, tmp_path):
        html = '<html><head><meta name="description" content="テスト説明文です"></head><body><p>内容です</p></body></html>'
        f = tmp_path / "test.html"
        f.write_text(html, encoding="utf-8")
        from i18n_extract import extract_texts_from_html
        result = extract_texts_from_html(f)
        assert "meta.description" in result

    def test_skips_script_content(self, tmp_path):
        html = "<html><body><script>var x = 'テスト';</script><p>本文テスト</p></body></html>"
        f = tmp_path / "test.html"
        f.write_text(html, encoding="utf-8")
        from i18n_extract import extract_texts_from_html
        result = extract_texts_from_html(f)
        values = list(result.values())
        assert any("本文テスト" in v for v in values)

    def test_extracts_alt_attribute(self, tmp_path):
        html = '<html><body><img alt="画像の説明テスト"></body></html>'
        f = tmp_path / "test.html"
        f.write_text(html, encoding="utf-8")
        from i18n_extract import extract_texts_from_html
        result = extract_texts_from_html(f)
        assert any("画像の説明テスト" in v for v in result.values())

    def test_skips_short_text(self, tmp_path):
        html = "<html><body><p>A</p><p>長いテキストです</p></body></html>"
        f = tmp_path / "test.html"
        f.write_text(html, encoding="utf-8")
        from i18n_extract import extract_texts_from_html
        result = extract_texts_from_html(f)
        assert not any(v == "A" for v in result.values())


class TestTranslateFileTexts:
    def test_batch_size_parameter(self):
        from i18n_extract import translate_file_texts
        sig = inspect.signature(translate_file_texts)
        assert "batch_size" in sig.parameters

    def test_uses_batch_size(self):
        from i18n_extract import translate_file_texts
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"key0": "val0", "key1": "val1"}'
        mock_client.models.generate_content.return_value = mock_response

        texts = {f"key{i}": f"テスト{i}" for i in range(5)}
        with patch("i18n_extract.time"):
            result = translate_file_texts(mock_client, texts, "en", "gemini-3-flash-preview", batch_size=2)
        assert mock_client.models.generate_content.call_count == 3


class TestTranslateAll:
    def test_batch_size_parameter(self):
        from i18n_extract import translate_all
        sig = inspect.signature(translate_all)
        assert "batch_size" in sig.parameters


class TestNoGlobalBatchSize:
    def test_no_global_mutation(self):
        """main() がglobal BATCH_SIZEを使っていないことを確認"""
        import i18n_extract
        source = inspect.getsource(i18n_extract.main)
        assert "global BATCH_SIZE" not in source
        assert "global " not in source
