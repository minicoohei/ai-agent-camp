---
description: When the user says /module-24-soql - Module 24 SOQL - retrieve Account / Opportunity with sf data query
nonInteractiveMode: incompatible
---
## Start Here (Shortest Path)

When you run **`/module-24-soql`** in chat, the SOQL exercise instructions are loaded into context.

# Module 24 - Retrieve data with SOQL

The user is working on the course material "Retrieve data with SOQL." **The agent should run sf commands in the terminal** and summarize the results.

## Prerequisites

- Already logged in to Sandbox (`-o dev` or `target-org=dev`) with `sf org login web`
- Do not query a production Org unless `-o prod` is explicit

## Steps

1. Check connected Orgs with `sf org list`
2. `sf data query -o dev -q "SELECT Id, Name, Industry FROM Account LIMIT 5"`
3. Open opportunities: `IsClosed = false`, `ORDER BY Amount DESC LIMIT 20`
4. Total for opportunities closed last month: `--json` + `SUM(Amount)` (use jq if needed)
5. If `MALFORMED_QUERY` occurs, switch to `-f query.soql`

## References

- Course: `slideId=soql` (e.g., `/en/course/module-24?slideId=soql`)
