---
trace_id: trace.internal_project_standards_review_and_hardening
id: design.features.internal_project_standards_review_and_hardening
title: Internal Project Standards Review and Hardening Feature Design
summary: Defines the technical design boundary for Internal Project Standards Review
  and Hardening.
type: feature_design
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

# Internal Project Standards Review and Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.internal_project_standards_review_and_hardening`
- `Design ID`: `design.features.internal_project_standards_review_and_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.internal_project_standards_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_standards_review_and_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.internal_project_standards_review_and_hardening`
- `Updated At`: `2026-03-11T17:51:15Z`

## Summary
Defines the technical design boundary for Internal Project Standards Review and Hardening.

## Source Request
- Please do another internal standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle, and continue until every issue is identified, fixed, validated, and committed.
- Reproduced defect: standard semantic validation and standard-index sync do not agree on when a governed local reference doc is required for external authority.
- Reproduced defect: valid document-relative repo-local Markdown links are accepted by semantic validation but dropped by derived sync and citation-audit extraction paths.
- Reproduced defect: decision-index sync leaves document-relative `Affected Surfaces` projected as raw relative strings instead of governed repo-relative paths.

## Scope and Feature Boundary
- Covers the adapter-level repo-path normalization and extraction logic used by governed Markdown sync and citation-audit surfaces.
- Covers the standard semantic-validation and standard-index sync rule that derives internal references, local reference docs, and external-authority requirements from standards documents.
- Covers the tests, planning artifacts, and companion docs needed to keep standards, workflows, references, and planning helpers aligned after the fix.
- Does not redesign the broader Markdown parser or replace the repository's current link-authoring conventions.
- Does not weaken the standards requirement to cite governed local reference docs when external authority materially shapes a standard.

## Current-State Context
- `DocumentSemanticsValidationService._validate_standard_document()` evaluates external authority by inspecting raw external URLs in `Related Standards and Sources` and internal repo-path references in `References`, which means it does not derive the same answer the standard-index sync path derives from the full standards source sections.
- `StandardIndexSyncService` and the broader citation-audit helpers rely on `extract_repo_path_references()`, but that adapter only normalizes absolute and repo-root-relative references because it has no source-document context for document-relative links.
- Governed semantic validation already supports document-relative Markdown links through `_resolve_repo_local_markdown_link_target()`, so the live repository rule is broader than the derived extraction path used by standards, references, workflows, and planning helpers.
- `DecisionIndexSyncService` still derives `related_paths` from raw path-like extraction in `Affected Surfaces`, so even after source-aware link validation a decision can publish `../../templates/` instead of `docs/templates/` in the machine-readable index.
- The result is an inconsistent enforcement boundary where human-valid governed docs can project incomplete machine-readable reference lineage.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared parsing and reference-accounting helpers should stay composable and deterministic rather than re-encoding the same rule in multiple families.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): fail-closed repository governance requires validation and derived indexes to apply the same authored standards contract.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): standards documents must preserve the local-reference rule for external authority and allow repository-absolute or document-relative repo-local links.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the derived standard index must audit applied references and external-authority usage accurately enough to stay aligned with the governed standards corpus.
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md): decision index related paths must stay normalized to repository-relative paths even when authored through document-relative links.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): repo-local Markdown links may use repository-absolute or document-relative targets, so derived extraction cannot silently ignore the latter.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): governed local reference docs are the repository-normalized bridge for external authority and therefore need consistent capture in both sync and validation layers.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow additional-load and related-reference extraction should honor the same repo-local link semantics as the rest of the governed Markdown corpus.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): planning, sync, tests, and acceptance artifacts must move in one traced change set.

## Design Goals and Constraints
- Remove the duplicated standard-reference decision logic that allowed semantic validation to drift from standard-index sync.
- Make repo-path extraction source-aware without allowing path resolution to escape the current repository root.
- Preserve support for repository-absolute links, repo-root-relative links, and document-relative links under one adapter contract.
- Keep the fix centralized in helpers and call-site updates instead of scattering family-specific patches across standards, decisions, references, workflows, and planning services.
- Preserve current behavior for invalid or missing repo-local targets: semantic validation should still fail closed when the link target does not exist.

## Options Considered
### Option 1
- Patch only the standard semantic validator and leave the existing repo-path extractor unchanged.
- Strength: smallest code delta in the reproduced standard-validation path.
- Tradeoff: document-relative links would remain invisible in derived indexes and audits outside the standard validator.

### Option 2
- Add source-aware repo-path extraction in the Markdown adapter, route all affected sync and planning helpers through that shared behavior, and centralize standard reference accounting so sync and validation share the same rule.
- Strength: closes both reproduced defects at their shared seams and reduces the chance of future drift.
- Tradeoff: touches multiple call sites and regression suites because the adapter contract becomes richer.

### Option 3
- Tighten the standards posture to require repository-absolute links only and document that document-relative links are unsupported in derived machine-readable surfaces.
- Strength: avoids changing adapter signatures.
- Tradeoff: directly conflicts with the current documentation semantics standard and would force a policy rollback instead of fixing the implementation defect.

## Recommended Design
### Architecture
- Extend `normalize_repo_path_reference()` and `extract_repo_path_references()` so callers can provide the source Markdown path and obtain one normalized repo-relative target whether the authored link is repository-absolute, repo-root-relative, or document-relative.
- Update governed sync, citation-audit, workflow, decision-index, and planning helper call sites to pass the source document path whenever repo-path extraction comes from authored Markdown.
- Move the standard reference-accounting logic into `watchtower_core.repo_ops.standards` so standard semantic validation and standard-index sync both derive internal reference paths, applied reference paths, local reference docs, and external-authority flags from the same helper.
- Keep document semantics as the fail-closed path for missing repo-local Markdown targets while derived sync uses the same source-aware normalization for machine-readable reference lineage.

### Data and Interface Impacts
- `core/python/src/watchtower_core/adapters/markdown.py` gains a source-aware repo-path normalization contract.
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py` and `core/python/src/watchtower_core/repo_ops/sync/standard_index.py` consume shared standard-reference helpers instead of locally duplicating the rule.
- `core/python/src/watchtower_core/repo_ops/planning_documents.py`, `core/python/src/watchtower_core/repo_ops/sync/decision_index.py`, `core/python/src/watchtower_core/repo_ops/sync/reference_index.py`, `core/python/src/watchtower_core/repo_ops/sync/foundation_index.py`, and `core/python/src/watchtower_core/repo_ops/sync/workflow_index.py` pass source-document paths into repo-path extraction.
- Derived machine-readable artifacts and query surfaces remain structurally stable; the change is in correctness of populated reference fields and the semantic validator's enforcement fidelity.

### Execution Flow
1. Rewrite the planning chain around the reproduced defects and split execution into a standards-reference-alignment task and a document-relative extraction task.
2. Implement source-aware repo-path extraction in the Markdown adapter and propagate the new contract through the affected sync, workflow, decision-index, planning, and citation-audit call sites.
3. Centralize standard reference accounting and update standard semantic validation plus standard-index sync to consume the same helper.
4. Add regression coverage for the reproduced failures, rerun the full repository validation stack, and close the trace with refreshed derived planning surfaces.

### Invariants and Failure Cases
- Repo-path extraction must never normalize a target outside the current repository root.
- A missing repo-local Markdown link target must still fail semantic validation with a concrete path-level error.
- A standard that cites raw external authority without any governed local reference doc must fail both semantic validation and standard-index sync.
- A standard, decision record, workflow, or reference doc that uses valid document-relative repo-local links must populate the same normalized repo-relative paths in derived machine-readable surfaces that a repository-absolute link would have produced.

## Affected Surfaces
- `docs/standards/`
- `core/python/src/watchtower_core/adapters/markdown.py`
- `core/python/src/watchtower_core/repo_ops/standards.py`
- `core/python/src/watchtower_core/repo_ops/planning_documents.py`
- `core/python/src/watchtower_core/repo_ops/sync/decision_index.py`
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/reference_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/foundation_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/workflow_index.py`
- `core/python/tests/`

## Design Guardrails
- Do not weaken the documented support for document-relative repo-local links to avoid fixing derived extraction.
- Do not duplicate the standard external-authority rule in separate sync and validation implementations again.
- Do not change schema shapes or query payloads unless the fix actually requires a contract change; prefer correctness of existing derived fields.

## Risks
- The adapter-level change can affect multiple derived families at once, so regression coverage needs to prove each affected call path still emits normalized repo-relative references and that no remaining raw path extractors are feeding machine-readable indexes.
- Centralizing standard reference accounting must preserve the existing applied-reference semantics used by the standard index, not just the external-authority check.
- The planning and coordination surfaces will churn because the trace moves from bootstrap to explicit execution tasks before implementation begins.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/data_contracts/decision_index_standard.md
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/workflow_md_standard.md
