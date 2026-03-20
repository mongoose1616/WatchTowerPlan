# `watchtower-core plan confirm-inputs`

## Summary
This command records maintainer confirmation of the current initiative-authored inputs into machine state so the live initiative package can proceed through readiness review and approval without stale authored-input hashes.

## Use When
- A pack-wide or project-scoped live initiative package has been reviewed and its authored Markdown or companion inputs should be confirmed into machine state.
- You need the initiative package to reflect the latest reviewed authored inputs before execution approval.
- You want a dry-run preview before persisting the confirmation event and refreshed plan surfaces.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan confirm-inputs` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/plan_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan confirm-inputs --initiative-slug <initiative_slug> [--project-slug <project_slug>] [--actor-id <actor_id>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--initiative-slug <initiative_slug>`: Initiative slug such as `example_initiative` or `watchtower_work_item_notes`.
- `--project-slug <project_slug>`: Project slug when the initiative lives under `plan/projects/<project_slug>/initiatives/`.
- `--actor-id <actor_id>`: Approver actor identifier recorded on the confirmation event. Defaults to `actor.repository_maintainer`.
- `--write`: Persist the confirmation state and refresh derived plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan confirm-inputs --initiative-slug plan_task_authority_rendering_governance_recovery --write
```

```sh
cd core/python
uv run watchtower-core plan confirm-inputs --project-slug watchtower --initiative-slug watchtower_work_item_notes --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate live plan state.
- The command confirms the current authored-input hashes into initiative machine state and appends an authored-input confirmation event in write mode.
- Pack-wide initiatives are resolved under `plan/initiatives/<initiative_slug>/`. Project-scoped initiatives are resolved under `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- In write mode, the command refreshes the initiative package and derived plan surfaces, then reruns readiness validation so the package reflects the confirmed state immediately.
- In `human` mode, the command prints the initiative root, lifecycle stage, review status, and write outcome.
- In `json` mode, the command prints one JSON object with the initiative identity, readiness summary, and write result.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for live initiative bootstrap and readiness operations. |
| `watchtower-core plan approve` | Approves the confirmed live initiative package into `ready_for_execution`. |
| `watchtower-core query readiness` | Reads the readiness view updated after confirmation. |
| `watchtower-core task` | Uses the same initiative package after confirmation and approval. |

## Source Surface
- `core/python/src/watchtower_core/cli/plan_family.py`
- `core/python/src/watchtower_core/cli/plan_handlers.py`
- `plan/python/src/watchtower_plan/initiative_packages.py`

## Updated At
- `2026-03-18T20:35:00Z`
