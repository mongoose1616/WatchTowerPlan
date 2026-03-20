# Pack Domain Hardcoding Remediation Decision Notes

## Summary
Record the implementation decisions and additional gap findings discovered while validating the pack-driven hard-cutover.

## Decisions
- Shared-core pack resolution must treat the active pack settings surface as an abstract selector, not a hardcoded `plan/.wt/...` path. The loader now resolves an explicit active pack, then a discovered repo-local default pack, and falls back to the shared-core pack only when no repo-local pack exists.
- Pack-owned runtime roots remain valid under the current explicit `plan_runtime` namespace for this tranche, but reusable helper layers in `control_plane`, `validation`, and sync harness entrypoints may only consume concrete roots through pack settings and `PackWorkspacePaths`. The clean-endstate mandate is stronger: reusable core stays in `watchtower_core`, while remaining plan-domain Python moves behind a plan-owned boundary under `plan/**`.
- Assessment pass one found residual active-schema allowance for the retired root `docs/` family. Those regex allowances are removed and guarded so the docs-root retirement fails closed instead of silently drifting back.
- The main-branch comparison did not justify reviving the old docs-backed planning families. The current `plan/tracking/**` tables already preserve the useful browseable summary/detail pattern, so the retained design is to keep machine indexes compact and human trackers table-rich without reintroducing legacy authority surfaces.
