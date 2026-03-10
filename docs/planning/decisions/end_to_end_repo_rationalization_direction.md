---
trace_id: "trace.end_to_end_repo_review_and_rationalization"
id: "decision.end_to_end_repo_rationalization_direction"
title: "End-to-End Repository Rationalization Direction"
summary: "Records the decision to keep the current planning-family model and coordination start-here path while focusing the final pre-implementation follow-up on trust-surface guardrails, external pack validation, and CLI modularity."
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T19:43:34Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/"
  - "core/control_plane/indexes/coordination/"
  - "core/python/src/watchtower_core/"
aliases:
  - "repo rationalization direction"
  - "planning surface follow-up decision"
---

# End-to-End Repository Rationalization Direction

## Record Metadata
- `Trace ID`: `trace.end_to_end_repo_review_and_rationalization`
- `Decision ID`: `decision.end_to_end_repo_rationalization_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.end_to_end_repo_review_and_rationalization`
- `Linked Designs`: `design.features.end_to_end_repo_rationalization`
- `Linked Implementation Plans`: `design.implementation.end_to_end_repo_rationalization_execution`
- `Updated At`: `2026-03-10T19:43:34Z`

## Summary
This decision records the choice to keep the current planning-family model and coordination start-here path while focusing the final pre-implementation follow-up on trust-surface guardrails, external pack validation, and CLI modularity.

## Decision Statement
Do not introduce another planning artifact family or collapse the authored planning corpus again before product implementation. Keep `query coordination` and `coordination_tracking.md` as the default start-here surfaces, and spend the final pre-implementation follow-up on documentation guardrails, closeout-consistent metadata, external pack validation seams, and smaller query CLI modules.

## Trigger or Source Request
The end-to-end review rechecked documentation, code structure, machine and human entrypoints, the planning task model, README usage, extensibility seams, and future CTF-oriented pack needs before WatchTower implementation begins.

## Current Context and Constraints
- The coordination index and coordination tracker already provide a working machine-first and human-first start-here path.
- README entrypoints are now compact enough that another navigation-only initiative would have low marginal value.
- Future WatchTower work still needs a better external pack validation seam and smaller CLI maintenance units.
- The repo should avoid reopening planning-model churn after several successful hardening initiatives.

## Applied References and Implications
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): keeps the compact coordination tracker as the root human start-here surface.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): keeps the initiative layer as the deeper family-specific coordination view rather than replacing it again.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): preserves the traceability index as the durable machine join beneath the coordination layer.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): external schema support should remain supplemental, not canonicalized into this repo's catalog.

## Affected Surfaces
- `docs/planning/README.md`
- `docs/planning/coordination_tracking.md`
- `core/control_plane/indexes/coordination/coordination_index.v1.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/cli/`

## Options Considered
### Option 1
- Create a new planning-graph artifact family above traceability and coordination.
- Strength: one more obviously singular machine surface.
- Tradeoff: adds more surface area and duplicates working coordination behavior.

### Option 2
- Keep the current planning-family model and coordination start-here path, then focus follow-up work on trust, extensibility, and modularity.
- Strength: addresses the concrete review findings without reopening stable planning boundaries.
- Tradeoff: keeps the family-specific tracking surfaces available instead of removing them.

### Option 3
- Freeze the repo after the review and defer all remaining issues to product implementation.
- Strength: smallest immediate scope.
- Tradeoff: leaves known correctness and extensibility gaps unresolved immediately before implementation begins.

## Chosen Outcome
Adopt option 2. The current planning entrypoint model stays in place for the pre-implementation end state, and the remaining follow-up focuses on guardrails, closeout-consistent metadata, external pack validation seams, and CLI modularity.

## Rationale and Tradeoffs
- The review did not justify another planning-model rewrite.
- The remaining issues are concrete and technical: guardrails, metadata trust, extensibility ergonomics, and module size.
- Keeping the current coordination model avoids adding another artifact family while still leaving room for a later product-era reassessment if WatchTower proves a new need.

## Consequences and Follow-Up Impacts
- Documentation semantics validation should become fail-closed for repo-local links.
- Traceability-derived initiative and coordination surfaces should treat closeout as a timestamped state change.
- External pack validation should become possible through file-system supplemental schema loading and CLI-level artifact validation.
- Query CLI modules should be split further before product-oriented expansion increases their scope.

## Risks, Dependencies, and Assumptions
- The family-specific trackers remain available, which means the repo still has multiple deeper views by design.
- The current follow-up assumes supplemental schema loading is enough for the first external pack validation seam and that supplemental validator overlays can wait.

## References
- [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
- [end_to_end_repo_rationalization.md](/home/j/WatchTowerPlan/docs/planning/design/features/end_to_end_repo_rationalization.md)
- [machine_first_coordination_entry_surface.md](/home/j/WatchTowerPlan/docs/planning/decisions/machine_first_coordination_entry_surface.md)

## Updated At
- `2026-03-10T19:43:34Z`
