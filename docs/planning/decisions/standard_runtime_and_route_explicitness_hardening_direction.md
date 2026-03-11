---
trace_id: trace.standard_runtime_and_route_explicitness
id: decision.standard_runtime_and_route_explicitness_direction
title: Standard, Runtime, and Route Explicitness Hardening Direction Decision
summary: Records the initial direction decision for Standard, Runtime, and Route Explicitness
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-11T05:35:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
---

# Standard, Runtime, and Route Explicitness Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.standard_runtime_and_route_explicitness`
- `Decision ID`: `decision.standard_runtime_and_route_explicitness_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.standard_runtime_and_route_explicitness`
- `Linked Designs`: `design.features.standard_runtime_and_route_explicitness`
- `Linked Implementation Plans`: `design.implementation.standard_runtime_and_route_explicitness`
- `Updated At`: `2026-03-11T05:35:00Z`

## Summary
Records the initial direction decision for Standard, Runtime, and Route Explicitness Hardening.

## Decision Statement
Close the still-valid report-set gaps by adding authored operationalization metadata to standards, documenting runtime package boundaries with package-level READMEs, and improving route-preview matching while keeping route preview advisory rather than autonomous.

## Trigger or Source Request
- The March 2026 expanded review set was rechecked against the live repository, and three gaps still reproduced directly: standards operationalization remained implicit, runtime package boundaries remained under-documented, and route preview still failed on realistic free-form maintenance requests.

## Current Context and Constraints
- The standard index currently answers citation questions well, but it cannot answer what operationalizes a standard without a human reading multiple docs and code paths manually.
- The `watchtower_core` package tree currently has no package-level README surfaces, even though the repo now expects contributors and agents to navigate export-safe versus repo-local boundaries accurately.
- The route-preview command currently requires exact trigger phrases before token overlap can contribute to scoring, which makes it too brittle for realistic maintenance requests.
- Foundation-scope drift, layered health reporting, and recurring maintenance-loop clarity are already addressed in the current repo, so this initiative should not reopen them.

## Affected Surfaces
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
- core/python/tests/

## Options Considered
### Option 1
- Add only narrative documentation and leave the machine-readable standard and routing surfaces unchanged.
- Strength: lowest implementation risk.
- Tradeoff: does not actually close the reproduced machine-queryability and routing failures.

### Option 2
- Keep the current authority model, add authored operationalization metadata to standards, publish package-level boundary docs, and harden route-preview scoring with deterministic token-aware matching.
- Strength: closes the verified gaps without introducing a second authority surface or an autonomous router.
- Tradeoff: requires a repository-wide standards backfill and careful tuning of route-scoring thresholds.

### Option 3
- Introduce a separate operationalization registry and a more semantic route planner that infers intent beyond the route index.
- Strength: would push the repo further toward full machine-first orchestration.
- Tradeoff: too much new machinery for one bounded remediation slice and too much risk of creating hidden authority.

## Chosen Outcome
Adopt option 2. The standard docs themselves will carry an `Operationalization` section with `Modes` and `Operational Surfaces`, standard `owner` and `applies_to` values will remain authoritative in front matter and the derived standard index, the runtime package tree will gain package-level boundary docs, and route preview will become more tolerant of natural maintenance requests while remaining advisory and deterministic.

## Rationale and Tradeoffs
- This keeps the current authority split intact: authored docs remain primary, derived indexes remain query surfaces, and route preview remains assistive rather than authoritative.
- Adding explicit standard-operationalization metadata is the smallest change that makes the standard index answer the report’s core machine-audit question without creating a second authored registry.
- Package READMEs close the clearest remaining runtime-doc gap without requiring immediate package extraction or new runtime behavior.
- Token-aware route matching is enough to fix the reproduced brittleness without escalating into a semantic router that the current design and standards do not authorize.

## Consequences and Follow-Up Impacts
- Every live standard will gain a compact `Operationalization` section with `Modes` and `Operational Surfaces`, and the standard-index family will gain corresponding schema, sync, query, and test updates.
- `core/python/src/watchtower_core/` will gain package-level README documents and updated workspace navigation guidance.
- Route-preview tests and docs will change to reflect the broader advisory matching behavior.
- Broader planning-document contract unification remains a separate future workstream if active drift appears later.

## Risks, Dependencies, and Assumptions
- The backfill assumes most standards can be classified cleanly with a small operationalization vocabulary.
- The route-preview change assumes deterministic token-aware scoring is enough for the current repo size and request patterns.
- The runtime boundary docs assume the current compatibility guards in `query`, `sync`, and `validation` accurately reflect the supported boundary.

## References
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md)
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/standard_runtime_and_route_explicitness_hardening.md)
- [workflow_operationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/workflow_operationalization_direction.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
