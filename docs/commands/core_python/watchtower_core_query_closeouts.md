# `watchtower-core query closeouts`

## Summary
This command searches the live closeout index for initiative-local closeout contracts and terminal recap state.

## Use When
- You need the expected outcome, evidence references, promotion-review expectation, or terminal-state summary without opening one initiative root directly.
- You want machine-readable closeout results for an agent, workflow, or script.
- You need to filter live closeout state by trace, initiative, status, or terminal state.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query closeouts` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query closeouts [--query <text>] [--initiative-id <initiative_id>] [--project-id <project_id>] [--trace-id <trace_id>] [--status <planned|active|completed>] [--terminal-state <completed|superseded|cancelled>] [--promotion-review-required <true|false>] [--limit <n>] [--format <human|json>]
```

## Arguments and Options
- `--query <text>`: Free-text query over closeout fields such as IDs, title, expected outcome, and follow-up handling.
- `--initiative-id <initiative_id>`: Exact initiative identifier such as `initiative.plan_live_evidence_closeout_review_indexes_foundation`.
- `--project-id <project_id>`: Exact project identifier such as `project.watchtower`.
- `--trace-id <trace_id>`: Exact trace filter such as `trace.plan_live_evidence_closeout_review_indexes_foundation`.
- `--status <planned|active|completed>`: Exact closeout status filter.
- `--terminal-state <completed|superseded|cancelled>`: Exact terminal-state filter.
- `--promotion-review-required <true|false>`: Filter by whether the closeout recap requires promotion review.
- `--limit <n>`: Maximum number of results to return. Defaults to `10`.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core query closeouts --status planned
```

```sh
cd core/python
uv run watchtower-core query closeouts --promotion-review-required true --format json
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- In `human` mode, the command prints closeout IDs, initiative titles, expected outcome summaries, and promotion-review expectations.
- In `json` mode, the command prints one JSON object with the command name, status, result count, and closeout-entry records.
- The command reads `plan/.wt/indexes/closeout_index.json`.
- If no entries match the requested filters, the command exits successfully and reports that no closeout entries matched.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query plan-evidence` | Shows the evidence bundles referenced by closeout recaps. |
| `watchtower-core query reviews` | Shows approval and review state that can gate closeout and promotion outcomes. |
| `watchtower-core closeout plan-initiative` | Applies terminal closeout state to one live initiative package. |
| `watchtower-core query authority` | Resolves when the live closeout index is the canonical lookup surface. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_lookup_handlers.py`
- `core/python/src/watchtower_core/repo_ops/query/closeouts.py`
- `plan/.wt/indexes/closeout_index.json`

## Updated At
- `2026-03-17T22:39:20Z`
