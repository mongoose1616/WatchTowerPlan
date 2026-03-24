# `watchtower_plan.closeout`

## Summary
Plan-domain closeout services for live initiative packages and retained trace closeout that still depend on the current plan workspace layout.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: `watchtower_plan.closeout.InitiativeCloseoutService`, `InitiativePackageCloseoutHelper`, and related result types.
- `Non-Goals`: Reusable generic release automation, a second generic closeout framework inside the core package, or pack-agnostic closeout helpers that belong in reusable core.
- `Machine-State Boundary`: Operate on governed initiative state and evidence; do not treat this package as a second machine-state root.

## Key Surfaces
- `initiative.py`: Retained trace closeout orchestration that now runs under `watchtower-core plan closeout retained-initiative`, refuses live `plan/**` initiatives, and refreshes the affected indexes and rendered views.
- `initiative_package.py`: Initiative-package terminal closeout helper over initiative state, evidence, closeout recap, and promotion artifacts.

## Related Surfaces
- `plan/python/src/watchtower_plan/README.md`
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/docs/standards/governance/initiative_closeout_standard.md`

## Shrink Rules
- Keep `watchtower_plan.closeout` limited to repo-local closeout flows that still depend on live plan state and local retention policy.
- Move generic closeout helpers back into reusable core when they stop depending on the current plan workspace.
