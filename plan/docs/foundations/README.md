# `foundations`

## Description
`This directory contains the shared WatchTowerPlan foundations corpus. core/docs/foundations/ is the authored source and plan/docs/foundations/ is the required byte-identical mirror. Update the authored copy in core and refresh the mirror in the same change set.`

## Audience Routes

| Audience | Start Here | Then Read | Why |
|---|---|---|---|
| Engineers and maintainers | `repository_scope.md` | `engineering_design_principles.md`, `engineering_stack_direction.md`, `repository_standards_posture.md` | Use this route when deciding what belongs in this repo and how the governed core should evolve. |
| Product owners and engineering leads | `repository_scope.md` | `product_direction.md`, `customer_story.md`, `engineering_design_principles.md` | Use this route when future product direction matters, but current repository scope still needs to stay explicit. |
| Designers and future product reviewers | `product_direction.md` | `customer_story.md`, `repository_scope.md` | Use this route when shaping future product experience while staying grounded in what this repo does and does not own yet. |
| Repo reviewers and auditors | `repository_scope.md` | `plan/plan_overview.md`, `repository_standards_posture.md` | Use this route when the main question is live repository coherence, authority, and the next active plan-domain action. |

## Machine Routes

| Need | Start Here | Why |
|---|---|---|
| Find the governing foundation document for one repo surface, citation path, or applied-reference path | `core/docs/commands/core_python/watchtower_core_query_foundations.md` | Uses the machine-readable foundation index for deterministic lookup instead of rescanning the full foundations corpus manually. |
| Rebuild the machine-readable foundations corpus after a foundations-doc change | `core/docs/commands/core_python/watchtower_core_sync_foundation_index.md` | Keeps the published foundation index aligned with the human foundation documents in the same change set. |

## Authoritative Backbone

| Path | Role |
|---|---|
| `repository_scope.md` | Canonical current-repository charter and ownership boundary. |
| `engineering_design_principles.md` | Canonical design-philosophy baseline for the repository and its operating model. |
| `repository_standards_posture.md` | Canonical standards-posture baseline for governed behavior and authority rules. |
| `engineering_stack_direction.md` | Canonical technology-direction baseline for current implementation choices. |
| `product_direction.md` | Canonical future-product shape baseline that must be read through the current repository boundary. |

## Supporting Future-State Context

| Path | Role |
|---|---|
| `customer_story.md` | Supporting future-state product narrative and operator story. |

## Mirror Rule

- `core/docs/foundations/` is the authored source.
- `plan/docs/foundations/` must remain byte-identical to the authored source.
- `docs/foundations/` is retired and must not be recreated as a third foundations family.

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the foundations directory and the intended read order across its documents. |
| `repository_scope.md` | Defines the authoritative current repository charter and ownership boundary. |
| `engineering_design_principles.md` | Defines the governing engineering design principles and operating model for the repository. |
| `product_direction.md` | Defines the future WatchTower product direction, layer boundaries, and first-wave scope. |
| `customer_story.md` | Provides supporting future-state product story, user problem, and intended operator experience. |
| `repository_standards_posture.md` | Explains the repository-wide standards posture and authority model. |
| `engineering_stack_direction.md` | Defines the current technology-direction baseline and selection rules for the repository. |
