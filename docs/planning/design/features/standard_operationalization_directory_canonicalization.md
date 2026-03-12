---
trace_id: trace.standard_operationalization_directory_canonicalization
id: design.features.standard_operationalization_directory_canonicalization
title: Standard Operationalization Directory Canonicalization Feature Design
summary: Defines the technical design boundary for Standard Operationalization Directory
  Canonicalization.
type: feature_design
status: draft
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

# Standard Operationalization Directory Canonicalization Feature Design

## Record Metadata
- `Trace ID`: `trace.standard_operationalization_directory_canonicalization`
- `Design ID`: `design.features.standard_operationalization_directory_canonicalization`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.standard_operationalization_directory_canonicalization`
- `Linked Decisions`: `decision.standard_operationalization_directory_canonicalization_direction`
- `Linked Implementation Plans`: `design.implementation.standard_operationalization_directory_canonicalization`
- `Updated At`: `2026-03-12T02:06:54Z`

## Summary
Defines the technical design boundary for Standard Operationalization Directory Canonicalization.

## Source Request
- Another expansive internal standards review reproduced one live standards defect: the CLI help standard publishes both `docs/commands` and `docs/commands/`, and the current parser/sync path preserves that semantic duplicate in the governed standard index.

## Scope and Feature Boundary
- Covers the governed standards parser, standard-document guidance, the affected live CLI help standard, and regression coverage for canonical operationalization-path behavior.
- Excludes changes to standards query ranking, unrelated standard families, or new command surfaces beyond the validation and sync behavior needed to close this defect.

## Current-State Context
- `parse_standard_operationalization(...)` currently validates existence and bounded globs but preserves directory path spellings exactly, so `docs/commands` and `docs/commands/` are treated as distinct values until they reach the standard index.
- The live standard corpus currently has one reproduced instance of the defect in [cli_help_text_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/cli_help_text_standard.md), and the generic standard-document guidance does not explicitly require canonical directory-path syntax.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): prefer a fail-closed contract fix at the shared parser boundary over leaving semantically duplicate metadata to be cleaned up only in downstream indexes.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the standards corpus must make operational enforcement explicit and auditable without ambiguous path forms.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the live standard index should not publish semantically duplicate operationalization metadata for one standard entry.
- [cli_help_text_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/cli_help_text_standard.md): the reproduced defect lives in the CLI help standard and must be corrected in the same slice as the parser hardening.

## Design Goals and Constraints
- Fail closed on non-canonical directory operationalization paths instead of silently tolerating duplicate spellings.
- Keep the operationalization data model string-based and backward-compatible for canonical exact paths, directories, and glob patterns.
- Preserve current lookup behavior for already-canonical exact-file, directory, and glob operationalization entries.

## Options Considered
### Option 1
- Normalize non-canonical directory paths silently during parsing and allow raw docs to keep mixed file and directory spelling.
- Keeps sync output canonical even if authored docs drift.
- Leaves the authored standards corpus inconsistent and delays failure until an artifact audit or reviewer notices the drift.

### Option 2
- Treat canonical operationalization syntax as a governed validation rule: exact files stay slash-free, directories must end in `/`, live standards are corrected, and regressions protect the rule.
- Removes ambiguity at the authoring boundary and prevents duplicate directory spellings from reaching downstream artifacts.
- Requires same-change updates across parser behavior, standards docs, the authoring template, and tests.

## Recommended Design
### Architecture
- Tighten the shared standard-operationalization parser so directory surfaces without a trailing `/` fail validation and sync, while canonical exact-file and glob entries continue to pass unchanged.
- Update the standard-document guidance and template so future standards authors publish one canonical path form intentionally instead of relying on implicit equivalence.
- Correct the live CLI help standard to use canonical directory syntax and add unit plus integration regressions that exercise both fixture-driven and live-corpus protection.

### Data and Interface Impacts
- `parse_standard_operationalization(...)` becomes stricter for directory surfaces and turns the canonical path form into a validation-time contract.
- The live standard index continues to publish string `operationalization_paths`, but canonical directory entries now use exactly one slash-terminated form.
- The standard authoring template and live artifact tests need same-change alignment so guidance, validation, and corpus state do not drift.

### Execution Flow
1. Parse each standard's `Operational Surfaces` metadata and reject any directory surface that omits the canonical trailing `/`.
2. Update the affected standards guidance and live CLI help standard to use canonical exact-file and directory syntax.
3. Rebuild the standard index and run regression coverage that proves non-canonical directory spellings fail closed and canonical live output remains duplicate-free.

### Invariants and Failure Cases
- Non-canonical directory operationalization paths must fail validation and sync before they can reach the standard index.
- Canonical exact-file and bounded glob operationalization paths must continue to validate and query exactly as they do today.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/control_plane/indexes/standards/standard_index.v1.json

## Design Guardrails
- Keep the remediation bounded to standard-operationalization canonicalization; do not broaden unrelated standards-query behavior in the same slice.
- Update live docs, validation coverage, and derived standard-index output in the same change set as the parser hardening.

## Risks
- Any additional latent non-canonical directory path in the live standards corpus will now fail validation immediately, so the final follow-up review pass must confirm no further corpus drift remains.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
