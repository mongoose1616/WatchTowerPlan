---
id: task.governed_front_matter_directory_canonicalization.normalization.002
trace_id: trace.governed_front_matter_directory_canonicalization
title: Normalize live governed applies_to directory metadata
summary: Update the live governed documents with non-canonical directory-valued applies_to
  entries, regenerate derived artifacts, and prove the no-new-issues stop condition.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T03:09:38Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/control_plane/
related_ids:
- prd.governed_front_matter_directory_canonicalization
- design.features.governed_front_matter_directory_canonicalization
- design.implementation.governed_front_matter_directory_canonicalization
- decision.governed_front_matter_directory_canonicalization.direction
- contract.acceptance.governed_front_matter_directory_canonicalization
depends_on:
- task.governed_front_matter_directory_canonicalization.enforcement.001
---

# Normalize live governed applies_to directory metadata

## Summary
Update the live governed documents with non-canonical directory-valued applies_to entries, regenerate derived artifacts, and prove the no-new-issues stop condition.

## Scope
- Normalize every currently non-canonical governed document discovered by the applies_to audit so the authored repo state matches the new path contract.
- Regenerate affected indexes, trackers, and acceptance evidence so machine-readable projections reflect the canonical paths.
- Run the final expansive audit and record the stop-condition result when no new issues remain.

## Done When
- All live governed documents in the current audit publish canonical slash-terminated directory applies_to values.
- Full validation passes after the regenerated derived artifacts are written.
- A final expansive audit reports zero remaining governed-directory applies_to issues.
