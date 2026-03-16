---
id: task.governed_front_matter_directory_canonicalization.enforcement.001
trace_id: trace.governed_front_matter_directory_canonicalization
title: Implement governed applies_to directory canonicalization
summary: Add shared validation and normalization for directory-valued governed front-matter
  applies_to paths across governed document families and indexed lookup surfaces.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T03:09:28Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/python/src/watchtower_core/
- core/control_plane/
related_ids:
- prd.governed_front_matter_directory_canonicalization
- design.features.governed_front_matter_directory_canonicalization
- design.implementation.governed_front_matter_directory_canonicalization
- decision.governed_front_matter_directory_canonicalization.direction
- contract.acceptance.governed_front_matter_directory_canonicalization
---

# Implement governed applies_to directory canonicalization

## Summary
Add shared validation and normalization for directory-valued governed front-matter applies_to paths across governed document families and indexed lookup surfaces.

## Scope
- Add one shared governed-path helper for path-like applies_to values that canonicalizes or rejects directory entries without a trailing slash.
- Wire the helper through standards, references, foundations, and traced planning document loaders or sync surfaces so repo validation and derived indexes agree.
- Ensure path-based query behavior and derived related-path projection stay consistent with the canonical forms.

## Done When
- Non-canonical directory-valued applies_to metadata is rejected or normalized consistently across the affected governed families.
- Exact path lookup surfaces return results for canonical slash-terminated directory filters.
- Targeted regression coverage proves the shared enforcement path.
