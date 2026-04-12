---
description: "When the user says /start-14-2 — Module 14 Lesson 14-2: Article Writing - Style Learning and Style Profile Creation"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-1"]
level: "beginner"
tags: ["article", "style"]
---

# 🎓 Lesson 14-2: Style Learning - Style Profile Creation

## 📍 What You'll Do

Welcome to **Lesson 14-2: Style Learning - Style Profile Creation**!

| Item | Details |
|------|---------|
| Goal | Feed multiple writing samples to analyze style characteristics and create a style profile |
| Duration | ~30 min |
| Skills Used | style-analyzer |
| Prerequisites | Lesson 14-1 complete, Gemini API key configured, writing samples for analysis (3-5 recommended) |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Prepare your writing samples (3-5 recommended)
2. Run style analysis with style-analyzer
3. Review and understand the generated style profile

By the end of this session, a style profile (YAML format) quantifying your writing style characteristics will be complete.

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

## 🚀 Step 1: Prepare Writing Samples

In Codex, you typically select from choices in chat to indicate your sample preparation status.

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Prepare Writing Samples",
  "questions": [{
    "id": "sample_status",
    "prompt": "Do you have writing samples for analysis?",
    "options": [
      {"id": "ready", "label": "Samples ready (specify file path)"},
      {"id": "write_now", "label": "Write sample text now"},
      {"id": "use_demo", "label": "Use demo samples"}
    ]
  }]
}
```

**Post-selection instructions (example)**:

**If "Samples ready":**
```text
Please provide the file paths of the writing samples for analysis.
3-5 Markdown or text files are ideal.
Example: output/samples/sample1.md, output/samples/sample2.md
```

**If "Write sample text now":**
```text
Let's create writing samples in the output/samples/ directory.
Using the template below, write 3 short texts (300-500 characters each):

Theme examples:
1. Something you learned recently
2. A tool recommendation
3. Work tips and tricks

Save each file as output/samples/sample1.md, sample2.md, sample3.md.
```

**If "Use demo samples":**
```text
Generate 3 demo sample texts and save them to output/samples/.
Samples with different style patterns (casual/formal/technical) will be included.
```

**Expected result**: 3-5 writing samples for analysis are prepared in output/samples/.

---

## 🚀 Step 2: Run Style Analysis with style-analyzer

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Run Style Analysis",
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
Use the style-analyzer skill to run a style analysis on the following writing samples.

Input files:
- output/samples/sample1.md
- output/samples/sample2.md
- output/samples/sample3.md

Analysis items:
1. Sentence ending patterns (polite form, plain form, mixed)
2. Average sentence length (characters per sentence)
3. Kanji/hiragana/katakana ratio
4. Tone characteristics (politeness, friendliness, technicality)
5. Conjunction tendencies (frequency, commonly used conjunctions)
6. Paragraph structure patterns (sentences per paragraph, line break frequency)

Save the results to output/style_profile.yaml.

Execution command:
python skills/style-analyzer/scripts/style_analyzer.py --input output/samples/sample1.md --input output/samples/sample2.md --input output/samples/sample3.md --output output/style_profile.yaml
```

**Expected result**: Writing style characteristics are quantified, structured, and saved as a YAML style profile.

---

## 🚀 Step 3: Review and Explain Profile Results

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Review Profile Results",
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
Read the contents of output/style_profile.yaml and explain the following:

1. Summary of my writing style characteristics (3-5 lines)
2. Meaning and interpretation of each analysis item's values
3. Article types suited to this writing style (blog/explainer/technical, etc.)
4. Writing style strengths (points that make a positive impression on readers)
5. Improvement hints (suggestions for better readability)

This profile will be used in Lesson 14-3 to generate articles,
so let's thoroughly understand its contents.
```

**Expected result**: Explanations of each style profile item and the writing style's characteristics, strengths, and improvement points are provided.

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
      {"id": "trouble_1", "label": "Too few samples, low analysis accuracy"},
      {"id": "trouble_2", "label": "Style profile values are extreme"},
      {"id": "trouble_3", "label": "Error with style-analyzer"},
      {"id": "trouble_4", "label": "File isn't saved"}
    ]
  }]
}
```


### Issue 1: "Too few samples, low analysis accuracy"
**Cause**: With only 1-2 samples, style tendencies cannot be accurately captured
**Solution prompt**:
```text
To increase sample count, try the following:
- Extract text from past emails, chats, or reports
- Even short texts can reveal basic tendencies with 3 or more samples
- If you can't prepare samples, practice with "demo samples" first,
  then re-analyze with your own samples later
```

### Issue 2: "Style profile values are extreme"
**Cause**: Styles vary greatly between samples (e.g., mixing work and personal writing)
**Solution prompt**:
```text
Check if the sample writing styles are consistent.
We recommend separating by purpose (business/casual) and
creating separate profiles for each:
- output/style_profile_business.yaml
- output/style_profile_casual.yaml
```

### Issue 3: "Error with style-analyzer"
**Cause**: Incorrect file path or unsupported file format
**Solution prompt**:
```text
Please check the following:
1. Is the file path correct? (specify absolute path)
2. Is the file format .md or .txt?
3. Is the file not empty?
4. Is the character encoding UTF-8?
```

### Issue 4: "File isn't saved"
**Cause**: The output directory doesn't exist
**Solution prompt**:
```bash
Check if the output directory exists, and create it if not.
mkdir -p ~/ai-agent-camp/output/samples
```

---

## ✅ Checkpoint
- [ ] Prepared 3 or more writing samples
- [ ] Ran style analysis with style-analyzer
- [ ] Style profile (YAML format) saved to output/
- [ ] Understood the meaning of each profile item

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-2-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-2-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-2-*.md
```

> 💡 View full text: `cat output/article-14-2-*.md` to display the entire file

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
      {"id": "next_window", "label": "Open in new window (/start-14-3)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-3 in a new window
- finish → End
