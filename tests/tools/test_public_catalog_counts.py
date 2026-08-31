"""Snapshot public README catalog numbers against this repo and the web-course labels.

Repo-derived figures come from courses/lessons.manifest.yaml and course.yaml.
Web-catalog figures (47 modules, 50–60 hours) are labeled claims that must
match https://ai-agent.camp as of 2026-08-31 — do not invent 200+ lessons.
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
README_FILES = (
    REPO_ROOT / "README.md",
    REPO_ROOT / "README.ja.md",
    REPO_ROOT / "README.es.md",
)
STALE_MARKETING = (
    "28 modules, 100+ lessons",
    "28モジュール、100以上のレッスン",
    "28 modulos, mas de 100 lecciones",
    "approx. 24 hours (30+ hours",
    "約24時間（演習込みで約30時間以上）",
    "aprox. 24 horas (mas de 30 horas",
    "Native Windows (PowerShell / cmd) is not supported",
    "Windows ネイティブ（PowerShell / cmd）はサポート対象外",
    "Windows nativo (PowerShell / cmd) no está soportado",
)


def _manifest_start_ids() -> list[str]:
    entries = yaml.safe_load(
        (REPO_ROOT / "courses/lessons.manifest.yaml").read_text(encoding="utf-8")
    )
    return [entry["lessonId"] for entry in entries if str(entry.get("lessonId", "")).startswith("start-")]


def _core_module_ids() -> list[str]:
    core = REPO_ROOT / "courses/aiagent/lesson03-core"
    return sorted(
        path.parent.name
        for path in core.glob("module*/chapter.yaml")
    )


def test_manifest_start_lesson_snapshot():
    ids = _manifest_start_ids()
    assert len(ids) == len(set(ids))
    assert len(ids) == 138, (
        f"start-* count in lessons.manifest.yaml is {len(ids)}; "
        "update the public README figures if this snapshot changes"
    )


def test_core_modules_skip_26_through_28():
    names = _core_module_ids()
    assert len(names) == 26
    numbers = [int(name.split("-", 1)[0].replace("module", "")) for name in names]
    assert 26 not in numbers
    assert 27 not in numbers
    assert 28 not in numbers
    assert 29 in numbers
    assert numbers == list(range(1, 26)) + [29]


def test_course_yaml_estimated_hours():
    course = yaml.safe_load(
        (REPO_ROOT / "courses/aiagent/course.yaml").read_text(encoding="utf-8")
    )
    assert course["estimatedHours"] == 50


def test_readmes_use_repo_or_labeled_web_catalog_figures():
    ids = _manifest_start_ids()
    lesson_count = str(len(ids))
    for path in README_FILES:
        text = path.read_text(encoding="utf-8")
        assert "https://ai-agent.camp" in text
        assert "47" in text
        assert lesson_count in text
        assert "50" in text
        for stale in STALE_MARKETING:
            assert stale not in text, f"{path.name} still advertises stale copy: {stale!r}"


def test_readmes_do_not_invent_200_plus_lessons():
    for path in README_FILES:
        text = path.read_text(encoding="utf-8")
        assert "200+" not in text
        assert "200以上" not in text
        assert "mas de 200" not in text
