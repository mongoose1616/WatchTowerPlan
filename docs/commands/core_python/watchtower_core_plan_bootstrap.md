# `watchtower-core plan bootstrap`

## Summary
This command scaffolds a compact traced PRD, feature design, implementation plan, acceptance contract, planning-baseline evidence artifact, and bootstrap task chain, with an optional decision record, and refreshes derived planning surfaces in write mode.

## Use When
- You want to start a new traced planning chain without hand-authoring each planning artifact from scratch.
- You need the initial PRD, design, plan, acceptance contract, evidence artifact, and bootstrap task to share one trace and coherent derived planning surfaces.
- You want dry-run preview before writing the scaffold chain to canonical planning paths.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan bootstrap` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/plan_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id <trace_id> --title <title> --summary <summary> [--owner <owner>] [--applies-to <path_or_concept>] [--alias <alias>] [--file-stem <stem>] [--include-decision] [--decision-id <id>] [--source-request <text>] [--reference <source>] [--task-id <task_id>] [--task-owner <owner>] [--task-kind <kind>] [--task-priority <priority>] [--updated-at <timestamp>] [--include-documents] [--write] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier for the full chain.
- `--title <title>`: Initiative title root used to derive document titles.
- `--summary <summary>`: One-line initiative summary applied to the scaffold chain.
- `--owner <owner>`: Planning-document owner recorded in front matter. Defaults to `repository_maintainer`.
- `--applies-to <path_or_concept>`: Optional applied path or concept. Repeat for multiple values.
- `--alias <alias>`: Optional retrieval alias. Repeat for multiple values.
- `--file-stem <stem>`: Optional shared filename stem for the scaffolded planning documents.
- `--include-decision`: Also create an initial decision record in the bootstrap chain.
- `--decision-id <id>`: Optional explicit decision ID when `--include-decision` is used.
- `--source-request <text>`: Optional source request or driver. Repeat for multiple values.
- `--reference <source>`: Optional companion reference or source. Repeat for multiple values.
- `--task-id <task_id>`: Optional explicit bootstrap task ID. Defaults to `task.<trace_suffix>.bootstrap.001`.
- `--task-owner <owner>`: Optional bootstrap task owner. Defaults to `--owner`.
- `--task-kind <feature|bug|chore|documentation|governance|research>`: Bootstrap task kind. Defaults to `governance`.
- `--task-priority <critical|high|medium|low>`: Bootstrap task priority. Defaults to `medium`.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now.
- `--include-documents`: Include rendered document content in the command output.
- `--write`: Persist the scaffold chain, acceptance contract, evidence artifact, and refresh derived planning surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative."
```

```sh
cd core/python
uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative." --include-decision --task-priority high --include-documents --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not create files.
- The bootstrap flow creates a PRD, feature design, implementation plan, acceptance contract, planning-baseline evidence artifact, and one bootstrap task. Add `--include-decision` to include a first decision record in the same chain.
- Document IDs are derived from the trace suffix and the bootstrap task defaults to `task.<trace_suffix>.bootstrap.001` unless overridden.
- In write mode, the command writes the scaffold chain, the acceptance contract, the planning-baseline evidence artifact, and refreshes derived planning, task, initiative, traceability, and coordination surfaces.
- In `json` mode, the command prints one JSON object with the scaffolded planning documents, acceptance contract, validation evidence, and bootstrap task outcome.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for planning scaffold operations. |
| `watchtower-core plan scaffold` | Creates one planning document at a time when full bootstrap is not needed. |
| `watchtower-core task` | Manages the bootstrap task or any follow-up tasks created after the chain exists. |
| `watchtower-core sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |
| `watchtower-core closeout initiative` | Use after the bootstrap task and its successors are terminal. |

## Source Surface
- `core/python/src/watchtower_core/cli/plan_family.py`
- `core/python/src/watchtower_core/cli/plan_handlers.py`
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`

## Updated At
- `2026-03-11T15:11:22Z`
