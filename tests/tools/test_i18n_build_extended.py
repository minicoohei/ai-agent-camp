"""i18n_build.py の拡張テスト - カバレッジ向上"""
import json
import re
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestLoadTranslations:
    def test_load_existing_file(self, tmp_path):
        from i18n_build import load_translations
        data = {"file.html": {"title": "Test"}}
        locale_file = tmp_path / "en.json"
        locale_file.write_text(json.dumps(data), encoding="utf-8")
        with patch("i18n_build.LOCALES_DIR", tmp_path):
            result = load_translations("en")
        assert result == data

    def test_load_missing_file(self, tmp_path, capsys):
        from i18n_build import load_translations
        with patch("i18n_build.LOCALES_DIR", tmp_path):
            result = load_translations("missing_lang")
        assert result == {}
        captured = capsys.readouterr()
        assert "ERROR" in captured.out


class TestLoadJaKeys:
    def test_load_existing(self, tmp_path):
        from i18n_build import load_ja_keys
        data = {"index.html": {"title": "test"}}
        ja_file = tmp_path / "ja.json"
        ja_file.write_text(json.dumps(data), encoding="utf-8")
        with patch("i18n_build.LOCALES_DIR", tmp_path):
            result = load_ja_keys()
        assert result == data

    def test_load_missing(self, tmp_path, capsys):
        from i18n_build import load_ja_keys
        with patch("i18n_build.LOCALES_DIR", tmp_path):
            result = load_ja_keys()
        assert result == {}
        captured = capsys.readouterr()
        assert "ERROR" in captured.out


class TestComputeRelativePath:
    def test_root_file(self, tmp_path):
        from i18n_build import compute_relative_path
        course = tmp_path / "course"
        course.mkdir()
        f = course / "index.html"
        with patch("i18n_build.COURSE_DIR", course):
            result = compute_relative_path(f, "dist", "en")
        assert result == ""

    def test_nested_file(self, tmp_path):
        from i18n_build import compute_relative_path
        course = tmp_path / "course"
        subdir = course / "setup"
        subdir.mkdir(parents=True)
        f = subdir / "index.html"
        with patch("i18n_build.COURSE_DIR", course):
            result = compute_relative_path(f, "dist", "en")
        assert result == "../"

    def test_deep_nested(self, tmp_path):
        from i18n_build import compute_relative_path
        course = tmp_path / "course"
        deep = course / "a" / "b"
        deep.mkdir(parents=True)
        f = deep / "page.html"
        with patch("i18n_build.COURSE_DIR", course):
            result = compute_relative_path(f, "dist", "en")
        assert result == "../../"


class TestBuildLangSwitcher:
    def test_generates_links(self, tmp_path):
        from i18n_build import build_lang_switcher
        course = tmp_path / "course"
        course.mkdir()
        f = course / "index.html"
        with patch("i18n_build.COURSE_DIR", course):
            html = build_lang_switcher(f, ["en", "es"])
        assert "lang-switcher" in html
        assert 'data-lang="ja"' in html
        assert 'data-lang="en"' in html
        assert 'data-lang="es"' in html

    def test_nested_file_links(self, tmp_path):
        from i18n_build import build_lang_switcher
        course = tmp_path / "course"
        subdir = course / "lesson1"
        subdir.mkdir(parents=True)
        f = subdir / "page.html"
        with patch("i18n_build.COURSE_DIR", course):
            html = build_lang_switcher(f, ["en"])
        assert "../" in html


class TestBuildLangSwitcherCss:
    def test_returns_css(self):
        from i18n_build import build_lang_switcher_css
        css = build_lang_switcher_css()
        assert ".lang-switcher" in css
        assert ".lang-btn" in css


class TestReplaceDirectText:
    def test_replaces_navigable_string(self):
        from bs4 import BeautifulSoup
        from i18n_build import _replace_direct_text
        soup = BeautifulSoup("<p>old text here</p>", "html.parser")
        p = soup.find("p")
        result = _replace_direct_text(p, "old text here", "new text here")
        assert result is True
        assert "new text here" in str(soup)

    def test_replaces_stripped_match(self):
        from bs4 import BeautifulSoup
        from i18n_build import _replace_direct_text
        soup = BeautifulSoup("<p>  old text  </p>", "html.parser")
        p = soup.find("p")
        result = _replace_direct_text(p, "old text", "new text")
        assert result is True

    def test_no_match(self):
        from bs4 import BeautifulSoup
        from i18n_build import _replace_direct_text
        soup = BeautifulSoup("<p>something else</p>", "html.parser")
        p = soup.find("p")
        result = _replace_direct_text(p, "not here", "replaced")
        assert result is False

    def test_element_string_property(self):
        from bs4 import BeautifulSoup
        from i18n_build import _replace_direct_text
        soup = BeautifulSoup("<span>old text</span>", "html.parser")
        span = soup.find("span")
        result = _replace_direct_text(span, "old text", "new text")
        assert result is True


class TestApplyTextSearchAll:
    def test_skips_code_block(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_text_search_all
        soup = BeautifulSoup("<body><code>some code text here</code></body>", "html.parser")
        result = _apply_text_search_all(soup, "some code text here", "replaced")
        assert not result

    def test_skips_script_block(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_text_search_all
        soup = BeautifulSoup("<body><script>some script text here</script></body>", "html.parser")
        result = _apply_text_search_all(soup, "some script text here", "replaced")
        assert not result


class TestApplyTranslationsMetaTags:
    def test_replaces_meta_content(self):
        from i18n_build import apply_translations
        html = '<html lang="ja"><head><meta name="description" content="old desc"></head><body></body></html>'
        ja_keys = {"meta.description": "old desc"}
        translations = {"meta.description": "new description"}
        result, applied, _ = apply_translations(html, ja_keys, translations, "en")
        assert "new description" in result
        assert applied >= 1

    def test_skips_same_text(self):
        from i18n_build import apply_translations
        html = '<html lang="ja"><body><p>same text here</p></body></html>'
        ja_keys = {"p.0": "same text here"}
        translations = {"p.0": "same text here"}
        result, applied, _ = apply_translations(html, ja_keys, translations, "en")
        assert applied == 0

    def test_attribute_replacement(self):
        from i18n_build import apply_translations
        html = '<html lang="ja"><body><img alt="old alt text value" title="old title text value"></body></html>'
        ja_keys = {"img[alt].0": "old alt text value"}
        translations = {"img[alt].0": "new alt text value"}
        result, applied, _ = apply_translations(html, ja_keys, translations, "en")
        assert "new alt text value" in result


class TestApplyKeyTranslationEdgeCases:
    def test_tag_class_index_out_of_range(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup('<body><p class="lead">text</p></body>', "html.parser")
        result = _apply_key_translation(soup, "p.lead.99", "text", "new")
        assert result is False

    def test_tag_index_out_of_range(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup("<body><p>text</p></body>", "html.parser")
        result = _apply_key_translation(soup, "p.99", "text", "new")
        assert result is False

    def test_img_alt_out_of_range(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup('<body><img alt="desc"></body>', "html.parser")
        result = _apply_key_translation(soup, "img[alt].99", "desc", "new")
        assert result is False

    def test_unknown_key_format(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup("<body><p>text</p></body>", "html.parser")
        result = _apply_key_translation(soup, "unknown_format", "text", "new")
        assert result is False

    def test_tag_index_skips_code_parents(self):
        from bs4 import BeautifulSoup
        from i18n_build import _apply_key_translation
        soup = BeautifulSoup("<body><pre><p>inside pre</p></pre><p>outside pre text</p></body>", "html.parser")
        result = _apply_key_translation(soup, "p.0", "outside pre text", "replaced text")
        assert result is True
        assert "replaced text" in str(soup)


class TestCopyAssets:
    def test_copy_css_with_font_override(self, tmp_path):
        from i18n_build import copy_assets
        course = tmp_path / "course"
        css_dir = course / "assets" / "css"
        css_dir.mkdir(parents=True)
        (css_dir / "bootcamp.css").write_text(
            "--font-sans: 'Noto Sans JP'; body { margin: 0; }",
            encoding="utf-8",
        )
        dist = tmp_path / "dist"
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist):
            copy_assets("en", verbose=True)
        output_css = dist / "en" / "assets" / "css" / "bootcamp.css"
        assert output_css.exists()
        content = output_css.read_text()
        assert "Inter" in content
        assert "lang-switcher" in content.lower() or "Language Switcher" in content

    def test_copy_images(self, tmp_path):
        from i18n_build import copy_assets
        course = tmp_path / "course"
        img_dir = course / "assets" / "images"
        img_dir.mkdir(parents=True)
        (img_dir / "test.png").write_bytes(b"fakepng")
        dist = tmp_path / "dist"
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist):
            copy_assets("en")
        assert (dist / "en" / "assets" / "images" / "test.png").exists()

    def test_no_assets_dir(self, tmp_path, capsys):
        from i18n_build import copy_assets
        course = tmp_path / "course"
        course.mkdir()
        dist = tmp_path / "dist"
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist):
            copy_assets("en")
        captured = capsys.readouterr()
        assert "WARN" in captured.out

    def test_copy_material(self, tmp_path):
        from i18n_build import copy_assets
        course = tmp_path / "course"
        mat_dir = course / "assets" / "material"
        mat_dir.mkdir(parents=True)
        (mat_dir / "doc.pdf").write_bytes(b"fakepdf")
        dist = tmp_path / "dist"
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist):
            copy_assets("en")
        assert (dist / "en" / "assets" / "material" / "doc.pdf").exists()

    def test_copy_subdir_assets(self, tmp_path):
        from i18n_build import copy_assets
        course = tmp_path / "course"
        # Create a main assets dir so the function doesn't warn and return early
        (course / "assets").mkdir(parents=True)
        sub_assets = course / "setup" / "assets"
        sub_assets.mkdir(parents=True)
        (sub_assets / "icon.png").write_bytes(b"fake")
        dist = tmp_path / "dist"
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist):
            copy_assets("en")
        assert (dist / "en" / "setup" / "assets" / "icon.png").exists()


class TestBuildLanguage:
    def test_builds_with_translations(self, tmp_path):
        from i18n_build import build_language
        course = tmp_path / "course"
        course.mkdir()
        html = '<html lang="ja"><head><title>T</title></head><body><nav>N</nav><p>test</p></body></html>'
        (course / "index.html").write_text(html, encoding="utf-8")
        dist = tmp_path / "dist"
        ja_keys = {"index.html": {"title": "T", "p.0": "test"}}
        translations = {"index.html": {"title": "T-en", "p.0": "test-en"}}
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist), \
             patch("i18n_build.find_html_files", return_value=[course / "index.html"]):
            stats = build_language("en", ja_keys, translations, ["en"], verbose=True)
        assert stats["files"] == 1
        assert stats["applied"] >= 1
        assert (dist / "en" / "index.html").exists()

    def test_builds_without_translations(self, tmp_path):
        from i18n_build import build_language
        course = tmp_path / "course"
        course.mkdir()
        html = '<html lang="ja"><body><p>nochange</p></body></html>'
        (course / "page.html").write_text(html, encoding="utf-8")
        dist = tmp_path / "dist"
        ja_keys = {"page.html": {"p.0": "nochange"}}
        translations = {}
        with patch("i18n_build.COURSE_DIR", course), \
             patch("i18n_build.DIST_DIR", dist), \
             patch("i18n_build.find_html_files", return_value=[course / "page.html"]):
            stats = build_language("es", ja_keys, translations, ["es"], verbose=True)
        assert stats["files"] == 1
        assert stats["missing"] >= 1
        content = (dist / "es" / "page.html").read_text()
        assert 'lang="es"' in content
