"""i18n_build.py の単体テスト"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestImport:
    def test_import_module(self):
        import i18n_build
        assert hasattr(i18n_build, "apply_translations")
        assert hasattr(i18n_build, "insert_lang_switcher")

    def test_uses_common_module(self):
        import i18n_build
        from i18n_common import COURSE_DIR
        assert i18n_build.COURSE_DIR == COURSE_DIR


class TestApplyTranslations:
    def test_replaces_title(self):
        from i18n_build import apply_translations
        html = "<html lang='ja'><head><title>テスト</title></head><body><p>内容テスト</p></body></html>"
        ja_keys = {"title": "テスト", "p.0": "内容テスト"}
        translations = {"title": "Test", "p.0": "Content Test"}
        result, applied, missing = apply_translations(html, ja_keys, translations, "en")
        assert "Test" in result
        assert applied >= 1

    def test_sets_lang_attribute(self):
        from i18n_build import apply_translations
        html = "<html lang='ja'><head><title>T</title></head><body></body></html>"
        result, _, _ = apply_translations(html, {}, {}, "en")
        assert 'lang="en"' in result

    def test_counts_missing_keys(self):
        from i18n_build import apply_translations
        html = "<html><body><p>テスト文章</p></body></html>"
        ja_keys = {"p.0": "テスト文章", "p.1": "存在しないテスト"}
        translations = {"p.0": "Test text"}
        _, _, missing = apply_translations(html, ja_keys, translations, "en")
        assert missing >= 1

    def test_no_double_replacement_short_text(self):
        """短いテキストのフォールバック二重置換が発生しないことを確認 (I4)"""
        from i18n_build import apply_translations
        html = "<html><body><p>AI</p><p>AI活用ガイド</p></body></html>"
        ja_keys = {"p.0": "AI", "p.1": "AI活用ガイド"}
        translations = {"p.0": "AI", "p.1": "AI Utilization Guide"}
        result, _, _ = apply_translations(html, ja_keys, translations, "en")
        assert "AI Utilization Guide" in result


class TestApplyKeyTranslation:
    def test_tag_index_format(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup("<body><p>テスト文1</p><p>テスト文2</p></body>", "html.parser")
        assert _apply_key_translation(soup, "p.0", "テスト文1", "Test1")
        assert "Test1" in str(soup)
        assert "テスト文2" in str(soup)

    def test_tag_class_index_format(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup('<body><p class="lead">テスト文章</p></body>', "html.parser")
        assert _apply_key_translation(soup, "p.lead.0", "テスト文章", "Test Text")
        assert "Test Text" in str(soup)

    def test_img_alt_format(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup('<body><img alt="説明文テスト"></body>', "html.parser")
        assert _apply_key_translation(soup, "img[alt].0", "説明文テスト", "Description Test")
        assert 'alt="Description Test"' in str(soup)


class TestApplyTextSearchAll:
    def test_skips_short_text(self):
        """5文字未満のテキストはフォールバック検索しない (I4)"""
        from bs4 import BeautifulSoup
        from i18n_build import _apply_text_search_all
        soup = BeautifulSoup("<body><p>AI</p><p>AI活用</p></body>", "html.parser")
        result = _apply_text_search_all(soup, "AI", "Artificial Intelligence")
        assert not result  # 2文字なのでスキップされる

    def test_replaces_long_text(self):
        """5文字以上のテキストはフォールバック検索する"""
        from bs4 import BeautifulSoup
        from i18n_build import _apply_text_search_all
        soup = BeautifulSoup("<body><p>テスト文章です</p></body>", "html.parser")
        result = _apply_text_search_all(soup, "テスト文章です", "This is test text")
        assert result
        assert "This is test text" in str(soup)


class TestInsertLangSwitcher:
    def test_inserts_into_nav(self):
        from i18n_build import insert_lang_switcher
        html = '<html><body><nav class="navbar"><div>Menu</div></nav><main>Content</main></body></html>'
        switcher = '<div class="lang-switcher"><a class="lang-btn" data-lang="en">EN</a></div>'
        result = insert_lang_switcher(html, switcher, "en")
        assert "lang-switcher" in result

    def test_no_nav_returns_unchanged(self):
        from i18n_build import insert_lang_switcher
        html = "<html><body><main>Content</main></body></html>"
        switcher = '<div class="lang-switcher">EN</div>'
        result = insert_lang_switcher(html, switcher, "en")
        assert result == html

    def test_active_class_on_current_lang(self):
        from i18n_build import insert_lang_switcher
        html = '<html><body><nav><div>Menu</div></nav></body></html>'
        switcher = '<div class="lang-switcher"><a class="lang-btn" data-lang="en">EN</a><a class="lang-btn" data-lang="es">ES</a></div>'
        result = insert_lang_switcher(html, switcher, "en")
        assert "active" in result

    def test_uses_last_nav(self):
        """複数navがある場合、最後のnavに挿入 (I5)"""
        from i18n_build import insert_lang_switcher
        html = '<html><body><nav id="first">First</nav><nav id="second">Second</nav></body></html>'
        switcher = '<div class="lang-switcher"><a class="lang-btn" data-lang="en">EN</a></div>'
        result = insert_lang_switcher(html, switcher, "en")
        # lang-switcherが2番目のnavの中にある
        second_nav_start = result.find('id="second"')
        assert second_nav_start != -1
        switcher_pos = result.find("lang-switcher")
        assert switcher_pos > second_nav_start
