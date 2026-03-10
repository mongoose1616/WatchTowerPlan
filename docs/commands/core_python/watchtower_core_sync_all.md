# `watchtower-core sync all`

## Summary
This command rebuilds all local deterministic indexes and human-readable trackers in one run, using the registry-backed sync target set in dependency order.

## Use When
- You changed several authored planning, standards, command, or reference surfaces and want one coordinated local rebuild.
- You want to materialize the full local derived state into a separate directory for inspection.
- You want a bounded alternative to manually running many sync commands in sequence.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync all` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync all [--write] [--output-dir <dir>] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write rebuilt indexes and trackers to their canonical repository paths.
- `--output-dir <dir>`: Optional explicit directory for materializing every rebuilt surface while preserving repo-relative paths below that directory.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync all
```

```sh
cd core/python
uv run watchtower-core sync all --write
```

```sh
cd core/python
uv run watchtower-core sync all --output-dir /tmp/watchtower_sync --format json
```

## Behavior and Outputs
- The command runs the registry-backed local deterministic sync target set in dependency order so later rebuilds can read the earlier generated surfaces from disk when needed.
- The current target set includes command, foundation, reference, standard, workflow, PRD, decision, design, initiative, task, traceability, and repository-path indexes, plus the PRD, decision, design, initiative, and task trackers.
- The command does not call hosted integrations. It intentionally excludes `sync github-tasks`.
- With no mutation flags, the command runs in dry-run mode and only reports what would be rebuilt.
- With `--write`, the command writes each rebuilt surface back to its canonical repository path.
- With `--output-dir`, the command writes every rebuilt surface into the selected directory while preserving each surface's repo-relative path.
- In `json` mode, the command returns one result object per rebuilt target with its output path and record count.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core sync command-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync foundation-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync reference-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync standard-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync workflow-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync traceability-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync initiative-index` | Rebuilds one of the surfaces included in `sync all`. |
| `watchtower-core sync initiative-tracking` | Rebuilds one of the surfaces included in `sync all`. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/all.py`
- `core/python/src/watchtower_core/sync/registry.py`

## Updated At
- `2026-03-10T05:24:43Z`
