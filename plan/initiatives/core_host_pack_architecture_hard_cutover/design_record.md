# Core Host Pack Architecture Hard Cutover Design Record

## Summary
Separates reusable core, host composition, and pack-native runtime behind governed pack contracts, host-owned CLI composition, and pack interface validation.

## Initial Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
