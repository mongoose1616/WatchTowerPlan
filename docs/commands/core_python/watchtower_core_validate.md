# `watchtower-core validate`

## Summary
This command group runs governed validation commands against repository artifacts and document surfaces.

## Use When
- You want command-family help for the available validation surfaces.
- You need to validate a governed artifact or document without opening implementation code directly.
- You are onboarding to the workspace and want to discover the current validation entrypoints.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate <validate_command> [args]
```

## Arguments and Options
- `<validate_command>`: Choose the validation surface you want to run, currently `all`, `front-matter`, `document-semantics`, `artifact`, or `acceptance`.
- `-h`, `--help`: Show the command help text.
- No group-level validation flags exist; pass validator-specific arguments to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core validate --help
```

```sh
cd core/python
uv run watchtower-core validate all --skip-acceptance
```

```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path docs/references/front_matter_reference.md
```

```sh
cd core/python
uv run watchtower-core validate document-semantics --path workflows/modules/code_validation.md
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path docs/standards/metadata/front_matter_standard.md --format json
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path docs/standards/metadata/front_matter_standard.md --record-evidence --trace-id trace.core_python_foundation
```

```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json
```

## Behavior and Outputs
- With no leaf command, the current implementation prints validate-specific help and exits successfully.
- The command group is a stable entrypoint for governed validation behavior rather than a one-off script surface.
- The current leaf commands are `all` for aggregate repo validation, `front-matter` for governed Markdown metadata, `document-semantics` for governed Markdown structure and applied-reference rules, `artifact` for schema-backed JSON artifacts, and `acceptance` for semantic reconciliation across PRD acceptance, contracts, evidence, validators, and traceability.
- Individual leaf commands may return a non-zero exit code when validation fails even if the command itself executed successfully.
- Leaf commands may optionally emit durable evidence artifacts and synchronized traceability updates when they explicitly support that behavior.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate all` | Runs the current explicit validation families across the governed repository surfaces. |
| `watchtower-core validate acceptance` | Validates one trace across PRD acceptance IDs, acceptance contracts, evidence, validators, and traceability. |
| `watchtower-core validate artifact` | Validates one governed JSON artifact against registry-backed schema validators. |
| `watchtower-core validate document-semantics` | Validates governed Markdown documents against repo-native semantic structure rules. |
| `watchtower-core validate front-matter` | Validates one Markdown document front-matter block. |
| `watchtower-core` | Root command that dispatches to this command group. |
| `watchtower-core query trace` | Helpful after validation when you need to inspect the related planning and evidence surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/validation/`

## Updated At
- `2026-03-09T23:59:23Z`
