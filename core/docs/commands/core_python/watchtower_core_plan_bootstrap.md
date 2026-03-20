# `watchtower-core plan bootstrap`

## Summary
This command bootstraps one live initiative package under `plan/**`, including authored package inputs, initiative-local machine state, an acceptance contract, a planning-baseline evidence artifact, and one bootstrap task.

## Use When
- You want to start a new traced initiative package without hand-authoring each package surface from scratch.
- You need the initial initiative-authored inputs, acceptance contract, evidence artifact, and bootstrap task to share one trace and coherent derived planning surfaces.
- You want dry-run preview before writing the package to canonical `plan/**` paths.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan bootstrap` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id <trace_id> [--initiative-slug <initiative_slug>] [--project-slug <project_slug>] --title <title> --summary <summary> [--owner <owner>] [--include-decision] [--task-id <task_id>] [--task-owner <owner>] [--task-kind <kind>] [--task-priority <priority>] [--updated-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier for the full chain.
- `--initiative-slug <initiative_slug>`: Optional initiative slug. Defaults to a slug derived from the trace ID.
- `--project-slug <project_slug>`: Optional project slug for project-scoped initiative bootstrap.
- `--title <title>`: Initiative title root used to derive the authored package titles.
- `--summary <summary>`: One-line initiative summary applied to the live package.
- `--owner <owner>`: Initiative owner recorded in authored inputs and task state. Defaults to `repository_maintainer`.
- `--include-decision`: Also create `decision_notes.md` in the initial package.
- `--task-id <task_id>`: Optional explicit bootstrap task ID. Defaults to `task.<trace_suffix>.bootstrap.001`.
- `--task-owner <owner>`: Optional bootstrap task owner. Defaults to `--owner`.
- `--task-kind <feature|bug|chore|documentation|governance|research|validation>`: Bootstrap task kind. Defaults to `governance`.
- `--task-priority <critical|high|medium|low>`: Bootstrap task priority. Defaults to `medium`.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now.
- `--write`: Persist the initiative package, acceptance contract, evidence artifact, and refresh derived plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative."
```

```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative." --include-decision --task-priority high --write --format json
```

```sh
cd core/python
uv run watchtower-core plan bootstrap --project-slug watchtower --trace-id trace.watchtower.example --title "WatchTower Initiative" --summary "Bootstraps a project-scoped initiative." --write
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not create files.
- The bootstrap flow creates `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, the optional `decision_notes.md`, an acceptance contract, a planning-baseline evidence artifact, and one bootstrap task.
- Document titles and IDs are derived from the trace suffix and the bootstrap task defaults to `task.<trace_suffix>.bootstrap.001` unless overridden.
- In write mode, the command seeds the live initiative package into the pre-execution review path. Use `watchtower-core plan confirm-inputs` and `watchtower-core plan approve` before transitioning tasks into execution-starting statuses such as `in_progress`, `in_review`, or `completed`.
- In write mode, the command writes the initiative package, the acceptance contract, the planning-baseline evidence artifact, and refreshes derived task, initiative, traceability, and coordination surfaces.
- While the bootstrap task is the only active task for the trace, initiative rendered surfaces keep the trace in `capture`; the phase moves to `execution` only after non-bootstrap active work exists.
- In `json` mode, the command prints one JSON object with the initiative package outcome, acceptance contract, validation evidence, and bootstrap task result.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for live initiative-package bootstrap and readiness operations. |
| `watchtower-core plan confirm-inputs` | Records reviewed initiative-authored inputs before readiness approval. |
| `watchtower-core plan approve` | Approves the live initiative package into `ready_for_execution`. |
| `watchtower-core task` | Manages the bootstrap task or any follow-up tasks created after the chain exists. |
| `watchtower-core sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |
| `watchtower-core closeout plan-initiative` | Use after the bootstrap task and its successors are terminal on the live `plan/**` initiative package. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/handlers.py`
- `plan/python/src/watchtower_plan/cli/namespace.py`
- `plan/python/src/watchtower_plan/initiative_packages.py`

## Updated At
- `2026-03-19T21:35:00Z`
