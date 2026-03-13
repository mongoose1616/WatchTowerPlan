---
trace_id: trace.typed_query_surface_modularity_hardening
id: decision.typed_query_surface_modularity_hardening_direction
title: Typed Query Surface Modularity Hardening Direction Decision
summary: Records the initial direction decision for Typed Query Surface Modularity
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:56:36Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/models/
- core/python/src/watchtower_core/control_plane/loader.py
- core/python/src/watchtower_core/repo_ops/query/
- core/python/tests/unit/
- core/python/src/watchtower_core/control_plane/README.md
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Typed Query Surface Modularity Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.typed_query_surface_modularity_hardening`
- `Decision ID`: `decision.typed_query_surface_modularity_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.typed_query_surface_modularity_hardening`
- `Linked Designs`: `design.features.typed_query_surface_modularity_hardening`
- `Linked Implementation Plans`: `design.implementation.typed_query_surface_modularity_hardening`
- `Updated At`: `2026-03-13T17:56:36Z`

## Summary
Records the initial direction decision for Typed Query Surface Modularity Hardening.

## Decision Statement
Split the typed planning and documentation retrieval models into domain-focused modules backed by small explicit helpers, split the oversized CLI query regression hotspot into narrower suites with one shared command or JSON helper, and preserve the stable `watchtower_core.control_plane.models` import surface throughout.

## Trigger or Source Request
- Another comprehensive internal refactor review was requested using the March 13, 2026 external audit, with instructions to keep reviewing under one stable theme until repeated confirmation passes found no new actionable issue.
- The discovery pass confirmed that `RF-PY-003` and `RF-TST-001` still reproduce under one retrieval-modularity slice after earlier refactor traces were already closed.

## Current Context and Constraints
- `core/python/src/watchtower_core/control_plane/models/planning.py` still carries seven near-parallel typed index families in one mixed-domain file.
- `core/python/tests/unit/test_cli_query_commands.py` still mixes unrelated command families in one large regression file.
- The repository foundations require explicit, inspectable typed models and deterministic real-command validation, so the refactor cannot trade clarity for generic magic.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the chosen design keeps explicit typed contracts and rejects opaque abstraction.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): the refactor stays local-first, deterministic, and reviewable.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the implementation must keep the Python package layout and runtime-boundary docs aligned.

## Affected Surfaces
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/typed_query_surface_modularity_hardening.md)
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/typed_query_surface_modularity_hardening.md)
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/typed_query_surface_modularity_hardening.md)
- `core/python/src/watchtower_core/control_plane/models/`
- `core/python/src/watchtower_core/control_plane/loader.py`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/tests/unit/`

## Options Considered
### Option 1
- Keep the current large files and add only local helper functions inside them.
- Lowest short-term churn.
- Leaves the confirmed hotspots largely intact and does not materially improve module or test locality.

### Option 2
- Split the models and tests by domain with small explicit shared helpers, while preserving stable re-exports and real-command coverage.
- Addresses both confirmed hotspots at their natural boundaries without changing external behavior.
- Requires careful direct-consumer review and same-change doc alignment.

### Option 3
- Generate most of the typed models through generic registries or metaprogrammed base classes.
- Reduces handwritten repetition aggressively.
- Rejected because it would undermine inspectability and debuggability for governed typed surfaces.

## Chosen Outcome
Accept Option 2. The implementation will split the mixed-domain typed model hotspot into smaller explicit modules, preserve stable public imports, split the CLI query regression hotspot into focused suites with one shared helper, and keep adjacent runtime docs and traced planning surfaces aligned through closeout.

## Rationale and Tradeoffs
- The confirmed maintenance problem is not just repeated lines; it is mixed responsibility inside two hotspots that both sit on the same retrieval boundary.
- Option 2 improves locality without crossing the foundation guardrails against opaque abstraction or coverage reduction.
- The tradeoff is modest import churn and more files, which is acceptable because the public boundary stays stable and validation will cover the direct consumers.

## Consequences and Follow-Up Impacts
- New helper-backed model modules and new focused CLI regression files will be added under `core/python/`.
- Loader, query, sync, validation, and test consumers will be reviewed and updated only where internal implementation paths changed.
- The trace must keep its acceptance contract, evidence ledger, tasks, trackers, and final closeout aligned as the loop progresses.

## Risks, Dependencies, and Assumptions
- Assumes the current public import surface is sufficient and does not need functional expansion.
- Depends on full targeted and full-repo validation to catch any missed consumer drift.
- Risks reopening the loop if confirmation surfaces reveal an adjacent retrieval-path issue not visible in the initial discovery pass.

## References
- March 13, 2026 refactor audit
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/typed_query_surface_modularity_hardening.md)
- [typed_query_surface_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/typed_query_surface_modularity_hardening.md)
