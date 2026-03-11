---
trace_id: "trace.foundation_scope_and_entrypoint_realignment"
id: "design.implementation.foundation_scope_and_entrypoint_realignment"
title: "Foundation Scope and EntryPoint Realignment Implementation Plan"
summary: "Breaks the foundation-scope and root-entrypoint cleanup into bounded documentation slices with one accepted scope decision and a traced acceptance baseline."
type: "implementation_plan"
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

# Foundation Scope and EntryPoint Realignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.foundation_scope_and_entrypoint_realignment`
- `Plan ID`: `design.implementation.foundation_scope_and_entrypoint_realignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.foundation_scope_and_entrypoint_realignment`
- `Linked Decisions`: `decision.foundation_scope_boundary`
- `Source Designs`: `design.features.foundation_scope_and_entrypoint_realignment`
- `Linked Acceptance Contracts`: `contract.acceptance.foundation_scope_and_entrypoint_realignment`
- `Updated At`: `2026-03-11T01:27:13Z`

## Summary
Breaks the foundation-scope and root-entrypoint cleanup into bounded documentation slices with one accepted scope decision and a traced acceptance baseline.

## Source Request or Design
- [foundation_scope_and_entrypoint_realignment.md](/home/j/WatchTowerPlan/docs/planning/prds/foundation_scope_and_entrypoint_realignment.md)
- [foundation_scope_and_entrypoint_realignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/foundation_scope_and_entrypoint_realignment.md)

## Scope Summary
- Add one repository-scope foundation doc and realign the existing foundation layer around current repository ownership versus future WatchTower product context.
- Update root and nearby planning entrypoint docs so they stay thin and route to scope, review, and coordination.
- Keep the work documentation-only.
- Exclude planning-graph changes, root-document validator expansion, and external pack runtime work.

## Assumptions and Constraints
- The root README remains a thin router.
- The initiative uses one new foundation doc rather than rewriting the full foundation layer structure.
- Future product direction stays in foundations because it still materially informs planning and design work in this repository.

## Current-State Context
- The repo is validated and currently in `ready_for_bootstrap`, so the main need is coherence rather than new execution capability.
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md) already captures the evidence and rationale for this cleanup.

## Proposed Technical Approach
- Record an accepted direction decision that establishes the repository-scope precedence model.
- Create an acceptance contract and planning-baseline evidence that tie the new trace to the expected doc-only slices.
- Implement the actual doc changes in two bounded tasks:
  - foundation scope realignment
  - root and planning entrypoint routing cleanup
- Rebuild the foundation and repository-path indexes plus the derived planning trackers after each slice.

## Work Breakdown
1. Bootstrap the initiative, acceptance contract, planning-baseline evidence, decision record, and bounded task set.
2. Add `repository_scope.md` and realign the foundation layer around current repository scope versus future product context.
3. Tighten the root and planning entrypoint docs so they route to scope, review, and coordination without broadening root narrative.
4. Rebuild derived surfaces, validate the repo, close the tasks, and close the initiative.

## Dependencies
- Existing foundation docs and the foundation index.
- Current root README and planning coordination entrypoints.

## Risks
- The new repository-scope doc could become redundant if it simply repeats the root README.
- The root entrypoint cleanup could drift into unrelated validation or planning-model work if not kept narrow.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning or documentation changes.
- Run `./.venv/bin/watchtower-core validate all --format json` after each slice.
- Run `./.venv/bin/watchtower-core doctor --format json` after the final slice.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src`, and `./.venv/bin/ruff check .` before closeout to preserve the full baseline.

## Rollout or Migration Plan
- Land one planning-bootstrap commit first.
- Land one documentation commit for the foundation-layer realignment.
- Land one documentation commit for the root and planning entrypoint contract.
- Land a final closeout commit after validation passes and the trace is terminal.

## References
- [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
- [foundation_scope_and_entrypoint_realignment.md](/home/j/WatchTowerPlan/docs/planning/prds/foundation_scope_and_entrypoint_realignment.md)
- [foundation_scope_and_entrypoint_realignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/foundation_scope_and_entrypoint_realignment.md)

## Updated At
- `2026-03-11T01:27:13Z`
