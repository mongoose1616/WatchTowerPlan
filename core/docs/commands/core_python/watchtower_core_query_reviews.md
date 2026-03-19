# `watchtower-core query reviews`

## Summary
This command searches the live review index for initiative review state and promotion approval state.

## Use When
- You need one machine-readable review surface without stitching together readiness and promotion records manually.
- You want machine-readable review results for an agent, workflow, or script.
- You need to filter live review state by subject kind, review state, trace, or review reference.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query reviews` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query reviews [--query <text>] [--subject-kind <initiative|promotion>] [--initiative-id <initiative_id>] [--project-id <project_id>] [--trace-id <trace_id>] [--review-state <state>] [--ready-for-execution <true|false>] [--review-ref <ref>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over review fields such as IDs, trace, title, review refs, and evidence refs.
- `--subject-kind <initiative|promotion>`: Exact subject-kind filter.
- `--initiative-id <initiative_id>`: Exact initiative identifier such as `initiative.plan_live_evidence_closeout_review_indexes_foundation`.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_evidence_closeout_review_indexes_foundation`.
- `--review-state <state>`: Exact review-state filter such as `pending` or `approved`.
- `--ready-for-execution <true|false>`: Filter initiative review entries by whether the subject is ready for execution.
- `--review-ref <ref>`: Exact review-ref filter such as `repository_maintainer_review` or `actor.repository_maintainer`.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query reviews --review-state pending
```

```sh
cd core/python
uv run watchtower-core query reviews --subject-kind promotion --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints review-subject IDs, subject kinds, review state, readiness state when applicable, and review references.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and review-entry records.
- The command reads `plan/.wt/indexes/review_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no review entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query readiness` | Shows initiative execution-readiness state for the same review-bearing initiative subjects. |
| `watchtower-core query plan-evidence` | Shows evidence bundles cited by review-bearing initiative and promotion subjects. |
| `watchtower-core query closeouts` | Shows closeout recaps that depend on promotion-review outcomes. |
| `watchtower-core query authority` | Resolves when the live review index is the canonical lookup surface. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/plan_runtime/query/reviews.py`
- `plan/.wt/indexes/review_index.json`

## Updated At
- `2026-03-17T22:39:20Z`
