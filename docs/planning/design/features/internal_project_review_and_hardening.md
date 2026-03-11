---
trace_id: trace.internal_project_review_and_hardening
id: design.features.internal_project_review_and_hardening
title: Internal Project Review and Hardening Feature Design
summary: Defines the review-backed design for validation-compatible planning bootstrap output and canonical coordination payload serialization.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T15:11:22Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/
- workflows/
---

# Internal Project Review and Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.internal_project_review_and_hardening`
- `Design ID`: `design.features.internal_project_review_and_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.internal_project_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_review_and_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.internal_project_review_and_hardening`
- `Updated At`: `2026-03-11T15:11:22Z`

## Summary
Defines the review-backed design for validation-compatible planning bootstrap output and canonical coordination payload serialization.

## Source Request
- User request to perform an ultra-deep internal project review, fix every validated issue, and continue through planning, implementation, validation, and closeout.
- Internal review evidence that `watchtower-core plan bootstrap --write` currently leaves the repository invalid for this trace.

## Scope and Feature Boundary
- Covers the planning bootstrap path from rendered docs through task creation, traceability refresh, acceptance contract publication, and baseline evidence recording.
- Covers the current trace's planning baseline so the repo returns to a validation-compatible state before code closeout.
- Covers initiative and planning JSON projection serialization used by sync and query surfaces.
- Does not relax repository governance rules to permit partial traces.
- Does not redesign the planning-family model or replace the existing coordination surfaces.

## Current-State Context
- The repository was green before this new trace was bootstrapped.
- After `watchtower-core plan bootstrap --write` created this trace, `./.venv/bin/watchtower-core validate all --format json` failed because the trace had no acceptance contract and `./.venv/bin/pytest -q` failed because the generated design docs omitted the repository's required applied-reference sections.
- The existing bootstrap renderer validates front matter and minimal section presence, but it does not validate against the executable documentation expectations enforced by the repo integration suite.
- Coordination-facing JSON payloads are currently shaped separately in initiative-index sync, planning-catalog sync, and query handlers, which increases maintenance and drift risk for the same machine-facing fields.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): bootstrap output should be small, deterministic, and valid by construction rather than depending on immediate manual cleanup.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): authored docs, machine-readable contracts, evidence, and derived mirrors should remain synchronized in one write flow.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): core repository hardening should improve shared substrate reliability before product work expands these flows further.

## Internal Standards and Canonical References Applied
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): generated feature-design docs must respect governed design-document structure.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): generated implementation plans must include the same repository-compliant applied-reference framing expected by validation and review.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): traced initiatives that publish durable acceptance IDs must publish one aligned machine-readable contract.
- [acceptance_evidence_reconciliation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/acceptance_evidence_reconciliation_standard.md): bootstrap should not create a trace that immediately fails acceptance reconciliation.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): coordination and planning projection fields should remain consistent across machine-readable lookup surfaces.

## Design Goals and Constraints
- Make `plan bootstrap --write` publish a minimal but validation-compatible traced baseline in one bounded flow.
- Keep generated planning documents compact while satisfying the repository's executable documentation expectations.
- Preserve existing bootstrap filenames, trace-derived IDs, and top-level command semantics unless a stronger safety constraint requires expansion.
- Keep query JSON contracts stable while reducing duplicated serializer logic behind them.

## Options Considered
### Option 1
- Repair only this trace manually by editing its docs, adding a contract, and recording evidence without changing bootstrap or serializer code.
- Strength: smallest immediate patch.
- Tradeoff: future bootstrap writes would still create repo-invalid traces and the serializer drift risk would remain.

### Option 2
- Harden bootstrap so it emits repository-compliant design docs, publishes the initial acceptance contract and planning-baseline evidence, and consolidate coordination/planning payload shaping behind shared serializers.
- Strength: fixes the current trace and the reusable workflow path at the same time while reducing future JSON drift.
- Tradeoff: touches multiple planning, control-plane, CLI, and test surfaces in one initiative.

### Option 3
- Relax the acceptance and documentation validators so partial bootstrap traces are allowed until later follow-up work lands.
- Strength: smallest code change to get bootstrap writes through.
- Tradeoff: weakens repository trust guarantees and hides incomplete planning state behind looser validation.

## Recommended Design
### Bootstrap Completeness
- Extend the scaffold renderer so feature and implementation documents include repository-compliant applied-reference sections with placeholder-safe explained bullets.
- Extend bootstrap write mode to publish a minimal acceptance contract derived from the bootstrap PRD acceptance and requirement IDs.
- Record a planning-baseline evidence artifact during bootstrap so acceptance reconciliation passes immediately after the trace is created.

### Sync and Write Ordering
- Write authored planning docs and the acceptance contract before rebuilding derived planning surfaces.
- Refresh traceability and coordination after the contract exists so the evidence recorder can link the contract cleanly.
- Record bootstrap evidence only after the traceability layer can resolve the new contract and planning surfaces.

### Projection Serialization
- Introduce shared serializer helpers for active task summaries, initiative entries, and planning-catalog entries.
- Reuse those helpers in sync builders and query handlers so the query layer reflects the canonical projection structure instead of re-encoding the same fields manually.
- Preserve current payload fields and field names to avoid breaking query consumers.

### Invariants and Failure Cases
- Bootstrap should fail before writing partial state when generated docs or contract/evidence artifacts would violate schema or governed-document expectations.
- Acceptance and documentation validators remain strict; the fix is to improve bootstrap output, not to lower repository standards.
- Shared serializers must be covered by regression tests so future field additions land in one place.

## Affected Surfaces
- `core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py`
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`
- `core/python/src/watchtower_core/evidence/validation_evidence.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py`
- `core/python/src/watchtower_core/cli/plan_handlers.py`
- `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- `core/python/tests/unit/`
- `core/python/tests/integration/`
- `docs/commands/core_python/watchtower_core_plan_bootstrap.md`
- `core/control_plane/contracts/acceptance/`
- `core/control_plane/ledgers/validation_evidence/`

## Design Guardrails
- Do not permit bootstrap to write a trace that immediately fails the repository's standard validation baseline.
- Do not fork public query payload shapes while consolidating serializer logic.
- Do not move acceptance or evidence authority back into PRD prose once machine-readable artifacts exist.

## Risks
- Bootstrap hardening spans authored docs, task creation, derived sync, and evidence recording, so tests must cover both dry-run and write mode carefully.
- Serializer consolidation could accidentally drop optional fields if regression tests only cover the happy path.
- Placeholder-safe applied-reference sections must stay compact enough that scaffold output remains useful rather than becoming noise.

## References
- docs/planning/coordination_tracking.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/control_plane/contracts/acceptance/README.md
