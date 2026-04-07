#!/usr/bin/env python3
"""i18n QA checking tool for translated HTML course files.

Verifies the quality of translated HTML files in ``course/dist/{lang}/``.
Runs 16 named checks covering text residue, attributes, links, assets,
and translation coverage.

Usage:
    uv run python tools/i18n_check.py --lang en es
    uv run python tools/i18n_check.py --lang en --checks original_text_residue,lang_attribute
    uv run python tools/i18n_check.py --lang en --fix
    uv run python tools/i18n_check.py --lang en --json
    uv run python tools/i18n_check.py --lang en --verbose
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable

try:
    from bs4 import BeautifulSoup, Comment
except ImportError:
    print(
        "ERROR: BeautifulSoup4 is required. Install with:\n"
        "  pip install beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(2)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT_DIR / "course"
DIST_DIR = COURSE_DIR / "dist"
LOCALES_DIR = COURSE_DIR / "locales"

# ---------------------------------------------------------------------------
# Unicode ranges for Japanese character detection
# ---------------------------------------------------------------------------
# Hiragana: U+3040-309F
# Katakana: U+30A0-30FF
# CJK Unified Ideographs (Kanji): U+4E00-9FFF
# Katakana Phonetic Extensions: U+31F0-31FF
# CJK Extension A: U+3400-4DBF
# Fullwidth ASCII variants: U+FF01-FF5E
# CJK Symbols and Punctuation: U+3000-303F
RE_HIRAGANA = re.compile(r"[\u3040-\u309F]")
RE_KATAKANA = re.compile(r"[\u30A0-\u30FF\u31F0-\u31FF]")
RE_KANJI = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF]")
RE_JAPANESE_ALL = re.compile(
    r"[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF\u4E00-\u9FFF\u3400-\u4DBF]"
)
RE_HIRAGANA_KATAKANA = re.compile(
    r"[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]"
)

# Template variable pattern: {{PLACEHOLDER}}
RE_TEMPLATE_VAR = re.compile(r"\{\{[A-Z_][A-Z0-9_]*\}\}")

# ---------------------------------------------------------------------------
# Result data classes
# ---------------------------------------------------------------------------

class Issue:
    """A single check issue (failure or warning)."""

    __slots__ = ("file", "line", "message", "severity")

    def __init__(
        self,
        file: str,
        line: int | None,
        message: str,
        severity: str = "FAIL",
    ):
        self.file = file
        self.line = line
        self.message = message
        self.severity = severity  # "FAIL" or "WARN"

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "file": self.file,
            "message": self.message,
            "severity": self.severity,
        }
        if self.line is not None:
            d["line"] = self.line
        return d

    def __repr__(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line else self.file
        return f"  - {loc}: {self.message!r}"


class CheckResult:
    """Result of a single named check."""

    __slots__ = ("name", "status", "total", "passed", "issues")

    def __init__(self, name: str):
        self.name = name
        self.status: str = "PASS"  # "PASS", "FAIL", "WARN"
        self.total: int = 0
        self.passed: int = 0
        self.issues: list[Issue] = []

    def add_issue(self, issue: Issue) -> None:
        self.issues.append(issue)
        if issue.severity == "FAIL":
            self.status = "FAIL"
        elif issue.severity == "WARN" and self.status != "FAIL":
            self.status = "WARN"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "total": self.total,
            "passed": self.passed,
            "issues": [i.to_dict() for i in self.issues],
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_html_files(lang_dir: Path) -> list[Path]:
    """Collect all .html files under a language dist directory."""
    return sorted(lang_dir.rglob("*.html"))


def _relative(path: Path, base: Path) -> str:
    """Return a short relative path string for display."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _parse_html(path: Path) -> BeautifulSoup | None:
    """Parse an HTML file, return None on failure."""
    try:
        text = path.read_text(encoding="utf-8")
        return BeautifulSoup(text, "html.parser")
    except Exception:
        return None


def _read_lines(path: Path) -> list[str]:
    """Read a file and return its lines (empty list on error)."""
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []


class _CodeContextTracker:
    """Track whether lines are inside code blocks or HTML comments across
    multiple lines, so Japanese text in code examples is properly skipped."""

    def __init__(self):
        self.in_pre = 0
        self.in_code = 0
        self.in_script = 0
        self.in_style = 0
        self.in_comment = False

    def is_inside(self, line: str) -> bool:
        stripped = line.strip()

        # Track HTML comments (<!-- ... -->)
        if self.in_comment:
            if "-->" in line:
                self.in_comment = False
            return True
        if "<!--" in line:
            if "-->" not in line or line.index("<!--") > line.index("-->"):
                self.in_comment = True
                return True
            # Single-line comment - check if it has Japanese
            return True

        # Code-fenced lines
        if stripped.startswith("```"):
            return True

        # Track <pre>, <code>, <script>, <style> blocks
        pre_opens = line.count("<pre")
        pre_closes = line.count("</pre")
        code_opens = line.count("<code")
        code_closes = line.count("</code")
        script_opens = line.count("<script")
        script_closes = line.count("</script")
        style_opens = line.count("<style")
        style_closes = line.count("</style")

        was_inside = self.in_pre > 0 or self.in_code > 0 or self.in_script > 0 or self.in_style > 0
        has_any_tag = (pre_opens + pre_closes + code_opens + code_closes +
                       script_opens + script_closes + style_opens + style_closes) > 0

        self.in_pre = max(0, self.in_pre + pre_opens - pre_closes)
        self.in_code = max(0, self.in_code + code_opens - code_closes)
        self.in_script = max(0, self.in_script + script_opens - script_closes)
        self.in_style = max(0, self.in_style + style_opens - style_closes)

        now_inside = self.in_pre > 0 or self.in_code > 0 or self.in_script > 0 or self.in_style > 0

        # 同一行で開閉する場合 (e.g. <pre>...</pre>) はカウンタが相殺され
        # now_inside が False になるため、ブロック要素の開始タグで別途検出する。
        # インライン <code> は除外（行内テキストの検査を妨げないようにする）
        has_block_open = (
            pre_opens > 0 or script_opens > 0 or style_opens > 0
        )
        return was_inside or now_inside or (has_any_tag and has_block_open)


def _is_inside_code_context(line: str) -> bool:
    """Rough heuristic: return True if line looks like it's inside a code block,
    contains file paths, CSS class names, or technical patterns.
    NOTE: For stateful tracking across lines, use _CodeContextTracker instead."""
    stripped = line.strip()
    # Lines that are code-fenced
    if stripped.startswith("```"):
        return True
    # Lines inside <code> or <pre> (inline check)
    if "<code" in line or "<pre" in line or "</code>" in line or "</pre>" in line:
        return True
    return False


def _extract_japanese_snippet(
    text: str,
    pattern: re.Pattern,
    *,
    context_chars: int = 30,
) -> str | None:
    """Extract a single representative Japanese text snippet from a string.

    Returns the first contiguous run of Japanese characters with surrounding
    context, or None if no match.
    """
    # Find contiguous runs of Japanese characters (possibly mixed with
    # punctuation, spaces, and ASCII) to form meaningful snippets.
    m = pattern.search(text)
    if m is None:
        return None
    start = max(0, m.start() - context_chars)
    end = min(len(text), m.end() + context_chars)
    snippet = text[start:end].strip().replace("\n", " ")
    return snippet


def _is_excluded_japanese_context(element, attr_value: str | None = None) -> bool:
    """Check if a BeautifulSoup element is inside a code/pre block or similar."""
    # Check if inside <code>, <pre>, <script>, <style>
    for parent in element.parents:
        if parent.name in ("code", "pre", "script", "style", "kbd", "samp"):
            return True
    return False


def _resolve_link(href: str, html_path: Path, lang_dir: Path) -> Path | None:
    """Resolve an href to an absolute filesystem path.

    Returns None for external URLs, anchors, javascript:, mailto:, etc.
    """
    if not href or href.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
        return None
    if href.startswith(("http://", "https://", "//")):
        return None

    # Strip fragment and query
    href_clean = href.split("#")[0].split("?")[0]
    if not href_clean:
        return None

    # URL-decode
    href_clean = urllib.parse.unquote(href_clean)

    # Resolve relative to the HTML file's directory
    resolved = (html_path.parent / href_clean).resolve()
    return resolved


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------

def check_original_text_residue(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Scan for Japanese characters remaining in translated files."""
    result = CheckResult("original_text_residue")
    result.total = len(html_files)

    # For EN and ES, detect hiragana/katakana (definitely Japanese).
    # For EN only, also detect kanji (could be Chinese but in this context it's Japanese).
    # For ES, hiragana/katakana are enough (kanji is not used in Spanish).
    if lang == "es":
        pattern = RE_HIRAGANA_KATAKANA
    else:
        pattern = RE_JAPANESE_ALL

    clean_count = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            result.add_issue(Issue(
                _relative(html_path, lang_dir),
                None,
                "Failed to parse HTML",
            ))
            continue

        # Remove elements that should be excluded from checks
        for excluded in soup.find_all(["code", "pre", "script", "style", "kbd", "samp"]):
            excluded.decompose()

        # Also remove HTML comments
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            comment.extract()

        file_has_issue = False
        lines = _read_lines(html_path)
        tracker = _CodeContextTracker()
        # Use line-based scanning for precise line numbers, but only
        # on visible text content (not tags/attributes)
        for lineno, line in enumerate(lines, 1):
            if tracker.is_inside(line):
                continue

            # Remove content inside inline <code>, <pre>, <kbd>, <samp> tags
            text_only = re.sub(r"<(code|pre|kbd|samp)[^>]*>.*?</\1>", " ", line, flags=re.DOTALL)

            # Skip lines that are purely HTML tags with class names / file paths
            # Strip HTML tags to get text content only
            text_only = re.sub(r"<[^>]+>", " ", text_only)

            # Also skip CSS class references, file paths
            # Remove quoted attribute values (src="...", class="...", href="...")
            text_only = re.sub(r'(?:src|href|class|id|style|data-\w+)\s*=\s*"[^"]*"', " ", text_only)
            text_only = re.sub(r"(?:src|href|class|id|style|data-\w+)\s*=\s*'[^']*'", " ", text_only)

            # Remove file path patterns
            text_only = re.sub(r"[\w./\\-]+\.\w{1,5}", " ", text_only)

            # Remove Japanese example text in quotation marks (「...」) used
            # as intentional teaching examples (e.g., proofreading lessons)
            text_only = re.sub(r"「[^」]*」", " ", text_only)
            text_only = re.sub(r"『[^』]*』", " ", text_only)

            # Also remove Japanese text inside double/single quotes – these
            # are intentional references (e.g., "はい", "日本語", 'サーバー')
            text_only = re.sub(r'"[^"]*"', " ", text_only)
            text_only = re.sub(r"'[^']*'", " ", text_only)

            if pattern.search(text_only):
                # Extract one representative snippet per line
                snippet = _extract_japanese_snippet(
                    text_only, pattern, context_chars=20,
                )
                if snippet:
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        lineno,
                        snippet[:80],
                    ))
                    file_has_issue = True

        if not file_has_issue:
            clean_count += 1

    result.passed = clean_count
    return result


def check_lang_attribute(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify <html lang="..."> is set to the correct language."""
    result = CheckResult("lang_attribute")
    result.total = len(html_files)
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            result.add_issue(Issue(
                _relative(html_path, lang_dir), None, "Failed to parse HTML",
            ))
            continue
        html_tag = soup.find("html")
        if html_tag is None:
            result.add_issue(Issue(
                _relative(html_path, lang_dir), None, "No <html> tag found",
            ))
            continue
        actual_lang = html_tag.get("lang", "")
        if actual_lang != lang:
            result.add_issue(Issue(
                _relative(html_path, lang_dir),
                None,
                f'lang="{actual_lang}" (expected "{lang}")',
            ))
        else:
            passed += 1
    result.passed = passed
    return result


def check_charset(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify <meta charset="UTF-8"> exists."""
    result = CheckResult("charset_check")
    result.total = len(html_files)
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            result.add_issue(Issue(
                _relative(html_path, lang_dir), None, "Failed to parse HTML",
            ))
            continue
        meta = soup.find("meta", attrs={"charset": True})
        if meta and meta.get("charset", "").upper() == "UTF-8":
            passed += 1
        else:
            result.add_issue(Issue(
                _relative(html_path, lang_dir),
                None,
                "Missing or incorrect <meta charset=\"UTF-8\">",
            ))
    result.passed = passed
    return result


def check_alt_attributes(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check all <img> tags have alt attributes that are not in Japanese."""
    result = CheckResult("alt_attribute")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for img in soup.find_all("img"):
            result.total += 1
            alt = img.get("alt")
            if alt is None:
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'<img> missing alt attribute (src="{img.get("src", "?")}")',
                ))
            elif RE_JAPANESE_ALL.search(alt):
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'alt text contains Japanese: "{alt[:60]}"',
                ))
            else:
                passed += 1
    result.passed = passed
    return result


def check_title_attributes(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check all elements with title attributes are translated."""
    result = CheckResult("title_attribute")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for el in soup.find_all(attrs={"title": True}):
            if _is_excluded_japanese_context(el):
                continue
            result.total += 1
            title_val = el.get("title", "")
            if RE_JAPANESE_ALL.search(title_val):
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'title contains Japanese: "{title_val[:60]}"',
                ))
            else:
                passed += 1
    result.passed = passed
    return result


def check_meta_tags(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check <meta name='description'>, og:title, etc. are translated."""
    result = CheckResult("meta_tags")
    result.total = 0
    passed = 0

    meta_names = {"description", "keywords", "author"}
    og_properties = {
        "og:title",
        "og:description",
        "og:site_name",
        "twitter:title",
        "twitter:description",
    }

    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue

        # Check <title> tag
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            result.total += 1
            if RE_JAPANESE_ALL.search(title_tag.string):
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'<title> contains Japanese: "{title_tag.string[:60]}"',
                ))
            else:
                passed += 1

        # Check <meta name="..."> tags
        for name in meta_names:
            meta = soup.find("meta", attrs={"name": name})
            if meta:
                content = meta.get("content", "")
                result.total += 1
                if RE_JAPANESE_ALL.search(content):
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        None,
                        f'meta[name="{name}"] contains Japanese: "{content[:60]}"',
                    ))
                else:
                    passed += 1

        # Check <meta property="og:..."> tags
        for prop in og_properties:
            meta = soup.find("meta", attrs={"property": prop})
            if meta:
                content = meta.get("content", "")
                result.total += 1
                if RE_JAPANESE_ALL.search(content):
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        None,
                        f'meta[property="{prop}"] contains Japanese: "{content[:60]}"',
                    ))
                else:
                    passed += 1

    result.passed = passed
    return result


def check_aria_labels(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check all aria-label attributes are translated."""
    result = CheckResult("aria_labels")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for el in soup.find_all(attrs={"aria-label": True}):
            result.total += 1
            val = el.get("aria-label", "")
            if RE_JAPANESE_ALL.search(val):
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'aria-label contains Japanese: "{val[:60]}"',
                ))
            else:
                passed += 1
    result.passed = passed
    return result


def check_placeholders(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check all placeholder attributes are translated."""
    result = CheckResult("placeholder_check")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for el in soup.find_all(attrs={"placeholder": True}):
            result.total += 1
            val = el.get("placeholder", "")
            if RE_JAPANESE_ALL.search(val):
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'placeholder contains Japanese: "{val[:60]}"',
                ))
            else:
                passed += 1
    result.passed = passed
    return result


def check_internal_links(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify all internal links point to files that exist within dist/{lang}/."""
    result = CheckResult("internal_links")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for a_tag in soup.find_all("a", href=True):
            # Skip language switcher links (intentionally cross directories)
            classes = a_tag.get("class", [])
            if isinstance(classes, str):
                classes = classes.split()
            if "lang-btn" in classes:
                continue
            href = a_tag["href"]
            resolved = _resolve_link(href, html_path, lang_dir)
            if resolved is None:
                continue  # external or anchor-only
            result.total += 1
            if resolved.exists():
                # Also check it's within the lang_dir (not escaping)
                try:
                    resolved.relative_to(lang_dir.resolve())
                    passed += 1
                except ValueError:
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        None,
                        f'Link escapes lang directory: "{href}"',
                    ))
            else:
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'Broken link: "{href}"',
                ))
    result.passed = passed
    return result


def check_nav_links(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify next/previous navigation links point to the correct language version."""
    result = CheckResult("nav_links")
    result.total = 0
    passed = 0

    # Common patterns for next/prev navigation
    nav_patterns = [
        re.compile(r"(next|prev|previous|forward|back)", re.IGNORECASE),
    ]

    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue

        # Find links with rel="next" or rel="prev"
        for a_tag in soup.find_all("a", href=True):
            rel = a_tag.get("rel", [])
            classes = a_tag.get("class", [])
            text = a_tag.get_text(strip=True).lower()

            is_nav = False
            if isinstance(rel, list) and any(r in ("next", "prev", "previous") for r in rel):
                is_nav = True
            elif any(p.search(" ".join(classes)) for p in nav_patterns if classes):
                is_nav = True
            elif any(p.search(text) for p in nav_patterns):
                is_nav = True

            # Also check for common nav class patterns
            if not is_nav:
                for cls in (classes if isinstance(classes, list) else [classes]):
                    if any(kw in str(cls).lower() for kw in ("nav-next", "nav-prev", "pagination")):
                        is_nav = True
                        break

            if not is_nav:
                continue

            href = a_tag["href"]
            resolved = _resolve_link(href, html_path, lang_dir)
            if resolved is None:
                continue

            result.total += 1

            # Check the link resolves within this lang dir
            if resolved.exists():
                try:
                    resolved.relative_to(lang_dir.resolve())
                    passed += 1
                except ValueError:
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        None,
                        f'Nav link escapes lang directory: "{href}"',
                    ))
            else:
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'Broken nav link: "{href}"',
                ))

    result.passed = passed
    return result


def check_image_references(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify all <img src="..."> reference files that actually exist.

    Images that are also missing in the original Japanese source are excluded,
    since those are source-level issues, not i18n translation issues.
    """
    result = CheckResult("image_references")
    result.total = 0
    passed = 0

    # Determine the source course directory for cross-checking
    source_course_dir = lang_dir.parent.parent  # dist/{lang} -> dist -> course
    if source_course_dir.name == "dist":
        source_course_dir = source_course_dir.parent  # course/

    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for img in soup.find_all("img", src=True):
            src = img["src"]
            # Skip data URIs and external URLs
            if src.startswith(("data:", "http://", "https://", "//")):
                continue
            result.total += 1
            resolved = _resolve_link(src, html_path, lang_dir)
            if resolved and resolved.exists():
                passed += 1
            else:
                # Check if this image is also missing in the source
                rel_html = html_path.relative_to(lang_dir)
                source_html = source_course_dir / rel_html
                if source_html.exists():
                    source_img = source_html.parent / src
                    if not source_img.exists():
                        # Also missing in source - not an i18n issue
                        passed += 1
                        continue
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'Missing image: "{src}"',
                ))
    result.passed = passed
    return result


def check_template_vars(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check no {{PLACEHOLDER}} template variables remain unprocessed."""
    result = CheckResult("template_vars")
    result.total = len(html_files)
    passed = 0
    for html_path in html_files:
        lines = _read_lines(html_path)
        file_clean = True
        for lineno, line in enumerate(lines, 1):
            matches = RE_TEMPLATE_VAR.findall(line)
            for match in matches:
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    lineno,
                    f"Unprocessed template variable: {match}",
                ))
                file_clean = False
        if file_clean:
            passed += 1
    result.passed = passed
    return result


def check_css_loading(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Verify CSS file references resolve to actual files."""
    result = CheckResult("css_loading")
    result.total = 0
    passed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for link in soup.find_all("link", rel="stylesheet"):
            href = link.get("href", "")
            # Skip CDN / external stylesheets
            if href.startswith(("http://", "https://", "//")):
                continue
            if not href:
                continue
            result.total += 1
            resolved = _resolve_link(href, html_path, lang_dir)
            if resolved and resolved.exists():
                passed += 1
            else:
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'Missing CSS file: "{href}"',
                ))
    result.passed = passed
    return result


def check_relative_paths(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check no paths accidentally reference the Japanese source by escaping dist."""
    result = CheckResult("relative_paths")
    result.total = 0
    passed = 0

    # Patterns that might escape the dist/{lang}/ directory
    # e.g., ../../assets/ from dist/en/foundation/ would reach course/assets/
    # which is the Japanese source

    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue

        # Collect all local resource references
        refs: list[tuple[str, str]] = []  # (tag_desc, href)
        for a_tag in soup.find_all("a", href=True):
            # Skip language switcher links (intentionally point outside dist)
            classes = a_tag.get("class", [])
            if isinstance(classes, str):
                classes = classes.split()
            if "lang-btn" in classes:
                continue
            refs.append(("a[href]", a_tag["href"]))
        for img in soup.find_all("img", src=True):
            refs.append(("img[src]", img["src"]))
        for link in soup.find_all("link", href=True):
            refs.append(("link[href]", link["href"]))
        for script in soup.find_all("script", src=True):
            refs.append(("script[src]", script["src"]))

        for tag_desc, ref in refs:
            # Skip external
            if ref.startswith(("http://", "https://", "//", "#", "javascript:", "mailto:", "tel:", "data:")):
                continue
            if not ref:
                continue

            result.total += 1
            resolved = _resolve_link(ref, html_path, lang_dir)
            if resolved is None:
                passed += 1
                continue

            # Check if resolved path is outside the lang_dir
            try:
                resolved.relative_to(lang_dir.resolve())
                passed += 1
            except ValueError:
                # The path escapes the lang dir -- this is a problem
                result.add_issue(Issue(
                    _relative(html_path, lang_dir),
                    None,
                    f'{tag_desc} escapes dist directory: "{ref}" -> {resolved}',
                ))

    result.passed = passed
    return result


def check_translation_coverage(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Compare keys in ja.json vs {lang}.json, report missing translations."""
    result = CheckResult("translation_coverage")

    ja_json = LOCALES_DIR / "ja.json"
    lang_json = LOCALES_DIR / f"{lang}.json"

    if not ja_json.exists():
        result.status = "WARN"
        result.add_issue(Issue(
            str(ja_json.relative_to(ROOT_DIR)),
            None,
            "ja.json not found in locales/; skipping coverage check",
            severity="WARN",
        ))
        return result

    if not lang_json.exists():
        result.status = "WARN"
        result.add_issue(Issue(
            str(lang_json.relative_to(ROOT_DIR)),
            None,
            f"{lang}.json not found in locales/; skipping coverage check",
            severity="WARN",
        ))
        return result

    try:
        ja_data = json.loads(ja_json.read_text(encoding="utf-8"))
        lang_data = json.loads(lang_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        result.add_issue(Issue(
            "locales/", None, f"Failed to parse JSON: {exc}",
        ))
        return result

    def _flatten_keys(d: dict, prefix: str = "") -> set[str]:
        keys: set[str] = set()
        for k, v in d.items():
            full_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                keys.update(_flatten_keys(v, full_key))
            else:
                keys.add(full_key)
        return keys

    ja_keys = _flatten_keys(ja_data)
    lang_keys = _flatten_keys(lang_data)

    result.total = len(ja_keys)
    missing = ja_keys - lang_keys
    result.passed = result.total - len(missing)

    if missing:
        pct = (result.passed / result.total * 100) if result.total > 0 else 0.0
        result.status = "WARN"
        result.add_issue(Issue(
            f"locales/{lang}.json",
            None,
            f"{pct:.1f}% coverage ({len(missing)} keys missing)",
            severity="WARN",
        ))
        if verbose:
            for key in sorted(missing):
                result.add_issue(Issue(
                    f"locales/{lang}.json",
                    None,
                    f"Missing key: {key}",
                    severity="WARN",
                ))

    return result


def check_image_coverage(
    lang: str,
    lang_dir: Path,
    html_files: list[Path],
    verbose: bool = False,
) -> CheckResult:
    """Check that all images referenced in HTML exist in dist/{lang}/assets/images/."""
    result = CheckResult("image_coverage")
    result.total = 0
    passed = 0

    images_dir = lang_dir / "assets" / "images"

    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if src.startswith(("data:", "http://", "https://", "//")):
                continue

            # Only check images that are meant to be in assets/images/
            resolved = _resolve_link(src, html_path, lang_dir)
            if resolved is None:
                continue

            # Check if this image is supposed to be under assets/images/
            try:
                rel = resolved.relative_to(lang_dir.resolve())
                rel_str = str(rel)
            except ValueError:
                continue

            if rel_str.startswith("assets/images/") or rel_str.startswith("assets\\images\\"):
                result.total += 1
                if resolved.exists():
                    passed += 1
                else:
                    result.add_issue(Issue(
                        _relative(html_path, lang_dir),
                        None,
                        f'Image not found in assets/images/: "{src}"',
                    ))

    result.passed = passed
    return result


# ---------------------------------------------------------------------------
# Auto-fix functions
# ---------------------------------------------------------------------------

def fix_lang_attribute(lang: str, lang_dir: Path, html_files: list[Path]) -> int:
    """Fix <html lang="..."> to the correct language. Returns number of files fixed."""
    fixed = 0
    for html_path in html_files:
        text = html_path.read_text(encoding="utf-8")
        # Replace lang="ja" or any other incorrect lang in <html> tag
        new_text, count = re.subn(
            r'(<html\b[^>]*\s)lang="[^"]*"',
            rf'\1lang="{lang}"',
            text,
        )
        if count == 0:
            # Try adding lang attribute if missing
            new_text, count = re.subn(
                r"<html\b",
                f'<html lang="{lang}"',
                text,
                count=1,
            )
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8")
            fixed += 1
    return fixed


def fix_charset(lang: str, lang_dir: Path, html_files: list[Path]) -> int:
    """Ensure <meta charset="UTF-8"> exists. Returns number of files fixed."""
    fixed = 0
    for html_path in html_files:
        soup = _parse_html(html_path)
        if soup is None:
            continue
        meta = soup.find("meta", attrs={"charset": True})
        if meta and meta.get("charset", "").upper() == "UTF-8":
            continue
        # Read raw text and fix/add charset
        text = html_path.read_text(encoding="utf-8")
        if meta:
            # Fix existing charset
            new_text = re.sub(
                r'<meta\s+charset="[^"]*"',
                '<meta charset="UTF-8"',
                text,
            )
        else:
            # Add charset after <head>
            new_text = re.sub(
                r"(<head[^>]*>)",
                r'\1\n    <meta charset="UTF-8" />',
                text,
                count=1,
            )
        if new_text != text:
            html_path.write_text(new_text, encoding="utf-8")
            fixed += 1
    return fixed


# ---------------------------------------------------------------------------
# Check registry
# ---------------------------------------------------------------------------

# Map of check name -> check function
CHECK_REGISTRY: dict[str, Callable] = {
    "original_text_residue": check_original_text_residue,
    "lang_attribute": check_lang_attribute,
    "charset_check": check_charset,
    "alt_attribute": check_alt_attributes,
    "title_attribute": check_title_attributes,
    "meta_tags": check_meta_tags,
    "aria_labels": check_aria_labels,
    "placeholder_check": check_placeholders,
    "internal_links": check_internal_links,
    "nav_links": check_nav_links,
    "image_references": check_image_references,
    "template_vars": check_template_vars,
    "css_loading": check_css_loading,
    "relative_paths": check_relative_paths,
    "translation_coverage": check_translation_coverage,
    "image_coverage": check_image_coverage,
}

# Map of fixable check name -> fix function
FIX_REGISTRY: dict[str, Callable] = {
    "lang_attribute": fix_lang_attribute,
    "charset_check": fix_charset,
}


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_text_report(lang: str, results: list[CheckResult], verbose: bool = False) -> str:
    """Format results as a human-readable text report."""
    lines: list[str] = []
    lines.append(f"=== i18n QA Report for {lang.upper()} ===")

    pass_count = 0
    fail_count = 0
    warn_count = 0

    for r in results:
        status_tag = f"[{r.status}]"
        # Summary line
        if r.total > 0:
            summary = f"{r.passed}/{r.total}"
            if r.name == "translation_coverage" and r.total > 0:
                pct = r.passed / r.total * 100
                summary = f"{pct:.1f}% ({r.total - r.passed} keys missing)"
        else:
            summary = "0 items checked"

        if r.status == "PASS":
            msg = f"{summary} OK"
            pass_count += 1
        elif r.status == "FAIL":
            msg = f"{len(r.issues)} issue(s)"
            fail_count += 1
        else:  # WARN
            msg = f"{len(r.issues)} warning(s)"
            warn_count += 1

        lines.append(f"{status_tag} {r.name}: {msg}")

        # Show issues (always for FAIL, only in verbose for WARN)
        if r.status == "FAIL" or (r.status == "WARN" and verbose):
            max_issues = 20 if not verbose else len(r.issues)
            for issue in r.issues[:max_issues]:
                lines.append(str(issue))
            if len(r.issues) > max_issues:
                lines.append(f"  ... and {len(r.issues) - max_issues} more")

    lines.append("")
    parts = []
    if pass_count:
        parts.append(f"{pass_count} PASS")
    if fail_count:
        parts.append(f"{fail_count} FAIL")
    if warn_count:
        parts.append(f"{warn_count} WARN")
    lines.append(f"Summary: {', '.join(parts)}")

    return "\n".join(lines)


def format_json_report(lang: str, results: list[CheckResult]) -> dict[str, Any]:
    """Format results as a JSON-serializable dict."""
    pass_count = sum(1 for r in results if r.status == "PASS")
    fail_count = sum(1 for r in results if r.status == "FAIL")
    warn_count = sum(1 for r in results if r.status == "WARN")
    return {
        "lang": lang,
        "summary": {
            "pass": pass_count,
            "fail": fail_count,
            "warn": warn_count,
            "total_checks": len(results),
        },
        "checks": [r.to_dict() for r in results],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_checks(
    lang: str,
    *,
    check_names: list[str] | None = None,
    verbose: bool = False,
) -> list[CheckResult]:
    """Run all (or specified) checks for a language and return results."""
    lang_dir = DIST_DIR / lang
    if not lang_dir.is_dir():
        result = CheckResult("setup")
        result.add_issue(Issue(
            str(lang_dir.relative_to(ROOT_DIR)),
            None,
            f"Directory does not exist: {lang_dir}",
        ))
        return [result]

    html_files = _collect_html_files(lang_dir)
    if not html_files:
        result = CheckResult("setup")
        result.add_issue(Issue(
            str(lang_dir.relative_to(ROOT_DIR)),
            None,
            f"No HTML files found in {lang_dir}",
        ))
        return [result]

    checks_to_run = check_names or list(CHECK_REGISTRY.keys())
    results: list[CheckResult] = []
    for name in checks_to_run:
        fn = CHECK_REGISTRY.get(name)
        if fn is None:
            r = CheckResult(name)
            r.add_issue(Issue("", None, f"Unknown check: {name}"))
            results.append(r)
            continue
        results.append(fn(lang, lang_dir, html_files, verbose=verbose))

    return results


def run_fixes(lang: str) -> dict[str, int]:
    """Run auto-fixes for a language. Returns dict of check_name -> files_fixed."""
    lang_dir = DIST_DIR / lang
    if not lang_dir.is_dir():
        return {}

    html_files = _collect_html_files(lang_dir)
    if not html_files:
        return {}

    fixed: dict[str, int] = {}
    for name, fn in FIX_REGISTRY.items():
        count = fn(lang, lang_dir, html_files)
        if count > 0:
            fixed[name] = count

    return fixed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="i18n QA checking tool for translated HTML course files",
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        required=True,
        help="Language code(s) to check (e.g., en es)",
    )
    parser.add_argument(
        "--checks",
        type=str,
        default=None,
        help="Comma-separated list of check names to run (default: all)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix simple issues (lang attribute, charset)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output report as JSON",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including all warnings",
    )
    args = parser.parse_args()

    check_names = None
    if args.checks:
        check_names = [c.strip() for c in args.checks.split(",")]
        # Validate check names
        for name in check_names:
            if name not in CHECK_REGISTRY:
                print(
                    f"ERROR: Unknown check '{name}'. Available: {', '.join(CHECK_REGISTRY)}",
                    file=sys.stderr,
                )
                return 2

    has_failure = False
    all_reports: list[dict[str, Any]] = []

    for lang in args.lang:
        # Run fixes first if requested
        if args.fix:
            fixed = run_fixes(lang)
            if fixed:
                if not args.json_output:
                    print(f"=== Auto-fixes applied for {lang.upper()} ===")
                    for name, count in fixed.items():
                        print(f"  Fixed {name}: {count} file(s)")
                    print()

        # Run checks
        results = run_checks(lang, check_names=check_names, verbose=args.verbose)

        if args.json_output:
            all_reports.append(format_json_report(lang, results))
        else:
            print(format_text_report(lang, results, verbose=args.verbose))
            print()

        if any(r.status == "FAIL" for r in results):
            has_failure = True

    if args.json_output:
        output = all_reports if len(all_reports) > 1 else all_reports[0] if all_reports else {}
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return 1 if has_failure else 0


if __name__ == "__main__":
    sys.exit(main())
