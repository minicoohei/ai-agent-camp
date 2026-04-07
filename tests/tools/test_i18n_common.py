"""i18n_common.py の単体テスト"""
import pytest
from pathlib import Path
from unittest.mock import patch


class TestConstants:
    """定数の検証"""

    def test_exclude_dirs_is_set(self):
        from i18n_common import EXCLUDE_DIRS

        assert isinstance(EXCLUDE_DIRS, set)
        assert "dist" in EXCLUDE_DIRS
        assert "_templates" in EXCLUDE_DIRS
        assert "locales" in EXCLUDE_DIRS

    def test_language_names_has_en_es(self):
        from i18n_common import LANGUAGE_NAMES

        assert "en" in LANGUAGE_NAMES
        assert "es" in LANGUAGE_NAMES
        assert LANGUAGE_NAMES["en"] == "English"
        assert LANGUAGE_NAMES["es"] == "Spanish"

    def test_course_dir_exists(self):
        from i18n_common import COURSE_DIR

        assert COURSE_DIR.exists()
        assert COURSE_DIR.name == "course"


class TestGetLanguageName:
    """get_language_name の検証"""

    def test_known_language(self):
        from i18n_common import get_language_name

        assert get_language_name("en") == "English"
        assert get_language_name("es") == "Spanish"
        assert get_language_name("ko") == "Korean"

    def test_unknown_language_returns_code(self):
        from i18n_common import get_language_name

        assert get_language_name("xx") == "xx"
        assert get_language_name("zz") == "zz"


class TestIsExcluded:
    """is_excluded の検証"""

    def test_excluded_dist(self):
        from i18n_common import is_excluded, COURSE_DIR

        path = COURSE_DIR / "dist" / "en" / "index.html"
        assert is_excluded(path) is True

    def test_excluded_templates(self):
        from i18n_common import is_excluded, COURSE_DIR

        path = COURSE_DIR / "_templates" / "manual.html"
        assert is_excluded(path) is True

    def test_excluded_locales(self):
        from i18n_common import is_excluded, COURSE_DIR

        path = COURSE_DIR / "locales" / "en" / "foundation.json"
        assert is_excluded(path) is True

    def test_included_modules(self):
        from i18n_common import is_excluded, COURSE_DIR

        path = COURSE_DIR / "modules" / "1-banner" / "index.html"
        assert is_excluded(path) is False

    def test_included_foundation(self):
        from i18n_common import is_excluded, COURSE_DIR

        path = COURSE_DIR / "foundation" / "what-is-ai.html"
        assert is_excluded(path) is False


class TestFindHtmlFiles:
    """find_html_files の検証"""

    def test_returns_list(self):
        from i18n_common import find_html_files

        result = find_html_files()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_all_items_are_paths(self):
        from i18n_common import find_html_files

        result = find_html_files()
        for item in result:
            assert isinstance(item, Path)
            assert item.suffix == ".html"

    def test_excludes_dist(self):
        from i18n_common import find_html_files

        result = find_html_files()
        for f in result:
            assert "dist" not in f.parts

    def test_excludes_templates(self):
        from i18n_common import find_html_files

        result = find_html_files()
        for f in result:
            assert "_templates" not in f.parts

    def test_excludes_locales(self):
        from i18n_common import find_html_files

        result = find_html_files()
        for f in result:
            assert "locales" not in f.parts


class TestRequireGeminiClient:
    """require_gemini_client の検証"""

    def test_exits_without_api_key(self, clean_env):
        from i18n_common import require_gemini_client

        with patch("bootcamp_utils.get_client", return_value=None):
            with pytest.raises(SystemExit) as exc_info:
                require_gemini_client()
            assert exc_info.value.code == 1

    def test_returns_client_with_key(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test_key_123")

        with patch("bootcamp_utils.get_client") as mock_get:
            mock_get.return_value = "mock_client"
            from i18n_common import require_gemini_client

            result = require_gemini_client()
            assert result == "mock_client"
