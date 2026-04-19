#!/usr/bin/env python3
"""
Module 4 & Module 7 コマンドファイル検証スクリプト
全コマンドファイルの構造・整合性・参照先を自動テストする。
"""

import os
import re
import sys
import json
import subprocess
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

# ─── テスト結果 ───

@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str = ""

@dataclass
class FileTestReport:
    file_path: str
    results: list = field(default_factory=list)

    @property
    def passed(self):
        return all(r.passed for r in self.results)

    @property
    def pass_count(self):
        return sum(1 for r in self.results if r.passed)

    @property
    def fail_count(self):
        return sum(1 for r in self.results if not r.passed)


# ─── テスト関数群 ───

def test_file_exists(path: Path) -> TestResult:
    """ファイルが存在するか"""
    exists = path.exists()
    return TestResult(
        "ファイル存在",
        exists,
        f"{'OK' if exists else 'NOT FOUND'}: {path.relative_to(ROOT)}"
    )

def test_yaml_frontmatter(content: str, filepath: str) -> list[TestResult]:
    """YAMLフロントマターの検証"""
    results = []

    # フロントマターの抽出
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        results.append(TestResult("YAML存在", False, "フロントマターが見つかりません"))
        return results

    results.append(TestResult("YAML存在", True, "フロントマター検出OK"))

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        results.append(TestResult("YAMLパース", False, f"パースエラー: {e}"))
        return results

    results.append(TestResult("YAMLパース", True, "パースOK"))

    # 必須フィールド
    required = ["description", "duration", "prerequisites", "level", "tags"]
    for field_name in required:
        has = field_name in fm
        results.append(TestResult(
            f"必須フィールド: {field_name}",
            has,
            f"{'OK' if has else 'MISSING'}: {fm.get(field_name, 'N/A')}"
        ))

    # level値の検証
    if "level" in fm:
        valid_levels = ["beginner", "intermediate", "advanced"]
        ok = fm["level"] in valid_levels
        results.append(TestResult(
            "level値",
            ok,
            f"{'OK' if ok else 'INVALID'}: {fm['level']}"
        ))

    # prerequisitesがリスト
    if "prerequisites" in fm:
        is_list = isinstance(fm["prerequisites"], list)
        results.append(TestResult(
            "prerequisites型",
            is_list,
            f"{'OK: list' if is_list else 'INVALID: ' + type(fm['prerequisites']).__name__}"
        ))

    # tagsがリスト
    if "tags" in fm:
        is_list = isinstance(fm["tags"], list)
        results.append(TestResult(
            "tags型",
            is_list,
            f"{'OK: list' if is_list else 'INVALID: ' + type(fm['tags']).__name__}"
        ))

    return results


def test_prerequisite_files_exist(content: str) -> list[TestResult]:
    """prerequisitesで参照されるレッスンファイルが存在するか"""
    results = []
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return results

    try:
        fm = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return results

    prereqs = fm.get("prerequisites", [])
    if not isinstance(prereqs, list):
        return results

    for prereq in prereqs:
        # start-X-Y 形式のファイル
        cursor_path = ROOT / ".cursor" / "commands" / "lesson" / f"{prereq}.md"
        claude_path = ROOT / ".claude" / "commands" / "lesson" / f"{prereq}.md"

        cursor_exists = cursor_path.exists()
        claude_exists = claude_path.exists()

        results.append(TestResult(
            f"前提レッスン存在 (.cursor): {prereq}",
            cursor_exists,
            f"{'OK' if cursor_exists else 'NOT FOUND'}: {cursor_path.relative_to(ROOT)}"
        ))
        results.append(TestResult(
            f"前提レッスン存在 (.claude): {prereq}",
            claude_exists,
            f"{'OK' if claude_exists else 'NOT FOUND'}: {claude_path.relative_to(ROOT)}"
        ))

    return results


def test_next_lesson_reference(content: str) -> list[TestResult]:
    """次のレッスン参照が存在するか"""
    results = []

    # /start-X-Y パターンを検出
    refs = re.findall(r'/start-(\d+-\d+)', content)
    seen = set()
    for ref in refs:
        if ref in seen:
            continue
        seen.add(ref)
        fname = f"start-{ref}.md"
        cursor_path = ROOT / ".cursor" / "commands" / "lesson" / fname
        exists = cursor_path.exists()
        results.append(TestResult(
            f"参照レッスン存在: start-{ref}",
            exists,
            f"{'OK' if exists else 'NOT FOUND'}: {cursor_path.relative_to(ROOT)}"
        ))

    return results


def test_referenced_paths(content: str) -> list[TestResult]:
    """コマンド内で参照されるファイルパスが存在するか（固定パスのみ）"""
    results = []

    # .claude/skills/*/SKILL.md パターン
    skill_refs = re.findall(r'\.claude/skills/([\w-]+)/SKILL\.md', content)
    for skill in set(skill_refs):
        path = ROOT / ".claude" / "skills" / skill / "SKILL.md"
        exists = path.exists()
        results.append(TestResult(
            f"スキル参照: {skill}",
            exists,
            f"{'OK' if exists else 'NOT FOUND'}: .claude/skills/{skill}/SKILL.md"
        ))

    # .cursor/commands/lesson/start-*.md パターン
    cmd_refs = re.findall(r'\.cursor/commands/lesson/(start-[\w-]+\.md)', content)
    for cmd in set(cmd_refs):
        path = ROOT / ".cursor" / "commands" / "lesson" / cmd
        exists = path.exists()
        results.append(TestResult(
            f"コマンド参照: {cmd}",
            exists,
            f"{'OK' if exists else 'NOT FOUND'}: .cursor/commands/lesson/{cmd}"
        ))

    # data/google-sync/scripts/sync_google.py や docs/setup-guides/*.md 等
    kb_refs = re.findall(r'((?:data/(?:google-sync|slack-sync)|docs/setup-guides)/[\w./-]+\.(?:py|txt|md))', content)
    for kb in set(kb_refs):
        path = ROOT / kb
        exists = path.exists()
        results.append(TestResult(
            f"KB参照: {kb}",
            exists,
            f"{'OK' if exists else 'NOT FOUND'}: {kb}"
        ))

    # .claude/skills/*/scripts/*.py パターン（固定名のみ）
    script_refs = re.findall(r'\.claude/skills/([\w-]+)/scripts/([\w_]+\.py)', content)
    for skill, script in set(script_refs):
        path = ROOT / ".claude" / "skills" / skill / "scripts" / script
        exists = path.exists()
        results.append(TestResult(
            f"スクリプト参照: {skill}/{script}",
            exists,
            f"{'OK' if exists else 'NOT FOUND'}: .claude/skills/{skill}/scripts/{script}"
        ))

    return results


def test_askquestion_json(content: str) -> list[TestResult]:
    """AskQuestion JSONブロックの構文検証"""
    results = []

    # ```json ... ``` ブロックを抽出
    json_blocks = re.findall(r'```json\n(.*?)```', content, re.DOTALL)

    if not json_blocks:
        results.append(TestResult("AskQuestion JSON", False, "JSONブロックが見つかりません"))
        return results

    for i, block in enumerate(json_blocks):
        try:
            data = json.loads(block.strip())
            # 必須フィールド検証
            has_title = "title" in data
            has_questions = "questions" in data and isinstance(data["questions"], list)

            if has_title and has_questions:
                for q in data["questions"]:
                    has_id = "id" in q
                    has_prompt = "prompt" in q
                    has_options = "options" in q and isinstance(q["options"], list)
                    valid = has_id and has_prompt and has_options

                    if valid:
                        # 各optionにid/labelがあるか
                        for opt in q["options"]:
                            if "id" not in opt or "label" not in opt:
                                valid = False
                                break

                    results.append(TestResult(
                        f"AskQuestion #{i+1} 構造",
                        valid,
                        f"{'OK' if valid else 'INVALID'}: title={data.get('title', 'N/A')[:40]}"
                    ))
            else:
                results.append(TestResult(
                    f"AskQuestion #{i+1} 構造",
                    False,
                    f"title={has_title}, questions={has_questions}"
                ))

        except json.JSONDecodeError as e:
            results.append(TestResult(
                f"AskQuestion #{i+1} JSON構文",
                False,
                f"JSONパースエラー: {e}"
            ))

    return results


def test_cursor_claude_parity(filename: str) -> list[TestResult]:
    """.cursorと.claudeの両方に同じファイルが存在するか"""
    results = []

    cursor_path = ROOT / ".cursor" / "commands" / "lesson" / filename
    claude_path = ROOT / ".claude" / "commands" / "lesson" / filename

    cursor_exists = cursor_path.exists()
    claude_exists = claude_path.exists()

    both = cursor_exists and claude_exists
    results.append(TestResult(
        "Cursor/Claude対称性",
        both,
        f"cursor={'OK' if cursor_exists else 'MISSING'}, claude={'OK' if claude_exists else 'MISSING'}"
    ))

    if both:
        cursor_content = cursor_path.read_text(encoding="utf-8")
        claude_content = claude_path.read_text(encoding="utf-8")
        identical = cursor_content == claude_content
        results.append(TestResult(
            "Cursor/Claude内容一致",
            identical,
            f"{'一致' if identical else '不一致（差分あり）'}"
        ))

    return results


def test_section_structure(content: str) -> list[TestResult]:
    """期待されるセクション構造の存在確認"""
    results = []

    expected_sections = [
        ("準備チェック", r"## 🎯 準備チェック"),
        ("Step定義", r"## 🚀 Step \d+"),
        ("トラブル", r"## ⚠️ よくあるトラブル"),
        ("チェックポイント", r"## ✅ チェックポイント"),
        ("完了チェック", r"## ✅ 完了チェック"),
        ("次のステップ", r"## [🎉➡️] (?:次のステップ|Module \d+ 完了)"),
    ]

    for name, pattern in expected_sections:
        found = bool(re.search(pattern, content))
        results.append(TestResult(
            f"セクション: {name}",
            found,
            f"{'OK' if found else 'MISSING'}"
        ))

    # Step数のカウント
    steps = re.findall(r'## 🚀 Step \d+', content)
    results.append(TestResult(
        "Step数",
        len(steps) >= 2,
        f"{len(steps)}ステップ定義"
    ))

    return results


def test_checklist_items(content: str) -> list[TestResult]:
    """チェックポイントのチェックリスト形式"""
    results = []

    checklists = re.findall(r'- \[ \] .+', content)
    has_checklist = len(checklists) >= 2
    results.append(TestResult(
        "チェックリスト項目",
        has_checklist,
        f"{len(checklists)}項目"
    ))

    return results


def test_gogcli_installed() -> TestResult:
    """gogcli がインストールされているか"""
    try:
        result = subprocess.run(
            ["gog", "--version"],
            capture_output=True, text=True, timeout=10
        )
        installed = result.returncode == 0
        version = result.stdout.strip() or result.stderr.strip()
        return TestResult("gogcliインストール", installed, f"{'OK' if installed else 'NOT INSTALLED'}: {version[:50]}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return TestResult("gogcliインストール", False, "gog コマンドが見つかりません")


def test_gogcli_auth_status() -> TestResult:
    """gogcli に認証済みアカウントがあるか"""
    try:
        result = subprocess.run(
            ["gog", "auth", "list"],
            capture_output=True, text=True, timeout=10
        )
        has_auth = result.returncode == 0 and len(result.stdout.strip()) > 0
        # メールアドレスをマスク
        output = result.stdout.strip()
        masked = re.sub(r'[\w.+-]+@[\w.-]+', '***@***.***', output)
        return TestResult("gogcli認証状態", has_auth, f"{'認証済み' if has_auth else '未認証'}: {masked[:80]}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return TestResult("gogcli認証状態", False, "gogコマンド実行失敗")


# ─── メイン ───

def run_all_tests():
    """全テスト実行"""

    all_reports = []

    # Module 4 ファイル
    module4_files = [f"start-4-{i}.md" for i in range(1, 8)]
    # Module 7 ファイル
    module7_files = [f"start-7-{i}.md" for i in range(1, 5)]

    all_files = module4_files + module7_files

    print("=" * 70)
    print("Module 4 & Module 7 コマンドファイル検証テスト")
    print("=" * 70)

    # 環境テスト
    print("\n--- 環境チェック ---")
    env_report = FileTestReport("環境")
    env_report.results.append(test_gogcli_installed())
    env_report.results.append(test_gogcli_auth_status())
    all_reports.append(env_report)

    for r in env_report.results:
        icon = "✅" if r.passed else "❌"
        print(f"  {icon} {r.name}: {r.detail}")

    # 各ファイルのテスト
    for filename in all_files:
        print(f"\n--- {filename} ---")
        report = FileTestReport(filename)

        cursor_path = ROOT / ".cursor" / "commands" / "lesson" / filename

        # ファイル存在
        report.results.append(test_file_exists(cursor_path))

        if not cursor_path.exists():
            all_reports.append(report)
            print(f"  ❌ ファイルが存在しません: {cursor_path}")
            continue

        content = cursor_path.read_text(encoding="utf-8")

        # YAML検証
        report.results.extend(test_yaml_frontmatter(content, filename))

        # 前提レッスン存在
        report.results.extend(test_prerequisite_files_exist(content))

        # 次レッスン参照
        report.results.extend(test_next_lesson_reference(content))

        # ファイルパス参照
        report.results.extend(test_referenced_paths(content))

        # AskQuestion JSON
        report.results.extend(test_askquestion_json(content))

        # Cursor/Claude対称性
        report.results.extend(test_cursor_claude_parity(filename))

        # セクション構造
        report.results.extend(test_section_structure(content))

        # チェックリスト
        report.results.extend(test_checklist_items(content))

        all_reports.append(report)

        for r in report.results:
            icon = "✅" if r.passed else "❌"
            print(f"  {icon} {r.name}: {r.detail}")

    # サマリー
    print("\n" + "=" * 70)
    print("テストサマリー")
    print("=" * 70)

    total_pass = 0
    total_fail = 0

    for report in all_reports:
        total_pass += report.pass_count
        total_fail += report.fail_count
        icon = "✅" if report.passed else "❌"
        print(f"  {icon} {report.file_path}: {report.pass_count}passed / {report.fail_count}failed")

    print(f"\n  合計: {total_pass}passed / {total_fail}failed / {total_pass + total_fail}total")

    if total_fail > 0:
        print("\n  ❌ 失敗したテスト:")
        for report in all_reports:
            for r in report.results:
                if not r.passed:
                    print(f"    [{report.file_path}] {r.name}: {r.detail}")

    print("=" * 70)

    return total_fail == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
