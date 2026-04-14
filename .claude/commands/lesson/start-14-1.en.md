---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~25 min"
prerequisites: []
level: "beginner"
tags: ["article", "planning"]
---

# 🎓 Lesson 14-1: Article Planning - Topic Selection and Outline Generation

## 📍 What You'll Do

Welcome to **Lesson 14-1: Article Planning - Topic Selection and Outline Generation**!

| Item | Details |
|------|---------|
| Goal | Determine the article theme, set the target audience, and generate an article outline |
| Duration | ~25 min |
| Skills Used | article-writer |
| Prerequisites | Gemini API key configured |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Set the article theme and target audience
2. Auto-generate an outline with the article-writer skill
3. Review and adjust the outline structure

By the end of this session, the article theme, target audience, and outline (heading structure) will be finalized.

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

## 🚀 Step 1: Set the Theme and Target Audience

In Codex, you typically select from choices in chat to choose the article type.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Choose Article Type",
  "questions": [{
    "id": "article_type",
    "prompt": "What type of article will you write?",
    "options": [
      {"id": "blog", "label": "Blog post (casual, readability-focused)"},
      {"id": "explainer", "label": "Explainer article (concept and mechanism explanation)"},
      {"id": "technical", "label": "Technical article (procedures and implementation details)"},
      {"id": "free_theme", "label": "Free theme (specify your own)"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
Input:
```text
Set the article theme and target audience with the following conditions.

Article type: Blog post
Theme candidate: Improving work efficiency with AI tools
Target audience: Business professionals in their 30s-40s, moderate IT literacy

Please output the following:
1. Article title proposals (3 candidates)
2. Target reader persona (age, occupation, challenges, goals)
3. Article purpose (what action to encourage from readers)
4. Estimated word count
5. Keyword candidates (for SEO, 3-5 keywords)

Save the results to output/article-14-1-theme.md.
```

**Expected result**: Theme candidates, target persona, and article purpose are organized and saved as a Markdown file.

---

## 🚀 Step 2: Generate Outline with article-writer Skill

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Generate Outline",
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
Use the article-writer skill to generate an article outline for the following theme.

Theme: Improving work efficiency with AI tools
Target: Business professionals in their 30s-40s
Article type: Blog post
Estimated word count: 3000-4000 characters

Create an outline that includes:
1. Introduction (hook + article overview)
2. Body heading structure (H2/H3 level)
3. Key points memo for each section (2-3 lines)
4. Illustration candidate positions (<!-- illustration: type=image/diagram, description="..." --> format)
5. Summary and CTA

Save the results to output/article-14-1-outline.md.
```

**Expected result**: An outline with heading structure, section key points, and illustration markers is generated.

---

## 🚀 Step 3: Review and Adjust the Outline

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Review and Adjust the Outline",
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
Review the outline in output/article-14-1-outline.md.

Please provide feedback from the following perspectives:
1. Logical flow: Are the connections between sections natural?
2. Comprehensiveness: Does it answer the target reader's questions?
3. Readability: Is the length balance between sections appropriate?
4. Illustration placement: Are the insertion points for figures and images effective?

If improvements are needed, propose a revised version and
save the final version to output/article-14-1-outline-final.md.
```

**Expected result**: Outline review results and improvement proposals are shown, and the final outline is saved.

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
      {"id": "trouble_1", "label": "Can't decide on a theme / theme is too broad"},
      {"id": "trouble_2", "label": "Outline is shallow / lacks specificity"},
      {"id": "trouble_3", "label": "Illustration markers aren't generated"},
      {"id": "trouble_4", "label": "File isn't saved"}
    ]
  }]
}
```


### Issue 1: "Can't decide on a theme / theme is too broad"
**Cause**: The theme granularity is too large and lacks focus
**Solution prompt**:
```text
To narrow down the theme, answer the following 3 questions:
1. What does the reader most want to know? (just one thing)
2. What do you want the reader to do after reading this article?
3. What differentiates this from similar articles?
Use these answers to reset the theme.
```

### Issue 2: "Outline is shallow / lacks specificity"
**Cause**: Insufficient theme or target information
**Solution prompt**:
```text
To make the outline more specific, add the following to each section:
- At least one concrete example or data point
- One question to the reader
- One action item
```

### Issue 3: "Illustration markers aren't generated"
**Cause**: The illustration marker format wasn't specified in the prompt
**Solution prompt**:
```text
Add illustration markers to the outline.
Format: <!-- illustration: type=image|diagram, description="description text" -->
Place at least one illustration marker in each H2 section.
```

### Issue 4: "File isn't saved"
**Cause**: The output directory doesn't exist
**Solution prompt**:
```bash
Check if the output directory exists, and create it if not.
mkdir -p ~/ai-agent-camp/output
```

---

## ✅ Checkpoint
- [ ] Determined the article theme and title proposals
- [ ] Set the target reader persona
- [ ] Generated an outline with the article-writer skill
- [ ] Reviewed the outline and saved the final version to output/

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-1-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-1-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-1-*.md
```

> 💡 View full text: `cat output/article-14-1-*.md` to display the entire file

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
      {"id": "next_window", "label": "Open in new window (/start-14-2)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-2 in a new window
- finish → End
