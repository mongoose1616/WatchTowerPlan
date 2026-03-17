# Plan Terminal Initiative Closeout Runtime Implementation Slice

## Summary
Adds the live terminal closeout mutation path for pack-wide and project-scoped initiative packages so closing initiatives can move into completed, superseded, or cancelled and the coordination surfaces can show recent closeouts instead of stuck active work.

## Initial Work Breakdown
- `task.plan_terminal_initiative_closeout_runtime.add_terminal_closeout_mutations`: Implement pack-wide and project-scoped terminal closeout state transitions that finalize initiative, evidence, closeout, and promotion shells.
- `task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface`: Add a CLI path and companion docs for closing live plan initiatives without manual JSON edits.
- `task.plan_terminal_initiative_closeout_runtime.validate_terminal_closeout_and_clear_closing_initiatives`: Add tests, rebuild validation, and use the new closeout path to move the current closing initiatives into terminal states.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
