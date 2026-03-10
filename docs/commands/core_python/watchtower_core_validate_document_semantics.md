# `watchtower-core validate document-semantics`

## Summary
This command validates one governed Markdown document against repo-native semantic rules such as repo-local link integrity, required sections, section order, applied-reference explanation, and family-specific guardrails.

## Use When
- You want to validate governed document structure beyond front matter alone.
- You want broken repo-local Markdown links to fail before closeout.
- You need a structured semantic validation result for a workflow, script, or agent.
- You want to confirm that a workflow, standard, foundation doc, PRD, decision, or design doc still satisfies its document standard.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core validate document-semantics` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core validate document-semantics --path <path> [--validator-id <validator_id>] [--format <human|json>]
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
uv run watchtower-core validate document-semantics --path workflows/modules/code_validation.md
```

```sh
cd core/python
uv run watchtower-core validate document-semantics --path docs/standards/documentation/workflow_md_standard.md --format json
```

```sh
cd core/python
uv run watchtower-core validate document-semantics --path /tmp/example.md --validator-id validator.documentation.standard_semantics
```

## Behavior and Outputs
- The command loads the validator registry and resolves the matching document-semantics validator automatically when the path is repository-local.
- Repo-local Markdown links are validated fail closed when they point to missing repository targets.
- If `--validator-id` is provided, the command validates against that explicit semantic validator instead of auto-selecting by path.
- In `human` mode, the command prints `PASS` or `FAIL`, the selected validator, and any validation issues.
- In `json` mode, the command prints one JSON object with the execution status, pass or fail result, selected validator, issue count, and issue records.
- If `--record-evidence` is used, the command writes a durable validation-evidence artifact and an updated traceability index document together.
- Evidence recording requires `--trace-id` and should target repository-local documents so the written artifact can join the governed traceability chain cleanly.
- The command exits with status code `0` when validation passes and `1` when validation fails or validator selection cannot be completed.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core validate` | Parent command group for governed validation operations. |
| `watchtower-core validate front-matter` | Validates governed Markdown metadata rather than document-shape semantics. |
| `watchtower-core validate artifact` | Validates governed JSON artifacts rather than Markdown documents. |
| `watchtower-core query standards` | Helps find the governing standards that define the semantic rules being enforced. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/validation/document_semantics.py`
- `core/control_plane/registries/validators/validator_registry.v1.json`

## Updated At
- `2026-03-10T20:33:00Z`
