---
trace_id: trace.reference_resolution_reuse_hardening
id: decision.reference_resolution_reuse_hardening_direction
title: Reference Resolution Reuse Hardening Direction Decision
summary: Records the initial direction decision for Reference Resolution Reuse Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T15:09:05Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Reference Resolution Reuse Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.reference_resolution_reuse_hardening`
- `Decision ID`: `decision.reference_resolution_reuse_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.reference_resolution_reuse_hardening`
- `Linked Designs`: `design.features.reference_resolution_reuse_hardening`
- `Linked Implementation Plans`: `design.implementation.reference_resolution_reuse_hardening`
- `Updated At`: `2026-03-12T15:09:05Z`

## Summary
Records the initial direction decision for Reference Resolution Reuse Hardening.

## Decision Statement
Use one explicit command-scoped reference-resolution snapshot for workflow semantics validation and reference-dependent sync orchestration instead of rebuilding the full reference index repeatedly or introducing a persistent cache.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- The review confirmed two repeated-work defects in live code paths: workflow document-semantics validation rebuilt the reference index `30` times for the current repo, and `sync all` rebuilt it `4` times.
- The repo is otherwise green, so the change must remain behavior-preserving and bounded to internal reuse rather than broad architectural churn.
- The reference index already owns the governed mapping from reference docs to canonical upstream URLs, so the solution should reuse that authority rather than create a competing source of truth.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): explicit local seams are preferable to implicit repeated work or hidden long-lived state.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the optimization must keep the full repository baseline green and must be evidenced through explicit validation.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow loading must remain aligned with the governed workflow index contract while internal reuse changes.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/

## Options Considered
### Option 1
- Leave the repeated reference-index rebuilds in place.
- Strength: no code churn.
- Tradeoff: preserves a confirmed scalability defect in the most frequently repeated validation and sync paths.

### Option 2
- Add a persistent loader-level or module-global cache for reference-resolution data.
- Strength: minimal call-site changes after the cache exists.
- Tradeoff: creates stale-state risk across repo mutations and weakens the explicitness of the orchestration layer.

### Option 3
- Reuse one explicit run-local reference-resolution snapshot and inject it only into the validation and sync paths that repeat the work.
- Strength: removes redundant full scans while preserving current authority layers and avoiding cross-command staleness.
- Tradeoff: requires a small amount of orchestration plumbing and regression coverage around reuse behavior.

## Chosen Outcome
Choose Option 3. Build one fresh reference-index document when the active validation or sync slice first needs reference-resolution data, derive `reference_urls_by_path` once, and reuse that data only within the current service or sync run.

## Rationale and Tradeoffs
- The shared run-local snapshot eliminates confirmed repeated work with the smallest behavior-preserving change set.
- It keeps the reference index as the only canonical resolution authority.
- It avoids the stale-state risk of persistent caching while still improving the current scale profile materially.

## Consequences and Follow-Up Impacts
- Validation and sync services now need explicit internal seams for injected reference-resolution data.
- Regression coverage should assert build-count reuse directly so a later refactor cannot silently reintroduce the repeated scans.
- No command docs or machine-readable schemas should need to change because the durable contract stays the same.

## Risks, Dependencies, and Assumptions
- Aggregate sync orchestration must only build shared reference-resolution state for slices that actually need it.
- The approach assumes one command run operates over one stable source snapshot; it is not intended to survive arbitrary in-process repo mutation.

## References
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/reference_resolution_reuse_hardening.md)

## Updated At
- `2026-03-12T15:09:05Z`
