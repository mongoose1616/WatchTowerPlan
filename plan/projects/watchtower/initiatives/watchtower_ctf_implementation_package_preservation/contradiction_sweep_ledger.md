# WatchTower CTF Contradiction Sweep Ledger

## Summary

This support surface records the major tensions that were already checked and reconciled while hardening the initiative. It exists so later engineers do not have to rediscover the same contradictions across the preserved mirror, canonical docs, live task state, and donor-pack precedent.

## Use Rules

- Treat this ledger as a resolved-contradictions companion to `decision_notes.md`, not as a second decision register.
- If a listed resolution must change, record a new live-contract delta first and then update the affected canonical docs, tasks, acceptance, and evidence surfaces in the same change set.
- If a topic is not listed here, do not assume it was unresolved; confirm against the canonical docs and the mirror.

## Resolved Tensions

| Sweep ID | Tension | Resolved Baseline | Governing Surfaces |
|---|---|---|---|
| `sweep.identity.current_compatible_slug` | workbook-era slug guidance drifted from the scaffold proof that actually works today | keep `pack_slug = offensivesecurity`, `pack_id = pack.offensivesecurity`, and `command_namespace = offsec` until upstream slug handling changes through an explicit delta | `initiative_brief.md`, `decision_notes.md`, `implementation_slice.md` |
| `sweep.raw_json.validator_collision` | the donor package includes JSON companions that would collide with initiative validators if mirrored raw | keep mirrored donor JSON byte-identical but stored as `.json.raw` inside `source_snapshot/CTF_implementation/` | `design_record.md`, `source_capture_notes.md`, `source_sha256.tsv` |
| `sweep.event_stream_envelope` | a preserved decision row used shorthand that implied stricter required event fields than the field-level state contract | implementation follows the field-level state contract with `event_id`, `event_type`, `timestamp_utc`, and `challenge_id` required, while the shorthand row remains historical source evidence only | `decision_notes.md`, `implementation_slice.md` |
| `sweep.domain_packs_topology` | older source material referenced retired `domain_packs/**` topology | keep first-party pack root `offensive_security/` and reject retired topology | `decision_notes.md`, `implementation_slice.md` |
| `sweep.docs_root_authority` | earlier assumptions blurred pack-owned docs with generic `/docs/**` authority | keep offsec docs pack-owned under `offensive_security/docs/` and route command or workflow discovery through the preserved machine and human surfaces | `initiative_brief.md`, `implementation_slice.md`, `starter_surface_blueprint.md` |
| `sweep.bootstrap_placeholder_vs_real_handoff` | the bootstrapped initiative originally exposed a placeholder task instead of the real implementation chain | keep the same initiative, retire the placeholder entrypoint, and publish the phase-aligned task graph as the real handoff surface | `implementation_slice.md`, `.wt/tasks/**/task.json`, `coordination_index.json` |
| `sweep.capture_label_vs_execution_handoff` | repo lifecycle vocabulary still shows `current_phase = capture` even when an initiative is execution-ready | accept the lifecycle label as-is and use the ready Phase 0 task, trace joins, and coordination next-action as the true execution-facing handoff | `design_record.md`, `coordination_index.json`, `readiness_index.json` |
| `sweep.placeholder_path_segments` | later workbook refinements suggested collapsing missing `platform` or `event` path segments entirely | keep fixed challenge paths with governed placeholder segments such as `unknown_platform` and `unknown_event` in v1 | `initiative_brief.md`, `decision_notes.md`, `implementation_slice.md` |
| `sweep.support_docs_vs_authority` | more engineer-support material could have created a second planning authority | keep the four canonical docs plus live task state authoritative, and keep support docs explicitly subordinate | `README.md`, `design_record.md`, `implementation_slice.md` |

## Still Open Only If Triggered

Items that remain intentionally deferred are tracked in `conditional_revisit_queue.md`. If an engineer feels pressure to reopen a resolved sweep, check that queue first and verify that the trigger condition actually fired.
