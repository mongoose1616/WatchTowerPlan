# `watchtower_core.cli`

## Summary
Reusable CLI support helpers plus the compatibility shim for stale console-script entrypoints. Host-owned parser construction, root command-family registration, handlers, registry metadata, and parser introspection now live under `watchtower_host.cli`.

## Boundary
- `Classification`: `reusable_core_cli_support`
- `Supported Imports`: Shared formatting, argument, handler, and sync-helper modules that pack-owned CLI namespaces reuse, plus `watchtower_core.cli.main` as the thin compatibility shim.
- `Non-Goals`: Host-owned parser construction, root command-family registration, root command handlers, host registry metadata, or parser introspection.

## Key Surfaces
- `main.py`: Thin compatibility shim that forwards stale console-script entrypoints to `watchtower_host.cli.main` without owning parser or dispatch logic.
- `common.py`: Shared help-formatting, common argument, and example helpers reused by pack-owned CLI namespaces.
- `handler_common.py`: Shared result-emission and error-shaping helpers reused by host and pack CLI handlers.
- `sync_family_common.py` and `sync_runtime_helpers.py`: Shared sync-command argument and runtime helpers reused by pack-owned sync namespaces.

## Files
| Path | Description |
|---|---|
| `core/python/src/watchtower_core/cli/README.md` | Describes the reusable CLI support-helper and compatibility boundary for `watchtower-core`. |
| `core/python/src/watchtower_core/cli/main.py` | Thin compatibility shim for console scripts that still target `watchtower_core.cli.main`. |
| `core/python/src/watchtower_core/cli/common.py` | Shared CLI formatting, argument, and example helpers reused by host and pack namespaces. |
| `core/python/src/watchtower_core/cli/handler_common.py` | Shared CLI result-emission and error-shaping helpers. |
| `core/python/src/watchtower_core/cli/sync_family_common.py` | Shared sync-command parser helpers reused by pack sync namespaces. |
| `core/python/src/watchtower_core/cli/sync_runtime_helpers.py` | Shared runtime helpers for sync commands that load services and shape results. |
| `core/python/src/watchtower_host/cli/main.py` | Host-owned console entrypoint for the `watchtower-core` binary. |
| `core/python/src/watchtower_host/cli/parser.py` | Host-owned parser construction for the `watchtower-core` binary. |
| `core/python/src/watchtower_host/cli/registry.py` | Host-owned root command-family registry metadata. |
| `core/python/src/watchtower_host/cli/introspection.py` | Host-owned parser metadata for command-index rebuilds and CLI surface validation. |
| `core/python/src/watchtower_host/cli/pack_family.py` | Registers the shared `pack` namespace for hosted-pack inspection and contract validation. |
| `core/python/src/watchtower_host/cli/query_family.py` | Registers the shared root `query` namespace for discovery, knowledge, and durable-record lookup. |

## Related Surfaces
- `core/python/src/watchtower_host/README.md`
- `core/docs/commands/core_python/README.md`
