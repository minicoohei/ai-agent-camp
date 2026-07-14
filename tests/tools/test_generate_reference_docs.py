from pathlib import Path

from tools.generate_reference_docs import main, replace_generated_block


COMMANDS_TEMPLATE = """# Commands

**対応コマンド数**: 1個

最終更新: 2020-01-01

## レッスンコマンド (1個)

old command inventory

## コマンド実行方法

This hand-written command guidance must remain.
"""

SKILLS_TEMPLATE = """# Skills

**対応スキル数**: 1個

最終更新: 2020-01-01

## 画像生成・編集系スキル (1個)

### 1. `known-skill` - Known

old skill details

## インストール方法

This hand-written skill guidance must remain.
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_repository(root: Path) -> None:
    write(root / "docs/commands-reference.md", COMMANDS_TEMPLATE)
    write(root / "docs/skills-reference.md", SKILLS_TEMPLATE)
    write(
        root / ".cursor/commands/lesson/start-1-1.md",
        """---
description: Lesson command
tags: [module-1]
---
# Lesson 1-1: First lesson
""",
    )
    write(
        root / ".cursor/commands/lesson/start-1-1.en.md",
        """---
description: Translated duplicate
---
# Lesson 1-1: English duplicate
""",
    )
    write(
        root / ".cursor/commands/utility/overview.md",
        """---
description: Show the repository overview
---
# Overview
""",
    )
    write(
        root / ".cursor/commands/module-1-helper.md",
        """---
description: Module helper
---
# Module helper
""",
    )
    write(
        root / "skills/known-skill/SKILL.md",
        """---
name: known-skill
description: Existing categorized skill
---
# Known skill
""",
    )
    write(
        root / "skills/new-skill/SKILL.md",
        """---
name: new-skill
description: Newly discovered skill
---
# New skill
""",
    )


def test_replace_generated_block_preserves_hand_written_content() -> None:
    original = "before\n<!-- AUTO-GENERATED:commands START -->\nold\n<!-- AUTO-GENERATED:commands END -->\nafter\n"

    updated = replace_generated_block(original, "commands", "new")

    assert updated == "before\n<!-- AUTO-GENERATED:commands START -->\nnew\n<!-- AUTO-GENERATED:commands END -->\nafter\n"


def test_generation_is_idempotent_and_check_exit_codes(tmp_path: Path, capsys) -> None:
    build_repository(tmp_path)
    arguments = ["--root", str(tmp_path), "--date", "2026-07-14"]

    assert main([*arguments, "--check"]) == 1
    assert "Reference docs are stale" in capsys.readouterr().err

    assert main(arguments) == 0
    commands_once = (tmp_path / "docs/commands-reference.md").read_bytes()
    skills_once = (tmp_path / "docs/skills-reference.md").read_bytes()

    assert main(arguments) == 0
    assert (tmp_path / "docs/commands-reference.md").read_bytes() == commands_once
    assert (tmp_path / "docs/skills-reference.md").read_bytes() == skills_once
    assert main([*arguments, "--check"]) == 0

    commands = commands_once.decode()
    skills = skills_once.decode()
    assert "**対応コマンド数**: 3個（レッスン 1個 + ユーティリティ 1個 + トップレベル 1個）" in commands
    assert commands.count("`/start-1-1`") == 1
    assert "This hand-written command guidance must remain." in commands
    assert "### 画像生成・編集系スキル（1個）" in skills
    assert "### 未分類（1個）" in skills
    assert "This hand-written skill guidance must remain." in skills


def test_check_fails_after_a_scanned_source_changes(tmp_path: Path) -> None:
    build_repository(tmp_path)
    arguments = ["--root", str(tmp_path), "--date", "2026-07-14"]
    assert main(arguments) == 0

    write(
        tmp_path / ".cursor/commands/utility/new-command.md",
        """---
description: Added later
---
# New command
""",
    )

    assert main([*arguments, "--check"]) == 1
