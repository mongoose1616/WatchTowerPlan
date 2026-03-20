# `watchtower_plan.closeout`

## Summary
Plan-domain closeout services for live initiative packages, retained trace closeout, and guarded trace purges.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: `watchtower_plan.closeout.InitiativeCloseoutService`, `TracePurgeService`, `InitiativePackageCloseoutHelper`, and related result types.
- `Non-Goals`: Reusable generic release automation or a second generic closeout framework inside the core package.

## Key Surfaces
- `initiative.py`: Retained trace closeout orchestration that refuses live `plan/**` initiatives and refreshes the affected indexes and rendered views.
- `initiative_package.py`: Initiative-package terminal closeout helper over initiative state, evidence, closeout recap, and promotion artifacts.
- `purge_trace.py`: Guarded trace-package purge orchestration and minimal surviving purge-ledger writes.

## Related Surfaces
- `plan/python/src/watchtower_plan/README.md`
- `core/python/src/watchtower_core/cli/closeout_handlers.py`
- `plan/docs/standards/governance/initiative_closeout_standard.md`
