---
description: Pull the latest course materials from the upstream repository
---

# Update Course Materials to Latest Version

## Usage
```
/update-material
```

## Overview
Pulls the latest course material changes from the original repository (minicoohei/ai-agent-camp) into your personal repository (e.g., your own GitHub ai-agent-camp) created via Import or clone + push.

## Execution Steps

Execute the following in order.

### 1. Check for upstream remote
```bash
git remote -v
```
If `upstream` is not displayed, add it in the next step.

### 2. Add upstream (only if not already configured)
```bash
git remote add upstream https://github.com/minicoohei/ai-agent-camp.git
```
Skip this step if `upstream` already exists.

### 3. Fetch the latest
```bash
git fetch upstream
```

### 4. Merge into the current branch
```bash
# Check the current branch (usually main)
git branch --show-current

# Pull in upstream's main
git merge upstream/main
```
If your branch is named `master`, using `git merge upstream/main` is still correct (upstream uses main).

## If Conflicts Occur
Conflicts may occur when files you have modified were also updated in the original repository. In that case, provide the following guidance.

- Open the conflicted files in your editor, review the `<<<<<<<` / `=======` / `>>>>>>>` markers, and resolve manually
- After resolution: `git add <file>` -> `git commit` to complete the merge
- If resolution is difficult, you can back up the file and use `git checkout --theirs -- <path>` to adopt the upstream version

## Notes
- **Target**: This is for repositories you copied for personal use (Import / clone+push). It also works for forks.
- **Safety**: `git push --force` is never executed. Only merge is performed; push to remote with `git push origin main` as needed.
