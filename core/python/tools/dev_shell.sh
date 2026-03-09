#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_root="$(cd "${script_dir}/.." && pwd)"
activate_path="${workspace_root}/.venv/bin/activate"

if [[ ! -f "${activate_path}" ]]; then
  cat <<EOF
core/python/.venv is not available yet.

Run the workspace bootstrap first:
  cd ${workspace_root}
  uv python install
  uv sync --extra dev

Then re-run:
  ./tools/dev_shell.sh
EOF
  exit 1
fi

cd "${workspace_root}"
# shellcheck disable=SC1091
source "${activate_path}"

cat <<EOF
Activated core/python/.venv
Workspace: ${workspace_root}

Inside this shell, run commands directly from the activated environment:
  watchtower-core --help
  watchtower-core doctor
  pytest
  ruff check .
  mypy src

If uv is installed globally, `uv run ...` also works, but it is not required here.

Exit this shell with:
  exit
EOF

exec "${SHELL:-/bin/bash}" -i
