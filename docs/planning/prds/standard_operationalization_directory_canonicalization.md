---
trace_id: trace.standard_operationalization_directory_canonicalization
id: prd.standard_operationalization_directory_canonicalization
title: Standard Operationalization Directory Canonicalization PRD
summary: Canonicalize directory operationalization paths in governed standards, eliminate
  semantically duplicate directory entries from the standard index, and harden standards
  validation against future duplicate-path drift.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T02:06:54Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/control_plane/indexes/standards/standard_index.v1.json
---

# Standard Operationalization Directory Canonicalization PRD

## Record Metadata
- `Trace ID`: `trace.standard_operationalization_directory_canonicalization`
- `PRD ID`: `prd.standard_operationalization_directory_canonicalization`
- `Status`: `active`
- `Linked Decisions`: `decision.standard_operationalization_directory_canonicalization_direction`
- `Linked Designs`: `design.features.standard_operationalization_directory_canonicalization`
- `Linked Implementation Plans`: `design.implementation.standard_operationalization_directory_canonicalization`
- `Updated At`: `2026-03-12T02:06:54Z`

## Summary
Canonicalize directory operationalization paths in governed standards, eliminate semantically duplicate directory entries from the standard index, and harden standards validation against future duplicate-path drift.

## Problem Statement
- `std.engineering.cli_help_text` currently publishes both `docs/commands` and `docs/commands/`, so the live standard index can carry semantically duplicate directory operationalization paths for one standard.
- The governed standards parser preserves file and directory spellings exactly, so non-canonical directory syntax can pass through sync and query surfaces instead of failing closed during standards validation.
- The standard authoring contract and template do not currently require one canonical directory-path form, so the standards corpus has no explicit guardrail against reintroducing duplicate directory entries.

## Goals
- Make standard operationalization parsing and validation reject non-canonical directory paths before they enter the live standard index.
- Align the affected live standards and authoring guidance on one canonical operationalization-path form for exact files and directories.
- Add regression coverage that proves duplicate directory spellings cannot return through sync, validation, or live-corpus standards audits.

## Non-Goals
- Change `watchtower-core query standards` matching semantics beyond the operationalization-path canonicalization needed for this defect.
- Rework unrelated standards families whose operationalization paths are already canonical and non-duplicative.
- Introduce a new artifact family or command surface for standards canonicalization.

## Requirements
- `req.standard_operationalization_directory_canonicalization.001`: Governed standard operationalization metadata must use one canonical path form: exact repo-relative file paths for files and repo-relative directory paths ending in `/` for directories.
- `req.standard_operationalization_directory_canonicalization.002`: Standards parsing, semantic validation, and standard-index sync must reject non-canonical directory operationalization paths so semantically duplicate directory entries cannot reach the live standard index.
- `req.standard_operationalization_directory_canonicalization.003`: The affected live standards, template guidance, and regression suite must be updated in the same slice so the standards corpus and validation behavior remain aligned.

## Acceptance Criteria
- `ac.standard_operationalization_directory_canonicalization.001`: The traced planning chain captures the issue, accepted direction, implementation approach, acceptance contract, evidence baseline, and bounded task set for this remediation slice.
- `ac.standard_operationalization_directory_canonicalization.002`: `parse_standard_operationalization(...)`, document-semantics validation, and standard-index sync reject directory operationalization paths that omit a trailing `/`, and the live CLI help standard publishes only canonical directory forms.
- `ac.standard_operationalization_directory_canonicalization.003`: Regression coverage proves non-canonical directory paths fail closed and the live standard corpus publishes canonical operationalization paths without semantically duplicate directory entries.
- `ac.standard_operationalization_directory_canonicalization.004`: The traced slice validates end to end, closes cleanly, and a final follow-up standards review pass finds no additional actionable issues.

## Risks and Dependencies
- Tightening the parser will fail fast on any latent non-canonical directory syntax in the standards corpus, so the live documents and template guidance must be updated in the same change set.
- The standard index, task trackers, traceability joins, and decision tracker must stay synchronized with the traced planning artifacts throughout the remediation and closeout cycle.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
