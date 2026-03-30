# `plan/workflows/roles`

## Description
`This directory is the authoritative plan-owned workflow-role root. Use it for persona-oriented or role-oriented workflow documents that orchestrate reusable modules for the live plan domain.`

## Notes
- Keep reusable, repeatable procedures under `plan/workflows/modules/`.
- Keep persona- or lens-oriented workflow docs here when plan-local work needs them.
- Future plan-owned workflow roles must include a `Composes Modules` section that explicitly names the reusable workflow modules the role directly orchestrates.
- `plan/workflows/ROUTING_TABLE.md` remains the authority for which workflow documents become active for one routed task.
- The active plan-owned role set is `planning_author.md`, `task_coordinator.md`, and `traceability_steward.md`.
- Keep this root thin: role docs should orchestrate modules and escalation boundaries, not copy the module procedures they reference.
