# Retention And Cleanup Policy Plan

## Purpose

Lock the v1 retention, archive, cleanup, and post-close authority rules for challenge-local and pack-level offensive-security artifacts.

## Step 1 Basis

- `STEP1_FINAL.md`
  - `Q02`: active challenge-local event stream authority with pack-level derived views during active work
  - `Q04`: freeze challenge-local `.wt_local/` in place after closeout instead of deleting it
  - `Q05`: keep `challenge.md`, `notes.md`, `solution/`, `recap.md`, `closeout_record`, and extraction output as the baseline closeout set, then reconcile solved-only `solution/` behavior with later workflow detail
  - `Q27`: require `solution/` for solved closeout and do not fabricate it for unsolved outcomes
  - `Q28`: require `recap.md` for solved and blocked closeout and treat recap as a governed closeout artifact
- `STEP1_FINAL_v2.md`
  - `R48`: exact canonical challenge-local and pack-level hidden paths
  - transition guidance: `closeout_record: active -> archived` and `extraction_output: active -> archived | superseded`
- `STEP1_FINAL_v3.md`
  - challenge-specific authority, closeout, and taxonomy remain pack-owned and must not be assumed from shared core

## Locked V1 Policy

- keep each challenge rooted permanently at its canonical path under `offensive_security/ctf/.../`;
- keep `challenge.md`, `notes.md`, `solution/`, and `recap.md` at the challenge root after closeout;
- keep challenge-local `.wt_local/` authoritative during active work only;
- freeze `.wt_local/` in place on closeout and treat it as historical machine state, not as the normal active authority surface;
- keep pack-level `.wt/` indexes, registries, and rendered views available after closeout as the durable pack-level lookup surfaces;
- require `challenge.md` and `notes.md` for every v1 closeout outcome;
- require `solution/` only when `closeout_record.outcome = solved`, and do not fabricate a final solution artifact for `blocked_closeout`, `unresolved`, or `closed_without_attempt`;
- require `recap.md` for `solved`, `blocked_closeout`, and `unresolved`; allow omission only for `closed_without_attempt`;
- treat `archived` as a logical lifecycle state in v1, not as an automatic path relocation event;
- do not support destructive challenge deletion in v1;
- allow reactivation of frozen `.wt_local/` only through an explicit reopen or `needs_review` workflow.

## Retained Surface Matrix

| Family | Canonical Path | Active-Phase Role | Post-Close Role | Visibility Rule |
|---|---|---|---|---|
| `challenge` | `offensive_security/ctf/<platform>/<event>/<challenge>/challenge.md` | durable human intake and source surface | retained durable closeout surface | user-visible |
| `notes` | `offensive_security/ctf/<platform>/<event>/<challenge>/notes.md` | active human working surface | retained working-history surface | user-visible |
| `solution` | `offensive_security/ctf/<platform>/<event>/<challenge>/solution/` | optional until solve/closeout | required solved-closeout evidence surface; omitted for blocked, unresolved, or no-attempt closeout | user-visible |
| `recap` | `offensive_security/ctf/<platform>/<event>/<challenge>/recap.md` | optional until closeout drafting starts | required closeout summary surface for solved, blocked, and unresolved outcomes; optional only for `closed_without_attempt` | user-visible |
| `raw_artifact_capture` | `offensive_security/ctf/<platform>/<event>/<challenge>/artifacts/<captured_file>` | active supporting raw capture surface | retained supporting evidence capture unless explicit governed cleanup occurs | user-visible |
| `event_stream` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson` | authoritative challenge-local event history | frozen authoritative history stream | hidden |
| `session_state` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json` | authoritative current session state | frozen historical session state unless reopened | hidden |
| `environment_context` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json` | authoritative current execution-context record | frozen historical environment snapshot unless reopened | hidden |
| `evidence_artifact` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/evidence/artifacts.json` | authoritative metadata, trust, and provenance inventory for evidence captures | retained hidden evidence inventory even when supporting raw captures are pruned or transferred | hidden |
| `closeout_record` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/closeout_record.json` | created during closeout | retained historical machine closeout summary with logical `archived` state | hidden |
| `extraction_output` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/extractions/<extraction_id>.json` | created during extraction and promotion review | retained hidden machine extraction history with `archived` or `superseded` lifecycle | hidden from active rendered views |
| `discrepancy_record` | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/discrepancies/<discrepancy_id>.json` | active discrepancy and drift management | retained historical discrepancy record; unresolved discrepancies with active governance limits remain visible through pack indexes | hidden |
| `artifact_index` | `offensive_security/.wt/indexes/artifact_index.json` | broad pack-level machine catalog | durable pack-level lookup and path-resolution surface | mixed |
| `challenge_index` | `offensive_security/.wt/indexes/challenge_index.json` | active challenge-state lookup | durable pack-level challenge lookup after closeout | mixed |
| `blocker_index` | `offensive_security/.wt/indexes/blocker_index.json` | active blocker lookup | historical plus current blocker lookup | mixed |
| `knowledge_index` | `offensive_security/.wt/indexes/knowledge_index.json` | optional until knowledge phase lands | durable promoted and candidate knowledge lookup | mixed |
| rendered views | `offensive_security/offensivesecurity_overview.md` and `offensive_security/tracking/*.md` | human-readable navigation and tracking | retained derived summaries of current and closed state | user-visible, derived |

## Locked Closeout Admissibility Rule

- closeout finalization requires `challenge.md`, `notes.md`, a valid `closeout_record`, a valid extraction output, and a passing closeout validation suite;
- if `closeout_record.outcome = solved`, require both `solution/` and `recap.md`;
- if `closeout_record.outcome = blocked_closeout` or `unresolved`, require `recap.md` and do not require or auto-fabricate `solution/`;
- if `closeout_record.outcome = closed_without_attempt`, allow omission of both `solution/` and `recap.md`, but require `closeout_record.summary` and `closeout_reason` to explain the no-attempt closure;
- any active discrepancy carrying `no_closeout`, or any unresolved discrepancy that still sets `forces_needs_review`, blocks final closeout until resolved or explicitly exceptioned through the governed discrepancy workflow.

## Cleanup, Redaction, And Transfer Exception Rule

- v1 allows post-closeout redaction, pruning of non-authoritative captures, and manual transfer only as explicit operator actions;
- these actions must never remove the ability to explain outcome, closeout status, and promotion provenance;
- every such action must write a governed ledger record to `offensive_security/.wt/ledgers/retention_actions/<action_id>.json`;
- when the action is an offline or cross-system transfer, also write the transfer record required by the airgapped-transfer contract.

## Planned Retention Action Ledger Shape

Required fields:

- `action_id`
- `challenge_id`
- `action_type`
- `acted_at_utc`
- `actor_id`
- `reason`
- `affected_artifact_ids[]`
- `from_paths[]`
- `to_paths[]`

Optional fields:

- `redaction_summary`
- `related_transfer_id`
- `notes`

Recommended `action_type` starter set:

- `redact_sensitive_output`
- `prune_non_authoritative_capture`
- `transfer_copy`
- `supersede_extraction_output`

## Rendered Visibility Rule

- active rendered views should not enumerate frozen `.wt_local/` paths directly;
- active rendered views should not list archived extraction outputs by default;
- rendered views may summarize solved, closed, blocked, and archived challenge state, but they should stay compact and navigational;
- detailed field-level lookup remains on the machine indexes and challenge-local records, not on rendered markdown summaries.

## Deferred Extension Rule

- do not add `offensive_security/.wt/registries/retention_policy_registry.json` in v1;
- if a future release needs physical archive relocation, destructive deletion, or purge eligibility, add:
  - an explicit `retention_policy_registry`
  - dedicated archive, cleanup, and delete workflows
  - surviving deletion ledgers and validation gates in the same change set
