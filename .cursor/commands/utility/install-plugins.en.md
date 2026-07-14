---
description: Install skills from external plugins
category: utility
nonInteractiveMode: compliant
---
# External Plugin Installation

## Usage
```text
/install-plugins
```

## Overview
Install curated skills from external plugin registries (`external-plugins.yaml`) defined across 6 repositories. Based on the SkillsBench paper, rather than installing all skills at once, we recommend combining 2-3 modules tailored to the task at hand.

## Subcommand Reference

### 1. List Available Skills
Display all registered plugins and recommended skills from the registry.
```bash
# Summary display
uv run python tools/skill_manager.py plugin-list

# Also show installation status of each skill
uv run python tools/skill_manager.py plugin-list --verbose
```

### 2. Batch Install Recommended Skills
Install all recommended skills from all plugins (approximately 17) at once.
```bash
uv run python tools/skill_manager.py plugin-install --all-recommended
```

### 3. Install from a Specific Plugin
```bash
# Specify a plugin (recommended skills only)
uv run python tools/skill_manager.py plugin-install --plugin knowledge-work-plugins

# Specify plugin + skill names
uv run python tools/skill_manager.py plugin-install --plugin claude-scientific-skills --skill matplotlib plotly

# Overwrite existing skills
uv run python tools/skill_manager.py plugin-install --plugin marimo-skills --force
```

## Available Plugins

| Plugin | Repository | Recommended Skills |
|--------|-----------|-------------------|
| knowledge-work-plugins | anthropics/knowledge-work-plugins | 5 |
| ui-ux-pro-max-skill | nextlevelbuilder/ui-ux-pro-max-skill | 1 |
| planning-with-files | OthmanAdi/planning-with-files | 1 |
| claude-scientific-skills | K-Dense-AI/claude-scientific-skills | 5 |
| claude-skills | alirezarezvani/claude-skills | 3 |
| marimo-skills | marimo-team/skills | 2 |

## Options

| Option | Description |
|--------|-------------|
| `--plugin NAME` | Specify the target plugin name |
| `--skill NAME...` | Specify skill names to install |
| `--all-recommended` | Install all recommended skills |
| `--force` | Overwrite existing skills |

## Notes
- A `source:` field is automatically added to the SKILL.md of installed skills (for origin tracking)
- If a name conflicts with an existing project skill, it will be skipped (use `--force` to overwrite)
- A network connection is required for the first run as repositories will be cloned
