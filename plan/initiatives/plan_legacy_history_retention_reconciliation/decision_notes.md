# Plan Legacy History and Retention Reconciliation Decision Notes

## Summary
Capture the implementation choices that turn the legacy-history follow-up from a docs-backed reminder into live machine authority.

## Notes
- Keep the first slice policy-focused. The follow-up tranche needs explicit retention authority first; actual purge or migration work can stay bounded to later slices.
- Reuse the existing guarded trace-purge workflow only as a supporting reference. The live plan workspace needs its own machine-readable retention rule under `plan/.wt/**`.
- Treat the legacy `docs/planning/**` corpus as intentionally hidden from live operational queries during the hard-cutover phase, not as an alternate authority surface.
