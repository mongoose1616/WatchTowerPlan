---
trace_id: trace.standard_operationalization_directory_canonicalization
id: design.implementation.standard_operationalization_directory_canonicalization
title: Standard Operationalization Directory Canonicalization Implementation Plan
summary: Breaks Standard Operationalization Directory Canonicalization into a bounded
  implementation slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T02:06:54Z'
audience: shared
authority: supporting
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

# Standard Operationalization Directory Canonicalization Implementation Plan

## Record Metadata
- `Trace ID`: `trace.standard_operationalization_directory_canonicalization`
- `Plan ID`: `design.implementation.standard_operationalization_directory_canonicalization`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.standard_operationalization_directory_canonicalization`
- `Linked Decisions`: `decision.standard_operationalization_directory_canonicalization_direction`
- `Source Designs`: `design.features.standard_operationalization_directory_canonicalization`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T02:06:54Z`

## Summary
Breaks Standard Operationalization Directory Canonicalization into a bounded implementation slice.

## Source Request or Design
- design.features.standard_operationalization_directory_canonicalization

## Scope Summary
- Covers parser hardening for canonical operationalization syntax, same-change standards and template updates, regression coverage, and traced validation/closeout.
- Excludes unrelated query-surface changes, new artifact families, and any standards corpus refresh not required by this canonicalization defect.

## Assumptions and Constraints
- The fix must preserve existing behavior for canonical exact-file and glob operationalization entries while rejecting non-canonical directory paths.
- The trace should stay bounded to one implementation task plus one validation/closeout task after the bootstrap task is closed.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the implementation must make canonical operationalization syntax explicit in both guidance and enforcement.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the slice needs explicit task transitions as it moves from planning to implementation and then to validation closeout.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): closeout must preserve the trace and task identifiers in the final commit metadata.

## Proposed Technical Approach
- Tighten the shared standard-operationalization parser so directory surfaces that omit `/` fail with a clear validation error before standard-index sync can publish them.
- Update the governing standard guidance, the standard authoring template, and the live CLI help standard so the corpus uses one canonical file-or-directory path form.
- Add unit and integration regressions for semantic validation, standard-index sync, and live-corpus canonicalization; then rebuild derived surfaces, validate the full repo, and close the trace.

## Work Breakdown
1. Replace the placeholder planning docs with real traced content, create the bounded implementation and validation tasks, and close the bootstrap task.
2. Implement the parser and standards-doc changes, then add regression coverage that proves non-canonical directory paths fail closed and live standard operationalization paths remain canonical.
3. Refresh derived surfaces, run targeted and end-to-end validation, update acceptance and evidence artifacts, close both execution tasks, close the initiative, and perform one more no-new-issues standards review pass.

## Risks
- Final closeout depends on the post-fix standards review pass finding no additional actionable issues in the standards corpus.

## Validation Plan
- Run targeted regressions: `pytest -q core/python/tests/unit/test_document_semantics_validation.py core/python/tests/unit/test_standard_index_sync.py core/python/tests/integration/test_control_plane_artifacts.py`.
- Rebuild and validate repository surfaces with `core/python/.venv/bin/watchtower-core sync standard-index --write --format json`, `core/python/.venv/bin/watchtower-core validate all --format json`, `core/python/.venv/bin/pytest -q`, `cd core/python && .venv/bin/python -m mypy src/watchtower_core`, and `core/python/.venv/bin/ruff check .`.
- Re-run the expansive standards audit after closeout to confirm no additional actionable issues remain.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/engineering/cli_help_text_standard.md
- docs/templates/standard_document_template.md
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
