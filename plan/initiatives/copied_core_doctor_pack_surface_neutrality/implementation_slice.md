# Copied Core Doctor Pack Surface Neutrality Implementation Slice

## Summary
Makes the generic doctor command tolerate copied-core repositories whose active pack does not publish plan-style live indexes such as task_index or initiative_index.

## Work Breakdown
- `task.copied_core_doctor_pack_surface_neutrality.bootstrap_copied_core_doctor_pack_surface_neutrality`
  - author the initiative inputs
  - confirm and approve the package
  - close the bootstrap task once execution is ready
- `task.copied_core_doctor_pack_surface_neutrality.reproduce_neighbor_surface_failure`
  - rerun the copied-core smoke with a first-party root pack
  - confirm the exact crash path and the affected adjacent host surfaces
- `task.copied_core_doctor_pack_surface_neutrality.make_doctor_pack_surface_aware`
  - update the doctor handler to conditionally load only declared optional pack-owned live indexes
  - keep shared governed-surface loading unchanged
- `task.copied_core_doctor_pack_surface_neutrality.refresh_pack_authoring_guidance`
  - update the doctor command page
  - update shared pack-interface and pack-authoring guidance so the optional-surface rule is explicit
- `task.copied_core_doctor_pack_surface_neutrality.validate_and_closeout`
  - run targeted validation
  - rerun the copied-core neighboring-surface smoke
  - run broad repository validation
  - close and commit the initiative if the tree is clean

## Commit Boundaries
- Commit 1: doctor handler fix plus copied-core regression coverage
- Commit 2: contract/reference doc refresh plus initiative closeout surfaces, if a second commit is needed

## Validation Commands
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_host/cli/doctor_handlers.py core/python/tests/integration/test_copied_core_doctor.py core/docs/commands/core_python/watchtower_core_doctor.md core/docs/standards/data_contracts/pack_interface_contract_standard.md core/docs/references/domain_pack_authoring_reference.md`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_host/cli/doctor_handlers.py`
- `cd core/python && ./.venv/bin/python -m pytest tests/integration/test_copied_core_doctor.py -q`
- copied-core manual smoke: scaffold root-pack `oversight`, bootstrap it, then run `doctor`, `pack validate`, `validate all`, and adjacent generic query surfaces
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Closeout Criteria
- `watchtower-core doctor` no longer crashes in a copied-core repo whose active pack omits `task_index` and `initiative_index`
- the copied-core neighboring-surface smoke finds no new generic-host portability regressions after the doctor fix
- shared command and pack-authoring docs describe the optional-surface rule clearly
- repo coordination returns to `ready_for_bootstrap`
- the worktree is clean after commit

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
