---
trace_id: trace.foundations_summary_entrypoint_continuity
id: decision.foundations_summary_entrypoint_continuity_direction
title: Foundations Summary Entrypoint Continuity Direction Decision
summary: Records the initial direction decision for Foundations Summary Entrypoint
  Continuity.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T23:50:46Z'
audience: shared
authority: supporting
applies_to:
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundations Summary Entrypoint Continuity Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundations_summary_entrypoint_continuity`
- `Decision ID`: `decision.foundations_summary_entrypoint_continuity_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundations_summary_entrypoint_continuity`
- `Linked Designs`: `design.features.foundations_summary_entrypoint_continuity`
- `Linked Implementation Plans`: `design.implementation.foundations_summary_entrypoint_continuity`
- `Updated At`: `2026-03-12T23:50:46Z`

## Summary
Records the initial direction decision for Foundations Summary Entrypoint Continuity.

## Decision Statement
Restore a compact durable root `SUMMARY.md` document and protect it with a
fail-closed integration check instead of rewriting the foundations and
historical planning references that already point to it.

## Trigger or Source Request
- Full validation of the foundations documentation review slice exposed broken SUMMARY.md references in foundations-adjacent docs.

## Current Context and Constraints
- The root [README.md](/home/j/WatchTowerPlan/README.md) still inventories
  `SUMMARY.md` as the durable whole-repo audit and roadmap report.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
  and several historical planning slices still link to the root summary.
- Full repository validation now fails because the target file is missing,
  making the foundations review route and historical planning references
  incoherent.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): explicitly routes whole-repo assessment questions to the root summary entrypoint.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the authored entrypoint docs, restored summary, and validation surfaces to move together.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): constrains the root README inventory that still advertises `SUMMARY.md`.

## Affected Surfaces
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py

## Options Considered
### Option 1
- Remove or rewrite every `SUMMARY.md` reference to point at current root or
  planning entrypoints instead.
- Avoids restoring a root-level summary file.
- Requires broad churn across historical planning records and erases the
  durable review artifact those documents intentionally reference.

### Option 2
- Restore a compact root `SUMMARY.md` document and add fail-closed coverage for
  the entrypoint.
- Repairs the broken references with the smallest behavior change and preserves
  historical trace context.
- Leaves one additional root-level doc in place, so the summary must stay
  tightly bounded.

## Chosen Outcome
Apply Option 2.

## Rationale and Tradeoffs
- Restoring the missing target is lower risk than rewriting many historical
  references across the foundations and planning corpus.
- A compact durable summary preserves the context that those historical slices
  were written against.
- The tradeoff is retaining one root-level report surface, but that is
  acceptable so long as it stays concise and clearly historical.

## Consequences and Follow-Up Impacts
- The broken foundations and planning links to `SUMMARY.md` will resolve again.
- Full repository validation can return to green once the missing entrypoint is
  restored.
- The new integration regression will fail if the summary entrypoint disappears
  again while root/foundations docs still reference it.

## Risks, Dependencies, and Assumptions
- Assumes the historical planning references should remain intact and keep
  citing a durable summary artifact.
- Risks reintroducing root-doc sprawl if the restored summary grows beyond its
  historical-review role.
- Depends on adding a fail-closed regression so the problem does not recur
  silently.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [README.md](/home/j/WatchTowerPlan/README.md)
