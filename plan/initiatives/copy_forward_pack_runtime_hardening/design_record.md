# Copy-Forward Pack Runtime Hardening Design Record

## Summary
Hardens reusable core for copied-core host scenarios by discovering unbootstrapped hosted packs from manifests, structuring stale-registry failures, and keeping current shared workspace contracts explicit.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/copy_forward_pack_runtime_hardening/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Runtime Design
### 1. Effective hosted-pack visibility
- Keep the authored `pack_registry.json` artifact unchanged as the persisted shared inventory surface.
- Add a reusable runtime helper that builds an effective hosted-pack view from:
  - authored registry entries that remain valid in the current repository
  - discovered hosted-pack manifests found through the existing pack-settings discovery rules
- Synthesize runtime-only entries for discovered packs when they are not already represented by a valid authored registry entry.
- Prefer authored entries when authored metadata is valid for the current repository.

### 2. Bootstrap-mode discovery rules
- Discovery markers remain `.wt/manifests/pack_settings.json` and adjacent `.wt/manifests/pack_runtime_manifest.json`.
- First-party/root pack roots such as `<pack>/` stay supported.
- Nested hosted-pack roots such as `packs/<slug>/` stay supported.
- Discovery remains deterministic and path-based rather than donor-name-based.

### 3. Structured stale-registry behavior
- When an authored registry entry points to missing manifests, host pack commands should return structured command errors rather than propagate raw `ArtifactLoadError` tracebacks.
- Selected pack namespace discovery should degrade to either:
  - a discovered valid pack namespace when a matching manifest-driven pack exists
  - an unavailable or error state that still preserves structured host behavior

### 4. Import strategy
- The preferred steady-state import path remains the shared `core/python` workspace registration.
- Add a bounded bootstrap-mode import fallback for hosted-pack integrations so copied-core host inspection can load a pack whose declared `python_root` exists even when the consuming repository has not yet rewritten `core/python/pyproject.toml`.
- Keep this fallback narrow and manifest-scoped. It must not become an unbounded repo-wide path mutation helper.

### 5. Validation posture
- Pack-contract validation remains fail-closed and should still surface missing authored registry or shared workspace registration when those are part of the steady-state contract.
- The improvement here is better structured behavior and manifest-driven discoverability, not silent acceptance of incomplete bootstrap.

## Affected Surfaces
- `core/python/src/watchtower_core/control_plane/**`
- `core/python/src/watchtower_core/pack_integration/**`
- `core/python/src/watchtower_host/cli/**`
- `core/python/tests/unit/**`
- `core/python/tests/integration/**`
- `core/docs/standards/**`
- `core/docs/references/**`
- `core/python/README.md`

## Evidence Strategy
- Add regression tests that simulate a consuming repository with copied donor core, a valid first-party/root pack, stale donor authored pack metadata, and no local shared workspace rewrite.
- Validate that pack commands and selected namespace discovery behave structurally in that scenario.
- Re-run the existing pack-runtime and pack-command suites to protect the current internal `plan` steady state.
