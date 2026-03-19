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

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/cli/README.md` | Describes the CLI parser and handler boundary for `watchtower-core`. |
| `core/python/src/watchtower_core/cli/query_coordination_family.py` | Registers the planning-oriented query subcommands and their parser contracts. |
| `core/python/src/watchtower_core/cli/query_coordination_rendered_handlers.py` | Handles the coordination, initiative, and planning rendered query subcommands plus their shared payload formatting. |
| `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py` | Handles the authority, task, and trace lookup subcommands plus their direct payload formatting. |

## Related Surfaces
- `core/python/src/watchtower_core/plan_runtime/README.md`
- `docs/commands/core_python/README.md`
