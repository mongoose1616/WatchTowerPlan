# `watchtower-core query project-context`

## Summary
This command loads one project-scoped runtime context from machine-authoritative project artifacts on top of the always-loaded pack context.

## Use When
- A command, workflow, or implementation step targets exactly one project under `plan/projects/**`.
- You need the validated project record, initiative root, and linked repositories without depending on rendered project views.
- You want a narrow proof surface that `project_context` loads separately from `pack_context`.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query project-context` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query project-context --project-slug <project_slug> [--format <human|json>]
```

## Arguments and Options
- `--project-slug <project_slug>`: Required project slug such as `watchtower`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query project-context --project-slug watchtower
```

```sh
cd core/python
uv run watchtower-core query project-context --project-slug watchtower --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- The command always loads `pack_context` first, then loads one explicit `project_context` from `plan/projects/<project_slug>/.wt/project.json` and `.wt/project_repository_map.json`.
- Rendered drift in `project.md`, `repositories.md`, `summary.md`, or pack-level project indexes does not block this context load; the command trusts machine-authoritative project artifacts instead of derived views.
- In `human` mode, the command prints the project identity, pack-context source, project and initiative roots, and linked repositories.
- In `json` mode, the command prints one JSON object with pack-context metadata plus the loaded project context payload.
- If the project container is missing or its machine artifacts are invalid, the command fails closed and reports the validation problem.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query coordination` | Pack-level current-state entrypoint before narrowing to one project. |
| `watchtower-core query initiatives` | Project-scoped initiative lookup once the project root is known. |
| `watchtower-core query trace` | Trace-linked initiative lookup after you know the exact trace you need. |
| `watchtower-core query authority` | Canonical-surface resolver when you are not sure which machine surface to trust. |
| `watchtower-core sync all` | Rebuilds command docs, live plan indexes, and retained companion surfaces after query-surface changes. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `plan/python/src/watchtower_plan/project_context.py`
- `plan/projects/<project_slug>/.wt/project.json`
- `plan/projects/<project_slug>/.wt/project_repository_map.json`

## Updated At
- `2026-03-19T20:15:00Z`
