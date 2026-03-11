---
trace_id: trace.planning_semantics_and_decision_contract_alignment
id: decision.planning_semantics_and_decision_contract_alignment_direction
title: Planning Semantics and Decision Contract Alignment Direction Decision
summary: Records the accepted direction for converging decision-record authoring
  rules and shared Markdown semantics enforcement.
type: decision_record
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

# Planning Semantics and Decision Contract Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_semantics_and_decision_contract_alignment`
- `Decision ID`: `decision.planning_semantics_and_decision_contract_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_semantics_and_decision_contract_alignment`
- `Linked Designs`: `design.features.planning_semantics_and_decision_contract_alignment`
- `Linked Implementation Plans`: `design.implementation.planning_semantics_and_decision_contract_alignment`
- `Updated At`: `2026-03-11T20:31:23Z`

## Summary
Records the accepted direction for converging decision-record authoring rules and
shared Markdown semantics enforcement.

## Decision Statement
Treat `Applied References and Implications` as a required decision-record
section, and enforce the shared heading-after-list blank-line rule through
common Markdown semantics helpers used by governed planning and workflow parsing
paths.

## Trigger or Source Request
- Follow-up internal standards review exposed live decision-record contract drift
  and missing shared planning-document semantics enforcement.

## Current Context and Constraints
- Decision-record scaffolds, document semantics, and decision-index sync already
  require `Applied References and Implications`, so the live repo contract is
  stricter than the current decision-record standard and template.
- Feature-design and implementation-plan scaffolds plus the live design-doc
  corpus already publish applied-reference sections consistently, so leaving
  their standards and templates optional preserves avoidable authoring drift.
- The shared heading-separation rule currently lives in a validator-local path,
  which means governed planning docs and workflow modules can bypass the
  published documentation-semantics standard.

## Applied References and Implications
- `docs/standards/documentation/decision_record_md_standard.md`: the governing
  authoring rule must match the already-enforced decision-record structure
  rather than advertising an optional section that the repo rejects.
- `docs/standards/documentation/feature_design_md_standard.md`: planning
  authoring contracts should match the live scaffolded and corpus-enforced
  applied-reference sections instead of leaving them optional.
- `docs/standards/documentation/implementation_plan_md_standard.md`: planning
  authoring contracts should match the live scaffolded and corpus-enforced
  applied-reference sections instead of leaving them optional.
- `docs/standards/documentation/documentation_semantics_standard.md`: shared
  document-semantic guardrails should hold across governed document families and
  workflow modules without family-specific weakening.

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

## Options Considered
### Option 1
- Relax repository enforcement so the stale decision-record standard and
  template remain technically correct, and keep blank-line heading checks
  family-specific.
- Strength: smaller short-term implementation delta.
- Tradeoff: weakens decision-record rationale capture and leaves the published
  cross-family semantics standard partially unenforced.

### Option 2
- Align the decision-record docs with the live required-section contract and
  move heading-separation enforcement into shared governed Markdown parsing
  helpers.
- Strength: standards, templates, validation, scaffolds, sync, and indexes all
  converge on one contract.
- Tradeoff: more code paths and regression surfaces change together.

## Chosen Outcome
Choose option 2 and land the standards, template, helper, loader, and
regression updates in one traced slice.

## Rationale and Tradeoffs
- The repository already depends on explicit applied-reference capture in
  decision records, so weakening that contract would discard useful traceable
  rationale just to preserve stale documentation.
- Shared Markdown semantics belong in shared parsing helpers because
  validation-only enforcement still leaves sync and index paths free to accept
  invalid authored input.

## Consequences and Follow-Up Impacts
- The decision-record standard and template will become stricter and must stay
  aligned with tests.
- Shared loader and sync code will reject a previously silent invalid heading
  pattern across governed planning docs and workflow modules.

## Risks, Dependencies, and Assumptions
- Existing authored Markdown may surface latent heading-separation violations
  when the shared helper lands.
- The change assumes there is no intentional family exception to the published
  cross-family heading-separation rule.

## References
- docs/standards/documentation/documentation_semantics_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/standards/governance/decision_capture_standard.md
- docs/planning/prds/internal_project_code_review_follow_up.md
