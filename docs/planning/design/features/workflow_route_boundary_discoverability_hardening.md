---
trace_id: trace.workflow_route_boundary_discoverability_hardening
id: design.features.workflow_route_boundary_discoverability_hardening
title: Workflow Route Boundary Discoverability Hardening Feature Design
summary: Defines the technical design boundary for Workflow Route Boundary Discoverability
  Hardening.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T21:17:49Z'
audience: shared
authority: authoritative
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

# Workflow Route Boundary Discoverability Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.workflow_route_boundary_discoverability_hardening`
- `Design ID`: `design.features.workflow_route_boundary_discoverability_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.workflow_route_boundary_discoverability_hardening`
- `Linked Decisions`: `decision.workflow_route_boundary_discoverability_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.workflow_route_boundary_discoverability_hardening`
- `Updated At`: `2026-03-13T21:17:49Z`

## Summary
Defines the technical design boundary for Workflow Route Boundary Discoverability Hardening.

## Source Request
- Do another comprehensive internal project review for refactor under one stable workflow-boundary theme until no new actionable issues remain.
- Address the remaining route-lattice discoverability drift identified by the March 13, 2026 refactor audit under `RF-WKF-001`.

## Scope and Feature Boundary
- Cover the route-preview scorer, authored routing-table trigger phrases, workflow metadata trigger tags, workflow-query discoverability, route and workflow indexes, command docs, and direct regression coverage for adjacent reconciliation and task routes.
- Review the direct workflow modules, standards, schemas, validators, sync paths, and control-plane read models around those surfaces for same-theme drift, but keep remediation bounded to workflow discoverability and route-boundary signaling unless discovery proves a direct dependency defect.
- Exclude workflow-family consolidation, unrelated CLI family restructuring, global query-service rewrites, and standards-threshold policy changes.

## Current-State Context
- The workflow family remains intentionally explicit and small per file, but realistic reconciliation prompts still fail to match the intended routes because the current route-preview scorer requires full exact phrase or full exact token coverage against authored trigger phrases.
- `query workflows` derives discoverability from workflow titles, purpose summaries, task-family metadata, related paths, and trigger tags, but the adjacent reconciliation and task-hand-off boundaries are not surfaced strongly enough for realistic lookup phrases such as `cli behavior` or `successor tasks`.
- The current route-preview selection merges every positive route match, which means single-word matches like `validation` can leak unrelated workflows into a strongly scored handoff preview even when the request clearly signals a different dominant route.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): route-first and inspectable deterministic behavior should be preserved instead of replaced with opaque fuzzy routing.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): thin routing entrypoints should guide users toward the right explicit surface without duplicating workflow behavior or leaving neighboring routes ambiguous.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): routing must use full prompt context rather than exact keyword matching alone, while keeping route preview advisory and deterministic.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow modules must stay narrow, explicit, and distinct rather than being collapsed to hide route ambiguity.
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md): route-preview behavior must stay aligned with the authored routing table and companion workflow lookup surfaces.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow metadata should publish retrieval-oriented trigger terms that help users distinguish adjacent workflows without scanning raw Markdown.

## Design Goals and Constraints
- Improve realistic route discoverability for adjacent reconciliation and task routes without widening the workflow family or weakening determinism.
- Keep the explicit route lattice intact; the design should sharpen boundaries, not hide them behind generic routing or broad workflow unions.
- Preserve deliberate multi-route unions for genuinely composite prompts while filtering low-signal secondary matches that add no material routing signal.

## Options Considered
### Option 1
- Expand the routing-table trigger keywords only and leave the scorer or workflow lookup behavior unchanged.
- Strength: small authored-surface change with minimal runtime code churn.
- Tradeoff: would not address low-signal route leakage or weak workflow-query discoverability, so the same boundary ambiguity would persist through adjacent surfaces.

### Option 2
- Harden the deterministic route scorer, add higher-signal routing examples and workflow trigger tags, and refresh the companion docs and tests together.
- Strength: fixes the runtime failure mode and the discoverability surfaces in one bounded slice while preserving explicit authored workflow boundaries.
- Tradeoff: touches both runtime and governed routing surfaces, so indexes, docs, and regressions must all stay synchronized in the same change set.

## Recommended Design
### Architecture
- Keep authored route and workflow boundaries explicit in `ROUTING_TABLE.md`, the workflow modules, and the workflow metadata registry.
- Add lightweight canonical token handling and near-complete phrase coverage to the route-preview scorer so realistic prompts can match high-signal adjacent routes without requiring verbatim wording.
- Filter secondary route matches using deterministic score separation so a dominant phase-transition route can suppress unrelated low-signal matches like generic `validation` while still preserving intentionally composite prompts.
- Expand workflow metadata trigger tags and companion docs so `query workflows` and route-preview guidance reinforce the same adjacent-route distinctions.

### Data and Interface Impacts
- Runtime query surfaces: `watchtower-core route preview` scoring and `watchtower-core query workflows` retrieval outcomes.
- Governed metadata and derived artifacts: workflow metadata registry, route index, workflow index, and their command-doc or standard companions.
- No artifact-schema expansion is planned unless discovery uncovers a same-theme limitation that cannot be addressed through the existing retrieval fields.

### Execution Flow
1. Confirm the current boundary failure modes across route preview, workflow lookup, and authored workflow guidance.
2. Update the scorer and authored trigger surfaces together so realistic prompts and query terms resolve through the existing explicit workflow lattice.
3. Refresh the derived indexes, command docs, and regression coverage, then rerun repeated confirmation passes to ensure no new same-theme ambiguity remains.

### Invariants and Failure Cases
- Explicit `--task-type` route preview must remain authoritative and unchanged by free-form scoring adjustments.
- No-match route previews must remain possible and should keep their advisory warning instead of force-matching a weak route.
- Strongly signaled composite prompts must still return the merged workflow set when more than one route truly belongs in scope.
- The implementation must fail closed on missing workflow-index entries or invalid derived route or workflow artifacts just as it does today.

## Affected Surfaces
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- docs/commands/core_python/

## Design Guardrails
- Do not collapse or delete adjacent workflow modules merely to hide discoverability issues.
- Do not replace deterministic matching with opaque fuzzy search or model-generated routing.

## Risks
- Near-complete token coverage could overmatch adjacent routes if the scorer thresholds are too permissive.
- Workflow-query discoverability could still lag route preview if the metadata or docs are only partially updated.

## References
- March 13, 2026 refactor audit
- [workflow_route_boundary_discoverability_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_route_boundary_discoverability_hardening.md)
