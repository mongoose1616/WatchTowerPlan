---
trace_id: "trace.preimplementation_repo_review_and_hardening"
id: "decision.preimplementation_machine_coordination_entrypoint"
title: "Machine Coordination Entrypoint Decision"
summary: "Records the decision to keep the current authored planning families and strengthen the initiative index as the primary machine coordination entrypoint for traced work."
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T17:55:24Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/planning/"
  - "core/control_plane/indexes/initiatives/initiative_index.v1.json"
  - "core/python/src/watchtower_core/repo_ops/query/initiatives.py"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "coordination entrypoint decision"
  - "machine planning start-here decision"
---

# Machine Coordination Entrypoint Decision

## Record Metadata
- `Trace ID`: `trace.preimplementation_repo_review_and_hardening`
- `Decision ID`: `decision.preimplementation_machine_coordination_entrypoint`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.preimplementation_repo_review_and_hardening`
- `Linked Designs`: `design.features.preimplementation_repo_readiness`
- `Linked Implementation Plans`: `design.implementation.preimplementation_repo_hardening_execution`
- `Updated At`: `2026-03-10T17:55:24Z`

## Summary
This decision records the choice to keep the current authored planning families and strengthen the initiative index as the primary machine coordination entrypoint for traced work.

## Decision Statement
Preserve the current authored planning families and use the initiative index, exposed through an explicit coordination query path, as the primary machine start-here surface for traced work instead of creating a new planning artifact family.

## Trigger or Source Request
The repository review identified real coordination friction for agent-first use, but the current initiative index already provides the right derived coordination boundary. The missing piece is explicit primacy and small coordination enrichments, not another authored family.

## Current Context and Constraints
- PRDs, decisions, designs, implementation plans, and tasks are already governed as separate authored families.
- The repository already has a traceability index and a derived initiative index.
- Adding another planning family would increase rather than reduce the number of entrypoints unless it replaced something, which would create migration and authority churn.

## Applied References and Implications
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): the repo already defines the initiative index as the compact machine-readable coordination view, so the right move is to strengthen that surface rather than invent a competing one.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the initiative layer is already the cross-family coordination layer and should stay derived rather than authored.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the traceability index remains the durable artifact join; coordination must project from it rather than replace it.

## Affected Surfaces
- `docs/planning/README.md`
- `docs/planning/initiatives/README.md`
- `docs/standards/data_contracts/initiative_index_standard.md`
- `docs/standards/governance/initiative_tracking_standard.md`
- `core/control_plane/schemas/artifacts/initiative_index.v1.schema.json`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`
- `core/python/src/watchtower_core/repo_ops/query/initiatives.py`
- `core/python/src/watchtower_core/cli/`

## Options Considered
### Option 1
- Collapse all planning families into one authored coordination family.
- Strength: visibly fewer planning directories.
- Tradeoff: destroys useful authority boundaries and increases merge contention on the source-of-truth surfaces.

### Option 2
- Add a brand new coordination artifact family next to the initiative index.
- Strength: could keep existing families untouched.
- Tradeoff: creates yet another entrypoint and duplicates the current coordination concept.

### Option 3
- Keep the current authored families and strengthen the initiative index plus query surface as the explicit machine coordination start-here path.
- Strength: reduces ambiguity without adding another family.
- Tradeoff: requires docs and code updates so contributors stop treating all family indexes as equal start-here candidates.

## Chosen Outcome
Adopt option 3. The current authored families stay intact, and the initiative index becomes the clearly documented primary machine coordination surface for traced work.

## Rationale and Tradeoffs
- This keeps authored planning boundaries stable while still making machine navigation simpler.
- It avoids creating another artifact family that would worsen the same discoverability problem it tries to solve.
- The main tradeoff is that the initiative index needs small enrichments and stronger routing guidance so it behaves like a true start-here surface rather than just one more index.

## Consequences and Follow-Up Impacts
- Coordination guidance should route traced-work navigation through the initiative layer first.
- The initiative index should carry enough active-task summary data that the first coordination pass does not require opening the task index immediately.
- A `query coordination` path should exist so agent workflows do not have to guess that `query initiatives` is the intended coordination entrypoint.

## Risks, Dependencies, and Assumptions
- If the initiative index becomes too denormalized, it could begin competing with task authority.
- The decision assumes traced work remains the main coordination boundary for pre-implementation and product work.
- The repo still needs family-specific indexes for detailed lookup after the coordination start-here step.

## References
- [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- [preimplementation_repo_readiness.md](/home/j/WatchTowerPlan/docs/planning/design/features/preimplementation_repo_readiness.md)
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md)

## Updated At
- `2026-03-10T17:55:24Z`
