# `watchtower-core sync`

## Summary
This command group rebuilds reusable-core derived governed artifacts from authored repository sources. Use it to refresh shared machine-readable indexes and other deterministic byproducts after core-owned source changes land.

## Use When
- You changed an authored command, routing, README inventory, or other shared core-governed surface and need the derived artifacts to match.
- You need the fastest route to the correct rebuild command instead of scanning all sync leaf docs.
- You want structured dry-run or write output for automation.
- You need to distinguish between shared root sync commands and pack-owned `watchtower-core <pack-namespace> sync ...` commands.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync <sync_command> [args]
```

## Arguments and Options
- `<sync_command>`: Choose one reusable-core leaf sync such as `command-index`, `route-index`, or `repository-paths`.
- `-h`, `--help`: Show the sync-group help text.
- Pass `--write`, output-directory flags, and any narrower options to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core sync --help
```

```sh
cd core/python
uv run watchtower-core <pack-namespace> sync coordination --format json
```

```sh
cd core/python
uv run watchtower-core sync route-index --write --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- The group itself is routing help; the selected leaf command owns dry-run defaults, write behavior, and artifact-specific output.
- Root `sync` owns only reusable-core shared surfaces.
- Pack-owned sync operations now live under the owning pack namespace such as `watchtower-core <pack-namespace> sync ...`.
- Cache-aware leaf sync commands may return `cache_status` and `cache_input_count` in JSON output so automation can tell warm-cache hits from rebuilds.
- Warm runs may reuse the canonical artifact when the declared sync inputs and canonical output hash are unchanged.
- Runtime sync cache manifests live under `<machine_root>/runtime/sync_cache/` when an active or default pack machine root is available, or under `core/python/.cache/watchtower/sync_cache/` as the reusable-core fallback.
- Portable export and staged bootstrap flows may rebuild sync surfaces while still disabling runtime cache emission into the staged artifact.
- Use narrower root leaf commands when one shared governed family changed and you do not need the pack-owned rebuild flows.
- Open the specific leaf command page or CLI help when you need exact flags, dependency order, or output-file details.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core <pack-namespace> sync coordination` | Focused live pack rebuild slice. |
| `watchtower-core sync route-index` | Rebuilds the machine-readable routing surface from the routing table. |
| `watchtower-core <pack-namespace> sync all` | Rebuilds the full deterministic pack-owned derived-artifact set. |
| `watchtower-core <pack-namespace> query coordination` | Reads one of the current-state surfaces that sync commands rebuild. |

## Source Surface
- `core/python/src/watchtower_host/cli/sync_family.py`
- `core/python/src/watchtower_host/cli/sync_handlers.py`
- `core/python/src/watchtower_core/sync/`

## Updated At
- `2026-04-04T21:20:00Z`
