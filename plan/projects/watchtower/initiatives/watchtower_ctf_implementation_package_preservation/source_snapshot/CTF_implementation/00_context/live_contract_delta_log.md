# Live Contract Delta Log

## Purpose

Record where the live repo state on `2026-03-26` differs from Step 1 workbook assumptions so the planning package stays aligned to current contract.

## Delta Register

| Delta ID | Earlier Assumption | Live Contract / Proof | Disposition |
|---|---|---|---|
| `delta.slug.current_compatible` | `STEP1_FINAL_v3.md` recommends underscore-safe identifiers such as `pack_slug = offensive_security` | live scaffold proof passes with `pack_slug = offensivesecurity`, `pack_id = pack.offensivesecurity`, `command_namespace = offsec` | keep scaffold-spec runnable identity as baseline |
| `delta.actor_registry.present` | v3 treats `actor_registry` as review / extension territory | shared core now ships `actor_registry.json` and typed schema plus loader support | adopt in Phase 2 pack machine contract |
| `delta.governance_surface_map.present` | older workbook phases treat governed surface map as future extension | shared core now ships `governance_surface_map.json` and typed schema plus resolver support | adopt in Phase 2 pack machine contract |
| `delta.path_status_registries.present` | older workbook treats several governance surfaces as pack-only future work | shared core now ships `path_pattern_registry.json` and `status_registry.json` | reuse shared surfaces and extend pack-local registries only where necessary |
| `delta.status_subset.current_compatible` | Step 1 often used challenge-local `solved` and `unresolved` semantics directly in artifact lifecycle sketches | live shared `status_registry.json` uses current-compatible global values such as `active`, `blocked`, `completed`, `closed`, `in_review`, and `needs_review`, but not `solved` or `unresolved` | adapt challenge/session `status` subsets to shared-core values and carry solve/unresolved semantics in `closeout_record.outcome` instead |
| `delta.workflow_catalog.not_required` | older workbook repeatedly assumes a future stronger `workflow_catalog` model | current contract still centers routing table + workflow metadata registry + workflow/route indexes | lock `workflow_catalog` as a post-v1 deferral, not a baseline requirement |
| `delta.domain_packs.retired` | early docs use `domain_packs/offensive_security/...` | current shared docs and scaffold use first-party root pack `offensive_security/` | reject retired topology |
| `delta.challenge_path.v1_placeholder_segments` | later Step 1 refinements collapse missing `platform` or `event` path segments entirely | the v1 package keeps the scaffold-compatible fixed root `offensive_security/ctf/<platform>/<event>/<challenge>/` and uses stable placeholders such as `unknown_platform` and `unknown_event` instead | keep placeholder segments in v1 and defer optional-segment collapse beyond v1 |
| `delta.target_repo.empty` | older docs assume a fuller target repo context | `/home/j/WatchTower` is empty except `.git` | plan export/bootstrap as first real content landing |

## Required Follow-Through

- Each affected phase doc must reference the relevant delta.
- `step1_traceability_matrix.md` and `step1_traceability.json` must carry `live_contract_delta` values where applicable.
- Any future package revision must update this log first if repo truth changes again.
