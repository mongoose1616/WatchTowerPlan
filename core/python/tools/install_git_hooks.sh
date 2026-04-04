#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./tools/install_git_hooks.sh [--mode <fast|all>] [--pack <pack_slug>] [--fail-fast]

Install the repository-local pre-push hook path and configure which
verification mode it should run.
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
hook_template_root="$repo_root/core/python/tools/git_hooks"
hook_root="$repo_root/.githooks"
mode="fast"
pack_slug=""
fail_fast=0

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

if [[ ! -f "$hook_template_root/README.md" || ! -f "$hook_template_root/pre-push" ]]; then
  echo "Missing shared git hook templates under $hook_template_root" >&2
  exit 1
fi

mkdir -p "$hook_root"
install -m 0644 "$hook_template_root/README.md" "$hook_root/README.md"
install -m 0755 "$hook_template_root/pre-push" "$hook_root/pre-push"

git -C "$repo_root" config core.hooksPath .githooks
git -C "$repo_root" config watchtower.verifyMode "$mode"
if [[ -n "$pack_slug" ]]; then
  git -C "$repo_root" config watchtower.verifyPack "$pack_slug"
else
  git -C "$repo_root" config --unset watchtower.verifyPack >/dev/null 2>&1 || true
fi
if [[ "$fail_fast" == "1" ]]; then
  git -C "$repo_root" config watchtower.verifyFailFast true
else
  git -C "$repo_root" config --unset watchtower.verifyFailFast >/dev/null 2>&1 || true
fi

printf 'Installed .githooks/pre-push with mode=%s' "$mode"
if [[ -n "$pack_slug" ]]; then
  printf ' pack=%s' "$pack_slug"
fi
if [[ "$fail_fast" == "1" ]]; then
  printf ' fail_fast=true'
fi
printf '\n'
