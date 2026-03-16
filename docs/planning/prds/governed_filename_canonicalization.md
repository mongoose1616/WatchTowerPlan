---
trace_id: trace.governed_filename_canonicalization
id: prd.governed_filename_canonicalization
title: Versionless Governed Artifact Filenames PRD
summary: Removes filename-embedded v1 tokens from governed schemas and control-plane
  artifacts so compatibility signaling lives inside the artifact content instead of
  the path.
type: prd
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

# Versionless Governed Artifact Filenames PRD

## Record Metadata
- `Trace ID`: `trace.governed_filename_canonicalization`
- `PRD ID`: `prd.governed_filename_canonicalization`
- `Status`: `active`
- `Linked Decisions`: `decision.governed_filename_canonicalization_direction`
- `Linked Designs`: `design.features.governed_filename_canonicalization`
- `Linked Implementation Plans`: `design.implementation.governed_filename_canonicalization`
- `Updated At`: `2026-03-16T17:55:05Z`

## Summary
Removes filename-embedded v1 tokens from governed schemas and control-plane artifacts so compatibility signaling lives inside the artifact content instead of the path.

## Problem Statement
- The repository currently encodes a major-version token such as `.v1` directly in governed schema, contract, index, ledger, and related artifact filenames across `core/control_plane/`.
- The active naming standard tells authors to keep that filename version token, which forces compatibility signaling into paths, increases rename churn, and makes ordinary path references noisier than the machine-readable artifact content already requires.
- Runtime loaders, sync services, tests, standards, and planning records have all been built around that filename convention, so the repository cannot adopt versionless governed filenames safely without one bounded migration that updates the standard, the physical files, and every live path consumer together.

## Goals
- Remove filename-embedded major-version tokens from governed schemas and control-plane artifacts under `core/control_plane/`.
- Keep compatibility signaling inside artifact content, primarily through schema URNs, artifact IDs, and explicit machine-readable metadata rather than through path suffixes.
- Update runtime code, validation logic, tests, registries, indexes, and documentation in one breaking but internally coherent slice so the repository does not keep mixed filename conventions.
- Enforce the new rule in the naming and schema standards so future governed artifacts do not reintroduce `.v1` path conventions.

## Non-Goals
- Changing human planning Markdown filenames or front matter IDs.
- Removing version tokens from schema URNs such as `urn:watchtower:schema:...:v1` in this slice.
- Preserving path-based compatibility aliases for old `.v1` governed filenames after the migration lands.
- Reworking artifact semantics beyond the filename and path convention change needed to keep the repository coherent.

## Requirements
- `req.governed_filename_canonicalization.001`: The initiative must publish a traced planning chain, direction decision, acceptance contract, evidence artifact, and bounded task set for the versionless governed-filename migration.
- `req.governed_filename_canonicalization.002`: The metadata naming and schema standards must explicitly prohibit filename-embedded major-version tokens for governed artifact files and must state that compatibility signaling lives in artifact content rather than the path.
- `req.governed_filename_canonicalization.003`: Governed control-plane schemas, contracts, indexes, ledgers, manifests, registries, and related generated outputs must remove `.v1` filename tokens from their canonical repository paths.
- `req.governed_filename_canonicalization.004`: Runtime loaders, sync services, bootstrap or closeout helpers, tests, command docs, and planning records that reference governed filenames must be updated in the same slice so no active path consumer depends on the retired `.v1` filenames.
- `req.governed_filename_canonicalization.005`: The migration must not leave active compatibility copies, duplicate physical files, or mixed filename conventions behind in the governed tree.
- `req.governed_filename_canonicalization.006`: The repository must remain green on sync, acceptance reconciliation, artifact validation, document validation, tests, type checking, and linting after the rename lands.

## Acceptance Criteria
- `ac.governed_filename_canonicalization.001`: The trace publishes an active PRD, accepted decision, active feature design, active implementation plan, aligned acceptance contract, evidence artifact, and bounded execution tasks for the versionless filename migration.
- `ac.governed_filename_canonicalization.002`: The naming and schema standards explicitly reject `.v1` or similar major-version tokens in governed filenames and direct compatibility signaling into artifact content.
- `ac.governed_filename_canonicalization.003`: The canonical governed file tree under `core/control_plane/` uses versionless filenames for schemas, contracts, indexes, ledgers, and related governed artifacts in scope.
- `ac.governed_filename_canonicalization.004`: Runtime code, tests, registries, generated docs, and planning records resolve the new versionless governed paths without active compatibility aliases for the old `.v1` filenames.
- `ac.governed_filename_canonicalization.005`: `watchtower-core sync all --write --format json`, `watchtower-core validate acceptance --trace-id trace.governed_filename_canonicalization --format json`, `watchtower-core validate all --format json`, `pytest -q`, `mypy src`, and `ruff check .` pass after the migration lands.
- `ac.governed_filename_canonicalization.006`: Initiative closeout records that the governed-filename migration is complete and that no active `.v1` filename convention remains in the governed artifact tree.

## Risks and Dependencies
- The migration is intentionally breaking and touches `209` governed files plus thousands of path references, so any missed consumer will surface as path or validation drift.
- Historical planning records and archived tasks may still cite old governed filenames; if those paths are preserved in retained docs, they still need the same-change path update to remain link-safe after the physical rename.
- Schema URNs and artifact IDs remain versioned in content, so the standards change must explain the boundary clearly to avoid conflating path versioning with contract versioning.

## References
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md)
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
