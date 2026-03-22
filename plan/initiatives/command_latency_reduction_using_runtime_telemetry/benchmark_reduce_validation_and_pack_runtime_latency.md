# Validation And Pack Runtime Latency Reduction

## Summary
- Captured on `2026-03-22T19:38:00Z` after the `reduce_validation_and_pack_runtime_latency` slice.
- The reusable-core validation context now loads only the shared validation surfaces it actually needs instead of materializing every declared pack surface.
- Pack boundary validation now parses each Python module once per package root and reuses the extracted import and `sys.path` mutation facts instead of reparsing the same tree for each boundary rule.
- Validation-suite execution now instantiates the artifact and front-matter services lazily so pack-contract-only runs do not pay for unused validators.

## Command Delta Against Baseline
| Command | Baseline Median (ms) | Current Median (ms) | Improvement (ms) | Improvement (%) |
| --- | ---: | ---: | ---: | ---: |
| `pack validate --pack plan --format json` | `1003.199` | `791.973` | `211.226` | `21.06` |

## Additional Runtime Signal
- `validate all --skip-acceptance --format json` now measured at a `10116.566 ms` median over `5` runs with `WATCHTOWER_TELEMETRY_STDERR=off`.
- In-process service timings moved substantially as well:
  - `PackValidationContext.from_loader`: about `213.014 ms` -> `125.144 ms`
  - `dependency_boundary_issues`: about `356.841 ms` -> `225.073 ms`
  - `PackContractValidationService.validate`: about `562.691 ms` -> `139.349 ms`

## Implementation Notes
- [context.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/context.py) now loads the reusable validation surface subset instead of every declared pack surface.
- [boundaries.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/_pack_contract/boundaries.py) now performs one AST scan per package root and derives the pack-boundary issues from cached module facts.
- [suite.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/suite.py) now initializes artifact and front-matter validation services only if the active suite step kinds need them.

## Remaining Hotspot Shape
- The baseline’s host/parser task still exists in the initiative, but the original hotspot inventory already showed that startup was materially smaller than the plan and validation families.
- The next tranche should focus on deciding whether any host/loader work is still justified after the two larger slices, then add the regression guards and rerun the full benchmark set.

## Notes
- The machine-readable companion for this note is `benchmark_reduce_validation_and_pack_runtime_latency.json`.
- The repo-wide `watchtower-core validate all --skip-acceptance --format json` gate still passed after this slice.
