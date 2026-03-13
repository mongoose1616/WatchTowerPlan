---
trace_id: trace.validation_test_hotspot_rebalancing
id: decision.validation_test_hotspot_rebalancing_direction
title: Validation Test Hotspot Rebalancing Direction Decision
summary: Records the initial direction decision for Validation Test Hotspot Rebalancing.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T18:46:53Z'
audience: shared
authority: supporting
applies_to:
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/cli/validation_handlers.py
- docs/commands/core_python/
- docs/planning/
---

# Validation Test Hotspot Rebalancing Direction Decision

## Record Metadata
- `Trace ID`: `trace.validation_test_hotspot_rebalancing`
- `Decision ID`: `decision.validation_test_hotspot_rebalancing_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.validation_test_hotspot_rebalancing`
- `Linked Designs`: `design.features.validation_test_hotspot_rebalancing`
- `Linked Implementation Plans`: `design.implementation.validation_test_hotspot_rebalancing`
- `Updated At`: `2026-03-13T18:46:53Z`

## Summary
Records the initial direction decision for Validation Test Hotspot Rebalancing.

## Decision Statement
Split the remaining governed validation hotspots into focused family-oriented suites with small explicit helper modules, keep the historical hotspot filenames as compatibility markers, and refresh README-driven repository-path discoverability in the same trace.

## Trigger or Source Request
- Another comprehensive internal refactor review was requested using the March 13, 2026 refactor audit, with instructions to keep reviewing under one stable theme until repeated confirmation passes found no new actionable issue.
- The discovery pass confirmed that the remaining live portion of `RF-TST-001` now sits in the oversized integration and document-semantics suites plus their README-backed path-discoverability gap.

## Current Context and Constraints
- `test_control_plane_artifacts.py` and `test_document_semantics_validation.py` remain the two largest remaining governed validation hotspots after the earlier CLI-query split.
- Those file paths are referenced broadly across planning artifacts, so deleting them outright would create avoidable path drift.
- The repository-path index is README-derived, and both hotspot files are currently omitted from the relevant README inventories, so `query paths` cannot discover them today.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keeps the split explicit, inspectable, and local-first rather than relying on generic test generation.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): requires preserving deterministic repository-aware validation instead of substituting shallow mocks.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): means README inventory changes are part of the authoritative discoverability contract, not optional documentation cleanup.

## Affected Surfaces
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/integration/README.md
- core/python/tests/unit/README.md
- core/control_plane/indexes/repository_paths/repository_path_index.v1.json
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/repo_ops/validation/all.py
- core/python/src/watchtower_core/cli/validation_handlers.py
- docs/commands/core_python/watchtower_core_validate.md
- docs/planning/

## Options Considered
### Option 1
- Keep the current large files and add only a few local helpers inside them.
- Lowest immediate churn.
- Leaves the hotspot boundaries largely intact and does not solve the README-driven discoverability gap.

### Option 2
- Split the real tests by validation family, add small helper modules, preserve the historical filenames as compatibility markers, and refresh README inventories so repository-path indexing stays aligned.
- Improves failure locality while preserving path stability and repository-aware coverage.
- Requires careful same-change updates across README inventories, indexes, and planning surfaces.

### Option 3
- Replace much of the current explicit coverage with broader generators or fixture factories.
- Reduces repetition aggressively.
- Rejected because it would undermine inspectability and make governed validation failures harder to debug.

## Chosen Outcome
Accept Option 2. The implementation will split both remaining validation hotspots into focused suites with small explicit helpers, retain the old file paths as compatibility markers, refresh README inventory and repository-path discoverability, and keep runtime validation behavior unchanged unless the review loop proves a direct same-theme defect.

## Rationale and Tradeoffs
- The confirmed maintenance cost is mixed responsibility inside two oversized suite files, not a lack of helper abstractions alone.
- Option 2 improves locality without weakening live repository-aware validation or creating historical path drift.
- The tradeoff is a larger file count, but that is acceptable because the new files map cleanly to validation families and the old filenames remain available for trace continuity.

## Consequences and Follow-Up Impacts
- New helper-backed test modules will be added under `core/python/tests/integration/` and `core/python/tests/unit/`.
- The unit and integration READMEs will need to enumerate the new suites so repository-path indexing and query-path lookup stay accurate.
- Acceptance, evidence, tasks, trackers, and final closeout metadata must stay aligned with the final suite layout.

## Risks, Dependencies, and Assumptions
- Assumes the current validation runtime code is already functionally correct and only needs adjacency review, not behavior changes.
- Depends on targeted and full validation to prove the split did not silently reduce coverage.
- Risks reopening the loop if post-fix review finds a validation-family edge case that only becomes visible after the suites are separated.

## References
- March 13, 2026 refactor audit
- [validation_test_hotspot_rebalancing.md](/home/j/WatchTowerPlan/docs/planning/prds/validation_test_hotspot_rebalancing.md)
