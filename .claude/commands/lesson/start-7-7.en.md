---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~40 min"
prerequisites: ["start-7-5", "start-7-1"]
level: "intermediate"
tags: ["skill", "skill-design", "python", "SKILL.md"]
---

# 🎓 Lesson 7-7: SKILL.md-Driven Skill Development

## 📍 What You'll Do

Welcome to **Lesson 7-7: SKILL.md-Driven Skill Development**!

| Item | Details |
|------|------|
| Goal | Create one skill from scratch with SKILL.md as the core |
| Duration | ~40 min |
| Skills used | SKILL.md, Python |
| Prerequisites | Lesson 7-5 completed (structure understanding), Lesson 7-1 recommended (skill design fundamentals) |

**Session flow:**
1. Decide on a skill idea (using AskUserQuestion)
2. Draft SKILL.md (purpose, input/output, usage)
3. Implement a Python script in the scripts/ directory
4. Finalize SKILL.md (comply with Anthropic best practices)
5. Run operation tests

By the end of this session, you will have your own original skill completed and managed as the authoritative version in `skills/`.

> **💡 Hint**: If the AI response stops midway, type "please continue" or "keep going" to resume. Responses may stop midway depending on the tool, but this is not a malfunction.

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
(view_html → Show course page URL https://ai-agent.camp/en/course/module-7)
(different_lesson → Display module list)

---

## 🚀 Step 1: Decide on a Skill Idea

First, let's decide what kind of skill to create. Choose from the categories below or enter your own idea.

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 1: Decide on a Skill Idea",
  "questions": [{
    "id": "skill_idea",
    "prompt": "What kind of skill do you want to create?",
    "options": [
      {"id": "doc_creation", "label": "Document Creation"},
      {"id": "workflow_auto", "label": "Workflow Automation"},
      {"id": "data_processing", "label": "Data Processing"},
      {"id": "custom", "label": "I want to create with my own idea (type it in)"}
    ]
  }]
}
```

**Idea examples for each category:**

### Document Creation
| Skill Name | Overview | Input | Output |
|-----------|---------|-------|--------|
| changelog-generator | Generate CHANGELOG from Git history | Git repository | CHANGELOG.md |
| email-drafter | Generate email text from key points | Notes/memo | Email body |
| invoice-generator | Auto-generate invoices | Customer info + line items | PDF/Markdown |

### Workflow Automation
| Skill Name | Overview | Input | Output |
|-----------|---------|-------|--------|
| file-organizer | Organize and rename files | Directory | Organized tree |
| csv-transformer | CSV format conversion and cleaning | CSV | Transformed CSV |
| git-branch-cleanup | Batch cleanup of unnecessary branches | Git repository | Report |

### Data Processing
| Skill Name | Overview | Input | Output |
|-----------|---------|-------|--------|
| log-analyzer | Log file analysis and summary | Log file | Analysis report |
| json-schema-validator | JSON schema validation | JSON + schema | Validation results |
| text-summarizer | Summarize long text | Text | Summary |

Input (for your own idea):
```
Flesh out your skill idea with the following information:

1. Skill name (English, hyphen-separated): e.g., changelog-generator
2. One-line description: e.g., Auto-generate CHANGELOG from Git history
3. Category: Document Creation / Workflow Automation / Data Processing
4. Input: What does it receive
5. Output: What does it generate
6. Who uses it: Engineer / PM / Designer / Everyone
7. Difference from existing skills: Does it overlap with existing skills in this project

Once the skill name and category are decided, proceed to Step 2.
```

**Expected result**: The skill's name, category, and input/output are clearly defined.

---

## 🚀 Step 2: Draft SKILL.md

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 2: Draft SKILL.md",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (create for your own skill)"},
      {"id": "review", "label": "Just review the example (view sample SKILL.md)"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Create the SKILL.md with the following structure. Based on Progressive Disclosure, keep metadata under 100 words and body under 5,000 words.

Input (example for changelog-generator):
```
Create the following directory and file:

mkdir -p skills/[skill-name]/scripts

Then create skills/[skill-name]/SKILL.md with the following structure:

---
name: [skill-name]
description: "[one-line description]"
version: 1.0.0
author: [your name]
dependencies:
  python: "3.9+"
  packages: ["required packages"]
---

# /[skill-name] - [Skill Display Name]

## Overview
[2-3 sentences explaining the skill's purpose and value]

## Quick Start

### Basic Usage
```bash
python skills/[skill-name]/scripts/main.py --input [input] --output [output]
```

### With Options
```bash
python skills/[skill-name]/scripts/main.py --input [input] --format markdown --verbose
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes | - | Input file/directory |
| --output | No | stdout | Output destination (file path or stdout) |
| --format | No | markdown | Output format (markdown / json / text) |
| --verbose | No | false | Verbose log output |

## Output Example

[Include actual output sample]

## Trigger Phrases

This skill activates on requests like:
- "[Phrase 1]"
- "[Phrase 2]"
- "[Phrase 3]"

## Notes
- [Constraint 1]
- [Constraint 2]
```

**Expected result**: SKILL.md draft is completed and the overall skill design is clear.

---

## 🚀 Step 3: Implement the Python Script

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 3: Implement the Python Script",
  "questions": [{
    "id": "step_action",
    "prompt": "What would you like to do with this step?",
    "options": [
      {"id": "practice", "label": "Proceed (create a script for your skill)"},
      {"id": "review", "label": "Just review the example (view sample script)"},
      {"id": "skip", "label": "Skip"}
    ]
  }]
}
```

**Guidance after selection:**

Implement scripts/main.py following the standard pattern below.

Input:
```
Create skills/[skill-name]/scripts/main.py.

Implement following this pattern:

#!/usr/bin/env python3
"""
[skill-name] - [one-line description]

Usage:
    python main.py --input <input> [--output <output>] [--format <format>]
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="[skill description]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --input data.csv
    python main.py --input data.csv --output report.md --format markdown
        """
    )
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", default=None, help="Output file path (defaults to stdout)")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "text"], default="markdown", help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose log output")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    return parser.parse_args()


def validate_input(input_path: str) -> Path:
    """Verify input file exists"""
    path = Path(input_path)
    if not path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    return path


def process(input_path: Path, output_format: str, verbose: bool) -> str:
    """Main processing (implement skill-specific logic here)"""
    if verbose:
        print(f"Processing: {input_path}", file=sys.stderr)

    # TODO: Implement skill-specific processing here
    result = f"# Processing Result\n\n- Input: {input_path}\n- Format: {output_format}\n- Processed at: {datetime.now().isoformat()}\n"

    return result


def output_result(result: str, output_path: str = None):
    """Output results"""
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(result, encoding="utf-8")
        print(f"Output complete: {output_path}", file=sys.stderr)
    else:
        print(result)


def run_test():
    """Test mode"""
    print("=== Test Mode ===")
    # Verify operation with dummy test input
    test_input = Path("/tmp/test_input.txt")
    test_input.write_text("Test data", encoding="utf-8")

    result = process(test_input, "markdown", verbose=True)
    print(result)
    print("=== Test Complete ===")

    # Cleanup
    test_input.unlink(missing_ok=True)


def main():
    args = parse_args()

    if args.test:
        run_test()
        return

    input_path = validate_input(args.input)
    result = process(input_path, args.format, args.verbose)
    output_result(result, args.output)


if __name__ == "__main__":
    main()

---

Replace the "TODO" section in the template above with your skill-specific processing.
Rewrite the contents of the process() function to match your skill's purpose.
```

**Expected result**: main.py is completed and can be verified with `python main.py --test`.

---

## 🚀 Step 4: Finalize SKILL.md

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 4: Finalize SKILL.md",
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

Reflect what was implemented in Step 3 and finalize the SKILL.md. Check compliance with Anthropic best practices.

Input:
```
Improve the SKILL.md created in Step 2 from the following perspectives:

### Anthropic Best Practices Checklist

1. **Progressive Disclosure**
   - [ ] Is metadata (name + description) under 100 words
   - [ ] Is SKILL.md body under 5,000 words
   - [ ] Is scripts/ configured to load only when needed

2. **Trigger Accuracy**
   - [ ] Are there 5+ phrases that should correctly activate
   - [ ] Are there 3+ phrases that should NOT activate
   - [ ] Is there no trigger collision with existing skills

3. **Input/Output Clarity**
   - [ ] Are input specifications (format, required/optional) documented
   - [ ] Are output samples included
   - [ ] Is error behavior explained

4. **Practicality**
   - [ ] Do quick start command examples work with copy-paste
   - [ ] Is the parameter table complete
   - [ ] Are notes/constraints documented

Update the SKILL.md based on this checklist.
```

**Expected result**: SKILL.md becomes a finalized version compliant with best practices.

---

## 🚀 Step 5: Operation Tests

Use AskQuestion to choose "Proceed / Just review the example / Skip".

**AskQuestion configuration:**
```json
{
  "title": "🚀 Step 5: Operation Tests",
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
Run operation tests on the skill you created:

1. Verify directory structure
   tree skills/[skill-name]/

   Expected structure:
   [skill-name]/
   ├── SKILL.md
   └── scripts/
       └── main.py

2. Run in test mode
   python skills/[skill-name]/scripts/main.py --test

3. Run with real data
   python skills/[skill-name]/scripts/main.py --input [actual file] --verbose

4. Verify error cases
   python skills/[skill-name]/scripts/main.py --input nonexistent_file.txt
   → Is an appropriate error message displayed?

5. Verify output formats
   python skills/[skill-name]/scripts/main.py --input [file] --format json
   python skills/[skill-name]/scripts/main.py --input [file] --format text

If all tests pass, the skill is complete.
```

**Expected result**: Both normal and error cases behave as expected.

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
      {"id": "trouble_1", "label": "Python script doesn't run"},
      {"id": "trouble_2", "label": "I don't know how to write SKILL.md"},
      {"id": "trouble_3", "label": "Skill is not recognized by Claude Code"},
      {"id": "trouble_4", "label": "I can't come up with an idea"}
    ]
  }]
}
```

### Issue 1: Python script doesn't run
**Cause**: Path or dependency package issues
**Solution prompt**:
```
Check the following:
1. Is python3 --version 3.9 or higher
2. Are required packages installed (pip install [package-name])
3. Does the script have execution permissions (chmod +x scripts/main.py)
4. Is the file encoding UTF-8
```

### Issue 2: I don't know how to write SKILL.md
**Cause**: Template is too abstract
**Solution prompt**:
```
The simplest SKILL.md only needs these 3 sections:
1. Metadata (name, description)
2. Quick start (one command example)
3. Parameter table
Write just these 3 first, then add more later.
```

### Issue 3: Skill is not recognized by Claude Code
**Cause**: Directory placement issue
**Solution prompt**:
```
Skills must be placed in skills/[skill-name]/.
Check the following:
1. Is SKILL.md at skills/[skill-name]/SKILL.md
2. Is the filename exactly SKILL.md (case-sensitive)
3. Restart Claude Code and try invoking with /skill-name
```

### Issue 4: I can't come up with an idea
**Cause**: The concept of skills is abstract
**Solution prompt**:
```
Answer these questions:
1. What did you find "tedious" in yesterday's work?
2. What task do you repeat every week?
3. What have you thought "I wish this could be automated"?
That answer is your skill idea.
```

---

## ✅ Checkpoint
- [ ] Skill idea (name, category, input/output) is decided
- [ ] SKILL.md draft is created
- [ ] scripts/main.py is implemented
- [ ] SKILL.md complies with Anthropic best practices
- [ ] Verified operation in test mode (--test)
- [ ] Verified operation with real data
- [ ] Verified error case behavior


---

## 📋 Deliverable Preview

### Expected Output
```
📁 skills/{skill_name}/
├── SKILL.md  (skill definition)
├── scripts/    (execution scripts)
└── tests/      (test files)
```

### Verification Commands
```bash
# Check skill directory structure
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Check the beginning of SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Completion Check
Paste the following into chat to verify completion:

```
# Completion check: Verify the following:
# 1. Does skills/[skill-name]/SKILL.md exist
# 2. Does skills/[skill-name]/scripts/main.py exist
# 3. Does python skills/[skill-name]/scripts/main.py --test succeed
```

**Expected result**: Skill directory structure is correct and tests pass.

---

## 🎉 Next Steps

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
      {"id": "next_window", "label": "Start in new window (/start-7-8)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

**After selection:**
- next_auto → /next_lesson
- next_window → Open new window with /start-7-8
- finish → End
