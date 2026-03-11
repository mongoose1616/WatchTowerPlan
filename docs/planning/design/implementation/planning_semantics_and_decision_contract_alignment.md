---
trace_id: trace.planning_semantics_and_decision_contract_alignment
id: design.implementation.planning_semantics_and_decision_contract_alignment
title: Planning Semantics and Decision Contract Alignment Implementation Plan
summary: Breaks the shared Markdown semantics and decision-record contract
  alignment work into a bounded implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T20:31:23Z'
audience: shared
authority: supporting
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

# Planning Semantics and Decision Contract Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.planning_semantics_and_decision_contract_alignment`
- `Plan ID`: `design.implementation.planning_semantics_and_decision_contract_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.planning_semantics_and_decision_contract_alignment`
- `Linked Decisions`: `decision.planning_semantics_and_decision_contract_alignment_direction`
- `Source Designs`: `design.features.planning_semantics_and_decision_contract_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-11T20:31:23Z`

## Summary
Breaks the shared Markdown semantics and decision-record contract alignment work
into a bounded implementation slice.

## Source Request or Design
- Follow-up internal standards review exposed live decision-record contract drift
  and missing shared planning-document semantics enforcement.

## Scope Summary
- Update the decision-record standard and template, introduce shared
  heading-separation validation helpers, and add focused regression coverage.
- Exclude unrelated workflow or planning-contract changes that were not
  reproduced in this standards review.

## Assumptions and Constraints
- The repository already treats `Applied References and Implications` as
  required in decision-record validation, scaffolding, and index construction.
- Shared Markdown-semantic enforcement should stay reusable across validation
  and sync loaders without duplicating family-local logic.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/decision_record_md_standard.md`: the code
  change must leave the authoring contract stricter only where the standard now
  says so.
- `docs/standards/documentation/documentation_semantics_standard.md`: the
  helper wiring must make the published shared rule true for governed docs and
  workflows.

## Proposed Technical Approach
- Add a small shared helper module for the heading-after-list blank-line rule,
  then call it from governed planning loaders and workflow, standard, reference,
  and foundation sync paths.
- Update the decision-record standard and template together, plus the
  documentation semantics standard's operationalization and regression checks
  that guard these contracts.

## Work Breakdown
1. Rewrite the traced PRD, design, implementation plan, decision, and task set
   so the reproduced defects and recommended direction are explicit.
2. Update the decision-record standard and template to require
   `Applied References and Implications`, then add regression coverage for the
   authoring contract.
3. Introduce the shared heading-separation helper, wire it through governed
   planning and workflow parsing paths, and add validation or sync regressions
   for planning docs and workflow modules.
4. Refresh derived planning and control-plane surfaces, rerun the repository
   validation stack, and close the trace with acceptance evidence.

## Risks
- Tightened shared semantics can surface existing invalid authored Markdown in
  unrelated files during full validation.

## Validation Plan
- Run targeted unit coverage for document semantics, decision index sync,
  workflow index sync, and control-plane artifact alignment.
- Run repository validation and quality gates: `watchtower-core sync all --write
  --format json`, `watchtower-core validate acceptance --trace-id
  trace.planning_semantics_and_decision_contract_alignment --format json`,
  `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy
  src`, and `ruff check`.

## References
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/templates/decision_record_template.md
- core/python/src/watchtower_core/repo_ops/planning_documents.py
