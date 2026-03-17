# WatchTowerPlan Required Surfaces And Endstate Requirements

This document adapts the conceptual structure of `/home/j/mvp_reference/required.md` to `WatchTowerPlan`.

It is intentionally written for the `plan` domain rather than reusing the source reference's domain-specific artifact names and directory examples. Where the reference uses domain-local examples, this document translates those ideas into planning-and-implementation concepts such as work-item notes, initiative briefs, design records, execution plans, tasks, evidence, closeout recaps, and routed workflow execution.

This file is not a claim that the full endstate already exists in this repository. It is a deep-dive map of:

- what the repo already has
- what is still partial or repo-local
- what new generic core and `plan`-domain surfaces should exist to reach a clean future pack model

## How To Read This File

- A `schema` defines the required shape of one governed machine-readable thing.
- A `registry` defines controlled entries or lookup metadata that multiple schemas or runtime helpers rely on.
- A `policy` defines allowed transitions, retention rules, or other rule-bearing behavior that should not hide in code.
- An `index` is a query-optimized derived surface, not the primary authority.
- A `governance surface` is an authoritative non-artifact control surface used by loaders, validators, routing, or synchronization logic.
- A `rendered view` is a human-readable derivative built from stronger machine authority.
- A `helper` is a focused reusable runtime utility.
- A `harness` is a multi-step runtime entrypoint that coordinates loaders, validators, routing, sync, or rebuild behavior.

Status labels in this file mean:

- `Current`: implemented and actively used in this repo.
- `Partial`: present, but too narrow, too repo-local, still provisional, or still carrying domain leakage.
- `Future`: required for a clean endstate, but not yet fully implemented here.

## Repository Filter And Terminology

The current repository boundary matters:

- `WatchTowerPlan` currently owns the reusable governed substrate under `core/control_plane/` and `core/python/`.
- It currently keeps most live planning state under `docs/planning/`, but this document treats that as a current-state compromise rather than the desired long-term authority model.
- `/home/j/WatchTower` already exists as the permanent downstream product repository, but it is intentionally not the primary execution surface for this requirements effort yet.
- `WatchTowerPlan` remains the planning authority and the proving ground for shared core behavior while the product repository is still intentionally sparse.
- Until explicit downstream product bootstrap begins, any `WatchTower`-facing structures, files, or contracts described here should be treated as implementation-detail requirements recorded in this repository rather than as immediate change targets in `/home/j/WatchTower`.
- In the future model described here, `core/` remains the home for core-only material: `core/python/`, `core/control_plane/`, and `core/docs/`.
- In that same future model, `plan/` becomes the home for everything else: live initiatives, plan-domain guidance, workflows, aggregate tracking, and project-oriented outputs.
- Live initiative state should live in neither `core/docs/` nor `plan/docs/`.
- Human-operational surfaces such as `README.md`, `AGENTS.md`, routed workflow docs, and rendered visibility views should live only on human-facing roots, not inside machine-only `.wt/` trees.

This document therefore uses `plan`-domain wording:

- `work item` as the neutral unit of active planning or implementation work
- `initiative brief` for scoped intake and intent capture
- `design record` and `implementation slice` for solution-shaping and execution planning
- `closeout recap` for terminal summary and evidence-backed completion
- `reference asset`, `standard`, `workflow module`, and `validation bundle` for reusable guidance and governance support

When this document proposes a future `plan/` live-work shape, that is the target authority model for the internal `plan` domain in this repo, not a claim that the migration is already complete.

## Executive Summary

- The repo already has the right architectural direction for a future core-plus-pack system: machine-readable control-plane authority, pack settings, typed loading, schema-first validation, routed workflows, and a large derived-index surface are all real.
- The strongest current reusable-core areas are `watchtower_core.control_plane`, `watchtower_core.validation`, the schema catalog, validator registry, validation suite registry, rendered-surface registry, workflow metadata registry, and the typed pack context.
- The strongest current repo-local consumer is the planning-and-implementation corpus under `docs/planning/`, but that is also the clearest current authority mismatch because live planning data is living in docs instead of in a first-class live workspace.
- The main missing area is not basic governance. It is the next layer of generic pack runtime: initiative-centric live state, event-backed lifecycle contracts, export-safe query, sync, rebuild, workflow execution, artifact-family resolution, and extraction or promotion of durable guidance out of live work.
- Validation has recently crossed an important boundary: it is now pack-aware reusable-core behavior with a `plan` fixture pack proving schema catalog, validator registry, and validation suite loading through `pack_settings`.
- Some pack-facing interfaces still carry legacy domain leakage and need cleanup before they should be treated as stable generic contracts. The most concrete examples are `challenge`-scoped status entries and `artifact_index` fields such as `challenge_id`, `source_platform`, and `source_event`.
- The future endstate should treat each initiative as a live planning container under either `plan/initiatives/<initiative_slug>/` for pack-wide work or `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work, with initiative-local `.wt/` machine state and initiative-local rendered human views such as `plan.md`, `progress.md`, and `summary.md`.
- In that endstate, `plan_overview.md` should answer "what is plan, what is in flight, and what needs attention now?" through a short domain description plus a sectioned status board built from pack-level aggregate state.
- In that endstate, `core/docs/foundations/` and `plan/docs/foundations/` intentionally duplicate the foundations corpus and stay aligned because both core and plan depend on the same guiding context.

## Current Architecture Snapshot

| Layer | Current State | Endstate Implication |
|---|---|---|
| Core docs corpus | `docs/foundations/` and other reviewed docs already act as durable core guidance, but they are not yet rooted under `core/docs/`. | `core/docs/` should hold documentation that is only about core function, management, engineering, and bootstrap guidance, including a duplicated `core/docs/foundations/` corpus kept aligned with plan. |
| Plan-domain guidance corpus | Missing as a distinct long-term home. | `plan/docs/` should hold approved extracted plan-domain guidance, including a duplicated `plan/docs/foundations/` corpus kept aligned with core. |
| Live planning workspace | There is no first-class live initiative root yet; `docs/planning/` and its companion control-plane indexes currently fill that role. | `plan/initiatives/<initiative_slug>/` should carry pack-wide work, while `plan/projects/<project_slug>/initiatives/<initiative_slug>/` should carry project-scoped work. |
| Initiative-local machine state | Missing as an explicit first-class layout. Current machine state is mostly derived from markdown planning families and sync outputs. | Each initiative should own a local `.wt/` machine layer with initiative snapshot, event history, task state, promotion records, and evidence. |
| Pack-level live aggregates | Missing as an explicit `plan/.wt/` root. Current planning, initiative, and coordination indexes live under `core/control_plane/` and are largely sourced from `docs/planning/`. | `plan/.wt/` should provide aggregate initiative and task lookup, status rollups, and fast tracking views without crawling every initiative directory. |
| Core workflow corpus | The current repo-level `workflows/` tree mixes concerns that should ultimately live under the domain they serve. | `core/workflows/` should hold core-only workflow docs, routing references, and operator procedures. |
| Plan-domain workflow corpus | The current repo-level `workflows/` tree exists, but the future `plan/` workspace shape does not yet account for a plan-local workflow home. | `plan/workflows/` should become the human workflow corpus for initiative, project, and promotion procedures, with machine companions under `plan/.wt/`. |
| Human navigation and instruction surfaces | README and AGENTS placement is mostly incidental today. | Human-facing roots should get deliberate `README.md` coverage, while `AGENTS.md` should exist only where interaction rules materially change; machine-only `.wt/` trees should not rely on local instruction files. |
| Project workspace | Missing as an explicit first-class layout. | `plan/projects/<project_slug>/` should hold that project's own context, supporting documentation, references, linked repository information, and other project-specific material. |
| Permanent product repository boundary | `/home/j/WatchTower` exists as the permanent downstream product repo, but the current requirements and core-shaping work are still being executed from `WatchTowerPlan`. | `WatchTower` should remain the long-term home for operator-facing product implementation, while this repo remains the planning authority and core proving area until downstream bootstrap is explicitly started. |
| Machine-readable control plane | `core/control_plane/` is already the canonical machine authority for schemas, registries, indexes, contracts, ledgers, and manifests. | Strong foundation. Future work should add missing pack-runtime families here or in future pack-owned `.wt/` roots without blurring authority. |
| Reusable runtime | `watchtower_core.control_plane`, `watchtower_core.validation`, `watchtower_core.evidence`, and selected adapters are reusable-core oriented. | Validation is now meaningfully pack-aware. Query, sync, and rebuild still need a cleaner export-safe story. |
| Repo-local orchestration | `watchtower_core.repo_ops` and `watchtower_core.cli` own planning-specific query, sync, rendered tracking, task lifecycle, and route CLI behavior. | This split is correct for now, but it needs to re-root from docs-backed planning families to initiative-backed live pack state. |
| Current pack-facing interfaces | `core/control_plane/schemas/interfaces/packs/` already publishes pack settings, governance map, path/status/actor registries, artifact index, work-item note, and extraction envelope interfaces. | Good seed set, but still incomplete and in places too domain-leaky for a stable pack contract. |
| Validation proof surface | `core/python/tests/fixtures/domain_packs/plan/.wt/` proves a minimal `plan` pack through pack-aware validation. | Important milestone. The same proof strategy should later expand to query, sync, route, and rendered-surface behavior. |
| Derived indexes and rendered views | The repo already generates command, route, workflow, planning, coordination, initiative, task, traceability, reference, and standards indexes plus rendered tracking pages. | Rich current state, but the live planning-derived surfaces should ultimately be sourced from `plan/initiatives/` and `plan/.wt/`, not from `docs/planning/`. |

## Endstate Authority And Precedence Rules

These rules are part of the intended endstate, not optional implementation detail.

- repository root stays thin and acts only as a routing entrypoint; first-class operational content belongs under `core/` or `plan/`
- `WatchTowerPlan` remains the planning authority and core proving repository even after `WatchTower` exists as the permanent product consumer repository
- `WatchTower` is the permanent product implementation repository, but it is not a second planning authority and it should not redefine planning truth owned here
- `core/control_plane/` remains the authoritative machine root for reusable core-owned surfaces
- `plan/.wt/` remains the authoritative machine root for plan-pack-owned surfaces
- authored human surfaces are governed by machine contracts; rendered human surfaces are derived from stronger machine authority and are never the primary source of truth
- rendered surfaces such as `plan_overview.md`, initiative `plan.md`, initiative `progress.md`, and initiative `summary.md` are not manually authoritative; any direct edits must be treated as regeneration drift unless a family is explicitly classified as authored
- pack-wide initiatives may live only under `plan/initiatives/`
- project-scoped initiatives may live only under `plan/projects/<project_slug>/initiatives/`
- if work affects more than one project or the pack itself, it is pack-wide rather than project-scoped
- `pack_context` is always the first runtime context load for standard commands and helpers
- `project_context` is a second, explicit context load that applies only when the path, command, or workflow targets one project
- duplicated foundations under `core/docs/foundations/` and `plan/docs/foundations/` must behave as one logical mirrored family; divergence between the copies is invalid
- any future exception to these precedence rules requires explicit owner approval plus machine-readable and human-readable justification

## Current Execution Boundary Before Product Bootstrap

The permanent product boundary and the current execution boundary are intentionally different right now.

- `/home/j/WatchTower` is the permanent downstream product repository
- current requirements capture, planning authority, core proving, and near-term implementation execution remain in `WatchTowerPlan`
- this document is therefore allowed to define future `WatchTower`-facing expectations without requiring immediate file creation or bootstrap work in `/home/j/WatchTower`
- until explicit downstream bootstrap begins, any `WatchTower` additions should be represented here as downstream implementation obligations, contracts, or directory-shape requirements rather than as parallel truth authored in the product repo
- when downstream product bootstrap does begin, `WatchTower` should receive implementation-backed outputs from approved requirements, designs, and implementation work here rather than ad hoc structure invented independently there
- this rule exists to avoid splitting authority too early while the shared core and internal `plan` pack are still being rationalized in place

## Python Modules / Helpers / Harness

| Name | Current State | Future Endstate Requirement | Required Change |
|---|---|---|---|
| `pack_context` | `Current` | Remain the canonical runtime context for pack-aware services. | Expand only by declared surfaces and typed models, not by repo-specific shortcuts. |
| `project_context_loader` | `Missing` | Load project-specific context separately from `pack_context` when a path, command, or workflow is project-scoped. | Build it on top of `project_record`, `project_repository_map`, and project-local guidance rather than overloading `pack_context`. |
| `pack_settings_loader` | `Current` inside `ControlPlaneLoader` | Keep fail-closed load-root validation, version checks, and startup resolution. | Split into a more explicit pack-entry helper only if a second consumer pack makes the seam valuable. |
| `schema_loader` / `schema_store` | `Current` | Remain the shared schema authority for core-owned and pack-owned schemas. | Keep merged-catalog behavior and add more explicit support for shared subschema families if future pack contracts require them. |
| `governance_surface_resolver` | `Partial` | Provide a direct helper that answers where a governed surface lives, whether it is authoritative, whether it is rebuildable, and what companion views depend on it. | Today this knowledge is spread across `pack_settings`, `governance_surface_map`, and loader logic. Consolidate it behind one query surface. |
| `artifact_family_resolver` | `Missing` | Load an authoritative artifact-family taxonomy for plan-pack artifacts and answer placement, status, visibility, and renderability rules. | Add `artifact_family_registry` and typed helpers instead of inferring family behavior from scattered indexes or path conventions. |
| `path_and_id_helpers` | `Partial` | Provide generic pack-relative path, id, slug, and naming coherence helpers. | Today path rules are split between path registries, per-family conventions, and repo-local helpers. |
| `query_harness` | `Current` at reusable-core root | Offer export-safe querying over pack surfaces, indexes, registries, routes, workflow metadata, and artifact families. | Keep reusable-core query exports focused on governed generic metadata while leaving live planning and docs-backed repo-local query services under `repo_ops`. |
| `validation_harness` | `Current` and strong | Stay the fail-closed, schema-first, pack-aware validation entrypoint. | Expand suite step kinds later for rendered views, compatibility checks, lifecycle rules, and discrepancy policies without leaking repo-local semantics. |
| `sync_harness` | `Partial` | Coordinate authority-preserving synchronization across pack-owned and repo-owned surfaces. | Today sync remains repo-local behind `watchtower_core.repo_ops.sync`. A reusable core sync layer is still missing. |
| `rebuild_harness` | `Missing` | Deterministically regenerate indexes and rendered views from stronger authority. | Separate rebuild from sync once a second pack or non-planning derived surface set exists. |
| `routing_engine` | `Partial` | Remain the authoritative machine route selector driven by routing metadata and workflow metadata. | The route system exists, but it is still operationally tied to repo-local CLI and workflow surfaces rather than a stable reusable runtime API. |
| `route_preview_helper` | `Partial` | Expose typed advisory route-preview results that downstream packs can call without importing repo-local CLI handlers. | The repo already has `watchtower-core route preview`, but the reusable runtime contract is still implicit. |
| `workflow_catalog_helper` | `Partial` | Query workflow metadata, route relationships, compatibility, and companion workflows through one helper. | Current metadata exists in `workflow_metadata_registry` and indexes, but the reusable helper layer is thin. |
| `workflow_execution_harness` | `Missing` | Execute routed workflow chains with mode checks, gates, and event recording. | The repo can route workflows, but it does not yet publish a generic workflow execution contract. |
| `event_stream_helper` | `Current` | Provide append-only event recording, validation, and replay for initiative-level and task-level live planning history. | Keep the helper generic and schema-backed while initiative-local and task-local planning services build on it for concrete event families. |
| `markdown_reconciliation` | `Partial` | Provide a pack-safe way to reconcile rendered human initiative surfaces with authoritative machine state. | Current front matter adapters and planning rendered builders are useful, but still planning-specific and docs-centric. |
| `rendered_view_builder` | `Partial` | Rebuild initiative-local and pack-level rendered views from authoritative machine surfaces through a generic registry-backed builder. | Today rendered planning trackers are rich, but their builders remain repo-local and mostly target docs-backed planning families. |
| `artifact_index_builder` | `Current` | Build a generic pack artifact index across plan-domain artifact families and lifecycle surfaces. | The live artifact-index builder now rebuilds the plan-pack artifact catalog across initiative, project, work-item-note, and aggregate-index families. |
| `evidence_helper` | `Partial` | Expand from validation evidence into a broader evidence bundle model usable by pack closeout and review. | `validation_evidence` already exists, but there is no general pack evidence contract. |
| `discrepancy_helper` | `Current` | Turn validation and sync drift into first-class discrepancy records with controlled severity and resolution. | Keep the helper schema-backed and reusable while plan services provide concrete drift detection and managed-category policy. |
| `initiative_tracking_builder` | `Current` | Build pack-level initiative and task rollups under `plan/.wt/` from both pack-wide initiatives and project-scoped initiatives. | Plan-workspace sync now rebuilds initiative, task, readiness, discrepancy, promotion, guidance, coordination, and project rollups across both initiative root types. |
| `guidance_promotion_helper` | `Current` | Extract reviewed durable decisions, standards, references, and long-term guidance out of live initiative state into `plan/docs/`, with optional core-specific duplication into `core/docs/`. | The live promotion helper now writes governed durable guidance, updates initiative-local promotion records, and supports mirrored foundation fan-out rules. |
| `closeout_helper` | `Partial` | Coordinate initiative closeout recaps, required evidence, promotion candidates, and terminal state transitions. | Current closeout logic is initiative-oriented but still coupled to the docs-based planning corpus. |
| `environment_context_helper` | `Missing` | Normalize execution context and expose it to routing, workflow safety, and evidence surfaces. | No durable environment contract exists yet. |
| `actor_registry_helper` | `Partial` | Resolve actors, validate actor references, and enforce actor-type expectations across surfaces. | Typed actor models exist, but there is no stronger reusable helper and validator layer yet. |
| `terminology_helper` | `Missing` | Provide shared terminology lookup, deprecation, and alias resolution for pack-local vocabulary. | This will matter once the `plan` pack gains a larger reusable guidance layer. |
| `template_catalog_helper` | `Current` | Resolve governed templates and section-spec contracts for pack-authored and rendered surfaces. | The typed template-catalog helper now resolves active template bindings and validates template-path plus section-spec alignment for pack and core surfaces. |
| `release_and_migration_helper` | `Current but not part of the clean target state` | Existing release or migration helpers should not define the long-term operating model for `plan`. | Keep only what is still needed for current cleanup work, then remove or isolate it rather than carrying it into the clean endstate. |

## Surface Type Reference

| Surface Type | Meaning In This Repo |
|---|---|
| `foundation` | Human-readable narrative authority for scope, product direction, standards posture, and design principles. |
| `manifest` | A machine-readable load root or startup contract such as `pack_settings`. |
| `registry` | Controlled machine authority for schemas, validators, workflow metadata, rendered surfaces, status values, actors, and similar lookup or rule-bearing data. |
| `schema` | JSON Schema describing one governed artifact or pack-facing interface. |
| `contract` | Machine-readable artifact describing required acceptance or compatibility conditions. |
| `ledger` | Durable append-style or record-style machine history such as validation evidence, release records, migration records, or purge records. |
| `index` | Derived machine-readable lookup surface optimized for query and navigation. |
| `rendered view` | Derived human-readable view from stronger authority. |
| `workflow module` | Human-readable, routed procedure unit selected through the routing system. |
| `instruction surface` | Human-readable navigation or agent-operational surface such as `README.md`, `AGENTS.md`, and workflow route docs. |
| `runtime boundary` | Python package seam distinguishing reusable core from repo-local orchestration. |

## Current Authoritative Surfaces

### Current Governing Startup And Control Surfaces

| Surface | Current Status | Notes |
|---|---|---|
| `pack_settings` | `Current` | The active load root for reusable core lives at `core/control_plane/manifests/pack_settings.json`. |
| `schema_catalog` | `Current` | Authoritative schema catalog exists and is now pack-aware through active pack settings. |
| `validator_registry` | `Current` | Authoritative validator selection exists and can be pack-declared. |
| `validation_suite_registry` | `Current` | Authoritative validation suite sequencing exists and is pack-declared. |
| `governance_surface_map` | `Current` | Declares non-artifact governed surfaces needed by core startup. |
| `path_pattern_registry` | `Current` | Provides path-pattern authority, but remains thinner than a full artifact-family placement system. |
| `status_registry` | `Partial` | Exists, but still carries domain-leaked family names and solution-centric values that need plan-domain cleanup. |
| `actor_registry` | `Current` | Typed actor authority exists. |
| `authority_map` | `Current` | Machine-readable surface authority map exists. |
| `rendered_surface_registry` | `Current` | Rendered planning surfaces are registry-backed and authoritative in configuration. |
| `workflow_metadata_registry` | `Current` | Workflow trigger and risk metadata already exist as machine authority. |

### Current Live Planning And Guidance Boundary

| Surface Family | Current Status | Notes |
|---|---|---|
| Current root docs corpus | `Current but mislocated` | The repo already has durable core-oriented guidance, but the future boundary should move core-only docs under `core/docs/`. |
| `plan/docs/` guidance layer | `Missing` | There is no distinct plan-domain guidance layer yet. |
| `docs/planning/` live planning families | `Current but misaligned` | The repo currently stores live planning here, but this conflicts with the intended split between live initiative state, plan-domain guidance, and core-development docs. |
| `plan/` live initiative roots | `Missing` | There is no first-class live `plan` workspace yet for either pack-wide initiatives or project-scoped initiatives. |
| `plan/.wt/` aggregate tracking root | `Missing` | There is no first-class pack-level aggregate root for initiative and task status rollups yet. |
| `core/workflows/` workflow root | `Missing` | There is no first-class core-only workflow root yet. |
| `plan/workflows/` workflow root | `Missing` | There is no first-class plan-domain workflow root yet. |
| Human-surface placement policy | `Missing` | There is no explicit machine-readable rule set for where `README.md` and `AGENTS.md` should exist. |
| `plan/projects/` project root | `Missing` | There is no first-class per-project area yet, including a home for project-scoped initiatives. |

### Current Schema Families

| Family | Current Status | Notes |
|---|---|---|
| Artifact schemas under `core/control_plane/schemas/artifacts/` | `Current` | Acceptance contracts, indexes, registries, evidence, migration, release, and purge records are schema-backed. |
| Documentation front-matter base schema | `Current but likely incomplete for the endstate` | Shared front-matter vocabulary already exists at `core/control_plane/schemas/interfaces/documentation/front_matter_base.schema.json`, but the final field set may still need removals, additions, and stronger constraints. |
| Documentation front-matter family schemas | `Current but likely incomplete for the endstate` | Governed markdown front matter is validated through dedicated family schemas today, but those family profiles should be treated as the current baseline rather than the final contract. |
| Documentation family binding registry | `Missing` | The machine-readable mapping from documentation family to schema, template, section spec, and allowed roots is still implicit rather than governed. |
| Pack-facing interface schemas | `Partial` | Good start, but still incomplete for full pack runtime and still contain some legacy field naming. |

### Documentation Front-Matter And Template Machine Contract

On the machine-facing side, front matter and template rules should not live only in prose standards. They should be captured through typed schemas and registries.

Required machine contract shape:

- one base schema that defines the shared front-matter vocabulary for governed documentation families
- one family subschema for each governed documentation family that composes the base schema, fixes the `type`, and declares the family's required fields
- one documentation-family registry that states which schema, template, section spec, roots, and indexes apply to each documentation family
- one template-catalog entry for each authored or rendered documentation family surface
- optional section-spec schemas when a family needs machine-validated heading or section structure

Current baseline:

- the current base front-matter schema is `core/control_plane/schemas/interfaces/documentation/front_matter_base.schema.json`
- the current family subschemas live under `core/control_plane/schemas/interfaces/documentation/`
- the current base and family schemas should be treated as a starting point, not as proof that the final field model is complete

Current shared base vocabulary:

- `trace_id`
- `id`
- `title`
- `summary`
- `type`
- `status`
- `tags`
- `owner`
- `updated_at`
- `audience`
- `authority`
- `applies_to`
- `aliases`

Future rule:

- the base schema defines the shared allowed field vocabulary
- family subschemas define what is required for that family
- the documentation-family registry binds a family to its front-matter schema, section rules, and template ids
- template and section rules do not replace schema requirements; they layer on top of the family schema

Current family-specific must-have fields in the baseline model:

| Family | Current Required Fields |
|---|---|
| `foundation` | `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `standard` | `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `reference` | `id`, `title`, `summary`, `type`, `status`, `tags`, `owner`, `updated_at`, `audience` |
| `workflow` | `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience` |
| `prd` | `trace_id`, `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `decision_record` | `trace_id`, `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `feature_design` | `trace_id`, `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `implementation_plan` | `trace_id`, `id`, `title`, `summary`, `type`, `status`, `owner`, `updated_at`, `audience`, `authority` |
| `task` | `id`, `title`, `summary`, `type`, `status`, `task_status`, `task_kind`, `priority`, `owner`, `updated_at`, `audience`, `authority` |

Future machine-facing placement rule:

- core-owned reusable documentation contracts live under `core/control_plane/schemas/interfaces/documentation/`
- core-owned documentation-family bindings live under `core/control_plane/registries/documentation_family_registry.json`
- core-owned template metadata lives under `core/control_plane/registries/template_catalog.json`
- pack-owned documentation contracts live under `plan/.wt/schemas/interfaces/documentation/`
- pack-owned documentation-family bindings live under `plan/.wt/registries/documentation_family_registry.json`
- pack-owned template metadata lives under `plan/.wt/registries/template_catalog.json`

Required fields for a future `documentation_family_registry` entry:

- `family_id`
- `front_matter_base_schema_id`
- `front_matter_schema_id`
- `template_ids`
- `section_spec_schema_id` when applicable
- `allowed_roots`
- `authorship_mode` such as `authored` or `rendered`
- `required_index_ids`
- `required_rendered_surface_ids` when applicable
- `mirror_group_id` when the family must exist in more than one required location
- `required_mirror_roots` when mirrored copies are mandatory
- `equivalence_mode` such as `byte_identical` or `content_equivalent`
- `mirror_update_mode` such as `same_change_set`, `generated_copy`, or `promotion_fan_out`

### Future Front-Matter Family Obligations

The current family schemas are only a baseline. The implementation plan should treat the following family obligations as the target semantic contract even if exact field names or nesting change.

Rules that remove ambiguity:

- authored durable documentation families under `core/docs/` and `plan/docs/` must have governed front matter
- rendered views such as `plan_overview.md`, initiative `plan.md`, initiative `progress.md`, initiative `summary.md`, `project.md`, `repositories.md`, and project `summary.md` should not become primary front-matter-authoritative families unless the implementation plan makes that choice explicitly
- if a rendered view includes front matter or header metadata, it should be treated as derived display metadata rather than the primary source of truth
- temporary live-work markdown families such as PRDs, feature designs, implementation plans, and tasks may exist during the migration or active-work period, but they are operational families rather than long-term knowledge families

Minimum future family obligations for authored documentation families:

| Family | Minimum Semantic Obligations That Must Exist |
|---|---|
| `foundation` | stable `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, plus a scope boundary and a statement that the family is durable guidance |
| `standard` | stable `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, plus normative applicability and rule-bearing intent |
| `reference` | stable `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, tags or classification metadata, and enough provenance metadata to distinguish curated reference from other guidance |
| `decision_record` | stable `id`, `trace_id` when promoted from initiative work, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, and explicit decision-state semantics such as active, superseded, or replaced |
| `pattern` | stable `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, and pattern applicability or usage-boundary metadata |
| `workflow` | stable `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, and a machine-bindable relationship to workflow metadata or route usage where applicable |
| `transitional_prd` | if retained during active work, require `trace_id`, `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, and initiative linkage so the family can be deleted safely after promotion |
| `transitional_feature_design` | if retained during active work, require `trace_id`, `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, and initiative linkage |
| `transitional_implementation_plan` | if retained during active work, require `trace_id`, `id`, `title`, `summary`, `status`, `owner`, `updated_at`, `audience`, `authority`, and initiative linkage |
| `transitional_task` | if retained as an authored markdown family during migration, require `id`, `title`, `summary`, `status`, `task_status`, `task_kind`, `priority`, `owner`, `updated_at`, `audience`, `authority`, and initiative linkage |

Future rule for mirrored authored families:

- if a documentation family is required to exist in both `core/docs/` and `plan/docs/`, the family should be modeled as one logical family with two required roots
- the machine contract must say whether those copies are human-coauthored in one change set or whether one copy is generated from the other
- no implementation should silently prefer one copy after commit if the family is declared content-equivalent across both roots

### Template Machine Contract

Templates need the same level of machine authority as front matter because different families need different sections, section order, and authoring hints.

Required template contract shape:

- one template catalog entry for each template-backed family surface
- one section-spec schema when a family needs machine-enforced section structure
- one documentation-family binding back to the relevant template ids
- one explicit place for LLM-facing authoring notes so family-specific guidance is machine-discoverable rather than hidden in prose only

Future rule:

- template files provide the text scaffold
- template catalog entries provide the machine-readable contract for what that template means
- section-spec schemas provide machine validation for required headings, section ids, section order, and section-local constraints
- LLM-facing notes are governed metadata, not ad hoc comments sprinkled through the repo

Recommended machine-facing placement rule for templates:

- core-owned reusable template metadata lives under `core/control_plane/registries/template_catalog.json`
- core-owned reusable template files should live under `core/control_plane/templates/`
- pack-owned template metadata lives under `plan/.wt/registries/template_catalog.json`
- pack-owned template files live under `plan/.wt/templates/`
- shared section-spec schemas should live under `core/control_plane/schemas/interfaces/documentation/` or `plan/.wt/schemas/interfaces/documentation/`, depending on ownership

Required fields for a future `template_catalog` entry:

- `template_id`
- `family_id` or `surface_id`
- `authorship_mode` such as `authored` or `rendered`
- `template_path`
- `front_matter_schema_id` when the template is for authored markdown with governed front matter
- `required_section_ids`
- `optional_section_ids`
- `section_order`
- `prohibited_section_ids` when a family must explicitly omit sections
- `section_cardinality_rules` when repeating or mutually exclusive sections are allowed
- `section_spec_schema_id` when applicable
- `llm_guidance` or equivalent structured authoring notes for agent or LLM use
- `llm_guidance_mode` such as `required`, `advisory`, or `none`
- `operator_notes` when human-specific instructions differ from LLM-facing guidance
- `required_rendered_surface_ids` when the template drives a rendered view
- `allowed_roots`

Examples of template-level machine requirements that should be captured here rather than left implicit:

- a PRD template requires goal, scope, acceptance, and out-of-scope sections
- a workflow template requires purpose, use-when, inputs, workflow, outputs, and done-when sections
- a project summary template requires project identity, linked repositories, current state, and delivery summary sections
- an initiative plan template may carry extra LLM guidance about how to phrase execution slices or how to avoid mixing live state with durable guidance

### Minimum Required Template Families And Sections

The implementation plan can still decide exact headings, section ids, and ordering details, but the following section concepts should be treated as required unless an explicit owner-approved decision removes one.

| Surface Or Family | Authorship Mode | Minimum Required Sections Or Section Concepts |
|---|---|---|
| `plan/plan_overview.md` | `rendered` | plan-domain summary, active pack-wide initiatives, active project initiatives, blocked or attention-needed items, recent completions or changes, navigation links into projects, docs, and workflows |
| Initiative `plan.md` | `rendered` | initiative identity, scope and non-goals, objectives, planned slices or workstreams, dependencies and risks, validation or completion gates, linked project or pack outputs |
| Initiative `progress.md` | `rendered` | current status, recent events or changes, active tasks, blockers, next actions, evidence or validation state |
| Initiative `summary.md` | `rendered` | outcome summary, delivered outputs, promoted guidance, evidence references, unresolved follow-ups, closeout state |
| Project `project.md` | `rendered` | project identity, purpose and scope, current state, linked initiatives, linked repositories, key references or docs |
| Project `repositories.md` | `rendered` | repository role summary, repository locations, ownership or access notes when needed, implementation-vs-planning distinction, active flags when needed |
| Project `summary.md` | `rendered` | project delivery summary, current health, open risks, next milestones or follow-ups, promotion or guidance impacts |
| `foundation` | `authored` | purpose or context, scope boundary, principles or guiding rules, implications for repo or project behavior |
| `standard` | `authored` | purpose, applicability, required or prohibited rules, enforcement or validation implications |
| `reference` | `authored` | subject summary, usage guidance, provenance or source notes when relevant, related surfaces |
| `decision_record` | `authored` | context, decision, consequences, current status or supersession notes |
| `pattern` | `authored` | scenario, recommended structure, boundaries or constraints, illustrative example or usage notes |
| Workflow module | `authored` | purpose, use-when, inputs, workflow, outputs, done-when |
| `README.md` at governed human roots | `authored` | root purpose, contents or subtrees, navigation hints, related machine surfaces where helpful |
| `AGENTS.md` at governed human roots | `authored` | scope, local instructions, routing or behavior differences, exclusions or constraints that materially change agent interaction |

Future rule:

- a template family is incomplete if it defines only a file path and no minimum section contract
- if a template is rendered, the template contract must identify which machine surfaces or indexes provide its source inputs
- if a template contains LLM-facing guidance, that guidance should be structured enough to distinguish hard requirements from advisory phrasing
- section requirements that matter for validation should live in `template_catalog` and section-spec schemas, not only in prose standards

### Current Baseline References For High-Impact Families

This requirements document should anchor the most important current baselines, but it should not become the full migration matrix. The implementation plan should carry the exhaustive current-to-future mapping.

High-impact current references that matter now:

- `core/control_plane/schemas/interfaces/documentation/front_matter_base.schema.json`
- `core/control_plane/schemas/interfaces/documentation/foundation_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/standard_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/reference_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/workflow_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/prd_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/decision_record_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/feature_design_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/implementation_plan_front_matter.schema.json`
- `core/control_plane/schemas/interfaces/documentation/task_front_matter.schema.json`
- `core/control_plane/registries/schema_catalog.json`
- `core/control_plane/registries/validator_registry.json`
- `core/control_plane/registries/validation_suite_registry.json`
- `core/control_plane/registries/rendered_surface_registry.json`
- `core/control_plane/registries/workflow_metadata_registry.json`
- `core/control_plane/registries/status_registry.json`
- `core/control_plane/schemas/interfaces/packs/pack_settings.schema.json`
- `core/control_plane/schemas/interfaces/packs/artifact_index.schema.json`
- `core/python/src/watchtower_core/control_plane/pack_context.py`
- `core/python/src/watchtower_core/repo_ops/`

Rule for this document:

- cite exact current references when the future requirement directly keeps, replaces, constrains, or disputes a current authoritative surface
- avoid turning the requirements document into a path-by-path migration ledger
- defer the exhaustive migration table to the implementation plan

### Minimum Semantic Fields For High-Value New Families

The implementation plan can still decide exact JSON shapes and nesting, but the following semantic fields should be treated as required unless an explicit owner-approved reason removes them.

| Family | Minimum Semantic Fields Or Concepts That Must Exist |
|---|---|
| `initiative_state` | `initiative_id`, `slug`, `title`, `summary`, `scope_type`, `project_id` when project-scoped, `status`, `lifecycle_stage`, `owner`, `updated_at`, `task_ids`, `evidence_ids`, `promotion_ids` |
| `task_state` | `task_id`, `slug`, `initiative_id`, `status`, `task_kind`, `priority`, `owner`, `updated_at`, dependency references, related ids |
| `initiative_event_stream` | stable event id or sequence, initiative id, timestamp, actor, event type, payload, deterministic ordering semantics |
| `task_event_stream` | stable event id or sequence, task id, initiative id, timestamp, actor, event type, payload, deterministic ordering semantics |
| `project_record` | `project_id`, `slug`, `title`, `summary`, `status`, linked repository refs, project-local initiative root, updated timestamp |
| `project_repository_map` | repository role, repository locator, ownership or access metadata as needed, implementation-vs-planning distinction, active flag when needed |
| `guidance_promotion_record` | source initiative id, source artifact refs, target guidance family, target path, approval state, approver or review refs, evidence refs, mirror update obligations when applicable |
| `initiative_index` | initiative id, slug, scope type, project id when present, status, lifecycle stage, owner, primary path, updated timestamp |
| `task_index` | task id, initiative id, project id when present, task status, task kind, priority, owner, primary path, updated timestamp |
| `status_rollup` | bucket definitions, counts, stale or blocked indicators, source generation timestamp, source index version or generation id |

Future rule:

- these semantic fields are requirements-level obligations even if the exact JSON property names change during implementation
- omitting one of these concepts should require an explicit decision in the implementation plan rather than happening by accident

### Current Derived Surface Families

| Surface Family | Current Status | Notes |
|---|---|---|
| Planning, coordination, initiative, task, PRD, decision, design, reference, standard, workflow, route, command, repository-path, and traceability indexes | `Current` | The repo already produces a dense machine-readable lookup layer. |
| Rendered planning trackers | `Current` | Generated from registry-backed rendered-surface definitions, but still mostly sourced from docs-backed planning families. |
| Generic pack-wide `artifact_index` | `Partial` | Interface schema exists, but the repo does not yet run a full generic builder over plan-domain artifacts. |

### Current Runtime Boundaries

| Package Area | Current Status | Notes |
|---|---|---|
| `watchtower_core.control_plane` | `Current` | Strong reusable-core area with typed models, loader, workspace, and schema-store logic. |
| `watchtower_core.validation` | `Current` | Strong reusable-core area with pack-aware validation suites and pack contract validation. |
| `watchtower_core.evidence` | `Partial` | Strong for validation evidence, but still narrow as a generic evidence layer. |
| `watchtower_core.query` | `Partial` | Guardrail root only; real query services still lean on `repo_ops`. |
| `watchtower_core.sync` | `Partial` | Guardrail root only; real sync services still lean on `repo_ops`. |
| `watchtower_core.closeout` | `Partial` | Useful for initiative closeout and purge, but not yet a generic pack closeout service set. |
| `watchtower_core.repo_ops` | `Current but intentionally transitional` | It should shrink toward zero; any remaining `repo_ops` surface in the clean endstate requires explicit approval plus companion documentation and machine-readable justification. |

## Required Endstate Surfaces

The future endstate for this repository is not "make everything generic." The endstate is:

1. the steady-state project structure is centered on `core/` and `plan/`, with core-only content under `core/` and non-core operational content under `plan/`
2. reusable core owns truly cross-pack runtime, validation, workflow, and governance services
3. pack-wide live planning state lives under `plan/initiatives/<initiative_slug>/`, while project-scoped live planning state lives under `plan/projects/<project_slug>/initiatives/<initiative_slug>/`
4. each initiative owns a local `.wt/` machine layer with current-state snapshots, event history, task state, evidence, and promotion records
5. each initiative exposes rendered human visibility files such as `plan.md`, `progress.md`, and `summary.md`, built from the initiative-local machine layer
6. `plan/.wt/` provides aggregate tracking, initiative and task rollups, and machine-readable status lookup so operators and agents do not need to crawl every initiative folder
7. `plan/plan_overview.md` becomes the primary human pack-level overview, with a short description of the plan domain and a sectioned status board over ongoing work
8. `core/docs/` and `plan/docs/` become the long-term documentation roots for their respective domains, with duplicated `docs/foundations/` corpora kept aligned across both
9. `plan/projects/<project_slug>/` becomes the home for project-specific context, supporting documentation, references, linked repository information, and project-scoped initiatives
10. `core/workflows/` and `plan/workflows/` become the homes for human-authored workflow guidance instead of a mixed repo-root workflow tree
11. `README.md` and `AGENTS.md` exist only at declared human-facing roots where they improve navigation or materially change agent behavior; they do not belong inside machine-only `.wt/` trees
12. `pack_context` loads on every standard operation, while `project_context` loads separately when the path, command, or workflow is project-scoped
13. the workflow remains human plus LLM or agent initiated, with Python helpers and harnesses providing deterministic loading, validation, query, sync, and rendered-view support
14. `WatchTowerPlan` remains the planning authority and shared-core proving area, while `/home/j/WatchTower` remains the permanent downstream product implementation repository

### Fully Implemented Clean Endstate

Once the intended operating model is fully implemented and the current transition period is over, the following should be true:

- the meaningful repository structure is `core/` and `plan/`, with no broad repo-root operational trees still carrying first-class project content
- there are no long-lived transition, compatibility, migration, or historical artifact families retained as part of the normal operating model
- important durable guidance has been normalized into foundations, standards, references, and other long-term guidance surfaces rather than being left in temporary planning artifacts
- completed or superseded tasks, PRDs, initiatives, implementation slices, and similar temporary planning records have been removed after their durable outputs are extracted
- there is a clean core split, and `repo_ops` is effectively absent unless explicitly approved by the repository owner with companion documentation and machine-readable justification
- the foundations corpus continues to guide WatchTower, but it lives as intentionally duplicated `core/docs/foundations/` and `plan/docs/foundations/` rather than as project-scoped material
- `pack_context` is always loaded, and `project_context` is loaded separately only when needed
- human and agent workflows still initiate the work, while Python helpers and harnesses remain the deterministic operational layer underneath

### Implementation-Ready Clarifications

#### Scope Classification Rules

- a pack-wide initiative is any initiative whose purpose is core work, plan-pack work, cross-project work, or work not cleanly owned by exactly one project
- a project-scoped initiative is any initiative whose work product, references, and operational ownership belong to exactly one project container
- tasks do not float at pack root or project root; they belong to one initiative
- project-local docs and references may exist without an initiative, but live execution work should still be routed through initiatives

#### Context Load Rules

- every standard helper or harness begins with `pack_context`
- `project_context` loads only when the current path, command arguments, or workflow metadata resolve to exactly one project
- project-scoped initiative work should load both `pack_context` and `project_context`
- pack-wide initiative work should not load `project_context` unless a specific operation also targets one project as an output or reference
- initiative and task context should be derived from the initiative or task path and underlying machine state rather than treated as independent startup roots

#### Promotion And Deletion Gates

- live planning artifacts are temporary operational state, not permanent knowledge artifacts
- before a completed initiative, task family, PRD, design, or implementation slice is removed, any durable guidance needed long term must be promoted into foundations, standards, references, decisions, patterns, or project-facing durable outputs
- before removal, any machine-readable obligations that remain relevant must already be represented in surviving indexes, project records, or guidance-promotion records
- rendered summaries are not enough by themselves to justify keeping temporary planning state
- deletion is allowed only after validation passes on the surviving surfaces that replace the deleted material
- if a surface is not promoted, referenced by an active project, or required by an explicit owner-approved exception, it should not survive into the clean endstate

#### Reserved Approval Areas

The following remain explicitly owner-gated and should never appear by default:

- any residual `repo_ops` behavior in the clean endstate
- any compatibility-contract or compatibility-ledger surface in the clean endstate
- any long-lived migration, release, historical, or archive family kept as normal operational state
- any new repo-root operational tree beyond thin routing entrypoints
- any divergence between duplicated foundations copies

### Required Endstate Startup And Governance Surfaces

| Surface | Current Coverage | Future Requirement |
|---|---|---|
| `pack_settings` | `Current` | Remain the load root and grow only through declared surfaces, versioned schema, and stable typed loading. |
| `schema_catalog` | `Current` | Continue to support core-owned plus pack-owned schema catalogs without copy-pasting schemas into core. |
| `validator_registry` | `Current` | Continue pack-aware validator selection and expand only when new step kinds or engines are truly needed. |
| `validation_suite_registry` | `Current` | Become the standard way to declare validation baselines for both internal and future external packs. |
| `artifact_family_registry` | `Current` | Add authoritative family taxonomy for pack artifacts, placement rules, allowed status subsets, renderability, and derived-index participation. |
| `relation_type_registry` | `Current` | Add controlled cross-artifact relation names before artifact graphs grow more complex. |
| `review_status_registry` | `Current` | Add controlled review state vocabulary instead of reusing loose string fields across artifacts. |
| `source_type_registry` | `Current` | Add a generic source/provenance vocabulary for references, external imports, generated outputs, and derived artifacts. |
| `lifecycle_stage_registry` | `Current` | Distinguish status from lifecycle stage for pack work items and evidence. |
| `status_transition_rules` | `Current` | Move family-specific allowed status transitions out of code and prose into machine-readable policy. |
| `promotion_policy_registry` | `Current` | Define what kinds of initiative-local outputs may be promoted into `plan/docs/` guidance surfaces and what review is required. |
| `project_surface_policy_registry` | `Current` | Define what kinds of project-specific artifacts, linked repository metadata, and initiative-derived outputs may live under `plan/projects/` and what metadata they must carry. |
| `documentation_family_registry` | `Current` | Bind each governed documentation family to its front-matter base schema, family subschema, template ids, section-spec schema, and allowed roots. |
| `template_catalog` | `Current` | Govern template ids, required and optional sections, section order, section-spec schemas, and any LLM-facing authoring guidance for initiative-local rendered views, project surfaces, and extracted guidance surfaces. |
| `human_surface_policy_registry` | `Current` | Define where `README.md`, `AGENTS.md`, authored workflow docs, and rendered visibility files are required, optional, or forbidden, and whether each human-facing surface is authored or rendered. |
| `retention_policy_registry` | `Current but transitional` | The live registry now governs migration-era retention and cleanup posture while the clean-endstate purge model is still being reconciled. |
| `compatibility_contract_registry` | `Not part of the clean endstate` | Do not add unless explicitly approved for a concrete external-consumer need. |

### Required Endstate Pack-Facing Artifact And Interface Contracts

| Interface Or Artifact Contract | Current Coverage | Future Requirement |
|---|---|---|
| `pack_work_item_note` | `Current` | Keep as a generic operator-authored note contract for plan-pack work items. |
| `artifact_index` | `Partial` | Make it truly domain-neutral for planning packs and back it with a real builder plus family registry. |
| `initiative_state` | `Missing` | Add an authoritative current-state snapshot contract for one initiative under either a pack-wide or project-scoped initiative root. |
| `initiative_event_stream` | `Current` | Keep an initiative-level append-only event contract so live planning can be event-backed instead of doc-backed. |
| `task_state` | `Missing` | Add a current-state snapshot contract for initiative-local tasks. |
| `task_event_stream` | `Current` | Keep a task-level append-only event contract where task churn needs separate event history. |
| `guidance_promotion_record` | `Current` | Add a governed record for extracting approved decisions, standards, references, and guidance from live initiatives into `plan/docs/` guidance surfaces. |
| `project_record` | `Missing` | Add a governed current-state contract for one project container under `plan/projects/<project_slug>/.wt/project.json`. |
| `project_repository_map` | `Missing` | Add a governed contract for linking a project to one or more repositories such as planning, implementation, or deployment repos. |
| `extraction_output_envelope` | `Partial` | Keep as an optional reusable output envelope, but align it with explicit promotion and extraction flows rather than ad hoc exports. |
| `validation_bundle` | `Missing` | Add a broader evidence or validation bundle contract if suites, reviews, and closeout start sharing evidence packages. |
| `discrepancy_record` | `Current` | Keep the governed discrepancy record authoritative for initiative-local validation drift, sync drift, and accepted exception tracking. |
| `environment_context` | `Missing` | Add if route safety and execution mode decisions need durable environment records. |
| `closeout_recap` | `Missing` | Add if future plan-pack closeout needs a stronger machine companion to initiative `summary.md` beyond current initiative closeout surfaces. |
| `review_record` | `Future` | Add if human approval, review state, and promotion decisions need stronger machine authority. |

### Required Endstate Runtime And Harness Boundaries

| Runtime Surface | Current Coverage | Future Requirement |
|---|---|---|
| `watchtower_core.control_plane` | `Current` | Keep as the reusable source of pack loading, typed models, schema store, and workspace mapping. |
| `watchtower_core.validation` | `Current` | Continue expanding here for generic validation only, not for repo-local document semantics. |
| `watchtower_core.query` | `Partial` | Grow from guardrail root into a reusable query boundary for declared surfaces, routes, registries, and pack indexes. |
| `watchtower_core.sync` | `Partial` | Grow into a reusable sync boundary for authority-preserving updates. |
| `watchtower_core.rebuild` | `Missing` | Add when derived indexes and rendered views need an export-safe rebuild harness distinct from sync. |
| `watchtower_core.routing` or equivalent exported route services | `Partial` | Expose route preview and selection as reusable runtime services rather than only CLI wiring and repo-local handlers. |
| `watchtower_core.workflow_execution` | `Missing` | Add only after route selection and workflow metadata are stable enough to support a generic execution contract. |
| `watchtower_core.evidence` | `Partial` | Broaden only when there is a concrete non-validation evidence need shared across packs. |
| `watchtower_core.closeout` | `Partial` | Broaden from initiative closeout into pack-level closeout coordination only if the same semantics truly apply across packs. |

### Required Endstate Derived Surfaces

| Derived Surface | Current Coverage | Future Requirement |
|---|---|---|
| Initiative-local `plan.md` | `Missing` | Render the current plan shape for one initiative from local `.wt/` state rather than authoring it as the primary machine authority. |
| Initiative-local `progress.md` | `Missing` | Render live progress and recent status for one initiative from local `.wt/` state. |
| Initiative-local `summary.md` | `Missing` | Render current summary or closeout recap for one initiative from local `.wt/` state. |
| Pack-level initiative and task indexes under `plan/.wt/` | `Missing` | Provide aggregate lookup and status rollups across both pack-wide and project-scoped initiatives without crawling every initiative path. |
| Pack-level `plan_overview.md` under `plan/` | `Missing` | Render a short description of the plan domain plus a sectioned status board over ongoing initiatives and projects. |
| Plan-domain workflow docs under `plan/workflows/` | `Missing` | Hold human-authored routing references, workflow modules, and operator procedures for the plan domain, backed by workflow metadata and route indexes. |
| Project-level views under `plan/projects/` | `Missing` | Provide project-local human-facing summaries, supporting docs, references, linked repository information, and implementation-boundary context. |
| Guidance and promotion indexes | `Missing` | Provide aggregate lookup over approved extracted guidance and promotion history under `plan/.wt/` and `plan/docs/`. |
| Human navigation and instruction surfaces | `Missing` | Govern and expose `README.md` and `AGENTS.md` only where they help navigation or materially change agent interaction. |
| Planning and coordination indexes | `Current` | Current family-specific indexes should eventually re-root to initiative-backed live state or be retired where they only mirror docs-backed planning families. |
| Route and workflow indexes | `Current` | Keep as derived views from routing guidance and workflow metadata; later expose more reusable query helpers over them. |
| Rendered planning trackers | `Current` | Current trackers should either become pack-level rendered live views under `plan/` or be retired once they no longer belong in docs. |
| Pack-wide `artifact_index` | `Partial` | Introduce as the cross-family query authority for future plan-pack artifacts when the family model is mature enough. |
| Evidence, discrepancy, review, closeout, and promotion indexes | `Missing` | Add only when the underlying artifact families become real. |

### Required Human-Surface Obligations By Root

The directory tree later in this document shows the future shape. The table below states the minimum behavioral contract for the most important human-facing roots so implementation does not have to infer intent from the tree alone.

| Root Or Surface Area | Required Human Surfaces | Expected Authorship Mode | Governing Machine Surfaces | Clarifying Rule |
|---|---|---|---|---|
| Repository root | root `README.md`, root `AGENTS.md` only if still needed as thin router surfaces | `authored` | `human_surface_policy_registry` | root should stay thin and must not act as a third operational workspace |
| `core/` | `README.md` | `authored` | `human_surface_policy_registry` | explain core-only scope and point to `core/docs/`, `core/workflows/`, `core/python/`, and `core/control_plane/` |
| `core/docs/` | `README.md` and optional `AGENTS.md` only if authoring behavior changes materially | `authored` | `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry` | holds durable core-only guidance, not live plan work |
| `core/workflows/` | `README.md`, `AGENTS.md`, `ROUTING_TABLE.md`, workflow modules | `authored` | `workflow_metadata_registry`, `human_surface_policy_registry`, `template_catalog` when templated | core-only workflow guidance should live here rather than at repo root |
| `plan/` | `README.md`, `AGENTS.md`, `plan_overview.md` | `README.md` and `AGENTS.md` are `authored`; `plan_overview.md` is `rendered` | `human_surface_policy_registry`, `rendered_surface_registry`, `template_catalog`, aggregate indexes under `plan/.wt/` | `plan_overview.md` is the pack-level human status board and is not a primary authority surface |
| `plan/docs/` | `README.md`, optional `AGENTS.md`, authored guidance families | `authored` | `documentation_family_registry`, `template_catalog`, `promotion_policy_registry`, `human_surface_policy_registry` | approved durable plan guidance lives here; live initiative state does not |
| `plan/workflows/` | `README.md`, `AGENTS.md`, `ROUTING_TABLE.md`, workflow modules | `authored` | `workflow_metadata_registry`, `human_surface_policy_registry`, `template_catalog` when templated | plan-domain workflow guidance lives here rather than at repo root |
| `plan/initiatives/` | `README.md`, optional `AGENTS.md` | `authored` | `human_surface_policy_registry` | root is for navigation only; state lives in initiative containers |
| `plan/initiatives/<initiative_slug>/` | `plan.md`, `progress.md`, `summary.md` | `rendered` | initiative state and task state families, `rendered_surface_registry`, `template_catalog` | initiative-local rendered views must be rebuildable from local `.wt/` state |
| `plan/projects/` | `README.md`, optional `AGENTS.md` | `authored` | `human_surface_policy_registry` | root is for project navigation and discovery |
| `plan/projects/<project_slug>/` | `project.md`, `repositories.md`, `summary.md`, optional project-local `docs/` and `references/` authored surfaces | project top-level summaries are `rendered`; project-local docs and references are `authored` | `project_record`, `project_repository_map`, `rendered_surface_registry`, `documentation_family_registry`, `template_catalog`, `project_surface_policy_registry` | project-scoped initiatives belong below this root |
| Any `.wt/` machine root | no required `README.md` or `AGENTS.md` | `machine_only` | all applicable schemas, registries, and policies | machine-only roots should be discoverable through helpers and indexes rather than local instruction files |

Future rule:

- human-surface obligations should be enforced through `human_surface_policy_registry`, not by relying only on folder conventions
- a root is incomplete if it has a declared human surface requirement but no matching template, rendered-surface entry, or authored-family binding
- machine-only roots should fail validation if stray `README.md` or `AGENTS.md` files appear where policy forbids them

### Companion Surface Rule

No newly proposed family or surface in this document should be considered complete if it is defined only by a path or a single schema name. Every new addition should declare its companion support set explicitly.

Minimum companion set for any new addition:

- one authoritative schema for each machine-readable artifact, registry, policy, or index
- one `validator_registry` entry for each schema-backed artifact family or registry
- one `validation_suite_registry` inclusion path so the family participates in at least one baseline or targeted suite
- one `artifact_family_registry` entry when the addition is a first-class artifact family
- one `documentation_family_registry` entry when the addition is a governed documentation family or template-backed documentation surface
- one `path_pattern_registry` entry for placement and path validation
- applicable `status_registry`, `lifecycle_stage_registry`, `review_status_registry`, `source_type_registry`, and policy bindings where the family carries lifecycle or provenance semantics
- one `workflow_metadata_registry` entry when the addition introduces routed workflow or route-preview behavior
- one `human_surface_policy_registry` entry when the addition introduces or changes expectations for `README.md`, `AGENTS.md`, workflow docs, or rendered visibility files
- one mirror binding or equivalent required-root rule when the family must exist in synchronized copies such as duplicated foundations
- explicit derived-index participation such as `initiative_index`, `task_index`, `project_index`, `promotion_index`, `guidance_index`, `status_rollup`, or `artifact_index`
- one `rendered_surface_registry` entry for every rendered human-facing view
- one `template_catalog` entry plus concrete template or section-spec files for every authored or rendered human-facing surface
- fixture examples and fail-closed negative cases for loaders, validators, and runtime tests

### Companion Support Matrix

| Addition Group | Required Schemas | Required Registries And Policies | Required Indexes | Required Rendered Or Template Surfaces | Required Validation And Test Coverage |
|---|---|---|---|---|---|
| Initiative live-state stack | `initiative_state.schema.json`, `initiative_event_stream.schema.json`, `task_state.schema.json`, `task_event_stream.schema.json` | `artifact_family_registry`, `path_pattern_registry`, `status_registry`, `lifecycle_stage_registry`, `status_transition_rules`, `relation_type_registry`, `source_type_registry` | `initiative_index`, `task_index`, `status_rollup`, `artifact_index` | `rendered_surface_registry` entries for `plan.md`, `progress.md`, `summary.md`; `template_catalog` entries and template files for those surfaces; path coverage for both pack-wide and project-scoped initiative roots | `validator_registry` entries for initiative and task families; `validation_suite_registry` coverage for live-state and rendered-view validation; fixture initiatives with pass/fail event and snapshot examples under both root types |
| Initiative evidence and closeout stack | `validation_bundle.schema.json`, `closeout_recap.schema.json`, `discrepancy_record.schema.json`, `environment_context.schema.json` | `artifact_family_registry`, `path_pattern_registry`, `review_status_registry`, `source_type_registry`, `retention_policy_registry`, `status_transition_rules` | `evidence_index`, `discrepancy_index`, `artifact_index`, optional `closeout_index` when needed | `rendered_surface_registry` entries for closeout-oriented summary surfaces; `template_catalog` entries for recap layouts when human-facing views are rendered | Validator entries for each family; suite coverage for evidence, discrepancy, and closeout baselines; fixture bundles and discrepancy cases |
| Guidance extraction and promotion stack | `guidance_promotion_record.schema.json`, extracted-doc front-matter schemas as needed, optional `guidance_index.schema.json`, `promotion_index.schema.json` | `promotion_policy_registry`, `artifact_family_registry`, `review_status_registry`, `source_type_registry`, `relation_type_registry`, `template_catalog` | `promotion_index`, `guidance_index`, `artifact_index` | `template_catalog` entries and templates for `plan/docs/standards`, `references`, `decisions`, and `patterns`; rendered or authored section specs for extracted guidance surfaces | Validator entries for promotion records and extracted-doc machine companions; suite coverage for promotion-policy enforcement; fixtures showing initiative-to-guidance promotion |
| Authored documentation stack | front-matter base schema, one family subschema per governed documentation family, section-spec schemas where needed, `documentation_family_registry.schema.json`, `template_catalog.schema.json` | `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry`, `path_pattern_registry`, `promotion_policy_registry` when the family can be promoted from live work | `guidance_index`, `artifact_index`, and workflow or project indexes when those families participate there | concrete templates for foundations, standards, references, decisions, patterns, workflow modules, and any transitional live-work docs that remain during migration | validator entries for every family subschema and registry; suite coverage for required fields, allowed roots, section rules, authored-versus-rendered mode, and fail-closed handling of missing templates or wrong family bindings |
| Duplicated foundations stack | front-matter schemas for foundations, section-spec schemas where needed, optional mirror-validation schema or equivalent rule-bearing fields | `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry`, and mirror-root rules carried by the documentation-family bindings | `guidance_index` and any foundation lookup indexes that survive in the endstate | synchronized copies under `core/docs/foundations/` and `plan/docs/foundations/` with no divergent authored content | Validator entries and suite coverage proving the duplicated copies stay equivalent and same-change-set updates keep them aligned |
| Project workspace stack | `project_record.schema.json`, `project_repository_map.schema.json`, optional `project_index.schema.json` | `project_surface_policy_registry`, `artifact_family_registry`, `path_pattern_registry`, `source_type_registry`, `relation_type_registry`, `review_status_registry` when approval is needed | `project_index`, `artifact_index`, optional `guidance_index` participation for project-local references | `rendered_surface_registry` entries plus `template_catalog` entries for `project.md`, `repositories.md`, `summary.md`, project-local `docs/` or `references/` surfaces, and project-local `initiatives/` roots | Validator entries for project record and repo-map artifacts; suite coverage for project container validation; fixtures with multiple linked repository scenarios |
| Pack-level aggregate tracking stack | `initiative_index.schema.json`, `task_index.schema.json`, `status_rollup.schema.json`, `project_index.schema.json`, `promotion_index.schema.json`, `guidance_index.schema.json` | `rendered_surface_registry`, `workflow_metadata_registry` where route or workflow links appear, `authority_map` for source-of-truth boundaries | the indexes themselves plus `artifact_index` participation | `rendered_surface_registry` entries for `plan_overview.md` and any pack-level boards; `template_catalog` entries or section specs for those rendered views | Validator entries for each aggregate index; suite coverage for rebuild correctness and stale-source fail-closed behavior; fixtures proving aggregate rebuild from pack-wide initiatives and project-scoped initiatives |
| Template and rendered-view governance stack | `template_catalog.schema.json` and any section-spec schemas needed for governed templates | `template_catalog`, `documentation_family_registry`, `rendered_surface_registry`, `artifact_family_registry` for template-backed families, `promotion_policy_registry` when templates drive extracted guidance | `guidance_index` or `artifact_index` participation where templates are queryable; no dedicated index when they are support-only | concrete templates for initiative views, project surfaces, and extracted guidance families, plus structured LLM-facing authoring notes where the template carries agent guidance | Validator entries for template catalog and rendered registry; suite coverage that required templates exist, required sections resolve, and referenced template notes or section specs remain in sync |
| Workflow and human-instruction stack | `human_surface_policy_registry.schema.json` plus existing workflow metadata schemas and route metadata schemas as needed | `workflow_metadata_registry`, `human_surface_policy_registry`, `path_pattern_registry`, `template_catalog` when human workflow docs are templated | `workflow_index`, `route_index`, optional `artifact_index` participation when workflow docs are governed as first-class artifacts | `README.md` and `AGENTS.md` only at declared human roots; `core/workflows/ROUTING_TABLE.md` and `plan/workflows/ROUTING_TABLE.md` where routing is used; workflow-module templates or section specs where standardization is required | Validator entries for workflow metadata and human-surface policy; suite coverage proving required surfaces exist and machine-only roots do not carry stray instruction files |

## Current Items That Need Change To Meet The Future Endstate

| Current Item | Why It Needs To Change | Current Evidence | Required Direction |
|---|---|---|---|
| `docs/planning/**` stores live planning state. | Live initiatives should not live inside either future `core/docs/` or `plan/docs/` guidance surfaces. | Current planning corpus under `docs/planning/` | Move live planning to `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work, and use `plan/docs/` for approved extracted plan guidance. |
| Core-oriented docs are not rooted under `core/docs/`. | The desired future boundary is that core-related material lives under `core/` and only core-related material lives there. | Current durable core docs remain under root `docs/`. | Move core-only documentation to `core/docs/` over time, keep a duplicated `core/docs/foundations/` corpus aligned with `plan/docs/foundations/`, and leave non-core material out of `core/`. |
| There is no first-class `plan/` live-work root. | Without a visible live domain root, planning stays coupled to docs and control-plane projections. | No current `plan/` hierarchy exists. | Add `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work. |
| There is no initiative-local `.wt/` machine layer. | Live initiative state needs a local machine authority for snapshots, events, tasks, evidence, and promotion records. | Current planning state is mostly docs-backed with derived machine companions. | Add initiative-local `.wt/` contracts and runtime helpers. |
| There is no pack-level `plan/.wt/` aggregate tracking root. | Operators and agents need fast status lookup without crawling every initiative directory. | Current rollups are mostly central control-plane indexes over docs-backed sources. | Add `plan/.wt/` indexes and rollups sourced from both pack-wide initiative state and project-scoped initiative state. |
| There is no first-class `plan/projects/` project root. | Project-specific material needs its own separated home so plan-pack development can support future projects cleanly. | No current `plan/projects/` hierarchy exists. | Add `plan/projects/<project_slug>/` with project identity, supporting docs, references, linked repo metadata, and project-facing summaries. |
| Project context is not a first-class runtime load standard. | Project-specific work needs a separate context load rather than overloading pack-wide context. | Current runtime emphasis is on pack-wide loading only. | Standardize `pack_context` as always-loaded and `project_context` as an explicit separate load when the path, command, or workflow is project-scoped. |
| There is no initiative-local rendered human visibility layer. | Live work needs human-facing `plan.md`, `progress.md`, and `summary.md` surfaces without making them the primary machine authority. | No current initiative-local rendered-view model exists. | Add initiative-local rendered views built from local `.wt/` state. |
| Core and plan workflow roots are not split. | The clean endstate should not rely on one mixed repo-root workflow tree. | Current workflow routing and modules live under `workflows/` at the repo root. | Split workflow guidance into `core/workflows/` and `plan/workflows/` according to domain ownership. |
| Human-surface placement is not governed explicitly. | `README.md` and `AGENTS.md` should be deliberate human-surface tools, not incidental files scattered across machine trees. | Current repo uses some README and AGENTS files, but placement rules are implicit. | Add `human_surface_policy_registry`, keep README coverage on human-facing roots, and keep AGENTS only where interaction semantics materially change. |
| There is no explicit scope-classification rule for pack-wide versus project-scoped initiatives. | Without a hard rule, the same work can be modeled under conflicting roots and break query, context loading, and deletion logic. | Current repo has no first-class initiative-root split yet. | Add explicit scope classification rules and enforce them through path patterns, initiative-state fields, and validation coverage. |
| Duplicated foundations have no machine-enforced mirror rule. | Two required copies without enforced equivalence create silent authority drift. | The future model intentionally duplicates foundations across core and plan, but no current mirror contract exists. | Add mirror-group semantics or equivalent required-root rules through `documentation_family_registry`, template bindings, and validation suites. |
| Deletion and promotion gates are not yet explicit. | The clean endstate depends on removing temporary planning state, but removal rules must be deterministic to avoid losing durable guidance. | Current repo still retains live planning artifacts and historical traces in docs-backed form. | Add explicit promotion-before-deletion rules plus validation gates for any surviving replacements. |
| There is no governed `template_catalog`. | New initiative, project, guidance, and workflow surfaces need governed templates and section specs rather than ad hoc file conventions. | Current template handling remains mostly implicit or repo-local. | Add `template_catalog`, template schemas if needed, and concrete template files for every new human-facing surface family. |
| There is no governed promotion path from live initiatives into `plan/docs/` guidance surfaces. | Durable plan guidance should be extracted and approved out of live work instead of authored directly inside live planning. | Current planning docs and durable docs are mixed in one broad docs tree. | Add promotion records, promotion policy, and runtime helpers for extraction into `plan/docs/`, and keep duplicated foundations aligned across `core/docs/foundations/` and `plan/docs/foundations/`. |
| `artifact_index` still exposes `challenge_id`, `source_platform`, and `source_event`. | Those field names leak the old example domain into what is supposed to be a generic pack-facing interface. | `core/control_plane/schemas/interfaces/packs/artifact_index.schema.json` and `core/python/src/watchtower_core/control_plane/models/pack_contracts.py` | Replace with plan-domain-neutral or domain-neutral fields such as `work_item_id`, `source_context`, `source_channel`, or a richer nested provenance object. |
| `status_registry` still names `challenge` in `allowed_families` and includes solution-centric values like `solved` and `unresolved`. | A shared pack-facing status vocabulary should not hard-code challenge semantics when this repo is centered on planning work. | `core/control_plane/registries/status_registry.json` | Generalize status vocabulary or push pack-specific status subsets into `artifact_family_registry` plus `status_transition_rules`. |
| `watchtower_core.query` now exports reusable generic query services, but live planning queries still remain repo-local. | A future pack model still needs a reusable query boundary that stays generic and does not absorb plan-specific query families. | `core/python/src/watchtower_core/query/README.md` | Keep export-safe query services focused on declared surfaces, registries, routes, workflow metadata, and artifact-family rules while live planning queries stay under `repo_ops`. |
| `watchtower_core.sync` now exports a reusable generic sync harness, but plan sync targets still remain repo-local. | Multi-pack and exported-core use cases need a reusable sync boundary without forcing repo-local target orchestration into the package root. | `core/python/src/watchtower_core/sync/README.md` | Keep reusable authority-preserving sync helpers generic and drive `repo_ops` toward thinner pack-local orchestration rather than letting it remain the long-term boundary. |
| There is no explicit `artifact_family_registry`. | Family behavior is currently implied by paths, indexes, and conventions rather than governed as a first-class contract. | Current surfaces stop at `path_pattern_registry`, `status_registry`, and the generic `artifact_index` interface. | Add a registry that defines family ids, allowed paths, status subsets, rendered companions, and derived-index participation. |
| There is no `status_transition_rules` policy surface. | Status meaning is weaker if allowed transitions remain hidden in code or prose. | Current machine authority includes a status vocabulary but not transition policy. | Add family-aware transition policy when pack tasking or lifecycle grows beyond current planning cases. |
| Rendered-surface generation is still planning-specific. | The rendered-surface registry is generic enough to describe outputs, but the actual builders remain repo-local. | `core/control_plane/registries/rendered_surface_registry.json` plus planning sync modules under `watchtower_core.repo_ops.sync` | Extract a generic rendered-view builder once a second non-planning rendered surface pattern appears. |
| The `plan` fixture pack proves validation only. | Validation is a major milestone, but endstate pack readiness also needs query, sync, route, and rendered-view proofs. | `core/python/tests/fixtures/domain_packs/plan/.wt/pack_settings.json` plus fixture validation tests | Expand fixture-driven proofs incrementally after reusable runtime seams exist. |
| Lifecycle contracts for discrepancy, event, environment, review, and closeout are absent. | Pack growth will eventually need first-class lifecycle artifacts instead of burying these concerns in logs, docs, or handlers. | No current schemas or registries exist for these families. | Add only the families that solve real pack problems; do not blindly copy the source reference. |
| Planning runtime still assumes docs-backed family authority. | The future plan model is initiative-centric and event-backed, not docs-first. | Current scope in `docs/foundations/repository_scope.md` and current planning corpus under `docs/planning/` | Re-root live planning runtime onto pack-wide and project-scoped initiative roots, move core-only docs toward `core/docs/`, and use `plan/docs/` for extracted plan guidance. |
| `watchtower_core.repo_ops` still holds meaningful behavior. | The clean endstate should not depend on a broad repo-local orchestration namespace. | Current runtime still routes real behavior through `repo_ops`. | Move reusable behavior into explicit core boundaries and require explicit owner approval plus companion documentation for any residual `repo_ops` surface. |
| `pack_settings` surface declarations are still minimal. | Current declarations are enough for startup and validation, but future policy, template, or compatibility surfaces may deserve stronger declared kinds. | `core/control_plane/schemas/interfaces/packs/pack_settings.schema.json` | Extend surface kinds only when future packs need machine-distinct treatment, not just because the schema can grow. |
| Generic evidence is still narrower than future pack needs. | Validation evidence exists, but cross-review, closeout, and release evidence are not yet unified. | `core/control_plane/schemas/artifacts/validation_evidence.schema.json` and `watchtower_core.evidence` | Add a broader evidence bundle only if one artifact family can serve multiple pack workflows cleanly. |

## Proposed New Surfaces And Contracts

These are not all immediate implementation tasks. They are the highest-value additions if the repo continues moving toward a clean reusable-core plus `plan`-pack endstate.

### Highest-Value New Machine Surfaces

- `initiative_state.schema.json`
  - Defines the authoritative current-state snapshot for one initiative under either `plan/initiatives/<initiative_slug>/.wt/initiative.json` or `plan/projects/<project_slug>/initiatives/<initiative_slug>/.wt/initiative.json`.
- `initiative_event_stream.schema.json`
  - Defines the canonical append-only initiative history used to support replay, audit, and current-state rebuild.
- `task_state.schema.json`
  - Defines the authoritative current-state snapshot for one initiative-local task.
- `task_event_stream.schema.json`
  - Defines the task-level event history when task transitions need separate traceability from initiative-level events.
- `guidance_promotion_record.schema.json`
  - Captures what durable output was extracted from a live initiative, who approved it, where it was promoted, and what source events or state it came from.
- `initiative_index.json`
  - Provides pack-level aggregate lookup over both pack-wide initiatives and project-scoped initiatives without scanning every initiative folder.
- `task_index.json`
  - Provides pack-level aggregate lookup over tasks across initiatives.
- `status_rollup.json`
  - Provides fast current-state status buckets and counts for initiative and task tracking under `plan/.wt/`.
- `project_record.schema.json`
  - Defines the authoritative current-state snapshot for one project container under `plan/projects/<project_slug>/.wt/project.json`.
- `project_repository_map.schema.json`
  - Defines how one project records linked repositories such as the planning repo, implementation repo, deployment repo, or other separated project homes.
- `project_index.json`
  - Provides aggregate lookup across project containers.
- `guidance_index.json`
  - Provides aggregate lookup across approved extracted guidance under `plan/docs/`.
- `promotion_index.json`
  - Provides aggregate lookup across initiative-to-guidance promotions and project-facing promotion reuse.
- `artifact_family_registry.json`
  - Defines plan-pack artifact families such as initiative state, initiative events, task state, task events, work-item notes, validation bundles, promotion records, project records, project repository maps, references, and closeout recaps.
  - Declares canonical placement rules, allowed status subsets, derived-index participation, and whether rendered companions exist.
- `documentation_family_registry.json`
  - Defines which front-matter schema, template ids, section-spec schema, and allowed roots belong to each governed documentation family.
- `lifecycle_stage_registry.json`
  - Separates lifecycle stage from status values for initiatives, tasks, evidence, promotions, and project containers where needed.
- `status_transition_rules.json`
  - Declares family-specific allowed transitions, terminal states, and review-required transitions.
- `promotion_policy_registry.json`
  - Declares what categories of initiative-local outputs may become `plan/docs/` guidance and what review path they must pass through.
- `human_surface_policy_registry.json`
  - Declares where `README.md`, `AGENTS.md`, human workflow docs, and rendered visibility files are required, optional, or forbidden across `core/` and `plan/`.
- `project_surface_policy_registry.json`
  - Declares what categories of project-specific surfaces and initiative-derived outputs may live under `plan/projects/` and what metadata they must carry.
- `template_catalog.json`
  - Declares governed template ids, section requirements, section ordering, section-spec schemas, and LLM-facing authoring notes for initiative-local rendered views, `plan_overview.md`, project-local human surfaces, and extracted guidance surfaces.
- `documentation_section_spec.schema.json` family set
  - Defines machine-readable section requirements for template-backed families whose heading structure and ordering must be validated.
- `relation_type_registry.json`
  - Declares controlled relation names such as `implements`, `depends_on`, `supersedes`, `evidences`, `derived_from`, and `covers`.
- `review_status_registry.json`
  - Separates review workflow state from artifact lifecycle state.
- `source_type_registry.json`
  - Normalizes provenance labels such as `human_authored`, `agent_authored`, `derived`, `imported`, `external_reference`, and `generated`.
- `environment_context.schema.json`
  - Defines durable execution context when workflow routing or safety needs stronger environment awareness.
- `discrepancy_record.schema.json`
  - Defines first-class records for accepted exceptions, validation drift, sync drift, or unresolved governance mismatches.
- `closeout_recap.schema.json`
  - Defines a pack-level closeout artifact if the future plan pack needs structured summary, evidence references, and outcome status beyond current initiative closeout.

### Highest-Value New Runtime Helpers

- `event_stream_helper`
  - Appends, validates, and replays initiative-level and task-level events.
- `initiative_state_builder`
  - Rebuilds `initiative.json` from event history and other authoritative local state.
- `task_state_builder`
  - Rebuilds `task.json` from task-local events and initiative-local dependencies.
- `initiative_tracking_builder`
  - Builds pack-level aggregate initiative and task indexes plus status rollups under `plan/.wt/` across both pack-wide and project-scoped initiative roots.
- `guidance_promotion_helper`
  - Extracts approved durable guidance from initiatives into `plan/docs/` and writes promotion records, with optional duplication into `core/docs/` where core guidance overlap is useful.
- `project_surface_builder`
  - Builds and refreshes project-specific summaries, linked repository information, supporting docs, and implementation-boundary context under `plan/projects/<project_slug>/`.
- `project_context_helper`
  - Loads project-specific runtime context separately from `pack_context` when a path, command, or workflow targets one project.
- `template_catalog_helper`
  - Resolves governed template metadata and required section specs for initiative views, project surfaces, and extracted guidance outputs.
- `human_surface_policy_helper`
  - Resolves whether a given path family should carry `README.md`, `AGENTS.md`, rendered views, or no human-authored companion at all.
- `artifact_family_resolver`
  - Answers "what family is this artifact?", "where may it live?", and "which statuses and rendered views are allowed?"
- `query_harness`
  - Lets CLI and Python callers query the pack model through one reusable surface instead of importing repo-local planning handlers.
- `sync_harness`
  - Coordinates authority-preserving updates and companion-surface refresh without hard-coding planning-specific behavior.
- `rebuild_harness`
  - Rebuilds indexes and rendered views deterministically from authoritative sources.
- `route_preview_helper`
  - Exposes typed route-preview results beyond CLI string formatting.
- `workflow_execution_harness`
  - Runs routed workflow chains with explicit gates, evidence hooks, and future event recording.
- `rendered_view_builder`
  - Builds human-readable pack views from machine authority through one reusable contract.
- `discrepancy_helper`
  - Converts validation or sync drift into durable machine-readable discrepancy records.

## Proposed Future Plan-Pack Directory Shape

This is a conceptual target for the future internal `plan` live-work model. It is not a claim that the migration is already complete.

The tree below starts at `plan/` and `core/` intentionally. In the clean endstate, the repository root should remain a thin router with minimal entrypoint files such as `README.md` and `AGENTS.md`, not a third operational workspace.

```text
plan/  # plan-domain operational root for all non-core work
  README.md  # human overview of the plan domain root
  AGENTS.md  # agent-specific guidance for the plan-domain root
  plan_overview.md  # rendered human overview with domain summary and ongoing-work board
  docs/  # approved durable plan-domain guidance corpus
    README.md  # navigation for plan guidance families
    AGENTS.md  # agent guidance for plan guidance authoring and maintenance
    foundations/  # duplicated foundations corpus aligned with core
    standards/  # approved plan-domain standards
    references/  # approved plan-domain references
    decisions/  # approved durable decisions promoted from live work
    patterns/  # reusable plan-domain patterns and examples
  workflows/  # plan-domain human workflow guidance
    README.md  # navigation for plan workflows
    AGENTS.md  # agent guidance for workflow documents in the plan domain
    ROUTING_TABLE.md  # plan-domain route selection guidance
    modules/  # plan-domain workflow modules and procedures
  .wt/  # machine-facing plan pack root
    manifests/  # startup and load-root manifests
      pack_settings.json  # canonical plan-pack load contract
    registries/  # machine-readable lookup and rule surfaces
      schema_catalog.json  # declared schemas available to the plan pack
      validator_registry.json  # validator bindings for schema-backed surfaces
      validation_suite_registry.json  # validation suite definitions for the plan pack
      artifact_family_registry.json  # artifact family taxonomy and placement rules
      documentation_family_registry.json  # documentation family to schema/template bindings
      status_registry.json  # allowed status vocabulary
      lifecycle_stage_registry.json  # lifecycle stage vocabulary separate from status
      relation_type_registry.json  # controlled cross-artifact relationship names
      review_status_registry.json  # controlled review-state vocabulary
      source_type_registry.json  # provenance/source vocabulary
      actor_registry.json  # actor identities and actor-type rules
      workflow_metadata_registry.json  # machine metadata for workflows and routing
      rendered_surface_registry.json  # declared rendered human-facing surfaces
      governance_surface_map.json  # map of non-artifact governed surfaces
      authority_map.json  # source-of-truth and precedence map
      promotion_policy_registry.json  # rules for promoting live work into durable guidance
      human_surface_policy_registry.json  # rules for README, AGENTS, and other human surfaces
      project_surface_policy_registry.json  # rules for project-scoped surfaces
      template_catalog.json  # machine contract for templates, sections, and LLM guidance
    policies/  # policy artifacts that enforce behavior
      status_transition_rules.json  # allowed lifecycle transitions per family
      retention_policy_registry.json  # cleanup and deletion rules where needed
    schemas/  # schemas owned or mounted by the plan pack
      shared/  # reusable subschemas shared by multiple families
        actor_identity.schema.json  # actor identity structure
        source_reference.schema.json  # source/provenance reference structure
        relation_edge.schema.json  # cross-artifact relation edge structure
      interfaces/  # interface schemas for pack-facing authored surfaces
        documentation/  # documentation contracts and section-spec schemas
          front_matter_base.schema.json  # shared front-matter vocabulary
          foundation_front_matter.schema.json  # foundation-specific front-matter profile
          standard_front_matter.schema.json  # standard-specific front-matter profile
          reference_front_matter.schema.json  # reference-specific front-matter profile
          workflow_front_matter.schema.json  # workflow-specific front-matter profile
          prd_front_matter.schema.json  # PRD-specific front-matter profile
          decision_record_front_matter.schema.json  # decision-record front-matter profile
          feature_design_front_matter.schema.json  # feature-design front-matter profile
          implementation_plan_front_matter.schema.json  # implementation-plan front-matter profile
          task_front_matter.schema.json  # task front-matter profile
          project_summary_section_spec.schema.json  # section rules for project summaries
          initiative_plan_section_spec.schema.json  # section rules for initiative plans
      artifacts/  # artifact-family schemas
        artifact_family_registry.schema.json  # schema for artifact family registry entries
        lifecycle_stage_registry.schema.json  # schema for lifecycle stage registry entries
        relation_type_registry.schema.json  # schema for relation type registry entries
        review_status_registry.schema.json  # schema for review status registry entries
        source_type_registry.schema.json  # schema for source type registry entries
        status_transition_rules.schema.json  # schema for lifecycle transition policies
        promotion_policy_registry.schema.json  # schema for promotion policy entries
        human_surface_policy_registry.schema.json  # schema for human-surface placement rules
        project_surface_policy_registry.schema.json  # schema for project surface policy entries
        initiative_state.schema.json  # snapshot contract for one initiative
        initiative_event_stream.schema.json  # append-only initiative event contract
        task_state.schema.json  # snapshot contract for one task
        task_event_stream.schema.json  # append-only task event contract
        initiative_index.schema.json  # aggregate initiative index contract
        task_index.schema.json  # aggregate task index contract
        status_rollup.schema.json  # aggregate status rollup contract
        plan_work_item_note.schema.json  # generic plan work-item note contract
        guidance_promotion_record.schema.json  # promotion record contract for durable guidance
        project_record.schema.json  # project snapshot contract
        project_repository_map.schema.json  # linked-repository contract for a project
        project_index.schema.json  # aggregate project index contract
        validation_bundle.schema.json  # bundled validation/evidence contract
        discrepancy_record.schema.json  # discrepancy and exception record contract
        environment_context.schema.json  # execution-context contract
        closeout_recap.schema.json  # structured closeout summary contract
        promotion_index.schema.json  # aggregate promotion index contract
        guidance_index.schema.json  # aggregate durable-guidance index contract
        documentation_family_registry.schema.json  # schema for documentation family bindings
        template_catalog.schema.json  # schema for template metadata and section rules
        artifact_index.schema.json  # cross-family artifact index contract
    templates/  # machine-governed template assets
      initiatives/  # templates for initiative-local human surfaces
        plan.md  # initiative plan template
        progress.md  # initiative progress template
        summary.md  # initiative summary template
      pack/  # templates for pack-level human surfaces
        plan_overview.md  # pack overview template
      projects/  # templates for project-level human surfaces
        project.md  # project identity and context template
        repositories.md  # linked-repository summary template
        summary.md  # project summary template
      guidance/  # templates for durable guidance families
        foundations/  # templates specific to duplicated foundations guidance
        standard.md  # standard document template
        reference.md  # reference document template
        decision.md  # decision record template
        pattern.md  # reusable pattern template
    indexes/  # derived machine-readable query surfaces
      initiative_index.json  # aggregate lookup across initiatives
      task_index.json  # aggregate lookup across tasks
      status_rollup.json  # aggregate status board backing surface
      artifact_index.json  # cross-family artifact lookup
      route_index.json  # query surface for routes
      workflow_index.json  # query surface for workflows
      evidence_index.json  # query surface for evidence bundles
      discrepancy_index.json  # query surface for discrepancies
      promotion_index.json  # query surface for promotion history
      project_index.json  # query surface for projects
      guidance_index.json  # query surface for approved durable guidance
  initiatives/  # pack-wide initiatives not tied to one project
    README.md  # navigation for pack-wide initiatives
    AGENTS.md  # agent guidance for pack-wide initiative workspaces
    <initiative_slug>/  # one pack-wide initiative container
      plan.md  # rendered initiative plan view
      progress.md  # rendered initiative progress view
      summary.md  # rendered initiative summary view
      .wt/  # machine-facing initiative root
        initiative.json  # current-state initiative snapshot
        events/  # append-only initiative event history
          0001_created.json  # example initiative creation event
          0002_scope_refined.json  # example scope-change event
          0003_task_added.json  # example task-addition event
        tasks/  # task containers local to this initiative
          <task_slug>/  # one task container
            task.json  # current-state task snapshot
            events/  # append-only task event history
              0001_created.json  # example task creation event
              0002_in_progress.json  # example task progress event
              0003_completed.json  # example task completion event
        evidence/  # validation or evidence artifacts for this initiative
          validation_bundle.<id>.json  # example validation/evidence bundle
        promotions/  # promotion records tied to this initiative
          promotion.<id>.json  # example durable-guidance promotion record
  projects/  # project containers with project-scoped material
    README.md  # navigation for project containers
    AGENTS.md  # agent guidance for project workspaces
    <project_slug>/  # one project container
      project.md  # human project overview and identity surface
      repositories.md  # human summary of linked repositories
      summary.md  # human project summary surface
      docs/  # project-local durable docs
        foundations/  # project-local foundation material if needed
      references/  # project-local references and supporting material
      initiatives/  # initiatives scoped to this project
        <initiative_slug>/  # one project-scoped initiative
          plan.md  # rendered initiative plan view
          progress.md  # rendered initiative progress view
          summary.md  # rendered initiative summary view
          .wt/  # machine-facing initiative root
            initiative.json  # current-state initiative snapshot
            events/  # append-only initiative event history
              0001_created.json  # example initiative creation event
              0002_scope_refined.json  # example scope-change event
            tasks/  # task containers local to this project initiative
              <task_slug>/  # one project-scoped task container
                task.json  # current-state task snapshot
                events/  # append-only task event history
                  0001_created.json  # example task creation event
                  0002_in_progress.json  # example task progress event
      .wt/  # machine-facing project root
        project.json  # current-state project snapshot
        repository_map.json  # linked-repository machine map
core/  # core-only repository root
  README.md  # human overview of the core domain
  docs/  # core-only durable documentation
    README.md  # navigation for core docs
    foundations/  # duplicated foundations corpus aligned with plan
    engineering/  # core engineering guides
    bootstrap/  # environment and bootstrap guides
    style_guides/  # coding and authoring style guides
  workflows/  # core-only workflow guidance
    README.md  # navigation for core workflows
    AGENTS.md  # agent guidance for core workflow content
    ROUTING_TABLE.md  # core workflow route selection guidance
    modules/  # core workflow modules and procedures
  python/  # canonical Python workspace for reusable runtime code and tests
  control_plane/  # canonical machine-readable authority for core-owned surfaces
```

## Current-To-Future Migration Direction

### Near-Term

1. Stop treating new live planning additions under `docs/planning/` as the preferred long-term direction.
2. Define the canonical live roots at `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work.
3. Introduce initiative-state, task-state, and event-stream contracts before proliferating more live planning artifact families.
4. Add pack-level aggregate tracking under `plan/.wt/` so active initiative lookup does not depend on recursive scans.
5. Define `plan/projects/<project_slug>/` for project-specific context, references, linked repository metadata, and project-scoped initiatives.
6. Introduce separate `project_context` loading on top of always-loaded `pack_context`.
7. Split the current repo-root workflow corpus into `core/workflows/` and `plan/workflows/`, and add placement rules for `README.md` and `AGENTS.md`.
8. Keep validation generic and pack-aware, and extend it only when new step kinds are justified by real surfaces.
9. Keep future `WatchTower`-facing structures in this requirements and planning flow until explicit downstream product bootstrap begins; do not spread partial product truth into `/home/j/WatchTower` early.

### Mid-Term

1. Add reusable query and sync helpers at the package root instead of relying only on docs-backed `repo_ops` flows.
2. Introduce `status_transition_rules`, `relation_type_registry`, `promotion_policy_registry`, and other small but high-value rule-bearing surfaces.
3. Add a generic rendered-view builder for initiative-local `plan.md`, `progress.md`, `summary.md` plus pack-level `plan_overview.md`.
4. Add governed promotion paths from live initiatives into `plan/docs/` guidance surfaces.
5. Add governed project contracts, builders, and project-context loading under `plan/projects/`.
6. Duplicate and align the foundations corpus across `core/docs/foundations/` and `plan/docs/foundations/`.
7. Add human-surface placement policy and helper coverage so workflow roots and guidance roots stay navigable without polluting machine trees.
8. Broaden fixture-pack proof coverage beyond validation to route preview, query, sync, rendered views, initiative state, and aggregate tracking.

### Later

1. Add lifecycle families only if they solve concrete problems: discrepancy, environment, closeout, review, and event recording should be demand-driven.
2. Migrate current live planning families away from `docs/planning/`, move core-only docs toward `core/docs/`, duplicate foundations into `core/docs/foundations/` and `plan/docs/foundations/`, and use `plan/docs/` for approved extracted plan-domain guidance.
3. Remove broad repo-root workflow ownership in favor of `core/workflows/` and `plan/workflows/`.
4. Keep future external product work in a consuming repository rather than letting this repo silently absorb operator-facing pack runtime content.
5. Bootstrap `/home/j/WatchTower` only when the product-facing implementation details are approved and mature enough to land as downstream outputs rather than exploratory planning state.

## Reviewed Surfaces

This document was grounded in the current repository and the two requested reference sources.

### Reference Sources

- `/home/j/mvp_reference/required.md`
- `/home/j/WatchTowerOversight/data/artifacts/assessments/watchtower_oversight_required_endstate_gap_analysis.md`

### Key Current-State Foundations

- `README.md`
- `docs/foundations/repository_scope.md`
- `docs/foundations/product_direction.md`
- `docs/foundations/customer_story.md`
- `docs/foundations/engineering_design_principles.md`
- `docs/foundations/repository_standards_posture.md`

### Key Current-State Control-Plane Surfaces

- `core/control_plane/manifests/pack_settings.json`
- `core/control_plane/registries/governance_surface_map.json`
- `core/control_plane/registries/schema_catalog.json`
- `core/control_plane/registries/validator_registry.json`
- `core/control_plane/registries/validation_suite_registry.json`
- `core/control_plane/registries/status_registry.json`
- `core/control_plane/registries/rendered_surface_registry.json`
- `core/control_plane/registries/workflow_metadata_registry.json`
- `core/control_plane/schemas/interfaces/packs/pack_settings.schema.json`
- `core/control_plane/schemas/interfaces/packs/artifact_index.schema.json`
- `core/control_plane/schemas/interfaces/packs/pack_work_item_note.schema.json`
- `core/control_plane/schemas/artifacts/validation_suite_registry.schema.json`

### Key Runtime And Boundary Surfaces

- `core/python/src/watchtower_core/control_plane/loader.py`
- `core/python/src/watchtower_core/control_plane/pack_context.py`
- `core/python/src/watchtower_core/validation/README.md`
- `core/python/src/watchtower_core/validation/suite.py`
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
- `core/python/src/watchtower_core/cli/README.md`

### Key Planning And Endstate Direction Surfaces

- `docs/planning/prds/core_export_readiness_and_optimization.md`
- `docs/planning/prds/end_to_end_repo_review_and_rationalization.md`
- `docs/planning/prds/validated_core_and_pack_data_shape_convergence.md`
- `docs/planning/prds/plan_domain_pack_core_validation.md`

## Bottom Line

`WatchTowerPlan` already has enough machine authority, validation maturity, routing structure, and index coverage to justify treating it as the first serious internal `plan`-domain consumer of reusable core. The biggest current mismatch is not missing governance. It is that live planning still lives in docs instead of in a first-class `plan/` workspace, and core-only documentation and workflows are not yet fully rooted under `core/`. The next step is to re-root live planning around initiative-local machine state, pack-wide and project-scoped initiative roots, `plan_overview.md`, plan-domain workflows, duplicated foundations under both `core/docs/foundations/` and `plan/docs/foundations/`, and a separate `project_context` load standard, while driving broad `repo_ops` behavior toward elimination unless it is explicitly approved.
