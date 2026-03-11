---
trace_id: trace.internal_project_review_and_hardening
id: decision.internal_project_review_and_hardening_direction
title: Internal Project Review and Hardening Direction Decision
summary: Records the decision to keep repository validation strict, harden planning bootstrap to produce a complete baseline, and consolidate coordination payload shaping behind shared serializers.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-11T15:11:22Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/
- workflows/
---

# Internal Project Review and Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.internal_project_review_and_hardening`
- `Decision ID`: `decision.internal_project_review_and_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.internal_project_review_and_hardening`
- `Linked Designs`: `design.features.internal_project_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_review_and_hardening`
- `Updated At`: `2026-03-11T15:11:22Z`

## Summary
Records the decision to keep repository validation strict, harden planning bootstrap to produce a complete baseline, and consolidate coordination payload shaping behind shared serializers.

## Decision Statement
Keep the current validation and governance rules intact, fix `watchtower-core plan bootstrap --write` so it publishes a validation-compatible traced baseline by default, and consolidate initiative and planning JSON shaping behind shared serializers instead of allowing parallel payload builders to drift.

## Trigger or Source Request
- User request to perform an ultra-deep internal project review and fix every validated issue end to end.
- Internal review evidence that the freshly bootstrapped trace immediately broke `validate all` and `pytest`.

## Current Context and Constraints
- The repository was green before this new trace was created.
- The current bootstrap flow can write a traced initiative without the acceptance contract and evidence artifacts required by acceptance reconciliation.
- The generated feature-design and implementation-plan docs currently omit applied-reference sections that the repository test suite treats as required for governed design docs.
- Coordination and planning query payloads currently shape the same fields in more than one place.

## Applied References and Implications
- [acceptance_evidence_reconciliation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/acceptance_evidence_reconciliation_standard.md): new traces should not enter the repo in a state that immediately fails acceptance reconciliation.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): bootstrap should publish the contract in the canonical family when the PRD emits durable acceptance IDs.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): generated feature-design docs must satisfy the repository's governed-document expectations, not just front matter shape.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): generated implementation plans need the same validation-compatible applied-reference framing.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): coordination and planning projections should stay structurally consistent across machine-readable lookup surfaces.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/evidence/validation_evidence.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/cli/plan_handlers.py
- core/python/src/watchtower_core/cli/query_coordination_handlers.py
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/

## Options Considered
### Option 1
- Repair only the current trace and leave reusable bootstrap and serializer code untouched.
- Strength: smallest patch to restore green quickly.
- Tradeoff: future bootstraps would still create repo-invalid traces and the projection drift risk would remain.

### Option 2
- Harden bootstrap to emit compliant design docs, acceptance contract, and baseline evidence, and extract shared serializers for coordination-facing JSON.
- Strength: fixes the current trace and the reusable workflow path while reducing future drift.
- Tradeoff: broader implementation scope and more companion-surface updates in one initiative.

### Option 3
- Relax acceptance and documentation validation so incomplete bootstrap traces are temporarily allowed.
- Strength: minimal implementation effort.
- Tradeoff: lowers repository trust and turns a real workflow defect into tolerated drift.

## Chosen Outcome
Adopt option 2. The repository keeps strict validation, bootstrap becomes validation-compatible by default, and coordination/planning projection logic is consolidated behind shared serializers.

## Rationale and Tradeoffs
- The review found a real workflow defect, not an overly strict validator.
- Strict validation is useful only if common write paths honor it, so bootstrap needs to improve rather than the validator weakening.
- Shared serializers reduce the chance that indexes and query payloads drift apart as future fields are added.
- The wider fix set is justified because it repairs both the current trace and the reusable maintenance path.

## Consequences and Follow-Up Impacts
- Bootstrap command docs, tests, and result payloads must expand to describe the acceptance-contract and evidence outputs.
- The current trace must publish its own acceptance contract, evidence artifact, and bounded tasks before closeout.
- Initiative and planning query regressions need targeted tests after serializer extraction.

## Risks, Dependencies, and Assumptions
- Bootstrap write ordering must be carefully sequenced so contract publication, traceability refresh, and evidence recording can all succeed in one flow.
- The serializer extraction assumes current payload shapes are already correct and should be preserved rather than redesigned.
- The current trace will generate broad but expected derived-surface churn once the missing baseline artifacts land.

## References
- docs/planning/coordination_tracking.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/control_plane/contracts/acceptance/README.md
