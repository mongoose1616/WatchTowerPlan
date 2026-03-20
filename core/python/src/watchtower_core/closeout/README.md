# `watchtower_core.closeout`

## Summary
Fail-closed compatibility guard for the moved plan-domain closeout services.

## Boundary
- `Classification`: `boundary_guard`
- `Supported Imports`: None.
- `Non-Goals`: Owning live initiative closeout, initiative-package closeout helpers, or trace-purge orchestration inside reusable core.

## Key Surfaces
- `__init__.py`: Fails closed and redirects callers to `watchtower_plan.closeout`.

## Related Surfaces
- `plan/python/src/watchtower_plan/README.md`
- `plan/python/src/watchtower_plan/closeout/README.md`
- `plan/docs/standards/governance/initiative_closeout_standard.md`
