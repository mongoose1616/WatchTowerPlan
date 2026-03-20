# `watchtower-core query plan-evidence`

## Summary
This command searches the live evidence index for initiative-local validation bundles captured under the plan workspace.

## Use When
- You need the current planned or completed validation contract for one initiative without opening the local evidence bundle directly.
- You want machine-readable evidence-bundle results for an agent, workflow, or script.
- You need to filter live initiative evidence by trace, owner, target phase, validation type, or acceptance label.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query plan-evidence` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query plan-evidence [--query <text>] [--initiative-id <initiative_id>] [--project-id <project_id>] [--trace-id <trace_id>] [--status <planned|active|completed>] [--owner <owner>] [--target-phase <phase>] [--validation-type <type>] [--acceptance-label <label>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over evidence fields such as IDs, title, acceptance labels, owners, and output paths.
- `--initiative-id <initiative_id>`: Exact initiative identifier such as `initiative.plan_live_evidence_closeout_review_indexes_foundation`.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_evidence_closeout_review_indexes_foundation`.
- `--status <planned|active|completed>`: Exact evidence status filter.
- `--owner <owner>`: Exact owner filter such as `repository_maintainer`.
- `--target-phase <phase>`: Exact target-phase filter such as `readiness`, `execution`, or `closeout`.
- `--validation-type <type>`: Exact validation-type filter such as `schema_validation` or `readiness_gate`.
- `--acceptance-label <label>`: Exact acceptance-label filter as captured in the validation bundle.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query plan-evidence --status planned
```

```sh
cd core/python
uv run watchtower-core query plan-evidence --trace-id trace.plan_live_evidence_closeout_review_indexes_foundation --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints evidence IDs, initiative titles, validation types, owners, and target phases.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and evidence-entry records.
- The command reads `plan/.wt/indexes/evidence_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no plan evidence entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query closeouts` | Shows the closeout recaps that consume or reference the same initiative-local evidence IDs. |
| `watchtower-core query reviews` | Shows review state for initiative and promotion subjects that often reference the same evidence bundles. |
| `watchtower-core query readiness` | Shows whether open evidence obligations still block execution readiness. |
| `watchtower-core query authority` | Resolves when the live evidence index is the canonical lookup surface. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `plan/python/src/watchtower_plan/query/plan_evidence.py`
- `plan/.wt/indexes/evidence_index.json`

## Updated At
- `2026-03-17T22:39:20Z`
