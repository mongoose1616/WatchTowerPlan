---
trace_id: trace.planning_semantics_and_decision_contract_alignment
id: prd.planning_semantics_and_decision_contract_alignment
title: Planning Semantics and Decision Contract Alignment PRD
summary: Align decision-record standards and templates with the enforced governed
  contract and extend shared document-semantics enforcement across governed planning
  documents.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T20:31:23Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/decision_record_template.md
- docs/templates/feature_design_template.md
- docs/templates/implementation_plan_template.md
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
---

# Planning Semantics and Decision Contract Alignment PRD

## Record Metadata
- `Trace ID`: `trace.planning_semantics_and_decision_contract_alignment`
- `PRD ID`: `prd.planning_semantics_and_decision_contract_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.planning_semantics_and_decision_contract_alignment_direction`
- `Linked Designs`: `design.features.planning_semantics_and_decision_contract_alignment`
- `Linked Implementation Plans`: `design.implementation.planning_semantics_and_decision_contract_alignment`
- `Updated At`: `2026-03-11T20:31:23Z`

## Summary
Align decision-record standards and templates with the enforced governed contract
and extend shared document-semantics enforcement across governed planning
documents.

## Problem Statement
The follow-up standards review reproduced three still-live contract gaps. First,
the repository's decision-record code, scaffolds, and tests already require
`Applied References and Implications`, but the governing decision-record
standard and template still publish that section as optional authoring guidance.
Second, feature-design and implementation-plan scaffolds plus the live design-doc
corpus always publish applied-reference sections, while their standards and
templates still describe those sections as optional and validators do not reject
their omission. Third, the shared documentation-semantics rule that headings
must be separated from the preceding list by a blank line is only enforced on a
subset of document families, so governed planning docs and workflow modules can
violate the published standard without failing validation or derived sync
surfaces consistently.

## Goals
- Restore one consistent planning authoring contract across decision records,
  feature designs, and implementation plans so standards, templates, scaffolds,
  validation, and derived indexes agree.
- Enforce the shared heading-separation semantics rule across governed planning
  documents and workflow modules through shared code paths instead of
  family-local special cases.
- Add regression coverage and traced evidence so the same drift does not recur.

## Non-Goals
- Introduce new Markdown-semantic rules beyond the already-published blank-line
  heading separation guardrail.
- Redesign the broader decision-record information model beyond aligning the
  already-enforced required section contract.

## Requirements
- `req.planning_semantics_and_decision_contract_alignment.001`: The governing
  decision-record, feature-design, and implementation-plan documentation
  surfaces must require the applied-reference sections that live scaffolds,
  corpus rules, or repository validation already depend on, and must stop
  telling authors those sections are optional.
- `req.planning_semantics_and_decision_contract_alignment.002`: Shared
  heading-after-list blank-line semantics must fail closed for governed PRDs,
  decision records, feature designs, implementation plans, standards,
  references, foundations, and workflow modules.
- `req.planning_semantics_and_decision_contract_alignment.003`: Regression
  coverage must exercise both the authoring-contract alignment and the shared
  semantics enforcement paths, including derived sync behavior where the same
  loaders are reused.

## Acceptance Criteria
- `ac.planning_semantics_and_decision_contract_alignment.001`: The
  trace publishes the full planning chain, accepted direction decision, and
  bounded task set for the completed standards-review slice.
- `ac.planning_semantics_and_decision_contract_alignment.002`:
  The decision-record standard and template publish
  `Applied References and Implications` as a required section, and regression
  checks fail if that decision-record authoring contract becomes optional again.
- `ac.planning_semantics_and_decision_contract_alignment.003`: The
  feature-design and implementation-plan standards and templates publish the
  live required applied-reference sections, and validators reject their
  omission.
- `ac.planning_semantics_and_decision_contract_alignment.004`:
  `watchtower-core validate document-semantics` rejects governed planning
  documents and workflow modules whose headings immediately follow list blocks
  without a blank separator line.
- `ac.planning_semantics_and_decision_contract_alignment.005`: The derived sync
  loaders used by planning and workflow indexes also reject the same invalid
  heading pattern, and the repository baseline revalidates cleanly after the
  fix.

## Risks and Dependencies
- Tightening shared Markdown semantics can expose existing authored documents
  that were previously accepted silently; the change must land with enough
  targeted coverage to localize failures quickly.
- The remediation depends on keeping standards, templates, validators, sync
  loaders, and traced planning artifacts aligned in one change set.

## References
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/standards/governance/decision_capture_standard.md
- docs/planning/prds/internal_project_code_review_follow_up.md
