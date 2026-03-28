---
id: reference.core_swap_integration_assessment_closeout
title: Core Swap Integration Assessment Closeout
summary: Durable reference recording current WatchTowerPlan verification of the external oversight-host core-swap integration assessment and the resulting local applicability decisions.
type: reference
status: active
owner: repository_maintainer
updated_at: '2026-03-28T23:55:00Z'
audience: shared
authority: reference
applies_to:
- core/control_plane/registries/pack_registry.json
- core/python/pyproject.toml
- plan/.wt/manifests/pack_settings.json
- core/python/tests/unit/test_control_plane_loader_surfaces.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_cli_validate_commands.py
- core/python/tests/integration/test_validate_all_cli.py
tags:
- reference
- assessment
- closeout
- pack_integration
- portability
---

# Core Swap Integration Assessment Closeout

This reference records how the external
`WatchTowerOversight/oversight/assessments/watchtowerplan_core_swap_integration_assessment.md`
maps to the current WatchTowerPlan repository after fresh local verification on
`2026-03-24`.

Use it to separate recipient-host rehost findings for `WatchTowerOversight` from
actual source-repository work in `WatchTowerPlan`.

## Canonical Upstream

- [WatchTowerOversight core-swap integration assessment](https://github.com/mongoose1616/WatchTowerOversight/blob/HEAD/oversight/assessments/watchtowerplan_core_swap_integration_assessment.md)

## Quick Reference or Distilled Reference

- The upstream assessment is useful as a recipient-host portability comparison,
  but its import, purge, bootstrap, and rehost actions are not remediation
  steps for the live `WatchTowerPlan` source repository.
- The local question this reference answers is whether the assessment findings
  indicate a real source-repository defect here or simply describe the
  intentional `plan` host shape and recipient-specific bootstrap work elsewhere.

### Current Verification Snapshot

- `watchtower-core doctor` passed and loaded the current shared-governance
  surface set for this repository.
- `watchtower-core pack list --format json` returned exactly one hosted pack:
  `pack.plan`, with `default_repo_pack=true`.
- `watchtower-core pack describe --pack plan --format json` succeeded.
- `watchtower-core pack validate --pack plan --format json` succeeded with
  `0` issues.
- `watchtower-core plan --help` succeeded.
- `watchtower-core query commands --query plan --format json` returned `10`
  command hits.
- `watchtower-core query paths --query plan --format json` returned `10` path
  hits.
- `watchtower-core query foundations --query plan --format json` returned `6`
  foundation hits.
- `watchtower-core query standards --query plan --format json` returned `10`
  standard hits.
- `watchtower-core query references --query plan --format json` returned `8`
  reference hits.
- `watchtower-core query workflows --query plan --format json` returned `10`
  workflow hits.
- `watchtower-core validate all --format json` passed with `464/464` checks.
- The report-adjacent pytest slice passed for:
  - `tests/integration/test_validate_all_cli.py`
  - `tests/unit/test_cli_validate_commands.py`
  - `tests/unit/test_control_plane_loader_surfaces.py`
  - `tests/unit/test_standard_index_sync.py`

### Findings Matrix

- `1`: Not applicable in WatchTowerPlan. The repository intentionally hosts
  `pack.plan`, and the persisted registry correctly declares it as the default
  pack here.
- `2`: Not applicable in WatchTowerPlan. `plan/.wt/manifests/pack_settings.json`
  exists locally and the persisted hosted-pack entry is usable.
- `3`: Not applicable in WatchTowerPlan. The shared Python workspace should
  provision `watchtower-plan` in this repository because `plan` is the active
  hosted pack.
- `4`: Not applicable in WatchTowerPlan. The merged validator registry and the
  active hosted pack both resolve to `plan`, and the loader tests now pass.
- `5`: Not applicable in WatchTowerPlan. The merged validation-suite registry
  and the active hosted pack both resolve to `plan`, and the loader tests now
  pass.
- `6`: Not applicable in WatchTowerPlan. Activating the default pack resolves
  to the live local `plan/.wt/manifests/pack_settings.json`.
- `7`: Not applicable in WatchTowerPlan. The checked-in command index matches
  the current `watchtower-core plan ...` CLI surface.
- `8`: Not applicable in WatchTowerPlan. Repository-path discovery correctly
  indexes the live `plan/**` host shape.
- `9`: Not applicable in WatchTowerPlan. The route index is current for this
  repository and the route-bearing loader tests pass.
- `10`: Not applicable in WatchTowerPlan. Foundation discovery should cite
  `plan/**` surfaces because this repository directly hosts the plan pack.
- `11`: Not applicable in WatchTowerPlan. Standard discovery should resolve to
  plan-owned standards in this repository.
- `12`: Not applicable in WatchTowerPlan. Reference discovery should resolve to
  plan-owned guidance and workflows in this repository.
- `13`: Not applicable in WatchTowerPlan. Workflow discovery should resolve to
  the live `plan/workflows/**` surfaces in this repository.
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
- `22`: Not applicable in WatchTowerPlan. The repository validation baseline is
  green here, and the affected validation CLI tests currently pass.
- `23`: Already implemented in shared core and reverified here. The
  pack-placeholder portability fix in
  `core/python/tests/unit/test_standard_index_sync.py` remains green and no
  longer hard-codes donor-host `plan/...` paths when verifying externalized-pack
  behavior.

## Local Mapping in This Repository

### Current Repository Status

- Supporting authority for current repository validation, hosted-pack boundary,
  and portability-interpretation decisions in `WatchTowerPlan`.

### Current Touchpoints

- `core/control_plane/registries/pack_registry.json`
- `core/python/pyproject.toml`
- `plan/.wt/manifests/pack_settings.json`
- `core/python/tests/unit/test_control_plane_loader_surfaces.py`
- `core/python/tests/unit/test_standard_index_sync.py`
- `core/python/tests/unit/test_cli_validate_commands.py`
- `core/python/tests/integration/test_validate_all_cli.py`

### Why It Matters Here

- The report's import, purge, bootstrap, and rehost contract sections are
  recipient-repository guidance for a copied-core consumer whose active hosted
  pack is `oversight`.
- Those steps are not remediation instructions for WatchTowerPlan. Rewriting
  `core/control_plane/registries/pack_registry.json` or
  `core/python/pyproject.toml` from `plan` to `oversight` in this repository
  would be incorrect.
- The repository-level reasons are explicit in current local authority:
  - `plan/README.md` and
    `core/docs/foundations/repository_scope.md` define live planning authority
    under `plan/**`.
  - `plan/python/README.md` and
    `core/docs/standards/engineering/core_host_pack_python_boundary_standard.md`
    keep `plan/python/src/watchtower_plan/` as the approved plan-owned Python
    boundary for this repository.
- The report's literal `plan/` path findings remain intentional here when they
  describe the active WatchTowerPlan host shape rather than a pack-neutral copy
  contract.

### If Local Policy Tightens

- The report's placeholder sweep is not actionable in this repository today
  because the current validator baseline is green and no active document
  semantics failure remains in the cited shared standards.
- If a future repository copies shared core out of WatchTowerPlan, that
  recipient must still perform its own bootstrap and discovery rebuild instead
  of inheriting WatchTowerPlan host composition as-is.

## References

- [WatchTowerOversight core-swap integration assessment](https://github.com/mongoose1616/WatchTowerOversight/blob/HEAD/oversight/assessments/watchtowerplan_core_swap_integration_assessment.md)
- `core/docs/foundations/repository_scope.md`
- `core/docs/standards/engineering/core_host_pack_python_boundary_standard.md`
- `core/control_plane/registries/pack_registry.json`
- `plan/.wt/manifests/pack_settings.json`

## Notes

- This reference replaces the deleted
  `plan/docs/references/core_swap_integration_assessment_applicability_reference.md`
  path with the current closeout record under a different durable filename.
- Treat the external oversight-host assessment as a portability comparison, not
  as evidence that the current WatchTowerPlan repository is broken.

## Updated At

- `2026-03-28T23:55:00Z`
