# `watchtower_host`

## Summary
`watchtower_host` owns the host-composition layer for the `watchtower-core` CLI. Keep parser construction, root command-family registration, root command handlers, command metadata introspection, and binary entrypoint wiring here rather than in the reusable-core package.

## Boundary
- `Classification`: `host_composition`
- `Supported Imports`: `watchtower_host.cli.main` for the console entrypoint and explicit `watchtower_host.cli.*` modules when changing CLI composition.
- `Non-Goals`: This package does not own reusable loaders, validators, query helpers, sync services, or pack-native orchestration.

## Key Surfaces
- `cli/main.py`: Host-owned console entrypoint for the `watchtower-core` binary.
- `cli/parser.py`: Registry-backed parser construction for the current host command tree.
- `cli/registry.py`: Root command-family registry metadata for the current host command tree.
- `cli/introspection.py`: Parser-backed command metadata used by command-index rebuilds and CLI surface validation.
- `cli/*_family.py`: Host-owned root command-family registration for `doctor`, `route`, `query`, `pack`, `sync`, and `validate`.
- `cli/*_handlers.py`: Host-owned root command handlers that delegate into reusable-core services.

## Related Surfaces
- `core/python/src/watchtower_core/README.md`
- `core/python/src/watchtower_core/cli/README.md`
- `plan/python/src/watchtower_plan/README.md`
