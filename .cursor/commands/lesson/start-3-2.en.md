---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module03-screenshot"
prerequisites: ["start-3-1"]
duration: "~25 min"
level: "intermediate"
tags: ["screenshot", "error-diagnosis", "analysis"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 3-2: Advanced Error Diagnosis

## 📍 What You'll Do

**Lesson 3-2: Advanced Error Diagnosis** !

| Item | Details |
|------|---------|
| Goal | Analyze complex error screens, determine priority levels, and propose solutions |
| Duration | ~25 min |
| Skills Used | screenshot-analyzer (advanced) |
| Prerequisites | Lesson 3-1 completed, Gemini API key configured |
| Course Page | [Module 3: Screenshot Analysis](https://ai-agent.camp/en/course/module-3) in parallel |

**Session flow:**
1. Analyze API response errors
2. Prioritize compound errors and determine solutions
3. Apply to real-world use cases

By the end of this session, you will be able to perform production-level error diagnosis.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-session confirmation",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Ready! Let's start"},
      {"id": "check_prereq", "label": "I want to check prerequisites"},
      {"id": "view_html", "label": "I want to see the course page first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready → Go to Step 1)
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Analyze API Response Errors

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Analyze API response errors",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Use the screenshot-analyzer skill to analyze the API response error.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/api-error-response.png
Output: output/screenshots/api-error-analysis.html

Analysis content:
- Meaning of error codes
- Root cause estimation
- Priority determination (High/Medium/Low)
- Specific resolution steps
```

**Expected result**: A detailed error analysis is output in HTML format with priority levels and resolution steps clearly documented.

---

## 🚀 Step 2: Prioritize Multiple Errors

Analyze screens where multiple errors occur simultaneously:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Prioritize multiple errors",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
Analyze the screenshot showing multiple errors.

Input: courses/aiagent/lesson03-core/module03-screenshot/practice/data/screenshots/multiple-errors.png
Output: output/screenshots/error-priority.png

Classify errors by severity:
- [High] Red frame: Immediate action required
- [Medium] Yellow frame: Early action preferred
- [Low] Blue frame: Address when time permits

Number each error and clarify the response order.
```

**Expected result**: An image is generated where each error is color-coded, making response priority clear at a glance.

---

## 🚀 Step 3: Diagnose Common Error Patterns

Let's practice diagnosing common HTTP errors:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Diagnose common error patterns",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Continue as-is"},
      {"id": "review", "label": "Just review examples"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**After selection (example)**:
Input:
```
For the following error patterns, propose diagnoses and solutions
even without screenshots:

1. 502 Bad Gateway
2. 503 Service Unavailable
3. 401 Unauthorized
4. CORS error

Summarize the cause and solution for each in table format.
```

**Expected result**: A table summarizing the cause and solution for each error is displayed.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select your issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Please select the one that applies",
    "options": [
      {"id": "trouble_1", "label": "Analysis results are too abstract"},
      {"id": "trouble_2", "label": "Cannot understand the relationship between multiple errors"},
      {"id": "trouble_3", "label": "Cannot understand the priority criteria"},
      {"id": "trouble_4", "label": "HTML output has character encoding issues"}
    ]
  }]
}
```


### Issue 1: "Analysis results are too abstract"
**Cause**: Insufficient information in the screenshot
**Solution prompt**:
```
Tell me what additional information is needed for more accurate error analysis.
Also suggest elements that should be included in the screenshot (console log, network tab, etc.).
```

### Issue 2: "Cannot understand the relationship between multiple errors"
**Cause**: The error chain relationship is complex
**Solution prompt**:
```
In this error screen, analyze which error is the root cause
and which errors are derived.
Diagram the causal relationships between errors.
```

### Issue 3: "Cannot understand the priority criteria"
**Cause**: The evaluation criteria are not clear
**Solution prompt**:
```
Tell me the criteria for determining error priority.
Explain from the following perspectives:
- User impact
- Business impact
- Technical severity
- Response urgency
```

### Issue 4: "HTML output has character encoding issues"
**Cause**: Character encoding issue
**Solution prompt**:
```
The generated HTML file has character encoding issues.
Please regenerate with UTF-8 encoding.
```

---

## ✅ Checkpoint
- [ ] Can automatically analyze error screenshots
- [ ] Can distinguish between root causes and derived issues
- [ ] Can determine response order based on priority
- [ ] Can output analysis reports in HTML format
- [ ] Can color-code and visualize multiple errors


---

## 📋 Output Preview

### Expected Output
```
📁 output/screenshots/
├── analyzed-{target-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File list
ls -la output/screenshots/

# Open image (macOS: open / Linux: xdg-open)
open output/screenshots/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "Please select the next action",
    "options": [
      {"id": "next_auto", "label": "Start the next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in new window (/start-3-3)"},
      {"id": "finish", "label": "End here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-3-3
- finish → End
