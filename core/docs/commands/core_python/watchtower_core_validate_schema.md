# `watchtower-core validate schema`

## Summary
This command validates one JSON Schema definition file against the Draft 2020-12 metaschema.

## Use When
- You changed a repository-owned `*.schema.json` file and need an explicit schema-definition check.
- You need a deterministic pass or fail result for schema authoring work without treating the schema file like an artifact instance.
- You want a structured JSON result that agents, scripts, or reviewers can consume directly.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate schema` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate schema --path <path> [--record-evidence --trace-id <trace_id>] [--format <human|json>]
```

## Arguments and Options
- `--path <path>`: Repository-relative or absolute path to the JSON Schema definition file to validate.
- `--record-evidence`: Write a durable validation-evidence artifact and synchronized traceability update.
- `--trace-id <trace_id>`: Required with `--record-evidence`. Shared trace identifier for the evidence artifact.
- `--evidence-id <evidence_id>`: Optional explicit evidence identifier. Otherwise the command derives one deterministically.
- `--subject-id <subject_id>`: Optional subject identifier to attach to the evidence check. Repeat for multiple values.
- `--acceptance-id <acceptance_id>`: Optional acceptance identifier to attach to the evidence check. Repeat for multiple values.
- `--evidence-output <path>`: Optional explicit output path for the evidence artifact.
- `--traceability-output <path>`: Optional explicit output path for the updated traceability index.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate schema --path core/control_plane/schemas/interfaces/packs/pack_settings.schema.json
```

```sh
cd core/python
uv run watchtower-core validate schema --path core/control_plane/schemas/artifacts/command_index.schema.json --format json
```

```sh
cd core/python
uv run watchtower-core validate schema --path /tmp/example.schema.json --format json
```

```sh
cd core/python
uv run watchtower-core validate schema --path core/control_plane/schemas/interfaces/packs/pack_settings.schema.json --record-evidence --trace-id trace.governed_acceptance_example --format json
```

## Behavior and Outputs
- The command validates the target file against the Draft 2020-12 metaschema and reports schema-definition issues rather than artifact-instance issues.
- Without `--record-evidence`, the command is read-only. It does not mutate the schema catalog, validator registry, or any derived index.
- Use this command for `*.schema.json` authoring. Use `watchtower-core validate artifact` for JSON documents that should conform to a published schema.
- `watchtower-core validate all` remains the broad repository baseline, but it does not replace explicit schema-definition checks when schema files changed.
- If `--record-evidence` is used, the command writes a durable validation-evidence artifact and an updated traceability index document together.
- Durable evidence recording requires `--trace-id` and should target repository-local schema files so the resulting evidence can join the governed traceability chain.
- In `human` mode, the command prints `PASS` or `FAIL`, the schema-definition validator ID, and any findings.
- In `json` mode, the command prints one JSON object with the pass or fail result, validator ID, metaschema ID, issue count, and issue records.
- The command exits with status code `0` when validation passes and `1` when validation fails.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate artifact` | Validates JSON artifact instances instead of schema-definition files. |
| `watchtower-core validate all` | Runs the broad repository validation baseline, which may still need explicit schema-definition checks when `*.schema.json` changed. |
| `watchtower-core release check` | Preferred one-shot local release gate when schema-definition checks should be tied directly to staged export creation. |

## Source Surface
- `core/python/src/watchtower_host/cli/validate_family.py`
- `core/python/src/watchtower_host/cli/validation_handlers.py`
- `core/python/src/watchtower_core/validation/schema_definition.py`

## Updated At
- `2026-03-25T02:15:00Z`
