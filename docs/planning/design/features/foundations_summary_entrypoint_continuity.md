---
trace_id: trace.foundations_summary_entrypoint_continuity
id: design.features.foundations_summary_entrypoint_continuity
title: Foundations Summary Entrypoint Continuity Feature Design
summary: Defines the technical design boundary for Foundations Summary Entrypoint
  Continuity.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T23:50:46Z'
audience: shared
authority: authoritative
applies_to:
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundations Summary Entrypoint Continuity Feature Design

## Record Metadata
- `Trace ID`: `trace.foundations_summary_entrypoint_continuity`
- `Design ID`: `design.features.foundations_summary_entrypoint_continuity`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.foundations_summary_entrypoint_continuity`
- `Linked Decisions`: `decision.foundations_summary_entrypoint_continuity_direction`
- `Linked Implementation Plans`: `design.implementation.foundations_summary_entrypoint_continuity`
- `Updated At`: `2026-03-12T23:50:46Z`

## Summary
Defines the technical design boundary for Foundations Summary Entrypoint Continuity.

## Source Request
- Full validation of the foundations documentation review slice exposed broken SUMMARY.md references in foundations-adjacent docs.

## Scope and Feature Boundary
- Covers restoring a durable root `SUMMARY.md` surface and the bounded
  regression coverage needed to keep the foundations-adjacent summary entrypoint
  coherent.
- Covers the foundations and root entrypoints that currently depend on that
  summary surface.
- Excludes re-running the full repository review or rewriting historical
  planning docs that only need their missing target restored.

## Current-State Context
- The root [README.md](/home/j/WatchTowerPlan/README.md) still inventories
  `SUMMARY.md` as the durable whole-repo audit and roadmap report.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
  and several historical planning slices still link to the root summary.
- `watchtower-core validate all --skip-acceptance --format json` now fails
  because the target file is missing, so the repo’s documented entrypoints and
  filesystem state no longer agree.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): explicitly routes repo-wide assessment questions to the root summary entrypoint.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the authored docs, derived indexes, and validation surfaces to stay aligned in the same change set.

## Internal Standards and Canonical References Applied
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): constrains the root README’s role as the inventory entrypoint that still advertises `SUMMARY.md`.
- [documentation_refresh.md](/home/j/WatchTowerPlan/workflows/modules/documentation_refresh.md): favors restoring existing documentation coherence over scattering ad hoc link rewrites across many files.
- [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py): is the bounded regression surface that can keep the summary entrypoint from disappearing again.

## Design Goals and Constraints
- Restore one durable summary target instead of forcing a broad rewrite of
  historical references.
- Keep the summary concise and historical; it should not become a new live
  handbook or task tracker.
- Preserve the root README and foundations review routes as valid entrypoints.

## Options Considered
### Option 1
- Remove or rewrite every `SUMMARY.md` reference to point at current root or
  planning entrypoints instead.
- Would avoid restoring a root-level summary file.
- Requires touching many historical planning records and erases the durable
  whole-repo review artifact they intentionally cite.

### Option 2
- Restore a compact durable root `SUMMARY.md` document and add fail-closed
  coverage for the entrypoint.
- Repairs the broken references with the smallest behavior change and preserves
  historical trace context.
- Leaves one additional root-level documentation file in place, so the summary
  must stay compact and clearly bounded.

## Recommended Design
### Architecture
- Reintroduce `SUMMARY.md` as a durable historical whole-repo review artifact at
  the repository root.
- Keep the restored summary focused on the historical findings and the
  foundations/planning follow-up context that existing docs cite.
- Add one integration artifact test that proves the root summary entrypoint
  exists while the root and foundations entrypoints reference it.

### Data and Interface Impacts
- Root entrypoint docs regain a valid repo-local target for `SUMMARY.md`.
- Document-semantics validation stops failing on the broken summary links.
- The repository-path index regains a live `SUMMARY.md` path target under the
  root README inventory.

### Execution Flow
1. Restore a concise durable `SUMMARY.md` document at the repository root.
2. Add integration coverage proving the root summary entrypoint exists and is
   still referenced by the root and foundations entrypoints.
3. Refresh derived indexes and rerun full validation so the repaired summary
   entrypoint is reflected everywhere.

### Invariants and Failure Cases
- The root README and foundations review routes must not point to missing local
  summary surfaces.
- The restored summary must remain a durable historical review artifact, not a
  mutable coordination tracker.
- If the root summary disappears again while entrypoint docs still reference it,
  targeted tests must fail.

## Affected Surfaces
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py

## Design Guardrails
- Do not mass-edit historical planning records when restoring the missing target
  is sufficient.
- Do not turn `SUMMARY.md` into a second root README or a live planning board.
- Keep the regression focused on entrypoint continuity rather than brittle
  prose snapshots.

## Risks
- The restored summary could drift into stale living documentation if it grows
  beyond its historical-review purpose.
- If regression coverage only checks the file’s existence and not the
  foundations entrypoints that rely on it, the route could break again through
  documentation drift.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [README.md](/home/j/WatchTowerPlan/README.md)
