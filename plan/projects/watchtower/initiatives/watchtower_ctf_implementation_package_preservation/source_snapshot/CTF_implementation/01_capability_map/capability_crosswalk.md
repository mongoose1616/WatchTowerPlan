# Capability Crosswalk

## Classification Legend

- `supported_now`: current shared core or host contract already provides the capability directly
- `adaptable_now`: generic current patterns exist, but offensive-security-specific surfaces still must be authored
- `must_develop`: pack-owned capability with no direct upstream implementation
- `conflict_or_extension`: deliberate locked deferral or future extension not needed for the first baseline

## Crosswalk

| Capability Family | Classification | Current Contract Source | Planned Owner |
|---|---|---|---|
| hosted pack root, manifests, bootstrap, validate, export | `supported_now` | shared pack authoring, pack interface, and pack commands | shared core + host |
| canonical CTF workspace path model | `adaptable_now` | current domain-root contract and hosted-pack topology | offensive-security pack |
| core / host / pack python boundary | `supported_now` | current boundary standard and package READMEs | shared core + host |
| workflow routing, route preview, workflow metadata registry | `supported_now` | shared route/index metadata model | shared core + pack workflow docs |
| shared governance surfaces (`governance_surface_map`, `path_pattern_registry`, `status_registry`, `actor_registry`) | `supported_now` | current shared control-plane registries and typed schemas | shared core, adopted by pack |
| challenge lifecycle, `.wt_local`, closeout semantics | `must_develop` | none upstream beyond generic patterns | offensive-security pack |
| pack schemas, ledgers, discrepancy records, artifact index | `adaptable_now` | generic schema and validation patterns | offensive-security pack |
| pack query runtime and pack sync runtime | `supported_now` for hook points, `must_develop` for content | integration descriptor contract | offensive-security pack |
| document-semantics validation for pack-owned docs | `adaptable_now` | current pack-owned validation service pattern | offensive-security pack |
| knowledge taxonomy, promotion, retrieval ranking | `must_develop` | no offensive-security corpus upstream | offensive-security pack |
| environment adapters and operating modes | `must_develop` | pack-owned by boundary | offensive-security pack |
| safety taxonomy, confirmation gates, audit rules | `must_develop` | no offensive-security safety model upstream | offensive-security pack |
| workflow catalog | `conflict_or_extension` | not required by live contract | locked post-v1 deferral |
| public rebuild CLI split from sync | `conflict_or_extension` | reusable rebuild primitives exist but public CLI still centers sync | locked post-v1 deferral |

## Implementation Rule

Default to reusing current shared surfaces exactly where they already exist. Only create pack-owned surfaces when the domain semantics are genuinely offensive-security-specific.
