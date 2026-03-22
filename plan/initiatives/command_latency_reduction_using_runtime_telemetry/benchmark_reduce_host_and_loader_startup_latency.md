# Host And Loader Startup Latency Reduction

## Summary
- Captured on `2026-03-22T19:52:00Z` after the `reduce_host_and_loader_startup_latency` slice.
- The host CLI now scopes parser registration to the selected top-level command family when the namespace is explicit instead of rebuilding every core family parser on every invocation.
- Reusable-core package exports for `watchtower_core.control_plane` and `watchtower_core.pack_integration` now resolve lazily, so importing the host entrypoint no longer pays the cost of eager re-export fan-out.
- Host registry registration now imports command-family modules only when the selected family is actually being registered, and missing-pack probes avoid loading runtime manifests unnecessarily.

## Command Delta Against Baseline
| Command | Baseline Median (ms) | Current Median (ms) | Improvement (ms) | Improvement (%) |
| --- | ---: | ---: | ---: | ---: |
| `doctor` | `500.166` | `464.874` | `35.292` | `7.06` |
| `pack list --format json` | `432.497` | `401.883` | `30.614` | `7.08` |

## Additional Runtime Signal
- Importing `watchtower_host.cli.main` now measures at about `99.081 ms` from `python -X importtime`, down from the baseline `115.858 ms`.
- The startup slice reduced both the Python import envelope and the parser-registration work without changing stdout payloads, exit codes, or command routing.

## Implementation Notes
- [main.py](/home/j/WatchTowerPlan/core/python/src/watchtower_host/cli/main.py) now chooses the narrowest parser surface possible for explicit top-level commands.
- [registry.py](/home/j/WatchTowerPlan/core/python/src/watchtower_host/cli/registry.py) now uses lazy family registrars and registry-only pack namespace probing before it loads pack runtime manifests.
- [__init__.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/__init__.py) and [__init__.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/pack_integration/__init__.py) now expose the same public names through lazy exports instead of eager package fan-out.
- [query_family.py](/home/j/WatchTowerPlan/core/python/src/watchtower_host/cli/query_family.py) and [sync_family.py](/home/j/WatchTowerPlan/core/python/src/watchtower_host/cli/sync_family.py) now defer their heavier subfamily imports until registration time.

## Regression Guards
- [test_cli_startup_runtime_guards.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_cli_startup_runtime_guards.py) locks the selected-family parser behavior and the missing-pack fast path.
- [test_pack_validation_context_runtime_guards.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_pack_validation_context_runtime_guards.py) preserves the narrower validation-context surface loading that earlier latency work introduced.

## Notes
- The machine-readable companion for this note is `benchmark_reduce_host_and_loader_startup_latency.json`.
- The next initiative task is the tranche-level regression guard and final closeout pass.
