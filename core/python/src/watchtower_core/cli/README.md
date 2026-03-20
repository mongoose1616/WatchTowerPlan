# `watchtower_core.cli`

## Summary
Reusable command-family registration and handler helpers for shared `watchtower-core` commands. Host-owned parser construction, registry metadata, and parser introspection now live under `watchtower_host.cli`, while `main.py` remains as a thin forwarding shim so already-installed console scripts keep working.

## Boundary
- `Classification`: `reusable_core_cli_support`
- `Supported Imports`: `watchtower_core.cli.main` as a forwarding shim for existing console-script environments, plus explicit family, helper, and handler modules when changing shared root-command wiring.
- `Non-Goals`: Host-owned parser construction, host registry metadata, or parser introspection.

## Key Surfaces
- `main.py`: Thin forwarding shim for environments where the installed `watchtower-core` script still imports `watchtower_core.cli.main`.
- `*_family.py`: Command-group registration entrypoints, including grouped sync-family helpers.
- `*_handlers.py`: Runtime handler facades, including grouped sync document, tracking, and orchestration helpers.

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/cli/README.md` | Describes the shared CLI family and handler boundary for `watchtower-core`. |
| `core/python/src/watchtower_core/cli/main.py` | Forwarding shim that preserves the installed `watchtower-core` script while the host owns the real entrypoint. |
| `core/python/src/watchtower_host/cli/main.py` | Host-owned console entrypoint for the `watchtower-core` binary. |
| `core/python/src/watchtower_host/cli/parser.py` | Host-owned parser construction for the `watchtower-core` binary. |
| `core/python/src/watchtower_host/cli/registry.py` | Host-owned root command-family registry metadata. |
| `core/python/src/watchtower_host/cli/introspection.py` | Host-owned parser metadata for command-index rebuilds and CLI surface validation. |
| `core/python/src/watchtower_core/cli/query_family.py` | Registers the shared root `query` namespace for discovery, knowledge, and durable-record lookup. |
| `plan/python/src/watchtower_plan/cli/query.py` | Registers the pack-owned `plan query` namespace for live plan-state lookup. |
| `plan/python/src/watchtower_plan/cli/query_rendered_handlers.py` | Handles the plan query rendered-view commands such as coordination and initiatives. |
| `plan/python/src/watchtower_plan/cli/query_lookup_handlers.py` | Handles the plan query lookup commands such as authority, tasks, trace, and project context. |

## Related Surfaces
- `plan/python/src/watchtower_plan/README.md`
- `core/python/src/watchtower_host/README.md`
- `core/docs/commands/core_python/README.md`
