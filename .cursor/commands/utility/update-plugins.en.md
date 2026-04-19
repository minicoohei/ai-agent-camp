---
description: Update installed external skills
category: utility
---

# Update External Plugins

## Usage
```text
/update-plugins
```

## Overview
Updates external skills installed via `plugin-install` to the versions specified in the registry (`external-plugins.yaml`).

## Subcommands

### 1. Update all external skills
```bash
uv run python tools/skill_manager.py plugin-update
```

### 2. Update a specific plugin only
```bash
uv run python tools/skill_manager.py plugin-update --plugin knowledge-work-plugins
```

### 3. Preview updates
```bash
uv run python tools/skill_manager.py plugin-update --dry-run
```

### 4. Clear cache
Delete repository clone caches to free disk space.
```bash
uv run python tools/skill_manager.py plugin-clean
```

## Options

| Option | Description |
|--------|-------------|
| `--plugin NAME` | Specify the target plugin name |
| `--dry-run` | Display update details only (does not actually update) |

## Notes
- Only skills with a `source:` field in SKILL.md are eligible for updates
- Network connection is required as the latest version of the repository is fetched during updates
- Clearing the cache with `plugin-clean` means a re-clone is required the next time you install/update
