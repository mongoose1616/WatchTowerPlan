---
trace_id: trace.refactor_review_and_hardening
id: design.features.refactor_review_and_hardening
title: Refactor Review and Hardening Feature Design
summary: Defines the phase-one refactor design for workflow route discrimination,
  compact coordination payloads, and route-first planning and command entrypoints.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T14:13:18Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/references/
- docs/standards/
- workflows/
---

# Refactor Review and Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.refactor_review_and_hardening`
- `Design ID`: `design.features.refactor_review_and_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.refactor_review_and_hardening`
- `Linked Decisions`: `decision.refactor_review_and_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.refactor_review_and_hardening`
- `Updated At`: `2026-03-13T14:13:18Z`

## Summary
Defines the phase-one refactor design for workflow route discrimination, compact coordination payloads, and route-first planning and command entrypoints.

## Source Request
- Perform a comprehensive internal refactor review, fix validated issues end to end, and continue the review loop until repeated confirmation passes find no new actionable issue in scope.

## Scope and Feature Boundary
- Covers the phase-one refactor slice from the audit: workflow-route discrimination, coordination current-state compaction, planning entrypoint clarification, and command umbrella-page thinning.
- Covers the current dirty workflow-routing worktree so it is either completed and validated under traced planning control or replaced deliberately in the same initiative.
- Covers the machine-readable and human-readable companion surfaces that operationalize the selected route and current-state behavior: routing docs, workflow metadata, route and workflow indexes, coordination sync and query paths, planning entrypoints, command pages, standards, and regression tests.
- Excludes deeper repo-local hotspot decomposition for planning scaffolds, task lifecycle, or planning/documentation models.
- Excludes reference-lifecycle grouping, placeholder control-plane-family cleanup, and policy-cost review unless one becomes a direct blocker for the phase-one slice.

## Current-State Context
- The audit confirmed that the workflow family is intentionally modular, but adjacent routes such as documentation review, documentation refresh, repository review, and reconciliation remain subtle enough that route-preview metadata has to work hard to keep them distinct.
- The current local worktree already contains an interrupted route-discrimination slice that adds a dedicated documentation-review route and companion workflow metadata, but that slice is not yet traced, fully reviewed, or committed.
- The coordination-index standard already says the coordination layer should stay compact and current-state focused, but the live sync path still serializes full closed-history initiative entries into the default coordination payload.
- The planning start-here docs and the root or group command pages still carry more route and example repetition than a route-first entrypoint needs, especially during closed-history-heavy repository states.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should remove duplicated start-here and routing burden at the projection boundary rather than by weakening explicit governed families.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human guidance, machine-readable lookup surfaces, and verification surfaces must change together when routing or current-state behavior changes.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the slice stays inside repository-maintenance refactor work and does not grow into broader product or policy redesign.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): route discrimination must stay explicit and minimal-context rather than collapsing narrow workflows into broad generic procedures.
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md): route-preview behavior must stay aligned with the authored routing table and machine-readable route index.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow retrieval metadata should help tooling distinguish adjacent routes without duplicating full workflow prose.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): the coordination surface is a compact current-state start-here projection, not a second deep historical planning join.
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): the human coordination tracker should mirror the compact machine current-state view rather than regrow full tracker-family detail.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): umbrella command pages should remain command references, not broad handbook-style catalogs that duplicate CLI help and leaf pages.

## Design Goals and Constraints
- Reduce high-leverage navigation and projection duplication without weakening governed artifact boundaries.
- Keep workflow modules narrow and distinct; clarify route discrimination before considering any later route consolidation.
- Preserve explicit closed-history lookup through the right deeper surface while shrinking default coordination payloads back to current-state use.
- Preserve leaf command docs, command indexes, deeper planning trackers, and initiative-family surfaces as valid deeper routes.

## Options Considered
### Option 1
- Treat the audit as a broad one-trace mandate and start deep hotspot or policy refactors in the same slice.
- Strength: attacks more findings immediately.
- Tradeoff: creates an uncloseable mega-trace and mixes safe current-state simplifications with higher-risk decomposition and policy decisions.

### Option 2
- Execute the audit's phase-one slice: sharpen workflow-route discrimination first, then slim coordination default payloads and route-first entrypoints while preserving deeper surfaces.
- Strength: fixes the highest-leverage current-state duplication with bounded same-change updates across docs, code, indexes, and tests.
- Tradeoff: deeper hotspot, reference, placeholder-family, and policy findings remain explicit follow-up work.

### Option 3
- Collapse near-neighbor workflow routes or remove deeper planning and command surfaces to reduce file and route count quickly.
- Strength: biggest immediate reduction in visible surface count.
- Tradeoff: blurs intentional authority boundaries, weakens route-first discoverability, and violates the audit's non-recommended refactor guardrails.

## Recommended Design
### Architecture
- Publish a dedicated documentation-review route and matching workflow metadata so documentation audits resolve through an explicit route instead of broad repository-review language.
- Keep `coordination_index` as the machine current-state start-here surface by storing only active initiative entries plus compact recent-closeout summaries in its default artifact payload.
- Preserve explicit closed-history coordination lookups by resolving terminal-status filters through initiative-family data instead of carrying duplicate full historical entries in the default coordination snapshot.
- Recast planning and command umbrella docs as route-first entrypoints that point readers at coordination, CLI help, indexes, and leaf pages instead of re-enumerating the full catalog inline.

### Data and Interface Impacts
- `workflows/ROUTING_TABLE.md`, `workflows/modules/*.md`, `core/control_plane/indexes/routes/route_index.v1.json`, `core/control_plane/indexes/workflows/workflow_index.v1.json`, and `core/control_plane/registries/workflows/workflow_metadata_registry.v1.json` change together for the route-discrimination slice.
- `core/python/src/watchtower_core/repo_ops/sync/coordination_index.py`, `core/python/src/watchtower_core/repo_ops/query/coordination.py`, `core/python/src/watchtower_core/cli/query_coordination_handlers.py`, coordination standards, coordination examples, and coordination-related tests change together for the compact-current-state slice.
- `docs/planning/README.md`, `docs/planning/initiatives/README.md`, `docs/commands/core_python/watchtower_core.md`, `docs/commands/core_python/watchtower_core_query.md`, and `docs/commands/core_python/watchtower_core_sync.md` change together for the route-first entrypoint slice.

### Execution Flow
1. Build and publish the coverage map plus findings ledger for the phase-one refactor slice using the audit and current repo state.
2. Complete the interrupted workflow-route discrimination change and align the routing table, workflow metadata, route preview docs, and targeted regressions.
3. Slim the coordination default payload, update the query path that serves explicit terminal-status coordination lookups, and keep coordination docs and standards aligned.
4. Thin planning and command umbrella docs so they route to the compact current-state and deeper leaf surfaces without duplicating large example catalogs.
5. Run targeted validation, full validation, post-fix review, second-angle review, and adversarial confirmation; if a new actionable issue appears inside this slice, add it to the findings ledger and repeat.

### Invariants and Failure Cases
- Workflow-route clarification must not collapse intentionally distinct workflow modules into generic catch-all procedures.
- Coordination compaction must not strand explicit closed-history lookup behavior behind missing or stale query paths.
- Route-first command and planning docs must not remove the deeper surfaces they point to or drift from the live command and query behavior.

## Affected Surfaces
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/references/
- docs/standards/
- workflows/

## Design Guardrails
- Do not weaken governance by deleting deeper planning or command surfaces just to reduce visible surface count.
- Do not blur workflow-route boundaries through generic merged language that makes reconciliation and review routes indistinguishable.
- Do not keep full closed-history initiative entries in the default coordination artifact once explicit closed-history lookup is available elsewhere.

## Risks
- Coordination-query compatibility is the main implementation risk because current consumers may rely on terminal initiative lookups through the coordination command even though the default coordination snapshot should stay compact.
- The interrupted workflow-route worktree may hide additional adjacent workflow drift that only appears after the first route fix lands and a second review pass starts from the new route boundaries.
- Entry-point thinning can accidentally drop the most useful example or next-step signal if the documents become too minimal instead of proportionally route-first.

## References
- March 2026 refactor audit
