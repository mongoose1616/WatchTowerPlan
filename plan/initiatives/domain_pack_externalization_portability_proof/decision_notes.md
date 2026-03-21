# Domain Pack Externalization and Portability Proof Decision Notes

## Summary
This initiative keeps the current core-host-pack split and uses portability proofing to harden it rather than introducing a new runtime layer.

## Locked Decisions
- `watchtower-core` remains the CLI binary.
- `watchtower_core` remains the reusable package namespace.
- `watchtower_host` remains the host-owned composition layer behind the CLI.
- `watchtower_<pack>` remains the only valid pack-native runtime boundary.
- Portability failures must become reusable-core validator failures when possible.

## Expected Follow-Through
- Keep `plan` as the first proof pack.
- Use WatchTowerOversight as a comparison input where it helps validate pack shape and guidance.
- Avoid adding new compatibility layers that would blur the portable pack capsule.
