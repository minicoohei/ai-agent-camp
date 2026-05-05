---
description: "Module completion check (with AI evaluation)"
nonInteractiveMode: compliant
---
# /verify-module [module number]

Automatically check the completion status of all lessons in a module, and have AI provide a comprehensive evaluation and feedback.

## Steps

### Step 1: Run fact check

```bash
uv run python tools/verify_module.py --module $ARGUMENTS --json
```

### Step 2: AI evaluation

Read the JSON results above and evaluate from these 3 perspectives:

#### Perspective 1: Output existence and validity
- Check `outputs` for `exists` / `valid`
- For directories, check `file_count`
- Specifically point out any missing or invalid files

#### Perspective 2: Checkpoint achievement
- Auto-assess checkpoints inferable from outputs (file exists → "was able to generate" is achieved)
- For subjective items like "understood" or "confirmed," **ask the user via AskUserQuestion**

#### Perspective 3: Quality assessment
- If outputs exist, **Read** the actual files to check content
- For image files, Read to display and check quality
- For JSON/HTML/Python files, check structure and code quality

### Step 3: Output results

Display results in this format:

```
## Module N: [Module Name] Completion Check Results

### Summary
| Item | Result |
|------|--------|
| Overall Rating | A / B / C / D |
| Lessons Completed | X / Y |
| Outputs | X confirmed / Y missing |
| Checkpoints | X / Y achieved |

### Rating Criteria
- **A**: All lessons complete, all outputs OK, good quality
- **B**: All lessons complete, minor issues with some outputs
- **C**: Major lessons complete, some not started
- **D**: Most not completed

### Lesson Details
(Show output status and checkpoint achievement for each lesson in table format)

### Feedback
(Specific remediation steps and improvement suggestions for missing items)

### Next Steps
(If all complete, guide to next module; if incomplete, list lessons to redo)
```

### Step 4: Next action

Present these options via AskUserQuestion:
1. Work on missing lessons → Guide to the relevant `/start-X-Y`
2. Proceed to next module → Guide to `/verify-module N+1`
3. Save results as JSON → `uv run python tools/verify_module.py --module N --json --output .cursor/module_verify_N.json`
