---
trace_id: trace.internal_project_standards_review_and_hardening
id: design.implementation.internal_project_standards_review_and_hardening
title: Internal Project Standards Review and Hardening Implementation Plan
summary: Breaks Internal Project Standards Review and Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T17:51:15Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/
- core/python/src/watchtower_core/adapters/markdown.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Internal Project Standards Review and Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.internal_project_standards_review_and_hardening`
- `Plan ID`: `design.implementation.internal_project_standards_review_and_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.internal_project_standards_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_standards_review_and_hardening_direction`
- `Source Designs`: `design.features.internal_project_standards_review_and_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.internal_project_standards_review_and_hardening`
- `Updated At`: `2026-03-11T17:51:15Z`

## Summary
Breaks Internal Project Standards Review and Hardening into a bounded implementation slice.

## Source Request or Design
- design.features.internal_project_standards_review_and_hardening

## Scope Summary
- Replace the placeholder planning chain with the confirmed standards-review findings, accepted direction, and two bounded execution tasks.
- Make repo-path extraction source-aware in the governed Markdown adapter and propagate that contract through the affected sync, workflow, decision-index, planning, and citation-audit call sites.
- Align standard semantic validation and standard-index sync on one shared external-authority and governed local-reference rule.
- Add regression coverage and refresh planning, acceptance, evidence, and coordination surfaces through closeout.

## Assumptions and Constraints
- The repository continues to allow repository-absolute and document-relative repo-local Markdown links, so derived extraction must support both.
- Repo-path normalization must stay bounded to the current repository root and must not turn out-of-repo references into apparently valid repo-relative paths.
- The standard index remains a derived surface; the fix should improve correctness of derived reference data without moving authority out of the standard docs themselves.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): standards documents need consistent external-authority enforcement and support for document-relative repo-local links.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the standard index must reflect applied and cited reference use accurately enough for governance audits and machine lookup.
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md): decision related paths need the same repository-relative normalization as other governed sync surfaces.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): document-relative repo-local links are governed-valid and therefore need matching machine-readable extraction.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): planning docs, tasks, acceptance artifacts, and evidence need to stay aligned through the full task cycle.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): the final commit should close the trace in one logical slice with the runtime, tests, and planning surfaces aligned.

## Proposed Technical Approach
- Extend the Markdown adapter's repo-path normalization helpers with optional source-document context so one shared path can normalize repository-absolute, repo-root-relative, and document-relative repo-local references.
- Update the planning helper and the standard, decision, reference, foundation, workflow, and citation-audit sync call sites to pass the source Markdown path whenever extraction happens from authored content.
- Centralize standard reference accounting in `repo_ops/standards.py` and use it from both standard semantic validation and standard-index sync so the governed local-reference rule cannot drift again.
- Add targeted regression coverage first for the reproduced failures, then rerun the full repository baseline and refresh the derived planning surfaces before closeout.

## Work Breakdown
1. Rewrite the PRD, feature design, implementation plan, decision record, acceptance contract, planning-baseline evidence, and bootstrap task so the trace captures the confirmed review findings and bounded task split.
2. Implement source-aware repo-path extraction in `adapters/markdown.py` and propagate the new contract through the affected planning, sync, workflow, decision-index, and citation-audit helpers.
3. Implement the shared standard-reference accounting helper and update standard semantic validation plus standard-index sync to consume it.
4. Add regression coverage for both fixes, run the full validation stack, close the bootstrap and execution tasks, refresh evidence and coordination surfaces, and close the initiative.

## Risks
- Adapter-level repo-path extraction changes can have wide blast radius because the helper is reused by multiple derived families.
- The shared standard-reference helper must preserve the existing applied-reference semantics while fixing the local-reference requirement, not collapse the two concepts together.
- The trace will not be complete until the planning and coordination surfaces show zero open tasks and the acceptance evidence records the final green baseline.

## Validation Plan
- `./.venv/bin/pytest -q tests/unit/test_document_semantics_validation.py tests/unit/test_standard_index_sync.py tests/unit/test_reference_index_sync.py tests/unit/test_workflow_index_sync.py`
- `./.venv/bin/pytest -q tests/unit/test_decision_index_sync.py`
- `./.venv/bin/python -m mypy src/watchtower_core`
- `./.venv/bin/ruff check`
- `./.venv/bin/watchtower-core validate acceptance --trace-id trace.internal_project_standards_review_and_hardening --format json`
- `./.venv/bin/watchtower-core validate all --format json`
- `./.venv/bin/pytest -q`
- Final refreshed planning evidence under `core/control_plane/ledgers/validation_evidence/internal_project_standards_review_and_hardening_planning_baseline.v1.json`

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/data_contracts/decision_index_standard.md
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/workflow_md_standard.md
