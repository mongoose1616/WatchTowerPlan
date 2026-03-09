# `watchtower-core validate front-matter`

## Summary
This command validates one Markdown document front-matter block against the governed front-matter profiles published in the control plane.

## Use When
- You want to check whether a governed Markdown document has valid front matter.
- You need a structured validation result for a workflow, script, or agent.
- You want to force validation with an explicit validator ID for an external or test file.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate front-matter` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate front-matter --path <path> [--validator-id <validator_id>] [--format <human|json>]
```

## Arguments and Options
- `--path <path>`: Repository-relative or absolute path to the Markdown document to validate.
- `--validator-id <validator_id>`: Optional explicit validator identifier. Required for files outside the repository tree.
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
uv run watchtower-core validate front-matter --path docs/references/front_matter_reference.md
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path docs/standards/metadata/front_matter_standard.md --format json
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path /tmp/example.md --validator-id validator.documentation.standard_front_matter
```

```sh
cd core/python
uv run watchtower-core validate front-matter --path docs/standards/metadata/front_matter_standard.md --record-evidence --trace-id trace.core_python_foundation
```

## Behavior and Outputs
- The command loads the validator registry and resolves the matching front-matter validator automatically when the path is repository-local.
- If `--validator-id` is provided, the command validates against that explicit front-matter validator instead of auto-selecting by path.
- In `human` mode, the command prints `PASS` or `FAIL`, the selected validator, and any validation issues.
- In `json` mode, the command prints one JSON object with the execution status, pass or fail result, selected validator, schema IDs, issue count, and issue records.
- If `--record-evidence` is used, the command writes a durable validation-evidence artifact and an updated traceability index document together.
- Evidence recording requires `--trace-id` and should target repository-local documents so the written artifact can join the governed traceability chain cleanly.
- The command exits with status code `0` when validation passes and `1` when validation fails or validator selection cannot be completed.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate artifact` | Validates governed JSON artifacts rather than Markdown front matter. |
| `watchtower-core query commands` | Helps discover nearby CLI surfaces if you are not sure which command family to use. |
| `watchtower-core query trace` | Useful after validation when you need the related PRD, decision, design, or evidence context. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/validation/front_matter.py`
- `core/python/src/watchtower_core/adapters/front_matter.py`
- `core/control_plane/registries/validators/validator_registry.v1.json`

## Updated At
- `2026-03-09T06:30:54Z`
