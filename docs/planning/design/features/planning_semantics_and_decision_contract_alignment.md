---
trace_id: trace.planning_semantics_and_decision_contract_alignment
id: design.features.planning_semantics_and_decision_contract_alignment
title: Planning Semantics and Decision Contract Alignment Feature Design
summary: Defines the technical design boundary for converging decision-record
  authoring rules and shared Markdown semantics enforcement.
type: feature_design
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

# Planning Semantics and Decision Contract Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.planning_semantics_and_decision_contract_alignment`
- `Design ID`: `design.features.planning_semantics_and_decision_contract_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.planning_semantics_and_decision_contract_alignment`
- `Linked Decisions`: `decision.planning_semantics_and_decision_contract_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.planning_semantics_and_decision_contract_alignment`
- `Updated At`: `2026-03-11T20:31:23Z`

## Summary
Defines the technical design boundary for converging decision-record authoring
rules and shared Markdown semantics enforcement.

## Source Request
- Follow-up internal standards review exposed live decision-record contract drift
  and missing shared planning-document semantics enforcement.

## Scope and Feature Boundary
- Align the decision-record standard and template with the already-enforced
  `Applied References and Implications` requirement.
- Introduce one shared heading-separation validation helper and wire it through
  governed planning, workflow, and companion sync or index paths that parse
  authored Markdown.
- Exclude new semantic rules, unrelated template refreshes, or document-family
  restructures beyond the reproduced contract gaps.

## Current-State Context
- `core/python/src/watchtower_core/repo_ops/planning_documents.py` requires
  `Applied References and Implications` for decision records, so planning sync
  and semantic validation already reject decision docs that omit it.
- `docs/standards/documentation/decision_record_md_standard.md` and
  `docs/templates/decision_record_template.md` still describe that same section
  as optional, which misleads new authored documents even though the live repo
  contract is stricter.
- Feature-design and implementation-plan scaffolds plus the live design-doc
  corpus already publish applied-reference sections consistently, but their
  standards and templates still describe those sections as optional and
  validators do not fail when they are omitted.
- The blank-line heading-separation rule currently lives in a validator-local
  path used for standards, references, and foundations, but governed planning
  documents and workflow modules bypass it through different loaders.

## Foundations References Applied
- `docs/foundations/repository_standards_posture.md`: governed human-readable
  contracts and their derived machine-readable or validation surfaces should stay
  aligned instead of publishing stale authoring guidance.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/decision_record_md_standard.md`: the authored
  standard must agree with the enforced decision-record shape and authoring
  template.
- `docs/standards/documentation/feature_design_md_standard.md`: the
  feature-design standard and template must match the live applied-reference
  contract already reflected in scaffolds and corpus checks.
- `docs/standards/documentation/implementation_plan_md_standard.md`: the
  implementation-plan standard and template must match the live
  applied-reference contract already reflected in scaffolds and corpus checks.
- `docs/standards/documentation/documentation_semantics_standard.md`: shared
  Markdown-semantic rules must not weaken across governed document families or
  workflows.

## Design Goals and Constraints
- Preserve one fail-closed authoring contract for decision records across docs,
  scaffolds, validation, and derived indexes.
- Reuse one shared heading-separation implementation path instead of copying the
  same rule into more family-specific validators.
- Avoid changing the actual semantic rule; the change is about consistent
  enforcement, not expanding scope.

## Options Considered
### Option 1
- Relax code and tests to match the stale decision-record docs and keep the
  heading-separation rule family-specific.
- Strength: smaller implementation change.
- Tradeoff: weakens the live contract, drops applied-reference expectations from
  decision records, and leaves the shared semantics standard only partially
  true.

### Option 2
- Align the decision-record docs to the live contract and centralize the
  design-doc authoring contracts plus the heading-separation rule in shared
  Markdown-semantic helpers used by planning and workflow loaders.
- Strength: standards, templates, validation, sync, and scaffolds all converge
  on one contract.
- Tradeoff: more surfaces must update together, including regression tests and
  traced planning artifacts.

## Recommended Design
### Architecture
- Publish a shared Markdown heading-separation helper under `repo_ops` and make
  governed Markdown loaders call it before section-order and metadata-specific
  validation.
- Keep repo-local link validation in the document-semantics service, but move
  the heading-separation rule into the shared loader path so workflow and
  planning index builders fail closed on the same invalid authored shape.
- Align the decision-record standard, template, and close-to-source regression
  checks with the already-governed required applied-reference section.

### Data and Interface Impacts
- `docs/standards/documentation/decision_record_md_standard.md` and
  `docs/templates/decision_record_template.md` change their required-section
  contract.
- `docs/standards/documentation/feature_design_md_standard.md`,
  `docs/templates/feature_design_template.md`,
  `docs/standards/documentation/implementation_plan_md_standard.md`, and
  `docs/templates/implementation_plan_template.md` change their required
  applied-reference contract.
- `docs/standards/documentation/documentation_semantics_standard.md` publishes
  the broader operational surface set for the shared helper.
- Shared loader and sync modules reject a previously accepted invalid Markdown
  shape, but no CLI flags or artifact schemas change.

### Execution Flow
1. Update the decision-record, feature-design, and implementation-plan
   standards and templates so required sections and optional guidance match the
   live contract.
2. Introduce a shared heading-separation helper and wire it through governed
   planning, workflow, standard, reference, and foundation parsing paths.
3. Add targeted regressions for authoring-contract alignment and for validation
   or sync rejection of the invalid heading pattern.

### Invariants and Failure Cases
- Decision records must continue to publish explained
  `Applied References and Implications` bullets instead of bare links or omitted
  sections.
- Any governed document or workflow module with a heading immediately following
  a list block must fail through the same shared helper regardless of family.

## Affected Surfaces
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/decision_record_template.md
- docs/templates/feature_design_template.md
- docs/templates/implementation_plan_template.md
- core/python/src/watchtower_core/repo_ops/markdown_semantics.py
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/decision_index.py
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/standard_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_decision_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_workflow_index_sync.py

## Design Guardrails
- Keep the shared helper narrow: it should enforce only the published
  heading-after-list blank-line rule and not accumulate unrelated Markdown style
  checks.
- Preserve the existing decision-record data model and IDs; the change is
  contract alignment, not a new planning artifact shape.

## Risks
- Existing authored docs could start failing sync or validation if they already
  violate the shared rule; the slice must land with enough targeted evidence to
  identify any fallout quickly.

## References
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/standards/governance/decision_capture_standard.md
- core/python/src/watchtower_core/repo_ops/planning_documents.py
