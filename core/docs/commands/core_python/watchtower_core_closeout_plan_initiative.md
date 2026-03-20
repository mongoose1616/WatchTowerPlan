# `watchtower-core closeout plan-initiative`

## Summary
This command records terminal closeout state for one live initiative package under `plan/**`
and, in write mode, refreshes the pack-level indexes and rendered views that surface active
work and recent closeouts.

## Use When
- A pack-wide or project-scoped live plan initiative has finished implementation and closeout.
- You need the initiative-local machine state, closeout shell, evidence bundle, promotion shell, and derived plan views to agree on the terminal outcome.
- You want to clear `closing` initiatives out of the active coordination surface without editing JSON by hand.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core closeout plan-initiative` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/closeout_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core closeout plan-initiative --initiative-slug <initiative_slug> [--project-slug <project_slug>] --initiative-status <completed|superseded|cancelled> --closure-reason <reason> [--superseded-by-trace-id <trace_id>] [--closed-at <timestamp>] [--write] [--format <human|json>]
```

## Arguments and Options
- `--initiative-slug <initiative_slug>`: Initiative slug such as `plan_workspace_bootstrap` or `watchtower_work_item_notes`.
- `--project-slug <project_slug>`: Project slug when the initiative lives under `plan/projects/<project_slug>/initiatives/`.
- `--initiative-status <status>`: Terminal initiative status to record on the live plan package.
- `--closure-reason <reason>`: Short human-readable reason for the closeout decision.
- `--superseded-by-trace-id <trace_id>`: Replacement trace identifier. Required when initiative status is `superseded`.
- `--closed-at <timestamp>`: Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.
- `--write`: Persist the updated terminal closeout state and regenerated plan surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core closeout plan-initiative --initiative-slug plan_terminal_initiative_closeout_runtime --initiative-status completed --closure-reason "Delivered the live closeout runtime" --write
```

```sh
cd core/python
uv run watchtower-core closeout plan-initiative --project-slug watchtower --initiative-slug watchtower_work_item_notes --initiative-status completed --closure-reason "Implemented and validated work-item notes" --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not mutate live plan state.
- The command validates the target live initiative package before terminal closeout and rejects the operation when local tasks remain non-terminal or readiness drift is still open.
- In write mode, the command updates the initiative snapshot, finalizes initiative-local evidence and closeout artifacts, advances the promotion shell into a terminal review posture, appends terminal events, and refreshes the pack and project rendered/index surfaces.
- Pack-wide initiatives are resolved under `plan/initiatives/<initiative_slug>/`. Project-scoped initiatives are resolved under `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- In `human` mode, the command prints the initiative root, terminal status, timestamp, and write outcome.
- In `json` mode, the command prints one JSON object with the initiative identity, scope, closeout metadata, and write result.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core closeout` | Parent command group for closeout operations. |
| `watchtower-core closeout initiative` | Use only for retained trace records, not live `plan/**` initiative packages. |
| `watchtower-core query coordination` | Reads the pack-level coordination view that this command refreshes in write mode. |
| `watchtower-core query trace` | Reads the retained traceability record when you need the historical closeout path instead of the live plan path. |
| `watchtower-core sync all` | Rebuilds the broader derived surface set that includes the indexes and rendered views this command updates directly. |

## Source Surface
- `core/python/src/watchtower_core/cli/closeout_family.py`
- `core/python/src/watchtower_core/cli/closeout_handlers.py`
- `plan/python/src/watchtower_plan/initiative_packages.py`
- `plan/python/src/watchtower_plan/closeout/initiative_package.py`

## Updated At
- `2026-03-17T10:30:00Z`
