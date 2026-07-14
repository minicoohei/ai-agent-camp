# CLI Mode Reports

Run `make cli-mode-check` from the repository root to regenerate `cli-mode.csv` and `cli-mode.md`.
The scanned command roots depend on the local checkouts available, so report regeneration is intentionally not enforced in CI.
When committing checker or command changes, regenerate the reports locally and include the updated tracked results in the same commit.
