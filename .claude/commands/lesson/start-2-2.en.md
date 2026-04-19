---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module02-diagram"
prerequisites: ["start-2-1"]
duration: "~25 min"
level: "beginner"
tags: ["diagram", "infographic", "visualization"]
---

# 🎓 Lesson 2-2: Infographic Creation

## 📍 What You'll Do

Welcome to **Lesson 2-2: Infographic Creation**!

| Item | Details |
|------|---------|
| Goal | Visualize statistical data with infographics and create persuasive diagrams |
| Duration | ~25 min |
| Skills Used | diagram-generator (infographic support) |
| Prerequisites | Lesson 2-1 completed, Gemini API key configured |
| Course Page | Refer to [Module 2: Diagrams & Flows](https://ai-agent.camp/en/course/module-2) in parallel |

**Session flow:**
1. Understand infographic elements
2. Visualize statistical data
3. Adjust layout and colors

By the end of this session, infographics visualizing data will be saved in outputs.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "it stopped" to resume. This is a Cursor behavior, not a malfunction.

---

## 🎯 Readiness Check

Let's verify that everything is ready.

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-Session Check",
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
(check_prereq → Run prerequisite check)
(view_html → Show course page path)
(different_lesson → Show module list)

---

## 🚀 Step 1: Understand Infographic Elements

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 1: Understand Infographic Elements",
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

**After selection (example)**:
Input:
```
Explain the basic elements for creating effective infographics.
Cover data visualization, icons, color usage, and layout tips.
```

**Expected result**: Four basic infographic elements are explained:
- Data visualization (graphs, charts)
- Icons and illustrations
- Color usage and emphasis
- Hierarchy and layout

---

## 🚀 Step 2: Visualize Statistical Data

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 2: Visualize Statistical Data",
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

**After selection (example)**:
Input:
```
Use diagram-generator to visualize the following data as an infographic:

Remote Work Implementation Results:
- Commute time reduction: 75%
- Productivity increase: 30%
- Cost savings: 40%
- Employee satisfaction: 85%

Design it so the numbers are immediately clear at a glance.
Output: ~/ai-agent-camp/output/infographic-remote.png
```

**Expected result**: An infographic is generated where four metrics are visually represented clearly.

---

## 🚀 Step 3: Create a Before/After Comparison

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 3: Create a Before/After Comparison",
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

**After selection (example)**:
Input:
```
Create an infographic comparing before and after AI adoption:

[Before]
- Processing time: 8 hours
- Error rate: 15%
- Cases handled: 100/day

[After]
- Processing time: 30 minutes
- Error rate: 2%
- Cases handled: 500/day

[Improvement]
- Time: 94% reduction
- Errors: 87% reduction
- Efficiency: 5x improvement

Use a layout that clearly shows the before/after comparison.
Output: ~/ai-agent-camp/output/infographic-comparison.png
```

**Expected result**: A comparison infographic showing changes before and after at a glance is generated.

---

## 🚀 Step 4: Practice Exercise - Service Usage Statistics

Create a practical infographic using the following prompts:

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 4: Practice Exercise - Service Usage Statistics",
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

**After selection (example)**:
Input:
```
Visualize SaaS service usage statistics as an infographic:

Key Metrics:
- Monthly active users: 500,000 (150% YoY growth)
- Average usage time: 25 min/day
- Paying users: 50,000 (10% conversion rate)
- Annual revenue: 1 billion yen

Emphasize the growth trend, showing YoY comparison and conversion rate.
Output: ~/ai-agent-camp/output/infographic-saas.png
```

**Expected result**: An infographic with hierarchically organized business metrics is generated.

---

## 🚀 Step 5: Create a Narrative Infographic

Use AskUserQuestion (AskQuestion) to choose "Continue / Just review examples / Skip."

**AskQuestion configuration example:**
```json
{
  "title": "🚀 Step 5: Create a Narrative Infographic",
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

**After selection (example)**:
Input:
```
Visualize "A User's Daily Behavior Pattern" as an infographic:

In timeline format, express the following:
- 7:00 Wake up, check weather on app (80% usage rate)
- 8:00 Commuting, browse news (65% usage rate)
- 12:00 Lunch break, check social media (90% usage rate)
- 18:00 Commuting home, watch videos (75% usage rate)
- 21:00 Before bed, browse shopping sites (55% usage rate)

Design it as a narrative that follows the flow of time.
Output: ~/ai-agent-camp/output/infographic-timeline.png
```

**Expected result**: User behavior along a timeline is visually expressed.

---

## ⚠️ Common Issues and Solutions

Use AskUserQuestion (AskQuestion) to select your issue and get guided assistance.

**AskQuestion configuration example:**
```json
{
  "title": "Select Your Issue",
  "questions": [{
    "id": "trouble",
    "prompt": "Select the issue that applies",
    "options": [
      {"id": "trouble_1", "label": "Too many numbers, hard to read"},
      {"id": "trouble_2", "label": "Comparison is unclear"},
      {"id": "trouble_3", "label": "Design is monotonous"},
      {"id": "trouble_4", "label": "Story doesn't come through"}
    ]
  }]
}
```


### Issue 1: "Too many numbers, hard to read"
**Cause**: Too much information packed in
**Solution prompt**:
```
Narrow down to the 3 most important metrics.
Move remaining information to a separate infographic or add as supplementary text.
```

### Issue 2: "Comparison is unclear"
**Cause**: Inconsistent expression of values
**Solution prompt**:
```
Express all values as percentages or multiples:
- "8 hours → 30 minutes" → instead "94% reduction"
- "100 cases → 500 cases" → instead "5x increase"
```

### Issue 3: "Design is monotonous"
**Cause**: Lacking visual elements
**Solution prompt**:
```
Add the following elements:
- Icons for each metric
- Large font for important numbers
- Color coding to distinguish items
- Use graphs and charts
```

### Issue 4: "Story doesn't come through"
**Cause**: Flow and relationships between information are unclear
**Solution prompt**:
```
Add the following elements to the infographic:
- A clear title (showing the conclusion)
- Arrows indicating information flow
- Group related metrics together
- Make the key message the most prominent
```

---

## ✅ Checkpoint
- [ ] Understood basic infographic elements
- [ ] Visually represented statistical data
- [ ] Effectively presented a Before/After comparison
- [ ] Completed the practice exercise (SaaS statistics)
- [ ] Created a narrative infographic


---

## 📋 Output Preview

### Expected Output
```
📁 output/diagrams/
├── flow-{theme-name}.png
└── (variations)
```
> Format: PNG | Size: Auto-configured

### Verification Commands
```bash
# File listing
ls -la output/diagrams/

# Open images (macOS: open / Linux: xdg-open)
open output/diagrams/
```

> 💡 **Claude Code**: Specify the file path with the Read tool to preview images in chat
> 💡 **Cursor**: Click on the image in the file explorer to preview

---

## ✅ Completion Check
Paste the following into Cursor chat to verify completion:

```
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: A pass/fail judgment and any missing items are displayed.

---

## ➡️ Next Steps

This section is now complete. Start the next section, or open a new window to begin a new section.

Use AskUserQuestion (AskQuestion) to choose.

**AskQuestion configuration example:**
```json
{
  "title": "Select Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Choose your next action",
    "options": [
      {"id": "next_auto", "label": "Start next section (/next_lesson)"},
      {"id": "next_window", "label": "Start in a new window (/start-2-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection (example)**:
- next_auto → /next_lesson
- next_window → Open new window with /start-2-3
- finish → End
