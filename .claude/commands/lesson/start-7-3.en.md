---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands"
prerequisites: ["start-7-2"]
duration: "~25 min"
level: "intermediate"
tags: ["agent", "testing", "iteration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-3: Testing and Iteration

## 📍 What You'll Do

Welcome to **Lesson 7-3: Testing and Iteration**!

| Item | Details |
|------|------|
| Goal | Verify the meeting-notes skill with 3 types of tests and run an improvement cycle |
| Duration | ~25 min |
| Skills used | meeting-notes-summarizer (created in Lesson 7-2) |
| Prerequisites | Lesson 7-2 completed (SKILL.md created) |

**Session flow:**
1. Run trigger tests
2. Functional tests (3 types of sample data)
3. Performance comparison (with/without skill)
4. Diagnose 5 typical trouble patterns
5. Practice the improvement loop

By the end of this session, you will be able to objectively evaluate skill quality and run improvement cycles.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's first check that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session check",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "Check prerequisites"},
      {"id": "view_html", "label": "View the course page first"},
      {"id": "different_lesson", "label": "Go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite verification)
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Run Trigger Tests

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Run Trigger Tests",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Test the trigger accuracy of the meeting-notes-summarizer skill.
Enter each phrase one at a time and check whether the skill triggers correctly.

[Phrases that SHOULD trigger (5)]

1. "Summarize the meeting notes"
2. "Organize the meeting memo"
3. "Extract action items"
4. "Structure the meeting notes"
5. "Summarize the key points from this meeting"

→ Expected: The meeting-notes-summarizer skill should trigger for all phrases

[Phrases that should NOT trigger (3)]

1. "Summarize the email"
2. "Search Slack messages"
3. "Create a report"

→ Expected: The skill should not trigger for these phrases

[How to record test results]
Record results in the following format:

| Phrase | Expected | Actual | Result |
|--------|----------|--------|--------|
| Summarize the meeting notes | Triggers | ? | OK/NG |
| Organize the meeting memo | Triggers | ? | OK/NG |
| Extract action items | Triggers | ? | OK/NG |
| Structure the meeting notes | Triggers | ? | OK/NG |
| Summarize the key points | Triggers | ? | OK/NG |
| Summarize the email | No trigger | ? | OK/NG |
| Search Slack messages | No trigger | ? | OK/NG |
| Create a report | No trigger | ? | OK/NG |

Check how many out of 8 worked correctly.
Pass criteria: 8/8 (all correct)
```

**Expected result**: All correct triggers activate the skill, and incorrect triggers do not.

---

## 🚀 Step 2: Functional Tests (3 Types of Sample Data)

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Functional Tests (3 Types of Sample Data)",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Test the meeting-notes-summarizer skill with 3 types of sample data.
Enter each sample and verify the output quality.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Sample 1: Short meeting (3 people, 5 min)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summarize the following meeting notes:

Attendees: Tanaka, Sato, Suzuki
Date: February 10, 2026, 10:00
Agenda: Confirm next week's release schedule
Tanaka: Is the release on 2/17 okay?
Sato: Testing will be completed by 2/14.
Suzuki: I'll update the documentation on 2/15.
Conclusion: Release confirmed for 2/17. Sato handles testing, Suzuki handles documentation.

→ Verification points:
  - Are attendees correctly extracted?
  - Is the date/time correctly recognized?
  - Are 2 action items extracted? (Sato: complete testing, Suzuki: update documentation)
  - Are deadlines correctly set? (2/14, 2/15)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Sample 2: Regular meeting (5 people, 30 min)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summarize the following meeting notes:

Attendees: Yamada (PM), Takahashi (Dev), Ito (Design), Watanabe (QA), Kobayashi (Sales)
Date: February 10, 2026, 14:00-14:30
Location: Meeting Room A / Zoom hybrid

[Agenda 1: Q1 Sales Review]
Kobayashi: Q1 sales are expected to land at 120% of target. Enterprise plan contracts performed particularly well.
Yamada: Great results. What should the Q2 target be?
Kobayashi: I propose 130% year-over-year. We can expect the effect of new feature releases.
Yamada: Understood. Let's proceed with Q2 target at 130%.

[Agenda 2: New Feature Progress Report]
Takahashi: The dashboard feature can be released on schedule by 2/28. There was a 1-day delay in the API integration part, but we've made up for it.
Ito: UI review is complete. One fix is needed for mobile support. The fix will be done by 2/12.
Watanabe: Test cases are 80% complete. The remaining 20% will be done by 2/20. Regression tests are included.
Yamada: Please prioritize the mobile fix. Testing can come after.

[Agenda 3: Customer Support Structure]
Watanabe: Last month's support tickets increased 30% month-over-month. Many can be addressed by updating the FAQ.
Yamada: Who will handle the FAQ update?
Watanabe: I'll take it. I'll update the top 10 FAQs by 2/17.
Kobayashi: I'll share a common questions list from the sales team. I'll send it by 2/13.

[Decisions]
1. Q2 sales target is 130% year-over-year
2. Dashboard feature releases on 2/28
3. Mobile UI fix gets top priority
4. FAQ update by Watanabe, completed by 2/17

[Next Meeting]
February 17, 2026, 14:00, same location

→ Verification points:
  - Are 5 attendees and their roles correctly recognized?
  - Are 3 agenda items structured?
  - Are 4 decisions extracted?
  - Are action items extracted with owners and deadlines?
    - Ito: Mobile UI fix (by 2/12)
    - Watanabe: Complete test cases (by 2/20)
    - Watanabe: FAQ update (by 2/17)
    - Kobayashi: Share common questions list (by 2/13)
  - Is the next meeting listed?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Sample 3: Mixed-language Workshop]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summarize the following meeting notes:

Attendees: Nakamura (Tech Lead), Matsumoto (Backend), Kimura (Frontend), Garcia (DevOps)
Date: February 10, 2026, 16:00-16:45
Format: Technical Workshop

Nakamura: Today we'll discuss improving the CI/CD pipeline. The current build time is too long, so let's come up with improvements.
Garcia: The current average build time is about 12 minutes. We'd like to target under 5 minutes. Introducing Docker layer caching should significantly reduce it.
Matsumoto: Backend unit tests account for 60% of the total time. Parallel execution should cut it in half.
Kimura: On the frontend side, migrating from webpack to Vite can reduce build time from 3 minutes to 30 seconds. The PoC is already done.
Nakamura: Great. Let's prioritize.
Garcia: My proposal: Phase 1 for Docker layer caching, Phase 2 for parallel test execution, Phase 3 for Vite migration. How about that order?
Nakamura: Agreed. What's the estimated effort for each?
Garcia: Phase 1 is 2 days, I'll handle it. Can be done by 2/14.
Matsumoto: Phase 2 takes 3 days. Need pytest-xdist setup and CI config changes. Done by 2/19.
Kimura: Please allow 1 week for Phase 3. Breaking changes need to be addressed. I'll submit the PR by 2/24.
Nakamura: Understood. Let's check progress at weekly checkpoints. KPI is 50% reduction in build time.

[Decisions]
1. CI/CD pipeline improvement in 3 phases
2. KPI: 50% build time reduction (12 min → under 6 min)
3. Weekly checkpoint for progress review

→ Verification points:
  - Are English technical terms (CI/CD, Docker layer caching, parallel execution, etc.) handled correctly?
  - Are the 3 phases structured?
  - Are action items extracted with owners and deadlines?
    - Garcia: Introduce Docker layer caching (by 2/14)
    - Matsumoto: Introduce parallel test execution (by 2/19)
    - Kimura: Submit Vite migration PR (by 2/24)
  - Is the KPI documented?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For all 3 samples, verify the following output sections are present:
1. Meeting basic info (date/time, attendees, location)
2. Agenda and discussion summary
3. List of decisions
4. Action items (with owners and deadlines)
5. Next meeting (if applicable)
```

**Expected result**: All 3 samples produce structured meeting notes with all required sections.

---

## 🚀 Step 3: Performance Comparison (With/Without Skill)

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Performance Comparison (With/Without Skill)",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Compare output quality with and without the skill.
Run the same meeting notes data in 2 patterns.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Meeting notes data for comparison]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Attendees: Yamada (PM), Takahashi (Dev), Ito (Design), Watanabe (QA), Kobayashi (Sales)
Date: February 10, 2026, 14:00-14:30
Location: Meeting Room A / Zoom hybrid

[Agenda 1: Q1 Sales Review]
Kobayashi: Q1 sales are expected to land at 120% of target. Enterprise plan contracts performed particularly well.
Yamada: Great results. What should the Q2 target be?
Kobayashi: I propose 130% year-over-year. We can expect the effect of new feature releases.
Yamada: Understood. Let's proceed with Q2 target at 130%.

[Agenda 2: New Feature Progress Report]
Takahashi: The dashboard feature can be released on schedule by 2/28.
Ito: UI review is complete. One fix is needed for mobile support. The fix will be done by 2/12.
Watanabe: Test cases are 80% complete. The remaining 20% will be done by 2/20.

[Decisions]
1. Q2 sales target is 130% year-over-year
2. Dashboard feature releases on 2/28
3. Mobile UI fix gets top priority

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern A: Run WITHOUT skill]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

First, temporarily disable the meeting-notes-summarizer skill.
Method: Temporarily rename the skills/meeting-notes-summarizer/ directory.

mv skills/meeting-notes-summarizer skills/_meeting-notes-summarizer_disabled

Then make a generic request:
"Summarize the above meeting content"

Save output to output/test-without-skill.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern B: Run WITH skill]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Re-enable the skill.

mv skills/_meeting-notes-summarizer_disabled skills/meeting-notes-summarizer

Use the same data and request:
"Summarize the above meeting notes"

Save output to output/test-with-skill.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Comparison criteria]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Compare on the following 5 criteria and evaluate the skill's effectiveness:

| Criterion | Without skill | With skill | Verdict |
|-----------|--------------|------------|---------|
| Structure completeness (all sections present?) | ? | ? | Which is better |
| Action item extraction accuracy (with owner/deadline) | ? | ? | Which is better |
| Format consistency (same format every time?) | ? | ? | Which is better |
| Information coverage (no omissions?) | ? | ? | Which is better |
| Execution time (perceived) | ? | ? | Which is faster |

If "with skill" is better in at least 3 of 5 criteria, the skill is functioning effectively.
```

**Expected result**: The skill version shows superiority in structure completeness, action item extraction accuracy, and format consistency.

---

## 🚀 Step 4: Diagnose 5 Typical Trouble Patterns

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Diagnose 5 Typical Trouble Patterns",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Review 5 common trouble patterns in skill development and diagnose whether any apply to your skill.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern 1: Undertriggering]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptom: Skill doesn't trigger when it should
Cause: Insufficient trigger phrases in SKILL.md description

Diagnosis:
1. Check Step 1 trigger test results
2. Check if any phrases that "should have triggered didn't"
3. If so, add those phrases to the SKILL.md description

Fix example:
Before: description: "A skill that structures meeting notes"
After: description: "A skill that structures meeting notes and memos. Also handles action item extraction and key point organization"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern 2: Overtriggering]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptom: Skill triggers in unrelated contexts
Cause: Description is too broad (e.g., "summarize" alone matches everything)

Diagnosis:
1. Check Step 1 trigger test results
2. Check if any phrases that "should NOT have triggered did"
3. If so, narrow the description to meeting-specific language

Fix example:
Before: description: "A skill that summarizes and organizes text"
After: description: "A skill that structures meeting notes (specialized for meetings and conferences)"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern 3: Incomplete output]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptom: Action items or attendees are missing, sections are incomplete
Cause: Insufficient step instructions in the SKILL.md body

Diagnosis:
1. Check Step 2 output results
2. Use the following checklist for missing items:
   □ Meeting basic info (date/time, attendees, location)
   □ Agenda and discussion summary
   □ List of decisions
   □ Action items (with owners and deadlines)
   □ Next meeting

3. If items are missing, add an output checklist to SKILL.md

Fix example (add to SKILL.md):
## Required Output Sections
1. Meeting overview (date/time, attendees, location)
2. Summary per agenda item
3. Decisions (numbered list)
4. Action items (always specify owner and deadline)
5. Next meeting (if info available)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern 4: Context overflow]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptom: SKILL.md is too long and performance degrades, responses slow down
Cause: Body exceeds 5,000 words

Diagnosis:
1. Check SKILL.md character count:
   wc -c skills/meeting-notes-summarizer/SKILL.md
2. If it exceeds 5,000 words (~15,000 characters), improvement is needed
3. Check for unnecessary explanations, verbose examples, or duplicate instructions

Fix methods:
- Move detailed examples and supplementary explanations to references/ directory
- Keep SKILL.md to core instructions only (target: under 2,000 words)
- Set references like "See references/examples.md for details"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pattern 5: Resource loading error]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Symptom: Files in scripts/ or references/ can't be read, reference errors appear
Cause: Path specification error or file not created

Diagnosis:
1. Check file reference paths in SKILL.md
2. Verify referenced files exist:
   ls -la skills/meeting-notes-summarizer/scripts/
   ls -la skills/meeting-notes-summarizer/references/
3. Verify paths are relative (avoid absolute paths)

Fix methods:
- Remove references to non-existent files
- Fix to correct path (use relative path from SKILL.md)
- Create necessary files if they haven't been created yet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Record any patterns that apply to your skill.
We'll fix them in Step 5.
```

**Expected result**: Understand the 5 trouble patterns and identify any issues in your own skill.

---

## 🚀 Step 5: Practice the Improvement Loop

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Practice the Improvement Loop",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review the example"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**
Input:
```
Based on the test results from Steps 1-4, practice the improvement loop.
Follow these steps to run at least one improvement cycle.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Improvement loop procedure]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ Step A: Identify the weakest area

From Steps 1-4 results, select the improvement target in this priority order:
1. If there were NGs in trigger test → Fix the description (top priority)
2. If output sections were missing in functional test → Fix the SKILL.md body
3. If there was no difference from "without skill" in performance comparison → Make instructions more specific
4. If any trouble patterns matched → Apply the fix for that pattern

■ Step B: Modify SKILL.md

Apply specific fixes to the identified issues.

Back up the pre-modification SKILL.md:
cp skills/meeting-notes-summarizer/SKILL.md \
   skills/meeting-notes-summarizer/SKILL.md.backup

Fix priorities:
- description: Improve trigger accuracy (undertriggering/overtriggering countermeasures)
- Body: Clarify output format, add checklists
- References: Separate verbose parts into references/

■ Step C: Re-run tests related to the fix

- If description was modified → Re-run Step 1 trigger tests
- If body was modified → Re-run Step 2 functional tests (1 sample is OK)
- If everything was modified → Re-run Step 3 performance comparison

■ Step D: Compare before and after results

Record improvement results in the following format:

[Improvement Report]
- Improvement target: (e.g., Insufficient trigger phrases in description)
- Fix content: (e.g., Added "meeting notes" and "meeting memo")
- Test result (before): (e.g., Trigger test 6/8 correct)
- Test result (after): (e.g., Trigger test 8/8 correct)
- Improvement effect: (e.g., Trigger accuracy improved from 75% to 100%)

Save the improvement report to output/skill-improvement-report.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Advanced: Second improvement loop and beyond]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have time, work on a second issue.
The improvement loop is a repetition of "Identify → Fix → Test → Compare".
This iterative process continuously improves skill quality.
```

**Expected result**: Complete at least one improvement cycle and record the before/after output quality comparison.

---

## ⚠️ Common Issues and Solutions

Use AskQuestion to select the issue, then follow the guidance.

**AskQuestion configuration:**
```json
{
  "title": "Select the issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "No test sample data available"},
      {"id": "trouble_2", "label": "Don't know how to toggle skill on/off"},
      {"id": "trouble_3", "label": "Output doesn't change after improvement"},
      {"id": "trouble_4", "label": "Don't know how to record test results"}
    ]
  }]
}
```

### Issue 1: No test sample data available
**Cause**: Unable to prepare meeting notes data for testing
**Solution prompt**:
```
Step 2 has 3 types of sample data prepared inline.
Use them as-is:
- Sample 1: Short meeting (3 people, 5 min)
- Sample 2: Regular meeting (5 people, 30 min)
- Sample 3: Mixed-language workshop
```

### Issue 2: Don't know how to toggle skill on/off
**Cause**: Don't know how to disable/enable skills
**Solution prompt**:
```
You can disable a skill by renaming the skill folder inside skills/.

Disable (temporarily hide by renaming):
mv skills/meeting-notes-summarizer skills/_meeting-notes-summarizer_disabled

Enable (restore original name):
mv skills/_meeting-notes-summarizer_disabled skills/meeting-notes-summarizer

Note: Always re-enable after testing.
```

### Issue 3: Output doesn't change after improvement
**Cause**: SKILL.md changes may be cached
**Solution prompt**:
```
Try the following steps:
1. Restart the editor (Cursor)
2. Re-save the SKILL.md file (Ctrl+S / Cmd+S)
3. Test again in a new chat session
4. If it still doesn't change, verify the SKILL.md changes were saved correctly:
   cat skills/meeting-notes-summarizer/SKILL.md
```

### Issue 4: Don't know how to record test results
**Cause**: Unclear where and in what format to save test results
**Solution prompt**:
```
Save in Markdown format in the output/ directory.

mkdir -p output

Test result save locations:
- Trigger test results: output/trigger-test-results.md
- Functional test results: output/functional-test-results.md
- Performance comparison: output/performance-comparison.md
- Improvement report: output/skill-improvement-report.md

Format example:
# Trigger Test Results
Date: 2026-02-10
Target skill: meeting-notes-summarizer

| Phrase | Expected | Actual | Result |
|--------|----------|--------|--------|
| Summarize the meeting notes | Trigger | Trigger | OK |
...
```

---

## ✅ Checkpoint
- [ ] Verified correct trigger/non-trigger behavior in trigger tests
- [ ] Ran tests with 3 types of sample data
- [ ] Compared performance with/without skill
- [ ] Understood the 5 trouble patterns
- [ ] Ran at least 1 improvement loop
- [ ] Compared before/after output


---

## 📋 Deliverable Preview

### Expected Output
```
📁 skills/{skill_name}/
├── SKILL.md  (skill definition)
├── scripts/    (execution scripts)
└── tests/      (test files)
```

### Verification Commands
```bash
# Check skill directory structure
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Check the beginning of SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Completion Check
Paste the following into Cursor's chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail determination with any missing items listed.

---

## ➡️ Next Steps

This section is now complete. Start the next section or open a new window to begin a new section.

Use AskQuestion to choose.

**AskQuestion configuration:**
```json
{
  "title": "Choose next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose what to do next",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-7-4)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-4
- finish → End
