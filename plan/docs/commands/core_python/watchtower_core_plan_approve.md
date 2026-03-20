# `watchtower-core plan approve`

## Summary
This command approves one validated live initiative package into `ready_for_execution`, which is the required precondition before task transitions may start real execution.

## Use When
- A pack-wide or project-scoped live initiative package has passed review and is ready to begin execution.
- You need the initiative package, readiness state, and derived plan surfaces to agree that execution is allowed.
- You want a dry-run preview before persisting the approval event and refreshed plan surfaces.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan approve` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan approve --initiative-slug <initiative_slug> [--project-slug <project_slug>] [--actor-id <actor_id>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--initiative-slug <initiative_slug>`: Initiative slug such as `example_initiative` or `watchtower_work_item_notes`.
- `--project-slug <project_slug>`: Project slug when the initiative lives under `plan/projects/<project_slug>/initiatives/`.
- `--actor-id <actor_id>`: Approver actor identifier recorded on the approval event. Defaults to `actor.repository_maintainer`.
- `--write`: Persist the approval state and refresh derived plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan approve --initiative-slug plan_task_authority_rendering_governance_recovery --write
```

```sh
cd core/python
uv run watchtower-core plan approve --project-slug watchtower --initiative-slug watchtower_work_item_notes --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate live plan state.
- The command validates the initiative package and rejects approval when capture, readiness, discrepancy, or derived-surface drift remains open.
- Pack-wide initiatives are resolved under `plan/initiatives/<initiative_slug>/`. Project-scoped initiatives are resolved under `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- In write mode, the command records the approval event, marks the initiative package `ready_for_execution`, and refreshes the derived plan surfaces that expose readiness and current work.
- Task commands that request execution-starting statuses such as `in_progress`, `in_review`, or `completed` rely on this approval state and fail closed when it is missing.
- In `human` mode, the command prints the initiative root, lifecycle stage, readiness state, and write outcome.
- In `json` mode, the command prints one JSON object with the initiative identity, readiness summary, and write result.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for live initiative bootstrap and readiness operations. |
| `watchtower-core plan confirm-inputs` | Confirms the current initiative-authored inputs before approval. |
| `watchtower-core plan task` | Starts or progresses execution after the initiative package is approved. |
| `watchtower-core plan query readiness` | Reads the readiness view updated after approval. |
| `watchtower-core plan closeout initiative` | Closes the live initiative package after its tasks are terminal. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/handlers.py`
- `plan/python/src/watchtower_plan/cli/namespace.py`
- `plan/python/src/watchtower_plan/initiatives/service.py`

## Updated At
- `2026-03-18T20:35:00Z`
