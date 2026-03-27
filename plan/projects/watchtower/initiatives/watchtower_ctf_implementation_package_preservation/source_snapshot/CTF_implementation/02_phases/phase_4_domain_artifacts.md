# Phase 4: Build The Domain Artifacts

## Purpose

Define the concrete CTF artifact model for active work, closeout, ledgers, discrepancy handling, and human-readable rendered summaries.

## In-Scope Surfaces

- `challenge.md`
- `notes.md`
- `solution/`
- `recap.md`
- challenge-local `.wt_local`
- event streams and discrepancy ledgers
- environment/session records
- rendered human views

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- `offensive_security/ctf/<platform>/<event>/<challenge>/challenge.md`
- `offensive_security/ctf/<platform>/<event>/<challenge>/notes.md`
- `offensive_security/ctf/<platform>/<event>/<challenge>/solution/`
- `offensive_security/ctf/<platform>/<event>/<challenge>/recap.md`
- `offensive_security/ctf/<platform>/<event>/<challenge>/artifacts/`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/challenge_metadata.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/notes_metadata.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/evidence/artifacts.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/closeout_record.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/extractions/<extraction_id>.json`
- `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/discrepancies/<discrepancy_id>.json`
- pack-level `.wt/` indexes and summaries as durable or derived pack views
- event stream, blocker/discrepancy records, closeout record, extraction output, environment context, and session state
- retention and cleanup policy or ledger surfaces if closeout supports post-closeout pruning, redaction, or transfer
- `offensive_security/.wt/ledgers/retention_actions/<action_id>.json` for any post-close redaction, pruning, or transfer action

## Dependencies

- Phase 2 schema definitions
- Phase 3 doc semantics, routing, and runtime hooks

## Upstream Assumptions

- challenge-local `.wt_local` is pack-owned convention, not a shared-core concept
- markdown remains directly editable with machine-managed metadata and reconciliation

## Validation And Acceptance Criteria

- `challenge.md` preserves source challenge text while allowing machine front matter
- `challenge.md` front matter may be filled at the next workflow opportunity without rewriting the locked challenge body
- `notes.md` remains the active working surface
- `notes.md` uses one canonical structure with optional sections and mode-specific overlays
- agent edits to `notes.md` are append-preserving and user ad hoc sections are normalized or flagged only before closeout
- closeout finalization requires `challenge.md`, `notes.md`, `closeout_record`, extraction output, a passing closeout validation suite, and no active discrepancy carrying `no_closeout`
- `solution/` is required only for `solved` outcomes and must not be fabricated for `blocked_closeout`, `unresolved`, or `closed_without_attempt`
- `recap.md` is required for `solved`, `blocked_closeout`, and `unresolved`; it may be omitted only for `closed_without_attempt`
- evidence capture keeps raw supporting files under `artifacts/` and governed evidence records in `.wt_local/evidence/artifacts.json`
- command capture always records metadata and summaries; raw or large stdout or stderr stays in artifact captures, and only clearly player-owned material is redacted from routine notes, events, query output, and rendered views
- `closeout_record`, `evidence_artifact`, and `extraction_output` follow the exact field contracts in `04_contracts/artifact_payload_contracts_plan.md`
- `challenge_metadata`, `notes_metadata`, `session_state`, `event_stream`, `artifact_index`, `environment_context`, and `discrepancy_record` follow the exact contracts in `04_contracts/state_and_index_contracts_plan.md`
- challenge-local active state and pack-level durable views are distinguished cleanly
- any retention or cleanup action after closeout preserves a governed surviving record
- closeout freezes `.wt_local/` in place instead of relocating or deleting the challenge root

## Risks And Unresolved Questions

- the reconciliation boundary between markdown edits and hidden machine state must stay predictable
- rendered views can drift if direct-edit rules are under-specified

## Exit Criteria

- the package defines the full artifact and ledger model for one challenge lifecycle
