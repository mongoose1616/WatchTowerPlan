# `watchtower-core plan sync`

## Summary
This command group rebuilds the plan-owned derived indexes, trackers, and orchestration slices that live under `plan/**` and `plan/.wt/**`.

## Use When
- You changed live plan state, plan-owned docs, standards, or workflow surfaces and need the derived pack surfaces refreshed.
- You need the coordination-only rebuild slice without running the broader root shared sync commands.
- You want structured dry-run or write output for plan-owned rebuild operations.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan sync` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/sync.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan sync <sync_command> [args]
```

## Arguments and Options
- `<sync_command>`: Choose a plan-owned leaf sync such as `all`, `coordination`, `initiative-index`, `task-index`, `traceability-index`, `initiative-tracking`, or `github-tasks`.
- `-h`, `--help`: Show the plan-sync group help text.
- Pass `--write`, `--output`, `--output-dir`, filter flags, and format flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core plan sync --help
```

```sh
cd core/python
uv run watchtower-core plan sync coordination --format json
```

```sh
cd core/python
uv run watchtower-core plan sync all --write --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- The group itself only routes help; the selected leaf command owns dry-run defaults, write behavior, output structure, and artifact-specific filters.
- Use `plan sync coordination` for the focused live task, traceability, initiative, and coordination slice.
- Use `plan sync all` when you need the full deterministic pack-owned rebuild across plan indexes and trackers.
- Use `plan sync github-tasks` when you need the push-only GitHub issue and project sync flow for matched live tasks.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan sync coordination` | Focused plan coordination rebuild slice. |
| `watchtower-core plan sync all` | Rebuilds the full deterministic plan-owned derived-artifact set. |
| `watchtower-core sync` | Rebuilds the reusable-core shared artifacts outside the plan pack. |
| `watchtower-core plan query coordination` | Reads one of the current-state plan surfaces that plan sync commands rebuild. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/sync.py`
- `plan/python/src/watchtower_plan/sync/`

## Updated At
- `2026-03-20T23:55:00Z`
