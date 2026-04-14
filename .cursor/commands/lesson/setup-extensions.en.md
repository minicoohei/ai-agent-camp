---
description: "Lesson command"
duration: "~5 min"
prerequisites: ["Cursor is running"]
level: "beginner"
tags: ["setup", "extensions"]
---

# /setup-extensions -- Automatic Extension Setup

## Step 0: Check Setup Progress

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py show --current setup-extensions` to display progress
2. Check already-installed extensions; if all are present, confirm "Extensions are already installed. Do you want to skip?"

## Purpose of This Command

The AI **automatically checks and installs** Cursor / VS Code extensions.
You don't need to run any terminal commands. The AI handles everything behind the scenes.

| Item | Details |
|------|---------|
| Goal | Automatically install all extensions required for the training |
| Duration | ~5 minutes |
| Prerequisites | Cursor (or VS Code) is running |
| User Action | Just press buttons (no CLI commands needed) |

> **Key point**: All operations in this command are auto-run by the AI. You don't need to type commands in the terminal.

---

## Readiness Check

**AskQuestion configuration:**
```json
{
  "title": "Starting extension setup",
  "questions": [{
    "id": "readiness",
    "prompt": "Are you ready?",
    "options": [
      {"id": "ready", "label": "Let's start"},
      {"id": "what_is_this", "label": "What are extensions? I want an explanation first"},
      {"id": "different_lesson", "label": "I want to go to a different lesson"}
    ]
  }]
}
```

(ready -> Proceed to Step 1)
(what_is_this -> Display the following)

> **What are extensions?**
> They are like "feature packs" you can add to Cursor (the editor).
> For example, installing the "Python extension" enables syntax highlighting and auto-completion for Python code.
> This setup automatically installs the extensions needed for the training.

(different_lesson -> Display module list)

---

## Step 1: Check Current Extensions

**What the AI auto-runs:**

1. The AI runs the following command **behind the scenes** to get the list of installed extensions:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

2. Display the list in an easy-to-read table format for the user:
```text
Currently installed extensions:
| # | Extension ID | Description |
|---|-------------|-------------|
| 1 | ms-python.python | Python |
| 2 | ... | ... |

Total: XX extensions are installed.
```

3. If the command fails (neither `cursor` nor `code` is found):
   - Display "Cursor command-line tool was not found"
   - **For Cursor**: Guide: "Open the Cursor menu > Command Palette (Cmd+Shift+P / Ctrl+Shift+P) > select 'Shell Command: Install 'cursor' command'"
   - **For VS Code**: Guide: "Open the Command Palette > select 'Shell Command: Install 'code' command in PATH'"
   - After resolving, re-run Step 1

**Note: Do not ask the user to type commands. The AI auto-runs everything and only shows results.**

---

## Step 2: Auto-Install Required Extensions

**What the AI auto-runs:**

1. Compare the "required extensions list" below with the Step 1 results and identify missing extensions:

| Extension ID | Purpose |
|-------------|---------|
| `marp-team.marp-vscode` | Create presentations in Markdown (Marp) |
| `hediet.vscode-drawio` | Create and edit diagrams in the editor (Draw.io) |
| `jebbs.plantuml` | Auto-generate UML diagrams from text (PlantUML) |
| `nicepkg.aide-pro` | AI development assistant (AIDE Pro) |
| `ms-python.python` | Python code execution and debugging |
| `ms-python.vscode-pylance` | High-accuracy Python completion and type checking |
| `esbenp.prettier-vscode` | Automatic code formatting (Prettier) |

2. If missing extensions are found, report to the user and install:
```text
The following extensions are not installed. Installing automatically:
- marp-team.marp-vscode (Markdown presentations)
- hediet.vscode-drawio (Diagram editor)

Installing...
```

3. Install each extension with the following command **behind the scenes**:
```bash
cursor --install-extension {extension_ID} 2>/dev/null || code --install-extension {extension_ID}
```

4. If all are already installed:
```text
All required extensions are already installed (7/7).
```

5. Report installation results one by one:
```text
| Extension | Status |
|-----------|--------|
| Marp | Installation complete |
| Draw.io | Installation complete |
| PlantUML | Already installed |
| ... | ... |
```

**Note: The AI auto-runs the install commands. Only results are shown to the user.**

---

## Step 3: Recommended Extensions

**AskQuestion configuration:**
```json
{
  "title": "Install recommended extensions too?",
  "questions": [{
    "id": "optional_install",
    "prompt": "The following extensions are not required but are useful to have. Would you like to install them?\n- Git Graph: Visualize Git history\n- GitLens: Show change history for each line\n- Markdown All in One: Convenient Markdown features bundle",
    "options": [
      {"id": "yes_all", "label": "Install all of them"},
      {"id": "choose", "label": "I want to choose which ones to install"},
      {"id": "skip", "label": "Skip for now"}
    ]
  }]
}
```

(yes_all -> Auto-install all of the following)
(choose -> Let user select individually via AskQuestion)
(skip -> Proceed to Step 4)

**Recommended extensions list:**

| Extension ID | Purpose |
|-------------|---------|
| `mhutchie.git-graph` | Display Git history as a graph (see branch flow at a glance) |
| `eamodio.gitlens` | Show the last author and date of each line |
| `yzhang.markdown-all-in-one` | Convenient Markdown editing features (auto table of contents, shortcuts, etc.) |

**What the AI auto-runs:**
- Install selected extensions with `cursor --install-extension {ID} 2>/dev/null || code --install-extension {ID}`
- Report results in table format

**(For choose) AskQuestion configuration:**
```json
{
  "title": "Select extensions to install",
  "questions": [
    {
      "id": "git_graph",
      "prompt": "Install Git Graph (visualize Git history)?",
      "options": [
        {"id": "yes", "label": "Install"},
        {"id": "no", "label": "Skip"}
      ]
    },
    {
      "id": "gitlens",
      "prompt": "Install GitLens (show per-line change history)?",
      "options": [
        {"id": "yes", "label": "Install"},
        {"id": "no", "label": "Skip"}
      ]
    },
    {
      "id": "markdown",
      "prompt": "Install Markdown All in One (convenient Markdown features)?",
      "options": [
        {"id": "yes", "label": "Install"},
        {"id": "no", "label": "Skip"}
      ]
    }
  ]
}
```

---

## Step 4: Verify Installation Results

**What the AI auto-runs:**

1. Re-run `cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null` **behind the scenes**
2. Cross-check that all required extensions are installed
3. Display the final results in table format:

```text
## Extension Setup Results

### Required Extensions (7)
| Extension | Purpose | Status |
|-----------|---------|--------|
| Marp | Presentation creation | Installed |
| Draw.io | Diagram creation | Installed |
| PlantUML | UML diagram generation | Installed |
| AIDE Pro | AI development assistant | Installed |
| Python | Python development | Installed |
| Pylance | Python completion | Installed |
| Prettier | Code formatting | Installed |

### Recommended Extensions
| Extension | Status |
|-----------|--------|
| Git Graph | Installed / Not installed |
| GitLens | Installed / Not installed |
| Markdown All in One | Installed / Not installed |
```

4. If all are installed: Display "Extension setup is complete"
5. If any extensions failed to install:
   - Display "The following extensions failed to install"
   - Guide with GUI instructions: "Open the extensions panel (Cmd+Shift+X / Ctrl+Shift+X), search for '{extension name}', and install it manually"

---

## Common Troubles and Solutions

**AskQuestion configuration:**
```json
{
  "title": "Any trouble?",
  "questions": [{
    "id": "trouble",
    "prompt": "Are you having any issues?",
    "options": [
      {"id": "trouble_1", "label": "Extension installation is failing"},
      {"id": "trouble_2", "label": "The cursor command is not found"},
      {"id": "trouble_3", "label": "I installed it but it's not working"},
      {"id": "no_trouble", "label": "No problems, move on"}
    ]
  }]
}
```

### Trouble 1: Extension Installation Fails
**Cause**: Network connection issues, or marketplace server outage
**What the AI does**:
1. Check network connection (AI runs behind the scenes):
```bash
# Mac / Linux
ping -c 1 marketplace.visualstudio.com

# Windows
ping -n 1 marketplace.visualstudio.com
```
2. If connection is OK, retry
3. If it still fails -> Guide with GUI instructions:
   "Open the extensions panel (Cmd+Shift+X / Ctrl+Shift+X) and search/install manually"

### Trouble 2: cursor Command Not Found
**Cause**: Cursor's command-line tool is not added to PATH
**What the AI does**:
- Guide: "Open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P), type 'Shell Command: Install', and select the item that appears"
- "Then restart Cursor and re-run this command"

### Trouble 3: Installed But Not Working
**Cause**: Cursor needs to reload
**What the AI does**:
- Guide: "Open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P) and select 'Developer: Reload Window'"

---

## Checkpoint

- [ ] All 7 required extensions are installed
- [ ] Can be confirmed in the extensions panel (Cmd+Shift+X / Ctrl+Shift+X)
- [ ] Syntax highlighting is active when opening a Python file

---

## Next Steps

**AskQuestion configuration:**
```json
{
  "title": "Select next step",
  "questions": [{
    "id": "next_step",
    "prompt": "What would you like to do next?",
    "options": [
      {"id": "security", "label": "Set up security settings (/setup-security)"},
      {"id": "check", "label": "Run a full environment check (/check-setup)"},
      {"id": "lesson", "label": "Start a lesson (/start-0-1)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(security -> Guide to /setup-security)
(check -> Guide to /check-setup)
(lesson -> Guide to /start-0-1)
(finish -> Display "Great work!")

---

## Completion

**What the AI auto-runs:**
1. Run `uv run python tools/setup_progress.py complete setup-extensions` to update progress
2. The updated progress summary is displayed automatically
3. Guide the user to the next step: "Next, set up security settings with `/setup-security`"
