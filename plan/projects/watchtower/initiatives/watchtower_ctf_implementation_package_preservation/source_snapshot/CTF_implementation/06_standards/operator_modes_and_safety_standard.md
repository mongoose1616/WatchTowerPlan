# Operator Modes And Safety Standard

## Purpose

Define allowed operating modes, autonomy expectations, confirmation gates, and refusal behavior for the offensive-security pack.

## Rules

- user-visible modes are `note_taker`, `assistant`, `teacher`, and `full_auto`;
- `interaction_mode` is a separate overlay vocabulary with `shared_workspace`, `guided_user_execution`, `delegated_agent_execution`, `airgapped_exchange`, `observer_review`, `async_handoff`, and `pairing`;
- assistant and note-taker remain non-executing by default;
- local, SSH, and VPN-reachable contexts all keep guidance-only as the baseline until the operator explicitly selects a stronger autonomy level;
- `teacher` is a distinct explanatory operating mode, not merely an overlay on `assistant`, and it must not weaken the same safety or provenance requirements that apply in other modes;
- note-taker remains a passive structured recorder and does not infer reusable candidates by default during active work;
- session state must distinguish `requested_mode` from `effective_mode` when safety rules or environment constraints narrow what the system may actually do;
- every mode or autonomy change must be explicitly confirmed, written to the event stream, and mirrored into visible session context on meaningful changes;
- stronger execution requires explicit confirmation and must be auditable;
- environment adapters remain pack-owned;
- all adapters expose `describe_context`, `check_capability`, `execute_command`, `capture_artifact`, `stage_transfer`, and `record_provenance`, with `airgapped` omitting live execution;
- local, SSH, VPN-reachable, and airgapped contexts all require explicit mode and provenance handling;
- airgapped work uses a structured exchange protocol; malformed pasted output must trigger re-paste before machine-state updates;
- every claims-bearing manual transfer must record transfer id, direction, checksum when practical, operator, source system, destination system, timestamp, purpose, and artifact refs;
- full-auto must show planned commands before execution, concise results after execution, grouped checkpoints, and a live journal, and must pause at risk or scope boundaries;
- full-auto observability detail remains operator-selectable rather than fixed;
- confirmation is mandatory for credential use, privilege escalation, remote state-changing actions, long-running automation, external transfer, destructive cleanup, and every mode or autonomy change;
- destructive unattended `full_auto` is refused outright;
- full-auto must also refuse scope-ambiguous actions, actions exceeding the active safety class, actions with insufficient environment context, claims-bearing actions with unresolved provenance gaps, and repeated-failure situations where notes or state are too stale;
- actor refs are mandatory for confirmations, approvals, promotion approvals, closeout approvals or finalization, remote or delegated execution, airgapped transfers, and destructive or retention actions, with only narrow low-risk note-only and derived-refresh exceptions;
- prohibited or out-of-scope actions must fail closed rather than degrade silently.

## Acceptance

- the package states exactly when confirmation is mandatory, when refusal is required, how transfers and actor refs are recorded, and how mode transitions are recorded.
