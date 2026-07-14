---
description: Pull the latest skills from upstream
category: utility
nonInteractiveMode: compliant
---
# Update Skills to Latest Version

## Usage
```text
/update-skills
```

## Overview
Pulls the latest skill updates from the original repository (minicoohei/ai-agent-camp).
Internally, this executes `git fetch upstream` + `git merge upstream/main`.
This works the same way as `/update-material`, but provides guidance specific to skill updates.

## Execution Steps

Execute the following command.

```bash
uv run python tools/skill_manager.py update-upstream
```

The script automatically performs the following:

1. Checks for the `upstream` remote (adds it if not configured)
2. Fetches the latest with `git fetch upstream`
3. Merges into the current branch with `git merge upstream/main`

## If Conflicts Occur
Conflicts may occur when skills you have modified were also updated in the original repository. In that case:

- Open the conflicted files in your editor, review the `<<<<<<<` / `=======` / `>>>>>>>` markers, and resolve manually
- After resolution: `git add <file>` -> `git commit` to complete the merge

## Post-Update Verification

```bash
# Check the current skill list
uv run python tools/skill_manager.py list
```

## Notes
- **Target**: This is for repositories you copied for personal use (Import / clone+push)
- **Safety**: `git push --force` is never executed. Only merge is performed
- Push to remote with `git push origin main` as needed
