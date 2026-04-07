"""check_i18n_coverage.py unit tests."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def temp_course(tmp_path):
    """Create a minimal course structure for testing."""
    course_dir = tmp_path / "course"
    course_dir.mkdir()

    # Create HTML files
    foundation = course_dir / "foundation"
    foundation.mkdir()
    (foundation / "page1.html").write_text("<html><body>Test</body></html>")
    (foundation / "page2.html").write_text("<html><body>Test</body></html>")

    # Create locales directory
    locales = course_dir / "locales"
    locales.mkdir()

    return course_dir


@pytest.fixture
def full_locale_data():
    """Return sample locale data with all keys present."""
    return {
        "foundation/page1.html": {
            "title": "Page 1",
            "h1.0": "Heading",
            "p.0": "Content",
        },
        "foundation/page2.html": {
            "title": "Page 2",
            "h1.0": "Heading 2",
        },
    }


class TestFindHtmlFiles:
    """Test HTML file discovery."""

    def test_finds_html_files(self, temp_course):
        """Finds HTML files under course directory."""
        from check_i18n_coverage import find_html_files, COURSE_DIR

        with patch("check_i18n_coverage.COURSE_DIR", temp_course):
            files = find_html_files()
        assert "foundation/page1.html" in files
        assert "foundation/page2.html" in files
        assert len(files) == 2

    def test_excludes_dist_directory(self, temp_course):
        """Excludes dist/ directory from results."""
        dist_dir = temp_course / "dist" / "en"
        dist_dir.mkdir(parents=True)
        (dist_dir / "page.html").write_text("<html></html>")

        with patch("check_i18n_coverage.COURSE_DIR", temp_course):
            from check_i18n_coverage import find_html_files
            files = find_html_files()
        assert all("dist" not in f for f in files)

    def test_excludes_assets_directory(self, temp_course):
        """Excludes assets/ directory from results."""
        assets_dir = temp_course / "assets"
        assets_dir.mkdir()
        (assets_dir / "template.html").write_text("<html></html>")

        with patch("check_i18n_coverage.COURSE_DIR", temp_course):
            from check_i18n_coverage import find_html_files
            files = find_html_files()
        assert all("assets" not in f for f in files)


class TestLoadLocale:
    """Test locale JSON loading."""

    def test_loads_existing_locale(self, temp_course, full_locale_data):
        """Loads and parses existing locale JSON."""
        locales = temp_course / "locales"
        (locales / "ja.json").write_text(
            json.dumps(full_locale_data, ensure_ascii=False),
            encoding="utf-8",
        )

        with patch("check_i18n_coverage.LOCALES_DIR", locales):
            from check_i18n_coverage import load_locale
            data = load_locale("ja")
        assert "foundation/page1.html" in data
        assert len(data) == 2

    def test_returns_empty_for_missing_locale(self, temp_course):
        """Returns empty dict for non-existent locale file."""
        locales = temp_course / "locales"

        with patch("check_i18n_coverage.LOCALES_DIR", locales):
            from check_i18n_coverage import load_locale
            data = load_locale("ko")
        assert data == {}


class TestCheckCoverage:
    """Test the main coverage check logic."""

    def _setup_locales(self, temp_course, ja_data, en_data=None, es_data=None):
        """Helper to write locale files."""
        locales = temp_course / "locales"
        (locales / "ja.json").write_text(
            json.dumps(ja_data, ensure_ascii=False), encoding="utf-8"
        )
        if en_data is not None:
            (locales / "en.json").write_text(
                json.dumps(en_data, ensure_ascii=False), encoding="utf-8"
            )
        if es_data is not None:
            (locales / "es.json").write_text(
                json.dumps(es_data, ensure_ascii=False), encoding="utf-8"
            )

    def test_all_pass(self, temp_course, full_locale_data):
        """Returns 0 when all checks pass."""
        self._setup_locales(
            temp_course, full_locale_data, full_locale_data, full_locale_data
        )

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en", "es"])
        assert result == 0

    def test_missing_file_section_fails(self, temp_course, full_locale_data):
        """Returns 1 when en.json is missing a file section."""
        en_data = {"foundation/page1.html": full_locale_data["foundation/page1.html"]}
        self._setup_locales(temp_course, full_locale_data, en_data)

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en"])
        assert result == 1

    def test_missing_keys_fails(self, temp_course, full_locale_data):
        """Returns 1 when en.json has missing keys within a section."""
        en_data = {
            "foundation/page1.html": {"title": "Page 1"},
            "foundation/page2.html": full_locale_data["foundation/page2.html"],
        }
        self._setup_locales(temp_course, full_locale_data, en_data)

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en"])
        assert result == 1

    def test_quick_skips_key_check(self, temp_course, full_locale_data):
        """Quick mode skips key-level check, passes with missing keys."""
        en_data = {
            "foundation/page1.html": {"title": "Page 1"},
            "foundation/page2.html": full_locale_data["foundation/page2.html"],
        }
        self._setup_locales(temp_course, full_locale_data, en_data)

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en"], quick=True)
        assert result == 0

    def test_unregistered_html_fails(self, temp_course):
        """Returns 1 when HTML file is not in ja.json."""
        ja_data = {"foundation/page1.html": {"title": "Page 1"}}
        en_data = {"foundation/page1.html": {"title": "Page 1"}}
        self._setup_locales(temp_course, ja_data, en_data)

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en"])
        assert result == 1

    def test_missing_locale_file_fails(self, temp_course, full_locale_data):
        """Returns 1 when locale file does not exist."""
        self._setup_locales(temp_course, full_locale_data)

        with patch("check_i18n_coverage.COURSE_DIR", temp_course), \
             patch("check_i18n_coverage.LOCALES_DIR", temp_course / "locales"):
            from check_i18n_coverage import check_coverage
            result = check_coverage(["en"])
        assert result == 1
