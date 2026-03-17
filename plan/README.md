# `plan/`

## Description
`This directory is the live plan-domain workspace for capture-first initiative and project state. Stage 1 seeds the root, machine authority entrypoint, and scoped containers that future WatchTower-targeted implementation work will use.`

## Paths
| Path | Description |
|---|---|
| `plan/README.md` | Describes the purpose of the plan root and the main surfaces seeded here. |
| `plan/AGENTS.md` | Defines plan-domain instructions for live plan work and authority surfaces. |
| `plan/plan_overview.md` | Renders the current pack-level plan status board from authoritative machine state. |
| `plan/.wt/` | Holds the authoritative machine-readable plan-pack root and Stage 1 bootstrap record. |
| `plan/docs/` | Holds the seeded durable plan-guidance root for future promoted guidance. |
| `plan/initiatives/` | Holds pack-wide initiative containers for live work. |
| `plan/projects/` | Holds project containers and project-scoped initiative roots. |
| `plan/workflows/` | Holds the plan-domain workflow routing tables and plan-owned workflow modules. |

## Notes
- Human start-here: `plan/README.md`, then `plan/plan_overview.md`.
- Authoritative implementation contract for the current migration: `requirements.md` and `decisions.md`.
- Use local standards, references, and retained docs-backed planning context only where they conform to that contract.
- Human workflow start-here: `plan/workflows/README.md`.
- `plan/.wt/` is the authoritative machine root for new live plan-pack state.
- `plan/AGENTS.md` is the local instruction layer for work under `plan/**`.
- Use `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work.
- `plan/plan_overview.md` and the initiative-local rendered views are derived from the live machine state and must stay current with the indexes under `plan/.wt/indexes/`.
- `plan/.wt/registries/retention_policy_registry.json` is the live policy surface for how frozen `docs/planning/**` history, transitional initiative archives, promoted guidance, and purge ledgers should be treated during migration and in the clean endstate.
- `plan/.wt/registries/promotion_policy_registry.json` governs what initiative-local outputs may be promoted into durable `plan/docs/**` guidance and when mirrored updates are required.
- `plan/.wt/registries/relation_type_registry.json` and `plan/.wt/policies/status_transition_rules.json` are the plan-pack rule surfaces for controlled relation names and family-specific lifecycle transitions.
- `plan/.wt/registries/artifact_family_registry.json` is the plan-pack taxonomy for artifact placement rules, allowed status subsets, renderability, and derived-index participation.
- `plan/.wt/registries/documentation_family_registry.json` and `plan/.wt/registries/template_catalog.json` now govern authored documentation families, template-backed rendered surfaces, allowed roots, and template assets under `plan/.wt/templates/`.
- `plan/.wt/registries/lifecycle_stage_registry.json`, `review_status_registry.json`, and `source_type_registry.json` now hold the live plan-pack vocabulary for lifecycle, approval, and provenance semantics that must stay consistent with initiative state, readiness views, and promotion/evidence surfaces.
- `plan/.wt/registries/project_surface_policy_registry.json` is the project-root contract for which machine artifacts, rendered views, and optional project-local subroots may exist under `plan/projects/<project_slug>/`.
- `plan/.wt/indexes/promotion_index.json` and `plan/.wt/indexes/guidance_index.json` are the pack-level lookup surfaces for initiative-local promotion records and approved plan guidance.
- Project containers publish their own rendered `project.md`, `repositories.md`, and `summary.md` views after bootstrap, with pack-level project lookup stored in `plan/.wt/indexes/project_index.json`.
- `plan/workflows/ROUTING_TABLE.md` is the authoritative plan-domain routing table, and its routes may reference shared reusable modules under `core/workflows/modules/`.
- Do not start new live work under `docs/planning/**`; the retained bootstrap trace there exists only until later cutover slices replace the old entrypoints.
