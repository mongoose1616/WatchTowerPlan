# Plan Human Surface Policy and Core Root Seeding Design Record

## Summary
Adds the governed human-surface policy contract, the helper that resolves those rules, and the missing core-owned human roots that the requirements call out as absent.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_human_surface_policy_and_core_root_seeding/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Direction
- The policy contract should model human-surface obligations by root pattern, not by one-off path checks buried in code.
- The helper should answer three questions deterministically:
  - which policy entry governs a given root
  - which human-facing files are required, optional, or forbidden there
  - whether the current root contents comply with that policy
- The initial slice should cover the roots explicitly called out in [requirements.md](/home/j/WatchTowerPlan/requirements.md#L626): repository root, `core/`, `core/docs/`, `core/workflows/`, `plan/`, `plan/docs/`, `plan/workflows/`, `plan/initiatives/`, `plan/projects/`, initiative containers, project containers, and machine-only `.wt/` roots.
- Validation should stay fail-closed for forbidden files under machine-only roots and for missing required router files under governed human roots.

## Out Of Scope
- Full template-catalog enforcement for every human-facing surface family.
- Promotion, retention, or documentation-family policy beyond what is necessary to govern human-surface placement in this slice.
- Splitting the canonical workflow backend out of the current repo-root `workflows/` implementation. This slice may add thin router surfaces under `core/workflows/` and `plan/workflows/`, but it does not move the backend yet.
