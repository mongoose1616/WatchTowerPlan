#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./tools/verify.sh <fast|all> [--pack <pack_slug>] [--fail-fast]

Run the canonical local verification flow from core/python.

Modes:
  fast  Shared-core mypy, Ruff, and unit pytest loop.
  all   Broad shared-core pass plus watchtower-core validate all.

Options:
  --pack <pack_slug>  Also run the hosted-pack typing and test pass for one
                      top-level pack root such as "my_pack".
  --fail-fast        Stop pytest-driven validation on the first failure. Use
                     this for faster remediation and refactor loops.
EOF
}

run_step() {
  local label="$1"
  shift
  printf '\n[%s]\n' "$label"
  "$@"
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
workspace_root="$repo_root/core/python"

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

mode="$1"
shift
pack_slug=""
fail_fast=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pack)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --pack" >&2
        exit 2
      fi
      pack_slug="$2"
      shift 2
      ;;
    --fail-fast)
      fail_fast=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

case "$mode" in
  fast|all)
    ;;
  *)
    echo "Unknown mode: $mode" >&2
    usage
    exit 2
    ;;
esac

pack_src=""
pack_tests=""
if [[ -n "$pack_slug" ]]; then
  pack_src="../../$pack_slug/python/src"
  pack_tests="../../$pack_slug/python/tests"
  if [[ ! -d "$repo_root/$pack_slug/python/src" ]]; then
    echo "Pack source root not found: $pack_slug/python/src" >&2
    exit 2
  fi
  if [[ ! -d "$repo_root/$pack_slug/python/tests" ]]; then
    echo "Pack test root not found: $pack_slug/python/tests" >&2
    exit 2
  fi
fi

cd "$workspace_root"

run_step "mypy (core)" uv run mypy src
run_step "ruff (core)" uv run ruff check src tests/unit tests/integration

pytest_args=(-q)
if [[ "$fail_fast" == "1" ]]; then
  pytest_args+=("--maxfail=1")
fi

if [[ "$mode" == "fast" ]]; then
  run_step "pytest (core unit)" uv run pytest "${pytest_args[@]}"
else
  run_step "pytest (core broad)" uv run python -m pytest "${pytest_args[@]}" tests/unit tests/integration
  run_step "validate all" uv run watchtower-core validate all
fi

if [[ -n "$pack_slug" ]]; then
  run_step "mypy ($pack_slug)" uv run mypy src "$pack_src"
  run_step "pytest ($pack_slug)" uv run python -m pytest "${pytest_args[@]}" "$pack_tests"
fi
