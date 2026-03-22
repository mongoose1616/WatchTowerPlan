# First-Party Root Pack Roots Implementation Slice

## Summary
Implement first-party root-pack discovery and default-pack resolution so copied repositories can host packs at <slug>/ without donor assumptions.

## Work Breakdown
- Add a shared path-oriented discovery helper for pack-settings surfaces that can enumerate direct root packs and `packs/*` pack roots in deterministic order.
- Update the control-plane loader fallback in `loader_pack_settings.py` so `default_pack_settings_path()` prefers the explicit registry default and uses the new deterministic discovery helper only when no usable default is declared.
- Update pack-root discovery helpers in `watchtower_core.pack_integration` to reuse the same deterministic pack-settings ordering instead of broad independent scans.
- Add targeted unit coverage for direct-root precedence, registry-default precedence, and mixed root-plus-`packs/*` repositories.
- Add or update pack-runtime and host-facing tests that use `plan` as the root-pack proof and confirm the changed discovery/defaulting behavior remains compatible with current host-pack flows.
- Refresh the pack-authoring or workspace docs only if the final runtime contract wording changes materially.

## Planned Change Set
- `core/python/src/watchtower_core/control_plane/loader_pack_settings.py`
- `core/python/src/watchtower_core/pack_integration/`
- `core/python/tests/unit/test_control_plane_loader_pack_settings.py`
- `core/python/tests/unit/test_pack_integration_runtime.py`
- `core/python/tests/unit/test_cli_pack_commands.py`
- `core/python/tests/pack_fixture_support.py`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
