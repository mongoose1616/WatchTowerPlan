# WatchTower CTF Phase Test Matrix

## Summary

This support surface maps each preserved phase to its must-pass validators, smoke tests, and proof artifacts. Use it together with `phase_output_manifest.md` and `phase_closeout_checklists.md` before claiming a phase is complete.

## Matrix

| Phase | Must-Pass Validation | Smoke / Proof Test | Required Proof Artifacts |
|---|---|---|---|
| `phase.0` | acceptance-contract validation, validation-evidence validation, acceptance reconciliation, `plan query trace`, `plan query coordination` | confirm one real ready task and no hidden baseline contradiction | current acceptance contract, durable evidence record, coordination/readiness query output |
| `phase.1` | `pack scaffold`, `pack bootstrap`, `pack validate`, `validate all` on the recipient repo | first scaffolded `offensive_security/` root exists with required starter roots and no starter workflow metadata | scaffold output, bootstrap output, validation output, starter-surface existence proof |
| `phase.2` | schema validation for every new schema, artifact validation for every new registry/policy surface, `pack validate`, `validate all` | starter registries and core machine records are loadable without manual schema guesswork | validated schema set, validated registry set, machine-surface specimen alignment notes |
| `phase.3` | `pack validate`, `validate all`, command-doc integrity, workflow-doc integrity, unit tests, CLI smoke tests | exact thin vertical slice in `vertical_slice_proof_spec.md` plus first real query and sync behavior | vertical-slice output, query output for `challenges` and `artifacts`, test run output |
| `phase.4` | artifact validation for challenge-local records, closeout validation suite, `pack validate`, `validate all` | one challenge root runs from intake through closeout with discrepancy enforcement | closeout record, extraction output, evidence inventory, discrepancy proof |
| `phase.5` | artifact validation for knowledge families and promotion policy surfaces, `pack validate`, `validate all` | candidate extraction, review gating, promotion, and retrieval all work on one real example set | candidate set, review result, promoted artifact proof, retrieval output |
| `phase.6` | artifact validation for safety and adapter policy surfaces, `pack validate`, `validate all` | every environment mode proves confirmations, refusals, and actor/provenance behavior | safety confirmation matrix proof, adapter proof, mode-state proof |
| `phase.7` | `pack validate`, `validate all`, changed-schema validation if applicable, `release check` | staged export and bootstrap rehearsal complete without donor-only assumptions | staged export bundle, release-check output, portability rehearsal notes |

## Immediate Test Expectations By Phase

### `phase.2`

- Validate every new schema individually before relying on pack-wide validation.
- Validate every new registry or policy artifact individually before relying on pack-wide validation.
- Confirm the first artifact specimens and machine-surface index are still representative of the implemented shapes.

### `phase.3`

- Add unit tests and CLI smoke tests immediately after the first vertical slice works.
- Do not defer the first smoke tests to a later cleanup phase.
- Keep query and sync smoke proof coupled to real command-doc pages.

### `phase.4`

- Closeout proof is incomplete without discrepancy gating.
- Evidence proof is incomplete if raw files exist without governed inventory rows.

### `phase.5`

- Retrieval proof is incomplete unless accepted artifacts win by default and candidate visibility requires explicit opt-in.
- Promotion proof is incomplete unless provenance fields and review workflow are visible.

### `phase.6`

- Safety proof is incomplete unless the refusal path is tested, not only the happy path.
- Full-auto claims are incomplete without observability proof.

### `phase.7`

- Portability proof is incomplete if it depends on the donor worktree instead of staged export outputs.
- Release proof is incomplete if the handoff mode is not named explicitly.

## Failure Heuristics

- If a phase only passes `pack validate` but not its specific smoke proof, the phase is not done.
- If a phase passes tests but leaves the proof artifacts undocumented, the phase is not handoff-ready.
- If a later phase test is used to justify skipping an earlier phase proof, the dependency chain is being weakened and should be corrected.
