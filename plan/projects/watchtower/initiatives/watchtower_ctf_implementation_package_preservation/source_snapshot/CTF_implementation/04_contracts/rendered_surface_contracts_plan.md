# Rendered Surface Contracts Plan

## Purpose

Lock the machine-readable contract shape for offsec rendered surfaces and define the recommended v1 rendered-surface inventory so implementation does not have to infer section or table structures from prose alone.

## Current Contract Basis

- donor-pack precedent:
  - `WatchTowerPlan/plan/.wt/registries/rendered_surface_registry.json`
  - `WatchTowerOversight/oversight/.wt/registries/rendered_surface_registry.json`
- package basis:
  - `04_contracts/query_sync_rendered_views_docs_plan.md`
  - `04_contracts/control_plane_registry_contracts_plan.md`
- Step 1 basis:
  - `STEP1_FINAL_v2.md`
    - `R50`: rendered registry markdown views from authoritative JSON
    - `R56`: rendered `artifact_index` view posture
  - `STEP1_FINAL_v3.md`
    - rendered views are pack-owned visibility surfaces, not shared-core assumptions

## Registry Artifact

Canonical path:

- `offensive_security/.wt/registries/rendered_surface_registry.json`

Required root fields:

- `$schema`
- `id = registry.rendered_surfaces`
- `title`
- `status`
- `surfaces[]`

## Rendered Surface Entry Contract

Required `surfaces[]` entry fields:

- `surface_id`
- `title`
- `output_path`
- `sections`

Optional fields:

- `notes`

Required `sections[]` fields:

- `section_id`
- `kind`
- `source_key`

Conditionally required section fields:

- `title` for visible content sections
- `empty_message` for `table` and `bullet_summary` sections
- `columns[]` for `table` sections
- `label_field` and `count_field` for `bullet_summary` sections

Allowed v1 `kind` values:

- `table`
- `bullet_summary`
- `lines`
- `updated_at`

Required `columns[]` fields for `table` sections:

- `header`
- `field`
- `formatter`

Optional `columns[]` fields:

- `path_field`
- `label_field`
- `empty_value`
- `enabled_when_key`

Locked formatter vocabulary for v1:

- `plain`
- `code`
- `repo_link`
- `markdown`

## Locked V1 Offsec Surface Inventory

### `rendered.offsec.overview`

- `output_path = offensive_security/offensivesecurity_overview.md`
- recommended sections:
  - `pack_summary` as `lines`
  - `active_challenges` as `table`
  - `blocked_challenges` as `table`
  - `recent_sessions` as `table`
  - `knowledge_summary` as `bullet_summary`
  - `navigation_links` as `lines`

### `rendered.offsec.challenge_tracking`

- `output_path = offensive_security/tracking/challenge_tracking.md`
- recommended sections:
  - `active_challenges` as `table`
  - `closed_state_summary` as `bullet_summary`
  - `closed_challenges` as `table`
  - `updated_at`

### `rendered.offsec.blocker_tracking`

- `output_path = offensive_security/tracking/blocker_tracking.md`
- recommended sections:
  - `open_blockers` as `table`
  - `resolved_blocker_summary` as `bullet_summary`
  - `recently_resolved_blockers` as `table`
  - `updated_at`

### `rendered.offsec.session_tracking`

- `output_path = offensive_security/tracking/session_tracking.md`
- recommended sections:
  - `active_sessions` as `table`
  - `recent_sessions` as `table`
  - `updated_at`

### `rendered.offsec.knowledge_tracking`

- `output_path = offensive_security/tracking/knowledge_tracking.md`
- recommended sections:
  - `promotion_summary` as `bullet_summary`
  - `candidate_knowledge` as `table`
  - `accepted_knowledge` as `table`
  - `updated_at`

## Recommended Column Contracts

The authoritative row-shape decisions are locked elsewhere in the package, and the rendered contract should assume these starter columns:

- challenge tracking:
  - `challenge_id`
  - `status`
  - `platform`
  - `event`
  - `summary`
  - `last_activity_at_utc`
- blocker tracking:
  - `blocker_id`
  - `challenge_id`
  - `severity`
  - `status`
  - `summary`
  - `active_governance_limits`
- session tracking:
  - `session_id`
  - `challenge_id`
  - `status`
  - `requested_mode`
  - `effective_mode`
  - `environment_type`
  - `last_activity_at_utc`
- knowledge tracking:
  - `knowledge_id`
  - `family`
  - `status`
  - `review_status`
  - `title`
  - `updated_at_utc`

## Locked Rules

- rendered surfaces are derived and non-authoritative;
- rendered surfaces must depend on authoritative indexes or authoritative hidden records, not on other rendered markdown;
- `human_surface_policy_registry` must require any rendered overview or tracking surface that the registry publishes;
- `rendered_surface_registry` must be the only machine-readable declaration of rendered view structure in v1;
- use stable `surface_id` values so sync and rendered-view tests do not depend on path text alone.

## Remaining Explicitly Open Items

No further rendered-surface feed contracts remain open in v1. The surface inventory, query-output baseline, and supporting row contracts are all locked elsewhere in the package.
