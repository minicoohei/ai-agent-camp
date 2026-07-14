---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-4"]
level: "intermediate"
tags: ["article", "proofreading"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 14-5: Proofreading - Proofreading Agent Review

## 📍 What You'll Do

Welcome to **Lesson 14-5: Proofreading - Proofreading Agent Review**!

| Item | Details |
|------|---------|
| Goal | Review the article from 5 perspectives using the proofreading agent and apply corrections |
| Duration | ~30 min |
| Skills Used | proofreading-agent |
| Prerequisites | Gemini API key configured, Lesson 14-4 (illustrated draft) complete |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Understand the 5 proofreading Sweeps (perspectives)
2. Run all Sweeps with proofreading-agent
3. Review results and apply corrections

By the end of this session, an article draft proofread from 5 perspectives will be complete.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. Responses may pause depending on the tool, but this is not a malfunction.

---

## 🎯 Readiness Check

First, let's confirm everything is ready.

**AskQuestion settings:**
```json
{
  "title": "🎯 Pre-Session Check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check the prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Proceed to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Understand the 5 Proofreading Sweeps

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Understand the 5 Proofreading Perspectives",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Explain the 5 Sweeps (review perspectives) used by the proofreading agent.

1. Accuracy Sweep: Accuracy of facts, data, and proper nouns
2. Grammar Sweep: Detection of grammar errors, punctuation, and typos
3. Consistency Sweep: Terminology unification, notation variations, and style consistency
4. Readability Sweep: Sentence length, structural complexity, and overuse of technical terms
5. Structure Sweep: Logical flow, paragraph length, and balance between introduction and conclusion

Explain the specific check items and common flagged patterns for each Sweep.
```

**Expected result**: Detailed check items for the 5 Sweeps and common flagged examples are explained.

---

## 🚀 Step 2: Run All Sweeps with proofreading-agent

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Run Proofreading",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Use the proofreading-agent skill to proofread the article draft.

Execution command:
python skills/proofreading-agent/scripts/proofreading_agent.py --input output/article-14-4-with-images.md --output output/article-14-5-review.json

Target file: output/article-14-4-with-images.md

Run all 5 Sweeps:
1. Accuracy Sweep
2. Grammar Sweep
3. Consistency Sweep
4. Readability Sweep
5. Structure Sweep

Output the following for each finding:
- Location (line number and text)
- Issue type (Sweep name)
- Severity (High/Medium/Low)
- Suggested correction

Save the results to output/article-14-5-review.json.
```

**Expected result**: Proofreading results from all 5 Sweeps are output in JSON format, with all findings listed.

---

## 🚀 Step 3: Review Results and Apply Corrections

In Codex, you typically select from choices in chat to choose the correction method.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Apply Corrections",
  "questions": [{
    "id": "apply_method",
    "prompt": "How would you like to apply corrections?",
    "options": [
      {"id": "auto_all", "label": "Auto-apply all corrections"},
      {"id": "one_by_one", "label": "Review and apply one at a time"},
      {"id": "summary_only", "label": "Just review the summary"}
    ]
  }]
}
```

**If "Auto-apply all corrections":**
Input:
```text
Apply all findings from output/article-14-5-review.json to the article.

Target file: output/article-14-4-with-images.md
Corrected file: output/article-14-5-proofread.md

Also output a summary of corrections:
- Number of corrections (by Sweep)
- Breakdown by severity
- Main corrections made
```

**If "Review and apply one at a time":**
```text
Display findings from output/article-14-5-review.json one at a time in order of severity.
Allow choosing "Apply/Skip/Modify correction" for each finding.
```

**If "Just review the summary":**
```text
Display the summary of proofreading results from output/article-14-5-review.json.
Show the number of findings by Sweep and list only "High" severity findings.
```

**Expected result**: Proofreading corrections are applied to the article, and the corrected draft is saved.

---

## ⚠️ Common Issues and Solutions

In Codex, you typically present choices in chat so the user can select their issue and get guidance instantly.

**AskQuestion settings example:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Too many findings to handle"},
      {"id": "trouble_2", "label": "Irrelevant findings"},
      {"id": "trouble_3", "label": "Text became unnatural after applying corrections"},
      {"id": "trouble_4", "label": "Review results file isn't generated"}
    ]
  }]
}
```


### Issue 1: "Too many findings to handle"
**Cause**: Draft quality is low, or proofreading standards are too strict
**Solution prompt**:
```text
Start by addressing only "High" severity findings.
Handle "Medium" and "Low" severity in the next iteration.
Filter and display only "High" severity findings.
```

### Issue 2: "Irrelevant findings"
**Cause**: Mechanical checking without context consideration
**Solution prompt**:
```text
You can ignore irrelevant findings.
Select "Skip" and move to the next finding.
Intentional expressions (style characteristics, rhetorical expressions) are excluded from proofreading.
```

### Issue 3: "Text became unnatural after applying corrections"
**Cause**: Local corrections ignoring context
**Solution prompt**:
```text
If the corrected text is unnatural, readjust including surrounding context.
You can also revert to the original text:
Refer to output/article-14-4-with-images.md (before corrections).
```

### Issue 4: "Review results file isn't generated"
**Cause**: Input file not found
**Solution prompt**:
```bash
Check the input file path:
ls output/article-14-4-with-images.md
If the file doesn't exist, complete Lesson 14-4 (/start-14-4) first.
```

---

## ✅ Checkpoint
- [ ] Understood the 5 proofreading Sweeps (accuracy/grammar/consistency/readability/structure)
- [ ] Ran all Sweeps with proofreading-agent
- [ ] Reviewed findings and decided on correction approach
- [ ] Saved the proofread draft with corrections to output/

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-5-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-5-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-5-*.md
```

> 💡 View full text: `cat output/article-14-5-*.md` to display the entire file

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```bash
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin.

In Codex, you can typically select from choices in chat.

**AskQuestion settings example:**
```json
{
  "title": "Select Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-14-6)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-6 in a new window
- finish → End
