# CLI smoke (PR #60 — /setup-19..25)

Plan-mode invocation against each new setup command via both CLIs. Verdict = PASS / WARN (signal mismatch) / FAIL (executed work or unknown command).

| CLI | Module | command | mode | verdict | rc | sec |
|---|---:|---|---|---|---:|---:|
| claude -p | 19 | `/setup-m365cli` | `deferred` | PASS | 0 | 29.6 |
| cursor-agent --print | 19 | `/setup-m365cli` | `deferred` | PASS | 0 | 24.5 |
| claude -p | 20 | `/setup-freee` | `incompatible` | PASS | 0 | 21.4 |
| cursor-agent --print | 20 | `/setup-freee` | `incompatible` | PASS | 0 | 19.3 |
| claude -p | 21 | `/setup-figma` | `incompatible` | PASS | 0 | 23.5 |
| cursor-agent --print | 21 | `/setup-figma` | `incompatible` | PASS | 0 | 19.0 |
| claude -p | 24 | `/setup-salesforce` | `incompatible` | PASS | 0 | 26.9 |
| cursor-agent --print | 24 | `/setup-salesforce` | `incompatible` | PASS | 0 | 22.6 |
| claude -p | 25 | `/setup-google-ads` | `incompatible` | PASS | 0 | 27.6 |
| cursor-agent --print | 25 | `/setup-google-ads` | `incompatible` | PASS | 0 | 22.5 |

Totals: 10 PASS / 0 WARN / 0 FAIL out of 10 runs.

Per-run transcripts: `reports/cli-smoke/<cli>-<slug>.txt`
