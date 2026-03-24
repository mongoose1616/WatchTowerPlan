# `plan/`

## Description
`This directory is the live plan-domain workspace for capture-first initiative and project state. It is the normal operating surface for live plan work, derived plan visibility, and promoted plan-domain guidance.`

## Paths
| Path | Description |
|---|---|
| `plan/README.md` | Describes the purpose of the plan root and the main surfaces seeded here. |
| `plan/AGENTS.md` | Defines plan-domain instructions for live plan work and authority surfaces. |
| `plan/plan_overview.md` | Renders the current pack-level plan status board from authoritative machine state. |
| `plan/.wt/` | Holds the authoritative machine-readable plan-pack root and Stage 1 bootstrap record. |
| `plan/docs/` | Holds durable promoted plan guidance plus the mirrored foundations family. |
| `plan/initiatives/` | Holds pack-wide initiative containers for live work. |
| `plan/projects/` | Holds project containers and project-scoped initiative roots. |
| `plan/workflows/` | Holds the plan-domain workflow routing tables, plan-owned workflow modules, and plan-owned workflow roles. |

## Notes
- Human start-here: `plan/README.md`, then `plan/plan_overview.md`.
- Current implementation contract: mirrored foundations under `plan/docs/foundations/`, promoted plan standards under `plan/docs/standards/`, and live plan-pack machine authority under `plan/.wt/**`.
- Use local references and helper docs only where they remain consistent with those current authority surfaces.
- Human workflow start-here: `plan/workflows/README.md`.
- `plan/.wt/` is the authoritative machine root for new live plan-pack state.
- `plan/.wt/**` is machine state only; keep Python source, workflow prose, and hand-maintained implementation logic out of that tree.
- `plan/AGENTS.md` is the local instruction layer for work under `plan/**`.
- `plan/docs/foundations/` is the mirrored foundations view and must stay byte-identical with `core/docs/foundations/`.
- `plan/python/` is the approved plan-owned Python boundary for narrow repo-local plan behavior that should not live in reusable core.
- `plan/` is the first internal hosted pack, not a universal downstream bootstrap requirement. Include it in copied repositories or customer handoff only when the recipient intentionally carries the plan pack.
- Use `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work.
- `plan/plan_overview.md` and the initiative-local rendered views are derived from the live machine state and must stay current with the indexes under `plan/.wt/indexes/`.
- `plan/.wt/registries/retention_policy_registry.json` is the live policy surface for promoted guidance and terminal initiative retention behavior.
- `plan/.wt/registries/promotion_policy_registry.json` governs what initiative-local outputs may be promoted into durable `plan/docs/**` guidance and when mirrored updates are required.
- `plan/.wt/registries/relation_type_registry.json` and `plan/.wt/policies/status_transition_rules.json` are the plan-pack rule surfaces for controlled relation names and family-specific lifecycle transitions.
- `plan/.wt/registries/artifact_family_registry.json` is the plan-pack taxonomy for artifact placement rules, allowed status subsets, renderability, and derived-index participation.
- `plan/.wt/registries/documentation_family_registry.json` and `plan/.wt/registries/template_catalog.json` now govern authored documentation families, template-backed rendered surfaces, allowed roots, and template assets under `plan/.wt/templates/`.
- `plan/.wt/registries/lifecycle_stage_registry.json`, `review_status_registry.json`, and `source_type_registry.json` now hold the live plan-pack vocabulary for lifecycle, approval, and provenance semantics that must stay consistent with initiative state, readiness views, and promotion/evidence surfaces.
- `plan/.wt/registries/project_surface_policy_registry.json` is the project-root contract for which machine artifacts, rendered views, and optional project-local subroots may exist under `plan/projects/<project_slug>/`.
- `plan/.wt/indexes/promotion_index.json` and `plan/.wt/indexes/guidance_index.json` are the pack-level lookup surfaces for initiative-local promotion records and approved plan guidance.
- `plan/.wt/indexes/artifact_index.json` is the pack-level cross-family lookup surface for live plan machine artifacts, pack work-item notes, and aggregate indexes.
- Project containers publish their own rendered `project.md`, `repositories.md`, and `summary.md` views after bootstrap, with pack-level project lookup stored in `plan/.wt/indexes/project_index.json`.
- `plan/workflows/ROUTING_TABLE.md` is the authoritative plan-domain routing table, and its routes may reference shared reusable modules under `core/workflows/modules/` and shared workflow roles under `core/workflows/roles/`.
- Legacy docs-backed planning has already been purged. Closed trace packages may be retired after promotion without creating a retained purge-history family.
- Customer-safe releases should exclude internal project views, retained records, and other donor plan state unless the recipient explicitly needs the internal plan pack history.
