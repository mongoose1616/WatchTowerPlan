# Target Repo Bootstrap Guide

## Goal

Move shared core from `/home/j/WatchTowerPlan/core` into `/home/j/WatchTower`, then bootstrap the offensive-security pack there through the canonical export and bootstrap flow.

## Sequence

1. export shared core from the donor repository using `watchtower-core pack export`;
2. copy the staged export into `/home/j/WatchTower`;
3. create or scaffold `offensive_security/` in the recipient repo;
4. run `watchtower-core pack bootstrap --replace-hosted-packs --write` in the recipient repo if donor pack wiring must be replaced;
5. run `pack validate`, `validate all`, and changed-schema validation;
6. run `pack export` or `release check` for the intended handoff mode.

## Rules

- do not manually copy donor `.venv`, caches, or runtime residue;
- do not treat bootstrap as a release scrub;
- do not treat pack-only output as a standalone repository.
