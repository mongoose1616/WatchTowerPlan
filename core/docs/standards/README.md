# `core/docs/standards`

## Description
`This directory contains normative repository standards. Use it for stable rules that govern documentation, metadata, workflows, data contracts, engineering practice, governance, operations, and validation behavior. Governed standard documents under this tree use standard front matter; short directory README.md files stay plain Markdown unless a narrower local rule says otherwise.`

## Paths
| Path | Description |
|---|---|
| `core/docs/standards/README.md` | Describes the purpose of the standards directory and its main standard families. |
| `core/docs/standards/data_contracts/` | Holds standards for schemas, structured artifacts, statuses, format selection, and the shared planning-index family baseline. |
| `core/docs/standards/documentation/` | Holds standards for repository document families and Markdown surfaces. |
| `core/docs/standards/engineering/` | Holds standards for engineering practice and commit behavior. |
| `core/docs/standards/governance/` | Holds shared governance standards for source hierarchy, citation discipline, and promotion of external guidance into durable local policy. |
| `core/docs/standards/metadata/` | Holds standards for front matter, naming, identifiers, and terminology. |
| `core/docs/standards/operations/` | Holds operations standards used by the repository. |
| `core/docs/standards/validations/` | Holds validation-related standards used by the repository. |
| `core/docs/standards/workflows/` | Holds standards for routing and workflow design behavior. |

## Notes
- Use `core/docs/standards/data_contracts/README.md` when the question is about governed structured artifacts or the planning-related derived index family.
- Use `core/docs/standards/governance/README.md` when the question is how source authority, citation, or external-guidance promotion should work across shared core and pack-owned docs.
- Use `cd core/python && ./.venv/bin/watchtower-core query standards --category data_contracts --tag planning_index_family --format json` when you want the shared planning-index family baseline plus its member standards.
