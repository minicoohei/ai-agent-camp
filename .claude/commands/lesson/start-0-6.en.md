---
description: "Lesson command"
chapter: "courses/aiagent/lesson02-setup/ch01-environment"
duration: "~15 min"
prerequisites: ["Node.js 18 or higher is installed", "OpenAI API key obtained"]
level: "beginner"
tags: ["setup", "codex", "cli"]
---

# Lesson 0-6: Codex CLI Setup

## Check Setup Progress

**Auto-run by AI:** Run `uv run python tools/setup_progress.py show` to display the current setup progress.

---

## What You'll Do

| Item | Details |
|------|---------|
| Goal | Install and authenticate Codex CLI so you can run lessons in ai-agent-camp |
| Duration | ~15 min |
| Prerequisites | Node.js 18 or higher; OpenAI API key obtained |
| Course Page | Refer to [Course Materials Top](https://ai-agent.camp/en/course/module-0) in parallel |

> **Hint**: This lesson is for Codex CLI users. Cursor users should start from Lesson 0-1.

---

## Step 1: Install Codex CLI

Install Codex CLI via npm. Run the following in your terminal:

**Recommended: Run directly with npx (no installation required)**

```bash
npx @openai/codex --version
```

Using npx lets you run the latest version without a global install.

**Alternative: Global install**

If you use nvm or fnm, sudo is not required:

```bash
npm install -g @openai/codex
codex --version
```

> **Note**: Node.js 18 or higher is required. Check with `node --version`.
> If you get a permissions error, refer to the [npm official guide](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) to change the prefix. `sudo npm install -g` is not recommended.

---

## Step 2: Authentication (OpenAI API Key)

Codex CLI authenticates with an OpenAI API key. Configure it using one of the following methods:

### Method A: Use credential_manager (Recommended)

Use `tools/credential_manager.py` to manage API keys securely:

```bash
uv run python tools/credential_manager.py store OPENAI_API_KEY
```

Follow the prompt to enter your key. It will be saved in an encrypted key store.

### Method B: Set as environment variable

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Add it to `.bashrc` or `.zshrc` to persist across sessions.

### Method C: Set in .env file (fallback)

Only if the above methods are unavailable, add the following to the `.env` in the ai-agent-camp repository:

```dotenv
OPENAI_API_KEY=your-api-key-here
```

> **Security warning**: The `.env` file contains sensitive information. **Never commit it to Git.** Always verify that `.env` is included in `.gitignore`. Accidental commits risk API key leakage.

---

## Step 3: Runtime Settings

Recommended settings for Codex CLI:

Codex CLI's approval mode is specified with `-a` (`--ask-for-approval`):

| Approval Mode | Description |
|--------------|-------------|
| `on-request` | The model automatically determines when to request user approval (recommended for learning) |
| `never` | Auto-execute without confirmation (advanced users only, not recommended) |

Example startup command:

```bash
codex -a on-request
```

> **Important**: Codex manages the sandbox automatically. Follow the recommended settings in `AGENTS.md` for detailed configuration. Do not use `never` mode during normal learning. See `docs/codex-safety.md` for details.

---

## Step 4: How to Run Lessons in Codex

In Cursor, you start lessons with slash commands like `/start-0-1`, but in Codex CLI you use **skills** instead.

### Slash Command to Skill Mapping

| Cursor Command | Codex Method |
|----------------|-------------|
| `/overview` | Use the `aiagent-guide` skill |
| `/check-setup` | Use the `aiagent-check-setup` skill |
| `/start-0-1` | Use the `aiagent-lesson-runner` skill with `start-0-1` |
| `/setup-security` | Use the `aiagent-tooling-setup` skill |

### How to Use

Launch Codex CLI and make a request like:

```text
Use the aiagent-lesson-runner skill to start the start-0-1 lesson
```

Or:

```text
I want to start the start-0-1 lesson
```

Codex automatically recognizes `AGENTS.md` and the `skills/` directory and uses the appropriate skill.

---

## Step 5: Verify Operation

Follow these steps to confirm Codex CLI is working correctly:

1. **Launch Codex in the ai-agent-camp directory**:
   ```bash
   cd /path/to/ai-agent-camp
   codex
   ```

2. **Verify the repository's hook configuration**:
   ```text
   Please run bash scripts/install_hooks.sh
   ```

3. **Run the setup check skill**:
   ```text
   Use the aiagent-check-setup skill to verify the environment
   ```

---

## Expected Output Example

```text
Environment Check Report
| Item        | Status | Details          |
|------------|--------|-----------------|
| Node.js    | OK     | 22.x            |
| Codex CLI  | OK     | 1.x.x           |
| OpenAI API | OK     | Authenticated   |
| Git        | OK     | 2.x             |
| Hooks      | OK     | pre-commit configured |
```

## Common Troubleshooting

- `codex: command not found` -> Run directly with `npx @openai/codex` or re-run `npm install -g @openai/codex`
- API authentication error -> Verify `OPENAI_API_KEY` is correctly configured
- Permission error -> Use nvm/fnm or [change the npm prefix](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally)
- Skill not found -> Verify you launched Codex from the ai-agent-camp root directory

---

## Checkpoint
- [ ] Codex CLI is installed (`codex --version` works)
- [ ] OpenAI API key is configured
- [ ] Approval mode is set to `on-request` (see recommended settings in AGENTS.md)
- [ ] Hooks are configured with `bash scripts/install_hooks.sh`
- [ ] The `aiagent-check-setup` skill runs successfully

---

## Next Steps

Once Codex CLI setup is complete, you can start lessons.

**Recommended flow for Codex users:**

1. Setup verification: Run `start-0-1` (Environment Setup Verification) with the `aiagent-lesson-runner` skill
2. Start lessons: Begin `start-1-1` (Module 1 Banner Generation Intro) with the `aiagent-lesson-runner` skill
3. Execute each lesson's slash commands via skills
4. If stuck, use the `aiagent-guide` skill to see the overall picture

> **Note**: Lesson files in `.cursor/commands/lesson/` can also be used as reference materials in Codex. However, they cannot be executed directly as slash commands.
