---
description: "When the user says /start-12-2 — Module 12 Lesson 12-2: Database Operations (CRUD)"
chapter: "courses/aiagent/lesson03-core/module12-notion"
prerequisites: ["start-12-1"]
duration: "~30 min"
level: "intermediate"
tags: ["notion", "database", "automation"]
---

# 🎓 Lesson 12-2: Notion Database Operations

## 📍 What You'll Do

**Lesson 12-2: Notion Database Operations**!

| Item | Details |
|------|------|
| Goal | Automate Notion database creation, querying, and updating, and operate task management from Claude Code |
| Duration | ~30 min |
| Skills used | Notion API (databases) |
| Prerequisites | Lesson 12-1 completed, Notion integration created |
| Course page | [Module 12: Notion](https://ai-agent.camp/en/course/module-12)  alongside this lesson |

**Session flow:**
1. Create a task management database
2. Queries and filters
3. Add, update, and delete records

By the end of this session, you will be able to manage Notion tasks and projects from code.

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
(view_html → Show course page path)
(different_lesson → Display module list)

---

## 🚀 Step 1: Create Task Management Database

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Create Task Management Database",
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
Please create the following database in Notion:

Database name: Project Tasks

Properties:
1. Task Name (Title)
2. Status (Select)
   - Not Started (gray)
   - In Progress (blue)
   - In Review (yellow)
   - Completed (green)
3. Deadline (Date)
4. Priority (Select)
   - Urgent (red)
   - High (orange)
   - Medium (yellow)
   - Low (gray)
5. Estimated Hours (Number) - in hours
6. Category (Multi-select)
   - Development
   - Design
   - Planning
   - Documentation
```

**Expected result:** A database with properties is created in Notion.

---

## 🚀 Step 2: Add Sample Tasks

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Add Sample Tasks",
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
Please add the following tasks to the "Project Tasks" database:

1. Task name: Create API Documentation
   - Status: Not Started
   - Deadline: Next Friday
   - Priority: High
   - Estimated hours: 4
   - Category: Documentation

2. Task name: Implement User Authentication
   - Status: In Progress
   - Deadline: 3 days later
   - Priority: Urgent
   - Estimated hours: 8
   - Category: Development

3. Task name: Create UI Mockup
   - Status: Not Started
   - Deadline: 5 days later
   - Priority: Medium
   - Estimated hours: 6
   - Category: Design

After adding, display the database contents.
```

**Expected result:** 3 tasks are added to the database.

---

## 🚀 Step 3: Data Retrieval and Filtering

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Data Retrieval and Filtering",
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
Please retrieve tasks from the "Project Tasks" database with the following conditions:

Query 1: Get all tasks
- Retrieve and display all tasks

Query 2: Incomplete tasks only
- Retrieve tasks whose status is not "Completed"

Query 3: High priority tasks
- Retrieve tasks with "Urgent" or "High" priority
- Sort by deadline

Display each result in table format.
```

**Expected result:** Tasks matching the conditions are retrieved and displayed.

---

## 🚀 Step 4: Update Tasks

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Update Tasks",
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
Please perform the following updates in the "Project Tasks" database:

1. "Create API Documentation" task
   - Change status to "In Progress"

2. "Implement User Authentication" task
   - Change status to "In Review"
   - Update estimated hours to 10 (actual time increased)

After updating, display the status of all tasks.
```

**Expected result:** Task statuses are updated.

---

## 🚀 Step 5: Aggregation and Report

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Aggregation and Report",
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
Please create an aggregation report for the "Project Tasks" database:

Aggregation content:
1. Task count by status
   - Not Started: X items
   - In Progress: X items
   - In Review: X items
   - Completed: X items

2. Total estimated hours by category
   - Development: X hours
   - Design: X hours
   - Planning: X hours
   - Documentation: X hours

3. Completion rate
   - Completed tasks / Total tasks = X%

4. Tasks due this week
   - Display task name, priority, status

Please output the report in a readable format.
```

**Expected result:** Database statistics are output in report format.

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
      {"id": "trouble_1", "label": "Database not found"},
      {"id": "trouble_2", "label": "Cannot create properties"},
      {"id": "trouble_3", "label": "Filters do not work"},
      {"id": "trouble_4", "label": "Date specification does not work"}
    ]
  }]
}
```


### Issue 1: "Database not found"
**Cause:** Database ID is incorrect or access permissions are missing
**Solution prompt:**
```
Please verify the following:
1. The integration has been added to the page where the database exists
2. The database name is correct
3. The integration has been added to the parent page
```

### Issue 2: Cannot create properties
**Cause:** Property type specification is incorrect
**Solution prompt:**
```
Please check the property types supported by the Notion API:
- title, rich_text, number, select, multi_select, date, people, checkbox, etc.
Select/Multi-select options need to be defined in advance.
```

### Issue 3: Filters do not work
**Cause:** Filter syntax is incorrect
**Solution prompt:**
```
Please check the Notion API filter syntax:
- Single condition: {"property": "Status", "select": {"equals": "Completed"}}
- Multiple conditions: {"and": [condition1, condition2]}
```

### Issue 4: Date specification does not work correctly
**Cause:** Date format is incorrect
**Solution prompt:**
```
Please specify Notion API dates in ISO 8601 format:
- Date only: "2024-01-15"
- Date and time: "2024-01-15T09:00:00"
Also consider the timezone.
```

---

## ✅ Checkpoint
- [ ] Database can be created
- [ ] Tasks can be added
- [ ] Filtering is working
- [ ] Tasks can be updated
- [ ] Aggregation report can be generated

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Please verify that the expected output files have been generated in the output/ folder.
```

**Expected result:** Completion/incomplete status and missing items are displayed.

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
      {"id": "next_window", "label": "Start in new window (/start-6-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Guidance after selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-6-1
- finish → End
