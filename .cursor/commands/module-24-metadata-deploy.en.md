---
description: When the user says /module-24-metadata-deploy - Module 24 - deploy metadata to Sandbox
nonInteractiveMode: incompatible
---
## Start Here (Shortest Path)

When you run **`/module-24-metadata-deploy`** in chat, the deploy instructions are loaded.

# Module 24 - Metadata deploy

The user is working on the **deploy** portion of the course material "Metadata deploy/retrieve."

## Steps

1. Validate with `sf project deploy start -o dev --dry-run`
2. If there are no issues, run `sf project deploy start -o dev`
3. Single class: `--metadata ApexClass:MyController`

## Notes

- During training, use Sandbox (`-o dev`) only
- Deploy to production only when the user explicitly specifies `-o prod`

## References

- Course: `slideId=project-deploy`
