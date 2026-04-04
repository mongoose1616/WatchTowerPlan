#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./tools/setup_dev_env.sh [--skip-python-install] [--skip-doctor] [--verify-fast]

Bootstrap or repair the canonical WatchTower Python workspace from core/python.

Options:
  --skip-python-install  Skip `uv python install` before syncing the workspace.
  --skip-doctor          Skip the `watchtower-core doctor` smoke check.
  --verify-fast          Run `./tools/verify.sh fast` after doctor succeeds.
  -h, --help             Show this help text.
EOF
}

print_uv_install_help() {
  cat <<'EOF'

Install uv, then re-run:
  ./tools/setup_dev_env.sh

Common installation options:
  curl -LsSf https://astral.sh/uv/install.sh | sh
  brew install uv
  pipx install uv
EOF
}

run_step() {
  local label="$1"
  shift
  printf '\n[%s]\n' "$label"
  "$@"
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="$(cd "${script_dir}/.." && pwd)"
venv_python="${workspace_root}/.venv/bin/python"
venv_watchtower="${workspace_root}/.venv/bin/watchtower-core"

skip_python_install=0
skip_doctor=0
verify_fast=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-python-install)
      skip_python_install=1
      shift
      ;;
    --skip-doctor)
      skip_doctor=1
      shift
      ;;
    --verify-fast)
      verify_fast=1
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

cd "${workspace_root}"

have_uv=0
if command -v uv >/dev/null 2>&1; then
  have_uv=1
fi

if [[ "${have_uv}" == "1" ]]; then
  if [[ "${skip_python_install}" == "0" ]]; then
    run_step "uv python install" uv python install
  fi
  run_step "uv sync --extra dev" uv sync --extra dev
else
  if [[ ! -x "${venv_python}" ]]; then
    cat <<EOF
uv is not available on PATH and core/python/.venv has not been created yet.

Run this from:
  ${workspace_root}
EOF
    print_uv_install_help
    exit 1
  fi
  echo "uv is not available on PATH; reusing the existing core/python/.venv."
fi

if [[ "${skip_doctor}" == "0" ]]; then
  if [[ "${have_uv}" == "1" ]]; then
    run_step "watchtower-core doctor" uv run watchtower-core doctor
  elif [[ -x "${venv_watchtower}" ]]; then
    run_step "watchtower-core doctor" "${venv_watchtower}" doctor
  else
    cat <<EOF
watchtower-core is not available in core/python/.venv.

Re-run this script after restoring uv on PATH:
  cd ${workspace_root}
  ./tools/setup_dev_env.sh
EOF
    exit 1
  fi
fi

if [[ "${verify_fast}" == "1" ]]; then
  run_step "verify fast" ./tools/verify.sh fast
fi

cat <<EOF

Environment ready.

Canonical daily entrypoints from ${workspace_root}:
  uv run watchtower-core doctor
  uv run pytest -q
  ./.venv/bin/python -m pytest tests/unit tests/integration -q
  ./tools/dev_shell.sh

Agent rule:
  Use uv run ... directly when available.
  If a direct interpreter or tool binary is needed after sync, use ./.venv/bin/python or ./.venv/bin/<tool>.
EOF
