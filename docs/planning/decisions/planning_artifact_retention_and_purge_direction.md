---
trace_id: trace.planning_artifact_retention_and_purge
id: decision.planning_artifact_retention_and_purge_direction
title: Planning Artifact Retention and Purge Direction Decision
summary: Records the accepted direction decision for Planning Artifact Retention and
  Purge.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-15T11:00:00Z'
audience: shared
authority: supporting
---

# Planning Artifact Retention and Purge Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_artifact_retention_and_purge`
- `Decision ID`: `decision.planning_artifact_retention_and_purge_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_artifact_retention_and_purge`
- `Linked Designs`: `design.features.planning_artifact_retention_and_purge`
- `Linked Implementation Plans`: `design.implementation.planning_artifact_retention_and_purge`
- `Updated At`: `2026-03-15T11:00:00Z`

## Summary
Records the accepted direction decision for Planning Artifact Retention and Purge.

## Decision Statement
For closed traces whose durable policy has already been promoted into surviving canonical artifacts, purge the full trace-local planning package by `trace_id` and keep only a minimal machine-readable purge ledger entry plus the promoted surviving authority surfaces.

## Trigger or Source Request
- Need a purge/clean plan so past decisions become part of standards and related artifacts are purged instead of being kept forever.

## Current Context and Constraints
- The repository already compacts human trackers to active-first views, but the underlying closed trace artifacts still remain in the repo by default.
- Current governance standards still assume retained history unless an explicit retirement or closeout model says otherwise.
- Some standards and planning docs still point directly at historical task files, which means direct deletion would break canonical references unless those dependencies are repaired first.
- A future purge model has to preserve minimal history and current authority without leaving partial cleanup or silent traceability drift.

## Applied References and Implications
- `docs/foundations/repository_standards_posture.md`: current policy should live in synchronized canonical artifacts rather than in duplicated historical surfaces.
- `docs/foundations/engineering_design_principles.md`: readable current authority must stay explicit and separate from historical clutter.
- `docs/standards/governance/decision_capture_standard.md`: accepted decisions should propagate into standards or other canonical artifacts instead of remaining the only active policy source.
- `docs/standards/governance/traceability_standard.md`: purge must not create silent link drift; it needs an explicit surviving machine-readable record.
- `docs/planning/design/features/summary_surface_retirement.md`: targeted retirement is acceptable when the direct dependency chain is repaired first.

## Affected Surfaces
- docs/standards/governance/planning_retention_and_purge_standard.md
- docs/standards/governance/traceability_standard.md
- docs/standards/governance/task_tracking_standard.md
- docs/planning/
- core/control_plane/ledgers/purges/
- core/control_plane/indexes/
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/cli/

## Options Considered
### Option 1
- Keep closed trace-local planning artifacts in the repository forever and rely only on compact trackers to hide the clutter.
- Strength: avoids new purge tooling.
- Tradeoff: current policy and low-value historical packages continue to accumulate together indefinitely.

### Option 2
- Delete older planning artifacts ad hoc once a maintainer believes the trace is no longer needed.
- Strength: reduces clutter quickly.
- Tradeoff: unsafe, unreviewable, and likely to leave broken references or partial trace cleanup behind.

### Option 3
- Promote the lasting rule into a surviving canonical artifact, then purge the entire closed trace package through a guarded workflow and retain only a minimal purge ledger entry.
- Strength: reduces clutter while preserving current authority and minimal machine-readable history.
- Tradeoff: requires a new standard, dependency cleanup, and guarded purge tooling.

## Chosen Outcome
Adopt option 3. Closed trace-local artifacts should not remain in the repository forever once their durable policy has been promoted into surviving canonical artifacts and the trace satisfies explicit purge preconditions.

## Rationale and Tradeoffs
- Keeping every closed planning package forever makes the planning corpus harder to navigate and lets historical artifacts compete visually with current policy.
- Ad hoc deletion is worse because it breaks the repository's governed same-change posture and leaves no trustworthy surviving history surface.
- A promote-then-purge model preserves the active rule in standards or other current authority while keeping one small machine-readable record of what was removed.

## Consequences and Follow-Up Impacts
- The repository needs a new retention standard that defines purge eligibility, surviving authority, and minimal retained history.
- Direct canonical references to purgeable historical task paths need to be removed or replaced.
- A guarded purge workflow and minimal purge ledger need to be implemented before any pilot purge is attempted.
- Closed trace history will become explicit, bounded, and removable rather than an implied permanent archive.

## Risks, Dependencies, and Assumptions
- Risk: a purge workflow could miss one surviving canonical reference and leave broken links behind.
- Dependency: lasting rationale must be promoted before a trace package is removed.
- Assumption: a single minimal purge ledger entry is sufficient surviving history once the active rule has moved into standards or other current authority surfaces.

## References
- docs/standards/governance/planning_retention_and_purge_standard.md
- docs/standards/governance/traceability_standard.md
- docs/standards/governance/decision_capture_standard.md
- docs/standards/governance/task_tracking_standard.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/standards/governance/rewrite_execution_control_standard.md
- docs/planning/design/features/summary_surface_retirement.md
