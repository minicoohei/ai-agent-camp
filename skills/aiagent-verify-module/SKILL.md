---
name: aiagent-verify-module
description: Verify module completion with AI evaluation. Use when the user wants to check if a module (e.g. module 1) was completed successfully after finishing lessons.
version: 1.0.0
author: AI Brain Partners
dependencies: []
---

# AI Agent Verify Module

Use this skill to verify whether a learner has successfully completed all lessons in a given module.

## Inputs
- A module number (e.g. `1` for Module 1: Banner/Image Generation)

## Workflow
1. Run the verification script to collect factual data:
   ```bash
   uv run python tools/verify_module.py --module <N> --json
   ```
2. Parse the JSON output to understand:
   - Which lessons exist in the module
   - Which output files were expected and whether they exist/are valid
   - What checkpoints each lesson defines
3. For each lesson with existing output files, **read the files** to evaluate quality.
4. For subjective checkpoints (e.g. "understood X"), ask the user for confirmation.
5. Produce a structured evaluation report:
   - **Grade**:
     - A: 全レッスン完了 + 出力ファイルが正しい形式 + 追加の工夫あり
     - B: 全レッスン完了 + 出力ファイルが正しい形式
     - C: 一部レッスン未完了だが主要タスクは完了
     - D: 主要タスクが未完了
   - **Per-lesson details**: output status, checkpoint achievement
   - **Feedback**: specific remediation steps for missing items
   - **Next steps**: which lessons to redo or which module to proceed to

## Required References
- `.cursor/commands/lesson/start-*.md` — lesson definitions with checkpoints and output paths
- `tools/verify_module.py` — factual verification script
- `tools/lesson_progress.py` — progress tracking utilities

## Safety
- This skill is read-only. It does not modify any files or progress state.
- Never pretend the user can run Cursor slash commands directly in Codex.

## Expected Output
- Module completion summary table
- Per-lesson breakdown with output status
- Overall grade (A/B/C/D)
- Actionable feedback and next steps
