# Copy-Forward Pack Runtime Hardening

## Summary
Hardens reusable core for copied-core host scenarios by discovering unbootstrapped hosted packs from manifests, structuring stale-registry failures, and keeping current shared workspace contracts explicit.

## Identity
- `initiative_id`: `initiative.copy_forward_pack_runtime_hardening`
- `trace_id`: `trace.copy_forward_pack_runtime_hardening`
- `scope_type`: `pack_wide`

## Problem
The current reusable core behaves correctly inside this repository, where `pack.plan` is authored in the shared hosted-pack registry and `watchtower-plan` is installed through the shared `core/python` workspace. That same donor core degrades poorly after a direct copy into a consuming repository that carries a different first-party/root pack but has not yet rewritten the copied registry and workspace metadata.

The external assessment under `/home/j/WatchTowerOversight/oversight/assessments/watchtowerplan_core_swap_integration_assessment.md` confirms that some findings are stale, such as the old schema-catalog canonical-root rejection, while other core-owned findings still expose real donor-core weaknesses:
- host discovery and selected pack routing still depend too heavily on the authored `pack_registry.json`
- selected pack commands degrade poorly when the authored registry contains stale or missing manifest paths
- copied-core adoption before `pack bootstrap` is not clearly separated from the steady-state shared workspace contract

## Desired Outcome
- A copied `core/` can discover a valid first-party/root pack from its manifests for bootstrap-mode host behavior before the consuming repository rewrites the authored registry and shared workspace metadata.
- `watchtower-core pack list`, `pack describe`, `pack validate --pack <slug>`, and selected top-level pack namespace discovery degrade structurally instead of failing on stale donor registry state.
- Current repository behavior stays intact: the internal `plan` pack remains the authored default repo pack in `WatchTowerPlan`, and the shared `core/python` workspace contract remains explicit rather than being silently removed.

## In Scope
- Reusable-core loader, pack-runtime, and host CLI changes under `core/python/src/watchtower_core/**` and `core/python/src/watchtower_host/**`
- Companion reusable-core tests under `core/python/tests/**`
- Shared pack-interface and Python-workspace docs under `core/docs/**` when the runtime contract changes materially
- Initiative tracking, validation evidence, and closeout surfaces under this initiative package

## Out Of Scope
- Editing `WatchTowerOversight/oversight/**`
- Replacing the current authored `pack.plan` entry in `WatchTowerPlan/core/control_plane/registries/pack_registry.json`
- Removing the current `watchtower-plan` shared workspace installation contract from `WatchTowerPlan/core/python/pyproject.toml`
- Changing current-repo derived indexes such as the command index or repository-path index to pretend this repository does not host `plan`
- Fixing Oversight pack-owned duplicate validator IDs or other Oversight-owned residue

## Operator Requirements
- Host commands must remain usable when the copied authored registry is stale for the consuming repository.
- Pack discovery for copy-forward bootstrap mode must be manifest-driven and deterministic.
- Bootstrap-mode runtime fallback must not hide the steady-state requirement that consuming repositories should still rewrite their authored hosted-pack registry and shared workspace metadata.
- Pack command stdout payloads and exit-code contracts must remain stable; improvements should favor additive structured detail and better failure handling rather than breaking output shape.

## Acceptance Criteria
- A root-pack or nested-pack fixture can be discovered from `<pack>/.wt/manifests/pack_settings.json` or `packs/<slug>/.wt/manifests/pack_settings.json` even when the authored registry still points at stale donor manifests.
- `watchtower-core pack list --format json` includes discovered bootstrap-mode packs instead of reporting only stale donor registry entries.
- `watchtower-core pack describe --pack <slug> --format json` returns a structured error payload instead of a raw traceback when the selected authored registry entry points at missing manifests.
- Selected pack namespace discovery can expose a discovered pack command group without requiring the consuming repository to pre-edit the donor registry first.
- Runtime and docs clearly distinguish:
  - steady-state hosted-pack registration through `pack_registry.json` plus shared `core/python` workspace metadata
  - bootstrap-mode discovery used only to keep copied-core adoption diagnosable and operable before rewiring
- Targeted tests and the normal validation loop pass.

## Non-Goals
- Do not make donor-core magically rewrite a consuming repository automatically on import.
- Do not weaken pack-contract validation so far that missing shared workspace registration or stale authored registry state becomes invisible.
- Do not introduce a second dynamic plugin-discovery authority that supersedes the authored pack registry once bootstrap is complete.

## Initial Task Set
- `task.copy_forward_pack_runtime_hardening.bootstrap_copy_forward_pack_runtime_hardening`: Bootstrap Copy-Forward Pack Runtime Hardening live initiative package.
