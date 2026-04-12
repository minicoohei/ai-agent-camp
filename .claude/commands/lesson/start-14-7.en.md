---
description: "When the user says /start-14-7 — Module 14 Lesson 14-7: Article Writing - Parallel Execution and Finishing"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~40 min"
prerequisites: ["start-14-1", "start-14-2", "start-14-3", "start-14-4", "start-14-5", "start-14-6"]
level: "advanced"
tags: ["article", "parallel"]
---

# 🎓 Lesson 14-7: Parallel Execution and Finishing - Multi-Article Batch Processing

## 📍 What You'll Do

Welcome to **Lesson 14-7: Parallel Execution and Finishing - Multi-Article Batch Processing**!

| Item | Details |
|------|---------|
| Goal | Learn how to generate articles in parallel across multiple themes and run the entire pipeline in batch |
| Duration | ~40 min |
| Skills Used | article-writer, style-analyzer, proofreading-agent, fact-checker, nanobanana, diagram-generator |
| Prerequisites | Lessons 14-1 through 14-6 complete (understanding of all stages) |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Set up multiple themes
2. Demonstrate parallel article generation using the Task tool
3. Run proofreading and fact-checking in parallel for each article
4. Final review and output of all articles

By the end of this session, articles across multiple themes will be completed in parallel, and you will have mastered the batch execution pattern for the entire pipeline.

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

## 🚀 Step 1: Set Up Multiple Themes

In Codex, you typically select from choices in chat to choose the number of themes.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Choose Number of Themes",
  "questions": [{
    "id": "theme_count",
    "prompt": "Select the number of themes for parallel generation",
    "options": [
      {"id": "two", "label": "2 themes (beginner-friendly, shorter processing time)"},
      {"id": "three", "label": "3 themes (standard, experience the effect of parallel processing)"},
      {"id": "custom", "label": "Specify themes yourself"}
    ]
  }]
}
```

**If "2 themes":**
Input:
```text
We will generate articles in parallel for the following 2 themes.

Theme A: "5 Tips to Boost Remote Work Productivity"
- Target: Business professionals working from home
- Article type: Blog post
- Estimated word count: 2500-3000 characters

Theme B: "Skills Required in the AI Era"
- Target: People in their 20s-30s considering career advancement
- Article type: Explainer article
- Estimated word count: 3000-3500 characters

Save each theme's outline to output/batch/theme-a-outline.md and theme-b-outline.md.
```

**If "3 themes":**
```text
We will generate articles in parallel for the following 3 themes.

Theme A: "5 Tips to Boost Remote Work Productivity"
Theme B: "Skills Required in the AI Era"
Theme C: "Communication Techniques to Improve Team Efficiency"

Save each theme's outline to output/batch/.
```

**Expected result**: Outlines for multiple themes are generated in output/batch/.

---

## 🚀 Step 2: Parallel Article Generation Using the Task Tool

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Run Parallel Article Generation",
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
Use the Task tool to generate articles for multiple themes in parallel.

Run the following stages in parallel for each theme:
1. Outline → draft generation (article-writer + style-analyzer)
2. Illustration marker detection and image generation (nanobanana / diagram-generator)
3. Image embedding

Parallel execution pattern:
- Task 1: Theme A article generation (output/batch/theme-a-draft.md)
- Task 2: Theme B article generation (output/batch/theme-b-draft.md)
(Add Task 3 for 3 themes)

Use the shared style profile output/style_profile.yaml for all themes.
Save all results to output/batch/ after all tasks complete.
```

**Expected result**: Article drafts for multiple themes are generated in parallel, with processing time shorter than sequential execution.

---

## 🚀 Step 3: Parallel Proofreading and Fact-Checking

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Run Parallel Proofreading and Fact-Checking",
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
Run proofreading and fact-checking in parallel for each article.

Parallel execution pattern:
- Task 1: Theme A proofreading (proofreading-agent)
- Task 2: Theme B proofreading (proofreading-agent)
- Task 3: Theme A fact-checking (fact-checker) *after proofreading completes
- Task 4: Theme B fact-checking (fact-checker) *after proofreading completes

Results for each task:
- output/batch/theme-a-proofread.md
- output/batch/theme-b-proofread.md
- output/batch/theme-a-final.md
- output/batch/theme-b-final.md

Pipeline: Proofreading → Fact-checking → Citation addition → Final version saved
```

**Expected result**: Proofreading and fact-checking for all articles are completed in parallel, with final versions saved.

---

## 🚀 Step 4: Final Review and Output of All Articles

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 4: Final Review and Output",
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
Create a final report for all articles in output/batch/.

Report contents:
1. Summary of each article
   - Theme, word count, number of illustrations, number of citations
2. Quality score
   - Proofreading correction rate
   - Fact-check pass rate
3. Parallel processing efficiency
   - Time comparison with sequential execution (estimated)
   - Time saved by parallel processing
4. List of all articles (with file paths)

Save the report to output/batch/batch-report.md.

Also display a summary reviewing the entire Module 14 learning content:
- Lesson 14-1: Theme setting and outline
- Lesson 14-2: Style profile
- Lesson 14-3: Style-applied draft
- Lesson 14-4: Illustration generation
- Lesson 14-5: Proofreading
- Lesson 14-6: Fact-checking
- Lesson 14-7: Parallel execution (this lesson)
```

**Expected result**: A final report for all articles and a Module 14 learning summary are output.

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
      {"id": "trouble_1", "label": "Some parallel tasks fail"},
      {"id": "trouble_2", "label": "Processing time is too long"},
      {"id": "trouble_3", "label": "Styles are inconsistent across articles"},
      {"id": "trouble_4", "label": "Files not found in output/batch/"}
    ]
  }]
}
```


### Issue 1: "Some parallel tasks fail"
**Cause**: API rate limits, or one task's error affecting others
**Solution prompt**:
```text
Re-run only the failed tasks.
If due to API rate limits, wait 30 seconds before re-running.
Results from successful tasks are preserved.
Check file paths for failed themes: ls output/batch/
```

### Issue 2: "Processing time is too long"
**Cause**: Too many themes, or article word count is too high
**Solution prompt**:
```text
You can reduce processing time by:
1. Reducing the number of themes to 2
2. Setting each article's estimated word count to under 2000 characters
3. Skipping illustration generation (can be added later)
4. Limiting proofreading and fact-checking to "High severity only"
```

### Issue 3: "Styles are inconsistent across articles"
**Cause**: Each task interpreting style independently
**Solution prompt**:
```text
Explicitly specify the same style profile (output/style_profile.yaml)
for all articles.
Make sure each task's --style option includes the profile path.
You can also run an additional style consistency check after generation.
```

### Issue 4: "Files not found in output/batch/"
**Cause**: Directory doesn't exist
**Solution prompt**:
```bash
Create the directory and re-run:
mkdir -p ~/ai-agent-camp/output/batch
```

---

## ✅ Checkpoint
- [ ] Set up outlines for multiple themes (2-3 articles)
- [ ] Generated article drafts in parallel with the Task tool
- [ ] Ran proofreading and fact-checking in parallel
- [ ] Final versions of all articles saved to output/batch/
- [ ] Verified quality and efficiency with the batch report

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-7-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-7-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-7-*.md
```

> 💡 View full text: `cat output/article-14-7-*.md` to display the entire file

---

## ✅ Completion Check
Enter the following in the Codex chat to verify completion:

```bash
# Completion check: Verify that the expected output files have been generated in the output/ folder.
```

**Expected result**: Completion/incomplete status and missing items are displayed.

---

## ➡️ Next Steps

All lessons in Module 14: Article Writing are now complete!

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
      {"id": "next_window", "label": "Open in new window (/start-15-1)"},
      {"id": "review_module", "label": "Review Module 14"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-15-1 in a new window
- review_module → Review each lesson of Module 14
- finish → End
