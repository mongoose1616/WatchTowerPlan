# `watchtower-core sync`

## Summary
This command group rebuilds derived governed artifacts from authored repository sources. Use it to refresh machine-readable indexes, human-readable trackers, and other deterministic byproducts after source changes land.

## Use When
- You changed an authored planning, workflow, command, standards, or control-plane surface and need the derived artifacts to match.
- You need the fastest route to the correct rebuild command instead of scanning all sync leaf docs.
- You want structured dry-run or write output for automation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync <sync_command> [args]
```

## Arguments and Options
- `<sync_command>`: Choose a leaf sync such as `all`, `coordination`, `planning-catalog`, `route-index`, `workflow-index`, `initiative-index`, `task-index`, `repository-paths`, or another narrower tracker or index refresh.
- `-h`, `--help`: Show the sync-group help text.
- Pass `--write`, output-directory flags, and any narrower options to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core sync --help
```

```sh
cd core/python
uv run watchtower-core sync coordination --format json
```

```sh
cd core/python
uv run watchtower-core sync planning-catalog --write --format json
```

```sh
cd core/python
uv run watchtower-core sync route-index --write --format json
```

```sh
cd core/python
uv run watchtower-core sync all --write --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- The group itself is routing help; the selected leaf command owns dry-run defaults, write behavior, and artifact-specific output.
- Use `sync coordination` for the focused task, traceability, initiative, planning-catalog, coordination-index, and coordination-tracker rebuild slice.
- Use `sync all` when you need the full deterministic local rebuild across indexes and trackers.
- Use narrower leaf commands when one governed family changed and you do not need the full repo rebuild.
- Open the specific leaf command page or CLI help when you need exact flags, dependency order, or output-file details.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync coordination` | Focused current-state planning rebuild slice. |
| `watchtower-core sync planning-catalog` | Rebuilds the canonical deep planning join. |
| `watchtower-core sync route-index` | Rebuilds the machine-readable routing projection from the routing table. |
| `watchtower-core sync all` | Rebuilds the full deterministic local derived-artifact set. |
| `watchtower-core query coordination` | Reads one of the current-state surfaces that sync commands rebuild. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/cli/sync_handlers.py`
- `core/python/src/watchtower_core/repo_ops/sync/`

## Updated At
- `2026-03-13T15:05:00Z`
