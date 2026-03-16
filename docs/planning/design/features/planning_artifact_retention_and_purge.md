---
trace_id: trace.planning_artifact_retention_and_purge
id: design.features.planning_artifact_retention_and_purge
title: Planning Artifact Retention and Purge Feature Design
summary: Defines the technical design boundary for Planning Artifact Retention and
  Purge.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-15T11:00:00Z'
audience: shared
authority: authoritative
---

# Planning Artifact Retention and Purge Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_artifact_retention_and_purge`
- `Design ID`: `design.features.planning_artifact_retention_and_purge`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.planning_artifact_retention_and_purge`
- `Linked Decisions`: `decision.planning_artifact_retention_and_purge_direction`
- `Linked Implementation Plans`: `design.implementation.planning_artifact_retention_and_purge`
- `Updated At`: `2026-03-15T11:00:00Z`

## Summary
Defines the technical design boundary for Planning Artifact Retention and Purge.

## Source Request
- Need a purge/clean plan so past decisions become part of standards and related artifacts are purged instead of being kept forever.

## Scope and Feature Boundary
- Covers the retention standard, direct dependency cleanup, minimal purge ledger, guarded trace purge workflow, and one pilot purge for a closed trace package.
- Excludes purging active traces, rewriting git history, or creating a second long-form historical archive outside the surviving ledger.

## Current-State Context
- The repository already uses active-first planning trackers, but the underlying closed trace-local planning corpus still accumulates indefinitely by default.
- The recent closed-task archive cleanup reduced root clutter but intentionally preserved archived task documents as canonical retained history.
- Current governance surfaces still assume retained history in places, including direct references from standards to historical task documents.
- A purge model has to protect current authority and machine-readable lookup surfaces while deleting the low-value closed trace package itself.

## Foundations References Applied
- `docs/foundations/repository_standards_posture.md`: current policy should remain in one synchronized canonical surface instead of duplicated historical packages.
- `docs/foundations/engineering_design_principles.md`: current authority must stay explicit and inspectable while historical material becomes clearly non-authoritative or removable.
- `docs/foundations/repository_scope.md`: repo-specific planning and governance cleanup belongs here and should stay governed rather than turning into ad hoc filesystem maintenance.

## Internal Standards and Canonical References Applied
- `docs/standards/governance/planning_retention_and_purge_standard.md`: defines the purge eligibility and surviving-authority contract this design must implement.
- `docs/standards/governance/traceability_standard.md`: purge cannot introduce silent trace-link drift or leave stale canonical references behind.
- `docs/standards/governance/task_tracking_standard.md`: normal task archival remains valid until an explicit trace purge removes the package.
- `docs/standards/governance/initiative_closeout_standard.md`: only terminal traces can enter the purge path.
- `docs/standards/governance/decision_capture_standard.md`: durable decisions must move into standards or surviving canonical artifacts before their local trace package is removed.

## Design Goals and Constraints
- Remove low-value closed trace packages without deleting the active policy that those traces produced.
- Purge by `trace_id` rather than by individual file family so cleanup remains reviewable and complete.
- Keep one minimal surviving machine-readable purge ledger entry instead of the full trace package.
- Preserve fail-closed behavior when a trace is still active, still referenced, or still the only place where durable rationale lives.

## Options Considered
### Option 1
- Keep the current retained-archive model and continue relying on compact trackers to hide history.
- Strength: minimal new implementation work.
- Tradeoff: the planning corpus keeps growing forever and historical artifacts keep competing with current authority.

### Option 2
- Delete closed planning artifacts directly once maintainers think the trace is no longer needed.
- Strength: fastest reduction in file count.
- Tradeoff: unsafe, partial, and likely to break current canonical references or derived indexes.

### Option 3
- Promote lasting policy into surviving canonical artifacts, then purge the full closed trace package through a guarded workflow and preserve only a minimal purge ledger entry.
- Strength: balances compactness with explicit surviving authority and safe automation.
- Tradeoff: requires new policy surfaces and a bounded purge implementation.

## Recommended Design
### Architecture
- One governance standard defines purge eligibility, surviving authority, and the minimal history that remains after purge.
- One minimal machine-readable purge ledger under `core/control_plane/ledgers/purges/` records purged traces and their surviving authority surfaces.
- One guarded repo-local purge workflow or command resolves the full trace package from `trace_id`, validates preconditions, deletes the package atomically, writes the purge ledger entry, and refreshes derived planning surfaces.

### Data and Interface Impacts
- Adds a purge-ledger artifact family under `core/control_plane/ledgers/purges/`.
- Updates planning trackers, indexes, and current standards so they no longer depend on purgeable historical task paths after purge.
- Adds a repo-local workflow or command interface for purging one eligible trace by `trace_id`.

### Execution Flow
1. Promote the lasting rule or rationale into surviving canonical artifacts and remove direct canonical references to the historical trace package.
2. Evaluate one closed trace for purge eligibility, reject the purge if any precondition fails, and materialize the full package path set from `trace_id`.
3. Delete the trace package, write the purge ledger entry, rebuild derived planning surfaces, and validate that no surviving canonical surface still depends on the removed paths.

### Invariants and Failure Cases
- A purge must never leave a partial trace package behind.
- A purge must fail closed when the trace still has open tasks, is not terminal, or remains referenced by surviving canonical surfaces.
- A purge must fail when the to-be-purged decision still contains unique rationale that has not been promoted into a surviving canonical artifact.

## Affected Surfaces
- docs/standards/governance/planning_retention_and_purge_standard.md
- docs/standards/governance/traceability_standard.md
- docs/standards/governance/task_tracking_standard.md
- docs/planning/
- core/control_plane/ledgers/purges/
- core/control_plane/indexes/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/cli/

## Design Guardrails
- Keep the surviving current policy in standards or other current canonical artifacts rather than in the purge ledger.
- Do not turn purge into a family-by-family cleanup shortcut; the workflow must remain trace-scoped and atomic.

## Risks
- The main risk is stale surviving references from standards, command docs, or indexes that would only surface after deletion if the precondition checks are incomplete.
- A second risk is choosing a pilot trace whose lasting rationale has not actually been promoted yet, which would remove information that still matters.

## References
- docs/standards/governance/planning_retention_and_purge_standard.md
- docs/standards/governance/traceability_standard.md
- docs/standards/governance/decision_capture_standard.md
- docs/standards/governance/task_tracking_standard.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/standards/governance/rewrite_execution_control_standard.md
- docs/planning/design/features/summary_surface_retirement.md
