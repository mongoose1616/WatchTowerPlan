# Copied Core Doctor Pack Surface Neutrality

## Summary
Makes the generic doctor command tolerate copied-core repositories whose active pack does not publish plan-style live indexes such as task_index or initiative_index.

## Identity
- `initiative_id`: `initiative.copied_core_doctor_pack_surface_neutrality`
- `trace_id`: `trace.copied_core_doctor_pack_surface_neutrality`
- `scope_type`: `pack_wide`

## Problem
- Repeated copied-core reviews against `WatchTowerOversight` kept surfacing portability regressions even after the larger pack-bootstrap and discovery-surface fixes had landed.
- A deeper copied-repo smoke pass found one remaining generic host assumption in `watchtower-core doctor`: it unconditionally loaded `task_index` and `initiative_index`.
- That worked in `WatchTowerPlan` because the live `plan` pack declares those surfaces, but it broke a freshly scaffolded copied-core repo whose active pack publishes only the smaller starter surface set.

## Desired Outcome
- `watchtower-core doctor` remains a generic shared-core health snapshot rather than a `plan`-shaped command.
- Copied-core repositories with a valid hosted pack but no pack-owned live task or initiative indexes report `0` for those counts instead of failing.
- Shared pack-authoring docs make the rule explicit so future packs and future agent loops do not reintroduce the same assumption.

## In Scope
- `core/python/src/watchtower_host/cli/doctor_handlers.py`
- copied-core regression coverage under `core/python/tests/**`
- core-owned command and pack-authoring docs that need to explain the optional-surface rule
- the normal plan initiative package, validation, traceability refresh, and closeout surfaces for this change

## Out Of Scope
- changing Oversight-owned files directly
- making `validate all` or other pack-contract checks ignore real pack manifest errors
- redesigning the whole doctor payload or the full host telemetry surface
- reopening already-fixed copied-core bootstrap or discovery-index tranches unless new evidence shows they are still wrong

## Operator Requirements
- A copied repo that scaffolds and bootstraps a root pack such as `oversight/` must be able to run `watchtower-core doctor --format json` successfully before any plan-style live indexes exist.
- `doctor` must still fail if core governed surfaces genuinely cannot load; only absent optional pack-owned surfaces should collapse to `0`.
- The fix must be proven against a copied-core temp repo, not only against the donor `WatchTowerPlan` tree.

## Acceptance Criteria
- `watchtower-core doctor` succeeds in a copied-core root-pack smoke repo whose active pack does not declare `task_index` or `initiative_index`.
- The doctor payload reports `0` for those counts and preserves the normal recommended baseline behavior.
- Shared pack-authoring or contract docs state that pack-owned live indexes are optional and generic host commands must tolerate their absence.
- Targeted validation plus broad `watchtower-core validate all --skip-acceptance --format json` pass after the change.

## Non Goals
- turning `task_index` or `initiative_index` into deprecated surfaces for packs that do own them
- hiding broken pack settings or malformed manifests behind a fake successful doctor result
- modifying the recipient repo’s authored content in this donor-core fix

## Task Set
- `task.copied_core_doctor_pack_surface_neutrality.bootstrap_copied_core_doctor_pack_surface_neutrality`: bootstrap, confirm, approve, and close the initiative package
- `task.copied_core_doctor_pack_surface_neutrality.reproduce_neighbor_surface_failure`: reproduce the copied-core root-pack failure and confirm the exact generic-host boundary at fault
- `task.copied_core_doctor_pack_surface_neutrality.make_doctor_pack_surface_aware`: change doctor so optional pack-owned live indexes are loaded only when the active pack declares them
- `task.copied_core_doctor_pack_surface_neutrality.refresh_pack_authoring_guidance`: update the relevant core-owned command and pack-authoring docs so future pack work keeps the same contract
- `task.copied_core_doctor_pack_surface_neutrality.validate_and_closeout`: run copied-core smoke validation, broad repo validation, and close the initiative cleanly
