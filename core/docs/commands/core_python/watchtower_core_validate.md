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
| Source Surface | `core/python/src/watchtower_host/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate <validate_command> [args]
```

## Arguments and Options
- `<validate_command>`: Choose the validation surface you want to run, currently `all`, `suite`, `front-matter`, `document-semantics`, `artifact`, `schema`, `acceptance`, or `portability`.
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
uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path /tmp/pack_note.json --schema-id urn:watchtower:schema:external:pack-note:v1 --supplemental-schema-path /tmp/pack_schemas --format json
```

```sh
cd core/python
uv run watchtower-core validate schema --path core/control_plane/schemas/interfaces/packs/pack_settings.schema.json --format json
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path core/docs/references/front_matter_reference.md
```

```sh
cd core/python
uv run watchtower-core validate document-semantics --path core/workflows/modules/code_validation.md
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path core/docs/standards/metadata/front_matter_standard.md --format json
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path core/docs/standards/metadata/front_matter_standard.md --record-evidence --trace-id trace.governed_acceptance_example
```

```sh
cd core/python
uv run watchtower-core validate acceptance --trace-id trace.governed_acceptance_example --format json
```

```sh
cd core/python
uv run watchtower-core validate portability --include-pack plan --format json
```

## Behavior and Outputs
- With no leaf command, the current implementation prints validate-specific help and exits successfully.
- The command group is a stable entrypoint for governed validation behavior rather than a one-off script surface.
- The current leaf commands are `all` for the current repo baseline suite plus acceptance reconciliation, `suite` for one pack-declared validation suite, `front-matter` for governed Markdown metadata, `document-semantics` for governed Markdown structure, repo-local link integrity, and applied-reference rules, `artifact` for schema-backed JSON artifacts or direct external schema validation, `schema` for Draft 2020-12 schema-definition validation of `*.schema.json` files, `acceptance` for semantic reconciliation across trace-level acceptance IDs, contracts, evidence, validators, source-surface links, and traceability, and `portability` for release/bootstrap exclusion scanning over a repository root or staged export.
- Individual leaf commands may return a non-zero exit code when validation fails even if the command itself executed successfully.
- Leaf commands may optionally emit durable evidence artifacts and synchronized traceability updates when they explicitly support that behavior.
- Use `watchtower-core release check` when customer or downstream bootstrap handoff needs this validation family wrapped into the full local release gate.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate all` | Runs the current explicit validation families across the governed repository surfaces. |
| `watchtower-core validate suite` | Runs one pack-declared validation suite with optional pack-settings selection. |
| `watchtower-core validate acceptance` | Validates one trace across trace-level acceptance IDs, acceptance contracts, evidence, validators, source-surface links, and traceability. |
| `watchtower-core validate artifact` | Validates one governed JSON artifact against registry-backed schema validators. |
| `watchtower-core validate schema` | Validates one JSON Schema definition file against the Draft 2020-12 metaschema. |
| `watchtower-core validate document-semantics` | Validates governed Markdown documents against repo-native semantic structure rules. |
| `watchtower-core validate front-matter` | Validates one Markdown document front-matter block. |
| `watchtower-core validate portability` | Validates a repo root or staged export against the release/bootstrap portability contract. |
| `watchtower-core release check` | Runs the local release gate that wraps this validation family with dirty-worktree protection and final export staging. |
| `watchtower-core` | Root command that dispatches to this command group. |
| `watchtower-core <pack-namespace> query trace` | Helpful after validation when you need to inspect the related pack-owned trace and evidence surfaces. |

## Source Surface
- `core/python/src/watchtower_host/cli/validate_family.py`
- `core/python/src/watchtower_host/cli/validation_handlers.py`
- `core/python/src/watchtower_core/validation/`

## Updated At
- `2026-03-25T02:15:00Z`
