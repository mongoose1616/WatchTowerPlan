---
trace_id: trace.reference.core_swap_integration_assessment_applicability
id: reference.core_swap_integration_assessment_applicability
title: Core Swap Integration Assessment Applicability
summary: Durable reference for interpreting the external WatchTowerPlan core-swap integration assessment against the current WatchTowerPlan repository.
type: reference
status: active
owner: repository_maintainer
updated_at: '2026-03-24T01:56:23Z'
audience: shared
authority: reference
applies_to:
- plan/docs/references/core_swap_integration_assessment_applicability_reference.md
- core/python/tests/unit/test_standard_index_sync.py
- core/python/src/watchtower_core/control_plane/operationalization_paths.py
- core/control_plane/registries/pack_registry.json
- plan/.wt/manifests/pack_settings.json
- core/control_plane/indexes/commands/command_index.json
- core/control_plane/indexes/references/reference_index.json
- core/control_plane/indexes/standards/standard_index.json
- core/control_plane/indexes/workflows/workflow_index.json
tags:
- reference
- assessment
- pack_integration
- portability
---

# Subject Summary

This reference records how the external
`WatchTowerOversight/oversight/assessments/watchtowerplan_core_swap_integration_assessment.md`
maps to the current WatchTowerPlan repository. Use it to separate
recipient-host integration findings from issues that are still actionable in
the source repository.

## Current Repository Status

- Verified on `2026-03-24`.
- `watchtower-core pack list --format json` returned `pack.plan` as the sole
  default repository pack.
- `watchtower-core pack describe --pack plan --format json` succeeded.
- `watchtower-core plan --help` succeeded.
- `pytest core/python/tests/unit/test_standard_index_sync.py -q` passed with
  `7/7` tests.
- `watchtower-core validate all --format json` passed with `464/464` checks.

## Applicability Matrix

- `1`: Not applicable in WatchTowerPlan. The persisted hosted-pack registry
  correctly declares `pack.plan` as the default repository pack here.
- `2`: Not applicable in WatchTowerPlan. `plan/.wt/manifests/pack_settings.json`
  exists locally and `watchtower-core pack describe --pack plan --format json`
  succeeds.
- `3`: Not applicable in WatchTowerPlan. The shared Python workspace should
  provision `watchtower-plan` in this repository because the live hosted pack is
  `plan`.
- `4`: Not applicable in WatchTowerPlan. The merged validator registry and the
  active hosted pack both resolve to `plan`.
- `5`: Not applicable in WatchTowerPlan. The merged validation-suite registry
  and the active hosted pack both resolve to `plan`.
- `6`: Not applicable in WatchTowerPlan. Activating the default pack settings
  path resolves to the current local `plan/.wt/manifests/pack_settings.json`.
- `7`: Not applicable in WatchTowerPlan. The checked-in command index matches
  the live `watchtower-core plan ...` CLI surface in this repository.
- `8`: Not applicable in WatchTowerPlan. Repository-path discovery correctly
  indexes the live `plan/**` host shape here.
- `9`: Not applicable in WatchTowerPlan. The checked-in route index is current
  for this repository after the latest sync pass.
- `10`: Not applicable in WatchTowerPlan. Foundation discovery should resolve to
  `plan/**` surfaces because this repository hosts the plan pack directly.
- `11`: Not applicable in WatchTowerPlan. Standard discovery should resolve to
  the plan-hosted guidance surfaces in this repository.
- `12`: Not applicable in WatchTowerPlan. Reference discovery should resolve to
  the plan-hosted guidance surfaces in this repository.
- `13`: Not applicable in WatchTowerPlan. Workflow discovery should resolve to
  the plan-hosted workflow surfaces in this repository.
- `14`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `15`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `16`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `17`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `18`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `19`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `20`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `21`: Not applicable now. The cited document-semantics failure is stale here;
  `watchtower-core validate all --format json` passed on `2026-03-24`.
- `22`: Not applicable in WatchTowerPlan. The local repository validation
  baseline is currently green, so the CLI tests that expect exit code `0`
  remain correct here.
- `23`: Applicable portability debt in shared-core tests. The shared
  `test_standard_index_sync.py` placeholder matcher previously hard-coded
  `plan/...` paths. This repository now derives the active pack roots from
  `ControlPlaneLoader` and also checks an externalized pack root under
  `packs/oversight/`.

## Recommendation And Contract Applicability

- The report's rehost/bootstrap procedure, normative rehost contract,
  acceptance criteria, and fix-order sections are recipient-repository
  guidance for a copied-core consumer whose hosted pack is `oversight`.
- Those sections are not remediation steps for WatchTowerPlan. This repository
  is the authored source host for `pack.plan`, so rewriting
  `core/control_plane/registries/pack_registry.json` or
  `core/python/pyproject.toml` to `oversight` here would be incorrect.
- The only report item that translated into a source-repository shared-core fix
  was item `23`, and the current `pytest core/python/tests/unit/test_standard_index_sync.py -q`
  pass confirms that host-aware placeholder coverage still holds.

## Additional Review Items

- Shared docs that mention literal `plan/` paths remain intentional when they
  are describing the current WatchTowerPlan repository rather than defining a
  pack-neutral portability contract.
- Remaining `<pack>` placeholders stay valid where they are deliberate
  pack-neutral authoring tokens, the report's placeholder sweep was aimed at a
  different recipient host, and no active validator flags them in the current
  repository.

## Related Surfaces

- `plan/docs/references/core_swap_integration_assessment_applicability_reference.md`
- `core/python/tests/unit/test_standard_index_sync.py`
- `core/python/src/watchtower_core/control_plane/operationalization_paths.py`
- `core/control_plane/registries/pack_registry.json`
- `plan/.wt/manifests/pack_settings.json`

## Notes

- Treat the external oversight-host assessment as a portability comparison, not
  as a statement that the current WatchTowerPlan repository is broken.
- Keep shared-core tests host-aware when they exercise `<pack>` placeholder
  expansion or other active-pack behavior.
