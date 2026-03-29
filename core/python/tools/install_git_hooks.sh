#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./tools/install_git_hooks.sh [--mode <fast|all>] [--pack <pack_slug>]

Install the repository-local pre-push hook path and configure which
verification mode it should run.
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
mode="fast"
pack_slug=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --mode" >&2
        exit 2
      fi
      mode="$2"
      shift 2
      ;;
    --pack)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --pack" >&2
        exit 2
      fi
      pack_slug="$2"
      shift 2
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

git -C "$repo_root" config core.hooksPath .githooks
git -C "$repo_root" config watchtower.verifyMode "$mode"
if [[ -n "$pack_slug" ]]; then
  git -C "$repo_root" config watchtower.verifyPack "$pack_slug"
else
  git -C "$repo_root" config --unset watchtower.verifyPack >/dev/null 2>&1 || true
fi

printf 'Installed .githooks/pre-push with mode=%s' "$mode"
if [[ -n "$pack_slug" ]]; then
  printf ' pack=%s' "$pack_slug"
fi
printf '\n'
