# Risk Register

| Risk ID | Risk | Impact | Mitigation |
|---|---|---|---|
| `risk.slug_drift` | upstream slug normalization changes current-compatible identity | manifest/runtime mismatch | keep live delta log and treat scaffold-spec baseline as current truth |
| `risk.contract_staleness` | Step 1 workbooks drift from live core | wrong pack plan | always privilege live contract docs and shared registries over older workbook assumptions |
| `risk.unlocked_decisions` | recommended defaults in the implementation gap audit are not locked before coding starts | implementation re-derives core behavior ad hoc | review and lock `open_decisions.json` and `implementation_gap_audit.md` before phase execution |
| `risk.workflow_placeholder` | starter workflow metadata remains in place too long | broken route preview and workflow indexing | make replacement part of immediate next slice |
| `risk.doc_index_drift` | markdown docs and JSON indexes diverge | package becomes untrustworthy | validate JSON parsing and cross-check artifact paths and phase IDs |
| `risk.safety_under_specified` | environment and refusal rules stay vague | unsafe runtime implementation | keep Phase 6 and safety standard explicit and fail closed |
