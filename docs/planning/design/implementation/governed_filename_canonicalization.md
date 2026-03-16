---
trace_id: trace.governed_filename_canonicalization
id: design.implementation.governed_filename_canonicalization
title: Versionless Governed Artifact Filenames Implementation Plan
summary: Breaks Versionless Governed Artifact Filenames into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T17:55:05Z'
audience: shared
authority: supporting
applies_to:
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/
---

# Versionless Governed Artifact Filenames Implementation Plan

## Record Metadata
- `Trace ID`: `trace.governed_filename_canonicalization`
- `Plan ID`: `design.implementation.governed_filename_canonicalization`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.governed_filename_canonicalization`
- `Linked Decisions`: `decision.governed_filename_canonicalization_direction`
- `Source Designs`: `design.features.governed_filename_canonicalization`
- `Linked Acceptance Contracts`: `contract.acceptance.governed_filename_canonicalization`
- `Updated At`: `2026-03-16T17:55:05Z`

## Summary
Breaks Versionless Governed Artifact Filenames into a bounded implementation slice.

## Source Request or Design
- design.features.governed_filename_canonicalization

## Scope Summary
- Covers the standards change, governed file rename, runtime and test path repair, planning reconciliation, and final validation needed to remove filename-embedded `.v1` tokens from governed artifacts.
- Excludes schema-URN redesign and any broader payload-model changes beyond what the path migration requires.

## Assumptions and Constraints
- The migration is allowed to be breaking because the product is not released, but the repository must end in one internally consistent state without compatibility leftovers.
- The physical rename has to include archived planning references and retained record links if they point at moved governed files.

## Internal Standards and Canonical References Applied
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md): will be changed to prohibit version tokens in governed filenames.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): still governs schema placement and contract metadata after the rename.
- [repository_validation_standard.md](/docs/standards/validations/repository_validation_standard.md): final validation has to prove the renamed paths work across artifact, document, and acceptance checks.

## Proposed Technical Approach
- Rename every governed file under `core/control_plane/` that currently carries `.v1` in its filename to the matching versionless filename.
- Apply one repo-wide path rewrite from versioned governed filenames to versionless governed filenames across Python code, tests, docs, registries, contracts, ledgers, and archived planning records.
- Repair any remaining dynamic filename builders in code so future generated artifacts use the new canonical names by construction.
- Refresh derived surfaces, then validate the repository before closing the initiative.

## Work Breakdown
1. Update the governing standards and planning artifacts, and create the bounded execution tasks for the migration.
2. Rename governed files under `core/control_plane/`, update runtime code and tests, and rewrite all repository path references to the versionless names.
3. Refresh derived planning surfaces, run the full validation stack, reconcile acceptance and evidence, and close the initiative.

## Risks
- Bulk file renames can leave the repo temporarily inconsistent; validation has to happen only after the physical rename and path-rewrite passes are both complete.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json`.
- Run `./.venv/bin/watchtower-core validate acceptance --trace-id trace.governed_filename_canonicalization --format json`.
- Run `./.venv/bin/watchtower-core validate all --format json`.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .`.
- Run scoped `rg` audits for versioned governed filenames after the rename to confirm no active `.v1` path convention remains.

## References
- [governed_filename_canonicalization.md](/docs/planning/prds/governed_filename_canonicalization.md)
- [governed_filename_canonicalization.md](/docs/planning/design/features/governed_filename_canonicalization.md)
