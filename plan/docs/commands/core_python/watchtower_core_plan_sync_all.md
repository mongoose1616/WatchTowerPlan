# `watchtower-core plan sync all`

## Summary
This command rebuilds all local deterministic indexes and human-readable trackers in one run, using the registry-backed sync target set in dependency order.

## Use When
- You changed several authored planning, standards, command, or reference surfaces and want one coordinated local rebuild.
- You want to materialize the full local derived state into a separate directory for inspection.
- You want a bounded alternative to manually running many sync commands in sequence.
- You do not want the narrower `sync coordination` slice because you need more than the coordination surfaces refreshed.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan sync all` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/sync.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan sync all [--write] [--output-dir <dir>] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write rebuilt indexes and trackers to their canonical repository paths.
- `--output-dir <dir>`: Optional explicit directory for materializing every rebuilt surface while preserving repo-relative paths below that directory.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan sync all
```

```sh
cd core/python
uv run watchtower-core plan sync all --write
```

```sh
cd core/python
uv run watchtower-core plan sync all --output-dir /tmp/watchtower_plan_sync --format json
```

## Behavior and Outputs
- The command runs the registry-backed local deterministic sync target set in dependency order so later rebuilds can read the earlier generated surfaces from disk when needed.
- The current target set includes foundation, reference, standard, workflow, initiative, task, review, traceability, coordination, and repository-path indexes, plus the coordination, initiative, and task trackers.
- The command does not call hosted integrations. It intentionally excludes `sync github-tasks`.
- With no mutation flags, the command runs in dry-run mode and only reports what would be rebuilt.
- With `--write`, the command writes each rebuilt surface back to its canonical repository path.
- With `--output-dir`, the command writes every rebuilt surface into the selected directory while preserving each surface's repo-relative path.
- In `json` mode, the command returns one result object per rebuilt target with its output path and record count.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core plan sync coordination` | Rebuilds the smaller task, traceability, initiative, and coordination slice when `sync all` would be unnecessarily broad. |
| `watchtower-core sync command-index` | Rebuilds one shared governed surface that often changes in the same broader repository slice. |
| `watchtower-core plan sync foundation-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync reference-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync standard-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync workflow-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync review-index` | Rebuilds one of the live plan-workspace review surfaces included in `sync all`. |
| `watchtower-core plan sync traceability-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync initiative-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core plan sync initiative-tracking` | Rebuilds one of the surfaces included in `sync all`. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/sync.py`
- `plan/python/src/watchtower_plan/sync/all.py`
- `plan/python/src/watchtower_plan/sync/registry.py`

## Updated At
- `2026-03-21T03:12:00Z`
