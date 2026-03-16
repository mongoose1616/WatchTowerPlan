---
trace_id: trace.versionless_governed_artifact_filenames
id: design.features.versionless_governed_artifact_filenames
title: Versionless Governed Artifact Filenames Feature Design
summary: Defines the technical design boundary for Versionless Governed Artifact Filenames.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T17:55:05Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/
---

# Versionless Governed Artifact Filenames Feature Design

## Record Metadata
- `Trace ID`: `trace.versionless_governed_artifact_filenames`
- `Design ID`: `design.features.versionless_governed_artifact_filenames`
- `Design Status`: `active`
- `Linked PRDs`: `prd.versionless_governed_artifact_filenames`
- `Linked Decisions`: `decision.versionless_governed_artifact_filenames_direction`
- `Linked Implementation Plans`: `design.implementation.versionless_governed_artifact_filenames`
- `Updated At`: `2026-03-16T17:55:05Z`

## Summary
Defines the technical design boundary for Versionless Governed Artifact Filenames.

## Source Request
- User request to stop using `v1` in governed filenames and to keep compatibility signaling inside the artifact content instead of the path.

## Scope and Feature Boundary
- Covers governed artifact and schema filenames under `core/control_plane/`, plus runtime code, tests, docs, and planning surfaces that reference those paths.
- Covers the repository naming and schema standards that currently require version tokens in governed filenames.
- Excludes schema-URN redesign or semantic changes to governed artifact payloads beyond what is needed to keep compatibility signaling inside the file content.

## Current-State Context
- The current naming standard explicitly requires versioned schema and machine-contract filenames, and the control-plane tree now contains `209` physical `.v1` governed files.
- Runtime code encodes those filenames directly in loader constants, sync outputs, bootstrap helpers, purge helpers, and test fixtures, so a partial rename would leave the repository inconsistent immediately.
- Most governed artifacts already signal compatibility inside content through schema URNs or machine-readable IDs, which makes the filename version token redundant for current repository use.

## Foundations References Applied
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): the path convention, runtime assumptions, and docs must change together in one same-change migration rather than drifting across multiple slices.
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): machine-readable artifacts should stay explicit and inspectable, which supports keeping compatibility signaling in content rather than path decoration.

## Internal Standards and Canonical References Applied
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md): this is the primary standard that must be changed because it currently mandates filename version tokens.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): schema placement and contract metadata remain governed even while filenames become versionless.
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): runtime path assumptions and validation must be repaired inside `core/python/` in the same change set.

## Design Goals and Constraints
- Eliminate `.v1` filename tokens from governed artifact paths without leaving compatibility copies behind.
- Preserve contract compatibility signaling through schema URNs, `$schema` references, and artifact IDs rather than inventing a second path-based version rule.
- Keep the migration repository-wide for governed path references so archived planning records remain link-safe after the physical rename.

## Options Considered
### Option 1
- Change the standard but leave existing `.v1` governed filenames in place until later.
- Lowest immediate implementation risk.
- Rejected because it would preserve the very convention the user wants removed and would leave mixed guidance active.

### Option 2
- Rename only active runtime paths and current docs while leaving archived planning references unchanged.
- Reduces immediate documentation churn.
- Rejected because the physical files would move, so archived planning references would become stale and link-unsafe.

### Option 3
- Rename the governed files, update every repository path reference, and revise the standards in one bounded breaking migration.
- Produces one coherent post-change state with no compatibility leftovers.
- Chosen because it matches the requested enforcement model and keeps the repo concise.

## Recommended Design
### Architecture
- Adopt versionless governed filenames such as `command_index.json` and `acceptance_contract.schema.json` while leaving schema URNs and artifact IDs versioned in content where needed.
- Rename the physical files under `core/control_plane/` and update every in-repo path consumer in Python code, tests, docs, registries, and planning records.
- Keep generated output families using the new versionless canonical paths so future sync runs do not reintroduce `.v1` filenames.

### Data and Interface Impacts
- Affects all governed schema filenames, acceptance contracts, indexes, ledgers, release or migration records, and generated file paths in scope.
- Affects loader constants, schema-catalog canonical paths, validator-registry paths, bootstrap or purge output naming, and sync output naming.
- Affects command docs, standards, planning docs, and tests that currently reference `.v1` filenames.

### Execution Flow
1. Update the naming and schema standards to define versionless governed filenames and clarify that compatibility signaling lives in artifact content.
2. Rename the governed files under `core/control_plane/` to their versionless canonical names.
3. Repair runtime code, tests, docs, registries, and planning references to use the renamed paths, then refresh generated surfaces and validate the repository.

### Invariants and Failure Cases
- Schema URNs and artifact IDs remain the canonical compatibility signals for this slice; the migration must not silently strip versioning from those content-level identifiers.
- The migration fails if any active runtime surface still depends on `.v1` governed paths or if both old and new filenames coexist in the governed tree.

## Affected Surfaces
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/

## Design Guardrails
- Do not leave compatibility copies, symlinks, or duplicate governed files with both versioned and versionless names.
- Do not expand the scope into payload-format redesign beyond the filename policy and the minimal metadata clarifications needed to explain it.

## Risks
- Bulk repo-wide path rewrites can miss edge-case test fixtures or historical planning references unless the final search and validation passes are comprehensive.

## References
- [versionless_governed_artifact_filenames.md](/docs/planning/prds/versionless_governed_artifact_filenames.md)
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md)
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md)
