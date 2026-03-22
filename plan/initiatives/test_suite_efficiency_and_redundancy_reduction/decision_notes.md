# Test Suite Efficiency And Redundancy Reduction Decision Notes

## Summary
The repository should pay full end-to-end sync cost only in tests that explicitly verify cross-surface materialization.

## Notes
- Treat a broad suite runtime above roughly half an hour as a real validation usability defect, not as an acceptable cost of coverage.
- Removing redundant tests is preferred over retaining many near-identical CLI envelope checks that duplicate lower-level service coverage.
- Keep at least one real integration path for each heavy flow so performance optimization does not silently hollow out behavioral proof.
- Do not add product-side “test fast path” flags unless a behavior contract genuinely requires a new bounded sync mode.
