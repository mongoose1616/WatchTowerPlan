# Phase 6: Build Environment Adapters And Safety Controls

## Purpose

Define how the pack operates across local, SSH, VPN-reachable, and airgapped environments while enforcing offensive-security safety, confirmation, provenance, and audit rules.

## In-Scope Surfaces

- environment adapters
- operating modes
- autonomy policy
- command safety taxonomy
- confirmation gates
- provenance and audit requirements
- refusal and stop conditions

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- environment context record
- session state record
- `offensive_security/.wt/ledgers/transfers/<transfer_id>.json`
- `offensive_security/.wt/ledgers/retention_actions/<action_id>.json`
- `offensive_security/.wt/policies/safety_confirmation_matrix.json`
- shared adapter interface for `local`, `vpn_reachable`, `ssh`, and `airgapped`
- interaction-mode overlay values for `shared_workspace`, `guided_user_execution`, `delegated_agent_execution`, `airgapped_exchange`, `observer_review`, `async_handoff`, and `pairing`
- airgapped transfer protocol and provenance notes
- command safety taxonomy and enforcement matrix
- mode/autonomy transition logging in the event stream
- operator-facing safety guide and standards

## Dependencies

- Phase 2 environment/session/discrepancy schemas
- Phase 3 runtime hooks and workflow docs
- Phase 4 artifact and event-stream model

## Upstream Assumptions

- environment adapters stay pack-owned
- shared release/validation discipline can be reused, but offensive-security admissibility remains pack policy

## Validation And Acceptance Criteria

- local, SSH, VPN, and airgapped modes are all addressed explicitly
- `note_taker`, `assistant`, `teacher`, and `full_auto` mode behaviors are distinguished clearly
- guidance-only remains the baseline in local and remote contexts until stronger autonomy is explicitly enabled
- session state distinguishes requested mode from effective mode and records meaningful mode changes in both machine and visible surfaces
- airgapped handling defines re-paste behavior for malformed structured output
- full-auto observability shows planned commands, concise execution summaries, grouped checkpoints, and a live journal while still pausing at risk boundaries
- higher-risk actions require explicit confirmation
- the pack locks one shared adapter protocol with `describe_context`, `check_capability`, `execute_command`, `capture_artifact`, `stage_transfer`, and `record_provenance`, with `airgapped` omitting live execution
- the safety matrix explicitly covers confirmation for mode changes, credential use, privilege escalation, remote state changes, long-running automation, external transfer, and destructive cleanup
- destructive unattended `full_auto` is refused, and full-auto refusal conditions also cover scope ambiguity, insufficient environment context, provenance gaps, repeated failures, and stale state
- every claims-bearing airgapped transfer requires a transfer manifest with operator, systems, purpose, timestamp, artifact refs, and checksum when practical; imported material stays quarantined at lower trust until manually verified
- actor refs are mandatory for approvals, confirmations, promotion approvals, closeout approvals or finalization, remote or delegated execution, airgapped transfer, and destructive or retention actions
- provenance and audit expectations are explicit enough for later validator and workflow-gate implementation
- lifecycle and safety policy artifact shapes align with `04_contracts/lifecycle_and_safety_policy_contracts_plan.md`

## Risks And Unresolved Questions

- airgapped workflows can become ambiguous if operators bypass the structured transfer manifest and re-paste rules

## Exit Criteria

- the package contains a concrete environment and safety model that can be implemented without reinterpreting policy intent
