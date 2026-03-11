---
trace_id: trace.reference_and_workflow_standards_alignment
id: design.implementation.reference_and_workflow_standards_alignment
title: Reference and Workflow Standards Alignment Implementation Plan
summary: Breaks the reference-authoring and workflow-additional-load contract
  alignment work into a bounded implementation slice.
type: implementation_plan
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

# Reference and Workflow Standards Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.reference_and_workflow_standards_alignment`
- `Plan ID`: `design.implementation.reference_and_workflow_standards_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.reference_and_workflow_standards_alignment`
- `Linked Decisions`: `decision.reference_and_workflow_standards_alignment_direction`
- `Source Designs`: `design.features.reference_and_workflow_standards_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-11T23:19:00Z`

## Summary
Breaks the reference-authoring and workflow-additional-load contract alignment
work into a bounded implementation slice.

## Source Request or Design
- Another expansive internal standards review exposed live drift between reference/workflow standards and the code paths that validate and index those governed Markdown families.

## Scope Summary
- Update the reference standard and template, tighten workflow additional-load
  validation, and add targeted regression coverage plus traced closeout
  artifacts.
- Exclude unrelated workflow-routing policy work, schema changes, or command
  behavior changes that were not reproduced in this review.

## Assumptions and Constraints
- `Canonical Upstream` is already required by the governed reference validator
  and the reference-index data contract, so the least-risk fix is to align the
  prose contract rather than weaken the machine contract.
- Workflow additional-load parsing should remain deterministic from one
  bullet-to-one-path semantics and should only tighten around the missing
  generic baseline surface.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/reference_md_standard.md`: the implementation
  must leave authoring guidance aligned with the live reference validator and
  index expectations.
- `docs/standards/documentation/workflow_md_standard.md`: the workflow change
  must reject only the generic standard surfaces that the prose contract
  already says to keep implicit.

## Proposed Technical Approach
- Update the reference standard and template together, plus integration checks
  that guard required reference-template sections and optional-section
  guidance.
- Extend the workflow additional-load routing-baseline disallow set and the
  matching unit and integration tests so generic workflow standards are
  rejected consistently.
- Rewrite the acceptance contract and planning-baseline evidence around the
  actual findings, then refresh derived planning and control-plane surfaces.

## Work Breakdown
1. Close the bootstrap task and publish concrete PRD, design, implementation,
   decision, and execution-task artifacts for the confirmed issue set.
2. Align the reference authoring standard, template, and regression coverage
   with the already-enforced canonical-upstream contract.
3. Tighten workflow additional-load enforcement and regression coverage around
   generic workflow standards, including
   `routing_and_context_loading_standard.md`.
4. Refresh derived planning and index surfaces, rerun the full validation
   baseline, and close the trace with acceptance evidence.

## Risks
- The stricter reference prose contract may require slightly clearer family
  boundary language so contributors do not misuse `docs/references/**` for
  repo-native-only topics.

## Validation Plan
- Run targeted regressions for reference document semantics, workflow index
  sync, and control-plane artifact alignment.
- Run `./.venv/bin/watchtower-core sync all --write --format json`,
  `./.venv/bin/watchtower-core validate acceptance --trace-id
  trace.reference_and_workflow_standards_alignment --format json`,
  `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest
  -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and
  `./.venv/bin/ruff check .`.

## References
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/data_contracts/workflow_index_standard.md
