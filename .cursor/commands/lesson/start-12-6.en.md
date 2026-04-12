---
description: "When the user says /start-12-6 — Module 12 Lesson 12-6: Workflow Automation with Notion"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-5"]
duration: "~35 min"
level: "intermediate"
tags: ["notion", "mcp", "write", "update"]
---

# 🎓 Lesson 12-6: Workflow Automation with Notion

## 📍 What You'll Do

**Lesson 12-6** !

| Item | Details |
|------|------|
| Goal | Perform **page body appending, property updates, and new child page creation** while learning **verification procedures that do not break production** |
| Duration | ~35 min |
| Skills used | Notion MCP (create / update / append), ncli as needed |
| Prerequisites | `/start-12-5` completed |
| Course page | [Module 12: Notion](https://ai-agent.camp/en/course/module-12)  alongside this lesson |

**Session flow:**
1. Duplicate/create a **draft** page or DB and only test there
2. **Present the changes as a diff to the user** before executing
3. After execution, verify the display on the Notion side and understand the rollback procedure

> **Safety**: In shared wikis or production DBs, **always work on a duplicated page**. Do not overwrite production properties without explicit user approval.

---

## 🎯 Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "🎯 Pre-write confirmation",
  "questions": [{
    "id": "target",
    "prompt": "What is the target of the changes?",
    "options": [
      {"id": "sandbox", "label": "Draft/duplicated pages only (recommended)"},
      {"id": "existing", "label": "Existing production page (user takes responsibility)"},
      {"id": "read_only", "label": "Just reviewing the procedure this time"}
    ]
  }]
}
```

---

## 🚀 Step 1: Prepare Sandbox

Agent instruction example:
```text
Create a sub-page with today's date under the "Practice Notion" page,
and only append text there. Do not touch other blocks on the parent page.
```

---

## 🚀 Step 2: Append or Update Properties

1. **Append**: Add headings + bullet points with block append (confirm existing block IDs with the user)
2. **Properties**: Write the **before and after values** for Select / Status / Date, etc. in chat before PATCHing
3. **New DB row**: Fill only the title and required properties, leaving the rest for the user to fill manually

---

## 🚀 Step 3: Verification and Rollback

1. Open Notion and confirm with the user that it is displayed as expected
2. If there are errors, **revert using the same tool** or guide to page history (if available)
3. Include the changed page URL, item name, and new value in the **completion report**

---

## ✅ Completion Criteria

- [ ] If production was directly edited, user approval was recorded in chat beforehand
- [ ] User confirmed the before/after diff at least once
- [ ] Included the exercise page/DB URL in the final report

---

## ➡️ Next Steps

Module 12 (Notion Integration) is now complete.

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
      {"id": "next_window", "label": "Start in new window (/start-13-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-13-1
- finish → End
