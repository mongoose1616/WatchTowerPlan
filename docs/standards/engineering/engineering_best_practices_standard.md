---
id: "std.engineering.best_practices"
title: "Engineering Best Practices Standard"
summary: "This standard defines repository-specific engineering best practices for implementation, validation, and synchronized updates across human-readable and machine-readable surfaces."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "best_practices"
owner: "repository_maintainer"
updated_at: "2026-03-12T22:05:00Z"
audience: "shared"
authority: "authoritative"
---

# Engineering Best Practices Standard

## Summary
This standard defines repository-specific engineering best practices for implementation, validation, and synchronized updates across human-readable and machine-readable surfaces.

## Purpose
Keep implementation work modular, deterministic, reviewable, and aligned with the repository's planning, control-plane, and Python workspace boundaries.

## Scope
- Applies to engineering work that changes code, command behavior, governed machine-readable artifacts, or tightly coupled documentation in this repository.
- Covers repository-specific implementation, validation, and synchronization expectations.
- Does not replace narrower standards for commit format, Python workspace layout, schema design, or command documentation.

## Use When
- Implementing or refactoring code under `core/python/`.
- Adding or changing governed control-plane artifacts under `core/control_plane/`.
- Changing a command, validator, index, contract, or planning surface that has companion machine-readable or human-readable artifacts.
- Reviewing whether a change is modular enough and validated enough for this repository.

## Related Standards and Sources
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): foundation intent this standard must remain aligned with.

## Guidance
- Start from the routed workflow set and the nearest applicable `AGENTS.md` and `README.md` before making changes.
- Keep human planning authority in `docs/planning/`, machine-readable authority in `core/control_plane/`, and executable Python behavior in `core/python/`.
- Prefer deterministic, local-first behavior over hidden heuristics or implicit repository scans.
- Prefer published indexes, registries, and contracts over hardcoded lookup tables when a governed control-plane surface already exists.
- Keep CLI entrypoints thin. Put real behavior in package services and pass explicit arguments rather than hardcoding one-off values in commands.
- Keep modules narrow and composable. Add a new module or service when that makes boundaries clearer instead of growing large mixed-purpose files.
- Prefer explicit `--format` arguments with `human` and `json` modes when a command serves both operators and agents.
- Keep query helpers read-oriented and side-effect free. Keep derived-artifact rebuild or materialization logic in dedicated `sync/` surfaces.
- Update human-readable and machine-readable companion surfaces in the same change set when one depends on the other. Examples include docs plus indexes, command pages plus command-index entries, and schemas plus examples and catalog records.
- Reuse shared schema fragments, typed models, and existing governed IDs instead of duplicating field rules across surfaces.
- When external guidance materially shapes repository policy or design, distill it into `docs/references/**` and have standards or designs cite the local reference doc in addition to, or instead of, raw vendor URLs.
- Use UTC timestamps with the canonical repository field names `updated_at`, `recorded_at`, and later `generated_at` when applicable.
- Prefer deletion over indefinite deprecation when an obsolete artifact no longer needs to remain present.
- Keep generated outputs, caches, and transient runtime state out of governed control-plane surfaces.

## Structure or Data Model
### Repository engineering checkpoints
| Checkpoint | Expectation | Notes |
|---|---|---|
| Boundary fit | Required | The change belongs in the correct repo surface: planning, control plane, or Python workspace. |
| Modularity | Required | New behavior is introduced through scoped services or modules rather than mixed-purpose files. |
| Argument-driven interfaces | Required | Commands and reusable services take explicit inputs instead of embedding task-specific constants. |
| Companion updates | Required when applicable | Related docs, indexes, schemas, examples, and trackers change in the same change set. |
| Validation | Required | The narrowest meaningful automated checks are run before the change is treated as complete. |
| Traceability | Required when applicable | Durable planning, acceptance, validator, or evidence links stay aligned when the change touches traced surfaces. |

## Process or Workflow
1. Confirm the target boundary and routed workflow context before implementing.
2. Place the change in the correct repository layer and keep new code or artifacts modular.
3. Update the companion human-readable and machine-readable surfaces that govern or describe the change.
4. Run the narrowest meaningful validation set for the touched surfaces.
5. Treat the change as incomplete if related indexes, schemas, examples, command docs, or planning trackers are left stale.

## Examples
- A new repo-local query command should add its reusable query service under `core/python/src/watchtower_core/repo_ops/query/`, thin CLI wiring under `cli/`, command docs under `docs/commands/`, and a matching command-index entry under `core/control_plane/indexes/commands/`.
- A new schema-backed artifact family should add the schema, examples, schema-catalog record, and any affected validators in the same change set.
- A change to a traced PRD or acceptance contract should keep the matching indexes, evidence expectations, and linked planning surfaces aligned.

## Operationalization
- `Modes`: `documentation`; `artifact`; `workflow`
- `Operational Surfaces`: `core/python/`; `core/control_plane/`; `docs/planning/`; `workflows/modules/core.md`

## Validation
- Code changes should run the narrowest meaningful automated checks for the touched surfaces, such as targeted `pytest`, schema validation, command smoke tests, or index validation.
- Reviewers should reject changes that hardcode values where a reusable argument-driven interface is expected.
- Reviewers should reject changes that leave companion machine-readable or human-readable surfaces stale.
- Reviewers should reject mixed-purpose modules when the behavior can be separated cleanly into a narrower service or artifact family.

## Change Control
- Update this standard when the repository's engineering operating model changes materially.
- Update related workspace, schema, command, or traceability standards in the same change set when the best-practices rules become more specific in one of those narrower areas.
- Update local instruction surfaces when the default implementation or validation path for contributors changes materially.

## References
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)

## Notes
- This standard is intentionally repo-specific. It complements narrower standards rather than replacing them.
- The goal is consistent engineering behavior, not maximum process weight.

## Updated At
- `2026-03-12T22:05:00Z`
