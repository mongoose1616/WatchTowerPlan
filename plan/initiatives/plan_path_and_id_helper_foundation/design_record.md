# Plan Path And ID Helper Foundation Design Record

## Summary
Adds reusable path and id helpers so plan initiative, project, task, and companion artifact naming stops living in scattered repo-local string conventions.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_path_and_id_helper_foundation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Planned Runtime Shape
- Add one reusable-core helper under `watchtower_core.control_plane` for canonical slug normalization, trace-stem derivation, plan initiative roots, project roots, and the standard dot-id forms used by live plan artifacts.
- Keep the helper deterministic and fail closed on empty or non-canonical identifiers instead of letting repo-local callers infer names from ad hoc string concatenation.
- Refactor the live `plan/**` runtime surfaces that currently hand-roll canonical naming so one helper governs initiative, project, task, deferred-item, evidence, closeout, and promotion identifiers.
- Preserve the current governed path layout under `plan/initiatives/**`, `plan/projects/**`, and initiative-local `.wt/**`; this slice centralizes derivation rather than changing the workspace model.
