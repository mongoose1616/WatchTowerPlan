# `watchtower_core.closeout`

## Summary
Repo-local closeout helpers for traced initiatives and adjacent future closeout flows.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: `watchtower_core.closeout.InitiativeCloseoutService`, `InitiativePackageCloseoutHelper`, and related result types.
- `Non-Goals`: Generic release automation or repo-specific path discovery hidden behind convenience imports.

## Key Surfaces
- `initiative.py`: Initiative closeout orchestration and result types.
- `initiative_package.py`: Pack-level initiative-package closeout coordination over initiative state, evidence, closeout recap, and promotion artifacts.

## Related Surfaces
- `core/python/src/watchtower_core/plan_runtime/README.md`
- `plan/docs/standards/governance/initiative_closeout_standard.md`
