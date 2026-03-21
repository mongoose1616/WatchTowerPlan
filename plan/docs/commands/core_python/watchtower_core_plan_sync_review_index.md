# `watchtower-core plan sync review-index`

## Summary
This command rebuilds the governed review index from initiative-local review, approval, and readiness state.

## Use When
- You changed initiative review state, readiness gates, approvals, or promotion shells and need the live review index to match.
- You want to inspect the rebuilt review index in dry-run mode before writing it to the canonical live plan-workspace path.
- You need an explicit operator path to heal `review_index` drift instead of relying on side-effect rebuilds.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan sync review-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/sync.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan sync review-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical review-index path at `plan/.wt/indexes/review_index.json`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan sync review-index
```

```sh
cd core/python
uv run watchtower-core plan sync review-index --write
```

```sh
cd core/python
uv run watchtower-core plan sync review-index --output /tmp/review_index.json --format json
```

## Behavior and Outputs
- The command reads live initiative review, readiness, approval, and closeout-adjacent state under `plan/**/.wt/` and rebuilds the machine-readable review index deterministically.
- The rebuilt artifact is the canonical backing surface for review-oriented plan queries and readiness checks.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many review entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt review-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source surfaces or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core plan sync all` | Rebuilds the broader local target set that also includes the review index. |
| `watchtower-core plan query reviews` | Reads the review index that this command rebuilds. |
| `watchtower-core plan approve` | Consumes review and readiness state that can surface as review-index drift. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/sync.py`
- `plan/python/src/watchtower_plan/sync/review_index.py`
- `plan/.wt/indexes/review_index.json`

## Updated At
- `2026-03-21T03:12:00Z`
