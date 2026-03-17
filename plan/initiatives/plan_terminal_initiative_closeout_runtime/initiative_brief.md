# Plan Terminal Initiative Closeout Runtime

## Summary
Adds the live terminal closeout mutation path for pack-wide and project-scoped initiative packages so closing initiatives can move into completed, superseded, or cancelled and the coordination surfaces can show recent closeouts instead of stuck active work.

## Identity
- `initiative_id`: `initiative.plan_terminal_initiative_closeout_runtime`
- `trace_id`: `trace.plan_terminal_initiative_closeout_runtime`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.plan_terminal_initiative_closeout_runtime.add_terminal_closeout_mutations`: Implement pack-wide and project-scoped terminal closeout state transitions that finalize initiative, evidence, closeout, and promotion shells.
- `task.plan_terminal_initiative_closeout_runtime.expose_terminal_closeout_command_surface`: Add a CLI path and companion docs for closing live plan initiatives without manual JSON edits.
- `task.plan_terminal_initiative_closeout_runtime.validate_terminal_closeout_and_clear_closing_initiatives`: Add tests, rebuild validation, and use the new closeout path to move the current closing initiatives into terminal states.
