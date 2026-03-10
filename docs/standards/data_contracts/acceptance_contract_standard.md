---
id: "std.data_contracts.acceptance_contract"
title: "Acceptance Contract Standard"
summary: "This standard defines machine-readable acceptance contracts stored under `core/control_plane/contracts/acceptance/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "acceptance_contract"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

# Acceptance Contract Standard

## Summary
This standard defines machine-readable acceptance contracts stored under `core/control_plane/contracts/acceptance/`.

## Purpose
- Provide a deterministic machine-readable acceptance surface derived from durable PRD acceptance criteria.
- Let Python helpers, validators, and workflows load acceptance expectations without parsing PRD prose directly.
- Keep human planning authority in PRDs while giving the control plane an explicit acceptance boundary.

## Scope
- Applies to acceptance contract artifacts stored under `core/control_plane/contracts/acceptance/`.
- Covers placement, required fields, synchronization with PRDs, and update expectations.
- Does not replace PRDs as the human source of truth for scope, goals, or rationale.
- Does not define validation evidence or the unified traceability index.

## Use When
- A PRD publishes durable acceptance criteria that need machine-readable loading.
- Python or workflow automation needs a stable acceptance surface for validation or closeout.
- Reviewing whether acceptance expectations are still only implicit in prose.

## Related Standards and Sources
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Keep the human source of acceptance intent in the PRD.
- Use acceptance contracts as the machine-readable projection of durable acceptance criteria.
- Store published acceptance contracts under `core/control_plane/contracts/acceptance/`.
- Use JSON for published acceptance contracts.
- Use one contract per traced initiative or other durable change boundary.
- Every contract should publish:
  - `trace_id`
  - a stable `contract_id`
  - the source `prd_id`
  - the durable `acceptance_id` values it covers
  - concrete validation targets, related paths, or required validators when those are known
- Prefer stable readable identifiers such as `contract.acceptance.core_python_foundation`.
- Update the acceptance contract in the same change set when the source PRD changes acceptance IDs or materially changes acceptance meaning.
- Keep acceptance contracts focused on what must be accepted, not on recording historical validation results.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the acceptance-contract artifact family. |
| `id` | Required | Stable identifier for the acceptance contract artifact. |
| `title` | Required | Human-readable contract title. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `trace_id` | Required | Shared trace identifier for the initiative. |
| `source_prd_id` | Required | Stable PRD identifier that owns the acceptance intent. |
| `entries` | Required | Array of acceptance records. |

### Acceptance entry fields
| Field | Requirement | Notes |
|---|---|---|
| `acceptance_id` | Required | Stable acceptance identifier from the source PRD. |
| `summary` | Required | Concise machine-readable statement of the acceptance item. |
| `source_requirement_ids` | Optional | Requirement IDs that materially justify the acceptance item. |
| `required_validator_ids` | Optional | Validators expected to support or prove the acceptance item. |
| `validation_targets` | Optional | Concrete repository surfaces or artifacts that should be checked. |
| `related_paths` | Optional | High-signal paths relevant to the acceptance item. |
| `notes` | Optional | Short contract-specific note. |

## Process or Workflow
1. Identify the PRD that publishes durable acceptance criteria.
2. Materialize or update the acceptance contract under `core/control_plane/contracts/acceptance/`.
3. Keep the contract aligned with the source `acceptance_id` values and upstream `trace_id`.
4. Validate the contract against its published schema.
5. Update traceability surfaces and any affected evidence expectations in the same change set.

## Examples
- A PRD that names `ac.core_python_foundation.001` through `.004` should publish those same IDs in the matching acceptance contract.
- A validator-backed acceptance item can list the expected validator IDs instead of forcing downstream tooling to infer them from prose.
- A temporary planning note with no durable acceptance IDs does not need an acceptance contract.

## Validation
- The acceptance contract should validate against its published artifact schema.
- Every `acceptance_id` in the contract should exist in the source PRD.
- Reviewers should reject acceptance contracts that drift materially from the source PRD or invent acceptance IDs not present upstream.
- `trace_id`, `source_prd_id`, and related validator references should stay aligned with the planning and registry surfaces.

## Change Control
- Update this standard when the repository changes how acceptance contracts are shaped or when acceptance becomes part of a broader contract family.
- Update the companion schema, examples, and live acceptance contracts in the same change set when this family changes structurally.
- Update the source PRD, traceability surfaces, and related evidence expectations in the same change set when acceptance meaning changes materially.

## References
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/README.md)

## Notes
- This family exists so Python and workflow automation can consume acceptance expectations consistently.
- It should stay smaller and more structured than the source PRD.

## Updated At
- `2026-03-09T23:02:08Z`
