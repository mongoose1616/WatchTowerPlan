---
trace_id: trace.internal_project_standards_review_and_hardening
id: prd.internal_project_standards_review_and_hardening
title: Internal Project Standards Review and Hardening PRD
summary: Closes reproduced standards-enforcement drift around external-authority validation
  and document-relative repo-path extraction across governed Markdown sync surfaces.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T17:51:15Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/
- core/python/src/watchtower_core/adapters/markdown.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Internal Project Standards Review and Hardening PRD

## Record Metadata
- `Trace ID`: `trace.internal_project_standards_review_and_hardening`
- `PRD ID`: `prd.internal_project_standards_review_and_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.internal_project_standards_review_and_hardening_direction`
- `Linked Designs`: `design.features.internal_project_standards_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_standards_review_and_hardening`
- `Updated At`: `2026-03-11T17:51:15Z`

## Summary
Closes reproduced standards-enforcement drift around external-authority validation and document-relative repo-path extraction across governed Markdown sync surfaces.

## Problem Statement
The internal standards review reproduced three still-live defects in the governed Markdown enforcement path. First, the standard document-semantics validator does not apply the same external-authority and local-reference rule that `watchtower-core sync standard-index` uses. A standard can therefore pass semantic validation while relying on a raw external URL in `References` without any governed local reference doc, and the validator also does not derive its decision from the same reference-accounting rules that the standard index publishes. Second, the repo-path extractor used by governed sync and citation-audit surfaces ignores document-relative Markdown links because it resolves repo-local references without any source-document context. A governed document can therefore pass semantic validation with valid document-relative links while the derived standard, reference, workflow, foundation, planning, or citation surfaces silently drop those same references. Third, decision-index sync still projects document-relative `Affected Surfaces` values as raw relative strings rather than normalized repository-relative paths, which leaves the decision index semantically valid but operationally inconsistent with the repository-path rules it is supposed to publish.

These gaps weaken the repository's standards posture in different ways. The first makes `watchtower-core validate all` less trustworthy because it is no longer enforcing the same standards authority the derived standard index depends on. The second makes machine-readable indexes and audits incomplete whenever a governed doc uses the document-relative link style that the documentation semantics standard explicitly permits. The third leaves one of those machine-readable indexes publishing non-normalized related paths even after source-aware extraction exists elsewhere. Together they create a fail-open path where authored standards remain valid human documents, but the derived machine layer loses or misinterprets their authority signals.

## Goals
- Make standard semantic validation and standard-index sync apply one shared external-authority rule so both surfaces agree on when governed local reference docs are required.
- Make repo-path extraction used by governed sync and citation-audit surfaces resolve document-relative Markdown links relative to the source document instead of only relative to the repo root.
- Make every governed sync surface that projects related repository paths normalize document-relative authored links to stable repo-relative paths.
- Keep standards, docs, tests, acceptance artifacts, and coordination surfaces aligned in one bounded trace with explicit execution tasks and closeout evidence.
- Return the repository to a green baseline on validation, tests, type checking, and linting after the fixes land.

## Non-Goals
- Redefining the repository's standards posture or relaxing the current requirement to normalize material external authority through governed local reference docs.
- Rewriting the entire Markdown parsing stack or changing the allowed repo-local link styles beyond what the current documentation semantics standard already permits.
- Migrating the existing governed corpus away from repository-absolute links as part of this trace.
- Starting a broader query, routing, or planning-authority review outside the reproduced standards-enforcement defects.

## Requirements
- `req.internal_project_standards_review_and_hardening.001`: This trace must publish a real PRD, accepted direction decision, feature design, implementation plan, updated acceptance contract, refreshed planning-baseline evidence, a closed bootstrap task, and bounded execution tasks for each confirmed standards-review defect.
- `req.internal_project_standards_review_and_hardening.002`: Standard semantic validation and standard-index sync must use the same deterministic rule for external authority and governed local reference docs across `Related Standards and Sources` and `References`.
- `req.internal_project_standards_review_and_hardening.003`: Repo-path extraction used by governed Markdown sync and citation-audit surfaces must resolve repository-absolute, repo-root-relative, and document-relative repo-local links relative to the source document without allowing paths to escape the repository root.
- `req.internal_project_standards_review_and_hardening.004`: Standards, workflow, reference, planning, decision-index, and citation-audit regression coverage must prove the fixes stay aligned, including document-relative link handling and the shared standard-reference rule.
- `req.internal_project_standards_review_and_hardening.005`: The repository must return to a green baseline on `./.venv/bin/watchtower-core validate acceptance --trace-id trace.internal_project_standards_review_and_hardening --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.

## Acceptance Criteria
- `ac.internal_project_standards_review_and_hardening.001`: The trace publishes the full planning chain, the accepted direction decision, the refreshed acceptance contract and planning-baseline evidence, the closed bootstrap task, and two bounded execution tasks covering standard-reference semantics alignment and document-relative repo-path extraction.
- `ac.internal_project_standards_review_and_hardening.002`: Regression coverage proves standard semantic validation and standard-index sync now agree on the governed local-reference requirement for external authority regardless of whether the external URL or local reference doc appears in `Related Standards and Sources` or `References`.
- `ac.internal_project_standards_review_and_hardening.003`: Regression coverage proves document-relative repo-local Markdown links are extracted correctly in the standard, reference, workflow, decision-index, citation-audit, and planning helper paths that feed derived machine-readable surfaces.
- `ac.internal_project_standards_review_and_hardening.004`: The accepted decision, command and standards guidance, and affected runtime helpers describe the shared standards-enforcement behavior accurately enough that future contributors do not reintroduce the split logic.
- `ac.internal_project_standards_review_and_hardening.005`: The repository passes `./.venv/bin/watchtower-core validate acceptance --trace-id trace.internal_project_standards_review_and_hardening --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check` after the trace closes.

## Risks and Dependencies
- The repo-path extraction fix is adapter-level and therefore affects multiple derived families; the change must stay source-aware without weakening the repository-root boundary checks or leaving any remaining raw path-projection call sites behind.
- The standards-reference fix touches both sync and validation layers, so the implementation should remove duplicated logic instead of patching one call path only.
- The trace depends on keeping planning docs, task records, acceptance artifacts, tests, and derived indexes synchronized as the fixes move from planning into execution.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared parsing and standards-enforcement helpers should preserve explicit seams and deterministic behavior rather than leaving correctness to duplicated family logic.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): authored standards remain authoritative, so the machine-readable and validation layers should conform to them instead of silently weakening them.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/data_contracts/decision_index_standard.md
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/workflow_md_standard.md
