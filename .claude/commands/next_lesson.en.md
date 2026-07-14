---
description: "Check completion and proceed to the next lesson"
nonInteractiveMode: deferred
---
# /next_lesson

## ✅ Completion Check and Next Lesson
Check completion status and automatically guide to the next lesson.

You can choose how to proceed using AskUserQuestion (AskQuestion).

**AskQuestion example:**
```json
{
  "title": "Proceed to the next lesson",
  "questions": [{
    "id": "next_action",
    "prompt": "What would you like to do?",
    "options": [
      {"id": "check_next", "label": "Check completion and proceed"},
      {"id": "mark_done", "label": "Manually mark as complete and proceed"},
      {"id": "list_lessons", "label": "View lesson list"}
    ]
  }]
}
```

## Actions

### 1) Check completion and proceed
```
uv run python tools/lesson_progress.py --next
```

### 2) Manually mark as complete and proceed
```
uv run python tools/lesson_progress.py --mark <current-lesson-id>
uv run python tools/lesson_progress.py --next
```
> Replace `<current-lesson-id>` with the lesson you just completed (e.g., `start-1-1`, `start-3-2`).

### 3) View lesson list
```
uv run python tools/lesson_progress.py --list
```
