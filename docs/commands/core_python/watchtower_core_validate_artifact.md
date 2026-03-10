# `watchtower-core validate artifact`

## Summary
This command validates one governed JSON artifact against the active schema-backed validators published in the control plane or against an explicitly supplied schema surface.

## Use When
- You want to check whether a governed JSON contract, index, ledger, or similar artifact matches its published schema.
- You need a structured validation result for a workflow, script, or agent.
- You want to force validation with an explicit validator ID for an external or temporary JSON file.
- You want to validate an external pack-owned artifact against a supplemental schema file or directory without patching the canonical schema catalog.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate artifact` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/validate_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate artifact --path <path> [--validator-id <validator_id> | --schema-id <schema_id>] [--supplemental-schema-path <path>] [--format <human|json>]
```

## Arguments and Options
- `--path <path>`: Repository-relative or absolute path to the JSON artifact to validate.
- `--validator-id <validator_id>`: Optional explicit validator identifier. Use this to force one registry-backed validator.
- `--schema-id <schema_id>`: Optional direct schema identifier. Use this to validate against a cataloged or supplemental schema without selecting a registry validator.
- `--supplemental-schema-path <path>`: Optional repository-relative or absolute path to one supplemental schema file or directory. Repeat for multiple locations.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `--record-evidence`: Write a durable validation-evidence artifact and synchronized traceability update.
- `--trace-id <trace_id>`: Required with `--record-evidence`. Shared trace identifier for the evidence artifact.
- `--evidence-id <evidence_id>`: Optional explicit evidence identifier. Otherwise the command derives one deterministically.
- `--subject-id <subject_id>`: Optional subject identifier to attach to the evidence check. Repeat for multiple values.
- `--acceptance-id <acceptance_id>`: Optional acceptance identifier to attach to the evidence check. Repeat for multiple values.
- `--evidence-output <path>`: Optional explicit output path for the evidence artifact.
- `--traceability-output <path>`: Optional explicit output path for the updated traceability index.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/indexes/traceability/traceability_index.v1.json --format json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path /tmp/example.json --validator-id validator.control_plane.acceptance_contract
```

```sh
cd core/python
uv run watchtower-core validate artifact --path /tmp/pack_note.json --schema-id urn:watchtower:schema:external:pack-note:v1 --supplemental-schema-path /tmp/pack_schemas --format json
```

```sh
cd core/python
uv run watchtower-core validate artifact --path /tmp/pack_note.json --supplemental-schema-path /tmp/pack_schemas
```

```sh
cd core/python
uv run watchtower-core validate artifact --path core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json --record-evidence --trace-id trace.core_python_foundation
```

## Behavior and Outputs
- The command loads the validator registry and resolves the matching schema-backed validator automatically when the path is repository-local.
- If `--validator-id` is provided, the command validates against that explicit artifact validator instead of auto-selecting by path.
- If `--schema-id` is provided, the command validates directly against that schema ID and does not require a validator-registry entry.
- External files may also validate directly when the document declares `$schema` and any required schema definitions are supplied through `--supplemental-schema-path`.
- Supplemental schema paths may point to one file or a directory tree of JSON Schema files. Missing, invalid, duplicate, or malformed supplemental schemas fail closed.
- In `human` mode, the command prints `PASS` or `FAIL`, the selected validator, and any validation issues.
- In `json` mode, the command prints one JSON object with the execution status, pass or fail result, selected validator, schema IDs, issue count, and issue records.
- If `--record-evidence` is used, the command writes a durable validation-evidence artifact and an updated traceability index document together.
- Evidence recording requires `--trace-id` and should target repository-local artifacts so the written artifact can join the governed traceability chain cleanly.
- The command exits with status code `0` when validation passes and `1` when validation fails or validator selection cannot be completed.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate front-matter` | Validates governed Markdown front matter rather than JSON artifacts. |
| `watchtower-core query trace` | Useful after validation when you need the related PRD, decision, design, acceptance, or evidence context. |

## Source Surface
- `core/python/src/watchtower_core/cli/validate_family.py`
- `core/python/src/watchtower_core/cli/validation_handlers.py`
- `core/python/src/watchtower_core/validation/artifact.py`
- `core/python/src/watchtower_core/control_plane/schemas.py`
- `core/python/src/watchtower_core/validation/common.py`
- `core/control_plane/registries/validators/validator_registry.v1.json`

## Updated At
- `2026-03-10T21:55:00Z`
