"""Module 18 (AI秘書 Google Workspace) の構造テスト

レッスンコマンド（start-18-1 〜 start-18-7）の存在と整合性を検証する。
旧 Module 18 は PM & システム要件定義だったが、現在は Google Workspace に変更済み。
"""
import pytest
import yaml
from pathlib import Path


@pytest.fixture
def skills_dir(project_root):
    return project_root / ".claude" / "skills"


@pytest.fixture
def commands_dir(project_root):
    return project_root / ".cursor" / "commands" / "lesson"


# ---------------------------------------------------------------------------
# スキル構造テスト（Google Workspace 関連スキルが存在すれば検証）
# ---------------------------------------------------------------------------

class TestPmToolkitSkill:
    """pm-toolkit スキルは他モジュールで使用されるため存在確認のみ"""

    def test_skill_md_exists(self, skills_dir):
        path = skills_dir / "pm-toolkit" / "SKILL.md"
        assert path.exists(), f"SKILL.md not found: {path}"

    def test_skill_md_has_frontmatter(self, skills_dir):
        text = (skills_dir / "pm-toolkit" / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---"), "SKILL.md should start with YAML frontmatter"
        parts = text.split("---", 2)
        assert len(parts) >= 3, "SKILL.md should have opening and closing ---"
        fm = yaml.safe_load(parts[1])
        assert "name" in fm
        assert fm["name"] == "pm-toolkit"
        assert "description" in fm


class TestTestPlannerSkill:
    def test_skill_md_exists(self, skills_dir):
        path = skills_dir / "test-planner" / "SKILL.md"
        assert path.exists(), f"SKILL.md not found: {path}"

    def test_skill_md_has_frontmatter(self, skills_dir):
        text = (skills_dir / "test-planner" / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---")
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert fm["name"] == "test-planner"


class TestMonitoringDashboardSkill:
    def test_skill_md_exists(self, skills_dir):
        path = skills_dir / "monitoring-dashboard" / "SKILL.md"
        assert path.exists()

    def test_script_exists(self, skills_dir):
        path = skills_dir / "monitoring-dashboard" / "scripts" / "main.py"
        assert path.exists(), f"main.py not found: {path}"

    def test_skill_md_has_frontmatter(self, skills_dir):
        text = (skills_dir / "monitoring-dashboard" / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---")
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert fm["name"] == "monitoring-dashboard"


# ---------------------------------------------------------------------------
# レッスンコマンド構造テスト（Module 18: AI秘書 Google Workspace）
# ---------------------------------------------------------------------------

TOTAL_LESSONS = 20  # start-18-1 ~ start-18-20


class TestLessonCommands:
    """全20レッスンのコマンドファイルが正しく構成されているか検証"""

    @pytest.mark.parametrize("n", range(1, TOTAL_LESSONS + 1))
    def test_lesson_file_exists(self, commands_dir, n):
        path = commands_dir / f"start-18-{n}.md"
        assert path.exists(), f"Missing: {path}"

    @pytest.mark.parametrize("n", range(1, TOTAL_LESSONS + 1))
    def test_lesson_has_frontmatter(self, commands_dir, n):
        text = (commands_dir / f"start-18-{n}.md").read_text(encoding="utf-8")
        assert text.startswith("---"), f"start-18-{n}.md missing frontmatter"
        parts = text.split("---", 2)
        assert len(parts) >= 3
        fm = yaml.safe_load(parts[1])
        assert "description" in fm, f"start-18-{n}.md missing description"

    @pytest.mark.parametrize("n", range(1, TOTAL_LESSONS + 1))
    def test_lesson_has_duration(self, commands_dir, n):
        text = (commands_dir / f"start-18-{n}.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert "duration" in fm, f"start-18-{n}.md missing duration"

    def test_total_lesson_count(self, commands_dir):
        files = list(commands_dir.glob("start-18-*.md"))
        assert len(files) == TOTAL_LESSONS, (
            f"Expected {TOTAL_LESSONS} lesson files, found {len(files)}"
        )


# ---------------------------------------------------------------------------
# HTML 教材構造テスト（コースディレクトリが存在する場合のみ）
# ---------------------------------------------------------------------------

class TestCourseStructure:
    @pytest.fixture(autouse=True)
    def _skip_if_no_course(self, project_root):
        # Module 18 の course ディレクトリはまだ存在しない可能性がある
        candidates = [
            project_root / "course" / "modules" / "18-google-workspace",
            project_root / "course" / "modules" / "18-pm-sysdef",
        ]
        for d in candidates:
            if d.exists():
                self.course_dir = d
                return
        pytest.skip("course directory for module 18 not found")

    def test_index_html_exists(self):
        assert (self.course_dir / "index.html").exists()


# ---------------------------------------------------------------------------
# 演習ファイル構造テスト
# ---------------------------------------------------------------------------

class TestExercises:
    """演習ディレクトリが未作成でも、レッスンコマンドの存在で代替検証する"""

    def test_lesson_commands_exist_for_module_18(self, project_root):
        """Module 18 のレッスンコマンドが .claude/commands/lesson/ に存在すること"""
        claude_cmds = project_root / ".claude" / "commands" / "lesson"
        files = sorted(claude_cmds.glob("start-18-*.md"))
        assert len(files) > 0, (
            f"Module 18 のレッスンコマンドが見つかりません: {claude_cmds}"
        )
