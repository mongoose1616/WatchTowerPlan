# Lifecycle And Safety Policy Contracts Plan

## Purpose

Lock the machine-readable artifact shapes for lifecycle transition policy and safety confirmation policy so Phase 2 and Phase 6 implementation can author policy artifacts without inventing new contract structure mid-build.

## Current Contract Basis

- donor-pack precedent:
  - `WatchTowerOversight/oversight/.wt/policies/status_transition_rules.json`
- package basis:
  - `06_standards/operator_modes_and_safety_standard.md`
  - `04_contracts/state_and_index_contracts_plan.md`
- Step 1 basis:
  - `STEP1_FINAL_v2.md`
    - `R07`: initial safety enforcement matrix shape
    - `R30`: exact `status` transition rules per family
  - `STEP1_FINAL.md` and `STEP1_FINAL_v3.md`
    - lifecycle coherence and safety enforcement remain pack-owned work

## Status Transition Rules Contract

Canonical path:

- `offensive_security/.wt/policies/status_transition_rules.json`

Required root fields:

- `$schema`
- `id = policy.status_transition_rules`
- `title`
- `status`
- `entries[]`

Required `entries[]` fields:

- `rule_id`
- `entry_status`
- `family_id`
- `transition_field`
- `initial_states`
- `terminal_states`
- `transitions`

Required `transitions[]` fields:

- `from_state`
- `to_state`
- `review_required`

Optional fields:

- `notes`

Locked rules:

- keep one transition-policy artifact for pack-owned lifecycle families rather than scattering lifecycle rules across service code;
- use one `entries[]` record per governed lifecycle family;
- keep `review_required` explicit on transitions rather than inferring it only from target status;
- let validators and workflow gates enforce discrepancy-derived governance limits separately from raw lifecycle admissibility.

Locked v1 starter families:

- `challenge_state`
- `session_state`
- `knowledge_state`
- `closeout_record`
- `extraction_output`

## Locked V1 Starter Entries

### `challenge_state`

- `initial_states`: `active`
- `terminal_states`: `closed`
- locked transitions:
  - `active -> blocked | needs_review | in_review | completed | closed`
  - `blocked -> active | needs_review | in_review | closed`
  - `needs_review -> in_review | active | blocked`
  - `in_review -> active | blocked | needs_review | completed | closed`
  - `completed -> closed`
  - `completed -> active` only through an explicit reopen path with `review_required = true`
  - `closed -> active` only through an explicit reopen path with `review_required = true`

### `session_state`

- `initial_states`: `active`
- `terminal_states`: `closed`, `cancelled`
- locked transitions:
  - `active -> blocked | needs_review | in_review | completed | cancelled | closed`
  - `blocked -> active | needs_review | in_review | cancelled | closed`
  - `needs_review -> in_review | active | blocked`
  - `in_review -> active | blocked | needs_review | completed | cancelled | closed`
  - `completed -> closed`

### `knowledge_state`

- `initial_states`: `candidate`
- `terminal_states`: `archived`
- locked transitions:
  - `candidate -> needs_review | in_review | accepted | archived`
  - `needs_review -> in_review | candidate | archived`
  - `in_review -> candidate | accepted | deprecated | needs_review | archived`
  - `accepted -> needs_review | deprecated | archived`
  - `deprecated -> needs_review | archived`
- locked review posture:
  - any transition into `accepted` or `deprecated` requires review;
  - runtime auto-promotion remains off by default even though `candidate -> accepted` is modeled explicitly.

### `closeout_record`

- `initial_states`: `active`
- `terminal_states`: `archived`
- locked transitions:
  - `active -> archived`

### `extraction_output`

- `initial_states`: `active`
- `terminal_states`: `archived`, `superseded`
- locked transitions:
  - `active -> archived | superseded`

Locked rules:

- validation and workflow gates must treat the starter entries above as the v1 source of truth rather than inferring lifecycle behavior only from allowed `status` values;
- challenge and session reopen edges must be explicit and review-gated rather than silently accepting backward status edits;
- reusable-knowledge promotion and deprecation must follow the published `knowledge_state` matrix rather than ad hoc review-side effects.

## Safety Confirmation Matrix Contract

Canonical path:

- `offensive_security/.wt/policies/safety_confirmation_matrix.json`

Required root fields:

- `$schema`
- `id = policy.safety_confirmation_matrix`
- `title`
- `status`
- `entries[]`

Required `entries[]` fields:

- `rule_id`
- `entry_status`
- `action_classification`
- `confirmation_required`
- `applies_to`

Conditionally required selector or enforcement fields:

- `interaction_modes`
- `environment_types`
- `requires_remote_execution`
- `requires_privilege_escalation`
- `requires_credentials`
- `requires_external_transfer`
- `is_long_running`
- `is_destructive_cleanup`
- `allowed_in_full_auto`
- `refusal_reason`
- `required_audit_fields`
- `notes`

Locked starter `action_classification` values:

- `read_only`
- `state_changing`
- `sensitive`
- `destructive`

Locked rules:

- keep confirmation policy declarative and artifact-backed rather than hard-coding mode-specific checks in command handlers;
- selectors may be combined, but the matrix must stay readable enough that an operator can explain why a confirmation was required or refused;
- refusal-bearing rules must state why the action is refused rather than silently falling through;
- audit-required fields in the matrix must stay compatible with `decision.actor_ref_requirement` and the event/evidence contracts already locked elsewhere.

## Relationship To Execution Defaults

These artifact shapes are locked here, while the concrete v1 execution defaults that populate them are locked in:

- `04_contracts/environment_and_safety_execution_plan.md`
- `06_standards/operator_modes_and_safety_standard.md`
- `06_standards/evidence_provenance_and_audit_standard.md`
