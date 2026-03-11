---
trace_id: trace.internal_project_standards_review_and_hardening
id: decision.internal_project_standards_review_and_hardening_direction
title: Internal Project Standards Review and Hardening Direction Decision
summary: Records the accepted direction for Internal Project Standards Review and
  Hardening.
type: decision_record
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

# Internal Project Standards Review and Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.internal_project_standards_review_and_hardening`
- `Decision ID`: `decision.internal_project_standards_review_and_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.internal_project_standards_review_and_hardening`
- `Linked Designs`: `design.features.internal_project_standards_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_standards_review_and_hardening`
- `Updated At`: `2026-03-11T17:51:15Z`

## Summary
Records the accepted direction for Internal Project Standards Review and Hardening.

## Decision Statement
Keep the current standards strict, fix repo-path extraction centrally in the Markdown adapter so document-relative repo-local links are normalized with source-document context across every governed sync surface, and centralize standard reference accounting so standard semantic validation and standard-index sync consume the same external-authority rule.

## Trigger or Source Request
- Please do another internal standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle, and continue until every issue is identified, fixed, validated, and committed.
- Reproduced defect: standard semantic validation allows a standard to rely on raw external authority in `References` without any governed local reference doc, even though standard-index sync treats that condition as invalid.
- Reproduced defect: valid document-relative repo-local Markdown links pass semantic validation but are dropped from derived sync and citation-audit surfaces because repo-path extraction lacks source-document context.
- Reproduced defect: decision-index sync still projects document-relative `Affected Surfaces` as raw relative strings instead of repository-relative paths.

## Current Context and Constraints
- The documentation semantics standard already allows repository-absolute and document-relative repo-local Markdown links, so this trace should fix the derived extraction path instead of narrowing the documented authoring contract.
- The standard index remains a derived audit surface, which means validation and sync need to agree on the same standard-reference rule or the machine-readable layer becomes untrustworthy.
- The affected repo-path extraction helper is reused by multiple governed families, and decision-index sync still had a raw `Affected Surfaces` projection path, so a standards-only patch would leave other derived surfaces inconsistent.

## Applied References and Implications
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the repository already requires standards to normalize material external authority through governed local references and explicitly permits document-relative repo-local links.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the standard index must publish accurate applied-reference and external-authority data, which depends on consistent reference accounting and path extraction.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): semantic validation is already the fail-closed path for repo-local link integrity, so derived extraction should reuse the same link semantics rather than silently narrowing them.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): governed local reference docs are the canonical bridge to external authority and should be recognized consistently no matter which standards source section cites them.
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md): decision related paths should be published as repository-relative paths rather than raw authored relative strings.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow additional-load extraction needs the same repo-local link resolution behavior as the rest of the governed Markdown corpus.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared adapter and standards helpers should be the seam for correctness, not duplicated family-specific logic.

## Affected Surfaces
- `docs/standards/`
- `core/python/src/watchtower_core/adapters/markdown.py`
- `core/python/src/watchtower_core/repo_ops/standards.py`
- `core/python/src/watchtower_core/repo_ops/planning_documents.py`
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `core/python/src/watchtower_core/repo_ops/sync/decision_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/standard_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/reference_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/foundation_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/workflow_index.py`
- `core/python/tests/`

## Options Considered
### Option 1
- Patch only the standard semantic validator and leave repo-path extraction unchanged.
- Strength: smallest local code change in the first reproduced defect.
- Tradeoff: document-relative references would remain invisible or raw in derived indexes, workflow metadata, planning helpers, and citation audits.

### Option 2
- Centralize source-aware repo-path extraction in the Markdown adapter, update the affected sync and planning call sites, and centralize standard reference accounting in one helper consumed by both validation and sync.
- Strength: closes both reproduced defects at the shared seam and makes future drift less likely.
- Tradeoff: touches multiple call sites and requires broader regression coverage.

### Option 3
- Narrow the standards posture to support only repository-absolute repo-local links and tolerate the current split between sync and semantic validation.
- Strength: avoids changing adapter signatures.
- Tradeoff: contradicts the current standards and accepts a weaker machine-readable governance contract.

## Chosen Outcome
Adopt option 2. The repository should keep the current standards contract, make repo-path extraction source-aware in one shared adapter helper, apply it to every governed path-projection call site including decision-index `Affected Surfaces`, and make standard semantic validation plus standard-index sync consume the same standard-reference accounting helper.

## Rationale and Tradeoffs
- The reproduced failures both come from duplicated or incomplete helper behavior, so shared helpers are the right correction seam.
- Relaxing the standards would paper over the defect and would invalidate the current documentation semantics and standard-index contracts.
- Updating the adapter contract is broader than a one-off patch, but it yields a durable fix across standards, decisions, references, workflows, and planning-derived surfaces.

## Consequences and Follow-Up Impacts
- Multiple sync and planning call sites need to pass source-document context into repo-path extraction.
- Regression coverage needs to prove document-relative references populate normalized repo-relative paths in derived surfaces, including decision-index `related_paths`, and that standard semantic validation now fails on the same invalid external-authority condition as standard-index sync.
- The trace should close only after the bootstrap task and the two bounded execution tasks are all marked done and the final evidence records the green repository baseline.

## Risks, Dependencies, and Assumptions
- The adapter change assumes callers can provide source-document paths wherever governed Markdown is being parsed for derived reference extraction.
- The shared standard-reference helper must preserve the difference between all cited references and the subset of applied references already modeled by the standard index.
- Final planning closeout depends on the derived coordination slice returning to zero open tasks once the fixes and validations are complete.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/data_contracts/decision_index_standard.md
- docs/standards/documentation/workflow_md_standard.md
