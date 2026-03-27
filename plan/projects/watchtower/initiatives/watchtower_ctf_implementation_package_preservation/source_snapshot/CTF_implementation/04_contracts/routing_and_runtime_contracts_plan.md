# Routing And Runtime Contracts Plan

## Purpose

Lock the current-compatible workflow metadata, route-index, route-preview, and generic query-helper contracts so Phase 3 runtime work can compose with live shared-core behavior instead of re-deriving or overspecifying it.

## Current Contract Basis

- live shared-core workflow metadata contract:
  - `core/control_plane/schemas/artifacts/workflow_metadata_registry.schema.json`
  - `core/docs/standards/engineering/hosted_pack_integration_standard.md`
- live shared-core routing and preview contract:
  - `core/docs/standards/data_contracts/route_index_standard.md`
  - `core/docs/commands/core_python/watchtower_core_route_preview.md`
  - `core/python/src/watchtower_host/cli/route_handlers.py`
- Step 1 basis:
  - `R15`, `R16`, `R17`, and `R53` from `STEP1_FINAL_v2.md`

## Workflow Metadata Registry Contract

Canonical path:

- `offensive_security/.wt/registries/workflow_metadata_registry.json`

Locked v1 contract:

- use the live shared-core `workflow_metadata_registry` schema as the pack-facing authority;
- required entry fields remain:
  - `workflow_id`
  - `phase_type`
  - `task_family`
  - `primary_risks`
- optional entry fields remain:
  - `extra_trigger_tags`
  - `companion_workflow_ids`

Deconfliction with Step 1:

- the richer `R15` fields such as `title`, `summary`, `inputs`, `outputs`, `owner`, `version`, `workflow_surface`, and relationship lists are not the current-compatible pack metadata contract;
- treat those richer fields as either:
  - already represented elsewhere by authored workflow docs and the shared workflow index, or
  - deferred behind the existing `workflow_catalog` locked post-v1 deferral;
- do not invent a pack-local superseding metadata schema in v1.

## Authored Routing Surface

Canonical authored authority:

- `offensive_security/workflows/ROUTING_TABLE.md`

Locked v1 rules:

- treat `offensive_security/workflows/ROUTING_TABLE.md` and `offensive_security/.wt/registries/workflow_metadata_registry.json` as co-equal authoritative routing surfaces;
- validate authored routing and workflow metadata together so task-type intent and machine metadata cannot drift independently;
- if the two surfaces disagree, fail validation immediately rather than selecting a precedence winner;
- keep the authored routing table in the current shared human-readable format:
  - task type
  - trigger keywords
  - required workflows
- keep the routing table as the operator-facing procedural authority for workflow activation;
- keep richer machine-readable routing data in the derived route index rather than expanding authored routing entries into a second pack-local routing schema.

## Derived Route Index Contract

Shared derived surface:

- `core/control_plane/indexes/routes/route_index.json`

Locked entry fields from the live shared standard:

- `route_id`
- `task_type`
- `trigger_keywords`
- `required_workflow_ids`
- `required_workflow_paths`

Locked rules:

- the route index is derived, deterministic, and non-authoritative relative to authored routing tables;
- pack-owned routing tables feed the shared route-index rebuild and do not create a second pack-specific route-index family in v1.

## Route Preview Contract

Authoritative command surface:

- `watchtower-core route preview`

Locked JSON output fields from the live shared-core command:

- `command`
- `status`
- `request`
- `task_type`
- `selected_route_count`
- `selected_routes`
- `selected_workflows`
- `warnings`

Locked `selected_routes` entry fields:

- `route_id`
- `task_type`
- `score`
- `matched_keywords`
- `required_workflow_ids`
- `required_workflow_paths`

Locked `selected_workflows` entry fields:

- `workflow_id`
- `workflow_kind`
- `title`
- `doc_path`
- `phase_type`
- `task_family`
- `composes_module_paths`

Locked human output posture:

- print selected routes first;
- print active workflows second;
- print warnings last;
- remain deterministic, read-only, and advisory.

Deconfliction with Step 1:

- Step 1’s richer advisory ideas such as `match_strength`, `why_selected`, and merged per-route module explanations remain useful rationale, but they are superseded by the live shared-core route-preview contract unless shared core evolves to publish them.

## Shared Query-Helper Contract

Locked generic query-helper posture from Step 1:

- shared core remains the home for generic pack-agnostic query surfaces;
- format changes presentation, not the underlying query operation;
- pack-specific offsec query helpers should compose on top of the generic query surface rather than bypassing it.
- do not add pack-specific aliases for shared route or workflow query surfaces in v1; keep offsec-specific queries focused on offsec-owned artifacts and rendered views.

Locked shared query-helper capabilities to assume exist or compose with:

- direct lookup by id or path
- filtered listing by family, status, and review status
- provenance and relation traversal
- workflow and routing lookup
- registry lookup and controlled-value validation
- search-style filtering by text, tags, source, and environment

## Remaining Explicitly Open Items

These still need explicit package-owned decisions because the source set does not fully settle them in current-compatible terms:

- `decision.workflow_catalog`: whether a future `workflow_catalog` becomes necessary after the baseline pack is proven
