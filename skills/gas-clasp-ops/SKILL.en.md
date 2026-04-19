---
name: gas-clasp-ops
description: "Skill for operating Google Apps Script (GAS) projects via clasp. Triggered by requests like 'deploy GAS,' 'clasp push,' 'test GAS function,' etc. Performs push / deploy / run individually or in batch. Supports multiple project management."
triggers:
  - gas-clasp-ops
  - GASデプロイ
  - clasp push
  - Apps Script
  - GASテスト
  - スクリプト反映
  - clasp
---

# GAS clasp Operations Skill

A skill for batch operations on Google Apps Script projects via the clasp CLI.

## Prerequisites

```bash
# clasp runs via npx (no installation required)
# Log in with your Google account (first time only)
npx -y @google/clasp login
```

## Quick Start

```bash
# Push all projects
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# Push and deploy a specific project
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy --project work/10.X-Calendar-GAS

# Run a function (test)
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction

# Dry-run to check
python skills/gas-clasp-ops/scripts/clasp_ops.py push --dry-run
```

## Commands

| Command | Description |
|---------|-------------|
| `push` | Push local code to GAS |
| `deploy` | Deploy a new version |
| `run` | Run a specified function (`--function` required) |
| `status` | Display deployment list |
| `open` | Open GAS editor in browser |

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project PATH` | Target project (multiple allowed) | All projects |
| `--function NAME` | Function name to run (required for run) | - |
| `--dry-run` | Check only without executing | false |
| `--base-dir PATH` | Search base directory | Workspace root |

## Detection Targets

Automatically detects directories containing `.clasp.json`:

- `work/10.X-Calendar-GAS/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-slides-generator/`
- `work/03.AiTutor/session_workshop/03.gas/samples/clasp-weather-recorder/`

## Examples

### Check project list

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py --list
```

Output example:
```
Detected projects (3):
  - work/03.AiTutor/.../clasp-slides-generator (scriptId: 1uIfFp1vuV...)
  - work/03.AiTutor/.../clasp-weather-recorder (scriptId: 1O6SBnHgY-...)
  - work/10.X-Calendar-GAS (scriptId: 1qLnnrFfzX...)
```

### Push and deploy all projects

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py push deploy
```

### Run a function on a specific project (test)

```bash
python skills/gas-clasp-ops/scripts/clasp_ops.py run \
  --project work/10.X-Calendar-GAS \
  --function processUnreadTweets
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Not logged in` | clasp not logged in | Run `npx -y @google/clasp login` |
| `Script API disabled` | GAS API disabled | Enable at [GAS API](https://script.google.com/home/usersettings) |
| `Permission denied` | Insufficient OAuth scope | Add required scopes to `appsscript.json` |
| `Function not found` | Invalid function name | Check function name in GAS editor |

## Notes

- `clasp run` requires the GAS API to be enabled and OAuth scope configuration
- Always `push` code before deploying
- On error, logs are output per target, and processing continues
- Timeout is set to 120 seconds (for long-running processes, recommend running from the GAS editor)

## Overview

A skill for batch operations on Google Apps Script (GAS) projects via the clasp CLI. Automatically detects projects containing `.clasp.json` and efficiently executes push, deploy, and run operations.

## Success Criteria

- [ ] push/deploy to target projects completed without errors
- [ ] When `--function` is specified, the function executed successfully
- [ ] For batch multi-project operations, results are logged for all projects

## Usage

See the "Quick Start" section above. Basic examples:

```bash
# Push all projects
python skills/gas-clasp-ops/scripts/clasp_ops.py push

# Run a function on a specific project
python skills/gas-clasp-ops/scripts/clasp_ops.py run --project work/10.X-Calendar-GAS --function myFunction
```
