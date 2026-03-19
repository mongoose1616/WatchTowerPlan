# Requirements And Decisions Adherence Remediation Design Record

## Summary
Retire the root docs tree, finish the initiative-package hard cutover, and restore rich machine-backed documentation surfaces.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Chosen Design
- Make `core/docs/**` and `plan/docs/**` the only active documentation roots.
- Re-root governed documentation families by ownership rather than by old root location:
  - shared command docs, references, templates, and shared or core-owned standards live under `core/docs/**`
  - durable plan-domain governance and promoted guidance live under `plan/docs/**`
  - foundations remain the only mandatory mirrored family
- Keep machine indexes compact and move human richness into rendered Markdown and authored doc structure rather than expanding index payloads.
- Treat the six-section `plan_overview.md` template and section schema as authoritative, then align the renderer, rendered-surface registry, tests, and fail-closed validation around them.
- Replace the stale initiative projection phase vocabulary with `capture`, `execution`, `closeout`, and `closed`.
- Retire the remaining pre-cutover planning-document semantic layer instead of renaming it in place.

## Authority Boundaries
- Root `docs/**` is removed from active authority.
- `core/docs/**` owns shared and core-specific human guidance.
- `plan/docs/**` owns durable plan-domain guidance and promoted outputs from live initiative work.
- `plan/.wt/**` remains the machine authority for live initiative, task, tracker, and aggregate-index state.
- `plan/tracking/**` and `plan/plan_overview.md` remain derived human surfaces built from machine authority.

## Applied Implications
- Command docs, standards, references, templates, validators, indexes, README navigation, authority maps, query help, and tests must move in the same change sets as the root move.
- Workflow routes and metadata must stop advertising retired planning terminology because those names influence both routing and user-visible command discovery.
- Runtime helpers that still assume `docs/**` roots or retired planning-document families must move or be removed as part of the cutover, not left behind as dead compatibility code.
- The implementation must preserve rich human tables and navigation patterns from `main` only where they fit the new roots and machine-backed plan model.

## Risks
- This cutover touches code, schemas, registries, generated indexes, tests, and many linked Markdown surfaces at once, so stale references are the main regression risk.
- The command, standard, and reference indexes are path-sensitive; moving doc roots without synchronized registry and loader updates will break discovery.
- Retired terminology still appears in many help strings and standards, so residue is easy to miss without explicit grep-based guards and assessment passes.
