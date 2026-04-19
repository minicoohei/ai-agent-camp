---
name: tmux-session-manager
description: "Manages Claude Code tmux sessions on Lightsail via SSH. Triggered by requests like 'Check sessions', 'Sync PRs', 'tmux status', etc."
triggers:
  - Check sessions
  - Session list
  - tmux status
  - Check PR progress
  - Send instructions to session
  - tmux-session-manager
  - sync-prs
---
# Tmux Session Manager Skill

A skill for managing Claude Code tmux sessions running on Lightsail via SSH.
Handles session status checks, instruction delivery, and PR synchronization on a per-Issue/PR basis.

## Triggers

Activated by the following keywords:
- "Check sessions", "Session list", "tmux status"
- "PR progress", "Issue work status"
- "Create session", "Sync PRs", "sync-prs"
- "Dashboard", "tmux dashboard"
- "Send instructions to session", "send-keys"

## Script Paths

On remote (Lightsail):
```
REPO=/home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata
CC=$REPO/ops/tmux-manager/cc-session.sh
SYNC=$REPO/ops/tmux-manager/sync-prs.sh
```

## Command Execution

All commands are executed via SSH. The `ssh lightsail` alias is configured in `~/.ssh/config`.

### Display Dashboard

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh dashboard"
```

### List Sessions

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh list"
```

### Check Session Status

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh status PR-45"
```

### Capture Session Output

```bash
# Default 100 lines
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45"

# Specify line count
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45 200"
```

### Create Session

```bash
# For PR
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create PR-45"

# For Issue
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create ISSUE-123"
```

### Send Instructions (send-keys)

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh send PR-45 'Address the review comments on this PR and push'"
```

### Sync All Open PRs

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/sync-prs.sh --cleanup"
```

### Kill Session

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh kill PR-45"
```

## Workflows

### 1. Overall Status Check

When user asks "Check sessions" or "What's the current status?":

1. Display overall overview with `dashboard` command
2. Check individual details with `status` as needed
3. Summarize and report results to user in an easy-to-understand format

### 2. PR Sync + Session Creation

When user says "Sync PRs" or "Create sessions for all PRs":

1. Sync all open PRs with `sync-prs.sh --cleanup`
2. Report results (created count, skipped count, cleanup count)

### 3. Sending Instructions to Specific Session

When user says "Have PR-45 handle the review":

1. Check current state with `status PR-45`
2. If idle, send instructions with `send PR-45 "instruction content"`
3. If working, confirm "Currently working. Would you like to wait for completion?"

### 4. Checking/Summarizing Session Output

When user asks "What's PR-45 doing?":

1. Get latest output with `capture PR-45 100`
2. Summarize the content and report to user

## Notes

- If SSH connection times out, add `-o ConnectTimeout=10`
- Do not send-keys to sessions that are actively working (always check status first)
- Recommend keeping simultaneous sessions to 5 or fewer (Lightsail resource constraints)
- Logs are saved in `ops/tmux-manager/logs/`
