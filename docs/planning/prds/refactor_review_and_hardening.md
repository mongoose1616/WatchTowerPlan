---
trace_id: trace.refactor_review_and_hardening
id: prd.refactor_review_and_hardening
title: Refactor Review and Hardening PRD
summary: Review and rationalize refactor opportunities across workflow routing, planning
  projections, command entrypoints, repo-local hotspots, reference signaling, and
  adjacent governed surfaces without weakening governance.
type: prd
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

# Refactor Review and Hardening PRD

## Record Metadata
- `Trace ID`: `trace.refactor_review_and_hardening`
- `PRD ID`: `prd.refactor_review_and_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.refactor_review_and_hardening_direction`
- `Linked Designs`: `design.features.refactor_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.refactor_review_and_hardening`
- `Updated At`: `2026-03-13T14:13:18Z`

## Summary
Review and rationalize refactor opportunities across workflow routing, planning projections, command entrypoints, repo-local hotspots, reference signaling, and adjacent governed surfaces without weakening governance.

## Problem Statement
The March 2026 refactor audit confirmed that the repository's biggest near-term simplification opportunity is not policy rollback or family collapse. It is targeted reduction of high-leverage derivative-surface sprawl. Four connected issues sit at the front of that path. First, workflow routing currently relies on subtle distinctions between adjacent routes, so bounded documentation-audit requests can fall through to broader review routes or no match at all. Second, the coordination index still carries full closed-history initiative entries even though the coordination standard defines it as a compact machine start-here surface. Third, the planning start-here docs still leave current-state routing and artifact-versus-initiative status semantics too easy to misread during closed-history-heavy repository periods. Fourth, the root and group command pages have grown into handbook-like catalogs that duplicate low-value route and example detail already covered by CLI help, command indexes, and leaf command pages.

These issues belong to one stable phase-one refactor slice because they all affect how humans and machines enter the repository, route to the right surface, and distinguish current-state summaries from deeper family or historical views. They are also the safest high-leverage refactors in the audit: they can reduce navigation cost and derivative duplication without weakening governance, collapsing artifact families, or reopening the higher-risk hotspot and policy work.

## Goals
- Build and publish one explicit coverage map and findings ledger for the phase-one refactor slice before remediation begins.
- Fix the confirmed workflow-route discrimination gap so bounded documentation-review requests land on the intended route and aligned workflow metadata surfaces.
- Slim coordination default payloads back to compact current-state behavior while preserving explicit recent-closeout context and explicit closed-history lookup behavior.
- Thin planning and command umbrella entrypoints so they route to the smallest useful deeper surfaces instead of restating large command or planning catalogs.
- Run targeted validation, full repository validation, repeated confirmation passes, and initiative closeout only after no new actionable issue remains inside this phase-one slice.

## Non-Goals
- Collapsing PRDs, feature designs, implementation plans, decision records, acceptance contracts, or validation evidence into fewer artifact families.
- Starting the deeper repo-local hotspot decomposition work for planning scaffolds, task lifecycle, or shared model boilerplate in this trace.
- Reducing traceability or task-handling policy cost in the same slice as the current-state and routing simplifications.
- Folding reference-lifecycle labeling or placeholder control-plane-family cleanup into this trace unless one of those surfaces becomes a direct blocker for the phase-one fixes.

## Requirements
- `req.refactor_review_and_hardening.001`: The trace must publish and follow an explicit coverage map plus findings ledger across workflow routing, workflow metadata, route preview, coordination sync and query paths, planning entrypoints, command umbrella docs, standards, indexes, trackers, and related regression tests before remediation begins.
- `req.refactor_review_and_hardening.002`: Workflow routing must distinguish bounded documentation review from documentation refresh, repository review, and adjacent reconciliation routes across authored workflow docs, route metadata, route preview behavior, and regression coverage.
- `req.refactor_review_and_hardening.003`: The coordination index and its human companion surfaces must stay compact current-state summaries by default; they must not reproduce full closed-history initiative detail in their default payloads, and explicit closed-history coordination lookups must remain available through the correct derived source.
- `req.refactor_review_and_hardening.004`: Planning and command umbrella entrypoints must remain route-first, clarify current-state versus deeper-history routing, and remove low-value duplicated example or catalog content already covered by CLI help, indexes, or leaf docs.
- `req.refactor_review_and_hardening.005`: The initiative must create bounded execution tasks, perform targeted and full validation, run post-fix, second-angle, and adversarial confirmation passes, refresh durable evidence, close the tasks, and finish in a clean committed state.

## Acceptance Criteria
- `ac.refactor_review_and_hardening.001`: The planning corpus for `trace.refactor_review_and_hardening` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the phase-one slice.
- `ac.refactor_review_and_hardening.002`: Bounded documentation-review prompts select the dedicated documentation-review route, and the routing table, workflow registry, workflow index, route index, route-preview docs, and regression tests all agree on the adjacent route distinctions.
- `ac.refactor_review_and_hardening.003`: The coordination index default payload and coordination tracker stay compact current-state surfaces, recent closeouts remain compact context, and explicit terminal-status coordination queries still resolve through the intended derived initiative data instead of requiring duplicated default coordination payload.
- `ac.refactor_review_and_hardening.004`: `docs/planning/README.md`, `docs/planning/initiatives/README.md`, `docs/commands/core_python/watchtower_core.md`, `docs/commands/core_python/watchtower_core_query.md`, and `docs/commands/core_python/watchtower_core_sync.md` stay route-first and no longer act like broad handbook catalogs for the same surface.
- `ac.refactor_review_and_hardening.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete without finding a new actionable issue inside this phase-one refactor slice.

## Risks and Dependencies
- The coordination compaction change touches sync output, query behavior, standards, examples, and tests in one slice, so incomplete same-change updates could create legitimate drift even if the core logic is correct.
- Workflow-route clarification must stay sharp enough to reduce ambiguity without collapsing intentionally distinct routes into broader generic review behavior.
- Entry-point thinning must preserve leaf command docs, deeper family trackers, and machine lookup surfaces so the change reduces low-value repetition instead of removing real navigation support.
- Deeper hotspot and policy findings from the audit remain real follow-up work; this initiative depends on keeping that later work explicit instead of letting the current slice expand into an uncloseable mega-trace.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): simplify by tightening explicit seams and current-state projections rather than weakening governed artifact boundaries.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human docs, machine-readable indexes, query behavior, and regression coverage must move together when start-here or routing behavior changes.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): this trace stays inside repository-maintenance refactor work and does not expand into future product implementation.

## References
- March 2026 refactor audit
