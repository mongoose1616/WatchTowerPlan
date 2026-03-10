# `watchtower-core validate all`

## Summary
This command runs the current explicit validation families across the governed repository surfaces and returns one aggregate summary.

## Use When
- You want one bounded validation pass instead of running each validation family manually.
- You need a quick view of whether governed front matter, document semantics, schema-backed artifacts, and acceptance reconciliation currently pass.
- You want structured JSON output for workflows, agents, or higher-level automation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate all` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate all [--skip-front-matter] [--skip-document-semantics] [--skip-artifacts] [--skip-acceptance] [--format <human|json>]
```

## Arguments and Options
- `--skip-front-matter`: Skip governed Markdown front-matter validation targets.
- `--skip-document-semantics`: Skip governed document semantic validation targets.
- `--skip-artifacts`: Skip schema-backed governed JSON artifact validation targets.
- `--skip-acceptance`: Skip trace-level acceptance reconciliation checks.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate all --skip-acceptance
```

```sh
cd core/python
uv run watchtower-core validate all --format json
```

```sh
cd core/python
uv run watchtower-core validate all --skip-front-matter --skip-document-semantics --skip-artifacts
```

## Behavior and Outputs
- The command is read-only and aggregates the existing validation services rather than writing evidence or mutating control-plane artifacts.
- The current validation families are governed front matter, governed document semantics, schema-backed governed artifacts, and acceptance reconciliation across traceability surfaces.
- Acceptance reconciliation runs only for traces that currently publish governed acceptance state through PRDs, contracts, evidence, or traceability.
- Use `--skip-acceptance` when you want a structural validation pass over documents and JSON artifacts only.
- In `json` mode, the command returns per-family summary counts plus one structured result per validation target.
- The command exits with status code `0` when every executed target passes and `1` when any target fails.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate front-matter` | Validates one governed Markdown document front-matter block. |
| `watchtower-core validate document-semantics` | Validates governed Markdown documents against repo-native semantic structure rules. |
| `watchtower-core validate artifact` | Validates one governed JSON artifact against registry-backed schema validators. |
| `watchtower-core validate acceptance` | Validates one trace across PRD acceptance, contracts, evidence, and traceability. |
| `watchtower-core sync all` | Useful after validation when you want to rebuild the full local derived state. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/validation/all.py`
- `core/python/src/watchtower_core/validation/front_matter.py`
- `core/python/src/watchtower_core/validation/document_semantics.py`
- `core/python/src/watchtower_core/validation/artifact.py`
- `core/python/src/watchtower_core/validation/acceptance.py`

## Updated At
- `2026-03-09T23:59:23Z`
