---
trace_id: trace.reference_and_workflow_standards_alignment
id: decision.reference_and_workflow_standards_alignment_direction
title: Reference and Workflow Standards Alignment Direction Decision
summary: Records the accepted direction for converging reference authoring
  rules and workflow additional-load enforcement.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-11T23:19:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
---

# Reference and Workflow Standards Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.reference_and_workflow_standards_alignment`
- `Decision ID`: `decision.reference_and_workflow_standards_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.reference_and_workflow_standards_alignment`
- `Linked Designs`: `design.features.reference_and_workflow_standards_alignment`
- `Linked Implementation Plans`: `design.implementation.reference_and_workflow_standards_alignment`
- `Updated At`: `2026-03-11T23:19:00Z`

## Summary
Records the accepted direction for converging reference authoring rules and
workflow additional-load enforcement.

## Decision Statement
Treat `Canonical Upstream` as a required governed reference-doc section and
reject generic workflow standards, including
`routing_and_context_loading_standard.md`, in workflow
`Additional Files to Load`.

## Trigger or Source Request
- Another expansive internal standards review exposed live drift between reference/workflow standards and the code paths that validate and index those governed Markdown families.

## Current Context and Constraints
- Governed reference validation and reference-index sync already require
  `Canonical Upstream`, and the reference-index standard already treats
  canonical upstream URLs as required machine-readable data.
- The reference standard and template still describe `Canonical Upstream` as
  optional, so current authoring guidance is weaker than live enforcement.
- The workflow Markdown standard already says generic workflow standards must
  stay implicit, but the workflow additional-load disallow list omits
  `routing_and_context_loading_standard.md`.

## Applied References and Implications
- `docs/standards/documentation/reference_md_standard.md`: the governed prose
  contract must match the stricter live reference validator and index behavior
  instead of advertising an optional upstream-authority section.
- `docs/standards/data_contracts/reference_index_standard.md`: reference-index
  entries already require canonical upstream URLs, so weakening the machine
  contract would expand scope beyond this review.
- `docs/standards/documentation/workflow_md_standard.md`: generic workflow
  standards must stay implicit, so workflow validation and sync should reject
  them wherever `Additional Files to Load` is parsed.

## Affected Surfaces
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/data_contracts/workflow_index_standard.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_workflow_index_sync.py

## Options Considered
### Option 1
- Relax the reference validator and index contract to match the current
  optional prose guidance, and leave the workflow disallow list unchanged.
- Strength: smaller short-term change set.
- Tradeoff: weakens the governed reference family boundary and leaves workflow
  additional-load enforcement inconsistent with its own published standard.

### Option 2
- Align the reference prose contract to the already-enforced machine contract
  and extend the workflow disallow set to cover the missing generic workflow
  standard.
- Strength: standards, templates, validators, sync, and review checks converge
  without changing schemas or command behavior.
- Tradeoff: more surfaces update together, including regression coverage and
  traced closeout artifacts.

## Chosen Outcome
Choose option 2 and land the prose, validation, sync, and regression updates in
one traced slice.

## Rationale and Tradeoffs
- The machine-readable reference contract and reference validator already agree
  on requiring canonical upstream authority, so aligning the weaker prose
  guidance is lower risk than weakening the governed family boundary.
- Workflow additional-load fields are intended for task-specific context; if a
  generic workflow standard is allowed through the validator, the workflow index
  can publish baseline governance as if it were task-specific.

## Consequences and Follow-Up Impacts
- Governed reference authoring guidance becomes stricter and must stay aligned
  with regression checks.
- Workflow additional-load validation becomes stricter for the missing generic
  baseline surface but should not affect legitimate task-specific extra files.

## Risks, Dependencies, and Assumptions
- The reference-family boundary needs explicit wording so contributors do not
  interpret the stricter guidance as a ban on repo-native lookup docs in other
  families.
- The workflow fix assumes `routing_and_context_loading_standard.md` is part of
  the generic routing baseline rather than task-specific load context.

## References
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/data_contracts/workflow_index_standard.md
