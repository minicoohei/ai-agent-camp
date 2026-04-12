---
description: "When the user says /start-17-2 — Module 17 Lesson 17-2: SEO audit & keyword strategy"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~40 min"
prerequisites: ["start-0-3"]
level: "intermediate"
tags: ["marketing", "seo", "keyword", "audit"]
---

# Lesson 17-2: SEO Audit & Keyword Strategy

## What You Will Do in This Session

Welcome to **Lesson 17-2: SEO Audit & Keyword Strategy**!

| Item | Details |
|------|---------|
| Goal | Conduct an SEO audit and develop a keyword strategy using the seo-audit + programmatic-seo skills |
| Duration | ~40 min |
| Skills used | seo-audit, programmatic-seo |
| Prerequisites | Gemini API key configured |
| Course page | Refer to [Module 17: Marketing](https://ai-agent.camp/en/course/module-17) in parallel |

**Session flow:**
1. Understand SEO audit fundamentals
2. Diagnose SEO issues for a target site using the seo-audit skill
3. Design keyword strategy and page templates using programmatic-seo

By the end of this session, an SEO audit report and keyword list will be complete.

> **Tip**: If the AI response stops midway, type "please continue" to resume.

---

## Readiness Check

First, confirm that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "Pre-session check",
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

(ready -> Go to Step 1)
(check_prereq -> Run prerequisite check)
(view_html -> Show the course page path)
(different_lesson -> Show module list)

---

## Step 1: Understand SEO Audit Fundamentals

**AskQuestion configuration:**
```json
{
  "title": "Step 1: Understand SEO audit fundamentals",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Explain the fundamental items to check in an SEO audit.
Organize them into the following categories:
- Technical SEO (site speed, crawling, indexing)
- On-page SEO (title, meta description, heading structure)
- Content SEO (keyword density, internal links, content quality)
- Off-page SEO (backlinks, domain authority)
```

**Expected result**: The 4 SEO audit categories and their checkpoints are explained.

---

## Step 2: Diagnose SEO Issues with the seo-audit Skill

**AskQuestion configuration:**
```json
{
  "title": "Step 2: Diagnose SEO issues with seo-audit",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Use the seo-audit skill to diagnose SEO issues for the following site:
URL: https://example.com (your own site or a practice site)

Focus on the following items:
- Meta tag optimization (title, description)
- Heading structure (H1-H3)
- Image alt attributes
- Internal link structure
- Mobile-friendliness

Save the results as a report to output/seo-audit-report.md.
```

**Expected result**: An SEO audit report is generated with prioritized issues.

---

## Step 3: Design Keyword Strategy with programmatic-seo

**AskQuestion configuration:**
```json
{
  "title": "Step 3: Design keyword strategy and page templates",
  "questions": [{
    "id": "step_action",
    "prompt": "What do you want to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```
Use the programmatic-seo skill to design a keyword strategy on the topic "AI Agent Utilization".

Include the following:
1. Main keywords (5) and long-tail keywords (15)
2. Search intent classification (informational/comparison/transactional)
3. Page template proposals for each keyword
4. Topic cluster structure (pillar page + satellite articles)

Save the results to output/keyword-strategy.md.
```

**Expected result**: A keyword list, page templates, and topic cluster structure are designed.

---

## Common Issues and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "SEO audit results are not displayed"},
      {"id": "trouble_2", "label": "URL access error"},
      {"id": "trouble_3", "label": "Keyword list is too small"},
      {"id": "trouble_4", "label": "Report file is not saved"}
    ]
  }]
}
```

### Issue 1: "SEO audit results are not displayed"
**Cause**: Cannot retrieve the target site HTML or skill loading error
**Solution**:
```
Check the seo-audit skill content.
Read the skill file first and then retry:
skills/seo-audit/SKILL.md
```

### Issue 2: "URL access error"
**Cause**: The target URL does not exist or has access restrictions
**Solution**:
```
Verify that the target URL is accessible.
For practice, you can use a web page like https://ai-agent.camp/en/course as the target.
```

### Issue 3: "Keyword list is too small"
**Cause**: The topic is specified too narrowly
**Solution**:
```
Broaden the topic and regenerate keywords:
"AI agent utilization" -> "AI productivity tools training automation"
Include multiple related concepts.
```

### Issue 4: "Report file is not saved"
**Cause**: The output directory does not exist
**Solution**:
```
Check if the output directory exists; create it if not.
mkdir -p ~/ai-agent-camp/output
```

---

## Checkpoint
- [ ] Understood SEO audit fundamentals (technical/on-page/content/off-page)
- [ ] Diagnosed SEO issues using the seo-audit skill
- [ ] SEO audit report is saved in the output folder
- [ ] Keyword list (5 main + 15 long-tail) is complete
- [ ] Topic cluster structure is designed

---

## Deliverables Preview

### Expected output
```
output/marketing/
  banner-*.png
  (variations)
```
> Format: PNG | Size: auto-configured

### Verification commands
```bash
# File list
ls -la output/marketing/

# Open image (macOS: open / Linux: xdg-open)
open output/marketing/
```

> **Claude Code**: Specify the file path with the Read tool to preview images in chat
> **Cursor**: Click images in the file explorer to preview

---

## Completion Check
Paste the following into the Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## Next Steps

This section is complete. Start the next section or open a new window to begin.

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Open in new window (/start-17-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection guide (example)**:
- next_auto -> /next_lesson
- next_window -> Open /start-17-3 in a new window
- finish -> End
