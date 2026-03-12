---
trace_id: trace.data_contract_example_operationalization_alignment
id: decision.data_contract_example_operationalization_alignment_direction
title: Data Contract Example Operationalization Alignment Direction Decision
summary: Records the initial direction decision for Data Contract Example Operationalization
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T01:19:10Z'
audience: shared
authority: supporting
---

# Data Contract Example Operationalization Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.data_contract_example_operationalization_alignment`
- `Decision ID`: `decision.data_contract_example_operationalization_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.data_contract_example_operationalization_alignment`
- `Linked Designs`: `design.features.data_contract_example_operationalization_alignment`
- `Linked Implementation Plans`: `design.implementation.data_contract_example_operationalization_alignment`
- `Updated At`: `2026-03-12T01:19:10Z`

## Summary
Records the initial direction decision for Data Contract Example Operationalization Alignment.

## Decision Statement
Update the affected data-contract standards to publish family-specific valid and invalid example glob patterns in `Operational Surfaces`, and protect that coverage with regression tests instead of relying on generic schema/example standards alone.

## Trigger or Source Request
- Another expansive internal standards review confirmed that concrete control-plane example artifacts do not resolve back to their governing family standards through standards lookup.

## Current Context and Constraints
- `watchtower-core query standards --operationalization-path core/control_plane/examples/valid/indexes/standard_index.v1.example.json --format json` omits `std.data_contracts.standard_index`.
- The same lookup blind spot reproduces for representative command-index, initiative-index, design-document-index, and traceability-index example artifacts, and the pattern extends beyond indexes into contract, ledger, and registry example families.
- The standards query path already supports bounded repo-relative glob matching, so the gap is authored operationalization coverage rather than missing runtime capability.

## Applied References and Implications
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the live standard index must reflect the authored operationalization surfaces, so the governing standards themselves need to publish the example-family coverage.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): example artifacts remain schema-governed machine-readable surfaces, but schema-level coverage alone is too generic to answer which artifact-family standard applies.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the authored standards, derived index, and regression coverage must land together.

## Affected Surfaces
- docs/standards/data_contracts/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_cli_query_commands.py
- docs/planning/prds/data_contract_example_operationalization_alignment.md
- docs/planning/design/features/data_contract_example_operationalization_alignment.md
- docs/planning/design/implementation/data_contract_example_operationalization_alignment.md

## Options Considered
### Option 1
- Leave example lookup governed only by the generic schema and format-selection standards.
- Requires no changes.
- Preserves the blind spot where the governing data-contract family standard is undiscoverable from the example artifact itself.

### Option 2
- Add broad example-directory operationalization paths such as `core/control_plane/examples/valid/indexes/` to the affected standards.
- Reduces the number of new operationalization entries.
- Overmatches neighboring example families and weakens the precision of standards lookup.

### Option 3
- Add family-specific valid and invalid example glob patterns to the affected data-contract standards and verify the resulting lookup behavior with regression coverage.
- Preserves precise family lookup while reusing the existing bounded-glob matching contract.
- Requires a coordinated update across multiple standards and derived surfaces.

## Chosen Outcome
Accept option 3. Publish family-specific valid and invalid example globs in the affected data-contract standards, rebuild the live standard index from those authored surfaces, and add regressions that prove representative example artifacts resolve back to their governing standards.

## Rationale and Tradeoffs
- Family-specific globs fix the real lookup gap without weakening the precision of standards matching.
- The change stays within the existing operationalization-path model, so no new family-specific runtime branching is required.
- The tradeoff is a larger coordinated standards edit set, but that is preferable to leaving example governance implicit or over-broadening every standard to entire example directories.

## Consequences and Follow-Up Impacts
- Multiple data-contract standards will gain valid and invalid example globs in `Operational Surfaces`.
- The live standard index will change after sync, and regression tests will need to reflect the new coverage.
- Final closeout evidence must show both the repaired lookup behavior and a clean repo-wide validation baseline.

## Risks, Dependencies, and Assumptions
- The repair assumes the current example filename conventions remain stable enough for bounded family globs to stay precise.
- Missing one artifact family would leave the standards lookup gap partially open, so the regression coverage must scan the intended set instead of relying on one or two examples.

## References
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/data_contracts/schema_standard.md
- core/control_plane/examples/valid/indexes/standard_index.v1.example.json
- core/control_plane/examples/valid/contracts/acceptance_contract.v1.example.json
