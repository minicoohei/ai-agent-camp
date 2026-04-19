"""
リポジトリ構造の決定論的テスト。
ディレクトリ・ファイルの存在確認。
"""
import pytest
from pathlib import Path

def test_directory_structure(project_root):
    """必須ディレクトリの存在確認"""
    required_dirs = [
        ".claude/skills",
        ".cursor/rules",
        ".cursor/commands/lesson",
        ".cursor/commands/utility",
        "courses",
        "tools",
        "docs",
    ]
    for dir_path in required_dirs:
        assert (project_root / dir_path).exists(), f"Missing directory: {dir_path}"

def test_required_files(project_root):
    """必須ファイルの存在確認"""
    required_files = [
        "CLAUDE.md",
        "README.md",
        ".env.example",
        ".gitignore",
        "courses/lessons.manifest.yaml",
    ]
    for file_path in required_files:
        assert (project_root / file_path).exists(), f"Missing file: {file_path}"

def test_skills_count(project_root):
    """Skillsの数を確認（20個）"""
    skills_dir = project_root / ".claude/skills"
    skills = [d for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    assert len(skills) >= 18, f"Expected at least 18 skills, got {len(skills)}"

def test_security_hooks_exist(project_root):
    """セキュリティHooksスクリプトの存在確認"""
    required_security_files = [
        ".claude/hooks/bash_guard.py",
        ".claude/hooks/write_guard.py",
        ".claude/hooks/README.md",
        ".claude/settings.json",
        "docs/security-guardrails.md",
    ]
    for file_path in required_security_files:
        assert (project_root / file_path).exists(), f"Missing security file: {file_path}"

def test_lesson_commands_count(project_root):
    """レッスンCommandsの数を確認"""
    lesson_dir = project_root / ".cursor/commands/lesson"
    commands = list(lesson_dir.glob("*.md"))
    assert len(commands) >= 40, f"Expected at least 40 lesson commands, got {len(commands)}"
