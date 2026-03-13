---
trace_id: trace.refactor_review_and_hardening
id: decision.refactor_review_and_hardening_direction
title: Refactor Review and Hardening Direction Decision
summary: Records the initial direction decision for Refactor Review and Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T14:13:18Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/references/
- docs/standards/
- workflows/
---

# Refactor Review and Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.refactor_review_and_hardening`
- `Decision ID`: `decision.refactor_review_and_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.refactor_review_and_hardening`
- `Linked Designs`: `design.features.refactor_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.refactor_review_and_hardening`
- `Updated At`: `2026-03-13T14:13:18Z`

## Summary
Records the initial direction decision for Refactor Review and Hardening.

## Decision Statement
Execute only the audit's phase-one current-state simplification slice in this trace: finish workflow-route discrimination first, then slim coordination default payloads and route-first planning and command entrypoints, while deferring deeper hotspot, reference-lifecycle, placeholder-family, and policy refactors to later bounded traces.

## Trigger or Source Request
- Perform a comprehensive internal refactor review, fix validated issues end to end, and continue the review loop until repeated confirmation passes find no new actionable issue in scope.

## Current Context and Constraints
- The audit confirmed many real refactor opportunities, but they are not all equally safe or equally prerequisite-free.
- The current local worktree already contains an interrupted workflow-route discrimination slice, and the audit explicitly says route discrimination should be clarified before any broader workflow rationalization.
- The coordination, planning-entrypoint, and umbrella command-doc findings are the highest-leverage current-state simplifications that can land without collapsing governed families or reopening deeper policy decisions.
- Deeper hotspot decomposition and policy-cost review remain important, but they are higher-risk follow-up work that would over-expand this trace.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the right simplifications remove duplicated current-state and routing burden while preserving explicit authority seams.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): docs, indexes, query behavior, and tests must stay aligned in the same change sets when start-here semantics change.
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): workflow modularity stays intact; route discrimination should get clearer before any consolidation is considered.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): the coordination layer remains a compact current-state surface rather than a second full historical planning join.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): umbrella command pages remain route-first command references and should not grow into broad handbooks.

## Affected Surfaces
- core/python/
- core/control_plane/
- docs/planning/
- docs/commands/core_python/
- docs/references/
- docs/standards/
- workflows/

## Options Considered
### Option 1
- Execute one mega-trace across every confirmed refactor finding from the audit, including deep hotspots, reference-family follow-up, placeholder cleanup, and policy review.
- Strength: addresses the largest total backlog immediately.
- Tradeoff: mixes safe current-state simplifications with higher-risk decomposition and policy choices, making closeout evidence and scope control unrealistic.

### Option 2
- Execute the phase-one current-state simplification slice, starting with workflow-route discrimination and then landing compact coordination plus route-first entrypoint updates.
- Strength: delivers the audit's highest-leverage low-regret improvements in one bounded loop and directly incorporates the interrupted local worktree.
- Tradeoff: later hotspot, reference, placeholder, and policy findings remain explicit follow-up work rather than disappearing in the same trace.

### Option 3
- Start with deeper hotspot decomposition of planning scaffolds, task lifecycle, or shared model boilerplate before touching the current-state entry surfaces.
- Strength: reduces some of the largest code hotspots first.
- Tradeoff: bypasses the audit's safer prerequisite simplifications and leaves the visible routing and current-state duplication live longer.

## Chosen Outcome
Adopt option 2. This trace owns the phase-one current-state simplification work only. It finishes the interrupted workflow-route discrimination slice, slims default coordination payloads back to compact start-here behavior, thins planning and command umbrella entrypoints, validates the full repository baseline, and closes only after repeated no-new-issues confirmation passes remain clean.

## Rationale and Tradeoffs
- The phase-one slice is the highest-leverage part of the audit that can land without weakening governance boundaries or inventing a risky all-at-once restructuring program.
- The workflow-route discrimination work is already partially present in the local worktree, and the audit identifies it as a prerequisite before any later workflow rationalization.
- Coordination compaction, planning routing clarification, and command umbrella thinning all reduce immediate navigation and projection duplication while preserving deeper family surfaces.
- The tradeoff is explicit deferral of deeper hotspot and policy findings, but that is preferable to creating a broad trace that cannot be validated or closed cleanly.

## Consequences and Follow-Up Impacts
- The trace creates one workflow-route execution task, one coordination or entrypoint simplification task, and one validation-closeout task.
- Later bounded traces should pick up the deeper hotspot decomposition, reference-lifecycle signaling, placeholder-family cleanup, and policy-cost review findings from the audit.
- Coordination-query behavior must preserve explicit terminal-status lookups even though the default coordination artifact becomes more compact.

## Risks, Dependencies, and Assumptions
- Assumes the interrupted workflow-route worktree is consistent enough to complete within this trace without reverting unrelated work.
- Depends on same-change updates across workflow docs, routing metadata, coordination sync/query code, command docs, standards, and tests.
- Risks under-scoping adjacent drift if the post-fix and adversarial review passes do not revisit the touched route, coordination, and entrypoint surfaces from a fresh angle.

## References
- March 2026 refactor audit
