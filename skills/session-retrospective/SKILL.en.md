---
name: session-retrospective
description: "A skill that automatically generates self-improvement Issues at the end of a session. Triggered by requests like 'Create a retrospective Issue', 'Retrospective', 'Create improvement Issues'."
triggers:
  - Create a retrospective Issue
  - Retrospective
  - Create improvement Issues
  - Self-improvement Issue
  - Session retrospective
  - session-retrospective
  - session-retro
version: 1.0.0
author: ai-agent-camp
dependencies: []
---

# Session Retrospective - Session Self-Improvement Issue Generation

## Overview

A skill that reviews problems encountered, inefficiencies, and areas for improvement at the end of a session (conversation), and automatically registers them as GitHub Issues.

## Triggers

Activated by requests such as:
- "Create a retrospective Issue", "Self-improvement Issue"
- "Retrospective", "session-retro"
- "Create improvement Issues"
- As an automatic routine at session end

## Workflow

### Phase 1: Session Review (Automatic Analysis)

Extract improvement points from conversation history in the following categories:

| Category | Label | Detection Pattern |
|----------|-------|-------------------|
| **Auth/Config Issues** | `auth` | Token acquisition failure, API auth errors, environment variable inconsistencies |
| **Path/Convention Gaps** | `convention` | Format variations, naming convention inconsistencies, non-compliant templates |
| **Tool/Script Gaps** | `tooling` | Areas handled with one-off scripts, manual work that should be automated |
| **Documentation Inconsistencies** | `docs` | CLAUDE.md and MEMORY contradictions, outdated entries, duplicate information management |
| **Workflow Inefficiencies** | `workflow` | Areas with excessive trial-and-error, processes that needed fallbacks |
| **Error Handling** | `error` | Unexpected errors, unhelpful error messages, processes that needed retries |

### Phase 2: Issue Draft Generation

Generate an Issue for each improvement point with the following structure:

```markdown
## Background
(What you were doing when the problem occurred)

## Problem
(Specific problem description. Include error messages or commands if available)

## Proposal
(1-3 improvement suggestions, specific and actionable)

## Context
(Which session/task this occurred in)
```

### Phase 3: User Confirmation

Display each Issue candidate via AskUserQuestion and let them choose whether to register:
- "Register all"
- "Select and register" (confirm one by one)
- "Edit and register" (edit content before registering)

### Phase 4: GitHub Issue Registration

```bash
# Get GH_TOKEN (extract from git remote URL)
export GH_TOKEN=$(git remote get-url origin | grep -oP '(?<=https://)[^@]+(?=@)' | sed 's/x-access-token://')

# Register Issue (use --body-file. heredoc causes escape issues with Markdown code blocks)
cat > /tmp/issue_body.md << 'EOF'
Issue body (Markdown)
EOF
gh issue create --repo minicoohei/ai-agent-camp \
  --title "Improvement: <Title>" \
  --body-file /tmp/issue_body.md
```

## Execution Methods

### Method 1: Skill Invocation

```text
Create a retrospective Issue
```

### Method 2: Direct Script Execution (Generate Issues from Template)

```bash
# Bulk register from JSON file
python skills/session-retrospective/scripts/create_issues.py --input issues.json

# Test mode (dry-run, does not actually register)
python skills/session-retrospective/scripts/create_issues.py --input issues.json --dry-run
```

## Issue Quality Guidelines

### Good Issues
- Reproducible, specific problem description
- Includes executed commands and error messages
- 1 Issue = 1 improvement point (clear scope)
- Proposals are implementable and specific

### Bad Issues (should not be created)
- Vague content like "want to make it better"
- Session-specific temporary problems (won't recur)
- Issues caused by user error
- Content duplicating existing Issues

## Analysis Template

Thinking framework for reviewing sessions:

1. **Blockers**: Were there moments when work stopped? → What was the root cause?
2. **Workarounds**: Were there places where you used a workaround instead of the proper method?
3. **Repetition**: Were there places where you did the same work 2+ times?
4. **Documentation lookup**: What questions couldn't be answered by looking at CLAUDE.md or MEMORY?
5. **Manual work**: What manual work could have been automated with scripts or tools?

## Output

- GitHub Issues (minicoohei/ai-agent-camp repository)
- Issue URLs displayed in console as a list
