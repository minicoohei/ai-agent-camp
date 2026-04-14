---
description: "Lesson command"
---

# /verify-module [module number]

Automatically check the completion status of all lessons in a module, and have the AI provide a comprehensive evaluation and feedback.

## Steps

### Step 1: Run Factual Check

```bash
uv run python tools/verify_module.py --module $ARGUMENTS --json
```

### Step 2: AI Evaluation

Read the JSON results above and evaluate from the following 3 perspectives.

#### Perspective 1: Existence and Validity of Deliverables
- Check `exists` / `valid` in `outputs`
- For directories, check `file_count`
- Specifically point out any missing or invalid files

#### Perspective 2: Checkpoint Achievement
- Auto-determine checkpoints that can be inferred from deliverables (file exists -> "generated" is considered achieved)
- For subjective items like "understood" or "confirmed", **ask the user via AskUserQuestion**

#### Perspective 3: Quality Evaluation
- If deliverables exist, **Read** the actual files to check their content
- View image files with Read to check quality
- Check structure and code quality for JSON/HTML/Python files

### Step 3: Output Results

Display results in the following format:

```
## Module N: [Module Name] Completion Check Results

### Summary
| Item | Result |
|------|--------|
| Overall Rating | A / B / C / D |
| Lessons Complete | X / Y |
| Deliverables | X confirmed / Y missing |
| Checkpoints | X / Y achieved |

### Rating Criteria
- **A**: All lessons complete, all deliverables OK, good quality
- **B**: All lessons complete, minor issues with some deliverables
- **C**: Major lessons complete, some not started
- **D**: Majority incomplete

### Lesson Details
(Display deliverable status and checkpoint achievement for each lesson in table format)

### Feedback
(Specific remediation and improvement suggestions for missing items)

### Next Steps
(If all complete, guide to next module; if incomplete, indicate lessons to redo)
```

### Step 4: Next Action

Present the following options via AskUserQuestion:
1. Work on missing lessons -> Guide to the relevant `/start-X-Y`
2. Proceed to the next module -> Guide to `/verify-module N+1`
3. Save results as JSON -> `uv run python tools/verify_module.py --module N --json --output .cursor/module_verify_N.json`
