---
trace_id: "trace.foundation_scope_and_entrypoint_realignment"
id: "decision.foundation_scope_boundary"
title: "Foundation Scope and EntryPoint Realignment Direction Decision"
summary: "Records the decision to publish an explicit repository-scope foundation, keep future product narrative clearly secondary for current repo ownership questions, and preserve a thin-root entrypoint model."
type: "decision_record"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:27:13Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/foundations/"
  - "README.md"
  - "docs/planning/README.md"
aliases:
  - "foundation scope"
  - "entrypoint realignment"
---

# Foundation Scope and EntryPoint Realignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundation_scope_and_entrypoint_realignment`
- `Decision ID`: `decision.foundation_scope_boundary`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundation_scope_and_entrypoint_realignment`
- `Linked Designs`: `design.features.foundation_scope_and_entrypoint_realignment`
- `Linked Implementation Plans`: `design.implementation.foundation_scope_and_entrypoint_realignment`
- `Updated At`: `2026-03-11T01:27:13Z`

## Summary
Records the decision to publish an explicit repository-scope foundation, keep future product narrative clearly secondary for current repo ownership questions, and preserve a thin-root entrypoint model.

## Decision Statement
Publish one authoritative repository-scope foundation for current `WatchTowerPlan` ownership, keep future product direction and customer narrative in clearly marked future-state or supporting roles, and keep root entrypoints as thin routers that link to scope and coordination rather than duplicating deeper narrative context.

## Trigger or Source Request
- User request to validate the issues captured in an earlier whole-repo review and execute the required remediation initiatives end to end.

## Current Context and Constraints
- The current foundation layer mixes present repository-operating truth and future WatchTower product framing.
- The root README is correctly thin, but it does not currently point to one explicit repository charter document.
- The repo is healthy and validated, so the problem is coherence and routing rather than correctness or missing tooling.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the chosen direction preserves explicit authority boundaries, compactness, and the reusable-core versus repo-ops split while clarifying current scope.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the decision favors one clearer authority surface over several co-equal foundation entrypoints for the same scope question.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the scope-direction change should remain explicitly tied to one trace, one accepted decision, and bounded closeable tasks rather than diffuse documentation edits.

## Affected Surfaces
- `docs/foundations/`
- `README.md`
- `docs/planning/README.md`

## Options Considered
### Option 1
- Add a few disclaimers to `product_direction.md` and `customer_story.md` only.
- Lowest editing cost.
- Rejected because contributors would still need to infer current repository scope from several documents.

### Option 2
- Add one authoritative repository-scope foundation and realign the existing foundation docs plus root entrypoints around it.
- Chosen because it makes current repository ownership explicit while preserving future product context where it still matters.
- Tradeoff: adds one more foundation doc and requires the foundation README to be very clear about precedence.

### Option 3
- Move future product direction and customer narrative out of the foundation layer entirely.
- Would maximize present-scope purity.
- Rejected because future product direction still materially informs planning and design work in this repository.

## Chosen Outcome
Adopt option 2. The repository will add a `repository_scope.md` foundation as the authoritative answer to current ownership questions, keep `product_direction.md` authoritative for future product shape, keep `customer_story.md` as supporting future-state narrative, and keep root entrypoints thin while routing readers to scope and coordination.

## Rationale and Tradeoffs
- This is the smallest change that removes the largest ambiguity in the current repo.
- It adds one clear scope authority without reopening planning architecture or validation behavior.
- The main tradeoff is another foundation file, which is acceptable because it resolves an already-confirmed ambiguity rather than adding decorative documentation.

## Consequences and Follow-Up Impacts
- Foundation routing and precedence need to be updated in the foundations README.
- Root and nearby planning entrypoints should point to repository scope and coordination instead of accumulating more root narrative.
- A later initiative can separately decide whether root documents should enter a stronger validation contract.

## Risks, Dependencies, and Assumptions
- The chosen model assumes the repo will still benefit from having future product direction available locally.
- If the new repository-scope doc is vague, the ambiguity will persist despite the extra file.

## References
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)

## Updated At
- `2026-03-11T01:27:13Z`
