# Copied Core Discovery Surface Reconciliation Followup

## Summary
Extends copied-core bootstrap so shared discovery surfaces converge beyond command and repository-path indexes, and updates copy-forward guidance to exclude runtime environment artifacts.

## Identity
- `initiative_id`: `initiative.copied_core_discovery_surface_reconciliation_followup`
- `trace_id`: `trace.copied_core_discovery_surface_reconciliation_followup`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.copied_core_discovery_surface_reconciliation_followup.bootstrap_copied_core_discovery_surface_reconciliation_followup`: Bootstrap Copied Core Discovery Surface Reconciliation Followup live initiative package.

## Problem
- Repeated copied-core reviews against `WatchTowerOversight` show that the original portability fixes landed, but one structural gap remains in reusable core.
- `watchtower-core pack bootstrap --write` currently reconciles the shared hosted-pack registry, shared `core/python/pyproject.toml`, shared command index, and shared repository-path index.
- After a raw `core/` copy, neighboring shared discovery surfaces can still retain donor `plan/**` state until a broader manual sync is run. The reproduced stale-surfaces cluster is:
  - `core/control_plane/indexes/references/reference_index.json`
  - `core/control_plane/indexes/standards/standard_index.json`
  - `core/control_plane/indexes/workflows/workflow_index.json`
  - `core/control_plane/indexes/routes/route_index.json`
- The copy-forward guidance is also still too weak. A downstream repo can copy `.venv`, editable-install metadata, caches, or runtime telemetry, which makes troubleshooting look like a core defect even when the stale environment is the real problem.

## Desired Outcome
- One `watchtower-core pack bootstrap --write` run on a copied-core repository reconciles all shared discovery surfaces that materially depend on the active hosted-pack composition.
- A copied-core consumer repo no longer needs a second implicit “run more shared sync commands until donor residue disappears” step just to get pack-neutral indexes.
- Core-owned docs tell downstream operators and future agents exactly what must not be copied with `core/` and what bootstrap is expected to reconcile afterward.
- `WatchTowerPlan` steady-state behavior stays unchanged; this slice only improves copied-core convergence.

## In Scope
- `core/python/src/watchtower_core/pack_integration/bootstrap.py`
- shared sync services or helpers needed to rebuild neighboring discovery surfaces during bootstrap
- copied-core regression fixtures and tests under `core/python/tests/**` and `plan/python/tests/**`
- core-owned bootstrap and copy-forward docs under `core/docs/**` and `core/python/**`

## Out Of Scope
- Oversight-owned fixes under `/home/j/WatchTowerOversight/oversight/**`
- Rewriting current `WatchTowerPlan` foundations or machine contracts that remain true in this repo
- A generic “copy the whole repository and self-heal everything” workflow
- Broad loader/query redesign beyond the copied-core bootstrap reconciliation boundary

## Operator Requirements
- Copying `core/` into a downstream repo and bootstrapping the active pack must produce a usable shared-core steady state without lingering donor route, workflow, reference, or standard discovery entries.
- Dry-run output must preview the wider set of changed paths accurately.
- Write mode must restore all touched shared surfaces on failure.
- Core-owned docs must make it explicit that `.venv`, caches, and runtime state are not part of the copy-forward contract.

## Acceptance Criteria
- `watchtower-core pack bootstrap --write` rebuilds the shared command, repository-path, reference, standard, workflow, and route indexes when the hosted-pack registry changes.
- Bootstrap dry runs report those additional changed paths when the broader reconciliation is needed.
- A copied-core fixture repo that starts with donor `plan` indexes and an unbootstrapped root pack ends with donor `plan/**` entries removed from the affected shared indexes after bootstrap.
- Core-owned command and authoring docs explain the stronger bootstrap reconciliation contract and the copy-forward exclusions clearly.

## Non Goals
- This initiative does not make raw copied repositories safe without an explicit bootstrap command.
- This initiative does not remove legitimate current-repo `plan` ownership facts from `WatchTowerPlan`.
- This initiative does not paper over bad downstream environments by treating copied `.venv` metadata as an approved workflow.
