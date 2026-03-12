# `watchtower-core route preview`

## Summary
This command previews the routed workflow modules for either free-form request text or one explicit task type using the governed route and workflow indexes.

## Use When
- You want to see which workflow modules a request is likely to activate before executing the task.
- You already know the routed task type and want the exact required workflow set.
- You need structured JSON output for agent or workflow orchestration.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core route preview` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/route_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core route preview (--request <text> | --task-type <task_type>) [--format <human|json>]
```

## Arguments and Options
- `--request <text>`: Free-form request text to score against the governed route index.
- `--task-type <task_type>`: Exact routed task-type label from the governed route index.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core route preview --request "implement the feature and validate it"
```

```sh
cd core/python
uv run watchtower-core route preview --request "review code and commit the change" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "review the WatchTower report and fix the valid issues with planning, tasks, validation, and commits" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "review the workflow docs against the current CLI behavior and lookup surfaces" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --task-type "Foundations Alignment Review"
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- Exactly one route selector is required: either `--request` or `--task-type`.
- In `human` mode, the command prints the selected routed task types, matched trigger keywords, and the merged active workflow-module set.
- In `json` mode, the command prints one JSON object with the command name, selected routes, selected workflows, and any advisory warnings.
- Free-form request matching is deterministic and advisory. It scores exact phrases first, then falls back to exact normalized trigger-keyword token coverage plus full authored task-type token-set matches so realistic maintenance requests and audit prompts do not require verbatim routing-table phrasing while generic partial title overlap does not leak across routes.
- Foundations-aware documentation-alignment prompts can now select the explicit `Foundations Alignment Review` task type, which combines foundations context loading with documentation refresh.
- The authored routing surfaces remain authoritative when a human or agent executes the task.
- If no route matches the request text strongly enough, the command exits successfully with an empty selection plus a warning to refine the request or use `--task-type`.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core route` | Parent command group for route preview operations. |
| `watchtower-core sync route-index` | Rebuilds the route index this command reads. |
| `watchtower-core query workflows` | Searches the companion workflow index for the selected modules. |

## Source Surface
- `core/python/src/watchtower_core/cli/route_family.py`
- `core/python/src/watchtower_core/cli/route_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/routes.py`
- `core/control_plane/indexes/routes/route_index.v1.json`

## Updated At
- `2026-03-12T03:50:56Z`
