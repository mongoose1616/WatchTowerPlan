---
id: "std.data_contracts.authority_map"
title: "Authority Map Standard"
summary: "This standard defines the role, structure, and boundary rules for the authored authority-map registry stored under `core/control_plane/registries/authority_map/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "authority_map"
owner: "repository_maintainer"
updated_at: "2026-03-11T03:10:00Z"
audience: "shared"
authority: "authoritative"
---

# Authority Map Standard

## Summary
This standard defines the role, structure, and boundary rules for the authored authority-map registry stored under `core/control_plane/registries/authority_map/`.

## Purpose
- Publish one machine-readable policy answer for which planning or governance surface is canonical for a recurring question.
- Reduce surface-lookup ambiguity for agents, scripts, and maintainers without turning the authority map into a second path index or prose encyclopedia.
- Keep canonical-versus-projection relationships explicit as the planning and governance corpus grows.

## Scope
- Applies to machine-readable authority-map artifacts stored under `core/control_plane/registries/authority_map/`.
- Covers placement, root artifact fields, question-entry shape, preferred-command capture, and fallback-path expectations.
- Does not replace the path index, command index, coordination index, planning catalog, or the human README and command-doc surfaces those canonical machine answers point to.

## Use When
- Publishing or changing the canonical machine answer for a common planning or governance question.
- Adding an authority-discovery query surface for agents or automation.
- Reviewing whether a proposed lookup policy belongs in the authority map or in a different registry or index.

## Related Standards and Sources
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): defines the canonical deep-planning machine join that the authority map should point to for full trace-linked planning context.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): defines the machine start-here planning surface the authority map should point to for current-state questions.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): defines the durable trace-linked source join the authority map should distinguish from the planning catalog.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): defines the broader repository path lookup surface the authority map must not duplicate.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): defines schema-catalog update expectations for this registry family.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/registries/authority_map/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model canonical-surface lookup as an authored registry, not as a derived index.
- Keep the authority map narrow and question-driven.
- Treat the authority map as policy that answers recurring planning and governance questions, not as a complete inventory of every governed artifact.
- Store published authority maps under `core/control_plane/registries/authority_map/`.
- Keep the companion schema under `core/control_plane/schemas/artifacts/`.
- Use repository-relative paths for canonical and fallback surfaces.
- Every authority entry should name:
  - one stable `question_id`
  - one `domain`
  - one human-readable `question`
  - one canonical `artifact_kind`
  - one canonical machine `canonical_path`
  - one `preferred_command`
  - one or more `fallback_paths`
- Use `preferred_human_path` when one human companion surface materially helps contributors route faster.
- Use `status_fields` only when the question depends on a specific status vocabulary or status interpretation.
- Point to canonical machine surfaces first and use fallback paths for narrower projections, companion trackers, or human guidance.
- Do not use the authority map to restate whole standards, command pages, or README prose.
- Do not let the authority map compete with the path index for general repository navigation or with the command index for exhaustive command discovery.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the authority-map registry family. |
| `id` | Required | Stable identifier for the authority-map registry artifact. |
| `title` | Required | Human-readable title for the registry. |
| `status` | Required | Use the governed lifecycle vocabulary for the registry artifact itself. |
| `entries` | Required | Array of supported planning or governance authority answers. |

### Authority entry fields
| Field | Requirement | Notes |
|---|---|---|
| `question_id` | Required | Stable identifier for the supported lookup question. |
| `domain` | Required | Use `planning` or `governance`. |
| `question` | Required | Human-readable lookup question the entry answers. |
| `status` | Required | Lifecycle status for the authority answer itself. |
| `artifact_kind` | Required | Canonical governed artifact kind that should answer the question. |
| `canonical_path` | Required | Repository-relative path to the canonical machine-readable artifact. |
| `preferred_command` | Required | Preferred CLI command for resolving the same question. |
| `fallback_paths` | Required | One or more narrower projections, companion docs, or adjacent lookup surfaces to use when the canonical path is not enough. |
| `preferred_human_path` | Optional | Human-oriented companion surface such as a tracker, README, or command page. |
| `status_fields` | Optional | Status fields that a consumer should trust when status interpretation matters. |
| `aliases` | Optional | Alternate search phrases that materially improve retrieval. |
| `notes` | Optional | Short policy note clarifying when to use the entry. |

## Validation
- The authority map should validate against its published schema.
- Every entry should point to an existing repository-relative canonical path.
- Every entry should publish at least one fallback path.
- `preferred_command` should name a currently supported command surface.
- Reviewers should reject entries that duplicate the path index, command index, or README prose without adding canonical-precedence value.

## Change Control
- Update this standard when the repository changes how canonical planning or governance surfaces are resolved.
- Update the companion schema, live registry, examples, command docs, root and planning entrypoints, and affected governance standards in the same change set when authority precedence changes materially.
- Prefer updating the authority map over scattering canonical-surface policy across several READMEs.

## References
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md)
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md)
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/registries/authority_map/README.md)

## Updated At
- `2026-03-11T03:10:00Z`
