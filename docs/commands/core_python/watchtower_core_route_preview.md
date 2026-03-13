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
uv run watchtower-core route preview --request "reconcile command docs with current cli behavior" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "reconcile schema-backed indexes examples and validators for one artifact family" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "do a documentation review of the command docs" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "hand off this task from implementation to validation and create successor tasks" --format json
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
- Free-form request matching is deterministic and advisory. It scores exact phrases first, then falls back to canonicalized trigger-keyword coverage so realistic maintenance requests and adjacent-route prompts do not require verbatim routing-table phrasing.
- When one route is materially stronger than the others, the preview keeps only the dominant route plus any materially strong secondary matches instead of leaking in low-signal single-word matches. Successor-task handoff prompts stay on `Task Phase Transition` even though that workflow later opens the lifecycle rules as supporting context.
- Bounded documentation and standards review prompts now route to `Documentation Review` instead of falling through to no match or a broad repository review.
- Foundations-aware documentation-alignment prompts can now select the explicit `Foundations Alignment Review` task type, which combines foundations context loading with documentation refresh.
- Adjacent route boundaries worth remembering:
  - Use `Documentation-Implementation Reconciliation` for command docs, README, example, or lookup-surface drift around live behavior.
  - Use `Governed Artifact Reconciliation` for schema, example, index, registry, or validator coherence inside one artifact family.
  - Use `Traceability Reconciliation` for traced planning links, trackers, and family-index drift.
  - Use `Task Lifecycle Management` for creating or editing task records; use `Task Phase Transition` when the main action is a handoff or successor-task boundary, including creating successor tasks for the next phase.
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
- `2026-03-13T21:40:13Z`
