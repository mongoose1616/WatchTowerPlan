# `docs/foundations`

## Description
`This directory contains the repository foundation documents. Use it for the durable scope, design-philosophy, standards-context, technology-direction, product-direction, and future-state narrative materials that shape the rest of the repository. Start with current repository scope, then load the narrower future-product or engineering foundations you need.`

## Audience Routes

| Audience | Start Here | Then Read | Why |
|---|---|---|---|
| Engineers and maintainers | `repository_scope.md` | `engineering_design_principles.md`, `engineering_stack_direction.md`, `repository_standards_posture.md` | Use this route when deciding what belongs in this repo and how the governed core should evolve. |
| Product owners and engineering leads | `repository_scope.md` | `product_direction.md`, `customer_story.md`, `engineering_design_principles.md` | Use this route when future product direction matters, but current repository scope still needs to stay explicit. |
| Designers and future product reviewers | `product_direction.md` | `customer_story.md`, `repository_scope.md` | Use this route when shaping future product experience while staying grounded in what this repo does and does not own yet. |
| Repo reviewers and auditors | `repository_scope.md` | `SUMMARY.md`, `repository_standards_posture.md` | Use this route when the main question is overall repository coherence, authority, and next remediation work. |

## Machine Routes

| Need | Start Here | Why |
|---|---|---|
| Find the governing foundation document for one repo surface, citation path, or applied-reference path | `docs/commands/core_python/watchtower_core_query_foundations.md` | Uses the machine-readable foundation index for deterministic lookup instead of rescanning the full foundations corpus manually. |
| Rebuild the machine-readable foundations corpus after a foundations-doc change | `docs/commands/core_python/watchtower_core_sync_foundation_index.md` | Keeps the published foundation index aligned with the human foundation documents in the same change set. |

## Authoritative Backbone

| Path | Role |
|---|---|
| `docs/foundations/repository_scope.md` | Canonical current-repository charter and ownership boundary. |
| `docs/foundations/engineering_design_principles.md` | Canonical design-philosophy baseline for the repository and its operating model. |
| `docs/foundations/repository_standards_posture.md` | Canonical standards-posture baseline for governed behavior and authority rules. |
| `docs/foundations/engineering_stack_direction.md` | Canonical technology-direction baseline for current implementation choices. |
| `docs/foundations/product_direction.md` | Canonical future-product shape baseline that must be read through the current repository boundary. |

## Supporting Future-State Context

| Path | Role |
|---|---|
| `docs/foundations/customer_story.md` | Supporting future-state product narrative and operator story. |

## Paths
| Path | Description |
|---|---|
| `docs/foundations/README.md` | Describes the purpose of the foundations directory and the intended read order across its documents. |
| `docs/foundations/repository_scope.md` | Defines the authoritative current repository charter and ownership boundary. |
| `docs/foundations/engineering_design_principles.md` | Defines the governing engineering design principles and operating model for the repository. |
| `docs/foundations/product_direction.md` | Defines the future WatchTower product direction, layer boundaries, and first-wave scope. |
| `docs/foundations/customer_story.md` | Provides supporting future-state product story, user problem, and intended operator experience. |
| `docs/foundations/repository_standards_posture.md` | Explains the repository-wide standards posture and authority model. |
| `docs/foundations/engineering_stack_direction.md` | Defines the current technology-direction baseline and selection rules for the repository. |
