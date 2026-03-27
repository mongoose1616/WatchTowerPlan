# Control-Plane Registry Contracts Plan

## Purpose

Lock the machine-readable entry shapes for the pack-owned control-plane registries that govern templates, durable documentation families, required human surfaces, and rendered-surface declarations.

## Current Contract Basis

- donor-pack precedent:
  - `WatchTowerPlan/plan/.wt/registries/template_catalog.json`
  - `WatchTowerPlan/plan/.wt/registries/documentation_family_registry.json`
  - `WatchTowerPlan/plan/.wt/registries/human_surface_policy_registry.json`
  - `WatchTowerPlan/plan/.wt/registries/rendered_surface_registry.json`
  - `WatchTowerOversight/oversight/.wt/registries/template_catalog.json`
  - `WatchTowerOversight/oversight/.wt/registries/rendered_surface_registry.json`
- Step 1 basis:
  - `STEP1_FINAL_v2.md`
    - `R49`: exact common registry JSON shape
    - `R50`: rendered registry markdown views generated from registry JSON
    - `R51`: canonical `template_standard` shape
    - `R59`: final governed-surface taxonomy and artifact-family registry
  - `STEP1_FINAL_v3.md`
    - pack-owned docs, rendered views, and workflow surfaces remain pack-owned governance work, not shared-core future assumptions

## Shared Registry Root Posture

Use the shared controlled-registry posture already locked elsewhere in the package:

- keep one authoritative JSON artifact per registry;
- keep root fields compatible with the donor-pack pattern:
  - `$schema`
  - `id`
  - `title`
  - `status`
- use `entries[]` for entry registries, `values[]` for controlled-value registries, and `surfaces[]` only for rendered-surface registries;
- use per-entry lifecycle via `entry_status` instead of deleting historical or deprecated entries in place.

## Template Catalog Contract

Canonical path:

- `offensive_security/.wt/registries/template_catalog.json`

Required entry fields:

- `template_id`
- `entry_status`
- `authorship_mode`
- `template_path`
- `required_section_ids`
- `optional_section_ids`
- `section_order`
- `allowed_roots`

Conditionally required fields:

- `surface_id` for root or human-surface templates such as `README.md` or `AGENTS.md`
- `family_id` for reusable documentation/workflow families
- `front_matter_schema_id` when the target family uses governed front matter
- `section_spec_schema_id` when section content is itself governed

Optional but strongly recommended fields:

- `llm_guidance`
- `llm_guidance_mode`
- `operator_notes`

Locked `llm_guidance` shape:

- `authoring_goal`
- `hard_requirements[]`
- `advisory_notes[]`

Locked rules:

- use `surface_id` and `family_id` as mutually exclusive selectors unless a future shared contract explicitly allows both;
- keep `allowed_roots` repository-relative and pack-relative, not absolute filesystem paths;
- keep section ordering explicit instead of treating required sections as unordered;
- govern authored roots and workflow docs through the same catalog rather than creating a second offsec-only template mechanism.

## Documentation Family Registry Contract

Canonical path:

- `offensive_security/.wt/registries/documentation_family_registry.json`

Required entry fields:

- `family_id`
- `entry_status`
- `summary`
- `allowed_roots`
- `authorship_mode`
- `required_index_ids`

Conditionally required fields:

- `front_matter_base_schema_id`
- `front_matter_schema_id`
- `template_ids`
- `section_spec_schema_id`

Optional mirror and equivalence fields:

- `mirror_group_id`
- `required_mirror_roots`
- `equivalence_mode`
- `mirror_update_mode`
- `notes`

Locked rules:

- every durable documentation family must name the templates that are valid for that family;
- every family must declare the roots in which the family may live;
- every family must declare the indexes that should surface it for lookup or promotion;
- mirror fields are allowed, but offsec must not assume cross-root byte-identical mirroring unless an explicit family needs it.

## Human Surface Policy Registry Contract

Canonical path:

- `offensive_security/.wt/registries/human_surface_policy_registry.json`

Required entry fields:

- `policy_id`
- `path_pattern`
- `match_mode`
- `root_kind`
- `entry_status`
- `governing_surfaces`
- `clarifying_rule`
- `surfaces`

Required `surfaces[]` entry fields:

- `relative_path`
- `entity_shape`
- `surface_role`
- `mode`
- `authorship_mode`

Optional `surfaces[]` fields:

- `notes`

Locked rules:

- keep `path_pattern` repository-relative and scoped to pack roots;
- use `mode` to distinguish `required` from `optional` human surfaces;
- use `authorship_mode` to distinguish `authored` from `rendered` surfaces;
- keep the policy registry focused on required human entrypoints by root, not as a duplicate of the repository path index.

Recommended offsec starter policy roots:

- `offensive_security`
- `offensive_security/docs`
- `offensive_security/workflows`
- `offensive_security/tracking`
- `offensive_security/knowledge`

## Rendered Surface Registry Contract

The exact rendered-surface entry contract is locked in the dedicated rendered-surface plan:

- `04_contracts/rendered_surface_contracts_plan.md`

## Query Family Registry Contract

Canonical path:

- `offensive_security/.wt/registries/query_family_registry.json`

Required entry fields:

- `family_id`
- `entry_status`
- `exposure_mode`
- `backing_surface`
- `output_contract_ref`
- `command_doc_path`

Conditionally useful fields:

- `curated_command_name`
- `supports_graph_expansion`
- `supports_generic_family_query`
- `notes`

Locked rules:

- use one registry for both curated and generic query families;
- generated command docs must stay aligned with this registry;
- route and workflow discovery remain shared-core surfaces and should not be duplicated here as pack-local aliases.

Control-plane rule:

- `human_surface_policy_registry` declares where rendered surfaces are required;
- `rendered_surface_registry` declares how they are generated.

## Locked Cross-Registry Rules

- every `template_id` referenced by `documentation_family_registry` must exist in `template_catalog`;
- every rendered human surface required by `human_surface_policy_registry` must exist in `rendered_surface_registry`;
- every curated or generic offsec query family must exist in `query_family_registry`;
- every authored workflow root policy that requires `ROUTING_TABLE.md` or `AGENTS.md` must stay aligned with `decision.routing_contract` and the workflow metadata registry;
- human-readable registry markdown companions may be rendered from authoritative JSON, but the JSON registry remains authoritative.

## Locked V1 Starter Registry Inventory

Phase-aware v1 inventory:

- baseline control-plane registries:
  - `artifact_family_registry`
  - `documentation_family_registry`
  - `template_catalog`
  - `human_surface_policy_registry`
  - `authority_map`
  - `rendered_surface_registry`
  - `query_family_registry`
  - `event_type_registry`
  - `discrepancy_type_registry`
  - `severity_registry`
  - `discrepancy_resolution_registry`
  - `governance_limit_registry`
- later-phase additions that still belong to the v1 package:
  - `source_type_registry`
  - `trust_state_registry`
  - `verification_status_registry`
  - `relation_type_registry`
  - `review_status_registry`
  - `promotion_policy_registry`

## Remaining Explicitly Open Items

No further control-plane inventory or entry-shape decisions remain open in v1. The remaining explicit package deferrals are the locked post-v1 items tracked in `08_tracking/implementation_gap_audit.md` and `indexes/open_decisions.json`.
