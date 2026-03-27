# Core Export And Target Bootstrap Plan

## Donor Export

Use the existing export flow from `/home/j/WatchTowerPlan/core` as the canonical shared-core handoff path.

```sh
cd /home/j/WatchTowerPlan/core/python
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack export \
  --output-root /tmp/watchtower_ctf_core_export \
  --overwrite \
  --format json
```

## Copy Into Target Repo

1. copy the staged export root into `/home/j/WatchTower`;
2. confirm `core/` now exists in `/home/j/WatchTower`;
3. author or scaffold `offensive_security/` in the copied repository, not in the donor repo.

## Recipient Bootstrap

In `/home/j/WatchTower/core/python`:

```sh
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack bootstrap \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --replace-hosted-packs \
  --write \
  --format json
```

Use `--replace-hosted-packs` if donor hosted-pack wiring must be scrubbed and replaced by the recipient pack.

## Recipient Validation

```sh
PATH="$HOME/.local/bin:$PATH" uv run watchtower-core pack validate \
  --pack-settings-path offensive_security/.wt/manifests/pack_settings.json \
  --format json

PATH="$HOME/.local/bin:$PATH" uv run watchtower-core validate all --format json
```

Run `validate schema --path <schema>` for every changed schema file.

## Release And Portability Proof

Choose one mode explicitly:

- core-only bundle
- core plus selected pack bundle
- pack-only bundle

Do not treat a raw repo copy as the deliverable. Use `pack export` or `release check` for the final staged artifact.
