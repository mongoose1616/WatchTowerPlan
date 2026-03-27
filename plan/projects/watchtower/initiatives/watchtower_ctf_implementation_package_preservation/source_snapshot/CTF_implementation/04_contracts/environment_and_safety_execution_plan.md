# Environment And Safety Execution Plan

## Purpose

Lock the adapter, confirmation, transfer, and actor-reference policies that govern Phase 6 execution so the offensive-security pack can be implemented without reopening safety posture questions.

## Step 1 Basis

- `STEP1_FINAL.md`
  - `Q08`: required v1 environment set
  - `Q09` and `Q10`: guidance-only baseline for local and remote work
  - `Q11`: structured airgapped exchange and re-paste behavior
  - `Q12` through `Q16`: user-visible modes, requested versus effective mode, confirmation, and observability
  - `Q68`: transfer provenance and trust downgrade
  - `Q69`: full-auto refusal conditions
  - `Q70`: minimum audit trail
- `STEP1_FINAL_v2.md`
  - `R29`: interaction-mode overlay vocabulary
  - `R87`: actor-ref validation posture
  - `R88`: actor bootstrap exception model
- reference guidance:
  - `WatchTowerPlan/core/docs/references/nist_sp_800_115_reference.md`
  - `WatchTowerOversight/core/docs/references/owasp_logging_cheat_sheet_reference.md`

## Environment Adapter Protocol

Planned runtime surface:

- `watchtower_offensivesecurity.environment.adapters`

Locked adapter ids:

- `local`
- `vpn_reachable`
- `ssh`
- `airgapped`

Locked shared adapter methods:

- `describe_context`
- `check_capability`
- `execute_command`
- `capture_artifact`
- `stage_transfer`
- `record_provenance`

Locked rules:

- keep one uniform adapter protocol across local, remote, and airgapped contexts rather than special-casing environment behavior in workflows;
- local, `vpn_reachable`, and `ssh` adapters remain guidance-only by default until the operator explicitly enables stronger autonomy;
- the `airgapped` adapter omits live `execute_command` and relies on staged exchange plus artifact-backed provenance;
- all adapters must return enough structured context to populate `environment_context`, session summaries, and event-stream references without re-parsing raw command output.

Locked starter `interaction_mode` values:

- `shared_workspace`
- `guided_user_execution`
- `delegated_agent_execution`
- `airgapped_exchange`
- `observer_review`
- `async_handoff`
- `pairing`

## Safety Confirmation Policy Values

Policy artifact:

- `offensive_security/.wt/policies/safety_confirmation_matrix.json`

Locked `action_classification` values:

- `read_only`
- `state_changing`
- `sensitive`
- `destructive`

Locked confirmation-required cases:

- every mode or autonomy change
- credential use
- privilege escalation
- remote state-changing actions
- long-running automation
- external transfers
- destructive cleanup or retention actions

Locked refusal rules:

- refuse destructive unattended `full_auto`;
- refuse execution when scope is ambiguous;
- refuse execution when the requested action exceeds the active safety class;
- refuse execution when environment context is insufficient for the proposed action;
- refuse execution when provenance gaps make the resulting claim or artifact unsafe to trust;
- refuse execution after repeated failures if notes or state are too stale to justify continued automation.

Locked rules:

- keep refusal-bearing entries explicit in the matrix rather than relying on undocumented code fallbacks;
- record required confirmations, refusals, and overrides in the event stream with actor refs when the event class requires them;
- keep sensitive-output handling aligned with the redaction rules already locked in `06_standards/evidence_provenance_and_audit_standard.md`.

## Airgapped Transfer Contract

Canonical ledger path:

- `offensive_security/.wt/ledgers/transfers/<transfer_id>.json`

Required fields:

- `transfer_id`
- `direction`
- `operator`
- `source_system`
- `destination_system`
- `timestamp_utc`
- `purpose`
- `artifact_refs`

Conditionally required fields:

- `sha256`
- `trust_state`
- `verification_status`
- `quarantine_reason`

Locked `direction` values:

- `import`
- `export`

Locked rules:

- record every manual or staged transfer, not only successful imports;
- store raw pasted or transferred claims-bearing material as artifact-backed evidence rather than inline note prose;
- imported or pasted claims-bearing material starts in a lower-trust or quarantined posture until it is manually verified or reproduced;
- when structured pasted output is malformed or partial, require re-paste before machine-state updates that depend on it;
- include transferred artifacts in `artifact_index` whenever the material is used for evidence, promotion, or closeout claims;
- capture checksums when practical and treat missing checksums as an explicit trust limitation rather than silently ignoring integrity evidence.

## Actor Reference Requirement

Locked actor-ref-required contexts:

- mode changes
- confirmations and overrides
- promotion approvals
- closeout approvals or finalization
- delegated or remote execution
- airgapped imports and exports
- destructive or retention actions

Locked contexts where actor refs may be omitted:

- low-risk note-only edits
- purely derived refresh work such as rendered-view regeneration
- machine-only index refresh events that do not represent a human decision or unsafe execution act

Locked rules:

- required actor fields must validate against shared `actor_registry` once bootstrap is complete;
- unresolved required actor refs are validation errors after bootstrap;
- the bootstrap exception remains intentionally narrow and should be removed as soon as minimal real actor entries exist;
- event, transfer, and approval surfaces must not silently downgrade required actor refs to optional fields.
