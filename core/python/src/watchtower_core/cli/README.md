# `watchtower_core.cli`

## Summary
CLI parser construction, command-family registration, and handler wiring for `watchtower-core`.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: `watchtower_core.cli.main` for the executable entrypoint and explicit CLI submodules when changing command wiring.
- `Non-Goals`: Export-safe application framework APIs or reusable business logic.

## Key Surfaces
- `main.py`: Root CLI entrypoint.
- `parser.py`: Registry-backed parser construction.
- `*_family.py`: Command-group registration entrypoints, including grouped sync-family helpers.
- `*_handlers.py`: Runtime handler facades, including grouped sync document, tracking, and orchestration helpers.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/README.md`
- `docs/commands/core_python/README.md`
