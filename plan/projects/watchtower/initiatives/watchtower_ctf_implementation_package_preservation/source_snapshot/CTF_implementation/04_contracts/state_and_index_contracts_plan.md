# State, Index, And Reconciliation Contracts Plan

## Purpose

Lock the field-level contracts for pack-owned state records, machine indexes, graph traversal, and discrepancy governance so Phase 2 through Phase 4 work does not need to reinterpret Step 1 decisions.

## Step 1 Basis

- `STEP1_FINAL_v2.md`
  - `R06`: event-stream envelope
  - `R12`, `R13`, and `R64`: `artifact_index`, `environment_context`, and final machine-surface posture
  - `R28` and `R81`: event-type registry plus sync or rebuild additions
  - `R32`, `R33`, `R34`, and `R74`: discrepancy record, discrepancy registries, resolution actions, and enforceable exception limits
- `STEP1_FINAL.md`
  - confirms the same discrepancy and artifact-index direction
- workshop normalization
  - richer queryable indexes, a separate derived graph index, denormalized graph edges, and broader starter event vocabularies are now locked into the package

## Event Stream Contract

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson`

Locked shared envelope:

- `event_id`
- `event_type`
- `timestamp_utc`
- `challenge_id`

Conditionally present envelope fields:

- `session_id`
- `actor_ref`
- `requested_mode`
- `effective_mode`
- `interaction_mode`
- `artifact_id`
- `artifact_family`
- `workflow_id`
- `route_id`
- `reason`
- `payload`

Locked rules:

- keep one stable top-level event envelope and use `payload` for event-type-specific detail;
- keep event payloads compact and searchable rather than turning the envelope into a catch-all field dump;
- keep command-related payload detail to summaries, execution metadata, and artifact refs; raw stdout or stderr belongs in evidence artifacts, not inline event payloads;
- use `event_stream` as the append-only audit surface, not as the sole source of current state;
- current-state provenance still lives on the affected artifact or index surface when relevant.

## Event Type Registry

Canonical path:

- `offensive_security/.wt/registries/event_type_registry.json`

Locked starter event types:

- lifecycle:
  - `challenge_created`
  - `status_changed`
  - `mode_changed`
  - `closeout_created`
  - `closeout_completed`
- session:
  - `session_started`
  - `session_resumed`
  - `session_completed`
  - `session_closed`
- command and execution:
  - `command_activity`
  - `command_refused`
- workflow and routing:
  - `workflow_started`
  - `workflow_completed`
  - `workflow_routed`
  - `workflow_handoff`
  - `workflow_escalated`
- review, promotion, and reconciliation:
  - `review_requested`
  - `review_completed`
  - `knowledge_promoted`
  - `discrepancy_detected`
  - `discrepancy_resolved`
- transfer and evidence:
  - `airgapped_import`
  - `airgapped_export`
  - `evidence_captured`
- validation, sync, and rebuild:
  - `validation_started`
  - `validation_completed`
  - `sync_started`
  - `sync_completed`
  - `rebuild_started`
  - `rebuild_completed`

Locked command-event posture:

- use one base `command_activity` event family rather than environment-specific event names;
- require `payload.stage = planned | executed | imported`;
- require `payload.execution_context_type = local | ssh | vpn_reachable | airgapped`;
- allow compact payload fields such as `command_summary`, `exit_code`, `related_evidence_refs`, `transfer_ref`, and `safety_classification`.

Per-entry governed fields should include:

- event name
- description
- required top-level fields beyond the shared envelope
- allowed payload fields
- lifecycle status

## Artifact Index Contract

Canonical path:

- `offensive_security/.wt/indexes/artifact_index.json`

Required core entry fields:

- `artifact_id`
- `artifact_family`
- `path`
- `pack`
- `status`
- `authoritative`
- `hidden`
- `derived`
- `created_at_utc`
- `updated_at_utc`

Conditionally required fields:

- `subdomain`
- `challenge_id`
- `session_id`
- flattened `source_*` fields when source metadata exists
- `title`
- `summary`
- `review_status`
- `trust_state`
- `verification_status`
- discrepancy cues
- family-specific visibility fields such as `workflow_surface`

Standard optional relationship and navigation fields:

- `parent_artifact_id`
- `related_artifact_ids`
- `route`
- `rendered_view_path`

Locked rules:

- keep `artifact_index` broad enough for machine lookup rather than reducing it to a minimal metadata list;
- keep family-specific extension fields optional rather than globally required;
- keep `related_artifact_ids` derived-only in the index rather than the primary relation authority;
- keep the machine `artifact_index` richer than its human-rendered summary view.

## Graph Index Contract

Canonical path:

- `offensive_security/.wt/indexes/graph_index.json`

Locked role:

- keep authoritative typed `relations[]` on source artifacts;
- derive a separate traversal-oriented `graph_index` for public graph queries and relation-heavy retrieval;
- refresh `graph_index` through a dedicated sync target and through `all`.

Required root fields:

- `generated_at_utc`
- `nodes`
- `edges`
- `adjacency`

Locked node model:

- `node_id`
- `family`
- `artifact_kind`
- `title_or_summary`
- `canonical_path`
- `status`
- `updated_at_utc`
- `review_status`
- `trust_state`
- `verification_status`
- `rendered_view_path`

Conditionally useful node fields:

- `challenge_id`
- `parent_refs`
- `family_context`

Locked edge model:

- keep typed directed edges with denormalized traversal metadata;
- required baseline:
  - `source_id`
  - `target_id`
  - `relation_type`
- standard denormalized edge fields:
  - `source_family`
  - `source_status`
  - `target_family`
  - `target_status`
  - `evidence_refs`
  - `provenance_refs`
  - `created_at_utc`
  - `review_status`
  - `trust_state`
  - `verification_status`
  - `challenge_id`
  - `environment_type`
  - `edge_summary`

Locked rules:

- graph roots may be any typed artifact id from relational families such as challenge, knowledge, evidence, event, discrepancy, transfer, closeout, and related governed families;
- public graph traversal defaults to both incoming and outgoing direction;
- graph traversal must support `--from`, `--depth`, `--direction`, `--relation`, `--family`, `--limit`, `--format`, `--status`, `--review-status`, `--trust-state`, and `--verification-status`;
- graph output must support `human`, `json`, and `both` render modes.

## Environment Context Contract

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json`

Locked authoritative shape:

- root governed record plus nested `environment_context`
- always require `environment_context.summary`
- always require `environment_context.type`

Recommended standard nested fields:

- `environment_context.os_family`
- `environment_context.shell`
- `environment_context.runtime`
- `environment_context.execution_location`
- `environment_context.transport`
- `environment_context.remote_host`
- `environment_context.constraints`
- `environment_context.capabilities`
- `environment_context.user_controls_execution`
- `environment_context.agent_can_execute`
- `environment_context.requires_human_transfer`

Locked starter `environment_context.type` values:

- `local`
- `ssh`
- `vpn_reachable`
- `airgapped`

Locked normalized `constraints` starter values:

- `no_bash`
- `read_only_filesystem`
- `no_direct_execution`
- `airgapped_transfer_required`
- `vpn_required`
- `no_root`
- `no_outbound_internet`
- `limited_tooling`

Locked normalized `capabilities` starter values:

- `bash_available`
- `python_available`
- `ssh_available`
- `vpn_reachable`
- `artifact_capture_available`
- `checksum_available`
- `can_execute_locally`
- `can_execute_remotely`
- `can_transfer_files`
- `can_copy_paste_batches`

Locked flattened index fields:

- `environment_type`
- `environment_summary`
- `environment_os_family`
- `environment_shell`
- `environment_runtime`
- `environment_execution_location`
- `environment_transport`
- `environment_remote_host`
- `environment_user_controls_execution`
- `environment_agent_can_execute`
- `environment_requires_human_transfer`

## Current-Compatible Lifecycle Subsets

Shared live-core status compatibility requires current-compatible family subsets rather than ad hoc pack-only status values.

Locked challenge `status` subset:

- `active`
- `blocked`
- `in_review`
- `needs_review`
- `completed`
- `closed`

Locked rules for challenge status:

- use `completed` for successful solve completion at the artifact `status` layer;
- carry `solved`, `blocked_closeout`, `unresolved`, and similar terminal semantics in `closeout_record.outcome` rather than inventing pack-only `status` values that do not exist in the live shared `status_registry`;
- use `closed` for terminal challenge closure when work is no longer active, regardless of whether the closeout outcome was successful or unresolved.

Locked session `status` subset:

- `active`
- `blocked`
- `in_review`
- `needs_review`
- `completed`
- `closed`
- `cancelled`

Locked rules for session status:

- use `blocked` for paused or waiting session states that cannot safely continue yet;
- model handoff readiness through explicit session fields such as `handoff_ready` and `handoff_notes` rather than through extra session-only status values;
- allow only one `active` session per challenge at a time;
- use `completed` when a session reaches its intended handoff or execution goal before final close, and `closed` when the session is terminal.

## Challenge Metadata Contract

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/challenge_metadata.json`

Required fields:

- `challenge_id`
- `challenge_slug`
- `canonical_path`
- `challenge_path`
- `notes_path`
- `source`
- `status`
- `created_at_utc`
- `updated_at_utc`

Conditionally required fields:

- `platform_slug`
- `event_slug`
- `display_title`
- `review_required`
- `review_status`
- `current_session_id`
- `active_blocker_count`
- `unresolved_discrepancy_count`
- `last_activity_at_utc`
- `rendered_view_path`
- `latest_closeout_ref`

Locked rules:

- keep identity and provenance compact, structured, and machine-governed;
- keep authored challenge body content authoritative in `challenge.md` rather than duplicating it into JSON;
- use the nested `source` shape from `04_contracts/artifact_payload_contracts_plan.md`;
- use the locked challenge `status` subset from this document.

## Notes Metadata Contract

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/notes_metadata.json`

Required fields:

- `challenge_id`
- `notes_path`
- `reconciliation_state`
- `updated_at_utc`
- `unresolved_blocker_count`
- `unresolved_discrepancy_count`

Conditionally required fields:

- `content_checksum`
- `last_user_edit_at_utc`
- `last_agent_edit_at_utc`
- `last_reconciled_at_utc`
- `current_session_id`
- `last_editor_actor_ref`
- `visible_summary_present`

Locked rules:

- `notes.md` remains authoritative for working narrative and sequential capture;
- `ctf_notes_metadata` exists only to support reconciliation, summaries, and aggregate views;
- metadata must stay append-safe and must not become a second competing notes surface.

## Session State Contract

Canonical path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json`

Required fields:

- `session_id`
- `challenge_id`
- `status`
- `requested_mode`
- `effective_mode`
- `interaction_mode`
- `environment_context_ref`
- `started_at_utc`
- `last_activity_at_utc`

Conditionally required fields:

- `current_workflow_id`
- `current_route_id`
- `current_summary`
- `recent_command_refs`
- `recent_evidence_refs`
- `blocker_ref`
- `pause_reason`
- `handoff_ready`
- `handoff_notes`
- `resumed_from_session_id`
- `closed_at_utc`
- `close_reason`
- `review_notes`
- `operator_actor_ref`
- `reviewer_actor_ref`

Locked rules:

- use the locked current-compatible session `status` subset from this document;
- capture handoff and pause semantics through explicit fields instead of unsupported session-only lifecycle values;
- allow only one `active` session per challenge;
- treat notes and event history as fallback reconstruction surfaces when `session_state` is incomplete or flagged for review.

## Discrepancy Contract

Canonical challenge-local path:

- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/discrepancies/<discrepancy_id>.json`

Canonical pack-level path when promoted to broad governance visibility:

- `offensive_security/.wt/discrepancies/<discrepancy_id>.json`

Required discrepancy fields:

- `discrepancy_id`
- `artifact_family`
- `discrepancy_type`
- `severity`
- `detected_at`
- `detected_by`
- `status`
- `source_artifact_ref`
- `summary`

Conditionally required fields:

- `challenge_id`
- `session_id`
- `affected_field`
- `machine_value`
- `observed_value`
- `expected_value`
- `related_artifact_refs`
- `related_event_refs`
- `forces_needs_review`
- `resolution`
- `resolved_at`
- `resolved_by`
- `resolution_notes`
- `governance_limits`

Locked discrepancy `status` values:

- `open`
- `in_review`
- `resolved`
- `dismissed`

Locked workflow:

1. detect discrepancy
2. create discrepancy record
3. emit `discrepancy_detected`
4. force `needs_review` when severity or semantics require it
5. reconcile or review
6. resolve, dismiss, or exception the discrepancy
7. emit `discrepancy_resolved`

Locked rules:

- mirror active discrepancy state into `artifact_index` for query and filtering;
- keep discrepancy `status` separate from `resolution`;
- treat `event_stream` as the audit trail of discrepancy activity, not as the active discrepancy surface;
- use governed `status`, `forces_needs_review`, and `governance_limits` instead of ad hoc severity names such as `policy_block`.

## Discrepancy Registries And Enforcement

Canonical registry paths:

- `offensive_security/.wt/registries/discrepancy_type_registry.json`
- `offensive_security/.wt/registries/severity_registry.json`
- `offensive_security/.wt/registries/discrepancy_resolution_registry.json`
- `offensive_security/.wt/registries/governance_limit_registry.json`

Locked starter `discrepancy_type` values:

- `sync_conflict`
- `validation_error`
- `unknown_value`
- `invalid_transition`
- `status_mismatch`
- `review_state_mismatch`
- `provenance_gap`
- `trust_mismatch`
- `verification_gap`
- `missing_required_field`
- `invalid_relation`
- `registry_violation`
- `route_drift`
- `workflow_metadata_drift`
- `preview_contract_drift`

Locked starter `severity` values:

- `informational`
- `low`
- `medium`
- `high`
- `critical`

Locked starter `resolution` values:

- `resolved`
- `dismissed`
- `exceptioned`

Locked starter `governance_limits` values:

- `read_only_only`
- `no_remote_execution`
- `no_closeout`
- `review_required`
- `no_promotion`
- `no_full_auto`
- `no_transfer`

Locked enforcement rules:

- discrepancy types define default severity and whether `forces_needs_review` is implied by default;
- `exceptioned` is allowed only for discrepancy types that explicitly permit exceptions;
- exception-imposed `governance_limits` live on the discrepancy record and may be mirrored onto affected artifacts while the discrepancy remains active;
- validators and workflow gates must enforce active `governance_limits` rather than treating them as advisory notes only.

## Derived Pack Index Row Contracts

### Challenge Index Rows

Canonical path:

- `offensive_security/.wt/indexes/challenge_index.json`

Required baseline fields:

- `challenge_id`
- `status`
- `summary`
- `canonical_path`
- `last_activity_at_utc`

Standard rich fields:

- `platform`
- `event`
- `challenge_slug`
- `challenge_title`
- `current_workflow_id`
- `current_session_id`
- `blocker_count`
- `unresolved_discrepancy_count`
- `active_governance_limits`
- `latest_closeout_ref`
- `closeout_outcome`
- `evidence_count`
- `knowledge_candidate_count`
- `rendered_view_path`

Locked rules:

- use `challenge_id` as the stable machine key and expose human labeling through `challenge_title` or `challenge_slug`;
- keep the row rich enough to answer challenge-state, workflow, blocker, and closeout questions without forcing raw challenge-local lookups first;
- treat closed-only fields such as `closeout_outcome` as conditional, not fabricated defaults.

### Blocker Index Rows

Canonical path:

- `offensive_security/.wt/indexes/blocker_index.json`

Required baseline fields:

- `blocker_id`
- `challenge_id`
- `status`
- `severity`
- `summary`

Standard rich fields:

- `blocker_type`
- `discrepancy_id`
- `active_governance_limits`
- `requires_review`
- `resolution_status`
- `opened_at_utc`
- `last_updated_at_utc`
- `canonical_path`
- `rendered_view_path`
- `source_artifact_ref`
- `owner_role`

Locked rules:

- use one blocker-oriented row shape even when the underlying source record is a discrepancy;
- keep blocker lookup independent from raw discrepancy traversal;
- mirror active governance limits when they materially affect operator action.

### Session Index Rows

Canonical path:

- `offensive_security/.wt/indexes/session_index.json`

Required baseline fields:

- `session_id`
- `challenge_id`
- `status`
- `requested_mode`
- `effective_mode`
- `environment_type`
- `started_at_utc`
- `last_activity_at_utc`
- `canonical_path`

Standard rich fields:

- `interaction_mode`
- `current_workflow_id`
- `environment_summary`
- `handoff_ready`
- `operator_actor_ref`
- `reviewer_actor_ref`
- `active_governance_limits`
- `recent_evidence_count`
- `last_command_summary`

Locked rules:

- answer session, execution-context, and handoff questions without forcing a raw `session_state` open first;
- project pause or handoff posture through explicit fields, not extra status values;
- keep the canonical challenge path visible for navigation.

### Knowledge Index Rows

Canonical path:

- `offensive_security/.wt/indexes/knowledge_index.json`

Required baseline fields:

- `knowledge_id`
- `family`
- `title`
- `status`
- `review_status`
- `trust_state`
- `verification_status`
- `canonical_path`
- `updated_at_utc`

Standard rich fields:

- `summary`
- `tactic_refs`
- `source_count`
- `evidence_count`
- `relation_count`
- `parent_refs`
- `freshness_bucket`
- `rendered_view_path`

Locked rules:

- keep reusable-knowledge review and provenance posture visible in the index;
- keep the row rich enough for retrieval and ranking without duplicating the full artifact payload;
- use `knowledge_id` as the stable machine key and keep navigation through the canonical path.

## Remaining Explicitly Open Items

No further Phase 2 or Phase 3 state or index record-shape decisions remain open in v1. Related closeout, knowledge-policy, and safety-policy defaults are now also locked elsewhere in the package.
