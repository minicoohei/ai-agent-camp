---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module14-article-writing/chapter.yaml"
category: "lesson"
duration: "~30 min"
prerequisites: ["start-14-5"]
level: "intermediate"
tags: ["article", "factcheck"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 14-6: Fact-Checking - Fact Verification Agent

## 📍 What You'll Do

Welcome to **Lesson 14-6: Fact-Checking - Fact Verification Agent**!

| Item | Details |
|------|---------|
| Goal | Verify factual claims in the article using the fact-checking agent and add citations |
| Duration | ~30 min |
| Skills Used | fact-checker |
| Prerequisites | Gemini API key configured, Lesson 14-5 (proofread draft) complete |
| Course Page | Refer to [Module 14: Article Writing](https://ai-agent.camp/en/course/module-14) in parallel |

**Session flow:**
1. Understand the fact-check target categories
2. Run fact verification with fact-checker
3. Review verification results and add citations to the article

By the end of this session, a fact-verified article with citations will be complete.

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

## 🚀 Step 1: Understand Fact-Check Target Categories

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 1: Understand Fact-Check Categories",
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
Explain the 5 categories verified by the fact-checking agent.

1. Numbers and statistics: Accuracy of values like "X%", "X times", "X billion yen"
2. Dates and timelines: Accuracy of dates like "started in year X", "released in month X"
3. Proper nouns: Spelling and official names of companies, products, and people
4. Causal relationships: Validity of claims like "X caused Y"
5. Citations and references: Verification of sources for claims like "according to X", "a study by X shows"

Explain the specific verification methods and common error patterns for each category.
```

**Expected result**: Details of the 5 verification categories and common error patterns are explained.

---

## 🚀 Step 2: Run Fact Verification with fact-checker

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 2: Run Fact-Check",
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
Use the fact-checker skill to fact-check the proofread article.

Execution command:
python skills/fact-checker/scripts/fact_checker.py --input output/article-14-5-proofread.md --output output/article-14-6-factcheck.json

Target file: output/article-14-5-proofread.md

Verify across all 5 categories:
1. Numbers and statistics
2. Dates and timelines
3. Proper nouns
4. Causal relationships
5. Citations and references

Output the following for each claim:
- Relevant text (with line number)
- Category
- Verification result: Verified / Needs review / Error / Source unknown
- Correct information (if error)
- Recommended source URL (if available)

Save the results to output/article-14-6-factcheck.json.
```

**Expected result**: All factual claims in the article are verified across 5 categories, with results output in JSON format.

---

## 🚀 Step 3: Review Results and Add Citations

In Codex, you typically select from choices in chat: "Continue / Review examples / Skip".

**AskQuestion settings example:**
```json
{
  "title": "🚀 Step 3: Add Citations",
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
Based on the verification results in output/article-14-6-factcheck.json,
apply the following corrections to the article.

1. "Error" claims: Correct with accurate information
2. "Needs review" claims: Change to cautious wording (e.g., "it is said that...")
3. "Source unknown" citations: Add sources or remove the citation
4. "Verified" claims: Add sources as footnotes

Place all citations at the end of the article:
## References
1. [Source title](URL) - Description of referenced section
2. ...

Save the result to output/article-14-6-factchecked.md.
```

**Expected result**: Fact verification corrections are applied and the article with citations is saved.

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
      {"id": "trouble_1", "label": "Most claims flagged as 'Needs review'"},
      {"id": "trouble_2", "label": "Source URLs can't be found"},
      {"id": "trouble_3", "label": "Fact-checking is too strict"},
      {"id": "trouble_4", "label": "Verification results file isn't generated"}
    ]
  }]
}
```


### Issue 1: "Most claims flagged as 'Needs review'"
**Cause**: Many claims in the article lack sources
**Solution prompt**:
```text
Consider the following approaches:
1. Change general facts (widely known information) from "Needs review" to "Verified"
2. Change claims without specific data to cautious expressions like "it is generally considered that..."
3. Add official sources (government, academic papers, official sites) for important claims
```

### Issue 2: "Source URLs can't be found"
**Cause**: Niche information or unpublished primary sources
**Solution prompt**:
```text
When sources can't be found:
1. Change the expression to "in the author's experience" or "generally"
2. Use similar information sources (industry reports, news articles) as alternative citations
3. Remove the claim itself (claims without evidence erode reader trust)
```

### Issue 3: "Fact-checking is too strict"
**Cause**: Applying academic paper-level verification to a blog post
**Solution prompt**:
```text
Adjust verification level according to article type:
- Blog posts: Focus on accuracy of numbers and proper nouns
- Explainer articles: Focus on causal relationships and citation accuracy
- Technical articles: Focus on command, version info, and procedure accuracy
Opinions and advice are excluded from verification.
```

### Issue 4: "Verification results file isn't generated"
**Cause**: Input file not found
**Solution prompt**:
```bash
Check the input file path:
ls output/article-14-5-proofread.md
If the file doesn't exist, complete Lesson 14-5 (/start-14-5) first.
```

---

## ✅ Checkpoint
- [ ] Understood the 5 fact-check categories (numbers/dates/proper nouns/causal relationships/citations)
- [ ] Ran verification across all categories with fact-checker
- [ ] Reviewed verification results and corrected errors
- [ ] Saved the article with citations added to output/

---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/
└── article-14-6-*.md  (article documents)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/article-14-6-*.md

# Check the beginning (first 30 lines)
head -30 output/article-14-6-*.md
```

> 💡 View full text: `cat output/article-14-6-*.md` to display the entire file

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
      {"id": "next_window", "label": "Open in new window (/start-14-7)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**Post-selection instructions (example)**:
- next_auto → /next_lesson
- next_window → Open /start-14-7 in a new window
- finish → End
