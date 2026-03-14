---
id: "std.governance.rewrite_surface_classification"
title: "Rewrite Surface Classification Standard"
summary: "This standard defines the four-axis classification and retention-reason model that the structural rewrite program must use before any surface is moved, retired, or reclassified."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "rewrite"
  - "surface_classification"
owner: "repository_maintainer"
updated_at: "2026-03-14T02:37:25Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/"
  - "docs/standards/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "rewrite classification"
  - "four-axis classification"
  - "rewrite retention reasons"
---

# Rewrite Surface Classification Standard

## Summary
This standard defines the four-axis classification and retention-reason model that the structural rewrite program must use before any surface is moved, retired, or reclassified.

## Purpose
- Keep rewrite cleanup decisions grounded in current repository authority boundaries instead of informal archive language.
- Separate lifecycle, authority, placement, and compatibility concerns so history and compatibility work do not blur into one vague status label.
- Make retained compatibility and historical surfaces reviewable before any Phase 2 or later cleanup slice changes them.

## Scope
- Applies to structural-rewrite planning, review, migration, and cleanup slices.
- Applies to governed docs, governed machine-readable artifacts, runtime boundary surfaces, and compatibility markers touched by the rewrite program.
- Covers surface classification, retention reasons, and rewrite-specific action selection.
- Does not replace family-specific lifecycle, task-placement, or acceptance-contract rules.

## Use When
- Completing Phase 0 or Phase 1 rewrite work.
- Preparing a later rewrite slice that proposes moving, deleting, reclassifying, or retiring a surface.
- Reviewing whether a surface is an intentional compatibility boundary, a historical record, or redundant cleanup debt.

## Related Standards and Sources
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md): lifecycle status must stay within the shared `draft` or `active` or `deprecated` vocabulary.
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): retained historical planning records should use existing `authority: historical` signaling instead of new lifecycle words.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task history already has a family-native placement model through `open/` and `closed/`.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): canonical planning-authority answers must remain explicit when classification work touches discoverability.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): compatibility shims stay temporary by default, but only after current consumers and boundary value are made explicit.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): history and compatibility work must preserve one clear canonical answer per question.

## Guidance
- Classify every significant rewrite surface on four independent axes before choosing a retirement, relocation, or retention action.
- Use the shared lifecycle vocabulary exactly as published:
  - `draft`
  - `active`
  - `deprecated`
- Do not use `archived` as a lifecycle state for rewrite execution.
- Use these rewrite authority-role values:
  - `authored_authority`
  - `canonical_machine_answer`
  - `discovery_index`
  - `generated_projection`
  - `historical_record`
  - `compatibility_surface`
- Use these storage or placement classes:
  - `active_family_location`
  - `family_native_closed_or_historical_location`
  - `compatibility_namespace_or_marker`
  - `deleted_after_proof`
  - `future_standardized_history_store`
- Use these compatibility support levels when a surface is acting as compatibility:
  - `supported`
  - `transitional`
  - `deprecated`
  - `n/a`
- Add an explicit retention reason when a surface is classified as a compatibility surface or retained historical record.
- Use only these rewrite retention-reason values:
  - `public_contract_preservation`
  - `import_stability`
  - `boundary_clarity`
  - `repository_path_continuity`
  - `discoverability`
  - `historical_context`
  - `migration_window`
- Treat `status: deprecated` plus `authority: historical` as the default in-place history model for retained planning records.
- Treat `docs/planning/tasks/open/` and `docs/planning/tasks/closed/` as the current family-native history model for task movement.
- Prefer deletion after proof only when consumer maps, discoverability checks, and rollback expectations show no active dependency remains.
- No rewrite slice may move or delete a surface until:
  - its four-axis classification is published
  - any required retention reason is published
  - current consumers are mapped
  - discoverability impact is documented

## Structure or Data Model
### Required classification axes
| Axis | Allowed Values | Question Answered |
|---|---|---|
| Lifecycle status | `draft`, `active`, `deprecated` | Is the governed artifact current, still being authored, or retained temporarily? |
| Authority role | `authored_authority`, `canonical_machine_answer`, `discovery_index`, `generated_projection`, `historical_record`, `compatibility_surface` | What job does this surface perform in the repository model? |
| Storage or placement class | `active_family_location`, `family_native_closed_or_historical_location`, `compatibility_namespace_or_marker`, `deleted_after_proof`, `future_standardized_history_store` | Where does the surface live and why? |
| Compatibility support level | `supported`, `transitional`, `deprecated`, `n/a` | Is the surface an intentional live boundary, a migration aid, or not a compatibility surface at all? |

### Retention reasons
| Retention Reason | Use When |
|---|---|
| `public_contract_preservation` | The surface still answers a supported public question or command/runtime boundary. |
| `import_stability` | Current code or supported import guidance still relies on the surface. |
| `boundary_clarity` | The surface exists to show an explicit wrapper, facade, or boundary rather than to own behavior. |
| `repository_path_continuity` | Planning docs, tasks, or repository-path lookup still need a stable historical path. |
| `discoverability` | Query or README navigation still intentionally exposes the surface for lookup. |
| `historical_context` | The surface remains needed for rationale, lineage, or cancelled/closed trace history. |
| `migration_window` | The surface is intentionally temporary while a bounded replacement is being proven. |

### Rewrite action model
| Condition | Preferred Action |
|---|---|
| Still answers a live authority question | Keep active in place. |
| No longer live authority but still needed for rationale or lineage | Keep as historical in place. |
| Family already has a governed historical placement model | Use that family-native move. |
| Compatibility surface still has active consumers or boundary value | Keep with explicit support level and retention reason. |
| Compatibility surface is proven transitional and replacement is live | Retire after proof and rollback review. |
| Surface has no active consumers and no retained policy value | Delete after proof. |

## Process or Workflow
1. Identify the surface family and the rewrite slice touching it.
2. Assign the four required axes using the controlled values above.
3. If the surface is compatibility-scoped or historical, record its retention reason and current consumers.
4. Choose the preferred action from the rewrite action model.
5. Update the consumer map, checkpoint doc, and any migration or evidence records before executing the slice.

## Examples
- `core/control_plane/indexes/coordination/coordination_index.v1.json` is `active`, `canonical_machine_answer`, `active_family_location`, and `n/a`.
- `docs/planning/prds/decision_supersession_and_regression_evidence_alignment.md` is `deprecated`, `historical_record`, `active_family_location`, and `n/a` when retained as explicit historical context.
- `core/python/src/watchtower_core/query/` is `active`, `compatibility_surface`, `compatibility_namespace_or_marker`, and usually `supported` while the repo still publishes the namespace as a current boundary-layer import surface.
- `core/python/tests/integration/test_control_plane_artifacts.py` can remain `active`, `compatibility_surface`, `compatibility_namespace_or_marker`, and `supported` when repository-path continuity and query-path discoverability still depend on it.

## Operationalization
- `Modes`: `documentation`; `workflow`
- `Operational Surfaces`: `docs/planning/design/implementation/structural_rewrite_program.md`; `core/control_plane/contracts/compatibility/`; `docs/planning/tasks/`; `core/control_plane/registries/authority_map/authority_map.v1.json`

## Validation
- Rewrite reviews should reject proposals that classify a surface with fewer than four axes.
- Rewrite reviews should reject `archived` as a lifecycle-state substitute.
- Compatibility-retirement proposals should publish a support level and retention reason before proposing deletion.
- Historical-cleanup proposals should use family-native history handling where it already exists instead of inventing a new archive model.

## Change Control
- Update this standard when the rewrite program changes its controlled classification or retention-reason vocabulary.
- Update the structural rewrite implementation plan, checkpoint surfaces, and any same-change history or compatibility classifications when this standard changes materially.

## References
- [status_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/status_tracking_standard.md)
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)

## Updated At
- `2026-03-14T02:37:25Z`
