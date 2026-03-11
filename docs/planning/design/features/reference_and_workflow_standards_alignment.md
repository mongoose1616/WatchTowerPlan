---
trace_id: trace.reference_and_workflow_standards_alignment
id: design.features.reference_and_workflow_standards_alignment
title: Reference and Workflow Standards Alignment Feature Design
summary: Defines the technical design boundary for converging governed
  reference authoring rules and workflow additional-load enforcement.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T23:19:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
---

# Reference and Workflow Standards Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.reference_and_workflow_standards_alignment`
- `Design ID`: `design.features.reference_and_workflow_standards_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.reference_and_workflow_standards_alignment`
- `Linked Decisions`: `decision.reference_and_workflow_standards_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.reference_and_workflow_standards_alignment`
- `Updated At`: `2026-03-11T23:19:00Z`

## Summary
Defines the technical design boundary for converging governed reference
authoring rules and workflow additional-load enforcement.

## Source Request
- Another expansive internal standards review exposed live drift between reference/workflow standards and the code paths that validate and index those governed Markdown families.

## Scope and Feature Boundary
- Align the reference document standard and template with the already-enforced
  canonical-upstream requirement for governed `docs/references/**` documents.
- Tighten workflow additional-load validation so generic workflow standards
  stay implicit and never surface as task-specific extra files to load.
- Exclude schema redesign, route-index policy changes, or new reference-family
  subtypes beyond the reproduced contract drift.

## Current-State Context
- `DocumentSemanticsValidationService` and `ReferenceIndexSyncService` already
  reject governed reference docs that omit `Canonical Upstream`.
- `reference_index_standard.md` already requires every reference-index entry to
  publish `canonical_upstream_urls`, so the machine-readable contract is
  stricter than the reference standard and template.
- `workflow_md_standard.md` and the workflow integration check both say generic
  workflow standards must stay implicit in `Additional Files to Load`, but the
  implementation disallow list omits
  `docs/standards/workflows/routing_and_context_loading_standard.md`.

## Foundations References Applied
- `docs/foundations/repository_standards_posture.md`: governed prose
  standards, templates, validators, and indexes should publish one coherent
  contract rather than leaving repo rules split between authoring guidance and
  enforcement code.

## Internal Standards and Canonical References Applied
- `docs/standards/documentation/reference_md_standard.md`: the reference
  authoring contract must match the live governed validator and index boundary.
- `docs/standards/data_contracts/reference_index_standard.md`: canonical
  upstream URLs are already required in the machine-readable reference family,
  so prose guidance must not imply that the field can be absent.
- `docs/standards/documentation/workflow_md_standard.md`: generic workflow
  standards must stay implicit in `Additional Files to Load`.
- `docs/standards/data_contracts/workflow_index_standard.md`: workflow sync
  should only project task-specific extra files to load, not routing-baseline
  standards.

## Design Goals and Constraints
- Preserve the existing machine-readable reference and workflow index schemas.
- Prefer fixing the weaker prose contract where the live validator and sync
  behavior already agree on the stricter rule.
- Keep workflow additional-load enforcement narrow so it rejects only generic
  baseline standards and not legitimate task-specific context.

## Options Considered
### Option 1
- Relax reference validation and reference-index expectations to match the
  current optional prose guidance, and keep the workflow disallow list as-is.
- Strength: smaller immediate code diff.
- Tradeoff: weakens the governed reference family boundary and leaves workflow
  additional-load enforcement inconsistent with its own published standard.

### Option 2
- Align the reference prose contract to the already-enforced machine contract
  and extend workflow additional-load enforcement to reject the missing generic
  workflow standard.
- Strength: standards, templates, validators, sync, and review checks converge
  on one contract without changing artifact schemas.
- Tradeoff: more documentation and regression surfaces update together.

## Recommended Design
### Architecture
- Keep reference validation and reference-index behavior intact, and instead
  tighten the reference standard and template so they make `Canonical Upstream`
  mandatory for governed reference docs.
- Extend the workflow routing-baseline disallow set to include
  `routing_and_context_loading_standard.md` so validation and sync reject that
  generic workflow standard wherever `Additional Files to Load` is parsed.
- Add close-to-source regression checks in unit and integration suites so the
  authoring guidance and workflow enforcement contracts fail closed if they
  drift again.

### Data and Interface Impacts
- `docs/standards/documentation/reference_md_standard.md` and
  `docs/templates/reference_template.md` become stricter and stop listing
  `Canonical Upstream` as optional for governed references.
- `core/python/src/watchtower_core/repo_ops/sync/workflow_index.py` changes its
  generic-baseline disallow set, but no CLI flag or schema changes.
- Integration and unit coverage expand around the reference authoring contract
  and workflow additional-load validation rules.

### Execution Flow
1. Rewrite the traced planning surfaces so the two reproduced drifts and their
   accepted remediation direction are explicit.
2. Update the reference standard and template to require `Canonical Upstream`
   and add regression guards around that contract.
3. Tighten workflow additional-load validation and integration checks to reject
   `routing_and_context_loading_standard.md` as a generic routing-baseline
   surface.
4. Refresh derived indexes and trackers, rerun the repository validation
   baseline, and publish acceptance evidence.

### Invariants and Failure Cases
- Governed reference docs under `docs/references/**` must continue to expose at
  least one canonical upstream URL so reference-index entries can publish
  `canonical_upstream_urls` deterministically.
- Workflow additional-load parsing must continue accepting one concrete
  task-specific repo-local path per bullet while rejecting generic baseline
  standards that should stay implicit.

## Affected Surfaces
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_workflow_index_sync.py

## Design Guardrails
- Do not weaken the reference-index standard or reference validator just to
  preserve stale optional prose guidance.
- Do not expand workflow additional-load rejection beyond generic routing
  baseline surfaces that the workflow standard already classifies as implicit.

## Risks
- Contributors may have interpreted the old reference template as permission to
  create repo-native references without upstream authority, so the revised
  prose must make the governed family boundary explicit.

## References
- docs/standards/documentation/reference_md_standard.md
- docs/templates/reference_template.md
- docs/standards/documentation/workflow_md_standard.md
- docs/templates/workflow_template.md
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/data_contracts/workflow_index_standard.md
