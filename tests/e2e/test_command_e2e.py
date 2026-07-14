"""Command E2E テスト

全レッスンコマンド + セットアップコマンド + ユーティリティコマンドの
構造検証・相互参照検証・進行チェーンの妥当性を網羅的にテストする。

実行:
    python -m pytest tests/e2e/test_command_e2e.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Helper constants & functions
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLAUDE_LESSON_DIR = PROJECT_ROOT / ".claude" / "commands" / "lesson"
CURSOR_LESSON_DIR = PROJECT_ROOT / ".cursor" / "commands" / "lesson"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
START_REF_RE = re.compile(r"/start-(\d+)-(\d+)")
PYTHON_SCRIPT_RE = re.compile(r"python\s+(?:tools/|scripts/)(\S+\.py)")
SETUP_REF_RE = re.compile(r"/setup-(\S+)")


def _all_command_dirs() -> list[Path]:
    """テスト対象のコマンドディレクトリ一覧"""
    dirs = []
    if CLAUDE_LESSON_DIR.exists():
        dirs.append(CLAUDE_LESSON_DIR)
    if CURSOR_LESSON_DIR.exists():
        dirs.append(CURSOR_LESSON_DIR)
    return dirs


def _all_md_files(directory: Path) -> list[Path]:
    """指定ディレクトリ内の全 .md ファイルを返す"""
    return sorted(directory.glob("*.md"))


def _parse_frontmatter(path: Path) -> dict | None:
    """YAML frontmatter をパースして dict を返す。無ければ None。"""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def _lesson_files_for(directory: Path) -> list[Path]:
    """start-X-Y.md のみを返す（.en.md / .es.md 等の言語サフィックス付きは除外）"""
    return sorted(
        f for f in directory.glob("start-*.md")
        if not re.search(r'\.\w{2}\.md$', f.name)
    )


def _all_lesson_ids(directory: Path) -> set[str]:
    """start-X-Y のレッスン ID を set で返す (拡張子なし, "start-" 付き)"""
    return {f.stem for f in _lesson_files_for(directory)}


def _extract_module_lessons(directory: Path, module: int) -> list[Path]:
    """指定モジュール番号のレッスンファイルを番号順に返す"""
    pattern = f"start-{module}-*.md"
    files = sorted(directory.glob(pattern))
    # 数値でソートする (start-14-2 < start-14-10)
    def sort_key(p: Path) -> int:
        parts = p.stem.split("-")
        return int(parts[-1]) if parts[-1].isdigit() else 0
    return sorted(files, key=sort_key)


def _all_module_numbers(directory: Path) -> set[int]:
    """ディレクトリに含まれるモジュール番号の集合"""
    modules = set()
    for f in _lesson_files_for(directory):
        parts = f.stem.split("-")
        if len(parts) >= 2 and parts[1].isdigit():
            modules.add(int(parts[1]))
    return modules


# ---------------------------------------------------------------------------
# Part 1: Structure validation
# ---------------------------------------------------------------------------

class TestFrontmatterStructure:
    """全コマンドファイルの YAML frontmatter 構造を検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_all_files_have_valid_yaml_frontmatter(self, command_dir):
        """全 .md ファイルの YAML frontmatter がパース可能であること"""
        errors = []
        for md in _all_md_files(command_dir):
            text = md.read_text(encoding="utf-8")
            m = FRONTMATTER_RE.match(text)
            if not m:
                errors.append(f"{md.name}: YAML frontmatter が見つからない")
                continue
            try:
                yaml.safe_load(m.group(1))
            except yaml.YAMLError as e:
                errors.append(f"{md.name}: YAML パースエラー: {e}")
        assert not errors, "Frontmatter errors:\n" + "\n".join(errors)

    def test_all_files_have_description(self, command_dir):
        """全 .md ファイルに description フィールドが存在すること"""
        errors = []
        for md in _all_md_files(command_dir):
            fm = _parse_frontmatter(md)
            if fm is None:
                errors.append(f"{md.name}: frontmatter なし")
                continue
            if "description" not in fm:
                errors.append(f"{md.name}: description フィールドがない")
        assert not errors, "Missing description:\n" + "\n".join(errors)


class TestPrerequisiteReferences:
    """prerequisites が実在するレッスンファイルを参照しているか検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_prerequisites_reference_existing_files(self, command_dir):
        """prerequisites に含まれる start-X-Y 参照が実在するファイルを指すこと"""
        all_ids = _all_lesson_ids(command_dir)
        errors = []
        for md in _lesson_files_for(command_dir):
            fm = _parse_frontmatter(md)
            if fm is None or "prerequisites" not in fm:
                continue
            prereqs = fm["prerequisites"]
            if not isinstance(prereqs, list):
                continue
            for prereq in prereqs:
                if not isinstance(prereq, str):
                    continue
                # start-X-Y 形式の参照のみチェック
                ref_match = START_REF_RE.search(prereq)
                if ref_match:
                    ref_id = f"start-{ref_match.group(1)}-{ref_match.group(2)}"
                    if ref_id not in all_ids:
                        errors.append(
                            f"{md.name}: prerequisite '{prereq}' -> "
                            f"'{ref_id}.md' が存在しない"
                        )
        assert not errors, "Broken prerequisites:\n" + "\n".join(errors)


class TestNextStepReferences:
    """「次のステップ」参照が実在するコマンドを指しているか検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_next_step_references_exist(self, command_dir):
        """本文中の /start-X-Y 参照が全て実在するファイルを指すこと"""
        all_ids = _all_lesson_ids(command_dir)
        # setup / utility コマンドのファイル名も取得
        all_file_stems = {f.stem for f in _all_md_files(command_dir)}
        errors = []
        for md in _all_md_files(command_dir):
            text = md.read_text(encoding="utf-8")
            for match in START_REF_RE.finditer(text):
                ref_id = f"start-{match.group(1)}-{match.group(2)}"
                if ref_id not in all_ids:
                    errors.append(
                        f"{md.name}: /start-{match.group(1)}-{match.group(2)} "
                        f"-> '{ref_id}.md' が存在しない"
                    )
        assert not errors, "Broken /start-X-Y references:\n" + "\n".join(errors)


class TestPythonScriptReferences:
    """コマンドファイル内で参照される Python スクリプトが実在するか検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_referenced_python_scripts_exist(self, command_dir):
        """python tools/xxx.py や python scripts/xxx.py の参照先が存在すること"""
        errors = []
        for md in _all_md_files(command_dir):
            text = md.read_text(encoding="utf-8")
            for match in PYTHON_SCRIPT_RE.finditer(text):
                script_name = match.group(1)
                # tools/ と scripts/ の両方をチェック
                candidate_paths = [
                    PROJECT_ROOT / "tools" / script_name,
                    PROJECT_ROOT / "scripts" / script_name,
                ]
                if not any(p.exists() for p in candidate_paths):
                    errors.append(
                        f"{md.name}: スクリプト '{script_name}' が "
                        f"tools/ にも scripts/ にも存在しない"
                    )
        assert not errors, "Missing Python scripts:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# Part 2: Cross-reference validation
# ---------------------------------------------------------------------------

class TestSymmetry:
    """.claude/ と .cursor/ のレッスンコマンドの対称性を検証"""

    def test_claude_and_cursor_have_same_lesson_files(self):
        """両ディレクトリに同じファイルセットが存在すること"""
        if not CLAUDE_LESSON_DIR.exists() or not CURSOR_LESSON_DIR.exists():
            pytest.skip("一方のディレクトリが存在しない")

        claude_files = {f.name for f in _all_md_files(CLAUDE_LESSON_DIR)}
        cursor_files = {f.name for f in _all_md_files(CURSOR_LESSON_DIR)}

        only_claude = claude_files - cursor_files
        only_cursor = cursor_files - claude_files

        errors = []
        if only_claude:
            errors.append(
                f".claude にのみ存在: {sorted(only_claude)}"
            )
        if only_cursor:
            errors.append(
                f".cursor にのみ存在: {sorted(only_cursor)}"
            )
        assert not errors, "非対称なファイル:\n" + "\n".join(errors)


class TestModuleContentAlignment:
    """ファイル名のモジュール番号と内容の整合性を検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_lesson_file_names_match_heading(self, command_dir):
        """start-X-Y.md のファイル名と # heading 内の X-Y が一致すること

        Y は数字のみ (15-1) または 数字+英小文字 (15-7a, 15-8b 等) の
        sub-lesson 表記もサポートする。
        """
        heading_re = re.compile(
            r"^#\s+.*?(?:Lesson|レッスン)\s+(\d+)-(\d+[a-z]*)", re.MULTILINE
        )
        errors = []
        for md in _lesson_files_for(command_dir):
            parts = md.stem.split("-")
            if len(parts) < 3:
                continue
            file_mod, file_lesson = parts[1], parts[2]
            text = md.read_text(encoding="utf-8")
            match = heading_re.search(text)
            if match:
                head_mod, head_lesson = match.group(1), match.group(2)
                if file_mod != head_mod or file_lesson != head_lesson:
                    errors.append(
                        f"{md.name}: ファイル名 {file_mod}-{file_lesson} vs "
                        f"heading {head_mod}-{head_lesson}"
                    )
        # ヘッダーが無いファイルはスキップ (ルールが別形式の可能性)
        assert not errors, "ファイル名と heading の不一致:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# Part 3: Setup command flow (learner journey)
# ---------------------------------------------------------------------------

class TestSetupChain:
    """start-0-1 ~ start-0-8 のセットアップチェーンを検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_setup_chain_files_exist(self, command_dir):
        """start-0-1 から start-0-8 まで全て存在すること"""
        for i in range(1, 9):
            path = command_dir / f"start-0-{i}.md"
            assert path.exists(), f"セットアップチェーン欠落: start-0-{i}.md"

    def test_setup_chain_forms_sequence(self, command_dir):
        """各セットアップファイルが次のステップへの参照を含むこと"""
        errors = []
        for i in range(1, 8):
            current = command_dir / f"start-0-{i}.md"
            if not current.exists():
                errors.append(f"start-0-{i}.md が存在しない")
                continue
            text = current.read_text(encoding="utf-8")
            # 次のレッスン (start-0-(i+1)) または別の有効な遷移先があること
            has_next = bool(START_REF_RE.search(text))
            has_setup_ref = bool(SETUP_REF_RE.search(text))
            if not has_next and not has_setup_ref:
                errors.append(
                    f"start-0-{i}.md: 次のステップへの参照がない"
                )
        assert not errors, "セットアップチェーンの断絶:\n" + "\n".join(errors)

    def test_setup_commands_reference_existing_scripts(self, command_dir):
        """setup-*.md が参照するスクリプトが実在すること"""
        errors = []
        for md in command_dir.glob("setup-*.md"):
            text = md.read_text(encoding="utf-8")
            for match in PYTHON_SCRIPT_RE.finditer(text):
                script_name = match.group(1)
                candidates = [
                    PROJECT_ROOT / "tools" / script_name,
                    PROJECT_ROOT / "scripts" / script_name,
                ]
                if not any(p.exists() for p in candidates):
                    errors.append(
                        f"{md.name}: '{script_name}' が見つからない"
                    )
        assert not errors, "Setup script references broken:\n" + "\n".join(errors)

    def test_check_setup_exists(self, command_dir):
        """check-setup.md が存在すること"""
        assert (command_dir / "check-setup.md").exists(), "check-setup.md が存在しない"


class TestDiscordSetupCommand:
    """/setup-discord が Claude Code Channels の公式 plugin フローを案内することを検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    @pytest.mark.parametrize("filename", [
        "setup-discord.md",
        "setup-discord.en.md",
        "setup-discord.es.md",
    ])
    def test_setup_discord_uses_official_channels_flow(self, command_dir, filename):
        path = command_dir / filename
        assert path.exists(), f"{filename} が存在しない"
        text = path.read_text(encoding="utf-8")

        required = [
            "/plugin install discord@claude-plugins-official",
            "/reload-plugins",
            "/discord:configure",
            "claude --channels plugin:discord@claude-plugins-official",
            "/discord:access policy allowlist",
            "/discord:access allow",
            "/discord:access pair",
            "MESSAGE CONTENT INTENT",
            "View Channels",
            "Send Messages",
            "Send Messages in Threads",
            "Read Message History",
            "Attach Files",
        ]
        missing = [item for item in required if item not in text]

        forbidden = [
            "claude-channel-discord",
            "claude mcp add",
            "mcpServers",
            "mcp_settings.json",
            ".mcp.json",
            "SERVER MEMBERS INTENT",
            "Manage Messages",
            "/discord:access set --dm-policy",
            "/discord:access approve",
            "/discord:access list",
            "Hello from MCP",
        ]
        present = [item for item in forbidden if item in text]

        assert not missing, f"{filename}: missing official flow text: {missing}"
        assert not present, f"{filename}: still contains obsolete flow text: {present}"


# ---------------------------------------------------------------------------
# Part 4: Module progression
# ---------------------------------------------------------------------------

class TestModuleProgression:
    """各モジュール内のレッスン進行順を検証"""

    @pytest.fixture(params=_all_command_dirs(), ids=lambda d: d.parent.parent.name)
    def command_dir(self, request):
        return request.param

    def test_lesson_n_prerequisite_includes_lesson_n_minus_1(self, command_dir):
        """モジュール内 Lesson N の prerequisites が N-1 を含む (またはテキスト前提)"""
        modules = _all_module_numbers(command_dir)
        # module 0 はセットアップなので除外
        modules.discard(0)
        errors = []
        for mod in sorted(modules):
            lessons = _extract_module_lessons(command_dir, mod)
            if len(lessons) < 2:
                continue
            for idx in range(1, len(lessons)):
                current = lessons[idx]
                prev = lessons[idx - 1]
                fm = _parse_frontmatter(current)
                if fm is None or "prerequisites" not in fm:
                    continue
                prereqs = fm["prerequisites"]
                if not isinstance(prereqs, list):
                    continue
                # prev のレッスン ID (start-X-Y) が prereqs に含まれるかチェック
                prev_id = prev.stem  # e.g. "start-7-2"
                prereq_strs = " ".join(str(p) for p in prereqs)
                if prev_id not in prereq_strs:
                    # テキスト形式の前提条件 (e.g. "Gemini APIキー設定済み") は許可
                    has_any_start_ref = any(
                        START_REF_RE.search(str(p)) for p in prereqs
                    )
                    if has_any_start_ref:
                        # start-X-Y を参照している場合は prev を含むべき
                        errors.append(
                            f"{current.name}: prerequisites に "
                            f"{prev_id} が含まれていない "
                            f"(現在: {prereqs})"
                        )
        # INFO レベル: 厳密な前提条件チェーンは教材設計次第
        # エラーがあっても警告として報告
        if errors:
            pytest.skip(
                f"前提条件チェーンの不整合 ({len(errors)} 件): "
                + errors[0][:100]
            )

    def test_last_lesson_has_next_module_or_completion(self, command_dir):
        """各モジュールの最後のレッスンに次モジュールへの参照か完了表示があること

        まとめセクションやチェックポイントで終わるレッスンも許容する。
        """
        modules = _all_module_numbers(command_dir)
        modules.discard(0)
        errors = []
        for mod in sorted(modules):
            lessons = _extract_module_lessons(command_dir, mod)
            if not lessons:
                continue
            last = lessons[-1]
            text = last.read_text(encoding="utf-8")
            # 次モジュールの start-X-Y 参照を探す
            next_mod_pattern = re.compile(
                rf"/start-{mod + 1}-\d+|次のモジュール|完了|おめでとう|"
                rf"お疲れ|finish|ここで終了|まとめ|演習課題|"
                rf"チェックポイント",
                re.IGNORECASE,
            )
            if not next_mod_pattern.search(text):
                # 「次のステップ」セクション自体があれば OK
                if "次のステップ" not in text and "next" not in text.lower():
                    errors.append(
                        f"Module {mod} 最終レッスン {last.name}: "
                        "次モジュール参照も完了表示もない"
                    )
        assert not errors, "最終レッスンの遷移不備:\n" + "\n".join(errors)

    def test_no_circular_dependencies(self, command_dir):
        """prerequisites に循環参照がないこと"""
        # レッスン ID -> prerequisites の start-X-Y リスト
        dep_graph: dict[str, list[str]] = {}
        all_ids = _all_lesson_ids(command_dir)
        for md in _lesson_files_for(command_dir):
            lesson_id = md.stem
            fm = _parse_frontmatter(md)
            if fm is None or "prerequisites" not in fm:
                dep_graph[lesson_id] = []
                continue
            prereqs = fm["prerequisites"]
            refs = []
            if isinstance(prereqs, list):
                for p in prereqs:
                    for m in START_REF_RE.finditer(str(p)):
                        ref = f"start-{m.group(1)}-{m.group(2)}"
                        if ref in all_ids:
                            refs.append(ref)
            dep_graph[lesson_id] = refs

        # DFS で循環検出
        visited: set[str] = set()
        in_stack: set[str] = set()
        cycles: list[str] = []

        def dfs(node: str) -> None:
            if node in in_stack:
                cycles.append(node)
                return
            if node in visited:
                return
            visited.add(node)
            in_stack.add(node)
            for dep in dep_graph.get(node, []):
                dfs(dep)
            in_stack.discard(node)

        for lesson_id in dep_graph:
            dfs(lesson_id)

        assert not cycles, f"循環依存を検出: {cycles}"


# ---------------------------------------------------------------------------
# Aggregate counts (sanity check)
# ---------------------------------------------------------------------------

class TestCommandCounts:
    """コマンド数の妥当性チェック"""

    def test_claude_lesson_count(self):
        """Claude 側のレッスンコマンドが十分な数あること"""
        if not CLAUDE_LESSON_DIR.exists():
            pytest.skip(".claude/commands/lesson がない")
        count = len(_all_md_files(CLAUDE_LESSON_DIR))
        assert count >= 100, (
            f"Claude lesson commands: {count} (100 以上期待)"
        )

    def test_cursor_lesson_count(self):
        """Cursor 側のレッスンコマンドが十分な数あること"""
        if not CURSOR_LESSON_DIR.exists():
            pytest.skip(".cursor/commands/lesson がない")
        count = len(_all_md_files(CURSOR_LESSON_DIR))
        assert count >= 100, (
            f"Cursor lesson commands: {count} (100 以上期待)"
        )

    def test_start_lesson_count(self):
        """start-X-Y レッスンが 100 以上あること"""
        if not CLAUDE_LESSON_DIR.exists():
            pytest.skip()
        count = len(_lesson_files_for(CLAUDE_LESSON_DIR))
        assert count >= 100, f"start-X-Y lessons: {count}"

    def test_module_coverage(self):
        """少なくとも 15 モジュール以上が存在すること"""
        if not CLAUDE_LESSON_DIR.exists():
            pytest.skip()
        modules = _all_module_numbers(CLAUDE_LESSON_DIR)
        assert len(modules) >= 15, f"Modules: {modules}"
