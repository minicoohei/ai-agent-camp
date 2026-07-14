---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Node.js 18 or higher installed", "Familiar with terminal operations"]
level: "beginner"
tags: ["setup", "claude-code", "cli"]
nonInteractiveMode: incompatible
---
# Lesson 0-7: Claude Code Setup

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Install Claude Code, complete authentication and project initialization. Understand how to use slash commands and skills |
| Duration | ~15 min |
| Prerequisites | Node.js 18 or higher installed; familiar with terminal operations |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: If the AI stops responding midway, type "please continue" or "it stopped" to resume.

---

## What Is Claude Code?

Claude Code is Anthropic's official CLI tool. You can call Claude directly from the terminal to edit code, manipulate files, and execute commands using natural language.

Differences from Cursor:
- **Cursor**: Use AI within a GUI editor (chat and inline editing)
- **Claude Code**: Use AI from the terminal (CLI-based, suited for automation)

You can take this curriculum's lessons with either tool.

---

## Step 1: Installation

Install Claude Code globally via npm.

```bash
npm install -g @anthropic-ai/claude-code
```

After installation, verify the version:

```bash
claude --version
```

**AskQuestion settings:**
```json
{
  "title": "Step 1: Installation",
  "questions": [{
    "id": "install_status",
    "prompt": "What is your Claude Code installation status?",
    "options": [
      {"id": "not_installed", "label": "Install now (run the command above)"},
      {"id": "already_installed", "label": "Already installed"},
      {"id": "error", "label": "Got an error during installation"}
    ]
  }]
}
```

(not_installed -> Run `npm install -g @anthropic-ai/claude-code` and verify the result)
(already_installed -> Go to Step 2)
(error -> Check if Node.js is 18+ with `node --version`. Guide to clear npm cache with `npm cache clean --force`)

---

## Step 2: Authentication (OAuth Login)

Claude Code automatically starts the authentication flow on first launch. Running the following command will open your browser:

```bash
claude
```

Log in to your Anthropic account in the browser and complete the authentication.

> **Note**: A Claude Pro / Max / Team / Enterprise plan is required. The free plan is not supported.
>
> **To authenticate with an API key**: Run `source ./.env` first (if `ANTHROPIC_API_KEY` is set in `.env`), then launch `claude`.
>
> **To re-authenticate within a session**: Type `/login` in the Claude Code chat.

**AskQuestion settings:**
```json
{
  "title": "Step 2: Authentication",
  "questions": [{
    "id": "auth_status",
    "prompt": "What is your authentication status?",
    "options": [
      {"id": "run_auth", "label": "Start authentication (run claude)"},
      {"id": "already_authed", "label": "Already authenticated"},
      {"id": "api_key", "label": "I want to authenticate with an API key"},
      {"id": "error", "label": "Got an error during authentication"}
    ]
  }]
}
```

(run_auth -> Run `claude`. The browser opens on first launch and the authentication flow begins)
(already_authed -> Go to Step 3)
(api_key -> Guide to set `ANTHROPIC_API_KEY=sk-ant-...` in `.env`, run `source ./.env`, then launch `claude`)
(error -> Check status with `claude auth status` and guide troubleshooting. Within a session, re-authenticate with `/login`)

---

## Step 3: Project Initialization

Launch `claude` at the root of the ai-agent-camp repository:

```bash
cd /path/to/ai-agent-camp
claude
```

On first launch, Claude Code automatically:

1. Reads `CLAUDE.md` to understand project settings
2. Recognizes commands under `.claude/commands/`
3. Recognizes skills under `skills/`

---

## Step 4: How to Use Slash Commands

In Claude Code, you can invoke lessons and utilities with **`/command-name`**.

### How to Start a Lesson

```text
/start-0-1    -> Environment Setup Verification
/start-0-7    -> This lesson (Claude Code Setup)
/start-1-1    -> Banner Generation Intro
```

### Utility Commands

```text
/check-setup  -> Comprehensive environment check
/overview     -> Project overview
```

> **Tip**: In Cursor, you run commands from Cmd+Shift+P -> Command Palette, but in Claude Code you simply type `/command-name` directly in the chat.

**AskQuestion settings:**
```json
{
  "title": "Step 4: Command Verification",
  "questions": [{
    "id": "command_check",
    "prompt": "Let's try a slash command",
    "options": [
      {"id": "try_check", "label": "Try /check-setup"},
      {"id": "understood", "label": "Understood, move on"},
      {"id": "more_info", "label": "I want to learn more"}
    ]
  }]
}
```

(try_check -> Run the contents of `/check-setup`)
(understood -> Go to Step 5)
(more_info -> Display the file list under `.claude/commands/lesson/` and describe each command)

---

## Step 5: Understanding the Skill System

Claude Code **skills** are specialized modules for executing specific tasks. They are stored under `skills/`.

### Differences Between Skills and Slash Commands

| Feature | Mechanism | Examples |
|---------|-----------|---------|
| **Slash commands** (`/command`) | Execute files in `.claude/commands/` | `/start-0-1`, `/check-setup` |
| **Skills** | Auto-selected by natural language trigger phrases | "Create a banner" -> banner-creator |

> **Important**: Skills cannot be invoked with slash commands like `/skill-name`. Slash commands are exclusively for files in `.claude/commands/`.

### How to Invoke Skills

Skills are **automatically selected when you request a task in natural language**, based on trigger phrases defined in each skill's `SKILL.md`:

```text
"Create a banner"        -> banner-creator is auto-selected
"Analyze data"           -> data-analyst is auto-selected
"Annotate a screenshot"  -> screenshot-annotator is auto-selected
```

> **Tip**: To ensure a specific skill is used, include its trigger phrase (e.g., "banner creation", "data analysis") in your request.

### Check Available Skills

```text
Type "Tell me what skills are available"
```

---

## Step 6: The Role of CLAUDE.md

`CLAUDE.md` is a configuration file placed at the project root. Claude Code reads it first and understands:

- Project rules and conventions
- List of available skills
- How to execute commands
- Security policies

> **Important**: You can customize Claude Code's behavior by editing CLAUDE.md. This is covered in detail in Module 6 (Agent Development).

---

## Recommended Workflow

Recommended steps for progressing through this curriculum with Claude Code:

1. **Review CLAUDE.md**: Understand project rules and skill list
2. **Environment check**: Run `/check-setup` to verify your environment
3. **Start lessons**: Begin lessons with `/start-{module}-{lesson}`
4. **Leverage skills**: Required skills are automatically invoked during lessons

---

## Permission Mode Settings (Recommended: Auto Mode)

Claude Code has permission confirmation modes for tool execution. This curriculum recommends using **Auto Mode**.

### Mode List

| Mode | Launch Method | Behavior |
|------|-------------|----------|
| **Default** | `claude` | Asks for confirmation on every file edit and command execution |
| **Auto-accept edits** | Type `/permissions` in chat -> acceptEdits | File edits are auto-approved; command execution requires confirmation |
| **Auto Mode (Recommended)** | Type `/permissions` in chat -> auto | Auto-approves based on permission rules |
| **Full auto** | `claude --dangerously-skip-permissions` | Executes all operations without confirmation |

### How to Set Up Auto Mode

After launching Claude Code, type the following in the chat:

```text
/permissions
```

Select **auto** from the displayed menu.

> **About risks**: In Auto Mode, operations matching permission rules (file edits, shell command execution, etc.) are executed without confirmation. Unintended file changes or command executions may occur. This curriculum recommends Auto Mode since it is intended for use with a local learning repository, but **use Default mode for production environments or repositories containing sensitive data**.
>
> `--dangerously-skip-permissions` (Full auto) skips all safety confirmations and is usually unnecessary even for learning purposes.

---

## Commands to Run

```text
npm install -g @anthropic-ai/claude-code
claude
/check-setup
```

## Expected Output Example

```text
$ claude --version
2.x.x (Claude Code)

$ claude auth status
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty",
  "email": "your-email@example.com",
  ...
}

$ claude
╭─────────────────────────────────────╮
│ ✻ Welcome to Claude Code!          │
│                                     │
│   /help for available commands      │
╰─────────────────────────────────────╯
```

## Common Troubleshooting
- `npm install` fails -> Verify Node.js is 18+ with `node --version`
- Cannot authenticate -> Verify you have a Pro / Max / Team / Enterprise plan
- Commands not recognized -> Verify you launched `claude` from the repository root. If you added or changed files in `.claude/commands/`, exit Claude Code (`/exit` or Ctrl+C) and restart
- Skills not found -> Verify the `skills/` directory exists

---

## Checkpoint
- [ ] Claude Code is installed (`claude --version` works)
- [ ] OAuth authentication is complete (`claude auth status` shows logged in)
- [ ] Can launch `claude` in the ai-agent-camp repository
- [ ] `/check-setup` runs successfully
- [ ] Understand how to use slash commands
- [ ] Understand the skill system overview
- [ ] Permission mode (Auto Mode) is configured

---

## Next Steps

**AskQuestion settings:**
```json
{
  "title": "Choose Next Step",
  "questions": [{
    "id": "next_step",
    "prompt": "Claude Code setup is complete. What would you like to do next?",
    "options": [
      {"id": "check", "label": "Run environment check (/check-setup)"},
      {"id": "start_lesson", "label": "Start the first lesson (/start-1-1: Banner Generation)"},
      {"id": "overview", "label": "Review the project overview (/overview)"},
      {"id": "finish", "label": "Finish here"}
    ]
  }]
}
```

(check -> Run the contents of /check-setup)
(start_lesson -> Guide to /start-1-1)
(overview -> Guide to /overview)
(finish -> Display "Great work! You can start the first lesson anytime with /start-1-1")

---

## Supplement: Using Claude for Chrome

Using Claude Code requires a Claude Pro / Team / Enterprise plan. This means **you can already use Claude!**

We recommend installing the "Claude for Chrome" extension to boost your browser productivity.

### How to Install
1. Search for "Claude" in the Chrome Web Store
2. Install "Claude" (Anthropic official)
3. Access Claude from the extension icon in the top-right of your browser

### Key Uses
- **Web page summarization**: Summarize long articles and documents
- **Code comprehension**: Explain code on GitHub
- **Translation**: Translate English documents
- **Research**: Technical research and API specification review

### When to Use Claude Code vs. Chrome
| Scenario | Recommended Tool |
|----------|-----------------|
| Edit and run code in terminal | Claude Code |
| Read documents in browser | Claude for Chrome |
| Review and understand API specs | Claude for Chrome |
| File and Git operations | Claude Code |
| Extract info from web pages | Claude for Chrome |
