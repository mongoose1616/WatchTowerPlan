# `watchtower_host.cli`

## Summary
Host-owned CLI composition for the `watchtower-core` binary. Keep the console
entrypoint, parser construction, root command-family registration, root command
handlers, root command registry, and parser metadata introspection here.

## Boundary
- `Classification`: `host_composition`
- `Supported Imports`: `watchtower_host.cli.main`, parser and registry modules, and the host-owned root `*_family.py` and `*_handlers.py` modules when changing the shared CLI tree.
- `Non-Goals`: Reusable CLI support helpers that belong in `watchtower_core.cli`, or pack-native CLI namespaces that belong in `watchtower_plan.cli` and future `watchtower_<pack>.cli` packages.

## Key Surfaces
- `main.py`: Console entrypoint used by the `watchtower-core` script.
- `parser.py`: Root parser construction for the hosted command tree.
- `registry.py`: Root command-family registry metadata for core commands and registered packs.
- `introspection.py`: Parser-backed metadata used by command-index rebuilds and CLI validation.
- `doctor_family.py`, `route_family.py`, `query_family.py`, `pack_family.py`, `sync_family.py`, `validate_family.py`: Host-owned root command-family registration.
- Matching `*_handlers.py` modules: Host-owned root command handlers that delegate to reusable-core runtime surfaces, including the hosted-pack inspection, scaffold, and validation flows.

## Related Surfaces
- `core/python/src/watchtower_host/README.md`
- `core/python/src/watchtower_core/cli/README.md`
- `plan/python/src/watchtower_plan/cli/README.md`
