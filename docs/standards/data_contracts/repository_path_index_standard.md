---
id: "std.data_contracts.repository_path_index"
title: "Repository Path Index Standard"
summary: "This standard defines the role, structure, and boundary rules for generated repository path indexes stored under `core/control_plane/indexes/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "repository_path_index"
owner: "repository_maintainer"
updated_at: "2026-03-12T01:22:49Z"
audience: "shared"
authority: "authoritative"
---

# Repository Path Index Standard

## Summary
This standard defines the role, structure, and boundary rules for generated repository path indexes stored under `core/control_plane/indexes/`.

## Purpose
Provide a machine-readable lookup surface for repository paths and entrypoints without overloading `README.md` files or misclassifying derived path catalogs as authoritative registries.

## Scope
- Applies to generated repository path indexes stored under `core/control_plane/indexes/repository_paths/`.
- Covers placement, coverage modes, entry shape, update expectations, and the boundary between human-facing README orientation and machine-facing path indexing.
- Does not replace directory `README.md` files, routing behavior, or the canonical schemas, registries, contracts, and policies the index points to.

## Use When
- Adding a repository path index for retrieval or navigation.
- Refreshing a path index after repository structure or entrypoint surfaces change.
- Reviewing whether a proposed machine-readable path catalog is correctly modeled as a derived index.

## Related Standards and Sources
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model repository path lookup as an index, not as a registry.
- Treat the path index as derived support data rather than as canonical authority.
- Store governed path-index artifacts under `core/control_plane/indexes/repository_paths/`.
- Keep the corresponding artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published index artifact.
- Use repository-relative paths in entries. Do not store absolute filesystem paths in the canonical index.
- Every published path index must declare its `coverage_mode`.
- Approved `coverage_mode` values are:
  - `entrypoints` for curated high-signal repository surfaces used for navigation and retrieval.
  - `full_tree` for a generated catalog intended to cover the repository tree more completely.
- Start with `entrypoints` unless a concrete retrieval need justifies the maintenance cost of a full-tree catalog.
- Keep entry summaries concise and retrieval-oriented rather than copying long README prose.
- Prefer deriving summaries and related-path hints from current repository documentation when that guidance exists.
- Publish retrieval metadata that helps both humans and agents distinguish authoritative entrypoints from scaffolding or support surfaces.
- Include optional aliases, tags, and related paths only when they materially improve lookup quality.
- Exclude ignored caches, transient runtime state, tool output, and other non-governed filesystem noise from the canonical path index.
- Do not let the path index silently replace `README.md` as the human-facing orientation layer.
- Do not use the path index to redefine the authority of a path. Authority belongs to the underlying artifact family, not to the index entry.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the path-index artifact family. |
| `id` | Required | Stable identifier for the index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `coverage_mode` | Required | Must be `entrypoints` or `full_tree`. |
| `root_path` | Required | Use `.` for repository-root indexes unless a narrower subtree index is being published. |
| `entries` | Required | Array of indexed path records. |

### Entry fields
| Field | Requirement | Notes |
|---|---|---|
| `path` | Required | Repository-relative file or directory path. |
| `kind` | Required | Use `file` or `directory`. |
| `surface_kind` | Required | Short family label such as `workflow`, `standard`, `template`, `control_plane`, or `source`. |
| `summary` | Required | Concise retrieval-oriented description of why the path matters. |
| `parent_path` | Required | Repository-relative parent path or `.` for root-level entries. |
| `maturity` | Required | Retrieval-oriented authority hint. Use `authoritative`, `supporting`, or `scaffold`. |
| `priority` | Required | Retrieval-oriented ranking hint. Use `high`, `medium`, or `low`. |
| `audience_hint` | Required | Retrieval-oriented audience hint. Use `shared`, `automation`, or `maintainer`. |
| `aliases` | Optional | Short alternate terms that materially help retrieval. |
| `tags` | Optional | Controlled or semi-controlled lookup terms when they improve query quality. |
| `related_paths` | Optional | Other repository-relative paths strongly associated with the entry. |

## Process or Workflow
1. Decide whether the index should cover curated entrypoints or a fuller repository tree.
2. Gather the current repository paths in scope and the README or standards context that should inform the entry summaries.
3. Generate or refresh the index artifact in `core/control_plane/indexes/repository_paths/`.
4. Validate the artifact against its published schema.
5. Update the path-index standard, schema, examples, and README inventory surfaces in the same change set when the artifact family changes structurally.

## Examples
- A curated list of the repository root, `docs/`, `workflows/`, `core/`, and the key control-plane subtrees is an `entrypoints` path index.
- A generated catalog that attempts to cover the whole governed repository tree is a `full_tree` path index.
- A manually curated catalog of validator identities is not a path index; it belongs in a registry.

## Operationalization
- `Modes`: `artifact`; `schema`
- `Operational Surfaces`: `core/control_plane/indexes/`; `core/control_plane/indexes/README.md`; `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/repository_paths/`; `core/control_plane/examples/valid/indexes/repository_path_index*.example.json`; `core/control_plane/examples/invalid/indexes/repository_path_index*.example.json`

## Validation
- The path index should validate against its published schema.
- Every entry should use repository-relative paths that currently exist in the repository.
- `coverage_mode` should match the actual breadth of the artifact.
- `maturity`, `priority`, and `audience_hint` should stay retrieval-oriented and consistent with the actual role of the indexed path.
- Reviewers should reject entries that merely repeat long prose from README files without improving lookup.
- Reviewers should reject path indexes that include ignored caches or transient runtime state as if they were governed surfaces.

## Change Control
- Update the index when repository entrypoints, major directory surfaces, or other indexed paths change materially.
- Update the companion schema and examples in the same change set when the path-index artifact shape changes.
- Prefer regenerating the index over hand-editing drift when the index is intended to be machine-produced.

## References
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/README.md)

## Notes
- README files remain the human orientation layer for directories.
- The repository path index exists to improve machine retrieval and path lookup, not to become a second prose documentation system.

## Updated At
- `2026-03-12T01:22:49Z`
