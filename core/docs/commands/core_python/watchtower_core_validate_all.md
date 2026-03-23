# `watchtower-core validate all`

## Summary
This command runs the active pack's default validation baseline through the reusable-core suite runtime, then adds acceptance reconciliation and returns one aggregate summary.

## Use When
- You want one bounded validation pass instead of running each validation family manually.
- You need a quick view of whether governed front matter, document semantics including repo-local link integrity, schema-backed artifacts plus canonical valid examples, and acceptance reconciliation currently pass.
- You want structured JSON output for workflows, agents, or higher-level automation.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate all` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate all [--skip-front-matter] [--skip-document-semantics] [--skip-artifacts] [--skip-acceptance] [--pack-settings-path <path>] [--format <human|json>]
```

## Arguments and Options
- `--skip-front-matter`: Skip governed Markdown front-matter validation targets.
- `--skip-document-semantics`: Skip governed document semantic validation targets.
- `--skip-artifacts`: Skip schema-backed governed JSON artifact validation targets.
- `--skip-acceptance`: Skip trace-level acceptance reconciliation checks.
- `--pack-settings-path <path>`: Optional repository-relative or absolute path to the pack settings surface whose `default_validation_suite_id` should supply the baseline suite.
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

```sh
cd core/python
uv run watchtower-core validate all --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json
```

## Behavior and Outputs
- The command is read-only and aggregates the current repo baseline validation families rather than writing evidence or mutating control-plane artifacts.
- The current validation families are governed front matter, governed document semantics including repo-local link integrity, schema-backed governed artifacts, and acceptance reconciliation across traceability surfaces.
- The front-matter, document-semantics, and artifact families run through the active pack settings surface's `default_validation_suite_id`, which is declared in the validation-suite registry and resolved through the reusable-core suite runtime.
- When no `--pack-settings-path` is supplied, the runtime uses the active selected pack when present; otherwise it discovers the repository-default pack settings surface and falls back to the shared-core pack only if no repo-local pack exists.
- Acceptance reconciliation runs only for traces that currently publish governed acceptance state through initiative-authored inputs, contracts, evidence, or traceability.
- Use `--skip-acceptance` when you want a structural validation pass over documents and JSON artifacts only.
- In `json` mode, the command returns per-family summary counts plus one structured result per validation target.
- The command exits with status code `0` when every executed target passes and `1` when any target fails.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate suite` | Runs one declared validation suite directly instead of the current repo baseline plus acceptance wrapper. |
| `watchtower-core validate front-matter` | Validates one governed Markdown document front-matter block. |
| `watchtower-core validate document-semantics` | Validates governed Markdown documents against repo-native semantic structure rules. |
| `watchtower-core validate artifact` | Validates one governed JSON artifact against registry-backed schema validators. |
| `watchtower-core validate acceptance` | Validates one trace across initiative acceptance, contracts, evidence, and traceability. |
| `watchtower-core <pack-namespace> sync all` | Useful after validation when you want to rebuild the full local derived state. |

## Source Surface
- `core/python/src/watchtower_host/cli/validate_family.py`
- `core/python/src/watchtower_core/validation/all.py`
- `core/python/src/watchtower_core/validation/suite.py`
- `<pack-root>/python/src/watchtower_<pack>/validation/targets.py`
- `core/python/src/watchtower_core/validation/front_matter.py`
- `<pack-root>/python/src/watchtower_<pack>/validation/document_semantics.py`
- `core/python/src/watchtower_core/validation/artifact.py`
- `core/python/src/watchtower_core/validation/acceptance.py`

## Updated At
- `2026-03-19T22:48:00Z`
