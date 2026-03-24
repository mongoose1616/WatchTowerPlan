# `watchtower-core plan closeout retained-initiative`

## Summary
This command applies terminal closeout state to one retained trace record after the live `plan/**` initiative is already closed or otherwise retired.

## Use When
- You need to finalize one retained trace record rather than a live initiative package.
- You need the retained traceability, initiative, and coordination mirrors refreshed in the same closeout slice.
- The target trace no longer belongs to a live `plan/**` initiative package.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan closeout retained-initiative` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/closeout.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan closeout retained-initiative --trace-id <trace_id> --initiative-status <completed|superseded|cancelled|abandoned> --closure-reason <reason> [--superseded-by-trace-id <trace_id>] [--closed-at <timestamp>] [--allow-open-tasks] [--allow-acceptance-issues] [--write] [--format <human|json>]
```

## Arguments and Options
- `--trace-id <trace_id>`: Stable trace identifier such as `trace.governed_acceptance_example`.
- `--initiative-status <completed|superseded|cancelled|abandoned>`: Terminal initiative status to record on the retained trace record.
- `--closure-reason <reason>`: Short human-readable reason for the closeout decision.
- `--superseded-by-trace-id <trace_id>`: Replacement trace identifier when the retained record is superseded.
- `--closed-at <timestamp>`: Explicit RFC 3339 UTC closeout timestamp. Defaults to the current UTC time.
- `--allow-open-tasks`: Allow terminal closeout even if linked tasks are still open.
- `--allow-acceptance-issues`: Allow terminal closeout when acceptance reconciliation still reports issues.
- `--write`: Persist the updated closeout state and refreshed retained mirrors.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan closeout retained-initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"
```

```sh
cd core/python
uv run watchtower-core plan closeout retained-initiative --trace-id trace.example --initiative-status superseded --superseded-by-trace-id trace.replacement --closure-reason "Replaced by the new initiative" --write
```

## Behavior and Outputs
- This is the retained-history closeout path, not the normal live initiative-package closeout path for `plan/**`.
- If the requested `trace_id` still belongs to a live `plan/**` initiative package, the command fails closed and points to `watchtower-core plan closeout initiative`.
- In write mode it updates the traceability index plus the derived retained initiative and coordination mirrors.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan closeout` | Parent command group for live and retained plan closeout operations. |
| `watchtower-core plan closeout initiative` | Use this when the target is still a live initiative package under `plan/**`. |
| `watchtower-core validate acceptance` | Run this first when retained closeout should still enforce trace-level acceptance reconciliation. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/closeout.py`
- `plan/python/src/watchtower_plan/closeout/initiative.py`

## Updated At
- `2026-03-24T23:45:00Z`
