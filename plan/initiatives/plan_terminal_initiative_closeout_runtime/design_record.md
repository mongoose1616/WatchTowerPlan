# Plan Terminal Initiative Closeout Runtime Design Record

## Summary
Adds the live terminal closeout mutation path for pack-wide and project-scoped initiative packages so closing initiatives can move into completed, superseded, or cancelled and the coordination surfaces can show recent closeouts instead of stuck active work.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_terminal_initiative_closeout_runtime/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
