---
id: task.governed_filename_canonicalization.rename_and_repair.002
trace_id: trace.governed_filename_canonicalization
title: Rename governed artifact filenames and repair consumers
summary: Renames the governed `.v1` file set to versionless paths and updates runtime,
  tests, docs, registries, and planning references to the new canonical names.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-16T18:16:42Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/
related_ids:
- prd.governed_filename_canonicalization
- design.features.governed_filename_canonicalization
- design.implementation.governed_filename_canonicalization
- decision.governed_filename_canonicalization_direction
- contract.acceptance.governed_filename_canonicalization
---

# Rename governed artifact filenames and repair consumers

## Summary
Renames the governed `.v1` file set to versionless paths and updates runtime, tests, docs, registries, and planning references to the new canonical names.

## Scope
- Rename the physical governed files under `core/control_plane/` from `.v1` names to versionless names.
- Repair Python code, tests, command docs, standards, registries, and planning records that reference the renamed files.
- Leave no active compatibility copies or duplicate governed file paths behind.

## Done When
- The governed file tree no longer uses `.v1` in canonical filenames.
- Runtime code and tests resolve only the new versionless canonical paths.
- Current and archived planning references remain link-safe after the rename.
