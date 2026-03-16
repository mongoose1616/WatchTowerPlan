---
trace_id: trace.transition_surface_retirement
id: design.implementation.transition_surface_retirement
title: Transition Surface Retirement Implementation Plan
summary: Breaks Transition Surface Retirement into a bounded implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T19:23:51Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/
---

# Transition Surface Retirement Implementation Plan

## Record Metadata
- `Trace ID`: `trace.transition_surface_retirement`
- `Plan ID`: `design.implementation.transition_surface_retirement`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.transition_surface_retirement`
- `Linked Decisions`: `decision.transition_surface_retirement_direction`
- `Source Designs`: `design.features.transition_surface_retirement`
- `Linked Acceptance Contracts`: `contract.acceptance.transition_surface_retirement`
- `Updated At`: `2026-03-16T19:23:51Z`

## Summary
Breaks Transition Surface Retirement into a bounded implementation slice.

## Source Request or Design
- design.features.transition_surface_retirement

## Scope Summary
- Covers the live retirement of obsolete runtime facades, the retired typed-model bridge, the old hotspot marker tests, stale current path references, and temporary audit helpers in the same bounded slice.
- Covers the source docs and governed artifacts needed so sync can rebuild current trackers, planning indexes, and repository-path discovery without pointing at retired files.
- Excludes redesign of current boundary roots or unrelated closed traces beyond the minimum rewrites needed to stop live discovery drift.

## Assumptions and Constraints
- The direct runtime owners and focused replacement test suites already exist and are the intended canonical surfaces.
- The product is unreleased, so hard breaks to retired local import or test paths are acceptable and preferable to another compatibility layer.
- Closeout is blocked until all temporary execution aids are removed from the live tree and the full validation stack stays green.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): code, tests, and docs must stay aligned within the canonical workspace.
- [rewrite_surface_classification_standard.md](/docs/standards/governance/rewrite_surface_classification_standard.md): proven transition surfaces should be deleted rather than retained as ambiguous support layers.
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md): current governed discovery surfaces should point at live canonical paths only.

## Proposed Technical Approach
- Delete the obsolete runtime and test files and move any remaining direct assertions to the current owners and focused suites.
- Rename the boundary-proof test to current semantics, refresh README inventories, and replace current governed references to retired paths with live directories or live files.
- Regenerate planning and repository-path outputs from the cleaned source set and use full validation to catch any hidden stale dependency.

## Work Breakdown
1. Retire the runtime facades, the retired model bridge, and the old hotspot marker tests; repair direct imports, direct tests, and current runtime docs.
2. Rename or rewrite remaining stale boundary-proof and planning surfaces so the active corpus no longer contains scaffold placeholders or current references to retired paths.
3. Run retired-path audits, `sync all`, acceptance validation, `validate all`, `pytest`, `mypy`, and `ruff`; only then transition tasks and close the initiative.

## Risks
- Source cleanup that is too narrow will let sync reintroduce stale deleted paths into derived indexes.
- Source cleanup that is too broad can blur historical narrative, so active initiative surfaces must be reviewed after the bulk path pass.

## Validation Plan
- Run scoped audits to confirm the retired runtime and test paths are absent from current source surfaces.
- Run `./.venv/bin/watchtower-core sync all --write --format json`.
- Run `./.venv/bin/watchtower-core validate acceptance --trace-id trace.transition_surface_retirement --format json`.
- Run `./.venv/bin/watchtower-core validate all --format json`.
- Run `./.venv/bin/pytest -q`.
- Run `./.venv/bin/mypy src`.
- Run `./.venv/bin/ruff check .`.

## References
- [transition_surface_retirement.md](/docs/planning/prds/transition_surface_retirement.md)
- [transition_surface_retirement.md](/docs/planning/design/features/transition_surface_retirement.md)
- [transition_surface_retirement_direction.md](/docs/planning/decisions/transition_surface_retirement_direction.md)
