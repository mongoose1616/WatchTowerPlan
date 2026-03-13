---
trace_id: trace.workflow_route_boundary_discoverability_hardening
id: decision.workflow_route_boundary_discoverability_hardening_direction
title: Workflow Route Boundary Discoverability Hardening Direction Decision
summary: Records the initial direction decision for Workflow Route Boundary Discoverability
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T21:17:49Z'
audience: shared
authority: supporting
applies_to:
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- docs/commands/core_python/
---

# Workflow Route Boundary Discoverability Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.workflow_route_boundary_discoverability_hardening`
- `Decision ID`: `decision.workflow_route_boundary_discoverability_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.workflow_route_boundary_discoverability_hardening`
- `Linked Designs`: `design.features.workflow_route_boundary_discoverability_hardening`
- `Linked Implementation Plans`: `design.implementation.workflow_route_boundary_discoverability_hardening`
- `Updated At`: `2026-03-13T21:17:49Z`

## Summary
Records the initial direction decision for Workflow Route Boundary Discoverability Hardening.

## Decision Statement
Accept a bounded workflow-discoverability hardening slice that sharpens deterministic route-preview scoring, improves authored workflow trigger cues, and refreshes companion docs and tests without collapsing the explicit workflow family.

## Trigger or Source Request
- The March 13, 2026 refactor audit left a live `RF-WKF-001` gap after the earlier documentation-review routing fix.
- Discovery for this trace reproduced no-match route previews for realistic reconciliation prompts, weak workflow-query discoverability for adjacent route boundaries, and low-signal validation leakage into a strongly signaled phase-transition prompt.

## Current Context and Constraints
- The repository already has explicit workflow modules and route types for documentation-implementation, governed-artifact, and traceability reconciliation plus task lifecycle and task phase transition.
- The routing standard says route preview should use full prompt context rather than exact keyword matching alone, but the current scorer still depends on exact phrase or exact token coverage.
- The workflow family should remain explicit, route-first, deterministic, and inspectable.

## Applied References and Implications
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route preview must stay advisory and deterministic while using full prompt context rather than exact keyword matching alone.
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md): any routing-surface changes must stay derived from the authored routing table and aligned with route-preview behavior.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow retrieval cues should remain explicit, machine-readable, and aligned with the authored workflow corpus.
- March 13, 2026 refactor audit: recommends clarifying route discrimination criteria and preserving the small explicit workflow family rather than collapsing it.

## Affected Surfaces
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- docs/commands/core_python/

## Options Considered
### Option 1
- Add a few routing-table trigger phrases and leave route preview plus workflow lookup behavior otherwise unchanged.
- Strength: smallest code change and minimal runtime churn.
- Tradeoff: no-match reconciliation prompts and weak workflow-query discoverability would still reproduce, and low-signal secondary route leakage would remain.

### Option 2
- Harden the deterministic scorer, expand authored trigger cues for adjacent workflows, and refresh the derived indexes, docs, and tests together.
- Strength: fixes the real runtime gap while reinforcing the same boundaries through the authored routing and lookup surfaces.
- Tradeoff: requires synchronized updates across code, docs, indexes, and tests.

## Chosen Outcome
Choose Option 2. Implement a bounded deterministic scorer hardening plus authored trigger-cue updates, then refresh the companion workflow lookup docs and derived surfaces in the same change set.

## Rationale and Tradeoffs
- The problem is not that the workflow family is too explicit. It is that the advisory lookup surfaces are not translating realistic requests into the explicit boundaries the repository already authored.
- A scorer-only fix would improve route preview but leave workflow lookup and human guidance underpowered.
- A docs-only or trigger-only fix would not remove the low-signal validation leakage that currently survives because every positive route match is merged.

## Consequences and Follow-Up Impacts
- The route-preview runtime, routing table, workflow metadata registry, derived indexes, command docs, and focused regression coverage will all move together under this trace.
- The workflow family remains explicit and small-filed; only its discoverability and route-boundary signaling are being hardened.

## Risks, Dependencies, and Assumptions
- Assumes lightweight canonical token handling and score-based filtering are enough to fix the current boundary gaps without introducing opaque fuzzy matching.
- Depends on keeping the derived route and workflow indexes refreshed whenever authored routing or workflow metadata changes.

## References
- March 13, 2026 refactor audit
- [workflow_route_boundary_discoverability_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_route_boundary_discoverability_hardening.md)
- [workflow_route_boundary_discoverability_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_route_boundary_discoverability_hardening.md)
