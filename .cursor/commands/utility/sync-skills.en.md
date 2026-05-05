---
description: Sync skills to global or other projects
category: utility
nonInteractiveMode: compliant
---
# Skill Sync

## Usage
```text
/sync-skills
```

## Overview
Copies and syncs skills from the project's `.claude/skills/` to global (`~/.claude/skills/`) or other projects. You can also view the skill list and access the official plugin installation guide.

## Subcommands

### 1. Display Skill List
View skills in both the project and global directories, and check for differences.
```bash
uv run python tools/skill_manager.py list
```

### 2. Sync to Global
Copy project skills to `~/.claude/skills/`. This makes skills available across all projects.
```bash
# Sync all skills
uv run python tools/skill_manager.py sync-global

# Sync specific skills only
uv run python tools/skill_manager.py sync-global --skills banner-creator diagram-generator

# Overwrite existing skills
uv run python tools/skill_manager.py sync-global --force

# Specify a custom destination
uv run python tools/skill_manager.py sync-global --target /path/to/target/skills
```

### 3. Sync to Another Project
Copy project skills to another project's `.claude/skills/`.
```bash
# Sync all skills
uv run python tools/skill_manager.py sync-project /path/to/other-project

# Sync specific skills only
uv run python tools/skill_manager.py sync-project /path/to/other-project --skills banner-creator

# Overwrite existing skills
uv run python tools/skill_manager.py sync-project /path/to/other-project --force
```

### 4. Official Plugin Installation Guide
Display instructions for installing plugins from the anthropics/skills repository.
```bash
uv run python tools/skill_manager.py plugin-guide
```

## Options

| Option | Applicable Commands | Description |
|--------|-------------------|-------------|
| `--force` | sync-global, sync-project | Overwrite existing skills (default is to skip) |
| `--skills NAME...` | sync-global, sync-project | Specify skill names to copy (default is all) |
| `--target DIR` | sync-global | Change the destination directory |

## Notes
- Without `--force`, skills that already exist at the destination are skipped
- Since this uses copying (not symlinks), synced skills are independent copies
- If you update a skill, you need to sync again
