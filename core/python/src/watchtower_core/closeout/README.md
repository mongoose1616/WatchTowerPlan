# `watchtower_core.closeout`

## Summary
Fail-closed compatibility guard for moved pack-owned closeout services.

## Boundary
- `Classification`: `boundary_guard`
- `Supported Imports`: None.
- `Non-Goals`: Owning live initiative closeout, initiative-package closeout helpers, or trace-purge orchestration inside reusable core.

## Key Surfaces
- `__init__.py`: Fails closed and redirects callers to the owning `watchtower_<pack>.closeout` package.
