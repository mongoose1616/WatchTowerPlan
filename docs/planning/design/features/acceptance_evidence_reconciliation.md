---
trace_id: "trace.acceptance_evidence_reconciliation"
id: "design.features.acceptance_evidence_reconciliation"
title: "Acceptance and Evidence Reconciliation Design"
summary: "Defines the feature-level design for the acceptance and evidence reconciliation flow that keeps acceptance contracts, validator expectations, validation evidence, and traceability joins aligned."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T18:25:06Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/design/features/acceptance_evidence_reconciliation.md"
  - "core/control_plane/contracts/acceptance/"
  - "core/control_plane/ledgers/validation_evidence/"
  - "core/control_plane/indexes/traceability/traceability_index.v1.json"
aliases:
  - "acceptance evidence reconciliation"
  - "acceptance coverage reconciliation"
---

# Acceptance and Evidence Reconciliation Design

## Record Metadata
- `Trace ID`: `trace.acceptance_evidence_reconciliation`
- `Design ID`: `design.features.acceptance_evidence_reconciliation`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-09T18:25:06Z`

## Summary
This document defines the feature-level design for the acceptance and evidence reconciliation flow that keeps acceptance contracts, validator expectations, validation evidence, and traceability joins aligned.

## Source Request
- User request to turn acceptance and evidence reconciliation into a reusable workflow and Python validation surface.

## Scope and Feature Boundary
- Covers the workflow phase and Python validation surface that reconcile PRD acceptance IDs, acceptance contracts, validator coverage, validation-evidence artifacts, and unified traceability joins.
- Covers when this concern should become its own reusable workflow module instead of remaining implicit inside broader validation or traceability work.
- Does not replace the narrower schema-validation commands or the separate initiative-closeout flow.
- Does not replace `traceability_reconciliation.md` or `governed_artifact_reconciliation.md`, which should remain narrower and immediately usable.

## Current-State Context
- The repository already defines machine-readable acceptance contracts under `core/control_plane/contracts/acceptance/` and durable validation evidence under `core/control_plane/ledgers/validation_evidence/`.
- The current traceability model expects acceptance and evidence surfaces to join back to PRDs, validators, and traced initiatives.
- The current workflow set now has stronger traceability and governed-artifact reconciliation phases, but it still does not have a dedicated reusable phase for acceptance-to-evidence coverage reconciliation.
- The repository now has enough acceptance, evidence, and traceability structure to justify a live workflow and a semantic validation command.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): keep repository behavior deterministic, inspectable, and local-first rather than dependent on hidden inference.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): preserve reusable validation and closeout capabilities that can support maintainers and automated workflows.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep companion human-readable and machine-readable surfaces aligned in the same change set when they depend on one another.

## Internal Standards and Canonical References Applied
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): acceptance IDs and expected outcomes need to stay machine-readable and stable across reconciliation.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): validation results need durable evidence records rather than ad hoc closeout notes.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): acceptance and evidence updates must stay linked through the shared trace chain.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): reconciled acceptance and evidence state must land in the unified machine index.
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): reconciliation should stay as a narrow composable workflow instead of a mixed-purpose catch-all.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): code, docs, indexes, and evidence surfaces should be refreshed in the same change set.

## Design Goals and Constraints
- Make acceptance-to-evidence reconciliation a repeatable concern once repository usage justifies it.
- Preserve clear authority boundaries between PRDs, acceptance contracts, validators, validation evidence, and traceability indexes.
- Keep blocker semantics explicit rather than leaving missing evidence or missing coverage to reviewer inference.
- Avoid adding a workflow module before the repository has enough recurring acceptance and evidence activity to make the module concrete.

## Options Considered
### Option 1
- Fold acceptance and evidence checks into `traceability_reconciliation.md`.
- Strengths: fewer named workflow modules and less routing surface.
- Tradeoffs or reasons not chosen: acceptance and evidence coverage is narrower and more semantic than general planning trace reconciliation, so it would make the traceability module broader and less focused.

### Option 2
- Capture the concern as a feature and then activate it as a dedicated workflow module plus Python validation command once the artifact families are active enough.
- Strengths: preserves a clean reusable boundary while still giving the repo a semantic validation surface now.
- Tradeoffs or reasons not chosen: adds one more workflow and command surface to maintain.

### Option 3
- Treat acceptance and evidence checks as part of generic code validation or task handoff review.
- Strengths: no new feature or module surface to maintain.
- Tradeoffs or reasons not chosen: too vague, likely to produce inconsistent reviewer behavior, and does not create a reusable acceptance-coverage workflow.

## Recommended Design
### Architecture
- Use a dedicated shared workflow module named `acceptance_evidence_reconciliation.md`.
- Expose a Python semantic validator through `watchtower-core validate acceptance`.
- Load the module when tasks materially touch acceptance contracts, validator coverage expectations, durable validation evidence, or closeout proof for traced initiatives.
- Keep `traceability_reconciliation.md` responsible for cross-family planning links and keep `governed_artifact_reconciliation.md` responsible for schema-backed artifact coherence; the acceptance-and-evidence module sits between them and closes the semantic coverage gap.

### Data and Interface Impacts
- Workflow module under `workflows/modules/acceptance_evidence_reconciliation.md`.
- Routing-table guidance for loading that module when acceptance or evidence drift becomes the main risk.
- Governance standard for pass or fail expectations around acceptance coverage and evidence sufficiency.
- Python query and validation helpers that materialize acceptance and evidence views explicitly.

### Execution Flow
1. A task changes PRD acceptance items, acceptance contracts, validator expectations, or validation-evidence artifacts.
2. The workflow loads the source PRD acceptance IDs, matching acceptance contracts, relevant validators, evidence artifacts, and unified traceability entries.
3. The workflow compares acceptance coverage, validator linkage, evidence linkage, and trace joins for completeness and consistency.
4. The workflow updates the relevant human-readable and machine-readable surfaces or records explicit follow-up work when policy allows deferment.
5. Closeout, review, or audit workflows consume the resulting explicit coverage state rather than reconstructing it from prose.

### Invariants and Failure Cases
- Acceptance IDs must be preserved from PRDs into acceptance contracts and any evidence that claims to cover them.
- Validation-evidence artifacts must remain durable historical records rather than being used as mutable current-state truth.
- Missing evidence may be deferred only when the repository policy for that task allows it; silent omission is not acceptable.
- Validator expectations must not be inferred only from prose when a machine-readable contract or evidence surface already exists.

## Affected Surfaces
- `workflows/modules/acceptance_evidence_reconciliation.md`
- `workflows/ROUTING_TABLE.md`
- `docs/standards/governance/acceptance_evidence_reconciliation_standard.md`
- `core/control_plane/contracts/acceptance/`
- `core/control_plane/ledgers/validation_evidence/`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`
- `core/control_plane/registries/validators/validator_registry.v1.json`
- `core/python/src/watchtower_core/query/`
- `core/python/src/watchtower_core/validation/acceptance.py`

## Design Guardrails
- Do not collapse durable acceptance and evidence semantics into generic task handoff notes.
- Keep source-of-truth boundaries explicit between PRDs, acceptance contracts, validation evidence, and traceability indexes.
- Keep the semantic validator narrow; do not let it become a generic substitute for traceability or schema validation.

## Implementation-Planning Handoff Notes
- Keep the acceptance and evidence rules aligned with the validator registry and durable evidence artifacts as new traces adopt them.
- Extend the command later if durable evidence writing should happen directly from semantic reconciliation.
- Add more traces to this flow before treating the current baseline as a generalized release gate.

## Dependencies
- Acceptance contracts under `core/control_plane/contracts/acceptance/`
- Validation-evidence artifacts under `core/control_plane/ledgers/validation_evidence/`
- The validator registry and unified traceability index

## Risks
- If the module is introduced too early, it will become abstract and underused.
- If the concern is deferred too long, acceptance and evidence drift will be handled inconsistently across tasks.
- If blocker semantics stay implicit, reviewers will apply different standards to missing evidence or incomplete acceptance coverage.

## Open Questions
- Should missing durable evidence for an active acceptance item block commit closeout, only release or closeout workflows, or depend on the artifact family?
- Should future semantic acceptance validation also write durable evidence directly, or should evidence remain a separately curated follow-on step?

## References
- [traceability_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/traceability_reconciliation.md)
- [governed_artifact_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/governed_artifact_reconciliation.md)
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json)

## Updated At
- `2026-03-09T18:25:06Z`
