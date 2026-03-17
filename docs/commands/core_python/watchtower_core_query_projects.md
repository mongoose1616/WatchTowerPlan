# `watchtower-core query projects`

## Summary
This command searches the live project index for project containers, their linked repositories, and their initiative roots.

## Use When
- You need pack-level project lookup before loading one full project context.
- You want machine-readable project browse results for an agent, workflow, or script.
- You need to filter project containers by slug, status, or linked repository role.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query projects` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query projects [--query <text>] [--project-id <project_id>] [--slug <slug>] [--status <status>] [--repository-role <role>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over project fields such as project ID, slug, title, summary, and repository locators.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--slug <slug>`: Exact project slug such as `watchtower`.
- `--status <status>`: Exact project status filter such as `active` or `planned`.
- `--repository-role <role>`: Exact repository-role filter such as `implementation` or `planning`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query projects --slug watchtower
```

```sh
cd core/python
uv run watchtower-core query projects --repository-role implementation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints matching project IDs, statuses, initiative counts, linked repository roles, and project roots.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and project-entry records.
- The command reads `plan/.wt/indexes/project_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no project entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query project-context` | Loads one full validated project context after browse identifies the target project. |
| `watchtower-core query coordination` | Pack-level start-here path that can point you toward project-scoped work. |
| `watchtower-core query authority` | Resolves when project lookup is the canonical planning surface. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/projects.py`
- `plan/.wt/indexes/project_index.json`

## Updated At
- `2026-03-17T19:13:00Z`
