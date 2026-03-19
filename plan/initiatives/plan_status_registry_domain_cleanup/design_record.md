# Plan Status Registry Domain Cleanup Design Record

## Summary
Removes legacy challenge-specific status leakage from the shared status registry and reconciles the authoritative requirements notes to the current pack-facing interface state.

## Design Boundary
- The shared status registry should stay generic enough for pack-facing validation and lookup, so the cleanup should remove challenge-specific language without replacing it with plan-only jargon.
- Existing pack-local lifecycle and review registries already own the richer plan-specific execution vocabulary, so this slice should not duplicate those semantics in the shared registry.
- Focused tests should prove the cleaned status values and allowed-family bindings through the current typed load path rather than through ad hoc JSON assertions alone.
