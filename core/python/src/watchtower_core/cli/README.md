# `watchtower_core.cli`

## Summary
Compatibility import surface plus the remaining command-family and handler modules for `watchtower-core`. The canonical root entrypoint, parser construction, registry metadata, and parser introspection now live under `watchtower_host.cli`.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: `watchtower_core.cli.main` as the compatibility import surface, plus explicit family and handler modules when changing command wiring.
- `Non-Goals`: Export-safe application framework APIs or reusable business logic.

## Key Surfaces
- `main.py`: Compatibility import surface for the host-owned root CLI entrypoint.
- `parser.py`: Compatibility import surface for the host-owned parser construction.
- `registry.py`: Compatibility import surface for the host-owned command registry metadata.
- `introspection.py`: Compatibility import surface for the host-owned parser metadata helpers.
- `*_family.py`: Command-group registration entrypoints, including grouped sync-family helpers.
- `*_handlers.py`: Runtime handler facades, including grouped sync document, tracking, and orchestration helpers.

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/cli/README.md` | Describes the CLI parser and handler boundary for `watchtower-core`. |
| `core/python/src/watchtower_host/cli/parser.py` | Host-owned parser construction for the `watchtower-core` binary. |
| `core/python/src/watchtower_core/cli/query_coordination_family.py` | Registers the planning-oriented query subcommands and their parser contracts. |
| `core/python/src/watchtower_core/cli/query_coordination_rendered_handlers.py` | Handles the coordination, initiative, and planning rendered query subcommands plus their shared payload formatting. |
| `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py` | Handles the authority, task, and trace lookup subcommands plus their direct payload formatting. |

## Related Surfaces
- `plan/python/src/watchtower_plan/README.md`
- `core/python/src/watchtower_host/README.md`
- `core/docs/commands/core_python/README.md`
