---
description: When the user says /module-24-metadata-retrieve - Module 24 - retrieve Apex / Flow / Layout
nonInteractiveMode: incompatible
---
## Start Here (Shortest Path)

When you run **`/module-24-metadata-retrieve`** in chat, the metadata retrieve instructions are loaded.

# Module 24 - Metadata retrieve

The user is working on the **retrieve** portion of the course material "Metadata deploy/retrieve."

## Steps

1. If it has not been created yet, run `sf project generate --name my-sf-project`
2. Run `sf project retrieve start -o dev --metadata ApexClass --metadata Flow --metadata Layout`
3. Summarize the added files under `force-app/main/default/`
4. Report the main paths with `git status`

## Notes

- If Sandbox UI changes are out of sync, check first with `sf org open -o dev`
- Retrieve from production only when `-o prod` is explicit

## References

- Course: `slideId=project-deploy` (e.g., `/en/course/module-24?slideId=project-deploy`)
