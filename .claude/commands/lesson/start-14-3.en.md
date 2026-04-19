---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~35 min"
prerequisites: ["start-14-1", "start-14-2"]
level: "intermediate"
tags: ["article", "writing"]
---

# 🎓 Lesson 14-3: Article Writing - Style-Applied Draft Creation

## 📍 What You'll Do

Welcome to **Lesson 14-3: Article Writing - Style-Applied Draft Creation**!

| Item | Details |
|------|---------|
| Goal | Apply the style profile to generate an article draft |
| Duration | ~35 min |
| Skills Used | article-writer, style-analyzer |
| Prerequisites | Lesson 14-1 (outline) and Lesson 14-2 (style profile) complete |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Review the outline from 14-1 and the style profile from 14-2
2. Generate a style-applied draft with article-writer
3. Review and manually adjust the draft

By the end of this session, an article draft (Markdown format) reflecting your writing style will be complete.

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

## 🚀 Step 1: Review Outline and Style Profile

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Review Previous Deliverables",
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
Read the following 2 files and verify the article writing preparation status.

1. Outline: output/article-14-1-outline-final.md
2. Style profile: output/style_profile.yaml

Verification points:
- Is the outline heading structure appropriate?
- Key style profile parameters (sentence endings, sentence length, tone)
- The expected article image from combining both

If there are issues, propose corrections.
```

**Expected result**: The outline and style profile contents are confirmed, and article writing preparation is complete.

---

## 🚀 Step 2: Generate Style-Applied Draft with article-writer

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Generate Style-Applied Draft",
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
Use the article-writer skill to generate an article draft combining the outline and style profile.

Execution command:
python skills/article-writer/scripts/article_writer.py --theme output/article-14-1-outline-final.md --style output/style_profile.yaml --output output/article-14-3-draft.md

Generation conditions:
- Outline: Follow the structure in output/article-14-1-outline-final.md
- Style: Apply the style parameters from output/style_profile.yaml
- Illustration markers: Maintain <!-- illustration: ... --> at positions specified in the outline
- Word count: Match the estimated word count set in the outline

Save the results to output/article-14-3-draft.md.
```

**Expected result**: An article draft reflecting your writing style is generated in Markdown format. Illustration markers are placed at appropriate positions.

---

## 🚀 Step 3: Review and Manually Adjust the Draft

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Review and Adjust the Draft",
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
Review the draft in output/article-14-3-draft.md.

Please review and provide feedback from these perspectives:
1. Style consistency: Is the style profile's characteristics reflected throughout the article?
2. Introduction hook: Do the first 3 lines capture reader interest?
3. Section transitions: Are conjunctions and introductory sentences natural?
4. Specificity: Are there sections that are too abstract?
5. Summary and CTA: Does it encourage reader action?

If you want to modify any sections, please indicate them.
Save the revised final draft to output/article-14-3-draft-final.md.
```

**Expected result**: Draft review results are shown, and the revised final draft is saved.

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
      {"id": "trouble_1", "label": "Style doesn't match the style profile"},
      {"id": "trouble_2", "label": "Article is too long or too short"},
      {"id": "trouble_3", "label": "Illustration markers disappeared"},
      {"id": "trouble_4", "label": "Previous files can't be found"}
    ]
  }]
}
```


### Issue 1: "Style doesn't match the style profile"
**Cause**: Style profile parameters weren't loaded correctly
**Solution prompt**:
```text
Re-check the style profile (output/style_profile.yaml) and
regenerate with the following parameters explicitly specified:
- Sentence endings: polite form (desu/masu)
- Average sentence length: 40-60 characters
- Tone: friendly but polite
Explicitly specify the profile with the --style option.
```

### Issue 2: "Article is too long or too short"
**Cause**: Word count specification was ambiguous
**Solution prompt**:
```text
Regenerate the draft with explicit target word counts per section:
- Introduction: 300-400 characters
- Each body section: 500-700 characters
- Summary: 200-300 characters
Adjust to fit within the overall target word count.
```

### Issue 3: "Illustration markers disappeared"
**Cause**: Markers were removed during draft generation
**Solution prompt**:
```text
Extract illustration markers from the outline (output/article-14-1-outline-final.md)
and re-insert them at the corresponding positions in the draft.
Format: <!-- illustration: type=image|diagram, description="description text" -->
```

### Issue 4: "Previous files can't be found"
**Cause**: Lesson 14-1/14-2 not completed, or file paths differ
**Solution prompt**:
```bash
Check the contents of the output directory:
ls -la ~/ai-agent-camp/output/
If the outline or style profile is missing,
complete Lesson 14-1 (/start-14-1) and Lesson 14-2 (/start-14-2) first.
```

---

## ✅ Checkpoint
- [ ] Reviewed the outline and style profile contents
- [ ] Generated a style-applied draft with article-writer
- [ ] Draft writing style matches the style profile
- [ ] Saved the reviewed and adjusted final draft to output/

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-3-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-3-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-3-*.md
```

> 💡 View full text: `cat output/article-14-3-*.md` to display the entire file

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
      {"id": "next_window", "label": "Open in new window (/start-14-4)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-4 in a new window
- finish → End
