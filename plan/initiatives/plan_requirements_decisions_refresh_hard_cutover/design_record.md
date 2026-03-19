# Requirements And Decisions Hard Cutover Refresh Design Record

## Summary
Tracks the hard-cutover refresh that retires legacy planning history, workflow compatibility roots, repo_ops, and domain_packs while aligning the repo to requirements.md and decisions.md.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
