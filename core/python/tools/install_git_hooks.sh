#!/usr/bin/env bash
# Activate the tracked .githooks/ directory for this clone.
# The hooks themselves live in the repository root at .githooks/ and are
# version-controlled.  This script only needs to run once per clone to
# point Git at that directory.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

if [[ ! -f "$repo_root/.githooks/pre-push" ]]; then
  echo "Missing .githooks/pre-push — is the repository checkout complete?" >&2
  exit 1
fi

git -C "$repo_root" config core.hooksPath .githooks

# Clean up legacy config keys from the old verify.sh-based hook.
git -C "$repo_root" config --unset watchtower.verifyMode >/dev/null 2>&1 || true
git -C "$repo_root" config --unset watchtower.verifyPack >/dev/null 2>&1 || true
git -C "$repo_root" config --unset watchtower.verifyFailFast >/dev/null 2>&1 || true

printf 'Activated .githooks/ (core.hooksPath set)\n'
