# Domain Pack Externalization and Portability Proof Design Record

## Summary
Proves that plan and future domain packs can be copied out with only packaging and path updates while reusable core and host integration remain stable.

## Architecture Decision
- Keep the three-layer runtime contract unchanged:
  - `watchtower_core` owns reusable contracts, loaders, validators, and pack-agnostic helpers.
  - `watchtower_host` owns CLI composition and hosted-pack dispatch.
  - `watchtower_<pack>` owns pack-native orchestration and may depend only on `watchtower_core`.
- Treat a domain pack as a portable capsule made of:
  - `<pack>/.wt/**`
  - `<pack>/docs/**`
  - `<pack>/workflows/**`
  - `<pack>/python/**`
  - any explicit domain roots declared by pack settings and the runtime manifest
- Fail closed on portability drift through reusable-core validation rather than ad hoc repo-local assumptions.

## Proof Strategy
- Use `plan` as the first proof pack and validate that its pack-local roots, manifests, and Python package can be exercised through host-owned seams without hidden repository assumptions.
- Add a stronger second-pack fixture so multi-pack registration, validation, and namespaced host dispatch are exercised through the same contracts.
- Use WatchTowerOversight as a reference shape for pack-local docs, workflows, and manifest layout where it strengthens the generic contract without importing oversight-specific behavior into core.

## Key Constraints
- Copy-out should require packaging and path updates only, not Python code rewrites.
- Missing expected install wiring or missing declared pack surfaces should fail deterministically in reusable-core validation.
- Pack-local docs and workflows must remain pack-owned; reusable guidance belongs in `core/docs/**` and `core/workflows/**`.
- Generic reusable helpers found during this proof should move back into core rather than proliferating plan-specific forks.

## Readiness Boundary
- The initiative package is machine-first and local to `plan/initiatives/domain_pack_externalization_portability_proof/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
