# `watchtower_host.cli`

## Summary
Host-owned CLI composition for the `watchtower-core` binary. Keep the console
entrypoint, parser construction, root command registry, and parser metadata
introspection here.

## Boundary
- `Classification`: `host_composition`
- `Supported Imports`: `watchtower_host.cli.main`, `watchtower_host.cli.parser`, `watchtower_host.cli.registry`, and `watchtower_host.cli.introspection`.
- `Non-Goals`: Shared command-family helpers that belong in `watchtower_core.cli`, or pack-native CLI namespaces that belong in `watchtower_plan.cli` and future `watchtower_<pack>.cli` packages.

## Key Surfaces
- `main.py`: Console entrypoint used by the `watchtower-core` script.
- `parser.py`: Root parser construction for the hosted command tree.
- `registry.py`: Root command-family registry metadata for core commands and registered packs.
- `introspection.py`: Parser-backed metadata used by command-index rebuilds and CLI validation.
- `closeout.py`: Host-owned retained-trace closeout family that composes reusable core helpers with pack-native closeout services.

## Related Surfaces
- `core/python/src/watchtower_host/README.md`
- `core/python/src/watchtower_core/cli/README.md`
- `plan/python/src/watchtower_plan/cli/README.md`
