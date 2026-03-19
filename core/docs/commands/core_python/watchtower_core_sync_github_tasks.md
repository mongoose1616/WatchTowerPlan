# `watchtower-core sync github-tasks`

## Summary
This command pushes initiative-local live task records to GitHub issues and optional project items while keeping the local task records authoritative.

## Use When
- You need hosted GitHub visibility for one or more initiative-local live task records.
- You want to dry-run the GitHub task sync plan before making remote or local changes.
- You want the command to persist GitHub foreign keys back onto live task records and rebuild the derived task surfaces after a successful sync.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync github-tasks` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/sync_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync github-tasks [--repo <owner/name>] [--task-id <task_id>] [--trace-id <trace_id>] [--task-status <task_status>] [--owner <owner>] [--task-kind <task_kind>] [--project-owner <login>] [--project-owner-type <user|organization>] [--project-number <n>] [--no-label-sync] [--write] [--format <human|json>]
```

## Arguments and Options
- `--write`: Call the GitHub APIs, persist returned foreign keys locally, and rebuild derived task surfaces.
- `--repo <owner/name>`: GitHub repository in `owner/name` form. Falls back to existing task metadata or `GITHUB_REPOSITORY`.
- `--task-id <task_id>`: Exact task identifier filter. Repeat for multiple task IDs.
- `--trace-id <trace_id>`: Exact trace filter.
- `--task-status <task_status>`: Exact task-status filter.
- `--priority <priority>`: Exact priority filter.
- `--owner <owner>`: Exact owner filter.
- `--task-kind <task_kind>`: Exact task-kind filter.
- `--blocked-only`: Select only tasks that declare blocking task IDs.
- `--blocked-by <task_id>`: Select only tasks blocked by the given task ID.
- `--depends-on <task_id>`: Select only tasks that depend on the given task ID.
- `--project-owner <login>`: GitHub project owner login when also syncing to a project.
- `--project-owner-type <user|organization>`: GitHub project owner type when also syncing to a project.
- `--project-number <n>`: GitHub project number when also syncing to a project.
- `--project-status-field <name>`: GitHub single-select status field name. Defaults to `Status`.
- `--no-label-sync`: Skip the managed GitHub label upsert and label mirroring step.
- `--token-env <env_var>`: Environment variable that holds the GitHub token in write mode. Defaults to `GITHUB_TOKEN`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo
```

```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo --task-id task.local_task_tracking.github_sync.001 --write
```

```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo --project-owner owner --project-owner-type organization --project-number 7 --write --format json
```

```sh
cd core/python
uv run watchtower-core sync github-tasks --repo owner/repo --no-label-sync --write
```

## Behavior and Outputs
- The command is push-only: initiative-local live task records remain the source of truth.
- Task selection resolves through the live plan task query path and then loads the matched initiative-local task records before planning or applying GitHub updates.
- In dry-run mode, the command reports which tasks would create or update issues and project items without mutating GitHub or local files.
- Dry-run `watchtower-core sync github-tasks ...` is the authoritative preview surface for this command's filter set.
- In write mode, the command creates or updates GitHub issues, keeps a bounded managed label set aligned unless `--no-label-sync` is used, optionally updates project placement and status, persists GitHub foreign keys back onto the live task records, and rebuilds the live task indexes plus companion human trackers.
- The synced issue body mirrors the live task metadata, summary, scope, done-when criteria, dependencies, and a short local-authority note.
- In `human` mode, the command prints one result block per selected task.
- In `json` mode, the command prints one JSON object with aggregate counts, per-task sync records, managed labels, and any returned GitHub issue URL.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync task-index` | Rebuilds the machine-readable task index after live task metadata changes. |
| `watchtower-core sync task-tracking` | Rebuilds the human-readable task tracker after live task metadata changes. |
| `watchtower-core sync traceability-index` | Rebuilds traceability after traced task metadata changes. |
| `watchtower-core query tasks` | Reads the separate plan-workspace task index; it does not control GitHub task sync selection. |
| `watchtower-core task update` | Adjusts the authoritative live task metadata before the GitHub push step. |

## Source Surface
- `core/python/src/watchtower_core/cli/sync_family.py`
- `core/python/src/watchtower_core/plan_runtime/sync/github_tasks.py`
- `core/python/src/watchtower_core/integrations/github/client.py`
- `.github/`

## Updated At
- `2026-03-18T00:00:00Z`
